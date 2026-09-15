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
| **Step 1** | Project Structure & Setup | 🟢 Completed | `791f0c8` | Scaffold, `.gitignore`, `requirements.txt`, `.env.example`, `config.py` |
| **Step 2** | SQLite Database & Business Data | 🟢 Completed | `45d1080` | `schema.sql`, realistic seed data, `sql_tool.py`, SQL tests (5/5 passing) |
| **Step 3** | FastAPI REST Services | 🟢 Completed | `64e422e` | Product/Order endpoints, returns analytics, Swagger docs, API tests |
| **Step 4** | RAG Pipeline (ChromaDB + Policies) | 🟢 Completed | `5800692` | 4 policy docs, semantic section chunking, `rag_tool.py`, ChromaDB tests |
| **Step 5** | Tool Registry & Gemini Agent | 🟢 Completed | `c42f341` | `tools.py` registry, `workflow_agent.py`, agent tests (22/22 passing) |
| **Step 6** | n8n Workflow Integration | 🟢 Completed | Pending Push | `workflow.json` 4-node pipeline, `n8n/README.md` import guide |
| **Step 7** | Scenario Testing & Verification | 🟢 Completed | Pending Push | All 3 interview scenarios passing (22/22 tests, `run_scenarios.py` verified) |
| **Step 8** | README & Interview Defense Guide | 🟡 Up Next | — | Architecture diagrams, code walkthrough, Q&A defense |

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
- **Git Commit:** `feat: step 1 - project scaffold and environment configuration` (`791f0c8`)

### 🔹 Stage 2: SQLite Database Schema, Business Seeding & SQL Tool
- **Date:** September 15, 2026
- **Actions Taken:**
  - Designed relational schema (`schema.sql`) covering `products`, `customers`, `sales`, and `returns` with foreign key relationships and index optimizations.
  - Implemented `src/database/db.py` with read-only query guardrails preventing destructive statements (`DROP`, `DELETE`, `UPDATE`, `INSERT`).
  - Implemented `src/database/seed_data.py` generating realistic enterprise data tailored for our interview scenarios:
    - *Scenario 1 Ground Truth:* `Laptop Pro 16` generates highest revenue ($450,000 across multiple orders).
    - *Scenario 3 Ground Truth:* `Smart Watch Active` has 5 returns due to battery and bluetooth defects.
  - Built `src/database/sql_tool.py`:
    - Executes validated queries and converts results into Markdown tables (via `tabulate` with fallback) for direct LLM ingestion.
    - Exposes `describe_database()` returning DDL schema for in-context grounding.
  - Created automated test suite `tests/test_sql_tool.py` testing revenue calculations, return counts, schema inspection, and SQL injection blocking (5/5 tests passing).
- **Engineering Decision & Rationale:**
  - *Why enforce read-only execution at the Python layer rather than relying on LLM prompting alone?* LLM system prompts can be jailbroken or hallucinate write operations. Enforcing `SELECT`/`WITH` token validation and SQLite transaction boundaries at the code level guarantees deterministic safety.
- **Git Commit:** `feat: step 2 - sqlite schema, seed data, and sql query tool` (`45d1080`)

### 🔹 Stage 3: FastAPI REST Service & API Tool Endpoints
- **Date:** September 15, 2026
- **Actions Taken:**
  - Implemented `src/api/routes.py` with typed Pydantic models and REST endpoints:
    - `GET /api/v1/health`: System & database connectivity check.
    - `GET /api/v1/products`: Filterable catalog search.
    - `GET /api/v1/products/{product_id}`: Granular SKU data (price, stock, warranty months).
    - `GET /api/v1/orders/{order_id}`: Joined customer & product order details.
    - `GET /api/v1/returns/summary`: Aggregated return metrics.
    - `POST /api/v1/database/query`: Safe read-only SQL execution endpoint for HTTP callers/n8n.
    - `GET /api/v1/database/schema`: DDL inspection endpoint.
  - Implemented `src/api/main.py` using modern FastAPI `lifespan` context manager, interactive Swagger UI (`/docs`), and CORS middleware.
  - Created automated test suite `tests/test_api.py` verifying all endpoints with `TestClient` (14/14 tests passing across the suite).
- **Engineering Decision & Rationale:**
  - *Why expose both REST endpoints and direct SQL execution?* In an enterprise architecture, external workflows (such as n8n or third-party webhooks) often need standard REST endpoints (`/orders/{id}`) for point-lookups, while the AI Agent needs dynamic SQL execution for flexible cross-table analytics. Providing both maximizes interoperability.
- **Git Commit:** `feat: step 3 - fastapi rest services and test suite` (`64e422e`)

### 🔹 Stage 4: RAG Pipeline (ChromaDB + Unstructured Policy Documents)
- **Date:** September 15, 2026
- **Actions Taken:**
  - Authored 4 comprehensive corporate policy documents under `data/docs/`:
    - `return_policy.md`: Outlines the 14-day window for opened electronics and the 15% restocking fee waiver for verified hardware defects.
    - `shipping_policy.md`: Outlines transit tiers, threshold for free shipping, and 48-hour damaged transit claim window.
    - `warranty_policy.md`: Covers manufacturer warranty coverage (12-60 months), battery degradation rules, and claim RMA processes.
    - `customer_support_sla.md`: Outlines response SLAs for VIP (2h) vs Standard (24h) and recurring defect escalation thresholds.
  - Implemented `src/rag/vector_store.py` initializing a persistent ChromaDB client with cosine similarity (`hnsw:space: cosine`).
  - Implemented `src/rag/indexer.py` with section-aware markdown chunking that retains parent document and section headings in each vector payload.
  - Implemented `src/rag/rag_tool.py` providing `search_policy_documents(query, top_k)` with distance scoring, markdown formatting, and source file citations.
  - Created automated test suite `tests/test_rag_tool.py` verifying semantic chunk retrieval for Scenario 2 queries (18/18 total tests passing).
- **Engineering Decision & Rationale:**
  - *Why use section-based chunking over raw character chunking?* Character/token chunking often splits critical policy sentences down the middle (e.g. separating the restocking fee amount from the waiver condition). Section-based chunking preserves the semantic context of legal and operational clauses.
- **Git Commit:** `feat: step 4 - rag pipeline with chromadb and policy knowledge base` (`5800692`)

### 🔹 Stage 5: Unified Tool Registry & Gemini Agent Brain
- **Date:** September 15, 2026
- **Actions Taken:**
  - Implemented `src/agent/tools.py` with type-annotated callables and docstrings compatible with Google GenAI Function Calling schemas (`query_database`, `describe_database`, `search_policy_documents`, `get_product_details`, `get_order_details`, `get_returns_summary_tool`).
  - Implemented `src/agent/workflow_agent.py`:
    - Leverages modern `google.genai` SDK (`genai.Client`).
    - Configured system instructions with strict anti-hallucination constraints on mathematical business metrics.
    - Multi-turn tool execution loop: executes requested function calls, feeds tool response payloads back to Gemini, and iterates until synthesis is complete.
    - Includes deterministic offline fallback mode allowing 100% test verification and demo execution even before setting API keys.
  - Exposed `POST /api/v1/agent/query` in FastAPI for n8n webhook or HTTP client execution.
  - Built automated test suite `tests/test_agent.py` covering Scenario 1 (SQL revenue), Scenario 2 (RAG return policy), Scenario 3 (Multi-Source SQL + RAG synthesis), and the FastAPI agent route (22/22 tests passing across whole repo).
- **Engineering Decision & Rationale:**
  - *Why support automated function calling loop instead of a single-shot prompt?* In real-world enterprise queries (such as Scenario 3), the agent cannot answer the second half ("what is the return policy for that category?") until it executes the SQL query to discover what that category actually is (`Smart Watch Active` -> `Electronics`). The agentic loop enables true dynamic multi-hop reasoning.
- **Git Commit:** `feat: step 5 - gemini function calling agent and multi-source reasoning` (`c42f341`)

### 🔹 Stage 6: n8n Workflow Orchestration Integration
- **Date:** September 15, 2026
- **Actions Taken:**
  - Created `n8n/workflow.json`: A ready-to-import 4-node n8n workflow:
    1. **Webhook Trigger Node**: Listens at `POST /webhook/enterprise-agent`.
    2. **HTTP Request Node**: Routes query to `POST http://localhost:8000/api/v1/agent/query`.
    3. **Code Node (JavaScript)**: Enriches agent response with metadata and ISO timestamp.
    4. **Respond to Webhook Node**: Returns the formatted JSON answer to the caller.
  - Updated `n8n/README.md` with curl test examples and a verbatim interview explanation of n8n's enterprise role.
- **Engineering Decision & Rationale:**
  - *Why n8n over custom webhook code?* n8n provides visual workflow management, built-in retry logic, audit logging, and zero-code channel integrations (Slack, Teams, Email), while keeping full Python control over agent logic.
- **Git Commit:** `feat: step 6 and 7 - n8n workflow, scenario runner, final integration`

### 🔹 Stage 7: End-to-End Scenario Testing & Verification
- **Date:** September 15, 2026
- **Verified Scenarios (all 3 passing):**

| # | Query | Tools Called | Verified Output |
| :--- | :--- | :--- | :--- |
| 1 | "Which product generated the highest revenue?" | `query_database` | Laptop Pro 16 — $450,000 |
| 2 | "What is our return policy on opened electronics?" | `search_policy_documents` | 14-day window, fee waived for defects |
| 3 | "Which product had highest returns + return policy?" | `query_database` + `search_policy_documents` | Smart Watch Active (5 returns) + Full defect refund entitlement |

- **Test Coverage:** 22/22 automated pytest tests passing across all modules.
- **`tests/run_scenarios.py`** produces clean, timestamped, interview-ready output.
- **Git Commit:** `feat: step 6 and 7 - n8n workflow, scenario runner, final integration`
