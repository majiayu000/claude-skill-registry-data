---
name: tg-rich-streaming
description: "Use when streaming LLM or AI-generated replies to Telegram in real time (ChatGPT-style progressive output in a bot), showing a model thinking indicator, or delivering token-by-token text as an animated rich message draft that finalizes into a permanent message."
license: MIT
---

# tg-rich-streaming

Stream AI-generated text into a Telegram private chat with native draft animation and a "thinking" indicator — the same UX as ChatGPT or Claude, directly inside the bot.

Sending requires network access to `api.telegram.org` and `TELEGRAM_BOT_TOKEN`.
Checked against the official docs on 2026-10-30: Bot API 10.3 (latest, August 24, 2026). Nothing here was run against a live bot.

| Method | Content | Since | Finalize with |
|---|---|---|---|
| `sendMessageDraft` | plain `text` 0–4096, `parse_mode` or `entities`; empty `text` shows a "Thinking…" placeholder | 9.3, all bots since 9.5 | `sendMessage` |
| `sendRichMessageDraft` | `InputRichMessage`, including `<tg-thinking>` | 10.1 | `sendRichMessage` |

Both work only with a private integer `chat_id`. Both take `draft_id`, `message_thread_id`,
`can_stop` and `keep_on_stop`, and both drafts live 30 seconds. Bot API 10.2 also permits direct
`InputRichMessage.blocks`; the draft lifecycle below is unchanged. A rich draft can't upload new
files or upload by URL, so media in a draft must already have a `file_id`.

## Core pattern

Four mandatory steps. Skip step 3 and the draft disappears after ~30 seconds.

### Step 1 — open draft with Thinking block

Send the first `sendRichMessageDraft` immediately after the LLM call starts.
`draft_id` is any non-zero integer you generate once per response; keep it for all updates.
`RichBlockThinking` signals the model is working.

```
POST /sendRichMessageDraft
{
  "chat_id": <integer>,          // private chat only — no @username
  "draft_id": 42,
  "rich_message": {
    "markdown": "<tg-thinking>Thinking…</tg-thinking>"
  }
}
```

> Rich HTML tags (like `<tg-thinking>`) are valid pass-through inside the `markdown` field — spec explicitly allows HTML tags in Rich Markdown.

> `RichBlockThinking` is **only** valid in `sendRichMessageDraft`. It is never stored in a `Message`.

### Step 2 — update draft as tokens arrive

Call `sendRichMessageDraft` again with the **same `draft_id`** each time you have enough new text. The client animates the transition.

**Throttle**: send at most once every 1–2 seconds. The draft is ephemeral (~30 s window) — keep sending updates or move to step 3 before the window closes.

Drop the Thinking block from the first update that contains real content.

```
# pseudocode — generic async LLM stream

draft_id = generate_nonzero_id()
accumulated = ""
last_sent = 0

send_draft(chat_id, draft_id, thinking_markdown())   # step 1

for chunk in llm.stream(prompt):
    accumulated += chunk.text
    now = time.monotonic()
    if now - last_sent >= 1.5:                        # throttle
        send_draft(chat_id, draft_id, accumulated)
        last_sent = now

finalize(chat_id, accumulated)                        # step 3 — mandatory
```

### Step 3 — finalize with sendRichMessage (mandatory)

After the LLM stream ends, call `sendRichMessage`. This creates the **permanent** message. If you skip this, the draft vanishes.

```
POST /sendRichMessage
{
  "chat_id": <integer>,
  "rich_message": {
    "markdown": "<full generated text>"
  }
}
```

### Step 4 — edits after finalization

Use `editMessageText` with the `rich_message` parameter to update the permanent message later (corrections, appended content, etc.).

```
POST /editMessageText
{
  "chat_id": <integer>,
  "message_id": <id from step 3 response>,
  "rich_message": {
    "markdown": "<revised text>"
  }
}
```

> `text` and `rich_message` are mutually exclusive in `editMessageText` — use exactly one.

> An edit through `rich_message` can drop custom emoji while returning `ok: true`: [tdlib #865](https://github.com/tdlib/telegram-bot-api/issues/865) (open, status checked 2026-10-30). Finalization through `sendRichMessage` isn't affected; this step and the group fallback are.

---

## Stop button (10.3)

Pass `can_stop: true` on every draft call to show a button that stops further drafts. When the
user presses it, the bot receives the `stopped_message_generation` update
(`MessageGenerationStopped`: `chat`, `message_thread_id`, `draft_id`).

1. Add `stopped_message_generation` to `allowed_updates`, if the bot sets that list.
2. Match the update to the running stream by `chat.id`, `message_thread_id` and `draft_id`.
3. Cancel the model call and stop sending drafts.
4. To keep the partial text, pass `keep_on_stop: true` on the draft calls and send the text as a
   new message. `keep_on_stop` alone isn't persistence: the draft still disappears after a short
   time or when the bot sends a message.

```
POST /sendMessageDraft
{
  "chat_id": <integer>,
  "draft_id": 42,
  "text": "Partial answer so far",
  "can_stop": true,
  "keep_on_stop": true
}
```

---

## Topics in private chats

`message_thread_id` targets a topic when the bot has forum topic mode enabled in private chats.
`getMe` reports it in `has_topics_enabled`. Check two things before you turn it on:

- **Money.** Under the [Bot Developer Terms](https://telegram.org/tos/bot-developers), §6.2.6, all
  Telegram Stars purchases in a bot with topics in private chats enabled carry a non-refundable
  15% fee, withheld by Telegram while the option stays on. A bot that sells for Stars pays it on
  every purchase.
- **Dead topics.** `createForumTopic` can succeed while the new topic answers
  "message thread not found" to every bot write and `TOPIC_ID_INVALID` to `deleteForumTopic`:
  [tdlib #905](https://github.com/tdlib/telegram-bot-api/issues/905) (practitioner report, filed
  2026-09-29, open on 2026-10-30, three episodes across several hundred topics). Handle the failed first write
  and create a replacement topic.

Whether streaming needs topics, the sources disagree. Terms §6.2.6 still ties "the streaming of
message drafts" to topics in private chats and the 15% fee; the
[Bot API 9.5 changelog](https://core.telegram.org/bots/api-changelog) allowed all bots to use
`sendMessageDraft`. Follow the changelog for the method, and read §6.2.6 before enabling topics on
a selling bot. Neither was tested live.

---

## Pitfalls

| Trap | What happens | Fix |
|---|---|---|
| Skipped `sendRichMessage` after stream ends | Draft disappears after ~30 s, no permanent message | Always call `sendRichMessage` with full text as last step |
| `chat_id` is a String or `@username` | `sendRichMessageDraft` returns error | Only Integer chat_id supported for drafts; fall back to `sendMessage` + `editMessageText` in groups/channels |
| Sending a draft update every token | Flood / rate limit, poor animation | Batch tokens, send at most every 1–2 s |
| `RichBlockThinking` in `sendRichMessage` | Not stored in Message; spec prohibits it | Remove Thinking block before finalization |
| Partial Markdown mid-stream | Unclosed `` ``` `` or `**` renders broken | Either send complete blocks only, or use raw text during streaming and apply Markdown only at finalization |
| 30-second window expires mid-stream | Draft gone | If stream is slow, send a keep-alive draft update (even unchanged text) before the window closes |
| Stream keeps running after the user pressed Stop | Tokens are spent, drafts keep coming | Handle `stopped_message_generation` and cancel the model call |
| `keep_on_stop` treated as saved text | The draft disappears after a short time | Send the partial text as a new message |

---

## Group / channel fallback

`sendRichMessageDraft` is private-chat only. For groups and channels:

1. Send initial `sendMessage` with `"⌛ Generating…"` placeholder.
2. Edit with `editMessageText` (rich_message) when done.

No real-time animation, but the final message is rich-formatted.

---

## Request reference

```
sendMessageDraft      POST /bot<TOKEN>/sendMessageDraft
  chat_id            Integer   required — private chat only
  message_thread_id  Integer   optional
  draft_id           Integer   required — non-zero; same id = animated update
  text               String    optional — 0-4096; empty shows "Thinking…"
  parse_mode         String    optional
  entities           Array of MessageEntity   optional
  can_stop           Boolean   optional — show the stop button
  keep_on_stop       Boolean   optional — keep the draft briefly after stop

sendRichMessageDraft  POST /bot<TOKEN>/sendRichMessageDraft
  chat_id            Integer   required — private chat only
  message_thread_id  Integer   optional
  draft_id           Integer   required — non-zero; same id = animated update
  rich_message       InputRichMessage   required
  can_stop           Boolean   optional — show the stop button
  keep_on_stop       Boolean   optional — keep the draft briefly after stop

sendRichMessage       POST /bot<TOKEN>/sendRichMessage
  chat_id        Integer or String   required
  rich_message   InputRichMessage    required
  → returns Message (use .message_id for edits)

editMessageText       POST /bot<TOKEN>/editMessageText
  chat_id        Integer or String
  message_id     Integer
  rich_message   InputRichMessage    (mutually exclusive with "text")
```

`InputRichMessage` fields: exactly one of `html`, `markdown`, or `blocks`, optional `is_rtl`, optional `skip_entity_detection`.

---

## Related

- [`../tg-rich-messages/SKILL.md`](../tg-rich-messages/SKILL.md) — full block & inline type reference
- [`../../reference/rich-messages-spec.md`](../../reference/rich-messages-spec.md) — core Bot API 10.3 reference
