---
name: convex-agents
displayName: Convex Agents
description: Building AI agents with the Convex Agent component including thread management, tool integration, streaming responses, RAG patterns, and workflow orchestration
version: 1.0.0
author: Convex
tags: [convex, agents, ai, llm, tools, rag, workflows]
---

# Convex Agents

Build persistent, stateful AI agents with Convex including thread management, tool integration, streaming responses, RAG patterns, and workflow orchestration.

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: https://docs.convex.dev/ai
- Convex Agent Component: https://www.npmjs.com/package/@convex-dev/agent
- For broader context: https://docs.convex.dev/llms.txt

## Instructions

### Why Convex for AI Agents

- **Persistent State** - Conversation history survives restarts
- **Real-time Updates** - Stream responses to clients automatically
- **Tool Execution** - Run Convex functions as agent tools
- **Durable Workflows** - Long-running agent tasks with reliability
- **Built-in RAG** - Vector search for knowledge retrieval

## Code Patterns

Full code samples live in the reference file. Read it before writing the matching code.

Sections in `references/patterns.md`:

- Setting Up Convex Agent
- Thread Management
- Sending Messages and Streaming Responses
- Tool Integration
- Agent with Tools
- RAG (Retrieval Augmented Generation)
- Workflow Orchestration
- Complete Chat Application Schema
- React Chat Component

## Best Practices

- Never run `npx convex deploy` unless explicitly instructed
- Never run any git commands unless explicitly instructed
- Store conversation history in Convex for persistence
- Use streaming for better user experience with long responses
- Implement proper error handling for tool failures
- Use vector indexes for efficient RAG retrieval
- Rate limit agent interactions to control costs
- Log tool usage for debugging and analytics

## Common Pitfalls

1. **Not persisting threads** - Conversations lost on refresh
2. **Blocking on long responses** - Use streaming instead
3. **Tool errors crashing agents** - Add proper error handling
4. **Large context windows** - Summarize old messages
5. **Missing embeddings for RAG** - Generate embeddings on insert

## References

- Convex Documentation: https://docs.convex.dev/
- Convex LLMs.txt: https://docs.convex.dev/llms.txt
- Convex AI: https://docs.convex.dev/ai
- Agent Component: https://www.npmjs.com/package/@convex-dev/agent
