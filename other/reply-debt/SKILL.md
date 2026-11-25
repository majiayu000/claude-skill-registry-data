---
name: reply-debt
description: Find the mail still waiting on a reply by dropping threads already answered, bots and newsletters, keeping messages that ask something, and ranking them by how long the person has waited. Use when asked what needs a reply, who is waiting, what fell through in the inbox, or to produce a daily follow-up brief.
---

# Reply Debt

## What it does

Reads recent inbound mail, removes everything that is not a person waiting on you,
and ranks what is left by wait time. The output is a short list: who, about what,
how long they have waited.

No language model reads the mail. Every include and exclude is a substring rule in
the config, so a wrong answer is a rule you can find and change.

## Prerequisites — read this before you start

**This skill is not credential-free.** It needs access to a mailbox:

| backend | needs | notes |
| --- | --- | --- |
| `gmail-api` | `GMAIL_ACCESS_TOKEN` in the environment | OAuth access token, `gmail.readonly` scope. Add `gmail.send` only if the user wants `--send`. |
| `composio` | `COMPOSIO_API_KEY` in the environment, plus `--connection-id` | For a Composio-managed Gmail connection. The connection id is an identifier, not a secret. |
| `fixture` | nothing | A local JSON file of messages. No network. |

Read the token from the environment only. Never pass it as a command-line
argument, never write it into a config file, never echo it.

If no mailbox is connected, use `--backend fixture` and say plainly that the
mailbox part is unverified. Do not describe a fixture run as a run against real
mail.

## How the filtering works

1. Fetch `in:inbox newer_than:{days}d from:me` and remember those thread ids.
   Anything you already replied to in the window is not debt.
2. Fetch `in:inbox newer_than:{days}d -from:me`.
3. Drop a message when the sender matches `skip_sender` (no-reply, notifications,
   newsletters, transactional addresses), when the subject matches `skip_subject`
   (receipts, invitations, promotions), or when neither subject nor snippet
   contains anything in `expects_reply`.
4. Rank: `wait_points_per_day` per day waited, capped at `wait_days_cap`, plus
   `important_points` for each `important_hints` match. Ties break oldest first.

`important_hints` only reorders. It never filters anything in or out, so a term
missing from that list cannot make mail disappear.

## Tuning the rules

Every list lives in `--config` JSON and replaces the default wholesale. Start from
[`examples/rules.example.json`](examples/rules.example.json).

The failure mode to watch for is **`expects_reply` being too narrow**, because that
silently hides real mail. A short note that just says "thanks, go ahead" contains
none of the default terms and will be dropped. Run with `--backend fixture` against
a saved sample of your own mail and check the drop counts before trusting it.

The opposite failure — `skip_sender` too broad — is the reason `support@`, `team@`
and `hello@` are separate entries you can remove: at a small company a real person
does write from `hello@`.

## Running it

```
python scripts/reply_debt.py --backend fixture --fixture tests/fixtures/inbox.json
python scripts/reply_debt.py --backend gmail-api --days 10 --top 10
python scripts/reply_debt.py --backend gmail-api --notify-email you@yourdomain --send
```

The brief is always written to `--out`. **Sending is off unless you pass `--send`.**
There is no default recipient: with `--send` and no `--notify-email`, the script
falls back to the address it saw on your own sent mail, and refuses to send if it
cannot find one. It will never mail an address that shipped with the skill.

Exit codes: `0` success, `1` the mail backend failed, `2` bad config.

A backend failure exits `1` and is never reported as an empty inbox. "Nothing is
waiting on you" only ever means the fetch succeeded and nothing matched.

## Boundaries

- Read-only against the mailbox, except the one optional brief you send yourself.
- It reads subjects, senders and snippets. It never reads full message bodies and
  never sends anything to a third-party model.
- It does not reply to anyone, never drafts a reply, and never contacts the sender.
- Do not use it to decide that a thread does not need an answer. It ranks what is
  probably waiting; it does not know what matters.
