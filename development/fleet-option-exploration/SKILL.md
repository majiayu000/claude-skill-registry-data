---
name: fleet-option-exploration
description: How the architect researches multiple approaches during investigation stage — not just the first idea, but structured option comparison with tradeoffs.
---

# Option Exploration — Architect's Investigation Skill

Investigation stage exists specifically for you to explore OPTIONS — plural. The methodology blocks fleet_task_complete during investigation precisely because you shouldn't commit to an approach yet. Your job is to find at least 2-3 viable options, evaluate tradeoffs, and present them to the PO.

## Why Multiple Options Matter

When you present only one option, the PO can only say yes or no. When you present three options with tradeoffs, the PO can make an INFORMED decision. This is the difference between "I chose this" and "Here are the options, here's my recommendation, you decide."

The PO's decision is always better than the architect's assumption.

## The Exploration Framework

### Step 1: Define Evaluation Criteria

Before researching options, define what matters for THIS task:

| Criterion | When It Matters Most |
|-----------|---------------------|
| Complexity | Always — simpler is better unless complexity buys something specific |
| Performance | High-traffic paths, data-intensive operations |
| Maintainability | Long-lived code, multiple contributors |
| Testability | Core business logic, complex state |
| Migration cost | Existing codebase, running production |
| Team familiarity | Fleet agents' existing patterns and conventions |
| Dependency risk | External libraries, version pinning, license |

For the fleet, **team familiarity** means: does this follow patterns already established in the codebase? The engineer reads your design_input and implements it — unfamiliar patterns increase rejection risk.

### Step 2: Research At Least 3 Options

Use these research strategies:

1. **Codebase precedent** — How does the fleet handle similar problems? (code-explorer sub-agent)
2. **Library docs** — What do official docs recommend? (context7 plugin)
3. **Adversarial debate** — Stress-test your ideas with multiple LLMs (/adversarial-spec)
4. **Prior art** — What did other projects do? (investigation document)

For each option, capture:
- **Approach name** — clear, specific
- **How it works** — concrete, not abstract
- **Target files** — where changes would go
- **Pros** — what it does well
- **Cons** — what it does poorly
- **Risk** — what could go wrong
- **Effort** — story points estimate

### Step 3: Produce Comparison Table

Use `arch_option_comparison(task_id)` to prepare the comparison context, then produce a structured document:

```
## Option Comparison: {task title}

### Criteria (weighted for this task):
1. Complexity (high weight — small team, maintenance matters)
2. Testability (high weight — QA predefinition depends on it)
3. Migration cost (medium — existing code needs updating)

### Option A: {name}
Approach: ...
Target files: fleet/core/X.py (new), fleet/infra/Y.py (modify)
Pros: Simple, follows existing patterns (Repository in mc_client.py)
Cons: Doesn't scale past 100k records
Risk: Performance cliff at scale
Effort: 3 SP

### Option B: {name}
Approach: ...
[same structure]

### Option C: {name}
[same structure]

### Recommendation: Option A
Rationale: For POC phase, simplicity and testability outweigh scalability.
When to revisit: If data volume exceeds 50k records, revisit Option B.
```

### Step 4: Post as Investigation Document

Use `fleet_artifact_create("investigation_document", "Options for {task}")` and build it progressively with `fleet_artifact_update`. The PO sees the completeness tracking and can review at any point.

## When NOT to Explore Multiple Options

- **Subtask with clear scope** — single obvious approach, just do it
- **Fix task** — the problem and solution are already specified
- **Spike** — research is the deliverable, not a decision
- **PM directed** — PO already decided the approach, you're just designing the details

In these cases, your design_input can go straight to the chosen approach without a comparison table.

## Integration With Other Systems

Your investigation document feeds into:
- **Reasoning stage** — you or the engineer uses it to produce the implementation plan
- **QA predefinition** — QA reads your options to understand what test scenarios matter
- **Fleet-ops review** — reviewer checks that the implemented approach matches the chosen option
- **Accountability trail** — investigation document proves the thinking happened
