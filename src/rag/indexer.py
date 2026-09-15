import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.config import DOCS_DIR
from src.rag.vector_store import get_policy_collection

def chunk_markdown_document(filepath: Path) -> List[Dict[str, Any]]:
    """
    Parses a markdown policy document into semantic section chunks.
    Ensures headers are retained with their associated policy clauses.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    filename = filepath.name
    doc_title = filepath.stem.replace("_", " ").title()
    
    # Check if doc has a top-level # title
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if title_match:
        doc_title = title_match.group(1).strip()

    # Split by section headers (##)
    sections = re.split(r"(^##\s+.+$)", content, flags=re.MULTILINE)
    
    chunks: List[Dict[str, Any]] = []
    
    # Handle intro before first ## if non-empty
    if sections and sections[0].strip():
        intro_text = sections[0].strip()
        chunks.append({
            "text": f"Document: {doc_title}\nSection: Overview\n\n{intro_text}",
            "metadata": {
                "source": filename,
                "document_title": doc_title,
                "section": "Overview"
            }
        })
    
    # Iterate through pairs of (header, body)
    for i in range(1, len(sections), 2):
        header_raw = sections[i].strip()
        section_title = re.sub(r"^##\s+", "", header_raw).strip()
        body = sections[i + 1].strip() if i + 1 < len(sections) else ""
        
        chunk_text = f"Document: {doc_title}\nSection: {section_title}\n\n{body}"
        chunks.append({
            "text": chunk_text,
            "metadata": {
                "source": filename,
                "document_title": doc_title,
                "section": section_title
            }
        })
        
    return chunks

def index_all_documents(docs_dir: Optional[Path] = None) -> int:
    """
    Reads all policy markdown documents in docs_dir and upserts them
    into the ChromaDB enterprise_policies collection.
    """
    target_dir = docs_dir or DOCS_DIR
    if not target_dir.exists():
        raise FileNotFoundError(f"Documentation directory not found: {target_dir}")
        
    md_files = list(target_dir.glob("*.md"))
    if not md_files:
        print(f"[!] No markdown files found in {target_dir}")
        return 0

    collection = get_policy_collection()
    
    all_ids: List[str] = []
    all_docs: List[str] = []
    all_metadatas: List[Dict[str, Any]] = []

    for file in md_files:
        chunks = chunk_markdown_document(file)
        for idx, chunk in enumerate(chunks):
            chunk_id = f"{file.stem}_chunk_{idx}"
            all_ids.append(chunk_id)
            all_docs.append(chunk["text"])
            all_metadatas.append(chunk["metadata"])

    # Upsert chunks into ChromaDB
    collection.upsert(
        ids=all_ids,
        documents=all_docs,
        metadatas=all_metadatas
    )
    
    print(f"[+] Successfully indexed {len(all_ids)} chunks across {len(md_files)} documents into ChromaDB.")
    return len(all_ids)

if __name__ == "__main__":
    index_all_documents()
