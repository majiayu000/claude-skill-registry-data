---
name: langgraph-persistence
description: Persistence and human-in-the-loop patterns for LangGraph. Use when implementing checkpointing, saving/restoring graph state, adding human approval workflows, managing conversation memory across sessions, enabling time-travel debugging, or building fault-tolerant agents that resume from failures.
---

# LangGraph Persistence

Persistence enables memory, human-in-the-loop, time-travel, and fault-tolerance.

## Checkpointers

Save graph state at every super-step. Available implementations:

| Checkpointer | Package | Use Case |
|--------------|---------|----------|
| `InMemorySaver` | langgraph-checkpoint | Development/testing |
| `SqliteSaver` | langgraph-checkpoint-sqlite | Local workflows |
| `PostgresSaver` | langgraph-checkpoint-postgres | Production |

### Basic Setup

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph

checkpointer = InMemorySaver()
graph = StateGraph(State)
# ... add nodes/edges ...
app = graph.compile(checkpointer=checkpointer)
```

### Threads

Unique identifier for each conversation/execution. Required for persistence.

```python
config = {"configurable": {"thread_id": "user-123-session-1"}}

# First invocation
result = app.invoke({"messages": [msg]}, config)

# Continue same thread (retains history)
result = app.invoke({"messages": [new_msg]}, config)
```

### PostgreSQL (Production)

```python
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

async with AsyncPostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:
    await checkpointer.setup()  # Create tables
    app = graph.compile(checkpointer=checkpointer)
```

## Human-in-the-Loop

### Static Interrupts

Pause at predefined points:

```python
# Pause BEFORE node executes
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["sensitive_action"]
)

# Pause AFTER node executes
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_after=["review_step"]
)
```

Execution and resume:

```python
config = {"configurable": {"thread_id": "1"}}

# Run until interrupt
for event in app.stream(inputs, config):
    print(event)
# Graph pauses at interrupt_before node

# ... human reviews state ...

# Resume from checkpoint (pass None as input)
for event in app.stream(None, config):
    print(event)
```

### Dynamic Interrupts

Pause based on runtime conditions using `interrupt()`:

```python
from langgraph.types import interrupt, Command

def sensitive_node(state: State) -> dict:
    if state["requires_approval"]:
        # Pause and request human input
        human_response = interrupt({
            "question": "Approve this action?",
            "proposed_action": state["action"]
        })
        if human_response == "reject":
            return {"status": "cancelled"}
    return {"status": "approved"}
```

Resume with `Command`:

```python
# Resume with human response
app.invoke(Command(resume="approve"), config)
```

### Editing State

Modify state before resuming:

```python
# Get current state
state = app.get_state(config)

# Update state
app.update_state(
    config,
    {"approved": True, "reviewer": "admin"},
    as_node="approval_node"  # Credit update to this node
)

# Resume
app.invoke(None, config)
```

## Common Patterns

### Approval Pattern

```python
from langgraph.types import interrupt

def approval_node(state: State) -> dict:
    response = interrupt({
        "type": "approval_request",
        "details": state["pending_action"]
    })
    if response["approved"]:
        return {"status": "approved"}
    return {"status": "rejected", "reason": response.get("reason")}
```

### Tool Call Review

```python
def review_tools(state: State) -> dict:
    last_msg = state["messages"][-1]
    if last_msg.tool_calls:
        decision = interrupt({
            "tool_calls": last_msg.tool_calls,
            "question": "Execute these tool calls?"
        })
        if not decision["proceed"]:
            # Modify or reject tool calls
            return {"messages": [modified_response]}
    return {}
```

### Multi-Turn Input Collection

```python
def collect_info(state: State) -> Command:
    missing = get_missing_fields(state)
    if missing:
        user_input = interrupt({
            "missing_fields": missing,
            "prompt": f"Please provide: {missing}"
        })
        return Command(update={"user_data": user_input})
    return Command(goto="process")
```

## Long-Term Memory (Store)

For cross-thread persistent storage:

```python
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()
app = graph.compile(
    checkpointer=checkpointer,
    store=store
)

# Access in node via runtime
def node_with_memory(state: State, *, store) -> dict:
    # Store/retrieve user preferences across threads
    user_prefs = store.get(("users", state["user_id"]))
    return {"preferences": user_prefs}
```

## State Inspection

```python
# Get current state snapshot
snapshot = app.get_state(config)
print(snapshot.values)  # Current state
print(snapshot.next)    # Next nodes to execute

# Get state history
for state in app.get_state_history(config):
    print(state.config, state.values)

# Time travel: resume from specific checkpoint
old_config = {"configurable": {
    "thread_id": "1",
    "checkpoint_id": "abc123"
}}
app.invoke(None, old_config)
```

## Key Points

- Always use `thread_id` in config for persistence
- `interrupt_before`/`interrupt_after` for static pauses
- `interrupt()` function for dynamic, conditional pauses
- Resume with `None` input or `Command(resume=...)`
- `update_state()` to edit state before resuming
- PostgresSaver for production deployments
