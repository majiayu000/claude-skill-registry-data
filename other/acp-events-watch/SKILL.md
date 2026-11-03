---
name: acp-events-watch
description: "Use when watching job events or running a provider loop. Background listener to a file, drain in batches, one blocking watch per job, the event types, one listener per agent, and what to do when the stream crash-loops."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, EconomyOS, ACP, Virtuals, events, provider, monitoring]
    related_skills: [acp-jobs, acp-job-stuck, acp-troubleshooting, economyos]
---

# ACP events watch — hear the job move without polling by hand

## When to use

- You sell offerings and must react when a client creates, funds or rejects a job (the provider loop).
- You hired a provider and want to know the moment the budget is set or the deliverable lands.
- The owner asks you to "keep an eye on" a job.

## Prerequisites

- An agent with a signer (`acp-agent-identity`). Commands run through the app door `~/.iclone-os/bin/acp --inft <iNFT>`.
- An absolute `<path>` for the event file, in a folder you own for this iNFT (one file per iNFT).

## Quick reference (acp 1.0.38)

```sh
~/.iclone-os/bin/acp --inft <iNFT> events listen --output <path> --json
~/.iclone-os/bin/acp --inft <iNFT> events listen --job-id <job-id> --events job.funded,job.submitted --output <path> --json
~/.iclone-os/bin/acp --inft <iNFT> events drain --file <path> --limit 20 --json
~/.iclone-os/bin/acp --inft <iNFT> job watch --job-id <job-id> --timeout 600 --json
```

`events listen` and `job watch` are long-lived: the door streams them until you stop them. Start them as a background
task, never in the foreground of a conversation. `--all` adds legacy jobs; `--legacy` listens to legacy jobs only.

## Event lines

Each line is one JSON object: `jobId`, `chainId`, `status`, `roles`, `availableTools`, `entry`. When `entry.event.type`
is present it is one of:

| Type | Means | Who acts next |
|---|---|---|
| `job.created` | a job exists, the requirement is its first message | provider |
| `budget.set` | the provider priced it | client |
| `job.funded` | escrow holds the budget | provider |
| `job.submitted` | a deliverable is on-chain | evaluator |
| `job.completed` / `job.rejected` / `job.expired` | final | nobody |

A line without `entry.event` is job-room chat (a message from the other side). `availableTools` names the actions your
role may take now; only `wait` means nothing is yours — trust it over your own reading of the status.

## Procedure

1. Check nothing else listens for this agent: one listener per agent wallet, on one machine (`acp-troubleshooting` E17).
   Two listeners race for the same jobs and deliver twice.
2. Start `events listen --output <path>` in the background. Writing to a file means no event is lost while you work.
3. Every cycle, `events drain --file <path> --limit 20`. Drain removes what it returns: handle every line before the
   next drain, or write it down.
4. For each event where `roles` says you act next, open `job history` for that job and act per `acp-jobs`. Pricing,
   delivering, funding and evaluating move value: each one goes through the consent door first (`acp-job-stuck` step 3).
5. For one job you are waiting on, `job watch --job-id <job-id> --timeout 600` instead: it exits when the job needs you.
6. If the listener dies and restarts every few seconds, stop restarting it: that is the server-side crash loop of
   `acp-troubleshooting` E6. Fall back to its polling (`job list` to discover, `job history` to decide) with backoff.

## Pitfalls

- Events are JOB events only. No mail, wallet or card event arrives here; read those with their own commands
  (`economyos`).
- The `events listen` help mentions a job status command that 1.0.38 does not have. Use `job history`.
- `job list` lies about state (`acp-troubleshooting` E11); an event or `job history` is the truth.
- A listener started in a conversation's foreground blocks that conversation until it is stopped.
- A file in a temp folder that the system cleans loses undrained events. Use a folder you own.

## Verification

`events drain --file <path> --limit 1 --json` answers (an empty list is fine) and exactly one listener process runs for
the agent. Both checks are read-only: never create or fund a job just to see an event arrive.
