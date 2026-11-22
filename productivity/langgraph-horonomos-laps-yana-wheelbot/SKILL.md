---
name: langgraph
description: "Use when building stateful multi-step agents, agent graphs, or workflows with LLMs. Triggers on: 'langgraph', 'state graph', 'stateful agent', 'agent workflow', 'agent loop', 'multi-step agent', 'persistent agent', 'human-in-the-loop agent', 'agent with memory', 'graph-based agent'."
---

# LangGraph Skill

Build stateful, long-running agents using graph-based orchestration.
Source: [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) (137K⭐, MIT)

## Core concepts

```
Node  = một function thực hiện một bước (LLM call, tool call, decision)
Edge  = transition giữa nodes (điều kiện hoặc unconditional)
State = shared dict truyền qua toàn bộ graph, persist across steps
```

## Install

```bash
pip install -U langgraph
# JS/TS
npm install @langchain/langgraph
```

## Workflow

### Step 1 — Xác định state schema

```python
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

class State(TypedDict):
    messages: Annotated[list, add_messages]   # tự động append, không overwrite
    step_count: int
```

### Step 2 — Định nghĩa nodes

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-6")

def call_llm(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response], "step_count": state["step_count"] + 1}

def check_done(state: State):
    last = state["messages"][-1]
    if last.tool_calls:
        return "tools"
    return END
```

### Step 3 — Build graph

```python
from langgraph.prebuilt import ToolNode

tools = [search_tool, calculator_tool]
tool_node = ToolNode(tools)
llm_with_tools = llm.bind_tools(tools)

graph = StateGraph(State)
graph.add_node("agent", call_llm)
graph.add_node("tools", tool_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", check_done)
graph.add_edge("tools", "agent")

app = graph.compile()
```

### Step 4 — Run với persistence

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app = graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "session-42"}}
result = app.invoke({"messages": [("user", "Tìm dân số Việt Nam")]}, config)
print(result["messages"][-1].content)
```

### Step 5 — Human-in-the-loop (interrupt)

```python
# Pause trước khi tool call để human review
app = graph.compile(
    checkpointer=memory,
    interrupt_before=["tools"]   # dừng tại node "tools"
)

# Resume sau khi human approve
app.invoke(None, config)         # tiếp tục từ checkpoint
```

## Patterns

### ReAct agent (observe → think → act)

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(llm, tools, checkpointer=memory)
result = agent.invoke({"messages": [("user", "task")]}, config)
```

### Subgraph (nested agent)

```python
subgraph = StateGraph(SubState)
# ... build subgraph ...
main_graph.add_node("subagent", subgraph.compile())
```

### Streaming output

```python
for chunk in app.stream({"messages": [("user", "task")]}, config):
    for node, values in chunk.items():
        print(f"[{node}]", values)
```

## Persistence backends

```python
# PostgreSQL (production)
from langgraph.checkpoint.postgres import PostgresSaver
checkpointer = PostgresSaver.from_conn_string("postgresql://...")

# Redis
from langgraph.checkpoint.redis import RedisSaver
```

## Lỗi thường gặp

| Lỗi | Fix |
|-----|-----|
| `InvalidUpdateError` | State update phải return dict, không return giá trị trực tiếp |
| `GraphRecursionError` | Tăng `recursion_limit` trong config: `{"recursion_limit": 25}` |
| Loop không dừng | Thêm conditional edge check `step_count` hoặc `max_iterations` |
