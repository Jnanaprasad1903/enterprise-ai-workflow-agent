"""
Enterprise AI Workflow Agent -- End-to-End Interview Scenarios Runner
Run: python tests/run_scenarios.py
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.database.seed_data import seed_database
from src.rag.indexer import index_all_documents
from src.agent.workflow_agent import EnterpriseWorkflowAgent

def banner(title: str):
    print("\n" + "=" * 80)
    print(f"  >>> {title}")
    print("=" * 80)

def print_result(res: dict):
    tools = res.get("tools_used", [])
    print(f"\n[?] User Query    : {res['query']}")
    print(f"[>] Tools Invoked : ({len(tools)}) -> {', '.join(tools) if tools else 'None'}")
    print(f"[T] Timestamp     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if res.get("execution_trace"):
        print("\n[TRACE] Agent Execution Steps:")
        for step in res["execution_trace"]:
            print(f"   Step {step.get('step')}: Tool='{step.get('tool')}'")
            if "arguments" in step:
                for k, v in step["arguments"].items():
                    preview = str(v)[:80].replace('\n', ' ')
                    print(f"           {k}: {preview}")
            elif "sql" in step:
                sql_preview = step['sql'].replace('\n', ' ').strip()[:80]
                print(f"           SQL: {sql_preview}")

    print("\n[ANSWER] Synthesized Executive Answer:\n")
    print(res["answer"])
    print("\n" + "-" * 80)

def main():
    print("\n[*] Initializing Enterprise AI Workflow Agent Demo Environment...")
    seed_database()
    index_all_documents()
    print("[+] Database seeded and RAG knowledge base indexed.\n")

    agent = EnterpriseWorkflowAgent()

    # -------------------------------------------------------------------------
    # SCENARIO 1: Structured SQL Query Only
    # -------------------------------------------------------------------------
    banner("SCENARIO 1: Structured Business Query (SQL Tool Only)")
    q1 = "Which product generated the highest revenue?"
    res1 = agent.run(q1)
    print_result(res1)

    # -------------------------------------------------------------------------
    # SCENARIO 2: Unstructured Knowledge Retrieval Only (RAG)
    # -------------------------------------------------------------------------
    banner("SCENARIO 2: Unstructured Company Knowledge (RAG Tool Only)")
    q2 = "What is our policy on returning opened electronics?"
    res2 = agent.run(q2)
    print_result(res2)

    # -------------------------------------------------------------------------
    # SCENARIO 3: Multi-Source Agentic Reasoning (SQL + RAG Synthesis)
    # -------------------------------------------------------------------------
    banner("SCENARIO 3: Multi-Source Reasoning (SQL + RAG Combined)")
    q3 = "Which product had the highest returns, and what does our return policy say about returning that category?"
    res3 = agent.run(q3)
    print_result(res3)

    print("\n[OK] All 3 Core Interview Scenarios Executed Successfully!\n")

if __name__ == "__main__":
    main()
