import pandas as pd
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from src.state import AgentState
from src.services.seo_data import SEODataService
import traceback

class SEOAgent:
    def __init__(self, llm_client: ChatOpenAI):
        self.llm = llm_client
        self.data_service = SEODataService()

    def run(self, state: AgentState) -> AgentState:
        """
        Main entry point for the SEO Agent node.
        """
        print(f"🕵️ SEO Agent processing: {state.user_query}")
        
        # 1. Fetch Live Data
        df = self.data_service.fetch_live_data()
        if df.empty:
            state.final_response = "I couldn't retrieve the SEO data at this time."
            return state

        # 2. Get Schema (Dynamic handling)
        schema_info = self.data_service.get_schema_info(df)
        state.data_schema = schema_info

        # 3. Generate Analysis Code via LLM
        # We ask the LLM to write a pandas query based on the schema
        code = self._generate_pandas_code(state.user_query, schema_info)
        state.generated_python_code = code

        # 4. Execute Code (Safe-ish Execution)
        # Note: In a real production env, use a sandboxed E2B env. 
        # For Hackathon, 'exec' with local variables is standard but risky.
        try:
            local_vars = {"df": df, "pd": pd, "result": None}
            exec(code, {}, local_vars)
            execution_result = local_vars.get("result", "No result variable set")
            state.execution_result = str(execution_result)
            
            # 5. Synthesize Natural Language Answer
            final_answer = self._synthesize_answer(state.user_query, str(execution_result))
            state.final_response = final_answer
            
        except Exception as e:
            error_msg = f"Error executing analysis: {str(e)}\nTrace: {traceback.format_exc()}"
            print(error_msg)
            state.final_response = "I encountered an error trying to analyze the data."
            state.execution_result = error_msg

        return state

    def _generate_pandas_code(self, query: str, schema: str) -> str:
        """
        Asks the LLM to convert natural language -> Pandas Python code
        """
        prompt = f"""
        You are an expert Python Data Scientist. 
        You have a pandas DataFrame named `df` containing SEO audit data.
        
        Current Schema:
        {schema}

        User Query: "{query}"

        Task: Write Python code to analyze `df` and answer the query.
        
        Rules:
        1. Store the final answer in a variable named `result`.
        2. `result` can be a number, a string, a list, or a string representation of a dataframe.
        3. Do NOT plot graphs.
        4. Handle potential missing values (NaN) gracefully.
        5. Return ONLY the executable Python code. No markdown backticks.
        """
        
        messages = [
            SystemMessage(content="You are a python coding assistant."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        code = response.content.replace("```python", "").replace("```", "").strip()
        return code

    def _synthesize_answer(self, query: str, raw_result: str) -> str:
        """
        Converts the raw data result back into a natural language response.
        """
        prompt = f"""
        User Question: "{query}"
        Analysis Result: {raw_result}

        Please provide a clear, concise natural language answer based on the result.
        If the result is a list of pages, summarize the key findings.
        """
        
        messages = [HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)
        return response.content