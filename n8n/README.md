# ⚙️ n8n Workflow Orchestration Guide

This guide explains how **n8n** is used as the **workflow orchestration layer** for the Enterprise AI Workflow Agent.

---

## 🏛️ High-Level Orchestration Architecture

```text
  [Slack / Teams / Client]
             │
             │ (POST { "query": "..." })
             ▼
  ┌────────────────────────────────────────────────────────┐
  │                 n8n Workflow Engine                    │
  │                                                        │
  │  1. Webhook Trigger Node                               │
  │     └─ Ingests request & validates payload             │
  │                                                        │
  │  2. HTTP Request Node                                  │
  │     └─ Calls FastAPI Agent (/api/v1/agent/query)       │
  │                                                        │
  │  3. Code / Transformation Node                         │
  │     └─ Enriches metadata, traces, and metrics          │
  │                                                        │
  │  4. Webhook Response Node                              │
  │     └─ Dispatches clean markdown response back to user │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
              ┌─────────────────────────────┐
              │    FastAPI Agent Backend    │
              │      (Port 8000)            │
              │                             │
              │  ┌───────────────────────┐  │
              │  │  Gemini Tool Calling  │  │
              │  └──────────┬────────────┘  │
              │             │               │
              │     ┌───────┴───────┐       │
              │     ▼               ▼       │
              │  [SQLite]        [ChromaDB] │
              │   (SQL)            (RAG)    │
              └─────────────────────────────┘
```

---

## 📥 How to Import `workflow.json` into n8n

1. **Launch your n8n instance** (Desktop app, Docker, or Cloud):
   ```bash
   # Optional: Launch via npx
   npx n8n
   # Or via Docker
   docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
   ```
2. Open your n8n editor at `http://localhost:5678`.
3. In the top right menu, click **Add Workflow** > **Import from File...** (or press `Ctrl+O`).
4. Select `d:/Office_agent/n8n/workflow.json`.
5. The 4 connected nodes will appear on your canvas:
   * **Webhook Trigger (User Query)**
   * **HTTP Request (FastAPI Agent)**
   * **Format Business Response**
   * **Respond to Webhook**
6. Click **Save** and toggle the workflow to **Active** (or click **Test step / Listen for event**).

---

## 🧪 Testing the n8n Webhook

### Scenario 1: Structured Query
```bash
curl -X POST http://localhost:5678/webhook/enterprise-agent \
  -H "Content-Type: application/json" \
  -d '{"query": "Which product generated the highest revenue?"}'
```

### Scenario 2: Unstructured Policy Query
```bash
curl -X POST http://localhost:5678/webhook/enterprise-agent \
  -H "Content-Type: application/json" \
  -d '{"query": "What is our policy on returning opened electronics?"}'
```

### Scenario 3: Multi-Source Reasoning Query
```bash
curl -X POST http://localhost:5678/webhook/enterprise-agent \
  -H "Content-Type: application/json" \
  -d '{"query": "Which product had the highest returns, and what does our return policy say about returning that category?"}'
```

---

## 🎤 Interview Explanation ("Why did you use n8n?")

> *"In production enterprise systems, you never expose internal LLM or database code directly to external channels like Slack, Teams, or client frontend applications.*
> 
> *I used **n8n as the workflow orchestration layer** to handle:
> 1. **Ingress & Authentication:** Secure webhook endpoints with rate limiting and token validation.
> 2. **Service Decoupling:** Isolating the external communication channel from our Python/FastAPI agent core.
> 3. **Auditing & Observability:** Every execution step, input, tool response, and latency metric is logged and visually monitorable inside n8n.*
> 4. **Multi-Channel Distribution:** Once the agent synthesizes the answer, n8n can simultaneously reply to the user on Slack, create an escalation ticket in Jira, or trigger an email alert if return rates exceed threshold."*
