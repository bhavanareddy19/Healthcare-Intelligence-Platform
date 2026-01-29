"""
Healthcare Intelligence Platform - Agent Routes
Handles multi-agent clinical analysis execution
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from loguru import logger

from agents.orchestrator import AgentOrchestrator

router = APIRouter()

# Initialize orchestrator
orchestrator = AgentOrchestrator()


class AgentRequest(BaseModel):
    """Agent execution request."""
    document_id: Optional[str] = None
    text: Optional[str] = None
    agents: Optional[List[str]] = None  # Specific agents to run, None = all


class AgentResult(BaseModel):
    """Individual agent result."""
    agent_name: str
    status: str
    output: Dict[str, Any]
    confidence: float
    execution_time_ms: float


class AgentResponse(BaseModel):
    """Complete agent analysis response."""
    analysis_id: str
    status: str
    agents_executed: int
    results: List[AgentResult]
    summary: str
    total_time_ms: float
    timestamp: str


# Store analysis results
analysis_history = {}


@router.post("/analyze", response_model=AgentResponse)
async def run_analysis(request: AgentRequest):
    """
    Run multi-agent clinical analysis on document or text.
    
    Available agents:
    - diagnosis: Extract diagnoses
    - risk_factors: Identify risk factors
    - quality_measures: Map quality measures
    - icd_codes: Extract ICD-10 codes
    - hedis: Check HEDIS compliance
    - medications: Analyze medications
    - lab_results: Interpret lab values
    - summary: Create clinical summary
    - compliance: Check regulatory compliance
    - patient_history: Analyze patient timeline
    - treatment: Evaluate treatment plans
    - doc_quality: Assess documentation quality
    - alerts: Generate clinical alerts
    - report: Generate formatted report
    """
    import time
    start_time = time.time()
    
    if not request.document_id and not request.text:
        raise HTTPException(
            status_code=400,
            detail="Either document_id or text must be provided"
        )
    
    analysis_id = str(uuid.uuid4())
    
    try:
        logger.info(f"🤖 Starting multi-agent analysis: {analysis_id}")
        
        # Get text content
        if request.document_id:
            from app.api.routes.documents import documents_db
            if request.document_id not in documents_db:
                raise HTTPException(status_code=404, detail="Document not found")
            text = documents_db[request.document_id].get("text_preview", "")
        else:
            text = request.text
        
        # Run orchestrator
        results = await orchestrator.run_analysis(
            text=text,
            agents=request.agents
        )
        
        # Format results
        agent_results = [
            AgentResult(
                agent_name=r["agent"],
                status=r["status"],
                output=r["output"],
                confidence=r["confidence"],
                execution_time_ms=r["execution_time_ms"]
            )
            for r in results["agent_results"]
        ]
        
        total_time = (time.time() - start_time) * 1000
        
        response = AgentResponse(
            analysis_id=analysis_id,
            status="completed",
            agents_executed=len(agent_results),
            results=agent_results,
            summary=results.get("summary", ""),
            total_time_ms=round(total_time, 2),
            timestamp=datetime.now().isoformat()
        )
        
        # Store in history
        analysis_history[analysis_id] = response.dict()
        
        logger.info(f"✅ Analysis completed: {len(agent_results)} agents in {total_time:.2f}ms")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@router.get("/agents")
async def list_agents():
    """List all available agents and their descriptions."""
    return {
        "agents": [
            {
                "id": "diagnosis",
                "name": "Diagnosis Extraction Agent",
                "description": "Extracts diagnoses from clinical notes with confidence scores"
            },
            {
                "id": "risk_factors",
                "name": "Risk Factor Identification Agent",
                "description": "Identifies patient risk factors including HCC categories"
            },
            {
                "id": "quality_measures",
                "name": "Quality Measure Mapping Agent",
                "description": "Maps findings to CMS quality measures"
            },
            {
                "id": "icd_codes",
                "name": "ICD Code Extraction Agent",
                "description": "Extracts and suggests ICD-10 codes"
            },
            {
                "id": "hedis",
                "name": "HEDIS Logic Check Agent",
                "description": "Checks HEDIS measure compliance"
            },
            {
                "id": "medications",
                "name": "Medication Analysis Agent",
                "description": "Analyzes medications and checks for interactions"
            },
            {
                "id": "lab_results",
                "name": "Lab Results Interpreter Agent",
                "description": "Interprets laboratory values and identifies abnormals"
            },
            {
                "id": "summary",
                "name": "Clinical Summary Agent",
                "description": "Creates executive clinical summaries"
            },
            {
                "id": "compliance",
                "name": "Compliance Checker Agent",
                "description": "Checks regulatory compliance status"
            },
            {
                "id": "patient_history",
                "name": "Patient History Analyzer Agent",
                "description": "Analyzes patient timeline and history"
            },
            {
                "id": "treatment",
                "name": "Treatment Plan Evaluator Agent",
                "description": "Evaluates and recommends treatment plans"
            },
            {
                "id": "doc_quality",
                "name": "Documentation Quality Agent",
                "description": "Assesses documentation completeness and quality"
            },
            {
                "id": "alerts",
                "name": "Alert Trigger Agent",
                "description": "Generates priority clinical alerts"
            },
            {
                "id": "report",
                "name": "Report Generator Agent",
                "description": "Generates formatted clinical reports"
            }
        ]
    }


@router.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """Get analysis results by ID."""
    if analysis_id not in analysis_history:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis_history[analysis_id]


@router.get("/history")
async def get_analysis_history(limit: int = 10):
    """Get recent analysis history."""
    history = list(analysis_history.values())[-limit:]
    return {
        "total": len(analysis_history),
        "recent": history
    }
