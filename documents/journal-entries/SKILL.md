---
name: journal-entries
description: How to write structured journal entries for the orchestrator's reflective log. Use when creating or appending journal entries at the end of a cycle, after significant decisions, or when recording observations and lessons learned.
user-invocable: false
---

# Writing Journal Entries

Procedure for creating and maintaining the orchestrator's reflective journal in `docs/journal/`.

## File structure

- One file per day: `docs/journal/YYYY-MM-DD.md`
- If the file already exists, **append** a new entry (separated by `---`)
- If creating a new day's file, start with the header

### New file header

```markdown
# Journal — YYYY-MM-DD

Reflective log for the schema-org-json-ld orchestrator.

---
```

## Entry structure

Each entry follows this template:

```markdown
## YYYY-MM-DD — Cycle N: Short Descriptive Title

### Context

One or two sentences explaining what triggered this cycle's work and the current project state.

### Previous commitment follow-through

**Required.** Before writing new commitments, read the previous cycle's journal entry and evaluate whether that cycle's "Concrete behavior change" was followed. Record the outcome:

- **Followed**: The commitment was honored this cycle. Brief evidence.
- **Not followed**: The commitment was not honored. Why not? Was it forgotten, deprioritized, or superseded?
- **Not applicable**: The commitment didn't apply this cycle (e.g., no relevant work occurred).
- **No prior commitment**: First cycle or no commitment was made last cycle.

This converts the journal from write-only to read-write — each entry builds on the previous rather than starting fresh. Per audit #113.

### [Themed sections]

Use descriptive headings that categorize the content. Common heading patterns:

- `### Observation — [what you noticed]`
- `### Decision — [what you chose and why]`
- `### Lesson — [what you learned]`
- `### Pattern — [a reusable insight]`
- `### Discovery — [something unexpected found]`

### Open questions

Optional. Bullet list of unresolved questions for future cycles.
```

## Content guidelines

### What to write about

- **Observations**: What happened and why it matters. E.g., "CI passed on PHP 8.5 with zero changes needed — the codebase's modern PHP practices pay off."
- **Decisions**: What you chose and the reasoning. E.g., "Dispatched both tasks in parallel because they modify non-overlapping files."
- **Lessons**: What went wrong and the takeaway. E.g., "Copilot can't rebase — it adds fix commits on top. Future parallel PRs should expect orchestrator-assisted rebase."
- **Patterns**: Reusable insights. E.g., "The Write-then-@file approach avoids all shell quoting issues."
- **Stats**: When they tell a story. Don't add stats for their own sake.

### What NOT to write

- Play-by-play narration of every command run
- Repetitive "all checks clean, nothing to do" entries (a brief note is fine)
- Vanity metrics or streak counting
- Implementation details that belong in worklog entries
- Speculation without evidence

### Tone

- Plain language, honest, reflective
- First person (the orchestrator's perspective)
- Concise — a typical entry is 15-40 lines
- Focus on insights, not activity

## Cross-references

Always use clickable markdown links for issue and PR references:

```markdown
[#N](https://github.com/EvaLok/schema-org-json-ld/issues/N)
[PR #N](https://github.com/EvaLok/schema-org-json-ld/issues/N)
```

GitHub auto-redirects `/issues/N` to `/pull/N` for PRs, so `/issues/` works for all references.

For QC repo references, use full URLs:

```markdown
[QC #N](https://github.com/EvaLok/schema-org-json-ld-qc/issues/N)
```

## Relationship to other files

| File | Purpose | Relationship |
|------|---------|-------------|
| `docs/worklog/YYYY-MM-DD/HHMMSS-name.md` | Operational log — what happened, what's in-flight, next steps | Journal reflects on worklog events |
| `docs/state.json` | Machine-readable state | Journal explains decisions that led to state changes |
| `doc/adr/` | Architecture Decision Records | Journal may reference ADRs for major decisions |
| `JOURNAL.md` (legacy) | Original single-file journal | Superseded by `docs/journal/` directory structure |

## When to write

- **End of every cycle**: At minimum, a brief entry noting what happened
- **After significant decisions**: Record the reasoning while it's fresh
- **After discovering something unexpected**: Capture the insight
- **After a failure or mistake**: Document what went wrong and the fix

## Committing

Journal entries are state files — commit and push directly to master:

```bash
git add docs/journal/YYYY-MM-DD.md
```

Commit as part of the regular state update at the end of each cycle. Do not create separate commits for journal entries alone unless the entry captures a time-sensitive insight.
