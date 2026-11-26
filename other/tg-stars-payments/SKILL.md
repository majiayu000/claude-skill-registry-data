---
name: tg-stars-payments
description: "Use when a Telegram bot or Mini App sells digital goods for Stars (XTR): invoices and invoice links, openInvoice, pre_checkout_query, crediting on successful_payment without double delivery, refunds and /paysupport, 30-day subscriptions, paid media, testing payments, Star payout figures."
license: MIT
---

# tg-stars-payments

Checked against the official docs on 2026-10-30: Bot API 10.3 (August 24, 2026), the [Stars payments guide](https://core.telegram.org/bots/payments-stars) and the [developer terms](https://telegram.org/tos/bot-developers) § 6.2. Nothing here was run against a live bot, see [Not verified live](#not-verified-live).

Digital goods and services sold inside Telegram apps go through Stars only: currency `XTR`, empty `provider_token`. Physical goods use a provider, see [Payments](https://core.telegram.org/bots/payments). Payout rates, the hold, expiry and the 15% topics fee live in [references/stars-economics.md](references/stars-economics.md); read it before quoting money or enabling topics in private chats.

## Purchase flow

1. **Subscribe.** The active `allowed_updates` includes `message` and `pre_checkout_query`, plus `subscription` and `purchased_paid_media` when you sell those. An omitted list keeps the previous setting, see `tg-bot-ops`. A bot without `pre_checkout_query` lets every checkout time out.
2. **Create the invoice** (table below). Put an order id in `payload` (1-128 bytes). The title is 1-32 characters, the description 1-255, `prices` has exactly one item, amounts are whole Stars.
3. **Answer pre-checkout** within 10 seconds with `answerPreCheckoutQuery`, or the transaction is canceled. Answer it in the handler itself, outside any update queue: a queue that lags 10 seconds cancels the purchase. Check stock and order state, not delivery. On `ok: false` pass `error_message`; Telegram shows it to the user.
4. **Credit on `successful_payment` only.** It arrives as a service message. Answering pre-checkout proves nothing; a Mini App `paid` status is a hint for the UI.
5. **Store first, deliver second.** See [Recording and delivery](#recording-and-delivery).
6. **Support.** The bot answers `/paysupport`, and refunds through [Refunds](#refunds-and-disputes).

Done when: a repeated `successful_payment` starts no new delivery, two parallel handlers claim a payment once, and a crash between storing and delivering returns the order to the queue.

## Creating the invoice

| Surface | Method | Notes |
|---|---|---|
| Chat of any type | `sendInvoice` | The first inline button must be Pay. Does not take `subscription_period` |
| Mini App, website, your own link | `createInvoiceLink`, then `Telegram.WebApp.openInvoice(url, callback)` | Required for subscriptions |
| Inline mode | `inputInvoiceMessageContent` | Always a multi-chat invoice |

For Stars the `need_*`, `send_*_to_provider` and `is_flexible` fields are ignored, tips are not supported.

**Forwarded copies.** Empty `start_parameter`: forwarded copies keep Pay, several people can pay one invoice. Non-empty: forwards get a deep link to the bot. A single-chat invoice in the chat with the bot is payable once; in any other chat it can be paid many times. In every multi-use case the guard is your pre-checkout answer: accept a second payment only when the order can run twice.

**Link host.** Keep the URL from `createInvoiceLink` out of allowlists and regexes: the host can change. The link the API returns may still fail to open. During the `t.me` outage on 2026-07-14 a practitioner saw the method return `telegram.me`, the invoice did not open, and only replacing the host by hand helped ([PTB #5296](https://github.com/python-telegram-bot/python-telegram-bot/issues/5296), practitioner report). Open a real invoice on a client before and after any workaround.

**Mini App.**

- `invoiceClosed` statuses are `paid`, `cancelled`, `failed` and `pending`. On `pending` the payment is still processing; wait for `successful_payment` on the server.
- Call `openInvoice` from the Mini App's own domain. Since July 20, 2026 Mini App methods are disallowed from other origins, opt-out in @BotFather ([Bot API 10.2](https://core.telegram.org/bots/api-changelog#july-14-2026)).
- Take the buyer from the signed `initData` on your server, never from `initDataUnsafe` (see `tg-miniapp-launch-auth`). The `successful_payment` sender is the final answer.
- On Telegram Desktop a Stars invoice with an insufficient balance can fail with `PROVIDER_ACCOUNT_INVALID` for third-party bots ([tdesktop #31262](https://github.com/telegramdesktop/tdesktop/issues/31262), practitioner report, open on 2026-10-30).

## Recording and delivery

One payment gets one ledger row and one live claim. Delivery itself runs at least once: a crash after your `deliver` and before the mark repeats it after the lease. The buyer gets one product only when `deliver` is idempotent by `payment.key`, or when the credit shares a transaction with the mark.

The key is `telegram_payment_charge_id`. It is the identifier the docs tell you to store, and `StarTransaction.id` equals it for incoming user payments, so `getStarTransactions` can reconcile against your ledger.

`update_id` is no key for money. A Bot API maintainer: it "can't be used as an idempotency key for payments", it only orders updates and discards duplicates ([tdlib #837](https://github.com/tdlib/telegram-bot-api/issues/837), 2026-03-27). After a week without updates the next `update_id` is [chosen randomly](https://core.telegram.org/bots/api#update). A practitioner reports repeated `successful_payment` deliveries ([dev.to](https://dev.to/haskelldev/how-to-accept-payments-in-a-telegram-mini-app-using-stars-step-by-step-guide-46je), self-report, not reproduced here).

**Renewals.** The docs do not say whether a subscription renewal gets a new charge id. Key on `telegram_payment_charge_id` plus `subscription_expiration_date` (0 for one-time payments): that credits each period once under either behavior.

[scripts/stars_ledger.py](scripts/stars_ledger.py) is a network-free SQLite reference with tests. A row moves through `pending`, `claimed`, `delivered`, with `refunded` reachable from each:

```python
import stars_ledger as ledger

conn = ledger.connect('/var/lib/mybot/stars.sqlite3')   # one connection per worker
payment = ledger.parse_payment(update)      # None for other updates, ValueError for a broken payment
if payment:
    ledger.record_payment(conn, payment)    # durable on return, acknowledge the update after this

for due in ledger.pending(conn, now=int(time.time())):  # also run on a timer
    if not ledger.claim(conn, due, now=int(time.time())):
        continue                            # another worker holds it
    try:
        deliver(due, idempotency_key=due.key)
    except Exception as error:
        ledger.release(conn, due)
        log_and_alert(due.key, error)       # the next rows still go out
        continue
    if not ledger.mark_delivered(conn, due) and ledger.state(conn, due) == ledger.REFUNDED:
        revoke(due)                         # the refund landed during delivery
```

One failing row must not stop the pass: a buyer who blocked the bot fails on every pass, and everyone who paid later waits behind that row. The alert is how a person learns about a row that keeps returning.

`mark_delivered` returns `False` in two cases, so read `state` before acting. `refunded` means the buyer has the Stars back and the goods went out, so revoke them. `delivered` means the lease ran out and another worker finished under the same key, so the grant stands.

Contract of the helper:

- **A file path is required.** `connect` refuses `:memory:`: a restart would erase paid orders, and a repeated update would pass as a new purchase. Telegram's [live checklist](https://core.telegram.org/bots/payments-stars#live-checklist) asks you not to lose payment data.
- **Each call commits on its own.** The ledger runs in autocommit, so no call leaves a write lock open. Use `with ledger.transaction(conn):` to join an order insert with `record_payment`.
- **`claim` is one conditional `UPDATE`.** With parallel webhooks (`max_connections` defaults to 40) `pending` shows the same row to every handler, and only one `claim` returns `True`. Delivering straight from `pending` delivers twice.
- **The lease replaces a reset on startup.** A startup reset would take claims away from workers still running. A crashed worker's row returns once `lease_until` passes (300 seconds by default). Set the lease longer than the slowest `deliver`.
- **Internal balance.** Credit only when the mark succeeds, inside one transaction: a crash undoes both, and a refund or another worker that got there first leaves the balance untouched:

```python
with ledger.transaction(conn):
    if ledger.mark_delivered(conn, due):
        credit_balance(conn, due.user_id, due.amount)
```

Keep the unique key and the conditional claim in your own schema if you adopt the logic elsewhere. Acknowledge the update only after `record_payment` returns (see `tg-bot-ops`); a dropped `successful_payment` is money taken and nothing delivered.

### Recovery from getStarTransactions

Use it after a lost update, after `drop_pending_updates`, and for dead-lettered payments. Page with `offset` and `limit` 1-100 and pass each [StarTransaction](https://core.telegram.org/bots/api#startransaction) to `ledger.reconcile_transaction(conn, transaction, since=failure_time)`.

`since` is required: set it to the Unix time of the failure, or to the moment the ledger went live if that is later. Transactions older than `since` return `False`. On a bot that sold before the ledger existed, a full history would queue every past buyer for delivery again.

`StarTransaction` has `id`, `date` and, in `TransactionPartnerUser`, `subscription_period`. It has no `subscription_expiration_date`, which is half of the ledger key, so a renewal can't be rebuilt exactly. The helper matches by these rules:

1. Search by `charge_id` first. One-time payments match on the key.
2. For a subscription, a row with the same `charge_id` is the same period when `subscription_expires_at - subscription_period` falls within half a period of `date`. Periods of one subscription lie a full period apart.
3. With no match, store a row with the estimate `date + subscription_period` and remember the period.
4. A late `successful_payment` within half a period of that estimate returns `False`, so delivery doesn't start again. It replaces the estimate with the true expiry, unless the row is `claimed`: the running delivery holds that key as its idempotency key, so the estimate stays.
5. An outgoing transaction to a user carries the id of the refunded payment and goes to `record_refund`.

A refund for a charge the ledger hasn't seen yet is stored and applied when the payment arrives, by update or by recovery, so that row never reaches delivery. Until the estimate is replaced, grant access by `subscription_expires_at` knowing it can be off by the gap between the renewal and the old expiry.

## Refunds and disputes

- `refundStarPayment(user_id, telegram_payment_charge_id)` returns the Stars in full; there is no partial-amount parameter. "invalid user_id specified" means `user_id` never reached the server: a wrapper bug ([tdlib #789](https://github.com/tdlib/telegram-bot-api/issues/789), maintainer, 2025-11-16).
- A refund shows up as a `refunded_payment` service message, handle it with `parse_refund_charge_id` and `record_refund`, and revoke access.
- `/paysupport` is mandatory (terms § 6.2.1). Failing to resolve legitimate disputes can lead to Stars debited from the balance, removal, a public SCAM label and account termination. Tell users that Telegram support will not help with purchases, and offer `/terms` ([Live Checklist](https://core.telegram.org/bots/payments-stars#live-checklist)).
- A buyer's chargeback with Apple or Google deducts the Stars from your balance ([StarTransaction](https://core.telegram.org/bots/api#startransaction)). Telegram discourages real-time sale of goods that can't be revoked after a chargeback (§ 6.2.1). Prefer access you can withdraw.

## Subscriptions

- `createInvoiceLink` with `subscription_period: 2592000`, the only allowed value (30 days), at most 10000 Stars. One user may hold several at once.
- Each paid period arrives as `successful_payment` with `is_recurring`, `subscription_expiration_date` and, on the first one, `is_first_recurring`. Grant access until `subscription_expiration_date`, and match periods by `invoice_payload`.
- `subscription` update (`BotSubscriptionUpdated`, Bot API 10.2): `state` is `canceled`, `active` (re-enabled) or `failed`. It carries `user` and `invoice_payload`, no charge id, so keep a unique payload per subscription.
- `canceled` keeps access until the end of the paid period. `editUserStarSubscription(user_id, telegram_payment_charge_id, is_canceled)` lets the bot stop or restore renewal.

## Paid media

`sendPaidMedia`: `star_count` 1-25000, up to 10 items, `payload` 0-128 bytes. In a channel the Stars go to the channel's balance, elsewhere to the bot's. `purchased_paid_media` fires only with a non-empty payload in a non-channel chat and carries `from` and `paid_media_payload`, no charge id: there the payload is your order record, and `getStarTransactions` (`transaction_type: "paid_media_payment"`) gives the transaction id. Paid media can't be copied with `copyMessage`.

## Testing payments

The sources disagree, and no official statement settles it:

| Source | Says | Date |
|---|---|---|
| [Stars payments guide](https://core.telegram.org/bots/payments-stars#testing-payments) | "You can freely test payments in Telegram Stars" in the [test environment](https://core.telegram.org/bots/features#dedicated-test-environment) | page checked 2026-10-30 |
| [tdesktop #29956](https://github.com/telegramdesktop/tdesktop/issues/29956) | A project collaborator, not Telegram: free test Stars were abused and locked | 2025-10-29 |
| [tdesktop #30037](https://github.com/telegramdesktop/tdesktop/issues/30037) | Request for test-environment purchases, closed with a redirect to bugs.telegram.org | 2025-11-23 |

Try the test environment first (separate account and bot, requests to `https://api.telegram.org/bot<token>/test/METHOD`). If you can't get Stars there, stop and ask the bot's owner. The next step spends real money, so the owner buys the Stars and makes the payment, and an agent never does either. The workaround appears in no documentation: on production, the owner pays a 1-Star invoice to themselves, then the bot calls `refundStarPayment` on the same charge. It exercises the real path at the cost of a small Stars pack bought once. Use a separate bot, so test orders stay out of real sales.

Verification checklist for that run: `successful_payment` stored once, a replayed copy of the same update delivers nothing, the refund produces `refunded_payment`, and access is revoked.

## Not verified live

No purchase, refund or subscription was executed for this skill. These remain open:

- A real Stars purchase and refund on production, and a real duplicate `successful_payment`. Duplicates are covered by unit tests on synthetic updates only.
- Whether test-environment Stars work today.
- Whether a renewal keeps or changes `telegram_payment_charge_id`.
- Which chat and which `Update` field carry `successful_payment` for invoices paid in groups, channels and inline. The guide does not say, so accept it from any chat and never filter by chat type. `parse_payment` reads every field of type `Message`. A channel post has no `from`, so the helper raises `ValueError`; dead-letter that update and recover the buyer through `getStarTransactions`. Privacy mode does not hide service messages.
- The behavior of a second `refundStarPayment` on one charge. Guard it with your ledger.
- How `date` of a renewal in `getStarTransactions` relates to `subscription_expiration_date`. The half-period window in the recovery rules rests on the 30-day period alone.
- Which transaction a `refunded_payment` means when one charge id covers several periods. It carries no expiry, so the ledger refunds the newest period it holds.
- Whether a renewal in `getStarTransactions` always has `subscription_period`. The field is optional. Without it the helper records a one-time row, and a late `successful_payment` then adds a second row.
- A repeated refund when renewals share a charge id. The next reconciliation passes the same outgoing transaction again, and `record_refund` takes the newest period not yet refunded, so one refund can withdraw one more period.
- The shape of a refund in `getStarTransactions`: the helper expects `receiver` of type `user` with `transaction_type` `invoice_payment`, inferred from the field descriptions.

## Sources

- https://core.telegram.org/bots/payments-stars
- https://core.telegram.org/bots/api#payments
- https://core.telegram.org/bots/webapps#events-available-for-mini-apps
- https://telegram.org/tos/bot-developers#6-2-digital-goods-and-services
