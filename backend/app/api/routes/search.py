"""
Healthcare Intelligence Platform - Search Routes
Handles semantic search across clinical documents
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from loguru import logger

from core.embeddings import EmbeddingService
from vectorstore.faiss_store import FAISSStore
from llm.rag_pipeline import RAGPipeline

router = APIRouter()

# Initialize services
embedding_service = EmbeddingService()
vector_store = FAISSStore()
rag_pipeline = RAGPipeline()


class SearchQuery(BaseModel):
    """Search query model."""
    query: str
    top_k: int = 5
    use_rag: bool = True


class SearchResult(BaseModel):
    """Individual search result."""
    chunk_id: str
    document_id: str
    content: str
    score: float
    metadata: dict


class SearchResponse(BaseModel):
    """Search response model."""
    query: str
    results: List[SearchResult]
    total_results: int
    rag_summary: Optional[str] = None
    latency_ms: float


@router.post("/semantic", response_model=SearchResponse)
async def semantic_search(search_query: SearchQuery):
    """
    Perform semantic search across clinical documents.
    
    Uses sentence embeddings to find contextually similar content,
    not just keyword matches.
    """
    import time
    start_time = time.time()
    
    try:
        logger.info(f"🔍 Semantic search: '{search_query.query}'")
        
        # Generate query embedding
        query_embedding = embedding_service.embed_query(search_query.query)
        
        # Search vector store
        results = vector_store.search(
            query_embedding=query_embedding,
            top_k=search_query.top_k
        )
        
        # Format results
        search_results = [
            SearchResult(
                chunk_id=r["chunk_id"],
                document_id=r["document_id"],
                content=r["content"],
                score=r["score"],
                metadata=r.get("metadata", {})
            )
            for r in results
        ]
        
        # Generate RAG summary if requested
        rag_summary = None
        if search_query.use_rag and results:
            context = "\n\n".join([r["content"] for r in results[:3]])
            rag_summary = await rag_pipeline.generate_answer(
                query=search_query.query,
                context=context
            )
        
        latency = (time.time() - start_time) * 1000
        logger.info(f"✅ Search completed in {latency:.2f}ms, found {len(results)} results")
        
        return SearchResponse(
            query=search_query.query,
            results=search_results,
            total_results=len(search_results),
            rag_summary=rag_summary,
            latency_ms=round(latency, 2)
        )
        
    except Exception as e:
        logger.error(f"❌ Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@router.get("/quick")
async def quick_search(
    q: str = Query(..., description="Search query"),
    limit: int = Query(5, ge=1, le=20, description="Number of results")
):
    """Quick search endpoint for autocomplete and suggestions."""
    try:
        query_embedding = embedding_service.embed_query(q)
        results = vector_store.search(query_embedding=query_embedding, top_k=limit)
        
        return {
            "query": q,
            "suggestions": [
                {
                    "content": r["content"][:200] + "..." if len(r["content"]) > 200 else r["content"],
                    "score": r["score"]
                }
                for r in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def search_stats():
    """Get search and vector store statistics."""
    stats = vector_store.get_stats()
    return {
        "total_documents": stats.get("total_documents", 0),
        "total_chunks": stats.get("total_chunks", 0),
        "index_size_mb": stats.get("index_size_mb", 0),
        "embedding_dimension": 768
    }
