---
name: jira-workflow
description: Link the current session to a Jira issue and keep it updated using the connected Atlassian Rovo MCP tools (no custom scripts, no API key file). Use when the user wants to track work on a Jira issue/story, mentions SAFe backlog sync, or explicitly asks to sync/save a finished task or a PO Requirement Refinement Final Backlog to Jira (e.g. "sync backlog này lên Jira", "tạo Jira issue cho cái này").
---

# Jira Workflow (Atlassian Rovo MCP-based)

This project has no custom Jira scripting layer — it relies entirely on
whatever Atlassian Rovo MCP tools are connected to the session. Tool names
are not hardcoded here because they haven't been verified against a live
connection yet (see `.claude/rules/jira.md`); check what's actually
available (list the session's tools) before assuming a specific tool name
exists.

## First-time setup in a session

1. Confirm the Rovo MCP tools are connected — if not, follow
   `.claude/rules/jira.md`'s connection section (Cowork connector or
   `.mcp.json` + `/mcp` for CLI).
2. Call the accessible-resources/site-listing tool to find which
   Atlassian site(s)/project(s) the connected account can see. If more
   than one site or project is accessible, ask the PO which one this
   session's work belongs to — don't guess.

## Link a session to an issue

1. Confirm the issue exists: call the MCP tool that reads a single Jira
   issue by key.
2. Write the issue key to `.claude/.jira-link` (plain text, e.g.
   `SAFE-123`).
3. Read existing comments on the issue before acting — don't rely on the
   description alone.

## Unlink

Delete `.claude/.jira-link`.

## Before acting on a linked issue

Re-fetch the issue (and its comments) if it's been more than a few turns
since you last read it — status/comments may have changed underneath you.

## Posting an update

Use the MCP comment-write tool with the issue key and a concise message.
Summarize — don't paste raw file diffs or full requirement documents into
a comment.

## Transitioning state / editing fields

First confirm the project's actual workflow state names and issue type
scheme (Epic/Feature/Story/Task/Sub-task, or whatever SAFe scheme this
org's Jira site actually uses) — do not assume a specific set of states.
Then use the MCP issue-write tool with the key and the field(s) to change.

## Syncing a PO Requirement Refinement Final Backlog to Jira

Only trigger this on an explicit request (e.g. "sync backlog này lên
Jira", "tạo Jira issue cho backlog này") — the `po-requirement-refinement`
skill's output is chat/artifact content by default, not auto-pushed
anywhere.

1. Confirm site/project per "First-time setup" above if not already done
   this session.
2. Map the Final Backlog's structure to Jira issues — a reasonable default
   is one Epic (top-level `# Epic`) with one child issue per backlog item
   under Frontend/Backend/Integration-Data/QA, but **ask the PO to confirm
   this mapping** (especially the issue type to use for each) rather than
   assuming it matches this org's actual SAFe scheme, since that scheme
   hasn't been verified (see `.claude/rules/jira.md`).
3. Create the Epic issue first, then each backlog item linked/nested under
   it per whatever hierarchy the Jira site actually supports.
4. Report back the created issue keys/URLs to the user — don't just say
   "done."

## Growing this beyond MCP

If this eventually needs script-enforced behavior (a fixed backlog→Jira
mapping, bulk import, PI/sprint assignment automation) — port that logic
once the actual site's scheme is confirmed and the mapping has been used
successfully a few times manually. Don't build it speculatively before
that.
