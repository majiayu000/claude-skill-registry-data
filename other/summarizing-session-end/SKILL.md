---
name: summarizing-session-end
description: Auto-generates a session summary on SessionEnd. Writes structured notes to ~/.claude/session-summaries/ for use by bigpicture synthesis.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Glob
  context: inline
  stability: development
---

# Session End Summary

Generates a structured session summary when triggered by the SessionEnd hook.
Reuses the compacting-context template to produce consistent, synthesis-ready
notes.

## Hook Configuration

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "type": "prompt",
        "prompt": "/summarizing-session-end"
      }
    ]
  }
}
```

## Workflow

1. **Gather context** -- Review the conversation for what was accomplished,
   which files were touched, and any unresolved issues.

2. **Generate session ID** -- Use the current date and a short identifier
   (first 8 chars of session UUID if available, or timestamp).

3. **Write summary** -- Create `~/.claude/session-summaries/YYYY-MM-DD-<id>.md`
   using the output template below. Create the directory if it does not exist.

4. **Keep it brief** -- The summary must be under 50 lines. This is a summary,
   not a transcript.

## Output Template

Write to `~/.claude/session-summaries/YYYY-MM-DD-<id>.md`:

```markdown
# Session Summary -- YYYY-MM-DD

## Trajectory
<!-- Phase reached: research / planning / implementation / review -->
<!-- One-line description of the session arc -->

## Key Files
<!-- Files touched with one-line purpose each -->

## Completed
<!-- Done items, one bullet per item -->

## Blockers
<!-- Blocking issues discovered (empty section if none) -->

## Findings
<!-- Key discoveries, decisions made, learnings -->
```

## Quality Check

- Correct > Complete > Minimal (ACE-FCA)
- Under 50 lines output
- No raw logs or tool dumps
- Enough for bigpicture synthesis to consume
