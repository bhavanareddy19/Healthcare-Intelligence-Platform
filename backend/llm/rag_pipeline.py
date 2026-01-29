"""
Healthcare Intelligence Platform - RAG Pipeline
Retrieval-Augmented Generation for clinical queries
"""

from typing import Optional, List, Dict, Any
from loguru import logger

from .groq_client import GroqClient
from .prompts import get_prompt


class RAGPipeline:
    """
    RAG pipeline for clinical question answering.
    
    Combines retrieval from vector store with LLM generation
    for accurate, context-aware responses.
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
        
        self.llm = GroqClient()
        self._initialized = True
    
    async def generate_answer(
        self,
        query: str,
        context: str,
        max_context_length: int = 4000
    ) -> str:
        """
        Generate answer using RAG.
        
        Args:
            query: User question
            context: Retrieved context from vector store
            max_context_length: Maximum context length
            
        Returns:
            Generated answer
        """
        # Truncate context if needed
        if len(context) > max_context_length:
            context = context[:max_context_length] + "..."
        
        system_prompt, user_prompt = get_prompt(
            "rag_answer",
            context=context,
            query=query
        )
        
        response = await self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.2
        )
        
        return response
    
    async def analyze_with_agent(
        self,
        text: str,
        agent_type: str
    ) -> Dict[str, Any]:
        """
        Analyze text using a specific agent type.
        
        Args:
            text: Clinical text to analyze
            agent_type: Type of analysis to perform
            
        Returns:
            Analysis results
        """
        import time
        start_time = time.time()
        
        # Map agent types to prompt templates
        agent_template_map = {
            "diagnosis": "diagnosis_extraction",
            "risk_factors": "risk_factor_identification",
            "icd_codes": "icd_code_extraction",
            "medications": "medication_analysis",
            "lab_results": "lab_results_interpretation",
            "summary": "clinical_summary",
            "quality_measures": "quality_measure_mapping",
            "hedis": "hedis_compliance",
            "compliance": "compliance_check",
            "patient_history": "patient_history_analysis",
            "treatment": "treatment_evaluation",
            "doc_quality": "documentation_quality",
            "alerts": "alert_generation",
            "report": "report_generation"
        }
        
        template_name = agent_template_map.get(agent_type)
        if not template_name:
            return {
                "error": f"Unknown agent type: {agent_type}",
                "status": "error"
            }
        
        try:
            system_prompt, user_prompt = get_prompt(template_name, text=text)
            
            response = await self.llm.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.2
            )
            
            execution_time = (time.time() - start_time) * 1000
            
            # Try to parse as JSON
            parsed_output = self._parse_response(response)
            
            return {
                "status": "success",
                "output": parsed_output,
                "raw_response": response,
                "execution_time_ms": round(execution_time, 2)
            }
            
        except Exception as e:
            logger.error(f"Agent analysis error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "execution_time_ms": (time.time() - start_time) * 1000
            }
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response, attempting JSON extraction. Always returns a dict."""
        import json

        # Try to find JSON in response
        try:
            # Look for JSON array
            if "[" in response and "]" in response:
                start = response.find("[")
                end = response.rfind("]") + 1
                parsed = json.loads(response[start:end])
                # Wrap list in dict to ensure consistent output type
                if isinstance(parsed, list):
                    return {"items": parsed, "count": len(parsed)}
                return parsed

            # Look for JSON object
            if "{" in response and "}" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                parsed = json.loads(response[start:end])
                if isinstance(parsed, dict):
                    return parsed
                return {"data": parsed}

        except json.JSONDecodeError:
            pass

        # Return as text if not JSON
        return {"text": response}
    
    async def multi_query_rag(
        self,
        queries: List[str],
        context: str
    ) -> List[str]:
        """
        Run RAG for multiple queries against the same context.
        
        Args:
            queries: List of questions
            context: Shared context
            
        Returns:
            List of answers
        """
        answers = []
        for query in queries:
            answer = await self.generate_answer(query, context)
            answers.append(answer)
        return answers
    
    async def summarize_findings(
        self,
        findings: List[Dict[str, Any]]
    ) -> str:
        """
        Summarize multiple agent findings into a cohesive summary.
        
        Args:
            findings: List of agent results
            
        Returns:
            Summary text
        """
        # Format findings for summarization
        findings_text = "\n\n".join([
            f"**{f.get('agent', 'Unknown')}:**\n{f.get('output', {})}"
            for f in findings
        ])
        
        prompt = f"""Synthesize the following clinical analysis findings into a cohesive executive summary.

FINDINGS:
{findings_text}

Create a concise summary (under 300 words) highlighting:
1. Key diagnoses and conditions
2. Risk factors and concerns
3. Recommended actions
4. Priority items"""

        response = await self.llm.generate(
            prompt=prompt,
            system_prompt="You are a clinical summarization specialist.",
            temperature=0.3
        )
        
        return response
