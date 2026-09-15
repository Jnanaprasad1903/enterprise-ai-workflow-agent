from typing import Optional
from src.rag.vector_store import get_policy_collection
from src.rag.indexer import index_all_documents

def search_policy_documents(query: str, top_k: int = 3) -> str:
    """
    Searches enterprise company documents and policy knowledge base using semantic vector retrieval (RAG).
    Use this tool whenever you need unstructured knowledge, such as:
    - Company return policy rules, time windows, and condition requirements
    - Restocking fees and fee waiver conditions for defective items
    - Shipping options, delivery estimates, damage-in-transit protocols
    - Hardware warranty coverage periods, exclusions, and RMA claim procedures
    - Customer support SLAs and escalation policies
    
    Args:
        query: The semantic search query (e.g., 'return policy for opened electronics', 'warranty for smart watch battery')
        top_k: Number of most relevant policy chunks to retrieve (default: 3)
        
    Returns:
        Markdown-formatted string containing the top relevant policy excerpts and citations.
    """
    try:
        collection = get_policy_collection()
        
        # If collection is empty, trigger indexing automatically
        if collection.count() == 0:
            print("[*] Knowledge base is empty. Running indexer...")
            index_all_documents()
            
        results = collection.query(
            query_texts=[query],
            n_results=min(top_k, max(1, collection.count()))
        )
        
        docs = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0] if "distances" in results else []
        
        if not docs:
            return f"No relevant policy documents found matching query: '{query}'."
            
        formatted_output = [
            f"### Semantic Search Results for: '{query}'\n",
            f"Found {len(docs)} relevant policy sections:\n"
        ]
        
        for idx, (doc, meta) in enumerate(zip(docs, metadatas), 1):
            source = meta.get("source", "Unknown Document")
            section = meta.get("section", "General")
            doc_title = meta.get("document_title", source)
            
            # Optional cosine distance conversion
            dist_str = f" (Distance: {distances[idx-1]:.3f})" if idx-1 < len(distances) else ""
            
            formatted_output.append(
                f"#### Excerpt {idx} — {doc_title} > {section}{dist_str}\n"
                f"*Source: `data/docs/{source}`*\n\n"
                f"{doc}\n"
                f"\n---"
            )
            
        return "\n".join(formatted_output)
    except Exception as e:
        return f"RAG Retrieval Error: {str(e)}"
