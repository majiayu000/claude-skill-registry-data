---
name: handoff
description: Use when preparing another person or agent to continue work.
---

# Handoff

Produce a handoff with objective, current branch/work reference, verified state, remaining risks, next action, and authoritative links. Reference the specification role for formal requirements, tracker for state, and repository for decisions. Preserve uncertainties. Ask services to store/link only when requested; omit credentials and personal notes irrelevant to the recipient.

Resolve provider-specific commands from the configured role provider’s instructions. The agent supplies judgment; services store, validate, and link artifacts.

When a selected session lesson should persist, use `learnings/<YYYY-MM-DD>-<work-id>.md`
with the sections `## What happened`, `## What to do differently`, and `## Links`.
Keep it short and link source evidence. Frontmatter follows the knowledge-note schema
(`id`, `kind: learning`, `scope`, `label`, `sources` with `uri` and `hash`, `author`,
`confidence`, `valid_from`, `valid_to`, `review_by`, `supersedes`); omit it to let
`work finish` generate it from the merged PR, or supply only the fields you know, such
as `confidence`. Never widen `scope` beyond `personal` for someone else. Set
`AI_DLC_AUTHOR` to `agent:<client>@<plugin digest>` when an agent records the lesson.
The format is documented in ai-dlc's `docs/design/local-and-shared-knowledge.md`.
When the repository is adopted (has `ai-dlc.toml` at its root) and `ai-dlc` is on PATH, pass the authored file to `ai-dlc work finish <id> --learning FILE` (MCP
`work_finish` accepts `learning` text), or use the knowledge provider's `note`
operation with a stable operation ID. A pending learning does not undo verified
completion; retry the same body instead of duplicating it. Never copy raw logs.


When the repository is adopted (has `ai-dlc.toml` at its root) and `ai-dlc` is on PATH, for delivery use `ai-dlc work start <id>` and, after checks and an explicit branch push, `ai-dlc work pr <id>`. Start and link commit only the work record by default (`--no-commit` opts out). Push the PR-link commit before review. Include the linked PR URL; repeated PR creation returns that link. Report an uncertain creation and recover by inspecting the SCM and linking its existing PR.
