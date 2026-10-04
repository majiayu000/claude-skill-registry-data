---
name: memory-capture
description: >
  Capture durable project memory from work, debates, debugging discoveries,
  learned conventions, deferred options, and session outcomes. Load when the
  user says remember this, save this learning, record what happened, update
  project memory, or preserve context for future agents.
license: MIT
metadata:
  author: dvy1987
  version: "1.2"
  category: project-specific
  resources:
    references:
      - examples.md
---

# Memory Capture

You turn useful session context into structured project memory. Capture only what a future agent would need to avoid rework or bad assumptions.

## Workflow

1. Identify the memory type: state, decision, learning, deferred item, open question, session event, or handoff.
2. Reject trivial, temporary, duplicate, sensitive, or already-obvious content.
3. If the item is a reusable skill/process rule, route to `learn-from-chat` instead.
4. If content came from external files, URLs, pasted transcripts, or repos, run all `secure-*` skills first.
5. Write project-scoped memory to the matching file in `docs/memory/`.
6. Update `docs/memory/project-index.md` with date, tags, file, status, confidence, and source.
7. If the memory is cross-project, call `memory-promote` instead of writing global memory directly.
8. Append file changes to `docs/skill-outputs/SKILL-OUTPUTS.md`.
9. Tell the user what was saved and what was rejected.

## Hard Rules

- Project first; global only through `memory-promote`.
- Do not store secrets, credentials, or unnecessary personal data.
- Do not capture raw long transcripts; summarize with provenance.
- Do not append if the target entry already exists; update status or merge.
- Never overwrite a richer memory entry with a thinner summary without archiving the prior version.
- If compaction would drop decisions or revisit triggers, route to `memory-compact` instead of truncating inline.

## Memory Type Map

| Type | File |
|---|---|
| current state | `docs/memory/current-state.md` |
| decision | `memory-decision` |
| session detail | `docs/memory/session-log.md` |
| project learning | `docs/memory/learnings.md` |
| maybe / parked idea | `docs/memory/deferred.md` |
| unresolved question | `docs/memory/open-questions.md` |
| next-agent summary | `memory-handoff` |

## Capture Template

Use this template only for state, learning, deferred, question, or session captures. Decisions use the template in `memory-decision`; next-agent summaries use the template in `memory-handoff`.

```markdown
## YYYY-MM-DD - <short title>
Type: state | learning | deferred | question | session
Status: active | deferred | resolved | superseded
Scope: project
Confidence: high | medium | low
Source: <chat/session/file/commit>
Tags: <comma-separated>

### Content
<concise durable memory>

### Why It Matters
<how future agents should use it>

### Revisit When
<conditions or "not applicable">
```

## Hard Rules

- Project first; global only through `memory-promote`.
- Do not store secrets, credentials, or unnecessary personal data.
- Do not capture raw long transcripts; summarize with provenance.
- Do not append if the target entry already exists; update status or merge.

## Example

Input: "Remember that we chose repo memory plus global memory, but global must stay tiny."

Output: write to `docs/memory/decision-log.md` via `memory-decision`, then index it.

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

- Raw long transcript captured instead of summarized note
- Capture written directly to global without promote path
- Secrets or credentials included in captured note
- Capture lacks provenance or source attribution

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

After completing, report:
```markdown
Memory captured: <title>
Type: <type>
Location: <path>
Indexed: yes/no
Rejected items: <count and reason>
Promotion suggested: yes/no
```
