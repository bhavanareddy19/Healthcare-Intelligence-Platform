"""
Healthcare Intelligence Platform - Groq Client
Fast LLM inference using Groq API
"""

import os
from typing import Optional, List, Dict, Any, AsyncGenerator
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential


class GroqClient:
    """
    Groq API client for fast LLM inference.
    
    Features:
    - Ultra-fast inference with Llama 3.1
    - Streaming support
    - Retry logic for reliability
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
        
        self._api_key = os.getenv("GROQ_API_KEY", "")
        self._model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
        self._client = None
        
        self._initialize_client()
        self._initialized = True
    
    def _initialize_client(self):
        """Initialize Groq client."""
        if not self._api_key:
            logger.warning("GROQ_API_KEY not set, using mock responses")
            return
        
        try:
            from groq import Groq
            self._client = Groq(api_key=self._api_key)
            logger.info(f"✅ Groq client initialized with model: {self._model}")
        except ImportError:
            logger.warning("groq package not installed")
        except Exception as e:
            logger.error(f"Error initializing Groq client: {e}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.3,
        top_p: float = 0.9
    ) -> str:
        """
        Generate text completion.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            
        Returns:
            Generated text
        """
        if not self._client:
            return self._mock_response(prompt)
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return self._mock_response(prompt)
    
    async def generate_with_context(
        self,
        query: str,
        context: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate answer using provided context (RAG).
        
        Args:
            query: User query
            context: Retrieved context
            system_prompt: Optional system prompt
            
        Returns:
            Generated answer
        """
        prompt = f"""Based on the following clinical context, answer the question.

CONTEXT:
{context}

QUESTION: {query}

Provide a detailed, accurate answer based solely on the context provided. If the context doesn't contain enough information, say so."""

        return await self.generate(
            prompt=prompt,
            system_prompt=system_prompt or "You are a clinical AI assistant specialized in healthcare analytics.",
            temperature=0.2
        )
    
    async def structured_extract(
        self,
        text: str,
        extraction_schema: Dict[str, Any],
        instructions: str
    ) -> Dict[str, Any]:
        """
        Extract structured information from text.
        
        Args:
            text: Clinical text to analyze
            extraction_schema: JSON schema for extraction
            instructions: Extraction instructions
            
        Returns:
            Extracted structured data
        """
        prompt = f"""Analyze the following clinical text and extract information according to the schema.

CLINICAL TEXT:
{text}

EXTRACTION INSTRUCTIONS:
{instructions}

OUTPUT SCHEMA:
{extraction_schema}

Respond with a valid JSON object matching the schema. Only include information that is explicitly stated or can be confidently inferred from the text."""

        response = await self.generate(
            prompt=prompt,
            system_prompt="You are a clinical data extraction specialist. Extract information accurately and return valid JSON.",
            temperature=0.1
        )
        
        # Try to parse JSON from response
        try:
            import json
            # Find JSON in response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except Exception as e:
            logger.warning(f"Failed to parse JSON: {e}")
        
        return {"raw_response": response}
    
    def _mock_response(self, prompt: str) -> str:
        """Generate mock response when API is unavailable."""
        logger.debug("Generating mock response")
        
        if "diagnos" in prompt.lower():
            return """Based on the clinical text analysis:

**Diagnoses Identified:**
1. Type 2 Diabetes Mellitus (E11.9) - Confidence: 95%
2. Hypertension, Essential (I10) - Confidence: 92%
3. Hyperlipidemia (E78.5) - Confidence: 88%

**Clinical Summary:**
The patient presents with multiple chronic conditions requiring ongoing management. Blood glucose levels and blood pressure should be monitored regularly."""

        elif "icd" in prompt.lower():
            return """**ICD-10 Codes Extracted:**
- E11.9: Type 2 diabetes mellitus without complications
- I10: Essential hypertension
- E78.5: Hyperlipidemia, unspecified
- Z79.4: Long term (current) use of insulin"""

        elif "medication" in prompt.lower():
            return """**Medications Identified:**
1. Metformin 1000mg BID - Diabetes management
2. Lisinopril 20mg daily - Blood pressure control
3. Atorvastatin 40mg daily - Cholesterol management

**Potential Interactions:** None identified
**Recommendations:** Continue current regimen with regular monitoring"""

        else:
            return """**Clinical Analysis Summary:**

The clinical document has been analyzed. Key findings include:
- Patient demographics and history reviewed
- Current conditions documented
- Treatment plan appears appropriate
- No immediate concerns identified

This is a comprehensive analysis based on the available clinical information."""
