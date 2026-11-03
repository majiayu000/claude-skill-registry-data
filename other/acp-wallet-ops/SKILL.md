---
name: acp-wallet-ops
description: "Use when checking balance, topping up or signing. Address and balance per chain, top-up by Coinbase or card, signing and raw transactions, wallet policies and the signer policy, compute status — reads first, every write behind the owner's yes."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, EconomyOS, ACP, Virtuals, wallet, policy, signer]
    related_skills: [economyos, consent, acp-agent-identity, acp-trade-hyperliquid, acp-troubleshooting]
---

# ACP wallet ops — know what the agent holds, move nothing without a yes

## When to use

- The owner asks what the agent holds, where to send funds, or why a payment failed for lack of balance.
- A job fund or a trade needs a top-up first.
- A dapp or a counterparty asks the agent to sign a message, typed data or a transaction.
- The owner asks which guardrails (wallet policy, signer policy) the agent runs under.

The Wallet app playbook and the six laws are in `economyos`. This skill is the exact command set and its order.

## Prerequisites

- Setup done: agent and signer (`acp-agent-identity`). Commands run through `~/.iclone-os/bin/acp --inft <iNFT>`.

## Quick reference — reads (free to run)

```sh
~/.iclone-os/bin/acp --inft <iNFT> wallet address --json
~/.iclone-os/bin/acp --inft <iNFT> wallet balance --json
~/.iclone-os/bin/acp --inft <iNFT> wallet balance --chain-id 8453 --ticker USDC --json
~/.iclone-os/bin/acp --inft <iNFT> chain list --json
~/.iclone-os/bin/acp --inft <iNFT> agent signer-policy --json
~/.iclone-os/bin/acp --inft <iNFT> policy global --json
~/.iclone-os/bin/acp --inft <iNFT> policy list --limit 20 --json
~/.iclone-os/bin/acp --inft <iNFT> policy show <policy-id> --json
~/.iclone-os/bin/acp --inft <iNFT> compute status --json
```

`wallet balance` with no flag covers every sponsored chain; `--token <symbolOrAddress>` reads one token, `--cluster
<name>` one cluster. A `null` total means "not read", never zero.

## Quick reference — writes (owner's yes first)

```sh
~/.iclone-os/bin/acp --inft <iNFT> wallet topup --method coinbase --chain-id 8453 --amount <usd> --json
~/.iclone-os/bin/acp --inft <iNFT> wallet topup --method card --chain-id 8453 --amount <usd> --email <owner-email> --json
~/.iclone-os/bin/acp --inft <iNFT> wallet send-transaction --chain-id 8453 --to <0xTo> --value <wei> --json
~/.iclone-os/bin/acp --inft <iNFT> wallet sign-message --message "<text>" --chain-id 8453 --json
~/.iclone-os/bin/acp --inft <iNFT> wallet sign-typed-data --data '<json>' --chain-id 8453 --json
~/.iclone-os/bin/acp --inft <iNFT> policy create --name "<name>" --contract <Label=0xContract> --json
~/.iclone-os/bin/acp --inft <iNFT> policy edit <policy-id> --json
~/.iclone-os/bin/acp --inft <iNFT> agent set-signer-policy --agent-id <agent-id> --json
```

Card top-ups by US residents add `--us`. `send-transaction` takes `--data <hex>` for a contract call. `policy edit`,
`policy delete <policy-id>` and `agent set-signer-policy` only return a dashboard URL: the wallet owner approves there.

## Procedure

1. Read before you write: `wallet address`, then `wallet balance` on the chain that matters. Report asset, amount, chain.
2. For any command in the writes block, state what will happen — amount, asset, chain, destination, fee if known — then
   ask through the consent door and wait for the owner's yes (you operate, the owner spends — `economyos` law 1):

   ```sh
   ~/.iclone-os/bin/acp --inft <iNFT> consent request spendTrade --reason "Send <amount> <asset> on Base to <0xTo>"
   ```

3. Top-up: the owner picks the method (`coinbase` or `card`) and the amount; you run it.
4. When a command returns a URL (top-up checkout, policy dashboard), STOP and paste it raw on its own line
   (`economyos` law 2). Then re-read `wallet balance` once the owner says they finished.
5. Signing: say what the message or typed data authorises (spender, amount, deadline) in plain words before asking.
   Typed data that grants an allowance is a value move, not "just a signature".
6. Policies: `policy global` lists the platform presets (`DENY_ALL`, `ACP_ONLY`); a custom policy is an allowlist of
   addresses (Ethereum only). The signer policy is the owner's call (`economyos` law 5) — explain, never change on your own.
7. Compute credits are not part of setup in iclone os (`economyos` → Identity and setup). Run `compute top-up` only
   when the owner asks for it by name, with the same consent step.

## Pitfalls

- `NO_SIGNER` on a write = the signer step is missing: `acp-agent-identity`, not a retry.
- `transfer amount exceeds balance` while funding a job: `acp-troubleshooting` E20.
- `--value` is in wei; `--amount` on `topup` is in dollars. Convert out loud before asking.
- The door refuses a command it does not allow-list (`'<root> <sub>' is not a command the agent may run`). Report the
  refusal verbatim to the owner; never run the CLI another way.

## Never

- Never top up, send, sign, create or edit a policy without the owner's yes through the consent door (`spendTrade`).
- Never print a private key, a seed or a card number; never read the CLI's config files.
- Never pick the funding method, the amount or the chain for the owner.

## Verification

`wallet balance --chain-id 8453 --json` after the write shows the expected change, or `agent signer-policy --json`
shows the policy the owner approved.
