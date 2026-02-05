---
name: session-continuity
description: Aggressive session accountability via Obsidian timeline. PROACTIVELY log decisions, commits, ideas, and blockers AS THEY HAPPEN. Triggers on any significant action.
---

# Session Continuity

Maintain context across Claude Code sessions using aggressive, real-time logging.

## Core Principle: Log Early, Log Often

**Don't wait for session end.** Log as things happen:

- Made a decision? Log it immediately.
- Committed code? Log the commit.
- Hit a blocker? Log it before context is lost.
- Had an insight? Capture it now.

**You are accountable for maintaining context.** The user may forget, the session may crash, context may compact. The timeline is the source of truth.

## Environment

| Variable | Required | Description |
|----------|----------|-------------|
| `CLAUDE_TIMELINE_PATH` | Yes | Path to timeline file |

## When to Log

Log **immediately** after any of these:

| Trigger | Format |
|---------|--------|
| Decision | `- HH:MM **Decision**: Using X because Y` |
| Commit | `- HH:MM **Commit**: message (abc123)` |
| Blocker | `- HH:MM **Blocker**: description` |
| Resolved | `- HH:MM **Resolved**: how it was fixed` |
| Idea | `- HH:MM **Idea**: insight or suggestion` |
| State | `- HH:MM **State**: service on port, config changed` |

**Be aggressive.** When in doubt, log it.

## Session Start

1. Read timeline from `$CLAUDE_TIMELINE_PATH`
2. **Check Inbox first** - this is how user communicates async
3. Acknowledge: "Timeline loaded. Inbox: [N items]. Last entry: [date]."

## Inbox Protocol

The Inbox is for async capture from any device (phone, tablet, mobile Obsidian).

```markdown
## Inbox

> Async capture from any device. Claude reviews at session start.

- [ ] Add Sonarr to Traefik routes
- [ ] Look into why n8n keeps disconnecting
```

**At session start:**
1. Check Inbox for items
2. Acknowledge what's there
3. Ask if user wants to address them now
4. When addressed: work on it, log the work, remove from Inbox

## Timeline Format

```markdown
# Claude Code Timeline

## Inbox

> Async capture from any device. Claude reviews at session start.

## Work Log

### 2025-12-19

- 23:15 **Decision**: Using Traefik - better Docker integration
- 23:30 **Commit**: feat: add prometheus (abc123)
- 23:45 **Blocker**: OAuth not redirecting
- 00:10 **Resolved**: OAuth needed explicit redirect_uri
```

## MCP vs Filesystem

**Prefer MCP** if `obsidian-mcp-server` is available:
- Read: `mcp__obsidian-mcp-server__obsidian_read_note`
- Write: `mcp__obsidian-mcp-server__obsidian_update_note` or `obsidian_search_replace`

**Fallback** to native Read/Edit tools.
