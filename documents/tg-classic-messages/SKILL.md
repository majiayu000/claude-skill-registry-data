---
name: tg-classic-messages
description: "Use when sending or editing ordinary Telegram bot messages: sendMessage text, MarkdownV2/HTML escaping and entities, quotes, date_time, custom emoji, link previews, photos and documents with captions, albums, upload size limits, protect_content, copy, forward, delete. Also use to choose between a classic message and a rich message."
license: MIT
---

# tg-classic-messages

Checked against the official docs on 2026-10-30: Bot API 10.3 (August 24, 2026). Pre-send rules below come from [Formatting options](https://core.telegram.org/bots/api#formatting-options), the method pages and [Sending files](https://core.telegram.org/bots/api#sending-files). Nothing here was run against a live bot.

## Classic or rich

Default to the classic message. Take `sendRichMessage` when the content needs structure the classic format lacks. [examples/same-post.md](examples/same-post.md) builds one post both ways.

| Need | Classic | Rich (`tg-rich-messages`) |
|---|---|---|
| Text up to 4096 characters | yes | yes |
| Longer than 4096, one message | no, split into several | up to 32768 |
| Headings, tables, lists, formulas, details | no | yes |
| Link preview control | `link_preview_options` | no such parameter |
| Media with a caption, spoiler flag, caption position | `caption`, `has_spoiler`, `show_caption_above_media` | media blocks with their own captions |
| Album of 2-10 items | `sendMediaGroup` | collage, slideshow |
| Poll | `sendPoll` (`tg-polls`) | no poll block |
| Old clients | render everything | show an update placeholder for features they lack ([2026-08-25](https://telegram.org/blog/welcome-messages-buttons-TG-13)) |

Editing is one method for both: `editMessageText` takes `text` or `rich_message`.

## Limits

| What | Limit |
|---|---|
| `text` | 1-4096 characters after entities parsing |
| `caption` | 0-1024 characters after entities parsing |
| `sendMediaGroup` | 2-10 items; documents and audio only group with their own type |
| Upload by multipart | photo 10 MB, other files 50 MB |
| Upload by HTTP URL | photo 5 MB, other 20 MB; `sendDocument` by URL only for .PDF and .ZIP |
| By `file_id` | no limit, but no type change, and a `file_id` belongs to one bot |
| Photo dimensions | width + height at most 10000, ratio at most 20 |
| Download with `getFile` | 20 MB |
| `deleteMessages`, `copyMessages`, `forwardMessages` | 1-100 ids |
| `reply_parameters.quote` | 0-1024 characters, exact substring of the replied message |
| Local Bot API server | upload 2000 MB, download unlimited, see `tg-bot-ops` |

Measure against the limits after parsing, on the visible text: tags and escapes don't count. Entity `offset` and `length` are in UTF-16 code units, so an emoji outside the BMP counts as two: in Python, `len(text.encode('utf-16-le')) // 2`.

Text over 4096: split on paragraph boundaries, re-open entities in each part, and send in order with the pacing from `tg-bot-ops`. Over 1024 in a caption: send the media with a short caption and the text as a reply, or switch to rich.

## Formatting

Pick one per message: `parse_mode` or an explicit `entities` list. Entities need no escaping, so generated text is safest that way.

- **HTML.** Escape `<`, `>` and `&` in all dynamic text as `&lt;`, `&gt;`, `&amp;`. Only the [listed tags](https://core.telegram.org/bots/api#html-style) work; an unknown tag fails the send.
- **MarkdownV2.** Escape `_ * [ ] ( ) ~ ` > # + - = | { } . !` outside entities, including every `.` and `-` of plain text. Inside `pre` and `code` escape only `` ` `` and `\`; inside the `(...)` of a link only `)` and `\`.
- **Markdown** is legacy, without nesting, underline, spoiler, quotes, custom emoji or `date_time`.

Nesting: entities overlap only by full containment. `bold`, `italic`, `underline`, `strikethrough` and `spoiler` nest freely, except with `pre` and `code`. Quotes can't nest. In MarkdownV2 two adjacent quotes need an empty bold entity (`**`) between them.

- **Mentions.** `tg://user?id=` works only inside an inline link or an inline keyboard button, never as plain text.
- **Quotes.** `<blockquote>`, `<blockquote expandable>`.
- **Time in the reader's timezone** (Bot API 9.5): `<tg-time unix="1647531900" format="wDT">22:45 tomorrow</tg-time>`, format per `r|w?[dD]?[tT]?`, and `r` stands alone. An empty format shows the text as written.
- **Custom emoji:** `<tg-emoji emoji-id="…">👍</tg-emoji>`, with a real emoji inside as fallback. Allowed for bots with extra usernames bought on Fragment, or for messages sent directly to private chats, groups and supergroups when the bot's owner has Premium. Channels are not on that second list: without Fragment usernames, plan the post without custom emoji. Not tested live for this skill.
- **Effects:** `message_effect_id` works in private chats only.

## Link previews

`link_preview_options` on `sendMessage` and `editMessageText`:

- `is_disabled: true` removes the preview.
- `url` picks the page instead of the first link in the text.
- `prefer_small_media`, `prefer_large_media` take effect only with an explicit `url`.
- `show_above_text` moves the preview above the text.

## Media

- Prefer `file_id` for anything already sent; keep it per bot.
- `show_caption_above_media`, `has_spoiler` sit on the media method or `InputMedia*`.
- A send can return `message_id` 0: the server may [schedule a heavy video](https://core.telegram.org/bots/api#message) for a big chat instead of sending at once. Treat 0 as unknown, never as a stored id.
- Rebuild the multipart body on every retry, see `tg-bot-ops`.

## Protecting, copying, deleting

- `protect_content` guards one message against forwarding and saving. Protection for a whole chat is a client setting, see `tg-capability-map`.
- `disable_notification` sends silently.
- `copyMessage` has no link to the original. It can't copy service, paid media, giveaway or invoice messages; a quiz only if the bot knows `correct_option_ids`.
- `deleteMessage`: under 48 hours old. A bot deletes its own messages and, in private chats, incoming ones. In channels it needs `can_post_messages` for its own posts and `can_delete_messages` for others. A dice in a private chat is deletable only after 24 hours.
- `pinChatMessage` needs `can_pin_messages` in groups and `can_edit_messages` in channels.

Editing: `editMessageText`, `editMessageCaption`, `editMessageMedia`, `editMessageReplyMarkup`. Edits count against the chat's flood limits.

## Before sending

1. Dynamic text escaped for the chosen `parse_mode`, or sent as `entities`.
2. Visible length within the limit.
3. Preview checked in a private chat with the bot, on mobile as well.
4. Delivery outcome handled as in `tg-bot-ops`: a timeout is unknown, not failed.

## Sources

- https://core.telegram.org/bots/api#formatting-options
- https://core.telegram.org/bots/api#sendmessage
- https://core.telegram.org/bots/api#sendmediagroup
- https://core.telegram.org/bots/api#sending-files
- https://core.telegram.org/bots/api#deletemessage
