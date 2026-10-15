---
name: evi-reply-guard
description: Use when an agent must never end its turn while an inbound chat message is still unanswered — a Stop hook that blocks turn-end until a reply is sent.
---

# Reply guard

A Stop hook that refuses to let the agent finish a turn while a message from
your chat channel has no reply yet. "Always answer on the channel you were
contacted on" stops being a prose rule the model can skim and becomes a
mechanical gate.

## What it guarantees

The agent cannot silently end a turn after the owner messaged it. Writing the
answer into the session transcript is not delivery — only a reply through the
channel's reply tool reaches the owner, and this hook holds the turn open until
that reply (or an MCP self-poke recovery) has happened.

## How it works

On every Stop event the hook walks the session transcript JSONL and finds two
line numbers: the last inbound `<channel source="...">` message and the last
outbound reply action (a `__reply` / `__edit_message` tool call, or a Bash
`send-keys '/mcp'` reconnect poke). If the last inbound is newer than the last
reply, it emits `{"decision":"block","reason":...}` instructing the model to
send the reply first. `stop_hook_active=true` (already blocked once this turn)
passes through so the turn can never deadlock.

## Implement in your project

Reference implementation: [`../../scripts/hooks/reply-guard.py`](../../scripts/hooks/reply-guard.py)

Wire it on the `Stop` event (see
[`../../.claude/settings.json`](../../.claude/settings.json)):

```json
"Stop": [
  {
    "matcher": "",
    "hooks": [
      {
        "type": "command",
        "command": "EVI_CHANNEL_CHAT_ID=$EVI_CHANNEL_CHAT_ID EVI_TMUX_TARGET=$EVI_TMUX_TARGET EVI_TMUX_BIN=$EVI_TMUX_BIN python3 $CLAUDE_PROJECT_DIR/scripts/hooks/reply-guard.py",
        "timeout": 30
      }
    ]
  }
]
```

`EVI_CHANNEL_CHAT_ID`, `EVI_TMUX_TARGET`, `EVI_TMUX_BIN` only feed the
instructional reason string; the block decision works without them.

## Adaptation points

- **Different channel:** keep the two-marker logic (detect inbound tag → look
  for an outbound reply tool call → compare order); change `REPLY_TOOLS` to your
  channel's reply tool name suffix and the inbound detector to your channel's
  tag.
- **No tmux:** the `send-keys '/mcp'` reconnect hint in the reason is optional.
  Drop `EVI_TMUX_*` and the recovery sentence; the gate still functions.
- **Inbound detection:** the hook matches `<channel ... source=...>`. If your
  harness frames inbound messages differently, adjust `is_channel_inbound`.

## Verify

1. `python3 -m py_compile scripts/hooks/reply-guard.py` exits 0.
2. Send a test message, then try to end the turn without replying → the turn is
   blocked with the reply instruction.
3. Reply, then end the turn → it ends normally (last reply is newer than last
   inbound).

## Rollback

Remove the `Stop` entry from `.claude/settings.json`.
