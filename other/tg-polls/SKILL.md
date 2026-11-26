---
name: tg-polls
description: "Use when sending a Telegram poll or quiz from a bot or a user account (Telethon/MTProto): one-message post with text plus poll (poll description), media on the poll or on options, up to 12 options, multiple answers, participants adding options, revoting, shuffle, hidden results, members-only and country-limited voting, quiz with several correct answers. Also use to decide whether text and poll fit in one message."
license: MIT
---

# tg-polls

Checked against the official docs on 2026-10-30: Bot API 10.3 (latest, August 24, 2026), MTProto layer 225+ (`poll`, `inputMediaPoll`), Telegram blog post of 2026-03-31 "AI Editor, Mighty Polls…". Nothing here was run against a live bot.

## One message: text + poll

A post and its poll fit in one message. Put the post text into the poll **description**, not into a separate message.

| Need | Bot API (`sendPoll`) | User account (MTProto / Telethon) |
|---|---|---|
| Post text above the poll | `description`, 0–1024 chars after entities parsing; `description_parse_mode` / `description_entities` | `message` of `messages.sendMedia` with `media=inputMediaPoll` (Telethon: `send_file(chat, InputMediaPoll(...), caption=TEXT)`) |
| One photo/video/file on the poll | `media` (InputPollMedia: animation, audio, document, live photo, location, photo, venue, video) | `inputMediaPoll.attached_media` |
| Media on an option | `InputPollOption.media` (animation, link, live photo, location, photo, sticker, venue, video) | `inputPollAnswer.media` |
| Text longer than 1024 chars | separate message first (for example a rich message), poll second | same |

A poll can't go inside a rich message (no poll block among the 24 `InputRichBlock` types), into an album (`sendMediaGroup` takes audio, document, live photo, photo, video only) or into `sendMessage`.

MTProto `attached_media` does not accept a freshly uploaded file: `inputMediaUploadedPhoto` returns `ATTACH_MEDIA_INVALID`. Upload first with `messages.uploadMedia`, then pass `inputMediaPhoto` with the returned photo's id, access hash and file reference. Verified 2026-11-11 in a self-chat: 12 options plus a photo, read back as `messageMediaPoll` with `attached_media`.

MTProto has no separate description field in `poll` / `inputMediaPoll`. The caption is the description. Verified 2026-10-16 with Telethon 1.44 (layer 227) in a self-chat: the server accepted a 12-option poll with a caption and returned the text in `message.message`.

## Limits

| What | Limit | Since |
|---|---|---|
| Options | **1–12** (`poll_answers_max` = 12 in client config) | max 12 in Bot API 9.1, min 1 in 10.0 |
| Question | 1–300 chars; only custom emoji entities | |
| Option text | 1–100 chars; only custom emoji entities | |
| Description | 0–1024 chars | 9.6 |
| Quiz explanation | 0–200 chars, at most 2 line feeds; `explanation_media` | media in 10.0 |
| `open_period` / `close_date` | 5–2628000 s, not both | 9.6 |
| `country_codes` | 0–12 ISO codes, channels only; `FT` = anonymous numbers | 10.0 |

Older code often hardcodes 10 options. Remove that check: it rejects valid 11- and 12-option polls.

## Settings

Bot API name → MTProto flag on `poll`:

- `allows_multiple_answers` → `multiple_choice`. Default off; turn it on when people combine tools.
- `is_anonymous` (default true) → inverse of `public_voters`.
- `allow_adding_options` → `open_answers`. Participants suggest options in an active poll; not for anonymous polls and quizzes. MTProto: `messages.addPollAnswer`, a participant may delete own answer within `poll_answer_delete_period` (300 s).
- `allows_revoting` (default true for regular polls, false for quizzes) → inverse of `revoting_disabled`.
- `shuffle_options` → `shuffle_answers`.
- `hide_results_until_closes` → `hide_results_until_close`.
- `members_only` → `subscribers_only`: only members for more than 24 h; channels only.
- `country_codes` → `countries_iso2`.
- Quiz: `type: "quiz"` + `correct_option_ids` (several correct answers allowed since 9.6) → `quiz` + `inputMediaPoll.correct_answers`.

`chat_id` can't be a channel direct messages chat: `sendPoll` rejects polls there.

## Reading results

Options can appear and disappear after sending, so positions aren't stable. Key votes by persistent id.

| Field | Where | Meaning |
|---|---|---|
| `persistent_id` | `PollOption` | Option id that survives option addition and deletion |
| `option_persistent_ids` | `PollAnswer` | Persistent ids of the chosen options; empty when the vote was retracted. `option_ids` holds 0-based positions |
| `poll_option_added`, `poll_option_deleted` | `Message` service messages | `PollOptionAdded` / `PollOptionDeleted`: `option_persistent_id`, `option_text`, `option_text_entities`, optional `poll_message` |
| `added_by_user`, `added_by_chat`, `addition_date` | `PollOption` | Who added the option and when; omitted for original options |
| `poll_option_id` | `ReplyParameters` | Reply to a specific option, by persistent id |
| `reply_to_poll_option_id` | `Message` | The option a message replies to |

Limits on what a bot can read:

- `poll_answer` updates arrive only for non-anonymous polls the bot sent itself. `poll` updates cover polls the bot sent and polls stopped manually. A bot can't count votes in someone else's poll beyond the `voter_count` it sees in a message.
- Detailed poll statistics are MTProto only: `stats.getPollStats`, available when `pollResults.can_view_stats` is set. The Bot API has no equivalent. Telegram's blog says they become available after a poll receives 100 votes.

## Bot API example

```bash
curl -s "https://api.telegram.org/bot$TOKEN/sendPoll" \
  -H 'Content-Type: application/json' \
  -d '{
    "chat_id": "@your_channel",
    "question": "Where do you track tasks when agents write the code?",
    "description": "Backlog, release plans, what to do tomorrow. Pick several if you combine tools.",
    "options": [{"text": "Jira"}, {"text": "Linear"}, {"text": "GitHub / GitLab Issues"},
                {"text": "Notion"}, {"text": "Obsidian"}, {"text": "Markdown files in the repo"},
                {"text": "Other (in comments)"}],
    "is_anonymous": true,
    "allows_multiple_answers": true
  }'
```

## Telethon example

```python
from telethon.tl.types import InputMediaPoll, Poll, PollAnswer, TextWithEntities

answers = [PollAnswer(text=TextWithEntities(text=o, entities=[]), option=bytes([i]))
           for i, o in enumerate(options)]          # up to 12
poll = Poll(id=0, hash=0, question=TextWithEntities(text=question, entities=[]),
            answers=answers, multiple_choice=True)
await client.send_file(chat, InputMediaPoll(poll=poll), caption=post_text)  # caption = description
```

## Before sending

1. Preview in your own chat (Saved Messages or a bot DM), then send to the audience.
2. Options and question within the limits above; description ≤ 1024.
3. A sent poll can't be edited: Bot API has no method for its question or options, and the description is frozen too. Verified 2026-10-16 from a user account: `messages.editMessage` with new text on a poll returns `MESSAGE_NOT_MODIFIED`, and Telegram apps show no Edit for polls. Fix mistakes in the preview; a correction is a new poll.

## Sources

- Bot API: https://core.telegram.org/bots/api#sendpoll · changelog https://core.telegram.org/bots/api-changelog
- MTProto: https://core.telegram.org/api/poll · https://core.telegram.org/constructor/inputMediaPoll · https://core.telegram.org/constructor/poll · client config https://core.telegram.org/api/config · poll statistics https://core.telegram.org/api/stats
- Blog: https://telegram.org/blog/ai-editor-mighty-polls-and-more · https://telegram.org/blog/ai-bot-revolution-11-new-features
