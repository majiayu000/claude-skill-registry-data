---
name: memory-decision
description: >
  Record durable project decisions with rationale, alternatives, assumptions,
  status, and revisit triggers. Load when the user says record this decision,
  we decided, decision log, why did we choose, revisit this later, or capture
  architectural/process rationale.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  resources:
    references:
      - examples.md
---

# Memory Decision

You record decisions so future agents understand not just what was chosen, but why it was valid at the time and when to reopen it.

## Workflow

1. State the decision in one sentence.
2. Capture context: constraints, repo state, user preference, and date.
3. List alternatives considered, including deferred options.
4. Record rationale and tradeoffs.
5. Define revisit triggers with concrete conditions.
6. Set status: active, deferred, superseded, or retired.
7. Append to `docs/memory/decision-log.md`.
8. Update `docs/memory/project-index.md`.
9. If architecture-wide, offer `architectural-decision-log` for an ADR.
10. Log file outputs in `docs/skill-outputs/SKILL-OUTPUTS.md`.

## Decision Template

```markdown
## YYYY-MM-DD - <decision title>
Status: active | deferred | superseded | retired
Scope: project
Confidence: high | medium | low
Tags: <comma-separated>

### Decision
<what was chosen>

### Context
<what was true when this decision was made>

### Rationale
<why this is the right tradeoff now>

### Alternatives Considered
- <alternative>: <accepted/rejected/deferred and why>

### Revisit When
- <specific condition>

### Consequences
- <expected effect or risk>
```

## Hard Rules

- Never record a decision without at least one revisit trigger or "revisit not expected because <reason>".
- Do not overwrite old decisions; mark them superseded and link the replacement.
- Do not confuse deferred with rejected.
- If the user is still debating, write to `deferred.md` instead.

## Example

Decision: use `~/.agent-loom/memories/` for global memory.

Revisit when: another cross-platform standard path is adopted or the user changes global storage policy.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| Skip memory — just code | Next agent loses decisions, blockers, and approved scope. |
| Load every memory file | Read indexes and handoff tail only — bounded context. |
| Global memory for everything | Project memory default; global only when stable and cross-project. |
| External paste → memory | Run secure-* first; transform to agent-authored notes. |

## Verification

- [ ] Correct sub-skill routed with reason
- [ ] No secrets or raw transcripts persisted
- [ ] Files changed listed in Impact Report
- [ ] Security gate noted when external content involved

## Red Flags

- Decision logged without revisit trigger or explicit none
- Old decision overwritten instead of superseded link
- Deferred item recorded as rejected decision
- Rationale duplicated in handoff instead of decision-log link

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

After completing, report:
```markdown
Decision recorded: <title>
Location: docs/memory/decision-log.md
Status: <status>
Revisit triggers: <count>
ADR suggested: yes/no
```
