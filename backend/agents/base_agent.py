"""
Healthcare Intelligence Platform - Base Agent
Abstract base class for all clinical agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from loguru import logger
import time

from llm.rag_pipeline import RAGPipeline


class BaseAgent(ABC):
    """
    Abstract base class for clinical analysis agents.
    
    Each agent specializes in a specific type of clinical analysis.
    """
    
    def __init__(self, name: str, description: str):
        """
        Initialize agent.
        
        Args:
            name: Agent name
            description: Agent description
        """
        self.name = name
        self.description = description
        self.rag_pipeline = RAGPipeline()
    
    @property
    @abstractmethod
    def agent_type(self) -> str:
        """Return the agent type identifier."""
        pass
    
    @abstractmethod
    async def analyze(self, text: str) -> Dict[str, Any]:
        """
        Perform analysis on clinical text.
        
        Args:
            text: Clinical text to analyze
            
        Returns:
            Analysis results
        """
        pass
    
    async def execute(self, text: str) -> Dict[str, Any]:
        """
        Execute agent with timing and error handling.
        
        Args:
            text: Clinical text to analyze
            
        Returns:
            Execution results with timing
        """
        start_time = time.time()
        
        try:
            logger.debug(f"🤖 {self.name} starting analysis")
            
            result = await self.analyze(text)
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "agent": self.name,
                "agent_type": self.agent_type,
                "status": "success",
                "output": result.get("output", result),
                "confidence": result.get("confidence", 0.85),
                "execution_time_ms": round(execution_time, 2)
            }
            
        except Exception as e:
            logger.error(f"❌ {self.name} error: {e}")
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "agent": self.name,
                "agent_type": self.agent_type,
                "status": "error",
                "output": {"error": str(e)},
                "confidence": 0.0,
                "execution_time_ms": round(execution_time, 2)
            }
    
    def validate_input(self, text: str) -> bool:
        """Validate input text."""
        if not text or len(text.strip()) < 10:
            return False
        return True


class DiagnosisAgent(BaseAgent):
    """Agent for extracting diagnoses from clinical text."""
    
    def __init__(self):
        super().__init__(
            name="Diagnosis Extraction Agent",
            description="Extracts diagnoses from clinical notes with confidence scores"
        )
    
    @property
    def agent_type(self) -> str:
        return "diagnosis"
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        return await self.rag_pipeline.analyze_with_agent(text, "diagnosis")


class RiskFactorAgent(BaseAgent):
    """Agent for identifying patient risk factors."""
    
    def __init__(self):
        super().__init__(
            name="Risk Factor Identification Agent",
            description="Identifies patient risk factors including HCC categories"
        )
    
    @property
    def agent_type(self) -> str:
        return "risk_factors"
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        return await self.rag_pipeline.analyze_with_agent(text, "risk_factors")


class QualityMeasureAgent(BaseAgent):
    """Agent for mapping to quality measures."""
    
    def __init__(self):
        super().__init__(
            name="Quality Measure Mapping Agent",
            description="Maps findings to CMS quality measures"
        )
    
    @property
    def agent_type(self) -> str:
        return "quality_measures"
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        return await self.rag_pipeline.analyze_with_agent(text, "quality_measures")


class ICDCodeAgent(BaseAgent):
    """Agent for extracting ICD-10 codes."""
    
    def __init__(self):
        super().__init__(
            name="ICD Code Extraction Agent",
            description="Extracts and suggests ICD-10 codes"
        )
    
    @property
    def agent_type(self) -> str:
        return "icd_codes"
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        return await self.rag_pipeline.analyze_with_agent(text, "icd_codes")


class HEDISAgent(BaseAgent):
    """Agent for HEDIS compliance checking."""
    
    def __init__(self):
        super().__init__(
            name="HEDIS Logic Check Agent",
            description="Checks HEDIS measure compliance"
        )
    
    @property
    def agent_type(self) -> str:
        return "hedis"
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        return await self.rag_pipeline.analyze_with_agent(text, "hedis")


class MedicationAgent(BaseAgent):
    """Agent for medication analysis."""
    
    def __init__(self):
        super().__init__(
            name="Medication Analysis Agent",
            description="Analyzes medications and checks for interactions"
        )
    
    @property
    def agent_type(self) -> str:
        return "medications"
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        return await self.rag_pipeline.analyze_with_agent(text, "medications")


class LabResultsAgent(BaseAgent):
    """Agent for lab results interpretation."""
    
    def __init__(self):
        super().__init__(
            name="Lab Results Interpreter Agent",
            description="Interprets laboratory values and identifies abnormals"
        )
    
    @property
    def agent_type(self) -> str:
        return "lab_results"
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        return await self.rag_pipeline.analyze_with_agent(text, "lab_results")


class SummaryAgent(BaseAgent):
    """Agent for creating clinical summaries."""
    
    def __init__(self):
        super().__init__(
            name="Clinical Summary Agent",
            description="Creates executive clinical summaries"
        )
    
    @property
    def agent_type(self) -> str:
        return "summary"
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        return await self.rag_pipeline.analyze_with_agent(text, "summary")


class ComplianceAgent(BaseAgent):
    """Agent for compliance checking."""
    
    def __init__(self):
        super().__init__(
            name="Compliance Checker Agent",
            description="Checks regulatory compliance status"
        )
    
    @property
    def agent_type(self) -> str:
        return "compliance"
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        return await self.rag_pipeline.analyze_with_agent(text, "compliance")


class PatientHistoryAgent(BaseAgent):
    """Agent for patient history analysis."""
    
    def __init__(self):
        super().__init__(
            name="Patient History Analyzer Agent",
            description="Analyzes patient timeline and history"
        )
    
    @property
    def agent_type(self) -> str:
        return "patient_history"
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        return await self.rag_pipeline.analyze_with_agent(text, "patient_history")


class TreatmentAgent(BaseAgent):
    """Agent for treatment plan evaluation."""
    
    def __init__(self):
        super().__init__(
            name="Treatment Plan Evaluator Agent",
            description="Evaluates and recommends treatment plans"
        )
    
    @property
    def agent_type(self) -> str:
        return "treatment"
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        return await self.rag_pipeline.analyze_with_agent(text, "treatment")


class DocQualityAgent(BaseAgent):
    """Agent for documentation quality assessment."""
    
    def __init__(self):
        super().__init__(
            name="Documentation Quality Agent",
            description="Assesses documentation completeness and quality"
        )
    
    @property
    def agent_type(self) -> str:
        return "doc_quality"
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        return await self.rag_pipeline.analyze_with_agent(text, "doc_quality")


class AlertAgent(BaseAgent):
    """Agent for alert generation."""
    
    def __init__(self):
        super().__init__(
            name="Alert Trigger Agent",
            description="Generates priority clinical alerts"
        )
    
    @property
    def agent_type(self) -> str:
        return "alerts"
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        return await self.rag_pipeline.analyze_with_agent(text, "alerts")


class ReportAgent(BaseAgent):
    """Agent for report generation."""
    
    def __init__(self):
        super().__init__(
            name="Report Generator Agent",
            description="Generates formatted clinical reports"
        )
    
    @property
    def agent_type(self) -> str:
        return "report"
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        return await self.rag_pipeline.analyze_with_agent(text, "report")
