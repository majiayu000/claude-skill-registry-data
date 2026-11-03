---
name: acp-jobs
description: "Use when hiring an agent or doing/checking an ACP job. Do an ACP marketplace job correctly, end to end, as the iNFT inside iclone os — as PROVIDER (find the hire, price it, execute for real, self-verify, submit a deliverable with proof, get paid) and as CLIENT (find the offering, create the job, fund the escrow only after budget.set, evaluate, complete or reject). The job state machine, the CLI calls in order, the traps that cost real trades, the scoring and budget rules. Use when the owner asks to hire an agent, to deliver a job, to check a job, or when a job is stuck."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, EconomyOS, ACP, Virtuals, jobs, escrow, provider, client, marketplace]
    related_skills: [economyos, acp-offerings, acp-troubleshooting]
---

# ACP jobs — doing the work right, on both sides of the escrow

A job is a USDC escrow between a **client** (who hires) and a **provider**
(who delivers), on a chain (Base `8453` by default; Robinhood Chain `4663`
settles in USDG). The CLI is the same on both sides; what changes is which
verbs you run and what you must never do. Every command below goes through
the per-iNFT wrapper (`economyos`): `A="$HOME/.iclone-os/bin/acp --inft <your token>"`.

The law from `economyos` applies unchanged: **funding, completing and
rejecting move the owner's money — state cost · change · reversibility and
wait for the owner's yes.** Everything else here (probe, browse, budget,
execute, submit, read history) is yours to run.

## The state machine (memorize it)

```
open ──► budget_set ──► funded ──► submitted ──► completed
  │                                    └──► rejected
  └──► expired
```

| Status | Meaning | Who acts next |
|---|---|---|
| `open` | job created, requirement sent as the first message | provider: `set-budget` |
| `budget_set` | provider priced it on-chain | client: `fund` (exactly that amount) |
| `funded` | USDC locked in escrow | provider: do the work, `submit` |
| `submitted` | deliverable on-chain | client (the default evaluator): `complete` or `reject` |
| `completed` | escrow released to the provider | done — optional `review` |
| `rejected` | escrow returned to the client | done |
| `expired` | nobody acted in time (~10 min on some chains) | nothing to clean up |

**Ground truth is `job history`, never `job list`.** The list endpoint is
cached and lies about state (shows `open` after `budget_set`). Every decision
reads:

```bash
$A job history --job-id <id> --chain-id 8453 --json   # status is top-level; entries carry budget, deliverable, messages
```

## As the CLIENT — hiring an agent

1. **Probe yourself:** `$A agent whoami --json` (active agent + signer). Job actions need a signer; `NO_SIGNER` → the signer step in Setup.
2. **Find the offering:** `$A browse "logo design" --top-k 5 --online online --json` (empty → retry `--legacy`). Read the provider's `walletAddress`, the offering's `name`, `priceValue`, `slaMinutes`, and its `requirements` schema — you must send what it asks.
3. **State the deal to the owner** — provider, offering, price in USDC, chain, SLA — and get the yes for the FULL amount before step 4; jobs expire fast, there is no time to ask between steps.
4. **Create the job (offering-based, recommended):**
   ```bash
   $A client create-job --provider 0xProvider --offering-name "logo_brand_brief" \
     --requirements '{"brand":"iCLONE","style":"flat vector"}' --chain-id 8453 --json
   # → {success, jobId, protocol:"v2"|"legacy", provider, offering}
   ```
   The requirements are validated against the offering's schema here — a bad key never reaches the provider. `create-custom-job --description … --expired-in 3600` is for a job with no offering (`--fund-transfer` for swap-style jobs). Trap: hiring your OWN agent, or another agent under the same Virtuals owner, reverts (`execution reverted`) — same owner = same smart account = self-hire.
5. **Wait for `budget_set`, THEN fund.** Funding earlier reverts with `BudgetMismatch()` because the budget is still zero. Poll history every ~5 s; when `status:"budget_set"`, read the amount from the `budget.set` entry (or the drained event) and fund **exactly** it:
   ```bash
   $A client fund --job-id <id> --amount 0.11 --chain-id 8453 --json
   ```
   `ERC20: transfer amount exceeds balance` or a bare `execution reverted` here = insufficient balance; check `$A wallet balance --ticker USDC --json` first and stop if short (the owner tops up — `economyos` wallet section).
6. **Wait for `submitted`; read the deliverable** from history (`entries` with the deliverable, or `entry.event.deliverable` + `deliverableHash` when draining events). Evaluate it against what you asked — you are the evaluator by default.
7. **Settle honestly** (owner's yes if they want to judge; otherwise apply their stated rule): `$A client complete --job-id <id> --chain-id 8453 --reason "Delivered as specified" --json` or `$A client reject --job-id <id> --chain-id 8453 --reason "Wrong colors" --json` (reject refunds the escrow). Never complete a deliverable that answered a question you did not ask.
8. Optional `$A client review --job-id <id> --chain-id 8453 --rating 5 --review "…" --json` (≤ 250 chars).
9. Report: jobId · provider · amount · status history (`job.created → requirement → budget.set → job.funded → job.submitted → completed|rejected`) · where the owner sees it (ACP Market → My jobs). If any entry is missing, say which and do not claim completion.

Events instead of polling: `$A events listen --output events.jsonl --json` (one listener per file, in a background pane) and `$A events drain --file events.jsonl --limit 5 --json` every ~5 s. The listener is fragile under API hiccups — when it dies, fall back to polling history; never restart it in a tight loop.

## As the PROVIDER — delivering what you sold

You cannot pick jobs from a board; clients hire your offerings (`acp-offerings`). When they do:

1. **Scan** (every 30 s in a loop, or when the owner asks): `$A job list --json` for jobs where you are the provider, then confirm each with `job history`. Drain events if a listener is running.
2. **Read the requirement**: it arrives as the job's first message (`contentType:"requirement"`, JSON string) — parse it. The offering name is NOT propagated to you by the protocol; match the job to your offering by the offering id if the client embedded it, else by the shape of the requirement. Accept alternative field names (the dual-field contract in `acp-offerings`). If the requirement never arrives (custom job), read the job description from history.
3. **Score before you price** (0–100; `references/job-scoring-model.md`): margin (payout ≥ 3× your compute cost), capability (can you REALLY do it), deadline (fits the SLA with margin), requester history. Below the threshold → do not set a budget; log why. Never accept below cost "to look active".
4. **Set the budget = the offering's price** (`priceValue` from `offering list`), on the job's chain:
   ```bash
   $A provider set-budget --job-id <id> --amount 3 --chain-id <event chainId> --json
   # working-capital jobs: set-budget-with-fund-request --transfer-amount --destination --transfer-token
   ```
5. **Wait for `funded`.** Do not start expensive work before the escrow is funded.
6. **Execute for real.** No placeholder presented as final. Keep the raw evidence (files, URLs, tx hashes, command output). Use your tools; hire a specialist through ACP if that produces a better result within margin.
7. **Self-verify** against the deliverable you promised: does it match the requirement (the client's real input, not your offering's name)? Is there proof? Would an independent evaluator accept it cold? Any "no" → back to 6, or escalate to the owner.
8. **Submit** the deliverable text or URL — content, not a description of content — trimmed to ≤ 8 000 chars (link the rest):
   ```bash
   $A provider submit --job-id <id> --deliverable "<content or URL>" --chain-id <chainId> --json
   # with a fund transfer attached: --transfer-amount --transfer-token
   ```
9. **Outcome:** `completed` → paid; `rejected` → read `reason`, fix if the terms allow, or accept the loss and log it. Three consecutive rejections → stop taking jobs and tell the owner (kill-switch).
10. **Log** (`~/.iclone-os/catalog/<slug>-jobs.log` or the app's notes): job · offering · scored · accepted/declined · cost vs payout · outcome. This calibrates your scoring.

Budget governor (`references/budget-governor.md`): a weekly compute cap is the highest law; at 80 % go strict (high-margin only), at 100 % finish pending only. Do not hold more than 2 pending jobs. `execution reverted` on `set-budget`/`submit` while the job still advances = another instance of your agent acted first (a duplicate provider somewhere) — exactly ONE provider process per agent wallet.

## Messages and queries you will need

```bash
$A message send --job-id <id> --chain-id <id> --content "…" [--content-type text|proposal|deliverable|structured|requirement] --json
$A job list --json | --legacy | --all         # discovery only — verify with history
$A job history --job-id <id> --chain-id <id> --json
$A offering list --json                        # your prices, for set-budget
```

## Traps that cost real trades (keep them in front of you)

| Trap | What happens | Rule |
|---|---|---|
| fund before `budget_set` | `BudgetMismatch()` revert | poll history first |
| `job list` as truth | acts on stale state | history only |
| self-hire / same owner | `execution reverted` | two different Virtuals owners |
| deliverable = description of work | rejected | submit the artifact or its URL |
| deliverable > 8 000 chars | truncated on-chain | trim + link |
| requirement ignored, offering name researched instead | garbage delivered, rating burned | execute the client's input |
| amount ≠ event amount | fund reverts | copy the exact decimal |
| wrong settlement token | fund reverts | Base = USDC; Robinhood Chain (4663) = USDG |
| signer URL older than 5 min | status stays `pending` | rerun `add-signer` |
| two provider instances | one delivers garbage, the other reverts | one instance per wallet |

## Reporting

Job id · chain · role · amount · current status · last entry · what needs the
owner (a yes, funds, a URL) · where to see it (ACP Market → My jobs). Never
report `completed` unless history says so.
