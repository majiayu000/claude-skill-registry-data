---
name: agentic-economy
description: "Use when a request touches agent commerce. Load it first. The map of the iNFT's economy inside iclone os and the law over all of it: which skill carries which commands (economyos · acp-offerings · acp-jobs · acp-paid-subscription-checkout · acp-troubleshooting) and the rule that you operate and the owner spends. Load FIRST when a request touches agent commerce, an agent wallet/email/card, hiring or selling agent work, subscriptions, ERC-8004 identity or tokenising an agent — it routes; it does not carry commands."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, EconomyOS, ACP, Virtuals, router, law]
    related_skills: [economyos, acp-offerings, acp-jobs, acp-paid-subscription-checkout, acp-troubleshooting]
---

# The agentic economy — the map, and the law

An iNFT is not just a model with tools. It holds an address, receives mail,
is paid, pays, is hired, hires, and carries a reputation that outlives any
one conversation. In iclone os all of that runs on **Virtuals ACP** through
ONE command, routed to this token's own isolated config:
`~/.iclone-os/bin/acp --inft <your token> … --json`.

**This skill is the map, not the manual.** Commands live in exactly one
skill each, so nothing contradicts:

| You need to… | Load |
|---|---|
| act on the wallet, inbox, card, Hyperliquid, or read the marketplace — the daily driver, and the per-app playbook | **`economyos`** |
| define, price, publish, edit or retire what the iNFT sells (offerings), its reference endpoints (resources) or subscriptions; the catalogue JSON file; the 40-offering cap | **`acp-offerings`** |
| hire an agent or deliver a job: the escrow state machine, funding only after `budget_set`, execute → verify → submit with proof, the traps | **`acp-jobs`** |
| pay for a subscription with the agent's own email + single-use card (3DS, receipts, paid-access check) | **`acp-paid-subscription-checkout`** |
| a command fails, an offering is invisible, a signer is revoked, state looks wrong, a headless provider server | **`acp-troubleshooting`** |
| drive the iclone os app itself (`it` CLI, windows, Setup wizard) | **`iclone-os`** |

The CLI's own operating guide, version-matched to the installed binary, is
always one command away and outranks any prose about it:
`~/.iclone-os/bin/acp --inft <token> skill print`.

## 0. The law that outranks everything below

**You operate. The owner spends.**

Every read, probe, provision and draft is yours to run without asking.
Anything that **moves value or cannot be undone** is prepared by you and
executed only on the owner's explicit, per-action approval:

- signing or broadcasting a transaction · funding · topping up · withdrawing
- `tokenize` (irreversible, spends VIRTUAL + gas, bakes in permanent economics)
- funding a job's escrow · completing/rejecting a job · buying, selling, swapping, bridging, opening a perp
- issuing a card (refused by the wrapper anyway — the owner's terminal), raising a spend limit, paying a merchant
- adding a signer or changing its policy

The vendor's own agent docs are more permissive. **The owner's rule wins
here**, and it is his decision, not a limitation of the tools. The shape of
every money move is: *proposal → safety check → the OWNER approves →
executed. Nothing self-initiates.* Say what a command will cost and what it
will change, then wait. An approval covers **that** action, not the next one.

Never handle a private key or seed phrase: not read, not echoed, not written
to a file. Signers are provisioned through a browser approval the owner
clicks — that is the whole point of their design.

## 1. Which iNFT? Which economy?

- Each iNFT in iclone os is its own agent, wallet, inbox, card and catalogue. Your runtime block names your token; **never** run another token's slug.
- "my agent", "hire", "sell a service", "the marketplace", "escrow", "offering", "job" → ACP (`acp-jobs`, `acp-offerings`).
- "my wallet", "balance", "swap", "bridge", "Hyperliquid", "email", "card" → `economyos`.
- "Robinhood Chain" (`4663`, settles in USDG) is a chain the ACP CLI reaches with `--chain-id 4663` — not a separate CLI. "Robinhood Agentic Trading" is an unrelated brokerage product; ask which the owner means.

## 2. Reporting on the economy

Money deserves the engineer's reporting discipline — claim · evidence · how
measured · what was not checked:

- Never state a balance, price or fee without its **unit and timestamp**. `total: null` from `wallet balance --ticker` means "not read", never zero.
- **Units are where agent-money bugs live:** `card issue --amount` and `card limit set --amount` are **cents**; `compute top-up --amount`, `wallet topup --amount`, `client fund --amount`, `provider set-budget --amount` are **whole USDC**; `wallet send-transaction --value` is **wei**. Read the flag, never the prose, and say the unit out loud.
- Distinguish **committed** from **available**: USDC in escrow on a funded job is not spendable.
- An agent that exists but was never set up earns nothing — say "not set up yet" rather than counting it as a business.
- Before proposing anything that spends: **what it costs · what it changes · whether it can be undone.** Those three lines are what the owner approves.

## 3. The open stack underneath (corrections worth carrying)

ERC-8004 = discovery and trust receipts (a draft; identity + reputation registries are deployed, validation is not; reputation is per chain) · A2A = the conversation between agents (v1.0 uses PascalCase methods and `/.well-known/agent-card.json`) · MCP = the toolbelt · x402 = the money (v2 headers `PAYMENT-REQUIRED` / `PAYMENT-SIGNATURE` / `PAYMENT-RESPONSE`, CAIP-2 networks) · ERC-6551 = the wallet that belongs to a token (registry `0x000000006551c19487814612e58FE06813775758`; the account is derived from the token, so selling the NFT hands over the wallet without changing its address — that is what makes an iNFT transferable). **None of them does escrow, disputes or refunds** — that is the hole ACP's USDC escrow fills.

## 4. Never

- Sign, send, fund, swap, tokenise or issue without the owner's explicit approval for that action.
- Touch a private key or seed phrase.
- Print a command for the owner to run, or swallow a URL they need to click.
- Report a browser-pending step as completed.
- Quote an amount without checking which unit that flag wants.
- Invent a flag: `acp <cmd> -h` outranks every document, including this one.
