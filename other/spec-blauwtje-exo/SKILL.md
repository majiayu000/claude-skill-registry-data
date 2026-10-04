---
name: spec
description: "Use when a request, or new wishes for a stored brief, issue or plan, leaves a product decision open: what counts as done, data, architecture or a trade-off. When a new visual surface does not name its displayed data, settings, or behavior, spec decides those first; design-ui follows for presentation. Not for a clear goal, a failure, or visual-only work."
argument-hint: <outcome to shape>
---

# Shaping

## Steps

1. **Gate.**
   - Spec always ends on a brief; with no open decision the brief still gets written.
   - An open decision is one the user would notice that neither request nor code settles.
   - Asked for options: list them, recommend one, no file.
   - New wishes for briefed work reopen that brief.
2. **Sort each point.**
   - Answerable by running or reading: record it, never ask.
   - Each open decision is a question, root decisions first.
   - A decision the user left open stays open whatever the code suggests.
   - A point the user would not notice goes in `Data:`.
   - Name the owning layer and a smaller alternative.
3. **Ask one at a time.**
   - Ask per `../route-skills/references/question.md`: decide nothing silently.
   - Close with up to three lines on what was agreed; brief after the user's yes.
   - After a compaction: list decisions first.
4. **Map, then locate.** Run `node "${CLAUDE_SKILL_DIR}/scripts/repo-map.mjs"` (plan mode too); read it; else `exo:locate-code`, at most eight ranges; never `cat`, `head` or `sed`.
5. **List tasks** per `references/task-list.md`; name a security-boundary task's reference in its heading or `Data:`; give each risk-category task `Risk:`. Plan mode: read-only commands; an edit-needing proof is the first task.
6. **Store it** per `specs` in `exo settings:`, else `docs` (plan mode: the harness plan file).
   `docs` → `docs/specs/<topic>.md`; `issues`/`both` → `references/brief-in-an-issue.md`; `issues` also writes the `node "${CLAUDE_SKILL_DIR}/../../lib/scratch-path.mjs" specs/<n>.md` path, for `build`.
7. **Check it.** Run `node "${CLAUDE_SKILL_DIR}/scripts/plan-check.mjs" --plan <brief file>`; fix flagged lines and any missing heading, `Data:`, Success criterion or `## Manual checks`.
8. **Hand off.** End on `node "${CLAUDE_SKILL_DIR}/../route-skills/scripts/next-stage.mjs" --after spec --artifact <brief path or #<n>>`'s output; on `C` reply with its `--fresh` output; never load `exo:build` unasked.
   - Past `exo: context`: keep the letters, hand on via a fresh delegate; stage- or workflow-invoked: ask nothing, return to it.

## References

| File | Read it when |
|---|---|
| `references/stored-brief.md` | The request names or extends a brief, issue or plan. |
| `../route-skills/references/question.md` | Step 3 and each reply. |
| `references/brief.md` | Before writing the brief. |
| `references/task-list.md` | Before writing the task list. |
| `references/example-plan.md` | Once, before the first task. |
| `../build/references/data-migration.md` | When its first line applies. |
| `../build/references/test-design.md` | When its first line applies. |
| `../build/references/security.md` | When its first line applies. |
| `references/brief-in-an-issue.md` | `specs` is `issues` or `both`. |
| `../file-issues/references/fields.md` | Before creating that issue. |
| `references/architecture-sketch.md` | Two or more structural shapes compete. |

Report: the brief's location and next stage, or the current question.
