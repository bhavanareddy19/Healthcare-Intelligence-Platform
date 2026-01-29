"""
Healthcare Intelligence Platform - Document Processor
Handles multi-format document ingestion and text extraction
"""

import io
from typing import List, Optional, Union
from pathlib import Path
from loguru import logger

from .text_cleaner import TextCleaner
from .chunker import DocumentChunker


class DocumentProcessor:
    """
    Multi-format document processor for clinical documents.
    
    Supports:
    - PDF files (using PyMuPDF)
    - Plain text files
    - Word documents (DOCX)
    """
    
    def __init__(self):
        self.text_cleaner = TextCleaner()
        self.chunker = DocumentChunker()
    
    def process(self, content: bytes, file_extension: str) -> str:
        """
        Process document content and extract text.
        
        Args:
            content: Raw file bytes
            file_extension: File extension (.pdf, .txt, .docx)
            
        Returns:
            Extracted and cleaned text content
        """
        logger.debug(f"Processing document with extension: {file_extension}")
        
        if file_extension == ".pdf":
            text = self._extract_pdf(content)
        elif file_extension == ".txt":
            text = self._extract_text(content)
        elif file_extension == ".docx":
            text = self._extract_docx(content)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        # Clean the extracted text
        cleaned_text = self.text_cleaner.clean(text)
        
        logger.debug(f"Extracted {len(cleaned_text)} characters")
        return cleaned_text
    
    def _extract_pdf(self, content: bytes) -> str:
        """Extract text from PDF using PyMuPDF."""
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(stream=content, filetype="pdf")
            text_parts = []
            
            for page_num, page in enumerate(doc):
                text = page.get_text()
                if text.strip():
                    text_parts.append(f"[Page {page_num + 1}]\n{text}")
            
            doc.close()
            return "\n\n".join(text_parts)
            
        except ImportError:
            logger.warning("PyMuPDF not installed, trying pdfplumber")
            return self._extract_pdf_fallback(content)
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            return self._extract_pdf_fallback(content)
    
    def _extract_pdf_fallback(self, content: bytes) -> str:
        """Fallback PDF extraction using pdfplumber."""
        try:
            import pdfplumber
            
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                text_parts = []
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text() or ""
                    if text.strip():
                        text_parts.append(f"[Page {page_num + 1}]\n{text}")
                return "\n\n".join(text_parts)
                
        except Exception as e:
            logger.error(f"PDF fallback extraction error: {e}")
            raise ValueError(f"Could not extract text from PDF: {e}")
    
    def _extract_text(self, content: bytes) -> str:
        """Extract text from plain text file."""
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return content.decode("latin-1")
    
    def _extract_docx(self, content: bytes) -> str:
        """Extract text from Word document."""
        try:
            from docx import Document as DocxDocument
            
            doc = DocxDocument(io.BytesIO(content))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n\n".join(paragraphs)
            
        except Exception as e:
            logger.error(f"DOCX extraction error: {e}")
            raise ValueError(f"Could not extract text from DOCX: {e}")
    
    def chunk_text(
        self,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> List[str]:
        """
        Split text into overlapping chunks for embedding.
        
        Args:
            text: Full text content
            chunk_size: Target chunk size in characters
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        return self.chunker.chunk(text, chunk_size, chunk_overlap)
    
    def process_file(self, file_path: Union[str, Path]) -> str:
        """
        Process a file from disk.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Extracted and cleaned text
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, "rb") as f:
            content = f.read()
        
        return self.process(content, file_path.suffix.lower())
