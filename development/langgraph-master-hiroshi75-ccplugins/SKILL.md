---
name: langgraph-master
description: Use when specifying or implementing LangGraph applications - from architecture planning and specification writing to actual code implementation. Also use for designing agent workflows or learning LangGraph patterns. This is a comprehensive guide for building AI agents with LangGraph, covering core concepts, architecture patterns, memory management, tool integration, and advanced features.
---

# LangGraph Agent Construction Skill

A comprehensive guide for building AI agents using LangGraph.

## 📚 Learning Content

### [01. Core Concepts](01_core_concepts_overview.md)

Understanding the three core elements of LangGraph

- [State](01_core_concepts_state.md)
- [Node](01_core_concepts_node.md)
- [Edge](01_core_concepts_edge.md)
- Advantages of the graph-based approach

### [02. Graph Architecture](02_graph_architecture_overview.md)

Six major graph patterns and agent design

- [Workflow vs Agent Differences](02_graph_architecture_workflow_vs_agent.md)
- [Prompt Chaining (Sequential Processing)](02_graph_architecture_prompt_chaining.md)
- [Parallelization](02_graph_architecture_parallelization.md)
- [Routing (Branching)](02_graph_architecture_routing.md)
- [Orchestrator-Worker](02_graph_architecture_orchestrator_worker.md)
- [Evaluator-Optimizer](02_graph_architecture_evaluator_optimizer.md)
- [Agent (Autonomous Tool Usage)](02_graph_architecture_agent.md)
- [Subgraph](02_graph_architecture_subgraph.md)

### [03. Memory Management](03_memory_management_overview.md)

Persistence and checkpoint functionality

- [Checkpointer](03_memory_management_checkpointer.md)
- [Store (Long-term Memory)](03_memory_management_store.md)
- [Persistence](03_memory_management_persistence.md)

### [04. Tool Integration](04_tool_integration_overview.md)

External tool integration and execution control

- [Tool Definition](04_tool_integration_tool_definition.md)
- [Command API (Control API)](04_tool_integration_command_api.md)
- [Tool Node](04_tool_integration_tool_node.md)

### [05. Advanced Features](05_advanced_features_overview.md)

Advanced functionality and implementation patterns

- [Human-in-the-Loop (Approval Flow)](05_advanced_features_human_in_the_loop.md)
- [Streaming](05_advanced_features_streaming.md)
- [Map-Reduce Pattern](05_advanced_features_map_reduce.md)

### [06. LLM Model IDs](06_llm_model_ids.md)

Model ID reference for major LLM providers. Always refer to this document when selecting model IDs. Do not use models not listed in this document.

- Google Gemini model list
- Anthropic Claude model list
- OpenAI GPT model list
- Usage examples and best practices with LangGraph

### Implementation Examples

Practical agent implementation examples

- [Basic Chatbot](example_basic_chatbot.md)
- [RAG Agent](example_rag_agent.md)

## 📖 How to Use

Each section can be read independently, but reading them in order is recommended:

1. First understand LangGraph fundamentals in "Core Concepts"
2. Learn design patterns in "Graph Architecture"
3. Grasp implementation details in "Memory Management" and "Tool Integration"
4. Master advanced features in "Advanced Features"
5. Check practical usage in "Implementation Examples"

Each file is kept short and concise, allowing you to reference only the sections you need.

## 🤖 Efficient Implementation: Utilizing Subagents

To accelerate LangGraph application development, utilize the dedicated subagent `langgraph-master-plugin:langgraph-engineer`.

### Subagent Characteristics

**langgraph-master-plugin:langgraph-engineer** is an agent specialized in implementing functional modules:

- **Functional Unit Scope**: Implements complete functionality with multiple nodes, edges, and state definitions as a set
- **Parallel Execution Optimization**: Designed for multiple agents to develop different functional modules simultaneously
- **Skill-Driven**: Always references the langgraph-master skill before implementation
- **Complete Implementation**: Generates fully functional modules (no TODOs or placeholders)
- **Appropriate Size**: Functional units of about 2-5 nodes (subgraphs, workflow patterns, tool integrations, etc.)

### When to Use

Use langgraph-master-plugin:langgraph-engineer in the following cases:

1. **When functional module implementation is needed**

   - Decompose the application into functional units
   - Efficiently develop each function through parallel execution

2. **Subgraph and pattern implementation**

   - RAG search functionality (retrieve → rerank → generate)
   - Human-in-the-Loop approval flow (propose → wait_approval → execute)
   - Intent analysis functionality (analyze → classify → route)

3. **Tool integration and memory setup**
   - Complete tool integration module (definition → execution → processing → error handling)
   - Memory management module (checkpoint setup → persistence → restoration)

### Practical Example

**Task**: Build a chatbot with intent analysis and RAG search

**Parallel Execution Pattern**:

```
Planner → Decompose into functional units
  ├─ langgraph-master-plugin:langgraph-engineer 1: Intent analysis module (parallel)
  │  └─ analyze + classify + route nodes + conditional edges
  └─ langgraph-master-plugin:langgraph-engineer 2: RAG search module (parallel)
     └─ retrieve + rerank + generate nodes + state management
Orchestrator → Integrate modules to assemble graph
```

### Usage Method

1. **Decompose into functional modules**

   - Decompose large LangGraph applications into functional units
   - Verify that each module can be implemented and tested independently
   - Verify that module size is appropriate (about 2-5 nodes)

2. **Implement common parts first**

   - State used across the entire graph
   - Common tool definitions and common nodes used throughout

3. **Parallel Execution**

   Assign one functional module implementation to each langgraph-master-plugin:langgraph-engineer agent and execute in parallel

   - Implement independent functional modules simultaneously

4. **Integration**
   - Incorporate completed modules into the graph
   - Verify operation through integration testing

### Testing Method

- Perform unit testing for each functional module
- Verify overall operation after integration. In many cases, there's an API key in .env, so load it and run at least one successful test case
  - If the successful case doesn't work well, code review is important, but roughly pinpoint the location, add appropriate logs to identify the cause, think carefully, and then fix.

### Functional Module Examples

**Appropriate Size (langgraph-master-plugin:langgraph-engineer scope)**:

- RAG search functionality: retrieve + rerank + generate (3 nodes)
- Intent analysis: analyze + classify + route (2-3 nodes)
- Approval workflow: propose + wait_approval + execute (3 nodes)
- Tool integration: tool_call + execute + process + error_handling (3-4 nodes)

**Too Small (individual implementation is sufficient)**:

- Single node only
- Single edge only
- State field definition only

**Too Large (further decomposition needed)**:

- Complete chatbot application
- Entire system containing multiple independent functions

### Notes

- **Appropriate Scope Setting**: Verify that each task is limited to one functional module
- **Functional Independence**: Minimize dependencies between modules
- **Interface Design**: Clearly document state contracts between modules
- **Integration Plan**: Plan the integration method after module implementation in advance

## 🔗 Reference Links

- [LangGraph Official Documentation](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
