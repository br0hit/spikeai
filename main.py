from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.graph import WorkFlowManager

app = FastAPI()

# Initialize the Graph (Single instance loaded on startup)
workflow_manager = WorkFlowManager()

class QueryRequest(BaseModel):
    query: str
    propertyId: Optional[str] = None

@app.post("/query")
async def handle_query(request: QueryRequest):
    print(f"📩 Received: {request.query}")
    
    try:
        # Run the LangGraph Workflow
        result = workflow_manager.process_query(
            query=request.query,
            property_id=request.propertyId
        )
        
        # Return strict JSON if the result contains it, otherwise natural language
        # (The hackathon requires specific JSON output sometimes, handled by agent logic)
        return result["answer"]
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": "Internal server error processing request."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}