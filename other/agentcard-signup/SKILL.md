---
name: agentcard-signup
description: "Use when signing up or resuming an AgentCard account. The acp card setup order (whoami, signup, signup-poll, profile, payment method, limit), the poll schedule, the magic link from the agent inbox and the one-signup-per-state rule."
version: 1.1.1
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, EconomyOS, AgentCard, card, signup, email]
    related_skills: [economyos, consent, agent-email, agentcard-troubleshooting, agentcard-cli, agentcard, acp-troubleshooting]
---

# AgentCard signup — one account, one link, no duplicates

The CLI fixes the order: **signup → profile → payment method → limit → issue**. You drive the first four
through `~/.iclone-os/bin/acp --inft <iNFT> card … --json` (`economyos`). The app refuses `card issue`; owner
runs it in their terminal. Every answer carries `nextStep`; follow it.

**Which path.** This skill is the iNFT's card through Virtuals (`acp card`): the account the Bank window and the Setup
wizard show. The owner's own agentcard.ai account is a different account on the `agentcard` CLI (0.4.0): Mastercard
Agent Pay, `agentcard identity` for KYC. For that one, open `agentcard-cli` (and the official `agentcard` skill).
Never mix them: a sign-in on one is not a sign-in on the other.

**What sends a link.** Only `card signup --email …` sends a sign-in e-mail. `card whoami` only reads: its 200
`verified: false` ("Magic link sent but not clicked yet") is about a link sent EARLIER. The Bank window never sends one
on open; its "Send sign-in link" button runs one `card signup` on the owner's click, then waits a minute.

## When to use

- The owner asks for a card, or a purchase needs one and `card whoami` is not verified.
- A signup started earlier (you, the wizard, before a restart) must be finished.

## Prerequisites

- The agent email exists (`agent-email`): the magic link lands in that inbox.
- Consent `sendMessages` (signup sends an email) and `spendTrade` (payment method, limit) — ask through the door.

## Quick reference

| Step | Command (after `~/.iclone-os/bin/acp --inft <iNFT>`) | Write? |
|---|---|---|
| state | `card whoami --json` | no |
| signup | `card signup --email <email> --json` → `state` | yes, sends mail |
| poll | `card signup-poll --state <state> --json` → `done` | no |
| profile | `card profile --json` · `card profile set --first-name <first> --last-name <last> --phone-number <+E164> --json` | set = yes |
| payment | `card payment-method --json` → `url` | yes |
| limit | `card limit --json` · `card limit set --amount <cents> --json` (min 100) | set = yes |

## Procedure

1. Read the state first, every time:

       ~/.iclone-os/bin/acp --inft <iNFT> card whoami --json

   Map it as the app does, in this order (first match wins):
   - `verified: true` = **ready** → skip to step 5. Never sign up again.
   - A 200 with `verified: false` = **signin-pending** with no state token: a link is out. Fetch it (step 4), then re-read
     `card whoami` every 3 minutes (the app's pending TTL), or poll a `<state>` kept from your own signup; the server
     wins.
   - An HTTP 401 error carrying `REAUTH:<state>:<email>` = **signin-pending**: resume that `<state>` (step 3); the server's
     state wins over a remembered one.
   - `TIMEOUT`, `NOT_AUTHENTICATED`, `NO_ACTIVE_AGENT`, no output = the probe did not run; so does an error saying the
     ACP session is gone (`Session expired`, `not authenticated`, `no active agent`, `run acp configure`), whatever its
     HTTP status. The last known state holds. It is NOT "none".
   - HTTP 403/429 or "blocked / locked / suspended" = **blocked**: stop, see `agentcard-troubleshooting`.
   - A plain HTTP 401 / "unauthorized" = **signin-pending**, no state token: as the 200 case.
   - HTTP 400 "not set up" / "call card signup" = **none**: the only answer allowing step 2. A bare 400/404 is no answer.
   - Anything else (HTTP 5xx, empty `{}`, an unrecognised error) is not an answer about the card: the last known
     state holds, NOT "none".
2. Only on **none**: ask through the consent door, naming the link's address; wait for yes.

       ~/.iclone-os/bin/acp --inft <iNFT> consent request sendMessages --reason "Send the AgentCard sign-in link to <email>"
       ~/.iclone-os/bin/acp --inft <iNFT> card signup --email <email> --json

   `<email>` is the agent's own address (`email whoami`) unless the owner names another — then the owner opens the
   link from their inbox and step 4 is skipped. Keep the returned `state`. One signup per state token: the app
   refuses another only during a signup, a 403/429 hold or the minute after the last link; the rule is yours.
3. Poll with backoff 5 → 10 → 20 → 40 → 60 s, then every 60 s, for at most 15 minutes (≤ 18 polls):

       ~/.iclone-os/bin/acp --inft <iNFT> card signup-poll --state <state> --json

   Success is `done: true` only — never infer it from words in a message.
4. Fetch the link from the agent inbox (at most 3 tries; stop once found):

       ~/.iclone-os/bin/acp --inft <iNFT> email search --query "agentcard" --json
       ~/.iclone-os/bin/acp --inft <iNFT> email extract-links --message-id <message-id> --json

   Keep only links on the AgentCard host. Relay the link raw, on its own line, once per state token. Then poll the same
   `<state>`; with no state token, re-read `card whoami` every 3 minutes.
5. Profile: read it; set only what the owner gives you (never invent them).
6. Payment method: ask through the door (`spendTrade`), run `card payment-method --json`, relay the `url` raw on its
   own line; the owner completes it in their browser.
7. Limit: `card limit --json` shows `spendLimitCents`, `spentCents`, `remainingCents`. To change it, state the amount in
   dollars, ask through the door (`spendTrade`), wait for yes, then `card limit set --amount <cents> --json`.
8. Issue: tell the owner the card is ready to issue from their terminal, amount $1–$75 in whole dollars.

## Pitfalls

- `card signup` without `--email` and `card limit set` without `--amount` hang waiting for input: pass both.
- 15 minutes without `done`: say "still waiting — resume", keep the state. A NEW link while the server says
  signin-pending needs the owner's second yes; it restarts the wait.
- 429 = wait 60 s; 403 or "blocked" = a 15-minute hold that survives an app restart. Never sign up into a hold.
- Never use a plain `acp` or another config to dodge a refusal (`economyos`).

## Never

- Never send a second signup without the owner's explicit confirmation.
- Never paste magic links, codes or card data into notes; never ask the owner for card numbers.
- Never run `card issue`; never set a limit, a payment method or profile data without the owner's yes.

## Verification

`card whoami --json` prints `verified: true`; `card limit --json` prints the `spendLimitCents` the owner approved.
