---
name: telegram-polls
description: Send Telegram polls and quizzes with up to 12 options.
version: 1.0.0
author: serejaris, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [telegram, polls, messaging]
    category: messaging
    related_skills: [telegram-client, telegram-rich-messages]
---

# Telegram Polls Skill

Send a Telegram poll or quiz from the `telegram_client` tool as one message: post text plus poll, up to 12 options, multiple answers, participants adding options, revoting, shuffle, hidden results, members-only and country-limited voting, and quizzes with several correct answers. This skill is a port of `tg-polls` (serejaris/telegram-skills, Bot API 10.3) to Telethon layer 233; it sends nothing itself.

## When to Use

Use when the user asks for a poll, a quiz, a vote, or a "pick one / pick several" question in a Telegram chat or channel. Use the Telegram client skill for other client operations and the rich-messages skill when the post needs headings, tables, or in-body buttons — a poll cannot go inside a rich message (no poll block exists among the rich blocks), so a long post goes first as a rich message and the poll second.

## Prerequisites

- `telegram_client` is available in this Telegram conversation. `poll_create`, `poll_results`, and `poll_stop` are owner-only actions with a confirmation card; all three target the current chat/topic and cannot be redirected.
- Polls are created with `InputMediaPoll` via `SendMediaRequest` (Telethon layer 233, verified by construction). There is no `StopPollRequest` in layer 233: stopping is a `closed=True` `EditMessageRequest` on the poll media, which the tool already does.

## How to Run

1. **Preview before sending.** A sent poll cannot be edited — neither its question, its options, nor its description. Fix mistakes in a preview (your own chat or a staging group); a correction is a new poll.
2. **Call `telegram_client` with `action="poll_create"`** and the params below. Confirm the question, options, and visibility on the confirmation card before submitting.
3. **Verify the result.** The tool returns a `message_id`. Read the poll back with `poll_results` to confirm it landed.
4. **Stop it with `action="poll_stop"`** and the `message_id` when voting should close. The tool copies every flag the poll was created with into the closed edit, so stopping never silently drops settings.

## Quick Reference

### `poll_create` params

| Param | Type | Notes |
| --- | --- | --- |
| `question` | string, 1–300 | Required. Only custom-emoji entities; the tool sends plain text. |
| `options` | list of 1–12 unique strings, 1–100 each | Required. The old 2–10 cap is gone: 11- and 12-option polls are valid. |
| `description` | string, 0–1024 | Post text above the poll (the `SendMedia` caption). Longer text goes in a separate rich message first. |
| `anonymous` | boolean, default `true` | `false` makes voters public (`public_voters`). |
| `multiple_choice` | boolean, default `false` | Several answers per voter. |
| `quiz` | boolean, default `false` | Quiz mode. |
| `correct_answers` | list of 0-based indexes | Required for a quiz; several correct answers allowed. The old single `correct_option` param was replaced — passing it fails loudly naming `correct_answers`. |
| `solution` | string, 0–200 chars, at most 2 line feeds | Quiz explanation shown after answering. |
| `open_period` | integer seconds, 5–2628000 | Auto-close after this long. Cannot combine with `close_date`. |
| `close_date` | unix time | Auto-close at this time, 5–2628000 seconds ahead. Cannot combine with `open_period`. |
| `country_codes` | list of 0–12 ISO codes | Channels only. `FT` means anonymous numbers. |
| `allow_adding_options` | boolean, default `false` | Participants suggest options in an active poll. Not for anonymous polls or quizzes. |
| `revoting` | boolean | Default `true` for regular polls, `false` for quizzes. |
| `shuffle_options` | boolean, default `false` | Shuffle the option order per voter. |
| `hide_results_until_close` | boolean, default `false` | Hide results until the poll closes. |
| `members_only` | boolean, default `false` | Only members for more than 24 h. Channels only. |

### Bot API → MTProto name map

| Bot API (`sendPoll`) | MTProto (`poll` / `InputMediaPoll`) |
| --- | --- |
| `description` | `SendMediaRequest.message` (the caption) |
| `allows_multiple_answers` | `multiple_choice` |
| `is_anonymous` (default true) | inverse of `public_voters` |
| `allow_adding_options` | `open_answers` |
| `allows_revoting` | inverse of `revoting_disabled` |
| `shuffle_options` | `shuffle_answers` |
| `hide_results_until_closes` | `hide_results_until_close` |
| `members_only` | `subscribers_only` |
| `country_codes` | `countries_iso2` |
| `type: "quiz"` + `correct_option_ids` | `quiz` + `InputMediaPoll.correct_answers` |
| `open_period` / `close_date` | `Poll.close_period` / `Poll.close_date` |

### Option bytes

Option identifiers are the opaque `PollAnswer.option` bytes. Hermes uses `bytes([i])` (the skill's Telethon form); polls created before this port used `bytes([65 + i])`. The bytes are per-poll identifiers — a vote is matched by the option bytes the server returns for that poll, so never assume an option's bytes from another poll.

## Procedure

### Regular poll with a description

```json
{
  "action": "poll_create",
  "params": {
    "question": "Where do you track tasks when agents write the code?",
    "description": "Backlog, release plans, what to do tomorrow. Pick several if you combine tools.",
    "options": ["Jira", "Linear", "GitHub / GitLab Issues", "Notion", "Obsidian", "Markdown files in the repo", "Other (in comments)"],
    "multiple_choice": true
  }
}
```

### Quiz with several correct answers

```json
{
  "action": "poll_create",
  "params": {
    "question": "Which two are valid?",
    "options": ["A", "B", "C", "D"],
    "quiz": true,
    "multiple_choice": true,
    "correct_answers": [0, 2],
    "solution": "A and C are valid."
  }
}
```

Quiz and multiple choice can be combined. `correct_answers` takes several indexes; a quiz with one correct answer passes a one-element list.

### Read results and stop

```json
{"action": "poll_results", "params": {"message_id": 123}}
{"action": "poll_stop", "params": {"message_id": 123}}
```

## Pitfalls

- A sent poll cannot be edited. Preview first; a correction is a new poll.
- `poll_results` reports only observed vote counts (cached poll media and `UpdateMessagePoll`). The bot must never call the user-only `messages.getPollResults` RPC, and voter identities are not exposed.
- Media on the poll (`InputMediaPoll.attached_media`) and media on an option (`InputPollAnswer.media`) exist in MTProto but are not wired into `poll_create` yet — there is no send path for them in this action. Do not invent one; a poll with attached media needs a raw `InputMediaPoll` send, which the agent tool does not offer.
- `country_codes` and `members_only` work in channels only; the tool refuses them elsewhere.
- `chat_id` cannot be a channel direct-messages chat.
- Do not use `poll_create` for a vote that needs headings, tables, or buttons — that is a rich message, and a poll cannot live inside one.

## Verification

- The tool result is `ok` with a `message_id`. `poll_results` on that ID returns the question and the option list.
- A quiz shows its explanation after answering; a regular poll shows the voter count.
- `poll_stop` returns `closed: true`, and `poll_results` afterwards reports `closed: true`.
- On a validation failure the tool fails before the confirmation card — no poll is created and nothing needs undoing.
