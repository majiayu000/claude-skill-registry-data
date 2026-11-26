---
name: tg-capability-map
description: "Use before promising a Telegram feature or designing around one: what a bot can do in Bot API, what lives only in the client or MTProto (scheduled posts, channel stats, poll stats, channel stories, folders, boosts, welcome messages, communities), and what never to promise from a bot."
license: MIT
---

# tg-capability-map

A map with no code. Absence from Bot API was established from the [method list](https://core.telegram.org/bots/api) at Bot API 10.3 (August 24, 2026), checked on 2026-10-30. In the tables, **Since** is when the feature appeared where known, and **Checked** is the date the address was read. MTProto methods are named so you can find them; building an account client is a separate decision.

## How to use

1. Find the row. A bot can do only what the **Bot API** column shows.
2. A row with "no" in that column is off the table for a bot: name the alternative (a person in the client, or an account session) in your plan.
3. Open the address when the answer decides the work.

## Bot API only reads or partly reaches it

| Capability | Bot API | Client or MTProto | Since | Checked | Source |
|---|---|---|---|---|---|
| Scheduled post | no; `SCHEDULE_BOT_NOT_ALLOWED`. Run your own timer | `schedule_date` on `messages.sendMessage`, `messages.sendMedia` | long-standing | 2026-10-30 | https://core.telegram.org/method/messages.sendMessage |
| Repeating scheduled post | no | `schedule_repeat_period`, Premium, one message, seven fixed intervals from 1 day to 365 days | 2025-11-19 | 2026-10-30 | https://core.telegram.org/api/scheduled-messages |
| Channel stats | no; `Message` has no view or forward counter | `stats.getBroadcastStats`, `stats.getMessageStats`; channels of a certain size | long-standing | 2026-10-30 | https://core.telegram.org/api/stats |
| Poll stats | no | `stats.getPollStats`; the client shows them after 100 votes | 2026-05-07 | 2026-10-30 | https://telegram.org/blog/ai-bot-revolution-11-new-features |
| Votes in polls the bot didn't send | no; `poll_answer` only for its own polls | `messages.getPollVotes` | long-standing | 2026-10-30 | https://core.telegram.org/bots/api#update |
| Channel stories | no; `postStory` is for managed business accounts only | `stories.sendStory`, right `post_stories`, enough boosts | long-standing | 2026-10-30 | https://core.telegram.org/bots/api#poststory |
| Live Stories | no | client, RTMP key, boosts on a channel | 2025-11-19 | 2026-10-30 | https://telegram.org/blog/live-stories-gift-auctions |
| Available reactions of a channel | read only, `ChatFullInfo.available_reactions` | `messages.setChatAvailableReactions` | long-standing | 2026-10-30 | https://core.telegram.org/api/reactions |
| Paid reactions | no; "Bots can't use paid reactions" | `messages.sendPaidReaction` | long-standing | 2026-10-30 | https://core.telegram.org/bots/api#setmessagereaction |
| Linking a discussion group | read only, `linked_chat_id` | `channels.setDiscussionGroup` | long-standing | 2026-10-30 | https://core.telegram.org/api/discussion |
| Channel direct messages | answers with `direct_messages_topic_id`, right `can_manage_direct_messages`; can't enable them | `channels.updatePaidMessagesPrice` | Bot API 9.2, 2025-08-15 | 2026-10-30 | https://core.telegram.org/api/monoforum |
| Boosts | read only, `getUserChatBoosts`, `chat_boost` | `premium.applyBoost`, Premium users | long-standing | 2026-10-30 | https://core.telegram.org/api/boost |
| Giveaways | no method to start one; winners arrive as messages | `payments.*`, channel admin | long-standing | 2026-10-30 | https://core.telegram.org/api/giveaways |
| Channel auto-translation | no | `channels.toggleAutotranslation`, boost level | long-standing | 2026-10-30 | https://core.telegram.org/api/translation |
| Chat folders | no | `messages.updateDialogFilter`, `chatlists.*` | long-standing | 2026-10-30 | https://core.telegram.org/api/folders |
| Protected content for a whole chat | no; `protect_content` per message | `messages.toggleNoForwards`, owner | long-standing | 2026-10-30 | https://core.telegram.org/api/content-protection |
| Welcome messages | right `can_send_welcome_messages`, which the API describes as letting a bot send them directly; no method found to set or send one | client, chat profile, Edit | 2026-08-25 | 2026-10-30 | https://telegram.org/blog/welcome-messages-buttons-TG-13 |
| Communities | read only, `Community`, service messages; can't create | client | 2026-07-14 | 2026-10-30 | https://core.telegram.org/bots/api-changelog#july-14-2026 |
| Rich text editor for people | bots send rich messages to everyone | client editor, Premium | 2026-07-14 | 2026-10-30 | https://telegram.org/blog/communities-editor-invisible-messages |
| AI text editor | no | `messages.composeMessageWithAI`, client | 2026-03-31 | 2026-10-30 | https://core.telegram.org/api/ai |
| AI summaries of long channel posts | no control; the reader taps it | client | 2026-01-03 | 2026-10-30 | https://telegram.org/blog/new-design-ai-summaries |
| Star withdrawal | no; balance and history only | `payments.getStarsRevenueWithdrawalUrl`, owner, 2FA | 2024 | 2026-10-30 | https://core.telegram.org/api/stars |

## Limits a bot does not share with an account

| Capability | Bot | Account | Since | Checked | Source |
|---|---|---|---|---|---|
| Caption length | 1024 | 1024, Premium 4096 (`caption_length_limit_*`, example config) | long-standing | 2026-10-30 | https://core.telegram.org/api/config |
| File upload | 50 MB, local server 2000 MB | 2 GB, Premium 4 GB | long-standing | 2026-10-30 | https://telegram.org/faq |
| Message effects | private chats only | client | long-standing | 2026-10-30 | https://core.telegram.org/bots/api#sendmessage |
| Custom emoji in channel posts | only with Fragment usernames; the Premium-owner route covers private chats and groups | Premium | Bot API 9.4, 2026-02-09 | 2026-10-30 | https://core.telegram.org/bots/api#formatting-options |
| Message drafts | private chats only, no streaming into a channel | client | Bot API 9.3, 2025-12-31 | 2026-10-30 | https://core.telegram.org/bots/api#sendmessagedraft |
| Reaction count per message | one reaction | 1, Premium 3 (example config) | long-standing | 2026-10-30 | https://core.telegram.org/bots/api#setmessagereaction |

## Do not promise from a bot

Each line follows from the tables above.

- "The bot will schedule it inside Telegram." Your server holds the timer, so the post sends only while the server runs.
- "The bot will report views and shares."
- "The bot will show poll statistics" or see votes in a poll a person posted.
- "The bot will post to the channel's stories."
- "The bot will set up the channel": reactions, comments, direct messages, folders, boosts, welcome text, protected content, auto-translation.
- "The bot will create a community or a giveaway."
- "The bot will withdraw the Stars."
- "The bot will stream an answer into a channel."

## When a map row is stale

Re-check on every Bot API version, starting with 10.4:

1. Read the new entry in the [changelog](https://core.telegram.org/bots/api-changelog).
2. For each new method or right, find the row it touches and update Bot API, Since and Checked.
3. Open the address of every row marked "no" whose topic the release touches, and confirm it.
4. Update the check date in this file's intro.

Done when each changed row has a new Checked date and the intro names the new version.
