---
name: building-agent-memory
description: Memory patterns for multi-turn, multi-session agents — buffer, summary, vector-backed semantic/episodic, hierarchical working/short/long-term, consolidation.
when_to_use: >
  Reach for this when an agent needs state that survives beyond a single completion — chat history
  longer than the context window, user preferences carried across sessions, episodic recall of
  past interactions, or hierarchical working/short/long-term memory. For the *vector backend*
  use using-pgvector or using-weaviate; for the *retrieval architecture* itself use
  building-rag-pipelines; for *stateful graph checkpointing* use building-langgraph-agents;
  for *provider-native* short-term memory primitives (prompt caching, context windows) defer to
  using-anthropic-platform / using-openai-platform; for *observability* of memory operations use
  using-langfuse. **ALWAYS WebFetch the current provider docs (Anthropic prompt caching, OpenAI
  Responses/conversation state, LangGraph checkpointers) BEFORE recommending a specific memory
  primitive — these features ship and rename faster than any training snapshot.**
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Building Agent Memory — Quick Reference

Agents need memory beyond a single LLM call. This skill catalogues the standard memory
*patterns* — provider-agnostic — and shows how to compose them with vector stores, graph
checkpointers, and provider-native primitives.

---

## Stay current — DO NOT rely on training-data knowledge of memory primitives

Provider-native memory features (Anthropic prompt caching tiers and the `memory` tool, OpenAI
Responses API conversation state, LangGraph `Checkpointer` interfaces) are rapidly evolving.
The names, shapes, and pricing change between releases. **Before** you (a) recommend a
provider-native memory feature, (b) cite a cache TTL/price, (c) pick a checkpointer backend,
(d) wire a long-term store integration, or (e) claim "X model supports Y memory", you **MUST**
WebFetch the live source and cite it:

- **Anthropic prompt caching:** https://docs.claude.com/en/docs/build-with-claude/prompt-caching
- **Anthropic Memory tool (if/when available):** https://docs.claude.com/en/docs/agents-and-tools/
- **OpenAI Responses / conversation state:** https://platform.openai.com/docs/guides/responses
- **LangGraph checkpointers & memory:** https://langchain-ai.github.io/langgraph/concepts/persistence/
- **LangGraph memory store:** https://langchain-ai.github.io/langgraph/concepts/memory/

Cite source URL + fetch date for every provider-native feature you reference. Defer model
selection and capability claims to the provider skill's own Stay-current. For the *vector store
backing* a long-term semantic memory, defer to `using-pgvector` / `using-weaviate`. For
*retrieval mechanics* used by memory recall, defer to `building-rag-pipelines`.

---

## When to Use

Load this skill when:
- Building a chatbot/agent with multi-turn context that exceeds the model's window
- User preferences or facts must persist across sessions
- The agent needs to "remember" past interactions episodically
- You see code like `memory.add(...)`, `chat_history`, `summarize_messages`, `checkpointer`
- Dependencies: `langchain.memory`, `langgraph.checkpoint`, `mem0`, `letta`/`memgpt`

---

## Memory Taxonomy

| Type | Lifetime | Stored as | Example |
|------|----------|-----------|---------|
| **Working** | Single turn | Tokens in current prompt | The model's attention over current context |
| **Short-term** | Session | Message buffer / summary | Last N messages of a chat |
| **Long-term semantic** | Indefinite | Facts in vector store | "User is allergic to peanuts" |
| **Long-term episodic** | Indefinite | Events in vector store | "On 2026-05-01, user asked about X" |
| **Procedural** | Indefinite | Tool / skill definitions | How to look up a flight |
| **Profile** | Indefinite | Structured K/V | `{name, timezone, prefs}` |

Most production agents need **at least** short-term buffer + long-term semantic.

---

## Pattern 1 — Conversation Buffer (short-term)

Simplest pattern: keep the last N messages.

```python
class BufferMemory:
    def __init__(self, max_messages: int = 20):
        self.messages: list[dict] = []
        self.max = max_messages

    def append(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self.messages = self.messages[-self.max:]

    def as_prompt(self) -> list[dict]:
        return self.messages
```

**Limit**: blows past context window for long sessions. Combine with summarization (below).

---

## Pattern 2 — Summarization Memory (short-term, compressed)

When buffer exceeds a threshold, summarize older messages into a "running summary" and discard
the raw turns.

```python
def maybe_compact(messages: list[dict], threshold_tokens: int, summary: str) -> tuple[list[dict], str]:
    if count_tokens(messages) < threshold_tokens:
        return messages, summary
    # Summarize oldest half
    half = len(messages) // 2
    old, recent = messages[:half], messages[half:]
    new_summary = llm_summarize(prior_summary=summary, messages=old)
    return recent, new_summary
```

System prompt then contains the running summary:

```
You are an agent. Conversation summary so far:
{summary}

Recent messages follow.
```

**Tradeoff**: cheap; loses verbatim detail. Pair with long-term semantic memory for facts you
must retain exactly.

---

## Pattern 3 — Vector-Backed Long-Term Memory (semantic / episodic)

Persist facts as embedded chunks; recall by similarity to the current turn.

```python
class SemanticMemory:
    def __init__(self, store, embedder):
        self.store = store          # pgvector / weaviate / etc.
        self.embed = embedder

    def remember(self, user_id: str, fact: str, kind: str = "semantic"):
        vec = self.embed(fact)
        self.store.upsert(
            namespace=user_id,
            text=fact,
            embedding=vec,
            metadata={"kind": kind, "ts": now()},
        )

    def recall(self, user_id: str, query: str, k: int = 5) -> list[str]:
        vec = self.embed(query)
        hits = self.store.search(namespace=user_id, embedding=vec, top_k=k)
        return [h.text for h in hits]
```

Inject recalled facts into the prompt:

```
Relevant memories about this user:
- {memory_1}
- {memory_2}

Conversation:
{messages}
```

See `building-rag-pipelines` for chunking / retrieval mechanics — memory recall **is** RAG with
the user as the corpus owner.

---

## Pattern 4 — Hierarchical Memory (working / short / long)

Inspired by MemGPT/Letta — the agent itself decides what to evict and what to consolidate.

```
┌─ Working memory (in-context) ──────────────────────────────┐
│  system prompt + running summary + last N turns + recalls  │
└────────────────────────────────────────────────────────────┘
                       │ overflow
                       ▼
┌─ Short-term store (session buffer) ────────────────────────┐
│  All messages this session, in order                       │
└────────────────────────────────────────────────────────────┘
                       │ consolidate (end of session / async)
                       ▼
┌─ Long-term store (vector + structured profile) ────────────┐
│  Facts, episodes, preferences, durable across sessions     │
└────────────────────────────────────────────────────────────┘
```

The agent gets tools: `memory.save(fact)`, `memory.search(query)`, `memory.forget(id)`.

---

## Pattern 5 — Structured Profile (key-value)

For typed facts (name, timezone, preferences), don't use a vector store — use a row.

```python
@dataclass
class UserProfile:
    user_id: str
    name: str | None = None
    timezone: str | None = None
    preferences: dict = field(default_factory=dict)
```

Update via tool calls. Cheaper, deterministic, queryable. Vector memory is for things you can't
schematize.

---

## Pattern 6 — Memory-of-Memory (Consolidation)

Periodic background job that reads recent episodes and writes summarized/deduped facts back to
semantic memory. Prevents long-term store from exploding with low-value entries.

```python
def consolidate(user_id: str, since: datetime):
    episodes = store.recent(user_id, since=since, kind="episodic")
    facts = llm_extract_facts(episodes)            # "User prefers dark mode"
    for fact in facts:
        if not store.has_similar(user_id, fact, threshold=0.92):
            store.upsert(user_id, fact, kind="semantic")
```

Run nightly or on session-end. Use `using-celery` or LangGraph background tasks.

---

## Provider-Native Primitives

These complement, not replace, the patterns above. **Verify currency via WebFetch.**

| Provider | Primitive | What it does |
|----------|-----------|--------------|
| Anthropic | Prompt caching | Caches large static prefix (system, RAG context) — cheap "working memory" |
| Anthropic | `memory` tool (beta) | Provider-managed memory operations — verify availability |
| OpenAI | Responses API conv state | Server-side conversation thread — verify shape |
| OpenAI | Assistants API threads | Older; check deprecation status |
| LangGraph | `Checkpointer` | Persists graph state (in-memory, SQLite, Postgres, Redis) |
| LangGraph | `Store` | Cross-thread long-term memory |

**Rule**: pair a provider's caching primitive (working memory) with your own store-backed
long-term memory. Don't rely on provider session features as your only memory layer.

---

## Raw SDK Loop with Memory (Python)

```python
def chat_turn(user_id: str, user_msg: str) -> str:
    profile = profiles.get(user_id)
    recalls = semantic.recall(user_id, user_msg, k=5)
    session.append("user", user_msg)
    msgs, session.summary = maybe_compact(session.messages, 8000, session.summary)

    system = build_system_prompt(profile=profile, summary=session.summary, recalls=recalls)
    response = llm.complete(system=system, messages=msgs)

    session.append("assistant", response.text)
    # Optionally extract & save new facts:
    for fact in extract_facts(user_msg, response.text):
        semantic.remember(user_id, fact)
    return response.text
```

---

## LangGraph Node with Memory

```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.postgres import PostgresSaver

def recall_node(state):
    state["context"] = semantic.recall(state["user_id"], state["input"], k=5)
    return state

def answer_node(state):
    prompt = render(state["context"], state["input"])
    state["answer"] = llm.complete(prompt)
    return state

graph = StateGraph(State)
graph.add_node("recall", recall_node)
graph.add_node("answer", answer_node)
graph.add_edge("recall", "answer")
app = graph.compile(checkpointer=PostgresSaver.from_conn_string(DSN))
```

The `Checkpointer` handles short-term per-thread state; your semantic store handles long-term.

---

## Security & Privacy

Memory is a privacy hotspot. Build these in from day one:

- **PII redaction at write.** Run PII detectors on facts before embedding/storing.
- **Per-user namespacing.** Never share a vector index across users without strict filters.
- **Right-to-be-forgotten.** Expose `delete_all_memory(user_id)` — must hit every store.
- **Retention policy.** TTL on episodic entries; consolidate or evict.
- **Audit log.** Every save/recall — see `using-langfuse` for tracing.
- **Encryption at rest.** Vector stores should encrypt; provider features inherit provider TOS.
- **Tenancy boundaries.** In multi-tenant SaaS, tenant_id filter is mandatory and tested.

---

## Common Patterns

- **Buffer + summary + recall** is the workhorse trio for most chatbots.
- **Write-on-write, read-on-every-turn** — save async after responding; recall synchronously
  before responding.
- **Tool-gated memory** — let the model call `save_memory(fact)` only when explicitly asked
  ("remember that…"). Higher precision than auto-extraction.
- **Hybrid retrieval for memory recall** — same RRF / rerank stack as RAG. See
  `building-rag-pipelines`.

---

## Anti-Patterns

- **Stuffing the whole session into every prompt.** Costs scale O(n²); compress.
- **Treating embeddings as a database.** Use a structured profile for typed facts.
- **No eviction policy.** Memory store grows unbounded; recall quality degrades.
- **Sharing memory across users.** Privacy incident waiting to happen.
- **Trusting the model to "remember" via instruction.** It won't; persist explicitly.
- **No observability.** When recall surfaces something weird, you can't debug without traces.

---

## See Also

- `building-rag-pipelines` — retrieval mechanics shared with semantic memory recall.
- `using-pgvector` / `using-weaviate` — vector backends.
- `building-langgraph-agents` — `Checkpointer` + `Store` for stateful agent graphs.
- `using-anthropic-platform` — prompt caching as a working-memory primitive.
- `using-openai-platform` — Responses API conversation state.
- `building-tool-orchestration` — expose `save_memory` / `recall_memory` as tools.
- `using-langfuse` — trace memory operations end-to-end.
- `using-celery` — background consolidation jobs.
