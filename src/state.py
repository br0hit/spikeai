from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    """
    The shared state of the application.
    Passes from Orchestrator -> Agent -> Response
    """
    # Input
    user_query: str
    property_id: Optional[str] = None
    
    # Internal Reasoning
    selected_agent: Optional[str] = None # 'seo' or 'analytics'
    
    # Data Context (Populated by Agents)
    data_schema: Optional[str] = None
    generated_python_code: Optional[str] = None
    execution_result: Optional[str] = None
    
    # Output
    final_response: Optional[str] = None
    json_output: Optional[Dict[str, Any]] = None # For strict JSON requirements