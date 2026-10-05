---
name: factory-llm-workflows
description: LLM workflow conventions distilled from production agent/RAG work. Covers LangGraph TypedDict state schemas, node factory closures, conditional edge routing, structured output via JSON schema, prompt fallback patterns with optional PromptHub override, hybrid search with confidence gating + fallback supplement, SSE streaming with event dispatch, hexagonal ports/adapters when scale justifies. Read when building any LLM-driven workflow with state, tool calls, or streaming UX.
---

# Factory LLM workflows

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint → option → tradeoff), then **Recipe** (the LangGraph / FastAPI / SSE shape we use), and **Failure mode** when there's one to name. Sections that are pure style with no deeper truth are marked `Recipe only`.

## State shape — TypedDict, not Pydantic

**Principle.** LangGraph state is a TypedDict, not Pydantic. The state library's merge semantics dictate the shape.

**Why.** LangGraph merges state between nodes by shallow dict update — the framework expects a dict-like object whose fields are independently updatable. Pydantic validates on construction; every partial update fails validation or requires `.model_copy(update=...)`, which loses the simplicity. TypedDict matches the framework's semantics: it's a dict, fields are optional via `total=False`, the type annotations are documentation that the type checker enforces at call sites.

**Recipe.**

```py
from typing import TypedDict
from typing_extensions import NotRequired

class ChatState(TypedDict, total=False):
    """Documented fields. total=False makes everything optional."""
    user_query: str
    intent: NotRequired[str]
    rewritten_query: NotRequired[str]
    retrieved_chunks: NotRequired[list[RetrievedChunk]]
    response: NotRequired[str]
    rag_fallback_attempted: NotRequired[bool]  # one-attempt loop guards
```

Nested TypedDicts (`RetrievedChunk`, `EvidenceChunk`, `ClaimVerdict`) for complex types.

**Failure mode.** Reaching for Pydantic state because "Pydantic is more rigorous" — every node update became a `.model_copy(update=...)` dance, and the graph wiring drowned in validation noise.

## Graph composition — node factory closures

**Principle.** Nodes are produced by factory functions that close over their dependencies; the graph wires the result.

**Why.** A node that imports its dependencies (LLM client, prompt template, retriever) at module scope is hard to test and impossible to swap. A factory function takes dependencies as parameters and returns a callable; the graph passes the factory the wired-up dependencies. Testing is "construct the node with mocks"; swapping is "construct the node with the alternative."

**Recipe.**

```py
def create_router_node(
    llm: LLM,
    prompt_template: str,
) -> Callable[[ChatState], Awaitable[ChatState]]:
    async def router_node(state: ChatState) -> ChatState:
        result = await llm.acomplete(
            prompt_template.format(query=state["user_query"]),
            output_schema=ROUTER_OUTPUT_SCHEMA,
        )
        return {"intent": result["intent"], "rewritten_query": result["rewritten_query"]}
    return router_node

# graph.py assembles:
graph.add_node("router", create_router_node(llm, ROUTER_PROMPT))
```

## Conditional edges — named router functions

**Principle.** Routing logic lives in named functions, not inline conditionals in `add_conditional_edges`.

**Why.** Inline routing logic in the graph builder is unreadable (deeply nested ternaries) and untestable (the graph has to be constructed to test one branch). A named function takes state, returns the next node's name, and is unit-testable in isolation. The graph builder becomes a one-line wire-up.

**Recipe.**

```py
def _should_continue_after_router(state: ChatState) -> str:
    if state.get("intent") == "general":
        return "general_node"
    if not state.get("rewritten_query"):
        return "END"
    return "rag_node"

graph.add_conditional_edges("router", _should_continue_after_router, {
    "general_node": "general_node",
    "rag_node": "rag_node",
    "END": END,
})
```

## Structured output — one JSON schema, two uses

**Principle.** A single JSON schema dict drives both the LLM instruction and the validation contract. Never define two.

**Why.** Defining the LLM tool schema in one place and the validation schema in another guarantees they drift — somebody adds a field to the LLM instruction, forgets the validator, and the validator silently passes outputs that no longer match. One schema, two uses: the LLM gets it as tool definition, the validator gets it as schema. Drift is impossible by construction.

**Recipe.**

```py
ROUTER_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {"type": "string", "enum": ["general", "rag", "claim_verify"]},
        "rewritten_query": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    },
    "required": ["intent", "confidence"],
}
```

## Prompts — local string is the truth; remote override is optional

**Principle.** The local prompt string is the source of truth; PromptHub (or any remote prompt service) is an optional override.

**Why.** A remote prompt service as the source of truth means offline dev doesn't work, CI can't run without network, and a service outage breaks the whole workflow. Local string as truth, remote as override: offline dev works, CI works, and the override is available when you genuinely want to A/B prompts in production without redeploying.

**Recipe.**

```py
ROUTER_PROMPT = """You are an intent classifier...
Examples:
- "what is X?" -> general
- "how does our team handle X?" -> rag
Output a JSON object matching the schema."""

async def get_router_prompt(prompt_hub: PromptHub | None) -> str:
    if prompt_hub:
        try:
            return await prompt_hub.get("router")
        except Exception:
            pass
    return ROUTER_PROMPT
```

## RAG — confidence gating + one-attempt fallback

**Principle.** RAG retrieval has a confidence threshold below which it tries one fallback supplement; never retry past one attempt.

**Why.** A retrieval that returns nothing useful is a signal — either the question is out of scope or the index is missing relevant chunks. Trying a broader search once gives the system one more shot before degrading gracefully. Retrying without a guard creates an infinite loop or a runaway cost spike. The `*_attempted` flag in state is the explicit guard.

**Recipe.**

```py
async def rag_node(state: ChatState) -> ChatState:
    chunks = await vector_store.hybrid_search(
        query=state["rewritten_query"],
        alpha=0.5,                          # BM25 vs semantic blend
        top_k=10 * TOP_K_MULTIPLIER,        # over-fetch for reranker
    )
    if reranker is not None:
        chunks = await reranker.rerank(state["rewritten_query"], chunks, top_k=10)

    # Confidence gating
    confident_chunks = [c for c in chunks if c.score >= CONFIDENCE_THRESHOLD]  # default 0.3
    if not confident_chunks and not state.get("rag_fallback_attempted"):
        return {"retrieved_chunks": [], "needs_fallback": True}

    return {"retrieved_chunks": confident_chunks}
```

`rag_fallback_attempted: True` flag prevents loops.

## Streaming — SSE with a shared event-name registry

**Principle.** Backend and frontend share an event-name registry; names must match exactly.

**Why.** SSE events are stringly-typed by nature — backend emits `"token"`, frontend dispatches on `"token"`. A typo on either side silently drops the event. The fix is a shared constant file (hand-maintained if the languages differ); the LLM workflow has too many events to leave names ad-hoc.

**Recipe.**

```py
@router.get("/chat/stream")
async def chat_stream(request: Request):
    async def event_generator():
        yield {"event": "status", "data": "starting"}
        async for chunk in workflow.astream(state):
            if "token" in chunk: yield {"event": "token", "data": chunk["token"]}
            if "intent" in chunk: yield {"event": "intent", "data": chunk["intent"]}
            if "sources" in chunk: yield {"event": "sources", "data": json.dumps(chunk["sources"])}
        yield {"event": "done", "data": ""}
    return EventSourceResponse(event_generator())
```

```ts
const eventHandlers: Record<string, (data: string) => void> = {
  status: (data) => setStatus(data),
  intent: (data) => setIntent(data),
  sources: (data) => setSources(JSON.parse(data)),
  token: (data) => appendToken(data),
  done: () => setDone(true),
  error: (data) => setError(data),
};
```

TypeScript codegen from Python is overkill; a hand-maintained const file is fine.

## Hexagonal ports/adapters — only when scale justifies

**Principle.** Reach for ports/adapters only when you actually need to swap the implementation; don't pre-build the abstraction.

**Why.** Ports/adapters from day one is an abstraction tax paid up front with no benefit. The right time to introduce a `StoragePort` is when there are two concrete storage backends, or one production backend and one local-dev fake. Before that, the interface adds indirection and code without justification.

**Recipe.**

```py
def get_storage() -> StoragePort:
    if settings.s3_bucket_name:
        return S3Storage(settings.s3_bucket_name)
    return FilesystemStorage(settings.local_storage_path)
```

Optional ports (`Port | None`) work for things like reranker where the caller checks before use.

## Multi-tenant vector store — per-tenant indexes

**Principle.** Never share a vector index across tenants; use the vector store's tenant API or one index per tenant.

**Why.** A shared index with app-level RBAC filtering is one missing filter away from cross-tenant retrieval. Vector store tenant APIs (Weaviate, Pinecone namespaces) enforce isolation at the infrastructure layer, where the failure mode is "no results" instead of "wrong tenant's results." The cost of per-tenant isolation is tenant-management overhead; the cost of not is a privacy incident.

**Recipe.**

```py
async def search(self, query: str, project_id: str, top_k: int) -> list[Chunk]:
    return await self._client.tenant(project_id).query(/* ... */)
```

## Token-based chunking with overlap

**Recipe only** — `tiktoken` for counting, sliding window with `max_token_limit` (e.g. 512) + `token_overlap` (e.g. 50), hierarchical markdown chunker preserves header tree as breadcrumbs, tables and code blocks are atomic (don't split mid-table).

## Lazy DI with `@lru_cache`

**Principle.** Heavy dependencies (vector store clients, LLM clients, reranker models) load lazily inside functions, not at module import.

**Why.** Module-scope imports of heavy clients mean tests can't import the module without paying the client-construction cost — including any network calls the client makes at construction. Lazy import + `@lru_cache` defers the cost to first call and keeps tests fast.

**Recipe.**

```py
@lru_cache
def get_vector_store() -> VectorStorePort:
    from .adapters.vectorstore.weaviate import WeaviateAdapter
    return WeaviateAdapter(...)
```

## Version anything editable later

**Principle.** Anything the user might edit later (claims, prompts, generated artifacts) is versioned from day one; retrofitting versioning is expensive.

**Why.** Editing without versioning is destructive — the old value is gone, audit trails are broken, undo is impossible. Versioning is cheap up front: one `version` column or one parent-child link. Retrofitting it means migrating existing rows into a versioned model and rewriting every read.

**Recipe.** Use a `claim_versions` table keyed by `claim_id`; the "current" version is the latest by `created_at` or by an explicit `is_current` flag.

**Failure mode.** Chat messages stored append-only but claims versioned in the same project — the inconsistency meant message editing, when it became a feature, was a full migration.

## Source patterns

All from cothon — the strongest single-source domain in the kit. Reference repo for any new LLM/agent work.

## Related

- `factory-verification.md` — verifies the *factory's own output* (L1/L3). Evaluating a shipped LLM feature — golden datasets, LLM-as-judge, regression runs (L2) — is a distinct problem, deferred but named there. When the L2 companion is built, it pairs with this skill.
