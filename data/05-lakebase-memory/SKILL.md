---
name: 05-lakebase-memory
description: >
  Use when implementing stateful agents that need conversation memory. Covers
  short-term continuity via AsyncDatabricksSession (prescribed for OpenAI Agents
  SDK), long-term preferences via DatabricksStore, graceful degradation, and
  thread_id resolution. Track A Step 5. Consumes authenticated client from Step 4.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Conversation memory backed by a Lakebase instance (provisioned via the Databricks SDK/CLI, not a DAB resource kind in this workshop) + AsyncDatabricksSession. Same on both clients; on Genie Code run any provisioning CLI through runDatabricksCli (pre-authenticated). See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "3.2.0"
  domain: "genai-agents"
  pipeline_position: "A5"
  consumes: "authenticated_client"
  produces: "lakebase_tables, checkpointer, thread_id, predict_fn"
  grounded_in: "docs.databricks.com/aws/en/generative-ai/agent-framework/agent-memory, github.com/databricks/app-templates/tree/main/agent-openai-advanced, github.com/databricks/app-templates/tree/main/agent-openai-agents-sdk-short-term-memory, github.com/databricks/app-templates/tree/main/agent-langgraph-short-term-memory, github.com/databricks/app-templates/tree/main/agent-langgraph-long-term-memory"
fields_read:
  - agent.memory
  - agent.benchmark_seeds.seed_examples
  - governance.verification.smoke_test_question
---

# Track A Step 5: Lakebase Memory for Stateful Agents

## When to Use

Use this skill when implementing stateful agents that need:
- **Short-term memory**: Conversation continuity within a session (thread_id)
- **Long-term memory**: User preferences and insights across sessions (user_id)
- **Graceful degradation**: Agent works without memory tables
- **Thread ID resolution**: Priority-based thread_id extraction from request context

## Lakebase Provisioned Patterns

### OAuth Token Refresh (Production)
Tokens expire after 1 hour. Production apps MUST implement token refresh:

```python
from databricks.sdk import WorkspaceClient
import uuid

w = WorkspaceClient()
cred = w.database.generate_database_credential(
    request_id=str(uuid.uuid4()),
    instance_names=["my-lakebase-instance"]
)
token = cred.token  # Use as password, expires in 1 hour
```

For long-running apps, implement a background refresh loop every 50 minutes.

### Databricks Apps Integration
Apps use environment variables for Lakebase configuration:
- `LAKEBASE_INSTANCE_NAME` / `LAKEBASE_DATABASE_NAME` — set automatically by Databricks Apps
- Use `databricks apps add-resource` CLI to bind Lakebase to an app

### MLflow Model Resources
Declare Lakebase as a model resource for automatic credential provisioning:
```python
from mlflow.models.resources import DatabricksLakebase
resources = [DatabricksLakebase(database_instance_name="my-lakebase-instance")]
```

### SDK Version Requirements
- `databricks-sdk >= 0.61.0` (0.81.0+ recommended for full API support)
- `psycopg >= 3.0` (supports `hostaddr` for DNS workaround)
- `SQLAlchemy 2.x` with `postgresql+psycopg` driver

### Capacity Sizing
Lakebase Provisioned uses compute unit sizing: `CU_1`, `CU_2`, `CU_4`, `CU_8`.

### Autoscaling vs provisioned Lakebase
Autoscaling Postgres for Lakebase is not yet declarable in `databricks.yml`. After `bundle run` (or equivalent deploy), add or adjust autoscaling capacity via the Databricks API or UI if your workload needs it; provisioned CU sizing remains the primary bundle-declared path today.

## Two-Layer Memory Architecture

Aligned with the Databricks [AI agent memory](https://docs.databricks.com/aws/en/generative-ai/agent-framework/agent-memory) guidance: memory splits cleanly into short-term (a single conversation) and long-term (knowledge persisting across conversations).

| Layer | Component | Scope | Lifecycle | What to store |
|---|---|---|---|---|
| **Short-term** | CheckpointSaver / `AsyncDatabricksSession` | One thread (one conversation) | Session-scoped; expires per TTL / cleanup | Message history, intermediate tool calls, in-flight plan state |
| **Long-term** | `LongTermMemory` / `DatabricksStore` | One user (across conversations) | Persistent; explicit deletion or policy-driven | User preferences, extracted facts, approved entitlements, recurring context |

**Two independent decisions:**

1. **Do I need short-term memory?** Needed when the UI allows multi-turn chat and the backend is stateless (e.g. `/invocations` on an Agent App is re-entered every request). Without it, the model has no conversational continuity.
2. **Do I need long-term memory?** Needed when the agent should remember something about the user next session (preferred workspace, frequent tickets, saved filters). Without it, every new session starts from zero.

Both layers are implemented on Lakebase and scoped via OBO so each user sees only their own data. For connection-level setup (Lakebase provisioning, SP permissions, schema ownership), this Track A skill delegates to [`apps_lakebase/skills/05-appkit-lakebase-wiring`](../../../../apps_lakebase/skills/05-appkit-lakebase-wiring/SKILL.md); this skill covers the **agent-side** integration of the two memory layers.

## Canonical pattern (Option B + agent-openai-advanced)

The canonical Track A pattern combines the [`agent-openai-advanced`](https://github.com/databricks/app-templates/tree/main/agent-openai-advanced)
template's two-layer memory with Option B handlers from
[A2: Agent Framework](../02-agent-framework/SKILL.md). Memory is loaded
**inside** the request handler so it is always user-scoped via OBO:

```python
# agent.py — canonical layout
import os
from agents import Agent, Runner
from agents_sdk_databricks.memory import AsyncDatabricksSession
from agents.memory import LongTermMemory
from mlflow.genai import agent_server
from databricks_app.utils import get_user_workspace_client

LAKEBASE_INSTANCE = os.environ["LAKEBASE_INSTANCE_NAME"]
LAKEBASE_DB = os.environ["LAKEBASE_DATABASE_NAME"]

def make_short_term(user_token: str) -> AsyncDatabricksSession:
    return AsyncDatabricksSession(
        instance_name=LAKEBASE_INSTANCE,
        database_name=LAKEBASE_DB,
        oauth_token=user_token,            # OBO-scoped
    )

def make_long_term(user_token: str) -> LongTermMemory:
    return LongTermMemory(
        instance_name=LAKEBASE_INSTANCE,
        embedding_endpoint="databricks-gte-large-en",
        embedding_dims=1024,
        oauth_token=user_token,
    )

def resolve_thread_id(custom_inputs: dict, conversation_id: str | None) -> str:
    return (custom_inputs or {}).get("thread_id") or conversation_id or str(uuid.uuid4())

@agent_server.invoke
async def handle_invoke(request: dict, http_request) -> dict:
    ws = get_user_workspace_client(http_request)
    user_id = ws.current_user.me().user_name

    short = make_short_term(ws.config.token)
    long_term = make_long_term(ws.config.token)
    thread_id = resolve_thread_id(request.get("custom_inputs"), request.get("conversation_id"))

    # Inject relevant long-term memories into the agent's context
    relevant = long_term.search_memories(user_id=user_id, query=request["input"], limit=5)
    instructions = build_instructions_with_memories(relevant)
    agent = Agent(name="loyalty-assistant", instructions=instructions, ...)

    result = await Runner.run(agent, input=request["input"], session=short, session_id=thread_id)

    # Persist new long-term facts extracted from this turn (if any)
    persist_extracted_facts(long_term, user_id, result)

    return {
        "output": result.final_output,
        "custom_outputs": {"thread_id": thread_id},
    }
```

**Key properties of the canonical pattern:**

1. **Lakebase clients are constructed inside the handler** with the user's
   OBO token. Module-level construction would use the SP token and break
   per-user isolation.
2. **`thread_id` is resolved per request** (custom_inputs → conversation_id
   → new UUID) and echoed in `custom_outputs` so the frontend can stitch
   subsequent turns onto the same thread.
3. **Long-term memory is _retrieved_ before the LLM call** (injected into
   `instructions`) and **_written_ after the LLM call** (extracted facts).
4. **Both layers share the same Lakebase instance** but different tables
   (`sessions` / `session_items` for short, `store` / `store_vectors` for
   long).

The same shape applies to streaming via `@agent_server.stream`. See the
template for the full streaming variant.

## Core Principles

### 1. Unity Catalog-Backed Storage
- All memory stored in Unity Catalog Delta tables
- Governed, auditable, queryable
- Automatic schema management via `.setup()`
- TTL-based cleanup for GDPR compliance

### 2. Graceful Degradation
- Memory is optional enhancement, not requirement
- Agent works without memory tables
- Silent fallback if tables don't exist
- No failures due to missing memory

## Quick Setup

### Short-Term Memory (OpenAI Agents SDK — Default)

```python
from agents_sdk_databricks.memory import AsyncDatabricksSession

session = AsyncDatabricksSession(
    instance_name="my_lakebase",
    database_name="my_database",
)

# Setup tables (run once)
await session.setup()

# Use with OpenAI Agents SDK Runner
from agents import Runner
result = await Runner.run(agent, input=messages, session=session)
```

### Thread ID Resolution

```python
# Priority: custom_inputs > conversation_id > new UUID
thread_id = resolve_thread_id(
    custom_inputs=request.custom_inputs,
    conversation_id=context.conversation_id
)
```

**Alternative (LangGraph):** If using LangGraph instead, use `memory.get_checkpointer()` with `graph.invoke(messages, config={"configurable": {"thread_id": thread_id}})`. See the [LangGraph short-term memory template](https://github.com/databricks/app-templates/tree/main/agent-langgraph-short-term-memory) for details.

### Long-Term Memory

```python
from agents.memory import LongTermMemory

# Initialize
memory = LongTermMemory(
    instance_name="my_lakebase",
    embedding_endpoint="databricks-gte-large-en",
    embedding_dims=1024
)

# Setup tables (run once)
memory.setup()

# Save user preference
memory.save_memory(
    user_id="user@example.com",
    memory_key="preferred_workspace",
    memory_data={"workspace_id": "12345"}
)

# Search memories
results = memory.search_memories(
    user_id="user@example.com",
    query="What workspace does the user prefer?",
    limit=5
)
```

## OpenAI Agents SDK: AsyncDatabricksSession

```python
from databricks_openai import AsyncDatabricksSession

# Sessions auto-manage conversation history:
# - Before each run: retrieves prior history, prepends to input
# - After each run: stores new items (messages, tool calls, responses)
session = AsyncDatabricksSession(
    instance_name="my-lakebase-instance",
    database_name="my-database",
)

# Use with OpenAI Agents SDK Runner
result = await Runner.run(
    agent=my_agent,
    input=user_message,
    session=session,
    session_id=session_id,  # or generate new
)
```

Reference: [agent-openai-agents-sdk-short-term-memory](https://github.com/databricks/app-templates/tree/main/agent-openai-agents-sdk-short-term-memory)

## Checkpoint Tables

Memory persistence on Lakebase (Postgres) uses dedicated tables. The exact
table names depend on your framework:

| Framework | Tables Created |
|---|---|
| **OpenAI Agents SDK** (`AsyncDatabricksSession`) | `sessions`, `session_items` (managed by `databricks_openai`) |
| **LangGraph** (`CheckpointSaver`) | `checkpoints`, `checkpoint_writes`, `checkpoint_blobs`, `checkpoint_migrations` |
| **Long-term** (`DatabricksStore`) | `store`, `store_vectors`, `store_migrations`, `vector_migrations` |

Align SP grants (see below) and monitoring with whatever tables your framework
creates. To inspect checkpoint data, connect to the Lakebase instance with
`psql` or any Postgres client and query these tables directly.

## Lakebase SP Permissions for Deployed Apps

For a Databricks App running as a service principal, grant the SP rights on the public schema (or your chosen schema) after tables exist:

```sql
DO $$
DECLARE
   app_sp text := 'app-sp-id';  -- Replace with App's Service Principal ID
BEGIN
   -- Checkpoint schema (short-term memory)
   EXECUTE format('GRANT USAGE, CREATE ON SCHEMA public TO %I;', app_sp);
   EXECUTE format('GRANT SELECT, INSERT, UPDATE ON TABLE public.checkpoint_migrations TO %I;', app_sp);
   EXECUTE format('GRANT SELECT, INSERT, UPDATE ON TABLE public.checkpoint_writes TO %I;', app_sp);
   EXECUTE format('GRANT SELECT, INSERT, UPDATE ON TABLE public.checkpoints TO %I;', app_sp);
   EXECUTE format('GRANT SELECT, INSERT, UPDATE ON TABLE public.checkpoint_blobs TO %I;', app_sp);

   -- Store schema (long-term memory)
   EXECUTE format('GRANT SELECT, INSERT, UPDATE ON TABLE public.store_migrations TO %I;', app_sp);
   EXECUTE format('GRANT SELECT, INSERT, UPDATE ON TABLE public.store TO %I;', app_sp);
   EXECUTE format('GRANT SELECT, INSERT, UPDATE ON TABLE public.store_vectors TO %I;', app_sp);
   EXECUTE format('GRANT SELECT, INSERT, UPDATE ON TABLE public.vector_migrations TO %I;', app_sp);
END $$;
```

Adjust schema name if your app uses a non-`public` schema.

## Common Mistakes to Avoid

### DON'T: Assume Tables Exist

```python
# BAD: Will fail if tables not created
class Agent:
    def __init__(self):
        self.memory = ShortTermMemory()
        with self.memory.get_checkpointer() as checkpointer:
            self.graph = workflow.compile(checkpointer=checkpointer)
```

### DO: Graceful Degradation

```python
# GOOD: Falls back gracefully
class Agent:
    def __init__(self):
        try:
            self.memory = ShortTermMemory()
            with self.memory.get_checkpointer() as checkpointer:
                self.graph = workflow.compile(checkpointer=checkpointer)
        except Exception as e:
            print(f"Memory unavailable, using stateless mode: {e}")
            self.graph = workflow.compile()  # No checkpointer
```

### DON'T: Forget to Return thread_id

```python
# BAD: Client can't track conversation
return {
    "choices": [{"message": {"content": response}}]
}
```

### DO: Return thread_id for Client Tracking

```python
# GOOD: Client can continue conversation
return {
    "choices": [{"message": {"content": response}}],
    "custom_outputs": {
        "thread_id": thread_id,  # Return for next turn
    }
}
```

### DON'T: Hardcode User IDs

```python
# BAD: Hardcoded user
memories = store.search_memories("hardcoded@example.com", query)
```

### DO: Extract from Context

```python
# GOOD: Dynamic user from request context
user_id = context.get("user_id") or custom_inputs.get("user_id") or "unknown"
memories = store.search_memories(user_id, query)
```

## Validation Checklist

Before deploying agent with memory:
- [ ] Lakebase instance name configured in settings
- [ ] Setup script run once (creates tables)
- [ ] Short-term memory uses `CheckpointSaver` with context manager
- [ ] Long-term memory uses `DatabricksStore` with embeddings
- [ ] Embedding endpoint configured (e.g., `databricks-gte-large-en`)
- [ ] Embedding dimensions match model (1024 for GTE-large)
- [ ] Thread ID resolution: custom_inputs → conversation_id → new UUID
- [ ] User ID extracted from context/custom_inputs
- [ ] Graceful degradation if tables don't exist
- [ ] thread_id returned in custom_outputs for client tracking
- [ ] Memory tools created with `create_memory_tools()` if autonomous use
- [ ] MLflow tracing enabled for memory operations
- [ ] App SP grants applied for checkpoint and store tables when using deployed apps

## Producing the predict_fn

At the end of Track A, your agent is complete — it has tools, auth, and memory.
The SDLC pipeline ([S4: Evaluation Runs](../../../sdlc/04-evaluation-runs/SKILL.md))
needs a standard `predict_fn(inputs: dict) -> str` interface to run
comprehensive evaluation. This is Track A's interface contract to SDLC,
matching the equivalent in Tracks B and C.

```python
from agents import Runner

def make_predict_fn(agent) -> callable:
    """Create the predict_fn interface for SDLC evaluation."""
    def predict_fn(inputs: dict) -> str:
        question = inputs.get("question", "")
        result = Runner.run_sync(agent, question)
        return result.final_output
    return predict_fn
```

Add this to your `agent.py` (or a separate `predict.py` module) and export it.
S4 calls this function during evaluation to generate responses that judges
then score against your benchmark dataset.

## Next Step

After passing the validation checklist and producing `predict_fn`, **load and
execute** `tracks/A-custom-agent-apps/06-evaluation/SKILL.md` (A6: Evaluation)
to smoke test the agent before deployment.

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [A4: Authentication](../04-authentication/SKILL.md) | Previous step — produces `authenticated_client` |
| [A6: Evaluation](../06-evaluation/SKILL.md) | Next step — smoke tests the agent |
| [S1: Prompt Registry](../../../sdlc/01-prompt-registry/SKILL.md) | SDLC entry point after Track A |
| [S4: Evaluation Runs](../../../sdlc/04-evaluation-runs/SKILL.md) | Consumes `predict_fn` for comprehensive evaluation |

## References

### App templates (grounding)
- **[agent-openai-advanced (canonical: short + long term + custom tools)](https://github.com/databricks/app-templates/tree/main/agent-openai-advanced)**
- [OpenAI Agents SDK short-term memory (Lakebase)](https://github.com/databricks/app-templates/tree/main/agent-openai-agents-sdk-short-term-memory)
- [LangGraph short-term memory](https://github.com/databricks/app-templates/tree/main/agent-langgraph-short-term-memory)
- [LangGraph long-term memory](https://github.com/databricks/app-templates/tree/main/agent-langgraph-long-term-memory)

### Detailed Patterns
- [Short-Term Memory](references/short-term-memory.md) - Complete CheckpointSaver implementation
- [Long-Term Memory](references/long-term-memory.md) - Complete DatabricksStore implementation
- [Graceful Degradation](references/graceful-degradation.md) - Fallback patterns

### Setup Scripts
- [Setup Lakebase](scripts/setup_lakebase.py) - Table initialization script

### Official Documentation
- [Databricks Short-Term Memory Pattern](https://docs.databricks.com/aws/en/notebooks/source/generative-ai/short-term-memory-agent-lakebase.html)
- [Databricks Long-Term Memory Pattern](https://docs.databricks.com/aws/en/notebooks/source/generative-ai/long-term-memory-agent-lakebase.html)
- [Stateful Agents Guide](https://learn.microsoft.com/en-us/azure/databricks/generative-ai/agent-framework/stateful-agents)
- [Lakebase Documentation](https://docs.databricks.com/en/lakebase/)
