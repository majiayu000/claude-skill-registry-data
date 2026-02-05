---
name: langgraph-v1
description: >
  Use when writing or refactoring Python code for LangGraph v1.x + LangChain v1:
  Graph API + Functional API import paths, checkpoint/store usage, and migrations off deprecated prebuilts
  (create_react_agent -> langchain.agents.create_agent).
---

# LangGraph v1 + LangChain v1 (Python): delta-only notes for writing valid v1 code

## 0) Version + Python floor

- Assume Python 3.10+ (LangGraph v1 drops 3.9).
- Upgrade baseline:
  - `pip install -U langgraph langchain-core`

## 1) LangGraph Graph API is stable (mostly unchanged)

- Graph API imports remain:
  - `from langgraph.graph import START, END, StateGraph`

## 2) LangGraph Functional API exists (v1 docs-first path)

- Entrypoints are defined via:
  - `from langgraph.func import entrypoint`
- Entrypoint function must accept **one positional input argument** (use a dict if multiple inputs are needed).
- Entrypoints can request injectable params by name + type annotation:
  - `previous`, `store`, `writer`, `config`
- Common v1 import paths shown in docs/examples:
  - `from langgraph.store.base import BaseStore`
  - `from langgraph.store.memory import InMemoryStore`
  - `from langgraph.checkpoint.memory import InMemorySaver`

## 3) Checkpointing / persistence packages and imports

- In-memory checkpointer:
  - `from langgraph.checkpoint.memory import InMemorySaver`
- SQLite/Postgres checkpointers are separate installables:
  - `langgraph-checkpoint-sqlite` (SqliteSaver / AsyncSqliteSaver)
  - `langgraph-checkpoint-postgres` (PostgresSaver / AsyncPostgresSaver)
- (If using custom serialization) serde lives under:
  - `langgraph.checkpoint.serde.*`

## 4) LangGraph v1 deprecations (replace these)

LangGraph v1 is backwards compatible overall, but deprecates specific agent/runtime helpers:

### 4.1) `MessageGraph` (deprecated) → `StateGraph` + `messages` key

- Replace `MessageGraph` usage with `StateGraph` and a state that contains a `messages` key.

### 4.2) `ValidationNode` (deprecated)

- If you were using `langgraph.prebuilt.ValidationNode`, prefer LangChain v1 `create_agent` tool validation + middleware error handling (see section 5).

### 4.3) Agent prebuilt + agent state moved out of LangGraph

- Deprecated in LangGraph v1:
  - `langgraph.prebuilt.create_react_agent`
  - `langgraph.prebuilt.AgentState` and pydantic variants
  - LangGraph interrupt TypedDicts (HumanInterruptConfig / ActionRequest / HumanInterrupt)
- Replacements live in LangChain v1:
  - `from langchain.agents import create_agent`
  - `from langchain.agents import AgentState`
  - interrupt types: `from langchain.agents.interrupt import HumanInterruptConfig, ActionRequest, HumanInterrupt`

## 5) LangChain v1 agent API (built on LangGraph)

If you’re building an “agent loop” via prebuilts, v1 expects LangChain’s API:

### 5.1) `create_react_agent` → `create_agent`

- Replace:
  - `from langgraph.prebuilt import create_react_agent`
- With:
  - `from langchain.agents import create_agent`

### 5.2) `prompt` → `system_prompt` (string)

- `system_prompt="..."` (string), not `SystemMessage`.

### 5.3) Hooks → middleware

- `pre_model_hook`/`post_model_hook` patterns move to middleware (`before_model`/`after_model`).

### 5.4) Tools: pass a list, not a ToolNode

- `create_agent(..., tools=[...])`
- Do not wrap tools in `ToolNode(...)` for `create_agent`.

### 5.5) State schemas: TypedDict-only

- `create_agent(..., state_schema=SomeTypedDict)`
- No pydantic/dataclass state schemas.

### 5.6) Streaming node name

- When streaming agent events, the node name is `"model"` (not `"agent"`).

## 6) Key “don’t break imports” reminders

- Graph API: `langgraph.graph` (START/END/StateGraph)
- Functional API: `langgraph.func` (entrypoint)
- Checkpointing: `langgraph.checkpoint.*` (InMemorySaver, sqlite/postgres modules)
- Store/memory: `langgraph.store.*`
- Agent prebuilt migration target: `langchain.agents` (create_agent, AgentState) and `langchain.agents.interrupt` (interrupt types)
