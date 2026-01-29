"""
Healthcare Intelligence Platform - Document Chunker
Intelligent text chunking for embedding and retrieval
"""

import re
from typing import List, Optional, Tuple
from loguru import logger


class DocumentChunker:
    """
    Intelligent document chunker for clinical text.
    
    Features:
    - Semantic-aware chunking (respects section boundaries)
    - Overlapping chunks for context preservation
    - Configurable chunk sizes
    """
    
    # Section patterns to preserve
    SECTION_PATTERNS = [
        r"^###\s+",  # Markdown headers
        r"^[A-Z][A-Z\s]+:\s*$",  # ALL CAPS headers
        r"^\d+\.\s+",  # Numbered sections
    ]
    
    def __init__(self):
        self.section_regex = re.compile(
            "|".join(self.SECTION_PATTERNS),
            re.MULTILINE
        )
    
    def chunk(
        self,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separator: str = "\n\n"
    ) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Full text to chunk
            chunk_size: Target size for each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
            separator: Primary separator to split on
            
        Returns:
            List of text chunks
        """
        if not text or len(text) <= chunk_size:
            return [text] if text else []
        
        # First, try to split on natural boundaries
        chunks = self._semantic_split(text, chunk_size, chunk_overlap, separator)
        
        # If semantic split fails or produces too few chunks, fall back to character split
        if len(chunks) <= 1 and len(text) > chunk_size:
            chunks = self._character_split(text, chunk_size, chunk_overlap)
        
        # Post-process chunks
        chunks = self._clean_chunks(chunks)
        
        logger.debug(f"Created {len(chunks)} chunks from {len(text)} characters")
        
        return chunks
    
    def _semantic_split(
        self,
        text: str,
        chunk_size: int,
        chunk_overlap: int,
        separator: str
    ) -> List[str]:
        """Split text on semantic boundaries."""
        # Split on separator
        segments = text.split(separator)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for segment in segments:
            segment_size = len(segment)
            
            # If adding this segment would exceed chunk size
            if current_size + segment_size > chunk_size and current_chunk:
                # Save current chunk
                chunk_text = separator.join(current_chunk)
                chunks.append(chunk_text)
                
                # Start new chunk with overlap
                overlap_text = self._get_overlap(current_chunk, chunk_overlap, separator)
                current_chunk = [overlap_text] if overlap_text else []
                current_size = len(overlap_text) if overlap_text else 0
            
            # Add segment to current chunk
            current_chunk.append(segment)
            current_size += segment_size + len(separator)
        
        # Don't forget the last chunk
        if current_chunk:
            chunks.append(separator.join(current_chunk))
        
        return chunks
    
    def _character_split(
        self,
        text: str,
        chunk_size: int,
        chunk_overlap: int
    ) -> List[str]:
        """Fall back to character-based splitting."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to find a good breaking point
            if end < len(text):
                # Look for sentence end
                best_break = self._find_best_break(text, start, end)
                if best_break:
                    end = best_break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start, accounting for overlap
            start = end - chunk_overlap
            if start <= 0:
                start = end
        
        return chunks
    
    def _find_best_break(
        self,
        text: str,
        start: int,
        end: int,
        search_window: int = 200
    ) -> Optional[int]:
        """Find a good breaking point near the target end position."""
        search_start = max(start, end - search_window)
        search_text = text[search_start:end + 50]  # Look a bit past end too
        
        # Priority: paragraph > sentence > word
        
        # Look for paragraph break
        para_match = list(re.finditer(r"\n\n", search_text))
        if para_match:
            return search_start + para_match[-1].end()
        
        # Look for sentence end
        sent_match = list(re.finditer(r"[.!?]\s+", search_text))
        if sent_match:
            return search_start + sent_match[-1].end()
        
        # Look for word boundary
        word_match = list(re.finditer(r"\s+", search_text))
        if word_match:
            return search_start + word_match[-1].start()
        
        return None
    
    def _get_overlap(
        self,
        segments: List[str],
        overlap_size: int,
        separator: str
    ) -> str:
        """Extract overlap text from end of segments."""
        full_text = separator.join(segments)
        
        if len(full_text) <= overlap_size:
            return full_text
        
        # Get the last overlap_size characters, respecting word boundaries
        overlap_start = len(full_text) - overlap_size
        
        # Find the next word boundary
        space_pos = full_text.find(" ", overlap_start)
        if space_pos != -1:
            overlap_start = space_pos + 1
        
        return full_text[overlap_start:]
    
    def _clean_chunks(self, chunks: List[str]) -> List[str]:
        """Clean up chunks - remove empty ones, trim whitespace."""
        cleaned = []
        for chunk in chunks:
            chunk = chunk.strip()
            if chunk and len(chunk) > 10:  # Skip very short chunks
                cleaned.append(chunk)
        return cleaned
    
    def chunk_with_metadata(
        self,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> List[Tuple[str, dict]]:
        """
        Chunk text and return with position metadata.
        
        Returns:
            List of (chunk_text, metadata) tuples
        """
        chunks = self.chunk(text, chunk_size, chunk_overlap)
        
        results = []
        current_pos = 0
        
        for i, chunk in enumerate(chunks):
            # Find actual position in original text
            pos = text.find(chunk[:50], current_pos)
            if pos == -1:
                pos = current_pos
            
            metadata = {
                "chunk_index": i,
                "total_chunks": len(chunks),
                "start_char": pos,
                "end_char": pos + len(chunk),
                "length": len(chunk)
            }
            
            results.append((chunk, metadata))
            current_pos = pos + len(chunk) - chunk_overlap
        
        return results
