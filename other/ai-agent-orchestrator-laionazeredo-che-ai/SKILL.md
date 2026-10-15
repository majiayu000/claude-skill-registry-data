---
name: "ai-agent-orchestrator"
description: "Advanced guide for developing and orchestrating AI agents using LangChain, LangGraph, and Swarm patterns. Covers memory management, tool usage, human-in-the-loop, and MCP integration."
---

# AI Agent Orchestrator Guide

This skill provides the architectural framework for building robust, autonomous, and multi-agent AI systems.

## 🤖 Agent Design & Logic
- **Single vs Multi-Agent**: Choose Single Agent for linear tasks and Multi-Agent (orchestrated via LangGraph or Swarm) for complex, parallelizable workflows.
- **Reasoning Patterns**: Use ReAct (Reason + Act) for standard tool usage. Leverage Chain-of-Thought (CoT) for complex reasoning before action.
- **MCP Integration**: Use Model Context Protocol (MCP) to provide agents with secure, standardized access to local and remote tools/data.

## 🧠 Memory & Context Management
- **Persistence**: Use Checkpointers (LangGraph) to persist state across sessions and enable "Time Travel" (debugging/rewinding state).
- **Short-term vs Long-term**: Manage ephemeral session state separately from durable user/project memory.
- **Context Window**: Prune or summarize message history to stay within token limits while maintaining essential context.

## 🔗 LangChain & LangGraph
- **Chains**: Use LCEL (LangChain Expression Language) for composing modular, readable agent components.
- **Graphs**: Define state machines using LangGraph for non-linear, cyclic agent workflows.
- **Human-in-the-Loop**: Implement `interrupt()` points for critical decisions requiring user approval (e.g., payments, file deletions).

## 🛠 Tool Usage & Security
- **Tool Definition**: Tools must have clear, descriptive names and JSON schemas.
- **Validation**: Sanitize tool inputs using Pydantic or Zod.
- **Security**: Never give agents access to root shell or unrestricted network calls without strict sandboxing and human oversight.

## 🧪 Testing & Observability
- **Evaluation**: Use LangSmith or similar tools to trace agent runs and evaluate performance against benchmarks.
- **Logging**: Log all tool calls, agent thoughts, and state transitions for auditability.

## 🔗 References
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [Swarm (OpenAI) Patterns](https://github.com/openai/swarm)
