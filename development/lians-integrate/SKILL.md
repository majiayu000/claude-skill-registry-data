---
name: lians-integrate
description: Wire Lians memory into an existing agent codebase, test-first and minimal-diff. Use when the user asks to add persistent/compliance memory to their agent, integrate Lians, or replace a vector store with bitemporal memory.
---

# Integrate Lians into this repository

A pipeline skill: add Lians as the memory layer for the agent in **this** repo.
Add a memory layer; don't rewrite the app. Work test-first.

## Procedure

1. **Survey the agent loop.** Find where the model is called, where context is
   assembled, and where a turn completes. Detect the framework in use.

2. **Branch.** `git checkout -b lians-integration` before editing.

3. **Install** the matching package:
   - LangChain → `pip install lians-sdk[langchain]`
   - LangGraph → `pip install lians-sdk[langgraph]`
   - CrewAI → `pip install lians-sdk[crewai]`
   - OpenAI Agents SDK → `pip install lians-sdk[openai-agents]`
   - AutoGen → `pip install lians-sdk[autogen]`
   - raw / unknown → `pip install lians-sdk` (use the harness)

4. **Wire memory in.**

   Raw loop - use the harness:
   ```python
   from lians import LiansClient, LiansMemoryHarness
   harness = LiansMemoryHarness(
       LiansClient(base_url=os.environ["LIANS_URL"], api_key=os.environ["LIANS_API_KEY"]),
       agent_id="<this-agent>",
       domain="finance",   # or healthcare / legal
   )
   # before model call: context = harness.recall_context(user_query)
   # after model call:  harness.remember(response)
   # or both:           answer = harness.run_turn(user_query, generate=call_model)
   ```

   Framework - import its integration module:
   ```python
   from lians.langchain_integration import LiansChatHistory, build_tools
   from lians.langgraph_integration import create_recall_node, create_remember_node
   from lians.crewai_integration import build_crewai_tools
   from lians.openai_agents_integration import build_openai_agent_tools
   from lians.autogen_integration import build_autogen_tools
   ```

5. **Test (required).** Add a test using `LocalLiansClient` (no server/API key)
   that proves: (a) a remembered fact is recalled, and (b) a superseding write
   hides the stale fact from `recall` but `recall_at(as_of=...)` still sees it.
   Run the suite.

6. **Report.** Summarize the diff, the env vars required (`LIANS_URL`,
   `LIANS_API_KEY`, `LIANS_AGENT_ID`), and how to verify locally. **Do not
   commit** - leave the branch for review.

## Guardrails

- Keep the diff small and reversible.
- Store `event_time` as the business time of each fact, not `datetime.now()`,
  wherever the source provides it - point-in-time recall and backtest checks
  depend on it.
- If tests fail, stop and report. Do not declare the integration complete.
