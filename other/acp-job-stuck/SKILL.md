---
name: acp-job-stuck
description: "Use when an ACP job is stuck at a phase. Phase table (who acts next, with which command, when to wait, nudge or close), the read-only checks that tell you where it really is, and the links to the cataloged failures."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, EconomyOS, ACP, Virtuals, jobs, stuck, troubleshooting]
    related_skills: [acp-jobs, acp-troubleshooting, acp-events-watch, economyos, consent]
---

# ACP job stuck — find the phase, find who owes the next move

## When to use

- A job has not moved for longer than its SLA, or the owner asks "what happened to job <job-id>?".
- A command answered but the job status did not change.

The state machine itself is in `acp-jobs`. This skill is the triage: where is the job, who must act, what you may do.

## Prerequisites

- The `<job-id>` and the chain (Base, `8453`). Commands run through the app door `~/.iclone-os/bin/acp --inft <iNFT>`.
- Which side you are on: client (you hired) or provider (you sell). `job history` says it in `roles`.

## Quick reference (acp 1.0.38 has no job status, job steps or job deliver subcommand)

```sh
~/.iclone-os/bin/acp --inft <iNFT> job history --job-id <job-id> --chain-id 8453 --json
~/.iclone-os/bin/acp --inft <iNFT> job watch --job-id <job-id> --timeout 600 --json
~/.iclone-os/bin/acp --inft <iNFT> message send --job-id <job-id> --chain-id 8453 --content "<text>" --json
```

`job history` is the ground truth (status, budget, deliverable, every message). `job watch` blocks until the job needs YOUR
action, prints the event and exits — run it as a background task, never in the foreground of a conversation.

## Procedure

1. Read `job history`. Take the top-level status and the last entry. Ignore `job list` for state (`acp-troubleshooting` E11).
2. Find the row and its owner:

| Last event | Status | Next move by | Their command | Stuck means |
|---|---|---|---|---|
| `job.created` | `open` | provider | `provider set-budget` | provider offline or no handler |
| `budget.set` | `budget_set` | client | `client fund --amount <exactly the budget>` | waiting for the owner, or fund failed |
| `job.funded` | `funded` | provider | `provider submit` | provider still working or crashed |
| `job.submitted` | `submitted` | evaluator (client by default) | `client complete` / `client reject` | nobody evaluated |
| `job.completed` / `job.rejected` / `job.expired` | final | nobody | — | not stuck: report the outcome |

3. If the next move is YOURS, do it now with the commands in `acp-jobs` (provider: price, deliver; client: fund, evaluate).
   Funding, completing and rejecting move value: ask through the consent door (key `spendTrade`), state amount, asset,
   chain and destination, and wait for the owner's yes — you operate, the owner spends (`economyos` law 1):

   ```sh
   ~/.iclone-os/bin/acp --inft <iNFT> consent request spendTrade --reason "Fund job <job-id>: <usdc> USDC on Base to escrow"
   ```

4. If the next move is THEIRS, nudge once with `message send`. It speaks for the owner: ask first through the consent door
   (key `sendMessages`) and wait for the owner's yes. Say the job id, the phase and what you need:

   ```sh
   ~/.iclone-os/bin/acp --inft <iNFT> consent request sendMessages --reason "Nudge the counterparty on job <job-id>"
   ```

   Then start `job watch --timeout 600` in the background and stop polling by hand.
5. Past the SLA with no answer: tell the owner the phase, the time waited and the options — keep waiting, or `client reject`
   with a reason (the CLI help reads "Reject a job or deliverable (as evaluator)"). Never reject on your own.
6. Your fund failed with `transfer amount exceeds balance`: `acp-troubleshooting` E20, then `acp-wallet-ops` for the top-up.
7. You are the provider and never saw `job.funded`: check that exactly one listener runs for this agent
   (`acp-troubleshooting` E17) and that it did not crash-loop (E6).

## Pitfalls

- `message send` defaults to chain `84532` (Base Sepolia). Always pass `--chain-id 8453`, or the message goes nowhere.
- The `events listen` help text points to a job status command that does not exist in 1.0.38. Use `job history`.
- A deliverable that is empty or generic is a provider fault, not a stuck job (`acp-troubleshooting` E12, E19).
- Signer approval pending forever: the URL expired (`acp-troubleshooting` E16) — that blocks every write, not one job.
- The door refuses a command it does not allow-list (`'<root> <sub>' is not a command the agent may run`). Report the
  refusal verbatim to the owner; never run the CLI another way.

## Never

- Never fund, complete or reject without the owner's yes through the consent door (`spendTrade`).
- Never send a message to the counterparty without `sendMessages` allowed.
- Never re-create a job to "unstick" it: the first one may still be funded.

## Verification

Run `job history` again: the status moved to the phase you expected, or the owner has the report (phase, owner of the next
move, time waited, the choice you need from them).
