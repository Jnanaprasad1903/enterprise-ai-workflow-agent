# 🚀 Enterprise AI Workflow Agent

> An intelligent, multi-tool enterprise business assistant that dynamically combines **structured SQL business data**, **unstructured policy documents (RAG)**, and **live REST APIs** using **Google Gemini Function Calling** and **n8n orchestration**.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-Function_Calling-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F00?style=flat)](https://www.trychroma.com/)
[![n8n](https://img.shields.io/badge/n8n-Orchestration-EA4B71?style=flat&logo=n8n&logoColor=white)](https://n8n.io/)

---

## 💡 What Makes This "Agentic" (vs a Simple Chatbot)?

A typical chatbot takes a user query and passes it directly to an LLM:
$$\text{User Query} \longrightarrow \text{LLM} \longrightarrow \text{Generic Answer}$$

This **Enterprise AI Workflow Agent** reasons over user intent, selects and executes the necessary specialized enterprise tools (in parallel or sequence), and synthesizes multi-source evidence:

```text
                                  USER QUERY
                                      │
                                      ▼
                               ┌─────────────┐
                               │     n8n     │  (Webhook Orchestration)
                               └──────┬──────┘
                                      │
                                      ▼
                            ┌───────────────────┐
                            │   FastAPI Agent   │  (Brain: Gemini 2.5 Flash)
                            └─────────┬─────────┘
                                      │
                   ┌──────────────────┼──────────────────┐
                   ▼                  ▼                  ▼
             ┌───────────┐      ┌───────────┐      ┌───────────┐
             │ SQL Tool  │      │ RAG Tool  │      │ API Tool  │
             └─────┬─────┘      └─────┬─────┘      └─────┬─────┘
                   │                  │                  │
                   ▼                  ▼                  ▼
              SQLite DB           ChromaDB          FastAPI Live
           (Sales/Returns)     (Company Docs)        (Orders/SKUs)
                   │                  │                  │
                   └──────────────────┼──────────────────┘
                                      │
                                      ▼
                            ┌───────────────────┐
                            │    Synthesis &    │
                            │ Reasoning Engine  │
                            └─────────┬─────────┘
                                      │
                                      ▼
                             ACCURATE ENTERPRISE
                                   ANSWER
```

---

## 🎯 The Three Core Interview Scenarios

| Scenario | Sample Query | Tools Invoked | What it Proves |
| :--- | :--- | :--- | :--- |
| **1. Structured Query** | *"Which product generated the highest revenue last month?"* | `SQL Tool` | SQL generation, schema grounding, zero hallucinations on math. |
| **2. Unstructured Query** | *"What is our policy on returning opened electronics?"* | `RAG Tool` | Semantic vector search, chunk retrieval, policy extraction. |
| **3. Multi-Source Reasoning** | *"Which product had the highest returns, and what does our return policy say about returning that category?"* | `SQL Tool` + `RAG Tool` | **True Agentic Behavior:** Tool chaining, cross-modal data synthesis. |

---

## 📂 Project Architecture

```text
d:\Office_agent/
├── README.md                 # Project vision, architecture & interview guide
├── updation.md               # Continuous progress log and milestone tracker
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── data/
│   ├── enterprise.db         # SQLite relational database (products, sales, returns)
│   ├── docs/                 # Unstructured knowledge base (policies)
│   │   ├── return_policy.md
│   │   ├── shipping_policy.md
│   │   ├── warranty_policy.md
│   │   └── customer_support_sla.md
│   └── chroma_db/            # Vector embeddings store
├── src/
│   ├── __init__.py
│   ├── config.py             # Environment configuration (Pydantic / dotenv)
│   ├── database/             # SQLite connection, schema, seed data, and SQL tool
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── schema.sql
│   │   ├── seed_data.py
│   │   └── sql_tool.py
│   ├── rag/                  # RAG indexing, chunking, and similarity search
│   │   ├── __init__.py
│   │   ├── vector_store.py
│   │   ├── indexer.py
│   │   └── rag_tool.py
│   ├── api/                  # FastAPI REST endpoints
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes.py
│   └── agent/                # Gemini Agent with Tool Calling & Reasoning Engine
│       ├── __init__.py
│       ├── tools.py          # Unified tool schemas for Gemini
│       └── workflow_agent.py # Agent execution loop & response synthesis
├── n8n/
│   ├── README.md             # How to import and run the n8n workflow
│   └── workflow.json         # Ready-to-import n8n workflow
└── tests/
    ├── test_sql_tool.py
    ├── test_rag_tool.py
    ├── test_api.py
    └── run_scenarios.py      # Automated runner for the 3 demo scenarios
```

---

## ⚡ Quick Start

### 1. Clone & Set Up Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and add your Google Gemini API key:
```bash
cp .env.example .env
```
Edit `.env`:
```env
GEMINI_API_KEY="your_api_key_here"
```

### 3. Initialize Database & Seed Business Data
```bash
python -m src.database.seed_data
```

### 4. Index Knowledge Base for RAG
```bash
python -m src.rag.indexer
```

### 5. Launch FastAPI Backend
```bash
uvicorn src.api.main:app --reload --port 8000
```
Visit Swagger documentation at `http://localhost:8000/docs`.

### 6. Run the 3 Demo Scenarios
```bash
python tests/run_scenarios.py
```

---
