---
name: agent-handoff-packager
description: Package agent context and state for handoff between agents or sessions. Use when transferring work between agents, saving checkpoint state, or preparing a compact summary for another agent to resume from.
---

# Agent Handoff Packager

## Overview

Packages the current agent's context, decisions, file changes, and open questions into a structured handoff artifact so another agent (or a future session) can resume seamlessly.

## Workflow

1. **Inventory** — List all files read, edited, or created during the current work.
2. **Summarize decisions** — Record what was decided, what was deferred, and why.
3. **Capture open questions** — Note blockers, ambiguities, or choices the next agent must make.
4. **Bundle artifacts** — Collect diffs, test results, and relevant snippets.
5. **Emit handoff document** — Produce a single Markdown artifact with all of the above.

## Handoff Document Structure

```markdown
# Handoff: <task summary>

## Status
- Current phase: <phase>
- Completion: <percentage or description>

## Context
- <key decisions and rationale>

## Files Touched
- <file path> — <what changed and why>

## Open Questions
- <question or blocker>

## Next Steps
- <concrete actions for the receiving agent>
```

## When to Use

- Handing work from a research agent to an implementation agent
- Saving state before a long-running task is interrupted
- Splitting a large task across multiple focused agents
- Resuming work in a new conversation session
