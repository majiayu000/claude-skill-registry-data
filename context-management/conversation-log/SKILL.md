---
name: evi-conversation-log
description: Use when channel conversations must survive session death and /compact — SessionEnd + PreCompact hooks flush raw messages to disk before they are lost.
---

# Conversation log

Channel messages are written to disk by the harness, not by the model. The model
cannot save memory at session-end (it is no longer running) or after `/compact`
(the content is already gone), so two hooks capture the raw conversation
deterministically before either event destroys it.

## What it guarantees

Every inbound/outbound channel message lands in an append-only raw layer
(`memory/conversations/YYYY-MM-DD.jsonl`) before the session is garbage-collected,
and everything since the last compact marker is captured into the daily log
before `/compact` compresses the context away. Raw data never dies; summaries
can be rebuilt from it later.

## How it works

- **SessionEnd → `session-end-flush.py`** runs `extract-conversations.py --today`,
  which scans the transcript JSONL for inbound `<channel>` messages and outbound
  `__reply` tool calls and appends them as structured JSONL
  (`{ts, dir, who, text, message_id}`), deduplicated on message id / text.
- **PreCompact → `pre-compact-flush.py`** finds the last `isCompactSummary`
  entry in the transcript and appends every user/assistant message after it to
  `memory/daily/YYYY-MM-DD.md` as a verbatim "Compact Extraction" section. No
  LLM summarization — just cheap, deterministic capture.

## Implement in your project

Reference implementations:
- [`../../scripts/hooks/session-end-flush.py`](../../scripts/hooks/session-end-flush.py)
- [`../../scripts/hooks/pre-compact-flush.py`](../../scripts/hooks/pre-compact-flush.py)
- [`../../scripts/extract-conversations.py`](../../scripts/extract-conversations.py)

Wire both events (see
[`../../.claude/settings.json`](../../.claude/settings.json)):

```json
"SessionEnd": [
  { "matcher": "", "hooks": [
    { "type": "command", "command": "EVI_PROJECT_DIR=$CLAUDE_PROJECT_DIR python3 $CLAUDE_PROJECT_DIR/scripts/hooks/session-end-flush.py", "timeout": 90 }
  ]}
],
"PreCompact": [
  { "matcher": "", "hooks": [
    { "type": "command", "command": "EVI_PROJECT_DIR=$CLAUDE_PROJECT_DIR CLAUDE_PROJECT_DIR=$CLAUDE_PROJECT_DIR python3 $CLAUDE_PROJECT_DIR/scripts/hooks/pre-compact-flush.py" }
  ]}
]
```

`extract-conversations.py` is configured via env (`EVI_CHANNEL_SOURCE`,
`EVI_REPLY_TOOL_SUFFIX`, `EVI_AGENT_NAME`, `EVI_OWNER_NAME`, `EVI_TZ`,
`EVI_TRANSCRIPT_DIRS`) — see [`../../.env.example`](../../.env.example).

## Adaptation points

- **Different channel:** set `EVI_CHANNEL_SOURCE` to your channel keyword and
  `EVI_REPLY_TOOL_SUFFIX` to your reply tool's name suffix; the extractor's regex
  adapts from those env values.
- **Different transcript location:** point `EVI_TRANSCRIPT_DIRS` at your
  harness's session log directory (colon-separated). Default scans all
  `~/.claude/projects/` subdirs.
- **No PreCompact event in your harness:** keep SessionEnd alone — you lose
  mid-session compaction capture but still get end-of-session flush.

**Unconfigured = silent no-op.** Both hooks return immediately when there is no
`.env` in the project dir, so a fresh clone never scans a transcript or writes to
`memory/`. The behavior switches on once you create your `.env`.

## Verify

1. `python3 -m py_compile scripts/hooks/session-end-flush.py scripts/hooks/pre-compact-flush.py scripts/extract-conversations.py` exits 0.
2. `echo '{}' | python3 scripts/hooks/session-end-flush.py` and the same for
   pre-compact-flush exit 0 (no transcript → graceful skip).
3. End a real session → a file appears/grows in `memory/conversations/`.

## Rollback

Remove the `SessionEnd` and `PreCompact` entries from `.claude/settings.json`.
