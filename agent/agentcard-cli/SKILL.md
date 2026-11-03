---
name: agentcard-cli
description: "Use when using the direct agentcard CLI (0.4.0). Pick the path first (the iNFT's acp card or the owner's own agentcard.ai account), read its status without leaking secrets, and walk the owner through signup, setup, KYC and limits on the direct account."
version: 2.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, EconomyOS, AgentCard, card, KYC, Mastercard Agent Pay]
    related_skills: [agentcard, agentcard-signup, agentcard-troubleshooting, economyos, consent]
---

# AgentCard — two paths, one owner

There are two ways to an AgentCard, and they are two separate accounts. Signing in on one never signs in the other.

| | `acp card` (Virtuals) | `agentcard` CLI (direct) |
|---|---|---|
| Whose account | The iNFT's own Virtuals agent | The owner's own agentcard.ai account |
| How you run it | `~/.iclone-os/bin/acp --inft <iNFT> card … --json` (`economyos`) | `agentcard …` (npm package `agentcard`, by Alchemy) |
| Session lives in | that iNFT's ACP config, kept by the app | `~/.agentcard/config.json`, one per Mac user |
| What the app shows | the Bank window and Settings → Setup | nothing; it is the owner's terminal tool |
| Skill with the commands | `agentcard-signup`, `agentcard-troubleshooting` | this skill, plus the official `agentcard` skill |

**Use `acp card`** for anything about the iNFT's card: the Bank window, the Setup wizard's card step, spend requests of
that iNFT, its agent inbox (`@agents.world`).

**Use the `agentcard` CLI** only when the owner chooses the direct account: Mastercard Agent Pay, his own connected card,
`agentcard identity` (KYC), the AgentCard USDC wallet, phone. The official `agentcard` skill (v2.2.0, shipped unedited)
is the full command reference. This skill adds what the official one cannot know: this Mac and its rules.

## When to use

- The owner asks to set up, redo or check his direct AgentCard account.
- An instruction you hold names `agentcard create` or `agentcard agentic …`: those families were REMOVED in 0.4.0.
  Purchases are `agentcard request …`; payment sources are `agentcard sources …`.

## Prerequisites

- `agentcard` on PATH (`~/.local/bin/agentcard`, installed with `npm install -g agentcard --prefix ~/.local`).
- **Every run updates itself first** (`npm view agentcard version`, then a global install). For a status read set
  `AGENTCARD_SKIP_UPDATE=1`. After a real update, re-read the official `agentcard` skill before the next command.
- Consent: `sendMessages` before a signup (it sends an e-mail); `spendTrade` before setup, limits, sources or a purchase.

## Quick reference (0.4.0)

| Need | Command | Write? |
|---|---|---|
| Who is signed in | `agentcard whoami` | no |
| KYC status | `agentcard identity --json --no-open` | no (but see Pitfalls) |
| Spend limits | `agentcard limit` | no |
| Payment sources | `agentcard sources list --json` | no |
| Purchases | `agentcard request get --json` | no |
| Sign up / log in | `agentcard signup --email <email>` | yes, sends a magic link |
| Payment path, agent email, wallet | `agentcard setup --mastercard` or `agentcard setup --no-mastercard` | yes |
| Complete KYC | `agentcard identity --no-open` → relay the URL | the owner completes it |
| Change a limit | `agentcard limit --amount <dollars> [--source connected]` | yes |
| Pay one purchase | `agentcard request new --merchant <name> --url <url> --item <item> --amount <dollars>` | yes, spends |

There is no `--json` on `whoami`, `limit` or `signup`; `request *`, `sources *`, `identity` and `3ds` take it.

## Procedure — read the status

    AGENTCARD_SKIP_UPDATE=1 agentcard whoami
    AGENTCARD_SKIP_UPDATE=1 agentcard identity --json --no-open
    AGENTCARD_SKIP_UPDATE=1 agentcard limit

Name the state in one sentence, nothing more:

- `Not logged in` or `Session expired` = **signed out**.
- `identityVerificationStatus` other than `verified`/`exempt` while `identityVerificationRequired` is true = **KYC required**.
- An HTTP 403, "locked", "blocked" or "suspended" = **blocked**: stop; the owner writes to AgentCard
  (`agentcard support --message "…"`, with his yes).
- A signed-in `whoami`, KYC `verified` or `exempt`, and a limit = **ready**.

## Procedure — the owner redoes the setup

1. Ask through the consent door (`sendMessages`), naming the address. Then `agentcard signup --email <owner's email>`.
   It polls for five minutes: let it finish; never kill and retry. The owner clicks the link in his own inbox.
2. Ask him one question: "Will you pay with a Mastercard?" Then `agentcard setup --mastercard` or
   `agentcard setup --no-mastercard`. Relay the printed card-entry URL raw, on its own line. He types the card in his
   browser; never ask him for card numbers.
3. `agentcard identity --no-open`. If it prints a verification URL, give it to the owner only (it carries his session
   token) and wait. KYC is his: you never fill identity data.
4. `agentcard limit`; a change needs his amount and his yes. Direct accounts have a $200 daily ceiling.
5. Read the status again (above) and say the one sentence.

## Pitfalls

- `agentcard identity --json` prints a URL whose `identity_token` is the owner's session token. Never paste it in chat,
  notes or files; redact it to `identity_token=<redacted>` if you must show the line.
- Magic links are single-use: opening one with `curl` spends it without signing in.
- A one-time card number prints PAN, CVV and expiry to stdout. Report `last4` and amount only.
- Do not run the direct CLI to work around a refusal of `acp card` (`economyos`): they are different accounts.

## Never

- Never sign up, set up, complete KYC, change a limit or spend without the owner's explicit yes.
- Never store the session token, magic links, KYC links, 3DS codes or card data anywhere.
- Never run `agentcard setup --reset` unless the owner asks to replace his payment method or agent email.

## Verification

`AGENTCARD_SKIP_UPDATE=1 agentcard whoami` prints the signed-in user, `agentcard identity --json --no-open` reports
`verified` or `exempt`, and `agentcard limit` prints the limit the owner approved.
