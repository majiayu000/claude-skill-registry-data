---
name: day-end
description: Use when wrapping up a work day or recording progress for later.
---

# Day End

Return outcomes supported by checks, unfinished work, blockers, and next actions with links. Keep architecture, decisions, and operational guidance in repository documents. Personal reflections belong to the knowledge role. Use the work service for requested persistence and completion; a summary never substitutes for completion gates.

Resolve provider-specific commands from the configured role provider’s instructions. The agent supplies judgment; services store, validate, and link artifacts.

Capture selected learning or unresolved questions with project/source links and applicability, using the linked workspace templates when available. Keep observations distinct from reviewed rules; never automatically copy every work log into the vault or promote a private note to company guidance.

When a selected session lesson should persist, use `learnings/<YYYY-MM-DD>-<work-id>.md`
with the sections `## What happened`, `## What to do differently`, and `## Links`.
Keep it short and link source evidence. Frontmatter follows the knowledge-note schema
(`id`, `kind: learning`, `scope`, `label`, `sources` with `uri` and `hash`, `author`,
`confidence`, `valid_from`, `valid_to`, `review_by`, `supersedes`); omit it to let
`work finish` generate it from the merged PR, or supply only the fields you know, such
as `confidence`. Never widen `scope` beyond `personal` for someone else. Set
`AI_DLC_AUTHOR` to `agent:<client>@<plugin digest>` when an agent records the lesson.
The format is documented in ai-dlc's `docs/design/local-and-shared-knowledge.md`.
Pass the authored file to `ai-dlc work finish <id> --learning FILE` (MCP
`work_finish` accepts `learning` text), or use the knowledge provider's `note`
operation with a stable operation ID. A pending learning does not undo verified
completion; retry the same body instead of duplicating it. Never copy raw logs.
