---
name: handoff
description: Compact the current conversation into a handoff brief on the mcp-brief server for another session (Claude web or Claude Code) to pick up.
argument-hint: "(optional) what the next session will focus on"
disable-model-invocation: true
allowed-tools: mcp__brief-local__get_brief, mcp__brief-local__list_briefs, mcp__brief-local__send_brief, mcp__brief-local__edit_brief, mcp__brief-local__complete_brief
model: claude-sonnet-5
---
Compact the current conversation into a handoff brief and submit it to the mcp-brief MCP server so a fresh session can continue the work.

The brief-mcp server is local, so `/handoff` → `/clear` → `/resume` is also the
same-machine session-continuation path — nothing about it requires a second device.
With no argument, treat this as a quick local checkpoint: capture tight, skip the
ceremony.

A brief is a living document holding the **current** state, not an append log. If a
brief for this thread already exists (`list_briefs` / `get_brief`), overwrite it with
`edit_brief` to reflect where things stand now. Only `send_brief` a new one when the
thread has none.

Capture what a fresh agent needs to continue, not a transcript:
- The goal, and where things currently stand.
- Decisions made and why (so they aren't relitigated).
- What's in flight or blocked, and the immediate next step.
- Open questions and known landmines.
- A "suggested skills" section — skills the next agent should invoke, only ones that exist in this setup.

Don't duplicate content already in other artifacts (specs, plans, ADRs, issues, commits, diffs) — reference them by path or URL.
Redact secrets and PII (API keys, passwords, tokens).
If arguments were passed, treat them as the next session's focus and tailor accordingly.
Report the brief's ID or reference once submitted, so it can be found from the other side.

Before compacting, consider invoking `/notice` to capture any friction or corrections
from this session — skip it for a quick no-arg checkpoint.
Once the brief is submitted, tell the user to run `/clear` — you can't run it yourself.