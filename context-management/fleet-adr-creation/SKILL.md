---
name: fleet-adr-creation
description: How the architect creates Architecture Decision Records — capturing the context, options, and rationale behind design decisions so future agents understand WHY, not just WHAT
user-invocable: false
---

# Architecture Decision Records

## Why ADRs Matter in a Fleet

Agents don't have persistent memory across sessions. An architect who
designs a pattern today won't remember why next week. An engineer who
encounters the pattern will ask "why not the simpler approach?"

ADRs answer that question before it's asked.

## When to Write an ADR

- Choosing between two viable approaches
- Introducing a new pattern or library
- Deviating from an established pattern
- Making a decision that constrains future choices

You DON'T need an ADR for:
- Obvious choices (use the existing pattern)
- Trivial decisions (variable naming)
- Decisions already documented elsewhere (fleet-elevation specs)

## ADR Structure

```
# ADR-{number}: {title}

## Status
{Proposed | Accepted | Deprecated | Superseded by ADR-{number}}

## Context
{What is the situation? What forces are at play? What constraints exist?
Be specific to the fleet — mention which agents, tools, or systems are affected.}

## Decision
{What we decided and WHY.}

## Options Considered

### Option A: {name}
- Pros: {list}
- Cons: {list}
- Fit for fleet: {how well this works in the multi-agent context}

### Option B: {name}
- Pros: {list}
- Cons: {list}
- Fit for fleet: {assessment}

## Consequences

### Positive
- {what gets better}

### Negative
- {what gets worse or constrained}

### Neutral
- {side effects that are neither good nor bad}

## Notes
{Any additional context, links to fleet-elevation docs, related ADRs}
```

## Quality Checklist

Before finalizing an ADR:
- [ ] Context explains WHY this decision was needed (not just what it is)
- [ ] At least 2 options were considered (even if one is obviously better)
- [ ] Consequences include negatives (if there are none, you haven't thought hard enough)
- [ ] Fleet context is explicit (which agents, tools, or systems are affected)
- [ ] A future agent reading this can understand the decision without additional context

## Where ADRs Live

- `docs/adr/` directory
- Numbered sequentially: `001-use-fastmcp-for-tools.md`
- Referenced in design contributions: "See ADR-001 for rationale"
- Referenced in fleet-elevation docs when decisions affect fleet architecture

## Common Mistakes

1. **Decision without options** — "We use X" without explaining why not Y
2. **Missing fleet context** — ADRs that read like generic software decisions
   instead of fleet-specific ones
3. **No consequences** — every decision has tradeoffs. If you can't find
   negative consequences, you're not looking hard enough
4. **Stale ADRs** — if a decision is superseded, mark it and link to the new one
5. **ADR for everything** — not every choice needs an ADR. Save them for
   decisions that constrain future options
