---
name: memory-compact
description: >
  Compress bloated project or global memory while preserving decisions, rationale,
  revisit triggers, provenance, and active user preferences. Load when memory
  exceeds budget, global memory is too large, session logs are repetitive, or
  before appending to an over-budget memory file.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  resources:
    references:
      - examples.md
---

# Memory Compact

You reduce memory bloat without losing the reasoning future agents need.

## Workflow

1. Identify scope: project file, global file, or whole store.
2. Check line counts and active budgets.
3. Classify entries as keep, merge, summarize, archive, delete-candidate, or unsafe.
4. Preserve active decisions, rationale, alternatives, revisit triggers, and provenance.
5. Merge duplicate or overlapping entries.
6. Move old session detail to `archived/` after producing a rollup summary.
7. For global memory, prefer deletion or archival over long summaries.
8. Update routing/index files after compaction.
9. Log project file outputs in `docs/skill-outputs/SKILL-OUTPUTS.md`.

## Global Budgets

- `user-preferences.md` <= 100 lines.
- `global-agent-rules.md` <= 150 lines.
- `reusable-learnings.md` <= 200 lines.
- `global-index.md` <= 250 lines.
- Active global total target: 500-700 lines.

## Compaction Rules

| Entry type | Action |
|---|---|
| active decision | keep or tighten |
| superseded decision | archive with replacement link |
| repeated session details | roll up |
| low-confidence maybe | keep local or archive |
| obvious general advice | delete |
| sensitive content | invoke `memory-forget` |

## Hard Rules

- Never append to an over-budget file without compacting first.
- Never delete active decisions, revisit triggers, or provenance.
- Never compact global memory without user approval.
- **Shrink guard:** Refuse compaction that removes >50% of indexed entries unless the user explicitly approves — archive superseded content instead of deleting.
- Never increase global memory during compaction.
- If meaning would change, stop and ask the user.

## Output Format

```markdown
Compaction complete
Scope: <project/global/file>
Before: <line count>
After: <line count>
Archived: <count/path>
Deleted: <count/reason>
Preserved decisions: <count>
```

## Example

If `reusable-learnings.md` is 240 lines, merge duplicate lessons, archive stale items, and stop only when it is <= 200 lines.

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

- Append to over-budget file without compacting first
- Active decisions or revisit triggers deleted during compact
- Global memory compacted without user approval
- Provenance stripped when merging duplicate entries

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

After completing, report:
```markdown
Memory compacted: <path>
Line reduction: <before> -> <after>
Budget compliant: yes/no
Entries archived: <count>
Entries deleted: <count>
```
