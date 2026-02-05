---
name: langgraph-fundamentals
description: Core concepts for building LangGraph applications. Use when creating StateGraph workflows, defining nodes and edges, managing state with TypedDict/Pydantic, or understanding basic graph structure. Covers state schemas, reducers, node functions, edge types (normal, conditional), and graph compilation.
---

# LangGraph Fundamentals

LangGraph is a low-level orchestration framework for building stateful, multi-actor LLM applications with cyclic graphs.

## Core Concepts

### StateGraph

The central abstraction. Initialize with a state schema, add nodes and edges, then compile.

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator

class State(TypedDict):
    messages: Annotated[list, operator.add]  # Reducer: append
    count: int  # Override: replace

graph = StateGraph(State)
```

### State Schema

Define with `TypedDict` or Pydantic `BaseModel`. Two update modes:

| Mode | Syntax | Behavior |
|------|--------|----------|
| Override | `field: Type` | Replace value |
| Reduce | `field: Annotated[Type, reducer]` | Apply reducer function |

Common reducers:
- `operator.add` - Append to list
- `add_messages` - Append messages with deduplication

```python
from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    messages: Annotated[list, add_messages]
```

### Nodes

Functions that receive state and return partial state updates.

```python
def my_node(state: State) -> dict:
    return {"count": state["count"] + 1}

graph.add_node("my_node", my_node)
# Or auto-name from function:
graph.add_node(my_node)  # name = "my_node"
```

Async nodes:
```python
async def async_node(state: State) -> dict:
    result = await some_async_call()
    return {"data": result}
```

### Edges

Connect nodes to define execution flow.

**Normal edges** - Fixed transitions:
```python
graph.add_edge(START, "node_a")
graph.add_edge("node_a", "node_b")
graph.add_edge("node_b", END)
```

**Conditional edges** - Dynamic routing:
```python
def route(state: State) -> str:
    if state["count"] > 5:
        return "finish"
    return "continue"

graph.add_conditional_edges(
    "node_a",
    route,
    {"finish": END, "continue": "node_b"}
)
```

**Fan-out/Fan-in** - Parallel execution:
```python
# Fan-out: single node to multiple
graph.add_edge("start", "task_a")
graph.add_edge("start", "task_b")

# Fan-in: multiple nodes to single (waits for all)
graph.add_edge(["task_a", "task_b"], "merge")
```

### Compilation and Execution

```python
# Compile
app = graph.compile()

# Invoke (sync)
result = app.invoke({"messages": [], "count": 0})

# Stream (sync)
for event in app.stream({"messages": []}, stream_mode="updates"):
    print(event)

# Async
result = await app.ainvoke({"messages": []})
async for event in app.astream({"messages": []}):
    print(event)
```

## Complete Example: ReAct Agent

```python
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

class State(TypedDict):
    messages: Annotated[list, add_messages]

@tool
def search(query: str) -> str:
    """Search the web."""
    return f"Results for: {query}"

tools = [search]
model = init_chat_model("gpt-4o").bind_tools(tools)

def agent(state: State) -> dict:
    response = model.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: State) -> Literal["tools", "__end__"]:
    last = state["messages"][-1]
    if last.tool_calls:
        return "tools"
    return "__end__"

graph = StateGraph(State)
graph.add_node("agent", agent)
graph.add_node("tools", ToolNode(tools))
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")

app = graph.compile()
```

## Key Points

- Nodes return partial state (only keys to update)
- Use `Annotated` with reducers for accumulating values
- `START` and `END` are special constants for entry/exit
- Always compile before invoke/stream
- Graph must have path from START to END
