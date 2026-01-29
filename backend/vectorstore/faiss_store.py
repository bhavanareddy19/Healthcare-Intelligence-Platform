"""
Healthcare Intelligence Platform - FAISS Vector Store
High-performance similarity search for clinical documents
"""

import os
import json
import sqlite3
import numpy as np
from typing import List, Dict, Any, Optional
from pathlib import Path
from loguru import logger
from datetime import datetime


class FAISSStore:
    """
    FAISS-based vector store for clinical document embeddings.
    
    Features:
    - Fast similarity search across millions of vectors
    - Metadata storage with SQLite
    - Persistent storage with save/load
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern for vector store."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize FAISS store."""
        if self._initialized:
            return
        
        self._dimension = 768
        self._index = None
        self._faiss = None
        self._chunks: List[str] = []
        self._metadata: List[Dict] = []
        self._doc_mapping: Dict[str, List[int]] = {}  # doc_id -> chunk indices
        
        self._initialize_faiss()
        self._initialized = True
    
    def _initialize_faiss(self):
        """Initialize FAISS index."""
        try:
            import faiss
            self._faiss = faiss
            
            # Use IndexFlatIP for Inner Product (cosine similarity with normalized vectors)
            self._index = faiss.IndexFlatIP(self._dimension)
            logger.info(f"✅ FAISS index initialized (dimension={self._dimension})")
            
        except ImportError:
            logger.warning("FAISS not installed, using mock index")
            self._faiss = None
            self._index = MockFAISSIndex(self._dimension)
    
    def add_documents(
        self,
        doc_id: str,
        chunks: List[str],
        embeddings: np.ndarray,
        metadata: Optional[Dict] = None
    ) -> int:
        """
        Add document chunks to the vector store.
        
        Args:
            doc_id: Unique document identifier
            chunks: List of text chunks
            embeddings: NumPy array of embeddings (n_chunks, dimension)
            metadata: Optional metadata for the document
            
        Returns:
            Number of chunks added
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must match number of embeddings")
        
        start_idx = len(self._chunks)
        chunk_indices = []
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            idx = start_idx + i
            chunk_indices.append(idx)
            
            self._chunks.append(chunk)
            self._metadata.append({
                "chunk_id": f"{doc_id}_{i}",
                "document_id": doc_id,
                "chunk_index": i,
                "added_at": datetime.now().isoformat(),
                **(metadata or {})
            })
        
        # Add to FAISS index
        embeddings = embeddings.astype(np.float32)
        if self._faiss:
            self._index.add(embeddings)
        else:
            self._index.add(embeddings)
        
        self._doc_mapping[doc_id] = chunk_indices
        
        logger.info(f"📥 Added {len(chunks)} chunks for document {doc_id}")
        return len(chunks)
    
    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        doc_filter: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar chunks.
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            doc_filter: Optional list of document IDs to filter
            
        Returns:
            List of search results with content, score, and metadata
        """
        if len(self._chunks) == 0:
            logger.warning("No documents in vector store")
            return []
        
        # Ensure query is 2D and float32
        query = query_embedding.reshape(1, -1).astype(np.float32)
        
        # Search more than needed if filtering
        search_k = min(top_k * 3 if doc_filter else top_k, len(self._chunks))
        
        if self._faiss:
            scores, indices = self._index.search(query, search_k)
        else:
            scores, indices = self._index.search(query, search_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self._chunks):
                continue
            
            meta = self._metadata[idx]
            
            # Apply document filter if specified
            if doc_filter and meta["document_id"] not in doc_filter:
                continue
            
            results.append({
                "chunk_id": meta["chunk_id"],
                "document_id": meta["document_id"],
                "content": self._chunks[idx],
                "score": float(score),
                "metadata": meta
            })
            
            if len(results) >= top_k:
                break
        
        return results
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from the store.
        
        Note: FAISS doesn't support deletion efficiently, so we mark as deleted
        and rebuild periodically in production.
        """
        if doc_id not in self._doc_mapping:
            return False
        
        # Mark chunks as deleted (set content to empty)
        for idx in self._doc_mapping[doc_id]:
            self._chunks[idx] = ""
            self._metadata[idx]["deleted"] = True
        
        del self._doc_mapping[doc_id]
        logger.info(f"🗑️ Marked document {doc_id} as deleted")
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics."""
        active_chunks = sum(1 for c in self._chunks if c)
        
        return {
            "total_documents": len(self._doc_mapping),
            "total_chunks": active_chunks,
            "index_size_mb": round(
                (active_chunks * self._dimension * 4) / (1024 * 1024), 2
            ),
            "dimension": self._dimension
        }
    
    def save(self, path: str):
        """Save index and metadata to disk."""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        if self._faiss:
            self._faiss.write_index(self._index, str(path / "index.faiss"))
        
        # Save metadata
        with open(path / "metadata.json", "w") as f:
            json.dump({
                "chunks": self._chunks,
                "metadata": self._metadata,
                "doc_mapping": self._doc_mapping
            }, f)
        
        logger.info(f"💾 Saved vector store to {path}")
    
    def load(self, path: str):
        """Load index and metadata from disk."""
        path = Path(path)
        
        if not path.exists():
            logger.warning(f"Index path {path} does not exist")
            return
        
        # Load FAISS index
        if self._faiss and (path / "index.faiss").exists():
            self._index = self._faiss.read_index(str(path / "index.faiss"))
        
        # Load metadata
        if (path / "metadata.json").exists():
            with open(path / "metadata.json", "r") as f:
                data = json.load(f)
                self._chunks = data["chunks"]
                self._metadata = data["metadata"]
                self._doc_mapping = data["doc_mapping"]
        
        logger.info(f"📂 Loaded vector store from {path}")
    
    def clear(self):
        """Clear all data from the store."""
        self._chunks = []
        self._metadata = []
        self._doc_mapping = {}
        self._initialize_faiss()
        logger.info("🧹 Cleared vector store")


class MockFAISSIndex:
    """Mock FAISS index for when FAISS is not installed."""
    
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.vectors: List[np.ndarray] = []
    
    def add(self, vectors: np.ndarray):
        for v in vectors:
            self.vectors.append(v)
    
    def search(self, query: np.ndarray, k: int):
        if not self.vectors:
            return np.array([[-1.0]]), np.array([[-1]])
        
        # Compute similarities
        vectors = np.array(self.vectors)
        similarities = np.dot(vectors, query.T).flatten()
        
        # Get top k
        k = min(k, len(similarities))
        indices = np.argsort(similarities)[::-1][:k]
        scores = similarities[indices]
        
        return np.array([scores]), np.array([indices])
