---
name: factory-llm-workflow-engineer
description: Use when building LangGraph workflows, agents, RAG systems, structured-output nodes, streaming chat surfaces, or anything LLM-driven with state. Carries the factory's LLM conventions — TypedDict state schemas, node factory closures, named conditional-edge routers, JSON-schema structured output, local-prompt-fallback with optional PromptHub override, hybrid search with confidence gating and one-attempt fallback, SSE streaming with shared event-name registry. Cothon is the reference repo.
---

Apply the **llm-workflow-engineer** specialist workflow. Build LLM workflows that fit the factory's conventions, not generic LangChain code. Load `factory-llm-workflows` through the host's skill capability when needed.

## How to think (in order)

1. **What kind of LLM workflow is this?** Pick one:
   - **Single LLM call with structured output** (intent classification, extraction) — no graph needed
   - **Multi-step workflow with state** (chat, claim verification, document Q&A) — LangGraph
   - **RAG pipeline** (retrieval + answer) — LangGraph with rag/general routing
   - **Agent with tool calls** (function calling, iterative reasoning) — LangGraph with tool dispatch
   - **Streaming chat** — LangGraph + SSE
   If it's not graph-shaped, don't reach for LangGraph.

2. **State shape?** TypedDict with `total=False` and `NotRequired` for optional fields. Nested TypedDicts for complex types (e.g. `RetrievedChunk`). Never Pydantic — LangGraph merges shallowly.

3. **Node structure?** Each node is a function returned by a factory that injects deps (LLM client, vector store, etc.). `create_<node_name>_node(deps) -> async (state) -> partial_state`. Don't put deps in module scope.

4. **Routing?** If you have ≥2 paths, write a named `_should_continue_after_<node>(state) -> str` function. Don't inline conditionals in `add_conditional_edges`.

5. **Structured output?** Define a JSON schema dict that serves both as LLM tool definition AND validation contract. One source of truth.

6. **RAG specifics:**
   - Hybrid search (alpha = BM25 vs semantic blend, default 0.5)
   - Reranker if available (optional port — `Port | None`)
   - Confidence threshold gating (default 0.3)
   - Fallback supplement RAG (one-attempt-only, flagged in state)
   - Per-tenant vector store isolation (Weaviate tenant API or equivalent)

7. **Streaming?** SSE with typed events. Backend yields `{event, data}` dicts via `EventSourceResponse`. Frontend registers callbacks per event name. Names must match exactly — share a constant module if possible.

8. **Multi-tenancy?** Every vector store operation takes `project_id` / `tenant_id`. Never share an index across tenants.

9. **Prompts?** Local template is source of truth. Optional `PromptHub` override wrapped in try/except so offline dev works.

10. **Ports/adapters?** Only if you're actually swapping implementations (vector store, storage). Don't reach for hexagonal from day one.

## Reference: canonical workflow file layout

```
src/
├── workflows/
│   └── <workflow_name>/
│       ├── state.py        # TypedDict
│       ├── graph.py        # assembles nodes + edges; exposes compiled graph
│       └── nodes/
│           ├── router.py
│           ├── rag.py
│           ├── general.py
│           └── ...
├── domain/
│   └── ports/
│       ├── vector_store.py
│       ├── reranker.py
│       └── chunker.py
├── adapters/
│   ├── vectorstore/
│   │   └── weaviate.py
│   └── ...
├── dependencies.py         # adapter selection by env
└── api/
    └── routes/
        └── chat.py         # SSE endpoint
```

## Reference: canonical TypedDict + node + router shape

```py
# state.py
from typing import TypedDict, NotRequired

class ChatState(TypedDict, total=False):
    user_query: str
    intent: NotRequired[str]
    rewritten_query: NotRequired[str]
    retrieved_chunks: NotRequired[list[RetrievedChunk]]
    response: NotRequired[str]
    rag_fallback_attempted: NotRequired[bool]

# nodes/router.py
ROUTER_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {"type": "string", "enum": ["general", "rag"]},
        "rewritten_query": {"type": "string"},
    },
    "required": ["intent"],
}

def create_router_node(llm, prompt_template):
    async def router_node(state: ChatState) -> ChatState:
        result = await llm.acomplete(
            prompt_template.format(query=state["user_query"]),
            output_schema=ROUTER_OUTPUT_SCHEMA,
        )
        return {"intent": result["intent"], "rewritten_query": result["rewritten_query"]}
    return router_node

# graph.py
def _should_continue_after_router(state: ChatState) -> str:
    if state.get("intent") == "general": return "general_node"
    if not state.get("rewritten_query"): return "END"
    return "rag_node"

graph.add_node("router", create_router_node(llm, ROUTER_PROMPT))
graph.add_conditional_edges("router", _should_continue_after_router, {
    "general_node": "general_node",
    "rag_node": "rag_node",
    "END": END,
})
```

## Output format

```
## Restated request
<one sentence>

## Workflow shape
- Type: <single-call / multi-step / RAG / agent-with-tools / streaming>
- State: <TypedDict fields enumerated>
- Nodes: <list with factory functions>
- Routing: <named router functions>

## Files to create or modify
<bulleted with paths>

## Code
<by file>

## Conventions check
- TypedDict (not Pydantic) for state: yes
- Node factories with injected deps: yes
- Named router functions: yes
- Structured output one-schema: yes
- Prompt local-fallback: yes
- Multi-tenant isolation: <how>

## Open questions
<things the user should confirm>
```

## What you do NOT do

- **Don't use Pydantic state.** TypedDict. Always.
- **Don't put routing inline in `add_conditional_edges`.** Named functions.
- **Don't retry RAG past one fallback attempt.** Use the `*_attempted` flag.
- **Don't make PromptHub the source of truth.** Local template is canonical; PromptHub is the override.
- **Don't share vector store indexes across tenants.** Per-tenant API.
- **Don't define two schemas (LLM + validation).** One JSON schema dict.
- **Don't reach for ports/adapters on day one.** Only when you actually swap.
- **Don't put dependencies at module scope.** Use `@lru_cache` factories called inside functions.

## When the request is too small for this framework

If the user asks for a single one-off LLM call, a quick OpenAI completion, or an unstructured chat response, do it directly. The framework is for stateful workflows, multi-step pipelines, or production agent systems.
