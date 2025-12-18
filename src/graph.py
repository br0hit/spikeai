import os
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from src.state import AgentState
from src.agents.seo import SEOAgent
from dotenv import load_dotenv

load_dotenv()

class WorkFlowManager:
    def __init__(self):
        # Configure LiteLLM (Proxy)
        self.llm = ChatOpenAI(
            model="gemini-2.5-flash", # Or 'gemini-1.5-pro'
            api_key=os.getenv("LITELLM_KEY"),
            base_url="http://3.110.18.218", # LiteLLM Proxy URL
            temperature=0
        )
        
        # Initialize Agents
        self.seo_agent = SEOAgent(self.llm)
        
        # Build Graph
        self.app = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        # Nodes
        workflow.add_node("router", self._route_query)
        workflow.add_node("seo_agent", self.seo_agent.run)
        
        # Edges
        workflow.set_entry_point("router")
        
        # Conditional Edge based on router output
        workflow.add_conditional_edges(
            "router",
            lambda state: state.selected_agent,
            {
                "seo": "seo_agent",
                "analytics": END, # Placeholder for Tier 1
                "unknown": END
            }
        )
        
        workflow.add_edge("seo_agent", END)
        
        return workflow.compile()

    def _route_query(self, state: AgentState) -> AgentState:
        """
        Orchestrator Logic: Decides which agent handles the query.
        For now, if no propertyId is present, we assume SEO.
        """
        print(f"🧠 Orchestrator routing: {state.user_query}")
        
        # Simple Heuristic for now (Tier 2 focus)
        # In Tier 3, we will use the LLM to decide this.
        if state.property_id:
            # If propertyId is present, it's likely GA4 (Tier 1)
            # For now, we don't have that agent, so we mark unknown or handle purely SEO
            print("Detected GA4 Property ID - Routing logic to be expanded.")
            state.selected_agent = "unknown" 
        else:
            # Default to SEO for Tier 2 evaluation
            state.selected_agent = "seo"
            
        return state
    
    def process_query(self, query: str, property_id: str = None) -> dict:
        """
        Main public method to run the flow.
        """
        initial_state = AgentState(user_query=query, property_id=property_id)
        final_state = self.app.invoke(initial_state)
        return {
            "answer": final_state.get("final_response", "No response generated"),
            "agent": final_state.get("selected_agent"),
            "execution_details": final_state.get("execution_result") # For debugging
        }