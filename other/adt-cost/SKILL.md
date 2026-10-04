---
name: cost
description: Track and report token usage and estimated cost per session, agent, and phase
triggers:
  - cost
  - how much did that cost
  - token usage
  - budget
  - spending
---

# Cost

Track token usage and cost across the session.

## When to Report

- After completing a major phase
- When switching agents or tiers
- At session end
- When asked explicitly

## Output

```text
Cost Report
───────────
Phase:   <current phase name>
Agent:   <agent name> (<tier>)
Tokens:  <input> in / <output> out
Est:     $<amount>
Session: $<running total>
Budget:  $<remaining or unlimited>
```

## Rules

- Report in-line, not as a separate step — cost is metadata, not a task
- Never stop work to report cost unless budget is exceeded
- On budget exceeded: warn, continue, and note the overage
- Track per-agent to identify which agents consume the most
- Use the cheapest tier that works — cost awareness drives routing
