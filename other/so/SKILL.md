---
name: so
description: >-
  Simplifies the last message and explains it with minimal bullet points.
  Use only when the user invokes /so.
disable-model-invocation: true
---

# so

Simplify the last message and explain it with minimal bullet points.

## Which chat

1. If this conversation already has real work before `/so`, that is the chat. Use the current thread. Do not open transcripts.
2. If this conversation is only `/so` (or the same ask with no prior work), use the **most recent other chat**:
   - Find the newest `*.jsonl` for the app you are running in: `~/.cursor/projects/*/agent-transcripts/` in Cursor, `~/.claude/projects/*/` in Claude Code.
   - Skip the current conversation if you can identify it.
3. If the user names a chat, use that one instead.

## What to read

Only the last message. Do not read or summarize earlier turns.

- Last user message, plus the assistant reply after it if that reply is the latest thing in the chat.
- Skip tool traces.
- Ignore the rest of the conversation.

## Write

- Outcome first, not process.
- Decisions, changes, and leftovers from that last message only.
- No preamble, no heading, no recap of the recap.
- No tool names, file dumps, or play-by-play.

## Shape

3–6 bullets. Never more than 7.

```
- what the last message was doing (1 line)
- what changed or was decided
- what is still open (omit if nothing)
```

Drop any of those lines if they add nothing.

## Example

```
- First skill is /so: recap the last message in a few bullets
- Next: commit, push, clone into ~/.cursor/plugins/local
```
