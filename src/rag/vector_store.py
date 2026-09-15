from pathlib import Path
from typing import Optional
import chromadb
from chromadb.config import Settings
from src.config import CHROMA_PERSIST_DIR

COLLECTION_NAME = "enterprise_policies"

def get_chroma_client(persist_dir: Optional[Path] = None) -> chromadb.PersistentClient:
    """Returns a persistent ChromaDB client pointing to the configured data directory."""
    target_dir = persist_dir or CHROMA_PERSIST_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=str(target_dir),
        settings=Settings(anonymized_telemetry=False)
    )

def get_policy_collection(persist_dir: Optional[Path] = None):
    """
    Retrieves or creates the enterprise policies vector collection using cosine similarity.
    Uses Chroma's default embedding function (all-MiniLM-L6-v2 via ONNX) for fast,
    deterministic local vector embeddings without external API rate-limit dependencies.
    """
    client = get_chroma_client(persist_dir)
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
