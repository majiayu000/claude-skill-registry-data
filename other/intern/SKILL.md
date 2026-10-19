---
name: intern
description: >-
  Explains the same thing as the last chat, as you do for intern. Use only
  when the user invokes /intern.
disable-model-invocation: true
---

# intern

explain this as you do for intern

## Which chat

1. If this conversation already has real work before `/intern`, that is the source. Use the current thread. Do not open transcripts.
2. If this conversation is only `/intern`, use the **most recent other chat**:
   - Find the newest `*.jsonl` for the app you are running in: `~/.cursor/projects/*/agent-transcripts/` in Cursor, `~/.claude/projects/*/` in Claude Code.
   - Skip the current conversation if you can identify it.
   - Read user turns and the assistant's actual explanation. Skip tool traces.
3. If the user names a chat, use that one instead.

## Write

- Same topic as the source. Do not add new analysis, options, or next steps.
- Assume a smart intern who is new to this codebase and domain.
- Start with the point. Then walk the why, the pieces, and how they connect.
- Define jargon the first time. Keep file paths, names, and code as-is.
- No preamble ("as if you were an intern").
