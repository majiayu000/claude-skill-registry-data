---
name: langgraph-multi-agent
description: Multi-agent architectures with LangGraph. Use when building systems with multiple collaborating agents, implementing supervisor or swarm patterns, creating hierarchical agent workflows, or designing agent handoff mechanisms. Covers langgraph-supervisor, langgraph-swarm, agent-as-tool patterns, and context engineering for multi-agent systems.
---

# LangGraph Multi-Agent Systems

Patterns for building multi-agent systems with LangGraph.

## Architecture Overview

| Pattern | Control Flow | Best For |
|---------|--------------|----------|
| **Supervisor** | Central orchestrator delegates to workers | Structured workflows, clear hierarchy |
| **Swarm** | Agents hand off directly to each other | Dynamic routing, lower latency |
| **Agent-as-Tool** | Main agent calls subagents as tools | Simple delegation, isolated subagents |

## Supervisor Pattern

Central supervisor routes tasks to specialized agents.

### Using langgraph-supervisor

```bash
pip install langgraph-supervisor
```

```python
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

# Create specialized agents
research_agent = create_react_agent(
    llm,
    tools=[search_tool, wiki_tool],
    name="researcher",
    prompt="You are a research specialist."
)

math_agent = create_react_agent(
    llm,
    tools=[calculator_tool],
    name="mathematician",
    prompt="You are a math expert."
)

# Create supervisor
workflow = create_supervisor(
    agents=[research_agent, math_agent],
    model=llm,
    prompt="Route tasks to the appropriate specialist."
)

app = workflow.compile()
result = app.invoke({"messages": [("user", "What is 25 * 17?")]})
```

### Manual Supervisor Implementation

```python
from langgraph.graph import StateGraph, START, END
from typing import Literal

class SupervisorState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str

def supervisor(state: SupervisorState) -> dict:
    # LLM decides which agent to call
    response = llm.invoke([
        SystemMessage("Route to 'researcher', 'coder', or 'FINISH'"),
        *state["messages"]
    ])
    return {"next_agent": response.content}

def route(state: SupervisorState) -> Literal["researcher", "coder", "__end__"]:
    if state["next_agent"] == "FINISH":
        return "__end__"
    return state["next_agent"]

graph = StateGraph(SupervisorState)
graph.add_node("supervisor", supervisor)
graph.add_node("researcher", research_agent)
graph.add_node("coder", coder_agent)

graph.add_edge(START, "supervisor")
graph.add_conditional_edges("supervisor", route)
graph.add_edge("researcher", "supervisor")
graph.add_edge("coder", "supervisor")
```

## Swarm Pattern

Agents hand off control directly to peers.

### Using langgraph-swarm

```bash
pip install langgraph-swarm
```

```python
from langgraph_swarm import create_swarm, create_handoff_tool
from langgraph.prebuilt import create_react_agent

# Create handoff tools
handoff_to_sales = create_handoff_tool(
    agent_name="sales_agent",
    description="Transfer to sales for pricing questions"
)
handoff_to_support = create_handoff_tool(
    agent_name="support_agent",
    description="Transfer to support for technical issues"
)

# Create agents with handoff tools
sales_agent = create_react_agent(
    llm,
    tools=[pricing_tool, handoff_to_support],
    name="sales_agent",
    prompt="You handle sales and pricing."
)

support_agent = create_react_agent(
    llm,
    tools=[docs_tool, handoff_to_sales],
    name="support_agent",
    prompt="You handle technical support."
)

# Create swarm
workflow = create_swarm(
    agents=[sales_agent, support_agent],
    default_active_agent="sales_agent"
)

app = workflow.compile(checkpointer=checkpointer)
```

### Custom Handoff Tool

```python
from langchain.tools import tool
from langgraph.types import Command
from langgraph.prebuilt import InjectedState

@tool
def transfer_to_specialist(
    reason: str,
    state: Annotated[dict, InjectedState]
) -> Command:
    """Transfer conversation to specialist agent."""
    return Command(
        update={
            "messages": state["messages"],
            "transfer_reason": reason
        },
        goto="specialist_agent"
    )
```

## Agent-as-Tool Pattern

Wrap subagents as tools for the main agent:

```python
from langchain.tools import tool

# Create subagent
researcher = create_react_agent(llm, tools=[search_tool])

@tool
def call_researcher(query: str) -> str:
    """Delegate research tasks to the research specialist."""
    result = researcher.invoke({
        "messages": [("user", query)]
    })
    return result["messages"][-1].content

# Main agent uses subagent as tool
main_agent = create_react_agent(
    llm,
    tools=[call_researcher, other_tools],
    prompt="You are a coordinator. Delegate research to the researcher."
)
```

### With State Propagation

```python
from langgraph.prebuilt import InjectedToolCallId
from langchain.messages import ToolMessage
from langgraph.types import Command

@tool
def call_subagent(
    query: str,
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """Call subagent and return result."""
    result = subagent.invoke({"messages": [("user", query)]})
    return Command(update={
        "messages": [ToolMessage(
            content=result["messages"][-1].content,
            tool_call_id=tool_call_id
        )]
    })
```

## Context Engineering

Control what information each agent sees.

### Message Filtering

```python
def filter_messages_for_agent(messages: list, agent_name: str) -> list:
    """Filter messages relevant to specific agent."""
    return [
        m for m in messages
        if not hasattr(m, 'name') or m.name in [agent_name, 'user']
    ]

def specialist_node(state: State) -> dict:
    filtered = filter_messages_for_agent(state["messages"], "specialist")
    result = specialist_agent.invoke({"messages": filtered})
    return {"messages": result["messages"]}
```

### Shared vs Private State

```python
class MultiAgentState(TypedDict):
    # Shared across all agents
    messages: Annotated[list, add_messages]
    
    # Agent-specific (private)
    researcher_scratchpad: str
    coder_scratchpad: str

def researcher_node(state: MultiAgentState) -> dict:
    # Only reads/writes own scratchpad
    return {
        "messages": [...],
        "researcher_scratchpad": "notes..."
    }
```

### Summary Handoff

Pass summaries instead of full history:

```python
def create_summary_handoff(from_agent: str, to_agent: str):
    @tool
    def handoff(context_summary: str) -> Command:
        """Hand off with summary instead of full history."""
        return Command(
            update={
                "messages": [HumanMessage(
                    content=f"Context from {from_agent}: {context_summary}"
                )],
                "active_agent": to_agent
            },
            goto=to_agent
        )
    return handoff
```

## Memory and Persistence

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

checkpointer = InMemorySaver()  # Short-term (conversation)
store = InMemoryStore()          # Long-term (cross-session)

app = workflow.compile(
    checkpointer=checkpointer,
    store=store
)

# Thread per conversation
config = {"configurable": {"thread_id": f"user_{user_id}"}}
result = app.invoke(inputs, config)
```

## Choosing Architecture

| Factor | Supervisor | Swarm |
|--------|------------|-------|
| Latency | Higher (routing overhead) | Lower (direct handoff) |
| Control | Centralized | Distributed |
| Complexity | Simpler to reason about | More flexible |
| Token usage | More (supervisor sees all) | Less (direct routing) |

**Use Supervisor when:**
- Clear hierarchy needed
- Consistent routing logic required
- Working with third-party agents

**Use Swarm when:**
- Latency is critical
- Agents are peers
- Dynamic, organic routing

## Key Points

- Supervisor: central control, higher latency, simpler logic
- Swarm: peer-to-peer, lower latency, explicit handoffs
- Agent-as-tool: simple delegation, isolated execution
- Filter context to avoid overwhelming agents
- Use checkpointer for multi-turn conversations
- Consider token usage when designing message flow
