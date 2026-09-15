# Enterprise AI Workflow Agent — Development & Updates Log (`updation.md`)

This file tracks the real-time engineering decisions, stage completions, git commit history, and interview talking points across the entire lifecycle of the **Enterprise AI Workflow Agent**.

---

## 📌 Project Overview
- **Project Name:** Enterprise AI Workflow Agent
- **Core Architecture:** Intent Understanding → Dynamic Multi-Tool Routing (SQL + RAG + REST API) → Result Synthesis → n8n Orchestration
- **Tech Stack:** Python 3.10+, FastAPI, SQLite, ChromaDB, Google Gemini API (Function Calling), n8n, Pytest.
- **Rule of Thumb:** *Build first, claim later.* Every claimed capability has real, runnable code, automated tests, and git commit history.

---

## 🚦 Milestone Roadmap & Status

| Step | Milestone | Status | Git Commit | Key Deliverables |
| :--- | :--- | :---: | :---: | :--- |
| **Step 1** | Project Structure & Setup | 🟡 In Progress | Pending | Scaffold, `.gitignore`, `requirements.txt`, `.env.example`, `config.py` |
| **Step 2** | SQLite Database & Business Data | ⚪ Pending | — | `schema.sql`, realistic seed data, `sql_tool.py`, SQL tests |
| **Step 3** | FastAPI REST Services | ⚪ Pending | — | Product/Order endpoints, healthcheck, Swagger docs |
| **Step 4** | RAG Pipeline (ChromaDB + Policies) | ⚪ Pending | — | 4 policy docs, chunking/indexing, `rag_tool.py`, semantic retrieval tests |
| **Step 5** | Tool Registry & Gemini Agent | ⚪ Pending | — | Gemini Function Calling schemas, multi-tool loop, synthesis engine |
| **Step 6** | n8n Workflow Integration | ⚪ Pending | — | `workflow.json`, webhook trigger, HTTP node chaining |
| **Step 7** | Scenario Testing & Verification | ⚪ Pending | — | 3 core interview queries tested end-to-end |
| **Step 8** | README & Interview Defense Guide | ⚪ Pending | — | Architecture diagrams, code walkthrough, Q&A defense |

---

## 📝 Stage-by-Stage Engineering Log

### 🔹 Stage 1: Project Scaffolding & Environment Setup
- **Date:** September 15, 2026
- **Actions Taken:**
  - Initialized repository architecture with dedicated layers: `database/`, `rag/`, `api/`, `agent/`, `n8n/`, `tests/`, `data/`.
  - Configured comprehensive `.gitignore` ensuring API secrets, Python caches, and local vector storage are excluded from version control.
  - Specified decoupled dependencies in `requirements.txt` (`fastapi`, `uvicorn`, `google-genai`, `chromadb`, `tabulate`, `pytest`).
  - Created `.env.example` defining central configurations (`GEMINI_API_KEY`, `DATABASE_PATH`, `CHROMA_PERSIST_DIR`, `API_PORT`).
  - Created `src/config.py` using `pydantic-settings`/`dotenv` for centralized, type-safe application configuration.
- **Engineering Decision & Rationale:**
  - *Why separate tools into independent modules?* Instead of monolithic agent scripts, each tool (`sql_tool`, `rag_tool`, `api_tool`) is built as an isolated Python callable with standalone unit tests. This ensures they can be invoked directly by FastAPI, locally in a CLI, or by Gemini function calling without tight coupling.
- **Git Commit:** `feat: step 1 - project scaffold and environment configuration`
