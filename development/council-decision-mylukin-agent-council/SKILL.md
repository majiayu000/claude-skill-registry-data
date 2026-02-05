---
name: council-decision
description: Get multi-model AI consensus on complex questions using Claude, Codex, and Gemini
---

# Council Decision Skill

Get multi-model AI consensus on complex decisions using the agent-council's 3-stage voting pipeline.

## When to Use

Automatically invoke this skill when facing:

- **Architectural design decisions** that affect system structure
- **Technology stack choices** with multiple valid options
- **Implementation approach evaluation** for complex features
- **Design pattern selection** when trade-offs are unclear
- **Multi-step planning** for large tasks

## How It Works

The skill runs the `agent-council` CLI which:

1. Sends your question to Claude, Codex, and Gemini
2. Each model provides an independent response
3. Models peer-rank each other's answers
4. A chairman synthesizes the final recommendation

## Usage

When you encounter a complex decision point:

1. Formulate the question clearly
2. Run: `agent-council "your question here"`
3. Wait for the 3-stage pipeline to complete
4. Use the synthesized answer to guide implementation

## Example Questions

- "What's the best way to implement real-time updates: WebSockets, SSE, or polling?"
- "Should this service use SQL or NoSQL database?"
- "What caching strategy would work best for this API?"
- "How should we structure error handling in this module?"

## Prerequisites

The `agent-council` CLI must be installed:

```bash
npm install -g agent-council
```

## Benefits

- **Reduced bias**: Multiple AI models reduce single-model bias
- **Diverse perspectives**: Different models have different strengths
- **Quality ranking**: Peer evaluation identifies best answers
- **Synthesized wisdom**: Chairman combines best insights
