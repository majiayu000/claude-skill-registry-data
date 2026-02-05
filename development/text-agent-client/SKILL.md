---
name: text-agent-client
description: Interact with the Text Processing AI Agent. Use when you need text analysis, formatting, or processing capabilities from the agent.
allowed-tools: Bash(curl:*), Read
---

# Text Processing Agent Client Skill

## Overview
This skill teaches how to effectively interact with the Text Processing AI Agent's REST-AP endpoints for various text operations.

## When to Use This Skill
- Need text analysis or processing
- Want to format or transform text content
- Require document processing capabilities
- Need content validation or cleaning

## Agent Interaction Patterns

### Basic Text Operations
```bash
# Echo text through the agent
curl -X POST http://agent.example.com/text/echo \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World"}'
```

### Conversational Interaction
```bash
# Talk to the agent (one-directional: send query, receive LLM response)
curl -X POST http://agent.example.com/talk \
  -H "Content-Type: application/json" \
  -d '{"message": "How can you help with text processing?"}'
```

### Agent Communication Workflow
1. **Discover Capabilities**: Check /.well-known/restap.json for available operations
2. **Talk First**: Use POST /talk endpoint (one-directional: send query, agent receives it and triggers LLM response)
3. **Execute Tasks**: Call specific capability endpoints based on agent guidance
4. **News Endpoint**: Use /news as a single bidirectional endpoint:
   - **GET /news**: Read updates (no processing)
   - **POST /news**: Write replies/messages (no processing)

**Key Points**:
- `/talk` is **one-directional** - client sends query, agent responds with LLM output
- `/news` is **bidirectional** - can read (GET) and write (POST), but **never triggers agent processing**

## Best Practices
- Always check agent capabilities before making requests
- Use the /talk endpoint to understand proper usage patterns
- Handle both successful responses and error cases
- Respect rate limits and implement appropriate backoff
- Validate response formats before processing

## Common Interaction Patterns
- Start with capability discovery via /.well-known/restap.json
- Use /talk for complex requests or when unsure of proper usage
- Implement proper error handling for network issues
- Poll GET /news for asynchronous operation completion
- Use POST /news to send replies directly to other agents (prevents loops)
- Use `since` parameter when polling: GET /news?since=timestamp
- Cache agent capabilities to reduce discovery overhead

## The /news Endpoint: Single Entrypoint for Reading and Writing

The `/news` endpoint is a **single bidirectional entrypoint** that handles both reading and writing. The critical property: **it never triggers agent processing**.

### Reading from /news (GET)
```bash
# Poll for updates (no processing triggered)
curl http://agent.example.com/news?since=0
```

### Writing to /news (POST)
```bash
# Send reply to another agent (no processing triggered)
curl -X POST http://agent-a.example.com/news \
  -H "Content-Type: application/json" \
  -d '{
    "type": "reply",
    "from": "agent-b",
    "in_reply_to": "query_123",
    "message": "Here is my response..."
  }'
```

### Complete Flow Example
```
Agent 1 → POST /talk → Agent 2 (one-directional: Agent 2 receives query, triggers LLM response)
Agent 2 → POST /news → Agent 1 (bidirectional write: just stored, no processing)
Agent 3 → GET /news → Agent 2 (bidirectional read: just reads, no processing)
```

**Why this matters**: 
- `/talk` is one-directional - client sends query, agent responds with LLM output
- `/news` is bidirectional but never triggers processing - prevents infinite loops
- When you send a reply via `POST /news`, the receiving agent doesn't process it - it's just stored
- This allows safe bidirectional communication without triggering endless processing cycles