---
name: japa
description: >-
  Explains the same thing as the last chat, in Japanese. Use only when the
  user invokes /japa.
disable-model-invocation: true
---

# japa

Explain the same thing in Japanese.

Not a recap of what the chat did. Take the explanation, answer, or conclusion from that chat and write that same content in Japanese.

## Which chat

1. If this conversation already has real work before `/japa`, that is the source. Use the current thread. Do not open transcripts.
2. If this conversation is only `/japa`, use the **most recent other chat**:
   - Find the newest `*.jsonl` for the app you are running in: `~/.cursor/projects/*/agent-transcripts/` in Cursor, `~/.claude/projects/*/` in Claude Code.
   - Skip the current conversation if you can identify it.
   - Read user turns and the assistant's actual explanation. Skip tool traces.
3. If the user names a chat, use that one instead.

## Write

- All output in Japanese. Keep proper nouns, file paths, skill names, and code as-is.
- Same meaning, same level of detail as the source explanation.
- Do not shorten it into a work-log, status update, or `/so`-style bullets.
- Do not add new analysis, options, or next steps that were not in the source.
- No preamble ("以下、日本語で説明します").
