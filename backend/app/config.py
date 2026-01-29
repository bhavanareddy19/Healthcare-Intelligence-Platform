"""
Healthcare Intelligence Platform - Configuration Module
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache
from dotenv import load_dotenv

# Load .env from project root (parent of backend)
_backend_dir = Path(__file__).parent.parent
_project_root = _backend_dir.parent
_env_file = _project_root / ".env"

if _env_file.exists():
    load_dotenv(_env_file)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Project Info
    app_name: str = "Healthcare Intelligence Platform"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Groq API - with default for demo mode
    groq_api_key: str = Field(
        default=os.getenv("GROQ_API_KEY", "demo_key"),
        validation_alias="GROQ_API_KEY"
    )
    groq_model: str = Field(
        default="llama-3.1-70b-versatile",
        validation_alias="GROQ_MODEL"
    )
    
    # Embedding Model
    embedding_model: str = Field(
        default="pritamdeka/S-PubMedBert-MS-MARCO",
        validation_alias="EMBEDDING_MODEL"
    )
    
    # Vector Store Paths
    faiss_index_path: str = Field(
        default="./data/faiss_index",
        validation_alias="FAISS_INDEX_PATH"
    )
    metadata_db_path: str = Field(
        default="./data/metadata.db",
        validation_alias="METADATA_DB_PATH"
    )
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", validation_alias="API_HOST")
    api_port: int = Field(default=8000, validation_alias="API_PORT")
    
    # Paths
    base_dir: Path = _project_root
    data_dir: Path = _project_root / "data"
    sample_docs_dir: Path = _project_root / "data" / "sample_documents"
    
    model_config = SettingsConfigDict(
        env_file=str(_env_file),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Create data directories on import
settings = get_settings()
settings.data_dir.mkdir(parents=True, exist_ok=True)
settings.sample_docs_dir.mkdir(parents=True, exist_ok=True)
