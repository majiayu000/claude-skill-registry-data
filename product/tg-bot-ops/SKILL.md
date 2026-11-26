---
name: tg-bot-ops
description: "Use when running a Telegram bot in production: webhook or long polling, allowed_updates, webhook secret token, privacy mode, 429 and retry_after, file retries, broadcast limits and paid broadcasts, lost updates on shutdown, a poison update after new Bot API types, t.me outage and fallback domains, local Bot API server."
license: MIT
---

# tg-bot-ops

Checked against the official docs on 2026-10-30: Bot API 10.3 (August 24, 2026). Reports from trackers are labeled with their date. No scenario here was run against a live bot; [scripts/retry_policy.py](scripts/retry_policy.py) has unit tests on simulated responses.

## Webhook or polling

Mutually exclusive. Either way, Telegram keeps undelivered updates [at most 24 hours](https://core.telegram.org/bots/api#getting-updates).

| | Long polling | Webhook |
|---|---|---|
| Fits | one process, no public HTTPS, a local machine | several workers, serverless |
| Ack | next `getUpdates` with a higher `offset` | your 2xx response |
| Limits | `limit` 1-100, `timeout` above 0 | ports 443, 80, 88, 8443; `max_connections` 1-100, default 40 |
| Failure | the same updates return until `offset` moves | non-2xx is repeated, then Telegram gives up "after a reasonable amount of attempts" |

Switching: `getUpdates` doesn't work while a webhook is set; use `deleteWebhook`. Keep `drop_pending_updates` off on a selling bot: it discards unprocessed `successful_payment` messages too.

Monitor `getWebhookInfo`: `pending_update_count`, `last_error_message`, `last_error_date`, `allowed_updates`.

A reply in the webhook response body (`method` plus parameters) saves a request, but its success and result can't be known. Use a normal request for anything you must confirm.

Webhook setup:

1. `setWebhook` with `secret_token`: 1-256 characters of `A-Za-z0-9_-`.
2. Reject any request whose `X-Telegram-Bot-Api-Secret-Token` header differs, using a constant-time compare.
3. Store the update durably, return 2xx, and process it afterwards. Answer `pre_checkout_query` right in the handler, ahead of any queue: it expires in 10 seconds (`tg-stars-payments`).

## allowed_updates

- Omitted: **the previous setting stays**. A list set once survives every deploy, so a new feature's update type never arrives until you pass a new list.
- Empty list: all types except `chat_member`, `message_reaction` and `message_reaction_count`, which need explicit opt-in and admin rights.
- A change doesn't affect updates created before the call.

Send the full list on startup and compare it with `getWebhookInfo.allowed_updates`. Types added in 2026: `guest_message`, `managed_bot`, `subscription`, `stopped_message_generation`.

## Privacy mode

On by default. In groups the bot sees commands meant for it, replies to it and messages sent via it, plus all service messages. An admin bot sees everything. After turning it off in @BotFather, re-add the bot to each group for the change to [take effect](https://core.telegram.org/bots/features#privacy-mode).

## 429 and retries

Documented [limits](https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this): about 1 message per second per chat (short bursts allowed), 20 per minute in a group, about 30 per second for bulk. Treat the numbers as approximate and let `retry_after` rule. Flood limits are not raised in the [test environment](https://core.telegram.org/bots/features#dedicated-test-environment) and may at times be stricter, and a [maintainer says](https://github.com/tdlib/telegram-bot-api/issues/677) the local server doesn't change them (2024-12-13). `answerCallbackQuery` has no limit, editing is under the per-chat limit ([maintainer, 2024-10-09](https://github.com/tdlib/telegram-bot-api/issues/648)).

| Response | Meaning | Action |
|---|---|---|
| 429 with `parameters.retry_after` | not applied | hold the whole scope that long, then repeat |
| `parameters.migrate_to_chat_id` | group became a supergroup | store the new id, repeat |
| other 4xx | rejected | fix the request; 403 usually means the user blocked the bot |
| 5xx, timeout, dropped connection, non-JSON | **unknown**, it may have been delivered | report it and reconcile; resend only if a duplicate is harmless |

```python
import retry_policy as rp

gate = rp.FloodGate()                       # one per process

def make_request():                         # called on every attempt
    return build_multipart(url, fields, open(path, 'rb'))

decision = rp.send(make_request, transport, gate, f'chat:{chat_id}')
if decision.action == rp.UNKNOWN:
    park_for_reconcile(decision.reason)     # never treat this as a failed send
```

`transport(request)` is yours: it returns `(status, body)`, it should close the file, and any exception it raises counts as **unknown**, because the bytes may have left. `make_request` runs outside that guard: when it raises, for example on a missing file, nothing was sent and the exception reaches you.

`FloodGate` lives in the memory of one process. Several workers need a shared store for pauses, for example Redis with a key per scope and a TTL of `retry_after`.

The pause length belongs to the server: `Decision.wait` carries `retry_after` as received. `send` sleeps up to `max_inline_wait` (60 seconds by default). A longer pause comes back as `FAIL` with the real `wait`, so a handler can reschedule the send and free its worker.

Two failure modes this shape avoids, both reported in libraries in 2026:

- **Stale multipart.** Retrying a consumed upload fails with "media not found" ([grammY #862](https://github.com/grammyjs/grammY/issues/862), fixed 2026-01-16). The factory rebuilds the body each attempt.
- **Pause lifted early.** A shared event let any finishing request end the `RetryAfter` pause ([PTB #5338](https://github.com/python-telegram-bot/python-telegram-bot/issues/5338), closed 2026-09-13). `FloodGate` ends a pause by clock only. aiogram has no built-in rate limiter yet ([#1875](https://github.com/aiogram/aiogram/issues/1875), open on 2026-10-30).

Scope the gate by chat for sends, and by bot for a broadcast. For bulk, a queue at 30 per second or fewer is cheaper than handling 429s.

### Paid broadcasts

`allow_paid_broadcast: true` raises the limit to 1000 messages per second, at 0.1 Star per message above the free 30. Eligibility is stated two ways, and [@BotFather](https://t.me/botfather) decides:

| Source | Requirement | Checked |
|---|---|---|
| [Bot API page](https://core.telegram.org/bots/api#paid-broadcasts) | 10,000 Stars on the balance | 2026-10-30 |
| [Bot FAQ](https://core.telegram.org/bots/faq#how-can-i-message-all-of-my-bots-subscribers-at-once), [Terms § 6.2.5](https://telegram.org/tos/bot-developers#6-2-5-broadcasting-messages-with-stars) | 100,000 Stars and 100,000 monthly active users | 2026-10-30 |

## Not losing updates

- An update counts as confirmed the moment `getUpdates` is called with a higher `offset`. Recalculate `offset` after every response and save the update first, so a crash replays it.
- **Shutdown.** Stop fetching, wait for running handlers, then exit. aiogram doesn't wait for handlers whose updates are already confirmed, so a running payment handler dies ([#1955](https://github.com/aiogram/aiogram/issues/1955), open on 2026-10-30).
- Duplicates happen: handlers are idempotent, by `update_id` for transport repeats and by the domain key for money (`tg-stars-payments`). After a week without updates the next `update_id` is [random](https://core.telegram.org/bots/api#update), so never assume it only grows across a gap.
- Webhook versus polling reliability: one practitioner lost messages on webhooks and fixed it with polling ([Reddit](https://www.reddit.com/r/TelegramBots/comments/1rrlzlb/built_a_monetized_ai_companion_bot_on_telegram/), self-report). No reproducible report exists either way; a durable inbox beats the choice of transport.

## Poison updates

New Bot API versions add fields and types without notice to old clients. A library that fails to decode one update never moves `offset`, and the bot stops. Bot API 10.3 did exactly that: `RichTextButton` made aiogram raise `ClientDecodeError` and block polling until 3.31 ([#1890](https://github.com/aiogram/aiogram/issues/1890), 2026-08-25). Deeply nested `rich_message.blocks` stalled validation with a single update ([#1842](https://github.com/aiogram/aiogram/issues/1842), 2026-06-29).

Before each Bot API version reaches users:

1. Read the raw JSON first, and persist it before typed parsing.
2. Put decoding inside a per-update guard. On failure, save the raw update to a dead-letter store, count it, and advance `offset` (or return 2xx).
3. Treat unknown fields and types as ignorable.
4. Alert on a repeating `update_id` and a growing `pending_update_count`.
5. Update your library when [the changelog](https://core.telegram.org/bots/api-changelog) moves, and test a replay of stored raw updates.

```python
for update in updates:
    store_raw(update)                       # before anything can fail
    try:
        handle(decode(update))
    except Exception as error:
        dead_letter(update, error)          # poison stops here, offset still moves
    offset = update['update_id'] + 1
```

A `successful_payment` in the dead-letter store still owes the buyer: replay it through the ledger, or follow the recovery rules in `tg-stars-payments`, because `getStarTransactions` lacks `subscription_expiration_date`.

## Domains

On 2026-07-13 at 19:24 UTC the `t.me` domain went down for about a day after an [OFAC listing](https://ofac.treasury.gov/recent-actions/20260713) named a `t.me` address; `telegram.me` kept working ([TechCrunch](https://techcrunch.com/2026/07/14/telegrams-shortlink-domain-is-back-online-after-day-long-suspension/), [Cybernews](https://cybernews.com/security/telegram-links-broken-after-domain-outage/)). No official post-mortem was found.

The fallback isn't universal. Reports from that day:

- Posts and bot links: `telegram.me` worked; profile images saved on `t.me` broke, and the swap fixed them ([HN](https://news.ycombinator.com/item?id=48898291)).
- Invoices: `createInvoiceLink` returned `telegram.me`, and the invoice did not open until the host was replaced with `t.me` ([PTB #5296](https://github.com/python-telegram-bot/python-telegram-bot/issues/5296)).
- Mini Apps: tma.js `openTelegramLink` rejected `telegram.me` and `telegram.dog` ([#879](https://github.com/Telegram-Mini-Apps/tma.js/issues/879), closed 2026-07-14).

So keep the host in one config value, avoid `t.me` allowlists in validators and store usernames instead of full links. A URL returned by the API can fail too: open an invoice on a client to check it, and test any fallback for invoices and Mini App links before relying on it.

## Local Bot API server

Run [tdlib/telegram-bot-api](https://github.com/tdlib/telegram-bot-api) for [these features](https://core.telegram.org/bots/api#using-a-local-bot-api-server): unlimited download, upload up to 2000 MB, `file://` paths, absolute `file_path` from `getFile`, HTTP webhooks on any port and local IP, `max_webhook_connections` up to 100000. Everything else, including flood limits, stays.

Moving a bot:

1. `logOut` before pointing it at the local server. The bot can't return to the cloud for 10 minutes.
2. Moving between local servers: `deleteWebhook`, then `close`. `close` returns 429 during the first 10 minutes after launch.
3. Put a TLS proxy in front; the local server speaks HTTP.

Done when `getMe` answers on the new URL and updates arrive there.

## Sources

- https://core.telegram.org/bots/api#getting-updates
- https://core.telegram.org/bots/api#setwebhook
- https://core.telegram.org/bots/api#getupdates
- https://core.telegram.org/bots/faq
- https://core.telegram.org/bots/webhooks
