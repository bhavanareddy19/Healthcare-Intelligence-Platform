"""
Healthcare Intelligence Platform - Medical Prompt Templates
Specialized prompts for clinical NLP tasks
"""

PROMPT_TEMPLATES = {
    "diagnosis_extraction": {
        "system": """You are a clinical NLP specialist trained in medical diagnosis extraction. 
Your task is to identify all diagnoses mentioned in clinical notes with high precision.
Always cite the specific text that supports each diagnosis.""",
        "user": """Extract all diagnoses from the following clinical text.

CLINICAL TEXT:
{text}

For each diagnosis, provide:
1. Diagnosis name
2. ICD-10 code (if determinable)
3. Confidence score (0-100%)
4. Supporting evidence from the text

Format as JSON array."""
    },
    
    "risk_factor_identification": {
        "system": """You are a healthcare risk assessment specialist. 
Identify patient risk factors for chronic diseases, hospitalizations, and adverse events.
Focus on HCC (Hierarchical Condition Categories) relevant factors.""",
        "user": """Identify all risk factors from the following clinical text.

CLINICAL TEXT:
{text}

Categorize risk factors as:
- Demographic (age, gender, etc.)
- Clinical (conditions, lab values)
- Social (smoking, diet, lifestyle)
- Medication-related

Format as JSON with categories."""
    },
    
    "icd_code_extraction": {
        "system": """You are an expert medical coder specializing in ICD-10-CM.
Extract and validate ICD-10 codes from clinical documentation.
Ensure codes are specific and supported by documentation.""",
        "user": """Extract ICD-10-CM codes from the following clinical text.

CLINICAL TEXT:
{text}

For each code provide:
1. ICD-10-CM code
2. Description
3. Specificity level (3-digit, 4-digit, etc.)
4. Documentation supporting the code

Format as JSON array."""
    },
    
    "medication_analysis": {
        "system": """You are a clinical pharmacist AI assistant.
Analyze medications for appropriateness, interactions, and adherence concerns.
Consider patient's diagnoses and lab values when available.""",
        "user": """Analyze medications in the following clinical text.

CLINICAL TEXT:
{text}

Provide:
1. Complete medication list with doses and frequencies
2. Drug-drug interactions (if any)
3. Drug-disease interactions (if any)
4. Adherence concerns
5. Recommendations

Format as JSON."""
    },
    
    "lab_results_interpretation": {
        "system": """You are a clinical laboratory specialist.
Interpret lab values in clinical context.
Identify abnormal values and their clinical significance.""",
        "user": """Interpret laboratory results from the following clinical text.

CLINICAL TEXT:
{text}

For each lab value:
1. Lab test name
2. Value and units
3. Reference range
4. Interpretation (normal/high/low/critical)
5. Clinical significance

Format as JSON array."""
    },
    
    "clinical_summary": {
        "system": """You are a clinical documentation specialist.
Create concise, accurate clinical summaries.
Prioritize clinically relevant information.""",
        "user": """Create a clinical summary from the following text.

CLINICAL TEXT:
{text}

Include:
1. Chief complaint
2. Key history
3. Current diagnoses
4. Treatment plan
5. Follow-up needed

Keep summary under 200 words."""
    },
    
    "quality_measure_mapping": {
        "system": """You are a healthcare quality specialist familiar with CMS quality measures.
Map clinical documentation to applicable quality measures.
Focus on HEDIS, MIPS, and CMS Star measures.""",
        "user": """Identify applicable quality measures for the following clinical text.

CLINICAL TEXT:
{text}

For each measure:
1. Measure ID and name
2. Whether patient meets or gaps criteria
3. Evidence from documentation
4. Recommended actions for gaps

Format as JSON array."""
    },
    
    "hedis_compliance": {
        "system": """You are a HEDIS compliance specialist.
Evaluate documentation for HEDIS measure compliance.
Identify gaps and documentation opportunities.""",
        "user": """Evaluate HEDIS compliance for the following clinical text.

CLINICAL TEXT:
{text}

Check for common HEDIS measures:
- Diabetes care (HbA1c, eye exams, nephropathy)
- Blood pressure control
- Breast/colorectal cancer screening
- Medication adherence

Format as JSON with measure status."""
    },
    
    "compliance_check": {
        "system": """You are a healthcare compliance specialist.
Check documentation for regulatory compliance.
Focus on CMS, HIPAA, and payer requirements.""",
        "user": """Check compliance requirements for the following clinical text.

CLINICAL TEXT:
{text}

Evaluate:
1. Documentation completeness
2. Required elements present
3. Signature/attestation requirements
4. Timely filing indicators

Format as JSON checklist."""
    },
    
    "patient_history_analysis": {
        "system": """You are a clinical historian AI.
Analyze patient history and create comprehensive timelines.
Identify patterns and significant events.""",
        "user": """Analyze patient history from the following clinical text.

CLINICAL TEXT:
{text}

Provide:
1. Chronological timeline of conditions
2. Significant events and procedures
3. Progression patterns
4. Risk trajectory

Format as JSON timeline."""
    },
    
    "treatment_evaluation": {
        "system": """You are a clinical decision support specialist.
Evaluate treatment plans for appropriateness and effectiveness.
Consider evidence-based guidelines.""",
        "user": """Evaluate treatment plan from the following clinical text.

CLINICAL TEXT:
{text}

Assess:
1. Treatment appropriateness for diagnoses
2. Alignment with clinical guidelines
3. Potential improvements
4. Monitoring recommendations

Format as JSON evaluation."""
    },
    
    "documentation_quality": {
        "system": """You are a clinical documentation improvement specialist.
Assess documentation quality and completeness.
Identify opportunities for specificity and accuracy.""",
        "user": """Assess documentation quality for the following clinical text.

CLINICAL TEXT:
{text}

Evaluate:
1. Completeness score (0-100)
2. Specificity score (0-100)
3. Missing elements
4. CDI opportunities

Format as JSON quality report."""
    },
    
    "alert_generation": {
        "system": """You are a clinical alert system.
Identify urgent and important clinical findings.
Prioritize patient safety concerns.""",
        "user": """Generate clinical alerts from the following text.

CLINICAL TEXT:
{text}

Identify:
1. Critical values requiring immediate attention
2. Drug safety concerns
3. Care gap alerts
4. Follow-up reminders

Format as JSON with priority levels (critical/high/medium/low)."""
    },
    
    "report_generation": {
        "system": """You are a clinical report generator.
Create formatted clinical reports from analysis results.
Ensure clarity and actionability.""",
        "user": """Generate a comprehensive clinical report from the following analysis.

ANALYSIS DATA:
{text}

Create a structured report with:
1. Executive summary
2. Key findings
3. Recommendations
4. Action items

Format as markdown."""
    },
    
    "rag_answer": {
        "system": """You are a clinical AI assistant with access to medical knowledge.
Answer questions accurately based on the provided context.
Cite specific information from the context.""",
        "user": """Based on the following context, answer the question.

CONTEXT:
{context}

QUESTION: {query}

Provide a detailed, accurate answer based on the context. If information is insufficient, say so clearly."""
    }
}


def get_prompt(template_name: str, **kwargs) -> tuple:
    """
    Get formatted prompt from template.
    
    Args:
        template_name: Name of the prompt template
        **kwargs: Values to format into the template
        
    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    if template_name not in PROMPT_TEMPLATES:
        raise ValueError(f"Unknown template: {template_name}")
    
    template = PROMPT_TEMPLATES[template_name]
    
    system_prompt = template["system"]
    user_prompt = template["user"].format(**kwargs)
    
    return system_prompt, user_prompt
