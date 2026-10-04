---
name: memory-promote
description: >
  Promote project-specific memories into strict, small global memory only when
  they are cross-project, stable, useful, safe, and worth the global context
  cost. Load when the user says make this global, remember across projects,
  save this globally, or promote this learning.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  resources:
    references:
      - examples.md
---

# Memory Promote

You are the global memory gatekeeper. Most memories should stay local. Promote only durable cross-project rules or user preferences.

## Global Store

`~/.agent-loom/memories/`

Active budgets:
- `user-preferences.md`: 100 lines.
- `global-agent-rules.md`: 150 lines.
- `reusable-learnings.md`: 200 lines.
- `global-index.md`: 250 lines.
- Total active target: 500-700 lines, excluding `archived/`.

## Workflow

1. Read the source project memory entry and provenance.
2. Classify target: user preference, global agent rule, or reusable learning.
3. Apply promotion gate: cross-project, stable, repeatedly useful, non-sensitive, and not obvious.
4. Check line counts for the target global file and `global-index.md`.
5. If any budget would be exceeded, invoke `memory-compact` before writing.
6. Write a concise global entry with source project, date, confidence, and scope.
7. Update `~/.agent-loom/memories/global-index.md`.
8. Update the source project entry with "promoted to global" provenance.

## Promotion Gate

Promote only if all are true:
- Applies beyond one repo.
- Likely useful in future sessions.
- Stable enough not to churn weekly.
- Safe to store globally.
- Short enough to justify active recall.

## Hard Rules

- Global memory is not a journal.
- Never promote secrets, credentials, internal URLs, or private project facts.
- Never promote low-confidence maybes; keep them local in `deferred.md`.
- Never append past budget; compact first.

## Output Format

```markdown
Promotion verdict: promote | keep local | reject
Target file: <global path or none>
Reason: <why>
Budget status: <within budget | compacted | blocked>
Source updated: <yes/no>
```

## Example

Project learning: "User prefers concise, direct engineering updates."

Verdict: promote to `user-preferences.md` if repeatedly confirmed and not already present.

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

- Low-confidence maybe promoted to global memory
- Internal URLs or private project facts promoted globally
- Global memory used as unstructured journal dump
- Promote executed without user intent confirmation

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

After completing, report:
```markdown
Memory promotion complete
Verdict: <promote/keep local/reject>
Global file changed: <path or none>
Budget after write: <line count>
Source provenance updated: yes/no
```
