---
name: building-langgraph-agents
version: "1.0.0"
description: >
  Builds stateful AI agents using LangGraph — the graph-based state
  machine framework for agents with complex conditional flows, retry
  loops, error recovery, and built-in HITL checkpoints. Covers when
  to choose LangGraph over LangChain or CrewAI, core concepts (StateGraph,
  TypedDict state, nodes, edges, conditional edges, reducers, checkpointers),
  and implementation patterns for production agent workflows. Activates
  when building agents with complex branching logic, designing agents
  that need to loop until a condition is met, implementing state machines
  for agent workflows, adding error recovery to agent loops, building
  agents that need to pause for human approval at specific graph nodes,
  or migrating from sequential LangChain agents to stateful LangGraph
  agents. Also triggers on: LangGraph, StateGraph, stateful agent,
  conditional agent, agent loop, graph-based agent, agent branching,
  LangGraph HITL, agent checkpointer.
---

# LangGraph Agent Construction

LangGraph is a state machine framework for agents. It's the right choice
when your agent needs explicit control over what happens next at each step.

**Choose LangGraph over LangChain (sequential) or CrewAI (role-based) when:**
- The agent needs to loop until a condition is met (not just chain steps)
- Different tool results should route to different next actions
- Error recovery requires specific retry or fallback paths
- Human-in-the-loop checkpoints need to be embedded in the flow
- You need to inspect or modify agent state mid-execution

---

## Core Concepts

### StateGraph

The central object. Nodes process state; edges define what runs next.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# 1. Define your state schema
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]  # reducer: new messages append
    task: str
    tools_called: Annotated[list, operator.add]
    outcome: str | None
    error: str | None
    retry_count: int

# 2. Create the graph
graph = StateGraph(AgentState)
```

### Nodes

Functions that take state and return partial state updates.

```python
async def call_model(state: AgentState) -> dict:
    response = await llm.ainvoke(state["messages"])
    return {"messages": [response]}

async def execute_tool(state: AgentState) -> dict:
    # Extract tool call from last message
    last_msg = state["messages"][-1]
    tool_name = last_msg.tool_calls[0]["name"]
    tool_args = last_msg.tool_calls[0]["args"]
    
    try:
        result = await tools_map[tool_name].ainvoke(tool_args)
        return {
            "messages": [ToolMessage(content=str(result), tool_call_id=last_msg.tool_calls[0]["id"])],
            "tools_called": [tool_name]
        }
    except Exception as e:
        return {"error": str(e), "messages": [...]}

# Add to graph
graph.add_node("call_model", call_model)
graph.add_node("execute_tool", execute_tool)
```

### Conditional edges

The key LangGraph primitive. Route based on state.

```python
def should_continue(state: AgentState) -> str:
    last_msg = state["messages"][-1]
    
    # Agent requested a tool call
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "execute_tool"
    
    # Error needs retry (max 3 attempts)
    if state.get("error") and state.get("retry_count", 0) < 3:
        return "retry"
    
    # Max retries exceeded
    if state.get("retry_count", 0) >= 3:
        return "escalate"
    
    # Natural completion
    return END

graph.add_conditional_edges("call_model", should_continue, {
    "execute_tool": "execute_tool",
    "retry": "call_model",
    "escalate": "escalate_to_human",
    END: END
})
graph.add_edge("execute_tool", "call_model")
graph.set_entry_point("call_model")
```

---

## Built-in HITL with Checkpointers

LangGraph's checkpointer enables pausing mid-graph for human approval.

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Create a persistent checkpointer
checkpointer = SqliteSaver.from_conn_string("./agent_state.db")
# For Supabase: use PostgresSaver from langgraph-checkpoint-postgres

# Compile with interrupt
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["execute_consequential_action"]  # pause before this node
)

# Run until the interrupt
config = {"configurable": {"thread_id": "session-123"}}
result = await app.ainvoke(initial_state, config=config)

# At this point: execution is paused, state saved to checkpointer
# Present approval request to human (Slack, email, Base44 panel)

# On human approval: resume
final_result = await app.ainvoke(None, config=config)  # None = resume from checkpoint
```

This integrates directly with `designing-hitl-workflows` — the checkpoint
persistence gives you a durable pause that survives worker restarts.

---

## Error Recovery Pattern

LangGraph makes retry logic explicit in the graph structure.

```python
def route_after_error(state: AgentState) -> str:
    error = state.get("error", "")
    retry_count = state.get("retry_count", 0)
    
    if retry_count >= 3:
        return "escalate"
    
    if "rate_limit" in error.lower():
        return "wait_and_retry"
    
    if "tool_not_found" in error.lower():
        return "rephrase_and_retry"
    
    return "standard_retry"

graph.add_node("handle_error", handle_error)
graph.add_node("wait_and_retry", wait_and_retry)
graph.add_node("escalate", escalate_to_human)

graph.add_conditional_edges("handle_error", route_after_error, {
    "standard_retry": "call_model",
    "wait_and_retry": "wait_and_retry",
    "rephrase_and_retry": "call_model",
    "escalate": "escalate"
})
```

---

## LangGraph vs. LangChain vs. CrewAI — Quick Guide

| Pattern | Use when |
|---|---|
| LangGraph | Complex conditional flows, explicit retry/error paths, HITL at specific nodes, loop-until-done patterns |
| LangChain (sequential) | Linear chains of steps, one tool at a time, simple question-answer agents |
| CrewAI | Multiple specialized roles collaborating, each agent handles its domain |
| Raw Claude API | Maximum control, no framework overhead, simple tool-use patterns |

You can mix: use CrewAI for role-based coordination, implement each
agent's internal logic as a LangGraph state machine.

---

## Production Checklist

- [ ] State schema defined with TypedDict and explicit reducers
- [ ] All conditional edges tested with unit tests for each branch
- [ ] Error retry logic has a max retry count and escalation path
- [ ] Checkpointer configured for production persistence (Postgres, not SQLite)
- [ ] HITL interrupt nodes defined for consequential actions
- [ ] Context management integrated (see `managing-agent-context`)
- [ ] Telemetry emitted from critical nodes (see `instrumenting-agent-telemetry`)

---

## CLAIMS
- LangGraph's explicit state machine produces more debuggable agent behavior
  than implicit chaining because every routing decision is a named, testable
  function
- Checkpointer-based HITL survives worker restarts; callback-based HITL
  (common in other frameworks) does not

## COUNTEREXAMPLE
- LangGraph's additional abstraction layer adds debugging complexity for
  simple linear agents; for agents with fewer than 5 nodes and no
  branching, raw Claude API tool use is less overhead

## CONTRADICTIONS
- LangGraph's graph compilation step makes dynamic agent modification
  harder than with raw API calls; for agents that need to change their
  own structure at runtime, a different architecture is required
