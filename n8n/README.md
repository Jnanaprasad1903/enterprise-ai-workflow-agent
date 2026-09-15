# ⚙️ n8n Workflow Integration

This directory contains the orchestration resources for the Enterprise AI Workflow Agent.

## Overview
The n8n workflow operates as the **Ingress & Orchestration Layer**:
1. **Webhook / Chat Trigger**: Listens for user queries from Slack, Teams, or HTTP clients.
2. **AI Agent / HTTP Node**: Forwards the query to our FastAPI Agent (`POST /api/v1/agent/query`).
3. **Response Node**: Formats the synthesized response and returns it to the user.

## Files
- `workflow.json`: Exported n8n workflow definition ready to import into any local or cloud n8n instance.
- `README.md`: Step-by-step import and execution instructions.
