---
name: t1k:predict
description: "5 expert personas debate proposed changes before implementation. Catches architectural, security, performance, and UX issues early. Use before major features or risky refactors."
keywords: [predict, debate, review, risky, tradeoffs, expert, pre-implementation]
version: 1.0.0
argument-hint: "<proposed change description>"
effort: medium
origin: theonekit-core
repository: The1Studio/theonekit-core
module: null
protected: true
---

# TheOneKit Predict — Expert Debate

5 expert personas review a proposed change and debate its merits, risks, and alternatives.

## Usage
```
/t1k:predict "Add caching layer to API responses"
```

## Personas

| # | Persona | Focus | Looks For |
|---|---------|-------|-----------|
| 1 | **Architect** | System design, scalability, coupling | Over-engineering, tight coupling, wrong abstractions, missing extensibility |
| 2 | **Security** | Attack surface, data flow, trust boundaries | Auth bypass, injection, data exposure, insufficient logging |
| 3 | **Performance** | Bottlenecks, memory, latency | N+1 queries, unnecessary allocations, cache invalidation issues |
| 4 | **UX/DX** | User/developer impact, edge cases | Breaking changes, poor error messages, confusing APIs |
| 5 | **Devil's Advocate** | Assumptions, alternatives, hidden costs | "What if this is the wrong approach entirely?" |

## Process

1. Read the proposed change description
2. Each persona reviews independently:
   - State their concerns (1-3 bullet points)
   - Rate risk for their domain (1-5 scale)
   - Suggest mitigations
3. Synthesize:
   - **Consensus risk score** (average of 5 ratings)
   - **Prioritized concern list** (highest risk first)
   - **Go/No-Go recommendation** with conditions

## Output Format

```
## Prediction: {change description}

### Architect (Risk: 3/5)
- Concern: ...
- Mitigation: ...

### Security (Risk: 2/5)
- Concern: ...
- Mitigation: ...

### Performance (Risk: 4/5)
- Concern: ...
- Mitigation: ...

### UX/DX (Risk: 1/5)
- Concern: ...
- Mitigation: ...

### Devil's Advocate (Risk: 3/5)
- Alternative: ...
- Hidden cost: ...

### Consensus
- **Overall Risk: 2.6/5**
- **Recommendation: GO with conditions**
- **Top 3 concerns to address:**
  1. ...
  2. ...
  3. ...
```

## Anti-Rationalization Guards

| Trap | Reality |
|------|---------|
| "This change is too simple for a debate" | Simple changes with hidden complexity cause the worst incidents. |
| "We already discussed this" | Discussion ≠ structured risk assessment. |
| "The user wants to start coding" | 5 minutes of prediction saves 5 hours of debugging. |

## When to Use
- Before any change affecting >3 files
- Before any security-sensitive change
- Before any architectural decision
- When the team disagrees on approach
- When risk feels "medium" or higher
