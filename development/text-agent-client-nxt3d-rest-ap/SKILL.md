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
# Talk to the agent for guidance
curl -X POST http://agent.example.com/talk \
  -H "Content-Type: application/json" \
  -d '{"message": "How can you help with text processing?"}'
```

### Agent Communication Workflow
1. **Discover Capabilities**: Check /.well-known/restap.json for available operations
2. **Talk First**: Use /talk endpoint to understand agent capabilities and get guidance
3. **Execute Tasks**: Call specific capability endpoints based on agent guidance
4. **Monitor Progress**: Check /news endpoint for long-running operation updates

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
- Monitor /news for asynchronous operation completion
- Cache agent capabilities to reduce discovery overhead