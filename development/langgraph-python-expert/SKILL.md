---
name: langgraph-python-expert
description: Expert guidance for LangGraph Python library. Build stateful, multi-actor applications with LLMs using nodes, edges, and state management. Use when working with LangGraph, building agent workflows, state machines, or complex multi-step LLM applications. Requires langgraph, langchain-core packages.
---

# LangGraph Python Expert

Comprehensive expert for building sophisticated stateful applications with LangGraph, focusing on production-ready workflows, state management, and agent orchestration.

## 📚 Official Source Documentation

This skill includes access to the official LangGraph source code through the `source/langgraph/` directory (managed as git submodule with sparse-checkout), which contains:

- **Core Libraries**: `libs/langgraph/`, `libs/prebuilt/`, `libs/checkpoint*/`
- **Official Examples**: `examples/` - Up-to-date examples and tutorials
- **Complete Documentation**: `docs/docs/` - Latest documentation and API references

### Source Structure (66MB with sparse-checkout)

```
source/langgraph/
├── libs/
│   ├── langgraph/          # Core StateGraph, nodes, edges
│   ├── prebuilt/           # create_react_agent, ToolNode
│   ├── checkpoint/         # Base checkpoint classes
│   ├── checkpoint-sqlite/  # SQLite persistence
│   └── checkpoint-postgres/# PostgreSQL persistence
├── examples/               # Official examples and tutorials
├── docs/docs/              # Documentation (concepts, how-tos, reference)
├── README.md               # Project overview
├── CLAUDE.md               # Claude Code instructions
└── AGENTS.md               # Agent development guide
```

### Updating Source Code
```bash
cd source/langgraph
git pull origin main
```

For detailed structure, see [SOURCE_STRUCTURE.md](SOURCE_STRUCTURE.md).

## Quick Start

### Installation
```bash
pip install langgraph langchain-core langchain-openai
```

### Basic Concepts

**StateGraph**: The core component for building workflows with state persistence
**Nodes**: Functions that process the state and return updates
**Edges**: Define the flow between nodes (conditional or direct)
**State**: TypedDict that holds conversation/application state
**Persistence**: Checkpointing for memory and conversation history

## Core Components

### 1. State Definition
```python
from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: List[BaseMessage]
    current_user: Optional[str]
    step_count: int
    requires_action: bool
```

### 2. Node Functions
```python
from langchain_core.messages import HumanMessage, AIMessage

def llm_node(state: AgentState) -> AgentState:
    """Process messages with LLM and return updated state"""
    messages = state["messages"]
    response = llm.invoke(messages)
    return {
        "messages": messages + [response],
        "step_count": state["step_count"] + 1
    }

def router_node(state: AgentState) -> str:
    """Decide next node based on state"""
    last_message = state["messages"][-1]
    if "tool_call" in last_message.additional_kwargs:
        return "tool_executor"
    return "end"
```

### 3. Graph Construction
```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# Create graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tool_executor", tool_node)
workflow.add_node("router", router_node)

# Add edges
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    router_node,
    {
        "tool_executor": "tool_executor",
        "end": END
    }
)
workflow.add_edge("tool_executor", "agent")

# Memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
```

## Advanced Patterns

### 1. Multi-Agent Collaboration
```python
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import create_react_agent

class MultiAgentState(MessagesState):
    researcher_notes: str
    writer_content: str
    reviewer_feedback: List[str]

def researcher_node(state: MultiAgentState) -> MultiAgentState:
    """Research agent that gathers information"""
    researcher_agent = create_react_agent(llm, research_tools)
    result = researcher_agent.invoke({
        "messages": state["messages"][-2:]  # Last two messages
    })

    return {
        "researcher_notes": result["messages"][-1].content,
        "messages": state["messages"] + result["messages"]
    }

def writer_node(state: MultiAgentState) -> MultiAgentState:
    """Writer agent that creates content based on research"""
    writer_agent = create_react_agent(llm, writing_tools)
    prompt = f"Research notes: {state['researcher_notes']}"

    result = writer_agent.invoke({
        "messages": [HumanMessage(content=prompt)]
    })

    return {
        "writer_content": result["messages"][-1].content,
        "messages": state["messages"] + result["messages"]
    }
```

### 2. Dynamic Tool Selection
```python
from typing import Dict, Any
from langchain_core.tools import BaseTool

class DynamicToolNode:
    def __init__(self, tool_registry: Dict[str, BaseTool]):
        self.tool_registry = tool_registry

    def __call__(self, state: AgentState) -> AgentState:
        last_message = state["messages"][-1]

        if not last_message.tool_calls:
            return state

        # Dynamically select tools based on context
        selected_tools = self.select_tools_by_context(state)

        # Execute tool calls
        tool_messages = []
        for tool_call in last_message.tool_calls:
            if tool_call["name"] in selected_tools:
                tool = selected_tools[tool_call["name"]]
                result = tool.invoke(tool_call["args"])
                tool_messages.append(
                    ToolMessage(
                        tool_call_id=tool_call["id"],
                        content=str(result)
                    )
                )

        return {
            "messages": state["messages"] + tool_messages
        }

    def select_tools_by_context(self, state: AgentState) -> Dict[str, BaseTool]:
        """Intelligently select tools based on conversation context"""
        context = " ".join([msg.content for msg in state["messages"][-5:]])

        available_tools = {}
        if "code" in context.lower():
            available_tools.update({"code_executor": code_tool})
        if "search" in context.lower():
            available_tools.update({"web_search": search_tool})
        if "math" in context.lower():
            available_tools.update({"calculator": math_tool})

        return available_tools
```

### 3. State Persistence and Recovery
```python
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver

# Production-ready persistence
def create_production_app():
    # Use PostgreSQL for production
    connection_string = "postgresql://user:pass@localhost/langgraph"
    checkpointer = PostgresSaver.from_conn_string(connection_string)

    # Build workflow
    workflow = StateGraph(AgentState)
    # ... add nodes and edges

    # Compile with persistence
    app = workflow.compile(checkpointer=checkpointer)
    return app

# Thread-based conversation management
def manage_conversation(app, thread_id: str):
    """Manage persistent conversations across sessions"""
    config = {"configurable": {"thread_id": thread_id}}

    # Continue existing conversation
    result = app.invoke({
        "messages": [HumanMessage(content="Continue our discussion")]
    }, config)

    return result
```

### 4. Error Handling and Retry Logic
```python
from typing import Union
from langgraph.graph import StateGraph
import time

class RobustAgentState(TypedDict):
    messages: List[BaseMessage]
    retry_count: int
    max_retries: int
    error_history: List[str]

def error_handling_node(state: RobustAgentState) -> Union[RobustAgentState, str]:
    """Node with built-in error handling and retry logic"""
    try:
        # Attempt the primary operation
        result = perform_operation(state)

        # Reset retry count on success
        return {
            **result,
            "retry_count": 0,
            "error_history": []
        }

    except Exception as e:
        error_msg = str(e)
        new_retry_count = state["retry_count"] + 1

        if new_retry_count >= state["max_retries"]:
            return "error_handler"  # Route to error handling

        # Add delay for exponential backoff
        time.sleep(2 ** new_retry_count)

        return {
            "retry_count": new_retry_count,
            "error_history": state["error_history"] + [error_msg]
        }

def fallback_node(state: RobustAgentState) -> RobustAgentState:
    """Fallback strategy when primary operation fails"""
    last_error = state["error_history"][-1] if state["error_history"] else "Unknown error"

    fallback_message = AIMessage(
        content=f"I encountered an error: {last_error}. "
                f"Let me try a different approach."
    )

    return {
        "messages": state["messages"] + [fallback_message],
        "retry_count": 0
    }
```

## Integration Examples

### 1. RAG with LangGraph
```python
def create_rag_graph():
    class RAGState(TypedDict):
        question: str
        context: List[str]
        answer: str
        sources: List[str]

    def retrieve_node(state: RAGState) -> RAGState:
        # Retrieve relevant documents
        docs = retriever.invoke(state["question"])
        return {
            "context": [doc.page_content for doc in docs],
            "sources": [doc.metadata.get("source", "unknown") for doc in docs]
        }

    def generate_node(state: RAGState) -> RAGState:
        # Generate answer using retrieved context
        prompt = f"""
        Question: {state['question']}
        Context: {state['context']}

        Generate a comprehensive answer based on the context.
        """

        response = llm.invoke([HumanMessage(content=prompt)])
        return {
            "answer": response.content
        }

    # Build RAG workflow
    workflow = StateGraph(RAGState)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)

    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()
```

### 2. Sequential Task Processing
```python
def create_sequential_processor():
    class TaskState(TypedDict):
        tasks: List[Dict[str, Any]]
        current_task_index: int
        results: List[Any]
        status: str

    def task_executor(state: TaskState) -> TaskState:
        idx = state["current_task_index"]
        if idx >= len(state["tasks"]):
            return {"status": "completed"}

        current_task = state["tasks"][idx]
        result = execute_task(current_task)

        return {
            "current_task_index": idx + 1,
            "results": state["results"] + [result],
            "status": "processing" if idx + 1 < len(state["tasks"]) else "completed"
        }

    def task_router(state: TaskState) -> str:
        if state["status"] == "completed":
            return END
        return "continue_processing"

    workflow = StateGraph(TaskState)
    workflow.add_node("execute_task", task_executor)
    workflow.add_conditional_edges("execute_task", task_router)

    return workflow.compile()
```

## Best Practices

### 1. State Design
- Keep state minimal and focused
- Use TypedDict for type safety
- Avoid storing large objects in state
- Use references/IDs instead of full objects when possible

### 2. Node Design
- Make nodes pure functions when possible
- Handle errors gracefully
- Return only the state keys that need updating
- Use descriptive names for clarity

### 3. Graph Architecture
- Break complex workflows into smaller, reusable subgraphs
- Use conditional edges for intelligent routing
- Implement proper error handling paths
- Design for testability and debugging

### 4. Performance Optimization
- Use streaming for long-running operations
- Implement proper caching strategies
- Consider async/await for I/O operations
- Monitor and optimize checkpoint sizes

## Testing and Debugging

### 1. Unit Testing Nodes
```python
import pytest
from langgraph.graph import StateGraph

def test_llm_node():
    # Mock state
    test_state = {
        "messages": [HumanMessage(content="Test message")],
        "step_count": 0
    }

    # Mock LLM
    with patch('your_module.llm') as mock_llm:
        mock_llm.invoke.return_value = AIMessage(content="Test response")

        result = llm_node(test_state)

        assert result["step_count"] == 1
        assert len(result["messages"]) == 2
        mock_llm.invoke.assert_called_once()
```

### 2. Integration Testing
```python
def test_full_workflow():
    app = create_test_workflow()

    initial_state = {
        "messages": [HumanMessage(content="Hello")],
        "step_count": 0
    }

    result = app.invoke(initial_state)

    assert "messages" in result
    assert result["messages"][-1].type == "ai"
```

### 3. Debugging Tools
```python
# Enable debug mode
import langgraph
langgraph.debug = True

# Print state transitions
def debug_node(state: AgentState) -> AgentState:
    print(f"Node input: {state}")
    result = your_node_logic(state)
    print(f"Node output: {result}")
    return result

# Use with context manager
from langgraph.graph import StateGraph

def create_debug_workflow():
    workflow = StateGraph(AgentState)
    workflow.add_node("debug_step", debug_node)
    # ... rest of workflow

    return workflow.compile()
```

## Common Patterns and Solutions

### 1. Human-in-the-Loop
```python
def human_approval_node(state: AgentState) -> AgentState:
    """Wait for human approval before proceeding"""
    last_message = state["messages"][-1]

    if state.get("awaiting_approval"):
        # Check if approval was received
        user_input = input(f"Approve this action? {last_message.content} (y/n): ")
        if user_input.lower() == 'y':
            return {
                "awaiting_approval": False,
                "messages": state["messages"] + [
                    AIMessage(content="Action approved by human")
                ]
            }
        else:
            return {
                "awaiting_approval": False,
                "messages": state["messages"] + [
                    AIMessage(content="Action rejected by human")
                ]
            }
    else:
        # Request approval
        return {
            "awaiting_approval": True,
            "messages": state["messages"]
        }
```

### 2. Parallel Processing
```python
from langgraph.graph import StateGraph, START, END

def parallel_processor(state: Dict[str, Any]) -> Dict[str, Any]:
    """Process multiple items in parallel"""
    input_data = state["input_items"]

    # Define parallel tasks
    def task_1(data):
        return process_type_1(data)

    def task_2(data):
        return process_type_2(data)

    # Execute in parallel (using threading or async)
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_1 = executor.submit(task_1, input_data)
        future_2 = executor.submit(task_2, input_data)

        result_1 = future_1.result()
        result_2 = future_2.result()

    return {
        "result_1": result_1,
        "result_2": result_2
    }
```

## Production Deployment

### 1. Environment Setup
```python
import os
from langgraph.graph import StateGraph
from langgraph.checkpoint.postgres import PostgresSaver

def create_production_app():
    # Load configuration
    db_url = os.getenv("DATABASE_URL")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Initialize components
    checkpointer = PostgresSaver.from_conn_string(db_url)

    # Build workflow with production settings
    workflow = StateGraph(ProductionState)
    # ... add nodes and edges

    app = workflow.compile(
        checkpointer=checkpointer,
        # Enable interrupts for human-in-the-loop
        interrupt_before=["human_approval"],
        interrupt_after=["critical_action"]
    )

    return app
```

### 2. Monitoring and Logging
```python
import logging
from datetime import datetime

class LoggingMiddleware:
    def __init__(self, logger_name="langgraph"):
        self.logger = logging.getLogger(logger_name)

    def __call__(self, func):
        def wrapper(state):
            start_time = datetime.now()
            self.logger.info(f"Starting {func.__name__} at {start_time}")

            try:
                result = func(state)
                duration = datetime.now() - start_time
                self.logger.info(
                    f"Completed {func.__name__} in {duration.total_seconds():.2f}s"
                )
                return result
            except Exception as e:
                self.logger.error(f"Error in {func.__name__}: {str(e)}")
                raise

        return wrapper

# Apply to nodes
@LoggingMiddleware()
def production_node(state: AgentState) -> AgentState:
    # Your node logic here
    pass
```

## Troubleshooting

### Common Issues and Solutions

1. **State Size Too Large**
   - Problem: Checkpoint files become too large
   - Solution: Store large data externally, use references

2. **Memory Leaks**
   - Problem: Memory usage increases over time
   - Solution: Clean up unused state, use proper object disposal

3. **Concurrency Issues**
   - Problem: Race conditions in multi-threaded execution
   - Solution: Use proper locking mechanisms, avoid shared mutable state

4. **Tool Execution Failures**
   - Problem: Tools fail or timeout
   - Solution: Implement proper error handling and retry logic

## Requirements

Ensure these packages are installed in your environment:

```bash
pip install langgraph>=0.2.0
pip install langchain-core>=0.3.0
pip install langchain-openai>=0.1.0
pip install langchain-anthropic>=0.1.0
pip install psycopg2-binary  # For PostgreSQL persistence
pip install sqlalchemy      # Alternative persistence options
```

### Source Code Access

The LangGraph source code is managed as a git submodule with sparse-checkout to reduce size (66MB vs full repo):

```bash
# Update to latest version
cd source/langgraph
git pull origin main

# View sparse-checkout configuration
git sparse-checkout list

# Temporarily access full repo (if needed)
git sparse-checkout disable
# ... do work ...
git sparse-checkout reapply
```

**Key locations:**
- `source/langgraph/libs/langgraph/langgraph/` - Core API (StateGraph, nodes, edges)
- `source/langgraph/libs/prebuilt/langgraph/` - Prebuilt components (create_react_agent)
- `source/langgraph/examples/` - Official examples and tutorials
- `source/langgraph/docs/docs/` - Documentation (concepts, how-tos, reference)

See [SOURCE_STRUCTURE.md](SOURCE_STRUCTURE.md) for detailed navigation guide.

## Performance Tips

1. **Use streaming** for long-running operations
2. **Optimize state size** - avoid storing large objects
3. **Cache effectively** - implement proper caching strategies
4. **Monitor checkpoints** - keep checkpoint sizes reasonable
5. **Use async/await** for I/O-bound operations
6. **Batch operations** when possible to reduce overhead