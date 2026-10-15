---
name: evi-auto-react
description: Use when every inbound chat message must be acknowledged instantly and model-independently — a two-stage read-receipt (hook fixed emoji now, model contextual emoji later).
---

# Auto-react

Every inbound message gets an acknowledgment that does not depend on the model
remembering to react. The acknowledgment is **two-stage**: the harness
guarantees instant receipt, the model later upgrades it to something that fits
the message.

## What it guarantees

The owner always sees that the message landed — within milliseconds, before the
model even starts a turn — and, by the end of the turn, sees a reaction that
actually reflects the content. Instant receipt is a harness promise; contextual
nuance is a model touch. Neither blocks the other.

## How it works

**Stage 1 — instant fixed (hook).** A `UserPromptSubmit` hook extracts
`chat_id`/`message_id` from the `<channel source="...">` tag and fires a
fire-and-forget `setMessageReaction` with a fixed emoji (👀). It runs before the
model's turn, so the receipt is model-independent: it lands even when context is
full or the model is mid-task. Failure is swallowed — a missing reaction must
never delay the turn.

**Stage 2 — model upgrade.** When the model processes the turn and understands
the message, it overwrites the placeholder with a contextually right emoji
(e.g. 🎉 for good news, 🔧 for a bug report) via the channel's react tool. The
fixed 👀 is the floor; the model's choice is the finish.

Role split: **immediacy is the hook, judgment is the model.** The hook can react
instantly but cannot know what the message means; the model knows what it means
but cannot be trusted to react every single time. Stacking them gives both.

## Implement in your project

Reference implementation: [`../../scripts/hooks/auto-react.sh`](../../scripts/hooks/auto-react.sh)

Wire it on `UserPromptSubmit` (see
[`../../.claude/settings.json`](../../.claude/settings.json)):

```json
"UserPromptSubmit": [
  {
    "matcher": "",
    "hooks": [
      { "type": "command", "command": "bash $CLAUDE_PROJECT_DIR/scripts/hooks/auto-react.sh", "timeout": 10 }
    ]
  }
]
```

For stage 2, add a line to your agent instructions: "after understanding an
inbound message, replace the 👀 placeholder with an emoji that fits, using the
channel react tool." No code needed — it is a model behavior, the hook is the
safety net under it.

The bot token is read from the channel plugin's own `.env`
(`$HOME/.claude/channels/telegram/.env`), never from the project `.env` and
never into model context.

## Adaptation points

- **Different channel:** replace the regex that pulls `chat_id`/`message_id` and
  the `curl` call with your channel's reaction API. Keep the two stages.
- **No reaction API on your channel:** stage 1 can post a lightweight ack
  instead; if even that is impossible, drop stage 1 and keep stage 2 only — but
  you lose the model-independent guarantee.
- **Different placeholder:** change the fixed emoji in the `curl` body; keep it
  distinct so stage 2 can tell "not yet upgraded" from "already contextual".

## Verify

1. `bash -n scripts/hooks/auto-react.sh` exits 0.
2. Send a test message → 👀 appears within a second (stage 1).
3. Let the model finish the turn → the reaction changes to a content-fit emoji
   (stage 2).

## Rollback

Remove the `UserPromptSubmit` entry from `.claude/settings.json`.
