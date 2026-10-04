---
name: memory-handoff
description: >
  Write concise next-agent handoff summaries across sessions, tools, and coding
  agents. Load when the user says handoff, next agent should know, save context,
  summarize where we are, switching agents, before ending a meaningful session,
  or when the user asks to commit, push, commit and push, create a git commit,
  push to origin, or publish commits — commit/push requests MUST run this skill
  first to prepare handoff docs, then proceed with git operations.
license: MIT
metadata:
  author: dvy1987
  version: "1.5"
  category: project-specific
  resources:
    references:
      - examples.md
      - harness-trajectory-mining.md
---

# Memory Handoff

You preserve continuity for the next agent. A handoff is short, actionable, and focused on what would otherwise be lost.

## Trigger Policy

Run when a future agent would lose important context:
- Meaningful code changes, debugging discoveries, architecture debates, spec changes, or deferred decisions.
- End of a long session with unresolved work.
- Before switching agents or tools.
- User says "handoff", "summarize where we are", "save context", "memory handoff", or "next agent should know".
- **User asks to commit and/or push** ("commit", "create a commit", "commit these changes", "prepare commit", "push", "push to origin", "git push", "commit and push", "commit and push when ready") — run full handoff workflow **before** staging/committing/pushing so the next session has continuity. Pair with `git-workflow-and-versioning` for git operations after handoff is saved.

Do not run after trivial interactions.

## Workflow

1. Read `docs/memory/project-index.md` and latest `docs/memory/agent-handoffs.md` if present.
2. Inspect current session context and `git status --short`.
3. Summarize only durable context: done, debated, decisions, blockers, deferred items, next steps, revisit triggers.
4. Append the handoff to `docs/memory/agent-handoffs.md`.
5. Update `docs/memory/current-state.md` if the project state changed.
6. Update `docs/memory/project-index.md` with the handoff entry.
7. **Update knowledge graph** — run `python3 .agents/skills/knowledge-graph/scripts/build_graph.py --incremental`. If it fails, add `### Graph` note in handoff; do not block save.
8. Append changes to `docs/skill-outputs/SKILL-OUTPUTS.md`.
9. **Optional harness mining:** When session had repeated agent failures and harness evolution is queued, distill failure digests per `references/harness-trajectory-mining.md` — never raw transcripts.

## Template

```markdown
## YYYY-MM-DD HH:MM - Handoff

### Done
- <completed work>

### Debated
- <tradeoff and conclusion>

### Decisions
- <decision and link/reference>

### Deferred
- <parked item and why>

### Next Agent Should Know
- <highest-value continuity note>

### Revisit Triggers
- <conditions that reopen decisions>

### Working Tree
- <clean or relevant dirty files>
```

## Hard Rules

- Keep each handoff under 80 lines.
- Do not include secrets, tokens, or raw private data.
- Link to decision entries instead of repeating long rationale.
- If the handoff gets repetitive, call `memory-compact`.

## Example

User: "I'm moving this to another agent, save a handoff."

Output: append a timestamped handoff with current status, unresolved tasks, and files touched.

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

- Handoff exceeds 80-line budget
- Secrets tokens or raw private data in handoff body
- Long decision rationale pasted instead of log link
- Git state omitted from handoff next-agent context

## Prune Log
Last pruned: 2026-07-05
- Deep learn-from: harness-trajectory-mining.md for RHO prerequisite path


## Impact Report

After completing, report:
```markdown
Handoff saved: docs/memory/agent-handoffs.md
Current state updated: yes/no
Index updated: yes/no
Next recommended action: <one sentence>
```
