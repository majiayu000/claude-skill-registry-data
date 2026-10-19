---
name: restate
description: >-
  Restates the last user message in the agent's own words so the user can
  confirm understanding. Use only when the user invokes /restate.
disable-model-invocation: true
---

# restate

restate to me what I just said in your own words so I know you understood me

## Which chat

1. If this conversation already has real work before `/restate`, that is the source. Use the current thread. Do not open transcripts.
2. If this conversation is only `/restate`, use the **most recent other chat**:
   - Find the newest `*.jsonl` for the app you are running in: `~/.cursor/projects/*/agent-transcripts/` in Cursor, `~/.claude/projects/*/` in Claude Code.
   - Skip the current conversation if you can identify it.
3. If the user names a chat, use that one instead.

## What to read

Only the last user message. Do not read or summarize earlier turns.

- Skip the `/restate` invocation itself.
- Skip tool traces.
- Ignore the rest of the conversation.

## Write

- Paraphrase that last user message in your own words.
- Same meaning. Do not add analysis, options, or next steps.
- Do not start doing the work they asked for.
- No preamble, no heading, no bullets unless their message was a list.
