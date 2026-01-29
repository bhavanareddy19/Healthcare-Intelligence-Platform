"""
Healthcare Intelligence Platform - Text Cleaner
Medical text normalization and preprocessing
"""

import re
from typing import Dict, List, Optional
from loguru import logger


class TextCleaner:
    """
    Medical text cleaner and normalizer.
    
    Handles:
    - Whitespace normalization
    - Medical abbreviation expansion
    - Section header detection
    - PHI/PII pattern detection (for awareness, not removal in this implementation)
    """
    
    # Common medical abbreviations
    MEDICAL_ABBREVIATIONS: Dict[str, str] = {
        "pt": "patient",
        "pts": "patients",
        "dx": "diagnosis",
        "hx": "history",
        "tx": "treatment",
        "rx": "prescription",
        "sx": "symptoms",
        "fx": "fracture",
        "bx": "biopsy",
        "cx": "culture",
        "d/c": "discharge",
        "f/u": "follow-up",
        "s/p": "status post",
        "w/": "with",
        "w/o": "without",
        "c/o": "complains of",
        "h/o": "history of",
        "r/o": "rule out",
        "sob": "shortness of breath",
        "cp": "chest pain",
        "bp": "blood pressure",
        "hr": "heart rate",
        "rr": "respiratory rate",
        "temp": "temperature",
        "wbc": "white blood cell count",
        "rbc": "red blood cell count",
        "hgb": "hemoglobin",
        "hct": "hematocrit",
        "plt": "platelets",
        "bmp": "basic metabolic panel",
        "cmp": "comprehensive metabolic panel",
        "cbc": "complete blood count",
        "ua": "urinalysis",
        "ekg": "electrocardiogram",
        "ecg": "electrocardiogram",
        "cxr": "chest x-ray",
        "ct": "computed tomography",
        "mri": "magnetic resonance imaging",
        "us": "ultrasound",
        "icu": "intensive care unit",
        "ed": "emergency department",
        "er": "emergency room",
        "or": "operating room",
        "pacu": "post-anesthesia care unit",
        "npo": "nothing by mouth",
        "prn": "as needed",
        "bid": "twice daily",
        "tid": "three times daily",
        "qid": "four times daily",
        "qd": "once daily",
        "qhs": "at bedtime",
        "ac": "before meals",
        "pc": "after meals",
        "po": "by mouth",
        "iv": "intravenous",
        "im": "intramuscular",
        "sq": "subcutaneous",
        "yo": "years old",
        "y/o": "years old",
        "m": "male",
        "f": "female",
        "htn": "hypertension",
        "dm": "diabetes mellitus",
        "cad": "coronary artery disease",
        "chf": "congestive heart failure",
        "copd": "chronic obstructive pulmonary disease",
        "ckd": "chronic kidney disease",
        "esrd": "end-stage renal disease",
        "uti": "urinary tract infection",
        "uri": "upper respiratory infection",
        "osa": "obstructive sleep apnea",
        "gerd": "gastroesophageal reflux disease",
        "dvt": "deep vein thrombosis",
        "pe": "pulmonary embolism",
        "cva": "cerebrovascular accident",
        "tia": "transient ischemic attack",
        "mi": "myocardial infarction",
        "afib": "atrial fibrillation",
        "a-fib": "atrial fibrillation",
    }
    
    # Section headers commonly found in clinical notes
    SECTION_HEADERS = [
        "CHIEF COMPLAINT",
        "HISTORY OF PRESENT ILLNESS",
        "HPI",
        "PAST MEDICAL HISTORY",
        "PMH",
        "PAST SURGICAL HISTORY",
        "PSH",
        "MEDICATIONS",
        "ALLERGIES",
        "SOCIAL HISTORY",
        "FAMILY HISTORY",
        "REVIEW OF SYSTEMS",
        "ROS",
        "PHYSICAL EXAMINATION",
        "PHYSICAL EXAM",
        "VITAL SIGNS",
        "LABORATORY",
        "LABS",
        "IMAGING",
        "RADIOLOGY",
        "ASSESSMENT",
        "PLAN",
        "ASSESSMENT AND PLAN",
        "A/P",
        "DISCHARGE DIAGNOSIS",
        "DISCHARGE MEDICATIONS",
        "DISCHARGE INSTRUCTIONS",
        "FOLLOW UP",
    ]
    
    def __init__(self, expand_abbreviations: bool = False):
        """
        Initialize text cleaner.
        
        Args:
            expand_abbreviations: Whether to expand medical abbreviations
        """
        self.expand_abbreviations = expand_abbreviations
    
    def clean(self, text: str) -> str:
        """
        Clean and normalize clinical text.
        
        Args:
            text: Raw text content
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = self._normalize_whitespace(text)
        
        # Normalize section headers
        text = self._normalize_sections(text)
        
        # Optionally expand abbreviations
        if self.expand_abbreviations:
            text = self._expand_abbreviations(text)
        
        # Remove special characters that might interfere with processing
        text = self._clean_special_chars(text)
        
        return text.strip()
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace in text."""
        # Replace multiple spaces with single space
        text = re.sub(r" +", " ", text)
        
        # Replace multiple newlines with double newline
        text = re.sub(r"\n{3,}", "\n\n", text)
        
        # Remove trailing whitespace from lines
        text = "\n".join(line.rstrip() for line in text.split("\n"))
        
        return text
    
    def _normalize_sections(self, text: str) -> str:
        """Normalize section headers for consistent formatting."""
        for header in self.SECTION_HEADERS:
            # Match header with optional colon and make it consistent
            pattern = rf"(?i)^({re.escape(header)})\s*:?\s*$"
            replacement = f"\n\n### {header}\n"
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
        
        return text
    
    def _expand_abbreviations(self, text: str) -> str:
        """Expand common medical abbreviations."""
        for abbrev, expansion in self.MEDICAL_ABBREVIATIONS.items():
            # Match abbreviation with word boundaries
            pattern = rf"\b{re.escape(abbrev)}\b"
            text = re.sub(pattern, expansion, text, flags=re.IGNORECASE)
        
        return text
    
    def _clean_special_chars(self, text: str) -> str:
        """Remove or replace problematic special characters."""
        # Replace smart quotes with regular quotes
        text = text.replace(""", '"').replace(""", '"')
        text = text.replace("'", "'").replace("'", "'")
        
        # Remove null bytes and other control characters
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
        
        return text
    
    def detect_phi_patterns(self, text: str) -> List[Dict[str, str]]:
        """
        Detect potential PHI/PII patterns in text.
        
        Note: This is for awareness/logging only. In production,
        proper PHI detection and de-identification would be required.
        
        Args:
            text: Text to scan
            
        Returns:
            List of detected patterns with type and location
        """
        patterns = []
        
        # SSN pattern
        ssn_matches = re.finditer(r"\b\d{3}-\d{2}-\d{4}\b", text)
        for match in ssn_matches:
            patterns.append({
                "type": "SSN",
                "start": match.start(),
                "end": match.end()
            })
        
        # Phone number pattern
        phone_matches = re.finditer(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", text)
        for match in phone_matches:
            patterns.append({
                "type": "phone",
                "start": match.start(),
                "end": match.end()
            })
        
        # Email pattern
        email_matches = re.finditer(r"\b[\w.-]+@[\w.-]+\.\w+\b", text)
        for match in email_matches:
            patterns.append({
                "type": "email",
                "start": match.start(),
                "end": match.end()
            })
        
        # Date patterns (various formats)
        date_matches = re.finditer(
            r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{2}[/-]\d{2}\b",
            text
        )
        for match in date_matches:
            patterns.append({
                "type": "date",
                "start": match.start(),
                "end": match.end()
            })
        
        if patterns:
            logger.warning(f"Detected {len(patterns)} potential PHI patterns")
        
        return patterns
