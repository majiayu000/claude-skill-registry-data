---
name: prototype
description: Use when building throwaway prototypes to answer specific design questions
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [prototyping, experimentation, design, exploration, quick]
---

# Prototype

Build throwaway prototypes to answer specific design questions before committing to an implementation. Fast exploration for high-risk decisions.

## Principles
- **Prototypes are throwaway** by design. Do not let prototype code leak into production.
- **One question per prototype.** Define the question before you start.
- **Minimum viable code** to answer the question. No error handling, no edge cases, no polish.

## Process
1. Define the question: what specific decision does this prototype inform?
2. Choose the axis: logic, UI, or both
3. Build the minimum code to answer the question
4. Present findings and make a decision
5. Discard or archive the prototype code

## Variation for UI prototypes
Use a separate UI prototype to explore visual/interaction questions independently from the logic.

## Common Pitfalls

- **Falling in love with the prototype**: Prototypes are throwaway by design. Do not let prototype code leak into production.
- **Over-engineering the prototype**: Prototypes should answer one question as quickly as possible. Adding error handling, edge cases, or polish defeats the purpose.
- **Not defining success criteria upfront**: Without a clear question to answer, the prototype has no completion criteria. Define what 'done' means before starting.

## Code Examples

```typescript
// Prototype: Can we implement real-time search with WebSockets?
// SPEND NO MORE THAN 30 MINUTES ON THIS

// 1. Server (basic WebSocket handler)
import { WebSocketServer } from "ws";
const wss = new WebSocketServer({ port: 8080 });

// 2. Client (quick test)
const ws = new WebSocket("ws://localhost:8080");

// 3. The question this answers:
//   - Is latency under 200ms for typical queries?
//   - Does the server handle 10 concurrent connections?
// DECISION: Proceed with WebSocket or switch to polling
```

## Verification Checklist

- [ ] Clear question defined that the prototype answers
- [ ] Minimum code written to answer the question
- [ ] Prototype marked as throwaway (not for production)
- [ ] Decision made based on prototype findings
