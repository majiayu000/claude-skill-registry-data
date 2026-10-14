---
name: clickmax-webchat
description: Use when the user wants to create, inspect, edit, enable, or disable a Clickmax webchat bot (the embeddable chat widget channel) and its pre-chat bot flow — greetings, lead capture, clickable questions, AI classification, and handoff to a human attendant.
---

## When this applies

Use this skill when the user wants a webchat bot: the chat widget embedded on their pages and the pre-chat flow that greets the visitor, captures name/email/phone, asks qualifying questions, and hands the conversation to a human attendant (LiveChat).

Not this skill:

- WhatsApp/Telegram/Instagram conversations and automations → `clickmax-flows`
- answering or assigning live conversations in the inbox → attendants/pipeline skills
- a quiz page with scoring and result screens → `clickmax-forms-quizzes` (a webchat question has no score)

- Read [pre-chat flow](references/prechat-flow.md) whenever you author or edit `preChatFlow.steps` — it has the exact step shapes and the branching rules, so you never guess a field.

## Key assumptions

- One channel = one widget. `preChatFlow` is ONE document ({enabled, steps}); `webchat_channel_update` replaces it whole, there is no step-level upsert.
- `enabled: false` on the CHANNEL takes the widget offline; `preChatFlow.enabled: false` (or `steps: []`) keeps the widget up but skips the bot and opens live chat directly. They are different switches.
- Every path of the flow must terminate in `handoff` (a human takes over in LiveChat) or `end`. A path that falls off the array ends silently — the visitor is left without an answer.
- `capture` is what turns the visitor into a CRM lead; a flow without it can hand off an anonymous visitor.
- Channels are created disabled. The user embeds the widget on a page; the bot only runs after `enabled: true`.

## Thought process

1. Find or read the channel first (`webchat_channels_list` → `webchat_channel_get`).
2. Draft the flow as a short script: greeting → capture → 1–3 qualifying questions → handoff/end. Keep it under ~8 steps; a widget is a conversation, not a form.
3. Give every step a stable, readable id (`s_welcome`, `s_capture`, `q_goal`, `h_sales`) and wire `next` explicitly wherever the array order is not the intended path.
4. Send the COMPLETE `steps` array in one `webchat_channel_update`. If it is rejected, fix that single payload against the reference shapes — do not create a second channel.
5. Leave `enabled` as it is unless the user asks to publish; say what is pending (embed on a page, enable).

## Execute guide

- Use `mcp__plugin_clickmax_clickmax__webchat_channels_list` to find the channel by name/project when the user did not give an id.
- Use `mcp__plugin_clickmax_clickmax__webchat_channel_get` before any edit; keep the existing widget settings and `appearance` untouched unless asked.
- Use `mcp__plugin_clickmax_clickmax__webchat_channel_update` with `preChatFlow: { enabled: true, steps: [...] }` to author the bot, and with `name` when the channel still has a generic name.
- Use `mcp__plugin_clickmax_clickmax__webchat_channel_create` only when the user asks for a NEW channel and none is open in the builder.

## Build a flow from scratch

When the user says "create the webchat with AI" from the builder, the channel ALREADY EXISTS (empty, generic name). Build INTO it:

1. `mcp__plugin_clickmax_clickmax__webchat_channel_get` by the given id → read `name`, `welcomeMessage`, `appearance`.
2. Compose the steps (see [pre-chat flow](references/prechat-flow.md)): `message` greeting → `capture` (name + email, phone optional) → `question` with 2–4 clickable options per qualifying axis → optional `condition`/`ai` branching → `handoff` for hot paths, `end` (or `handoff`) for the rest.
3. `mcp__plugin_clickmax_clickmax__webchat_channel_update` with `{ channelId, name: <short name from the goal>, welcomeMessage: <one-line greeting>, preChatFlow: { enabled: true, steps } }`.
4. Report the path(s) and what is still pending (enable, embed).

## Report

- Say the channel name, the number of steps, whether the flow captures the lead, and where each path ends (handoff or end).
- If the channel is disabled, say so and that enabling + embedding is the user's call.
- When offering a next-step CTA for the channel just built, point to the concrete builder route: `action="open-page"` with `path="/marketing/webchat/<channelId>"`.

## Warnings

- Do not create a second channel after a rejected update — fix the payload and retry on the same `channelId`.
- Do not send a partial `steps` array: `preChatFlow` is replaced whole and the missing steps are gone.
- Do not point `next` at an id that is not in `steps` (or at anything but `"handoff"`/`"end"`) — the widget stalls there.
- A `question` with clickable options needs at least one option; free text is `answerMode: "text"` with `options: []`.
- Do not set `enabled: true` unless the user asked to publish.

## Anti-patterns

- Building a 20-step interrogation; the visitor abandons the widget. Capture + 2–3 questions is the norm.
- Using a `question` for name/email instead of `capture` — only `capture` enriches the lead reliably.
- Hard-coding an attendant in `handoff.assignTo` without a real user id — leave it out so the conversation lands in the open queue.

---

Clickmax skill revision: `b8294822a4d6`
