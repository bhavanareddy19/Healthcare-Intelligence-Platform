"""
Healthcare Intelligence Platform - Agent Orchestrator
Multi-agent coordination and execution
"""

import asyncio
from typing import List, Dict, Any, Optional
from loguru import logger

from .base_agent import (
    BaseAgent,
    DiagnosisAgent,
    RiskFactorAgent,
    QualityMeasureAgent,
    ICDCodeAgent,
    HEDISAgent,
    MedicationAgent,
    LabResultsAgent,
    SummaryAgent,
    ComplianceAgent,
    PatientHistoryAgent,
    TreatmentAgent,
    DocQualityAgent,
    AlertAgent,
    ReportAgent
)
from llm.rag_pipeline import RAGPipeline


class AgentOrchestrator:
    """
    Multi-agent orchestrator for clinical analysis.
    
    Coordinates 15 specialized agents to analyze clinical documents,
    managing parallel execution and result aggregation.
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # Initialize all agents
        self.agents: Dict[str, BaseAgent] = {
            "diagnosis": DiagnosisAgent(),
            "risk_factors": RiskFactorAgent(),
            "quality_measures": QualityMeasureAgent(),
            "icd_codes": ICDCodeAgent(),
            "hedis": HEDISAgent(),
            "medications": MedicationAgent(),
            "lab_results": LabResultsAgent(),
            "summary": SummaryAgent(),
            "compliance": ComplianceAgent(),
            "patient_history": PatientHistoryAgent(),
            "treatment": TreatmentAgent(),
            "doc_quality": DocQualityAgent(),
            "alerts": AlertAgent(),
            "report": ReportAgent()
        }
        
        self.rag_pipeline = RAGPipeline()
        self._initialized = True
        
        logger.info(f"🤖 Orchestrator initialized with {len(self.agents)} agents")
    
    async def run_analysis(
        self,
        text: str,
        agents: Optional[List[str]] = None,
        parallel: bool = True
    ) -> Dict[str, Any]:
        """
        Run multi-agent analysis on clinical text.
        
        Args:
            text: Clinical text to analyze
            agents: Optional list of specific agents to run (None = all)
            parallel: Whether to run agents in parallel
            
        Returns:
            Combined analysis results
        """
        # Determine which agents to run
        if agents:
            selected_agents = {
                k: v for k, v in self.agents.items() 
                if k in agents
            }
        else:
            selected_agents = self.agents
        
        logger.info(f"🚀 Running analysis with {len(selected_agents)} agents")
        
        # Execute agents
        if parallel:
            results = await self._run_parallel(text, selected_agents)
        else:
            results = await self._run_sequential(text, selected_agents)
        
        # Generate summary from all results
        summary = await self._generate_summary(results)
        
        return {
            "agent_results": results,
            "summary": summary,
            "agents_executed": len(results)
        }
    
    async def _run_parallel(
        self,
        text: str,
        agents: Dict[str, BaseAgent]
    ) -> List[Dict[str, Any]]:
        """Run agents in parallel for faster execution."""
        tasks = [
            agent.execute(text) 
            for agent in agents.values()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append({
                    "status": "error",
                    "error": str(result)
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _run_sequential(
        self,
        text: str,
        agents: Dict[str, BaseAgent]
    ) -> List[Dict[str, Any]]:
        """Run agents sequentially."""
        results = []
        for name, agent in agents.items():
            result = await agent.execute(text)
            results.append(result)
        return results
    
    async def _generate_summary(
        self,
        results: List[Dict[str, Any]]
    ) -> str:
        """Generate overall summary from agent results."""
        try:
            # Filter successful results
            successful = [r for r in results if r.get("status") == "success"]
            
            if not successful:
                return "No successful agent analyses to summarize."
            
            summary = await self.rag_pipeline.summarize_findings(successful)
            return summary
            
        except Exception as e:
            logger.error(f"Summary generation error: {e}")
            return "Summary generation failed. Please review individual agent outputs."
    
    def get_agent_info(self) -> List[Dict[str, str]]:
        """Get information about all available agents."""
        return [
            {
                "id": agent_id,
                "name": agent.name,
                "description": agent.description
            }
            for agent_id, agent in self.agents.items()
        ]
    
    async def run_single_agent(
        self,
        text: str,
        agent_id: str
    ) -> Dict[str, Any]:
        """
        Run a single specific agent.
        
        Args:
            text: Clinical text to analyze
            agent_id: ID of the agent to run
            
        Returns:
            Agent analysis result
        """
        if agent_id not in self.agents:
            return {
                "status": "error",
                "error": f"Unknown agent: {agent_id}"
            }
        
        return await self.agents[agent_id].execute(text)
    
    async def run_workflow(
        self,
        text: str,
        workflow: str = "standard"
    ) -> Dict[str, Any]:
        """
        Run a predefined analysis workflow.
        
        Workflows:
        - standard: All agents
        - quick: Essential agents only
        - coding: Diagnosis and ICD coding
        - quality: Quality and compliance focus
        
        Args:
            text: Clinical text
            workflow: Workflow name
            
        Returns:
            Workflow results
        """
        workflows = {
            "standard": None,  # All agents
            "quick": ["diagnosis", "medications", "summary", "alerts"],
            "coding": ["diagnosis", "icd_codes", "risk_factors", "hedis"],
            "quality": ["quality_measures", "hedis", "compliance", "doc_quality"]
        }
        
        if workflow not in workflows:
            return {
                "status": "error",
                "error": f"Unknown workflow: {workflow}"
            }
        
        agents = workflows[workflow]
        return await self.run_analysis(text, agents=agents)
