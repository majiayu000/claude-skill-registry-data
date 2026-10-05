---
name: brief
description: Generates a morning briefing — what ran overnight, what it cost, what to do next
when_to_use: "morning briefing, what happened overnight, overnight activity, daily brief — read-only report; NOT for launching autonomous runs (use /start)"
argument-hint: '[--all]'
user_invocable: true
---

# Brief Skill

Generates a morning briefing: what ran overnight, what it cost, what to do next.

## When to use

Run at the start of a session to catch up on overnight/unattended work.

## Usage

/brief                   # Full briefing for current project
/brief --all             # Briefing across all registered sessions (if orchestrator running)

## Queue Status needs a token

The orchestrator's control plane rejects every unauthenticated request with a
`401` whose body is still valid JSON, so the queue probe reads `api_token` from
`~/.claude/orchestrator-settings.json` and branches on the HTTP status. Without
that token the briefing says so explicitly rather than reporting the queue as
offline or inventing counts. See `docs/configuration.md`, "Control-plane
authentication".
