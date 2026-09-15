import pytest
from src.rag.indexer import index_all_documents
from src.rag.rag_tool import search_policy_documents
from src.rag.vector_store import get_policy_collection

@pytest.fixture(scope="module", autouse=True)
def setup_rag():
    """Ensure all corporate markdown policy documents are indexed before running tests."""
    count = index_all_documents()
    assert count > 0

def test_collection_contains_chunks():
    """Verify ChromaDB collection has been populated with chunks."""
    col = get_policy_collection()
    assert col.count() >= 10

def test_return_policy_electronics_query():
    """Verify Scenario 2 RAG query retrieves the electronics return policy."""
    query = "What is our policy on returning opened electronics?"
    result = search_policy_documents(query, top_k=2)
    
    assert "return_policy.md" in result
    assert "14 calendar days" in result
    assert "restocking fee" in result.lower()
    assert "waived" in result.lower()

def test_warranty_wearables_query():
    """Verify RAG retrieval for smart watch hardware and battery warranty."""
    query = "What is the warranty coverage for smart watches and battery failure?"
    result = search_policy_documents(query, top_k=2)
    
    assert "warranty_policy.md" in result
    assert "12 months" in result
    assert "battery" in result.lower()

def test_shipping_damaged_transit_query():
    """Verify RAG retrieval for damaged shipping protocol."""
    query = "How to report items damaged in transit during delivery?"
    result = search_policy_documents(query, top_k=2)
    
    assert "shipping_policy.md" in result
    assert "48 hours" in result
