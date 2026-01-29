"""
Healthcare Intelligence Platform - Document Routes
Handles document upload, processing, and retrieval
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from loguru import logger

from core.document_processor import DocumentProcessor
from core.embeddings import EmbeddingService
from vectorstore.faiss_store import FAISSStore

router = APIRouter()

# Initialize services
doc_processor = DocumentProcessor()
embedding_service = EmbeddingService()
vector_store = FAISSStore()


class DocumentResponse(BaseModel):
    """Document response model."""
    id: str
    filename: str
    status: str
    uploaded_at: str
    chunks_count: int
    message: str


class DocumentListResponse(BaseModel):
    """Document list response model."""
    total: int
    documents: List[dict]


# In-memory document store (would use DB in production)
documents_db = {}


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload a clinical document for processing.
    
    Supports:
    - PDF files
    - Text files (.txt)
    - Word documents (.docx)
    """
    # Validate file type
    allowed_types = [".pdf", ".txt", ".docx"]
    file_ext = "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""
    
    if file_ext not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed types: {allowed_types}"
        )
    
    # Generate document ID
    doc_id = str(uuid.uuid4())
    
    try:
        # Read file content
        content = await file.read()
        
        # Process document
        logger.info(f"📄 Processing document: {file.filename}")
        text_content = doc_processor.process(content, file_ext)
        
        # Chunk the document
        chunks = doc_processor.chunk_text(text_content)
        logger.info(f"📝 Created {len(chunks)} chunks")
        
        # Generate embeddings
        embeddings = embedding_service.embed_texts(chunks)
        logger.info(f"🧠 Generated {len(embeddings)} embeddings")
        
        # Store in vector database
        vector_store.add_documents(
            doc_id=doc_id,
            chunks=chunks,
            embeddings=embeddings,
            metadata={"filename": file.filename, "uploaded_at": datetime.now().isoformat()}
        )
        
        # Store document metadata
        documents_db[doc_id] = {
            "id": doc_id,
            "filename": file.filename,
            "status": "processed",
            "uploaded_at": datetime.now().isoformat(),
            "chunks_count": len(chunks),
            "text_preview": text_content[:500] + "..." if len(text_content) > 500 else text_content
        }
        
        return DocumentResponse(
            id=doc_id,
            filename=file.filename,
            status="processed",
            uploaded_at=datetime.now().isoformat(),
            chunks_count=len(chunks),
            message=f"Successfully processed {file.filename}"
        )
        
    except Exception as e:
        logger.error(f"❌ Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.get("/", response_model=DocumentListResponse)
async def list_documents():
    """List all uploaded documents."""
    return DocumentListResponse(
        total=len(documents_db),
        documents=list(documents_db.values())
    )


@router.get("/{doc_id}")
async def get_document(doc_id: str):
    """Get document details by ID."""
    if doc_id not in documents_db:
        raise HTTPException(status_code=404, detail="Document not found")
    return documents_db[doc_id]


@router.delete("/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document by ID."""
    if doc_id not in documents_db:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Remove from vector store
    vector_store.delete_document(doc_id)
    
    # Remove from memory
    del documents_db[doc_id]
    
    return {"message": f"Document {doc_id} deleted successfully"}


@router.post("/sample")
async def load_sample_documents():
    """Load sample clinical documents for testing."""
    from data.sample_documents import SAMPLE_DOCUMENTS
    
    loaded = []
    for doc in SAMPLE_DOCUMENTS:
        doc_id = str(uuid.uuid4())
        
        # Process and store
        chunks = doc_processor.chunk_text(doc["content"])
        embeddings = embedding_service.embed_texts(chunks)
        
        vector_store.add_documents(
            doc_id=doc_id,
            chunks=chunks,
            embeddings=embeddings,
            metadata={"filename": doc["title"], "type": doc["type"]}
        )
        
        documents_db[doc_id] = {
            "id": doc_id,
            "filename": doc["title"],
            "status": "processed",
            "uploaded_at": datetime.now().isoformat(),
            "chunks_count": len(chunks),
            "type": doc["type"],
            "text_preview": doc["content"][:500]
        }
        
        loaded.append(doc["title"])
    
    return {"message": f"Loaded {len(loaded)} sample documents", "documents": loaded}
