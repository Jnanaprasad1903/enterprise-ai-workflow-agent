import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.agent.workflow_agent import EnterpriseWorkflowAgent
from src.database.seed_data import seed_database
from src.rag.indexer import index_all_documents

@pytest.fixture(scope="module", autouse=True)
def setup_environment():
    """Ensure database is seeded and RAG vectors are indexed before agent tests."""
    seed_database()
    index_all_documents()

client = TestClient(app)

def test_agent_scenario_1_structured_revenue():
    """Scenario 1: Which product generated the highest revenue?"""
    agent = EnterpriseWorkflowAgent()
    res = agent.run("Which product generated the highest revenue?")
    
    assert res["status"] == "success"
    assert "query_database" in res["tools_used"]
    assert "Laptop Pro 16" in res["answer"]
    assert "450,000" in res["answer"] or "450000" in res["answer"]

def test_agent_scenario_2_unstructured_policy():
    """Scenario 2: What is our policy on returning opened electronics?"""
    agent = EnterpriseWorkflowAgent()
    res = agent.run("What is our return policy on opened electronics?")
    
    assert res["status"] == "success"
    assert "search_policy_documents" in res["tools_used"]
    assert "14 calendar days" in res["answer"] or "14" in res["answer"]
    assert "restocking fee" in res["answer"].lower()

def test_agent_scenario_3_multi_source_synthesis():
    """Scenario 3: Which product had the highest returns and what does our return policy say?"""
    agent = EnterpriseWorkflowAgent()
    res = agent.run("Which product had the highest returns, and what does our return policy say about returning that category?")
    
    assert res["status"] == "success"
    # Proves multi-source agentic capability: invoked BOTH tools
    assert "query_database" in res["tools_used"]
    assert "search_policy_documents" in res["tools_used"]
    
    # Proves synthesis of both structured data and unstructured policy
    answer = res["answer"]
    assert "Smart Watch Active" in answer
    assert "5" in answer
    assert "14" in answer
    assert "waived" in answer.lower()

def test_agent_fastapi_endpoint():
    """Verify n8n-compatible HTTP endpoint POST /api/v1/agent/query"""
    payload = {
        "query": "Which product had the highest returns, and what does our return policy say?"
    }
    response = client.post("/api/v1/agent/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "query_database" in data["tools_used"]
    assert "search_policy_documents" in data["tools_used"]
    assert "Smart Watch Active" in data["answer"]
