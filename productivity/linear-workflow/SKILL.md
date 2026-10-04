---
name: linear-workflow
description: Link the current session to a Linear issue and keep it updated using the connected Linear MCP tools (no custom scripts, no API key file). Use when the user wants to track work on a Linear issue, a linear-*-nudge hook fires, or the user explicitly asks to sync/save a just-finished task's results to Linear (e.g. "lưu vào Linear", "cập nhật Linear", "chốt lên Linear").
---

# Linear Workflow (MCP-based)

This project has no `bun scripts/linear/*.ts` layer (unlike the reference
project this template was cloned from) — it relies entirely on whatever
Linear MCP server/tools are connected to this Claude Code session. Check
what's actually available before assuming a tool name below exists;
tool names depend on which MCP connector is configured.

## Link a session to an issue

1. Confirm the issue exists: call the MCP tool that reads a single issue
   (e.g. `get_issue`) with the identifier the user gave you.
2. Write the identifier to `.claude/.linear-link` (plain text, just the
   ID, e.g. `ENG-123`).
3. Call `list_comments` for that issue and read them — don't rely on the
   description alone.

## Unlink

Delete `.claude/.linear-link`.

## Before acting on a linked issue

Always re-fetch first if it's been more than a few turns since you last
read it — comments/state may have changed:

```
get_issue(identifier)
list_comments(identifier)
```

## Posting an update

Use the MCP comment tool (e.g. `save_comment`) with the issue identifier
and a concise message. Don't paste raw file diffs — summarize.

## Transitioning state / editing fields

Use the MCP issue-write tool (e.g. `save_issue`) with the identifier and
the field(s) to change. **First** call `list_teams` / `get_project` (or
open the issue in Linear) to learn your team's actual workflow state
names — don't assume they match the reference project's
(Backlog/Todo/In Progress/In Review/Blocked/Done).

## Responding to a nudge hook

When a `linear-*-nudge.sh` hook prints a reminder (you'll see it as
stderr/stdout in the tool result, not as a separate message from the
user):

1. Check `.claude/.linear-link` — if empty/absent, the nudge doesn't
   apply, do nothing.
2. If linked, perform the suggested MCP call (comment or state update)
   right away, in the same turn — don't defer it, since there's no
   second automatic trigger to catch a missed one.

## Creating a new issue

If no issue exists yet and the user wants one tracked, use the MCP
issue-create tool with a clear title + description. Ask the user which
Project/team it belongs to if that's not obvious — don't guess.

## Wrapping up a task (explicit sync command)

Only trigger this when the user explicitly asks to sync the finished task to
Linear (e.g. "lưu vào Linear", "cập nhật Linear", "chốt lên Linear", "tạo
issue cho task này"). A generic completion phrase alone ("xong rồi", "done")
is NOT enough — per `.claude/rules/linear.md`, a Linear ref stays optional,
and auto-creating an issue for every finished task would spam the tracker.

1. Verify the workspace (see `.claude/rules/linear.md`) if not already
   verified this session — this is a write action.
2. Check `.claude/.linear-link`:
   - **Not linked (no pre-existing issue):**
     a. Create the issue — see "Creating a new issue" above for
        title/description/Project selection.
     b. Immediately post one follow-up comment structured as:
        ```
        ## Kết quả
        - <what was done/changed — links to files/PR if relevant>

        ## Kinh nghiệm
        - <decisions made and why, gotchas hit, what to remember next
          time this area is touched>
        ```
     c. Write the new issue identifier into `.claude/.linear-link` so the
        session stays linked going forward.
     d. Report the issue identifier/URL back to the user.
   - **Already linked (issue was written by the user beforehand):**
     a. Re-fetch per "Before acting on a linked issue" above if it's been a
        while since you last read it.
     b. Post exactly one comment using the same `Kết quả` / `Kinh nghiệm`
        template. Do not create a duplicate issue.
     c. Don't change issue state here — `gh pr merge` already nudges a
        state transition (see the lifecycle table in
        `.claude/rules/linear.md`); keep this step content-only so the two
        flows don't fight over the same field.

## Growing this beyond MCP

If you eventually want script-enforced behavior (PII scanning before
posting, mandatory label taxonomy, dedup on repeated uploads, branch-name
convention tied to issue ID) — that's exactly what the reference project's
`scripts/linear/*.ts` did. Port that logic once you've picked a runtime for
this project and decided it's worth the engineering cost; don't build it
speculatively.
