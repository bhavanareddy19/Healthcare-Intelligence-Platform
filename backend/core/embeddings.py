"""
Healthcare Intelligence Platform - Embedding Service
Sentence transformer embeddings for clinical text
"""

import numpy as np
from typing import List, Optional, Union
from loguru import logger
from functools import lru_cache


class EmbeddingService:
    """
    Embedding service using sentence transformers.
    
    Uses PubMedBERT-based model for medical text embeddings.
    """
    
    _instance = None
    _model = None
    
    def __new__(cls):
        """Singleton pattern for embedding service."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize embedding service with lazy model loading."""
        self._model_name = "pritamdeka/S-PubMedBert-MS-MARCO"
        self._dimension = 768
        self._model_loaded = False
    
    def _load_model(self):
        """Lazy load the sentence transformer model."""
        if self._model_loaded:
            return
        
        try:
            from sentence_transformers import SentenceTransformer
            
            logger.info(f"🧠 Loading embedding model: {self._model_name}")
            self._model = SentenceTransformer(self._model_name)
            self._model_loaded = True
            logger.info("✅ Embedding model loaded successfully")
            
        except ImportError:
            logger.warning("sentence-transformers not installed, using mock embeddings")
            self._model = None
            self._model_loaded = True
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            logger.warning("Using mock embeddings")
            self._model = None
            self._model_loaded = True
    
    @property
    def dimension(self) -> int:
        """Get embedding dimension."""
        return self._dimension
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            NumPy array of shape (len(texts), dimension)
        """
        self._load_model()
        
        if not texts:
            return np.array([])
        
        if self._model is None:
            # Return mock embeddings for testing
            logger.debug(f"Generating mock embeddings for {len(texts)} texts")
            return self._generate_mock_embeddings(texts)
        
        try:
            logger.debug(f"Generating embeddings for {len(texts)} texts")
            embeddings = self._model.encode(
                texts,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            return embeddings.astype(np.float32)
            
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            return self._generate_mock_embeddings(texts)
    
    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a single query.
        
        Args:
            query: Query string
            
        Returns:
            NumPy array of shape (dimension,)
        """
        embeddings = self.embed_texts([query])
        return embeddings[0] if len(embeddings) > 0 else np.zeros(self._dimension)
    
    def _generate_mock_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate deterministic mock embeddings for testing.
        
        Uses text hash to create reproducible embeddings.
        """
        embeddings = []
        for text in texts:
            # Create deterministic embedding based on text hash
            np.random.seed(hash(text) % (2**32))
            emb = np.random.randn(self._dimension).astype(np.float32)
            # Normalize
            emb = emb / np.linalg.norm(emb)
            embeddings.append(emb)
        
        return np.array(embeddings)
    
    def compute_similarity(
        self,
        query_embedding: np.ndarray,
        doc_embeddings: np.ndarray
    ) -> np.ndarray:
        """
        Compute cosine similarity between query and documents.
        
        Args:
            query_embedding: Query embedding vector
            doc_embeddings: Document embedding matrix
            
        Returns:
            Array of similarity scores
        """
        # Normalize query
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        
        # Normalize documents
        doc_norms = np.linalg.norm(doc_embeddings, axis=1, keepdims=True)
        doc_normalized = doc_embeddings / (doc_norms + 1e-10)
        
        # Compute cosine similarity
        similarities = np.dot(doc_normalized, query_norm)
        
        return similarities
    
    def batch_embed(
        self,
        texts: List[str],
        batch_size: int = 32
    ) -> np.ndarray:
        """
        Embed texts in batches to manage memory.
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts per batch
            
        Returns:
            NumPy array of all embeddings
        """
        self._load_model()
        
        if not texts:
            return np.array([])
        
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.embed_texts(batch)
            all_embeddings.append(batch_embeddings)
            
            if (i + batch_size) % 100 == 0:
                logger.debug(f"Embedded {min(i + batch_size, len(texts))}/{len(texts)} texts")
        
        return np.vstack(all_embeddings) if all_embeddings else np.array([])
