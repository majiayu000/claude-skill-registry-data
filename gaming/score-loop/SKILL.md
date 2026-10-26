---
name: score-loop
description: Run an unattended experiment loop that hill-climbs one rerunnable numeric score — local grader-mirroring harness, one hypothesis per commit, keep only gains beyond the noise margin, auto-revert the rest, append-only results ledger; stops on budget, deadline or plateau. Use for "improve this score", "hill-climb a metric", "optimize until plateau/deadline", or "resume" / "status" / "summary" of a score loop.
argument-hint: "[setup | resume | status | summary]"
---

You run **one metric** up (or down) unattended, one hypothesis per commit, and log every experiment to `skilleddocs/experiments.md`. Only for a score you can rerun and that is a number; an unrepeatable or subjective score → say so and stop.

Commands: `setup` (default; also when `experiments.md` has no setup header), `resume`, `status`, `summary`.

## 1. Setup (confirmed once)

1. Fill the header below from the request and the repo; ask only for what's missing. Create the loop branch off the current HEAD.
2. **Harness first.** No local harness that mirrors the grader → write one and commit it before experiment 1. It runs a **correctness check** (pass/fail) and the score **N times**, and prints the median. It must defeat caching/memoisation: fresh inputs or a fresh process per timed run, and the correctness check never warms the timed call. A near-zero or implausible score is `invalid` unless correctness proves otherwise.
3. **Noise margin**: run the harness once on the baseline; propose margin = (max − min of its N runs) / baseline median, as a %.
4. **Calibrate** (after the gate): one official submission of the baseline; record the local–official gap. A gap wider than the margin (as a % of the baseline) → fix the harness before experiment 1. No official grader → skip and write `calibration: none (no official grader)`.
5. Freeze time = deadline − lead, lead = max(10% of remaining, min(30 min, 50% of remaining)) (≥5h left: 10%; 1-5h: 30 min; <1h: half the remaining time); no deadline → no freeze. One experiment (one harness run, as timed on the baseline) plus the calibration must fit before freeze; otherwise refuse, say so, and stop.
6. Gate: show the filled header, how the score could be gamed and how the harness blocks it (proxy-metric gaming: the score improves without the real goal improving, e.g. work moved outside the measured region or special-cased fixed inputs; the correctness check, fresh or hold-out inputs and timing the whole call guard it), and each outward action (the calibration submission, the quota, any paid step). One explicit yes covers this setup; anything vaguer is a no. Then write the header, run the calibration, and go unattended.

```
# Score loop: <slug>
- metric: <name>, <higher|lower> is better
- grader: <official grader cmd/URL, or none>
- harness: <local cmd>  (correctness check + median of N=<n>)
- submission: <path or cmd>
- quota: <official submissions pre-approved, or 0 = ask each time>
- spend cap: <amount, or 0 = no paid steps>
- deadline: <local datetime, or none>  freeze: <datetime>
- noise margin: <p>% of best  (spread <s> / baseline median <m>, from <n> runs: <values>)
- calibration: local <x> vs official <y>
- K: 5   parallel: 1
- branch: <prefix>score-loop/<slug>   resume: /score-loop resume

## Ledger
| n | time | commit | hypothesis | local median | official | keep/revert | note |
|---|---|---|---|---|---|---|---|

## Next ideas
- <idea>

## Tried
- <idea>: <why it failed>
```

`<prefix>` is the user's branch prefix with its slash (from their `CLAUDE.md`), or empty. Commit `experiments.md` or leave it untracked per [TRACKING.md](../handoff-auto/TRACKING.md).

## 2. Loop

Per experiment:

1. Pick the most promising idea from **Next ideas**; the list empty → add 3 from what the ledger shows so far and Tried (not repeating Tried ones).
2. Make one change for that one hypothesis; commit `exp <n>: <hypothesis>`.
3. Run the harness (local runs are ungated).
4. Decide, then append one ledger row:
   - Correctness check fails → `git revert --no-edit <sha>`, `invalid`; not counted toward K.
   - Gain = the median's relative improvement over the best median (direction-aware); m = the margin.
   - Gain > m → `keep`; it is the new best.
   - m/2 < gain ≤ m → **borderline**: rerun both now, interleaved so drift hits both alike: N single runs each in ABBA order (best, candidate, candidate, best, repeated), which cancels steady drift exactly (harness at N=1; correctness already passed), and take each fresh median. Candidate's fresh median beats the best's fresh median by more than m/2 → `keep`; else `git revert --no-edit <sha>`, `noise`. The fresh medians only decide this row; the best stays unless the candidate is kept (then its fresh median is the new best). Note: `borderline: fresh best <b> (was <best>), fresh cand <c> (was <cand>), gain <g>% vs m/2 <h>%`.
   - 0 ≤ gain ≤ m/2 → `git revert --no-edit <sha>`, `noise`.
   - Worse (gain < 0) → `git revert --no-edit <sha>`, `revert`.
5. A failed idea moves from Next ideas to Tried with one line why. The user may append ideas at any time; read the list fresh each experiment.

Ledger rows are append-only: reverted rows stay, a correction is a new row.

**Parallel** (`parallel: N > 1`, opt-in): spawn N subagents, each with its own worktree and branch off the loop branch and one idea. Each runs the harness and returns its median and correctness. One row per variant; merge only the best qualifying variant into the loop branch, then remove the worktrees. Graders that share the machine get noisier: say so at setup.

## 3. Outward actions

- **Official submission**: only inside the setup quota; past it, show the exact submission and wait for an explicit yes. Record the result in the row's `official` column.
- **Paid** (submission, compute, API): through [spend-gate](../spend-gate/SKILL.md), which takes its own yes per action; record the cost in the row's `note`. The spend cap is a ceiling, not approval.
- Push or merge: only on an explicit yes to that push or merge.

## 4. Stops

Check before each experiment:

- **Budget**: the next experiment needs a paid step that would take total spend (sum of costs in the ledger) past the spend cap. Cap 0 → any paid step stops the loop; unpaid experiments never hit this stop.
- **Deadline**: freeze time reached → no new experiments; rerun the harness on the best commit, show the final submission and submit on a yes, then §5.
- **Plateau**: K consecutive experiments without a `keep` (`invalid` rows don't count).

On any stop: §5, then report why it stopped.

**Context degrading** (smartzone warning, or the ledger no longer fits your head): finish or revert the current experiment, then call `handoff-auto` with "continue the score loop from skilleddocs/experiments.md: /score-loop resume", and stop.

## 5. Summary

From the ledger only, no reruns: kept commits ranked by relative gain (gain / best before them), not absolute, reverted ideas with why, `noise` rows, `invalid` rows, best local and official score. Append it to `experiments.md` under `## Summary <date>` and print it. Ablation reruns only when the user asks.

## Commands

- `resume`: read the header and ledger, switch to the loop branch. HEAD is an `exp <n>:` commit with no ledger row for n → evaluate it as that experiment. Recheck the stops, then §2. No new setup gate.
- `status` (read-only): best (commit, local, official), experiment count (kept / noise / revert / invalid), time to freeze and deadline, spend and quota left, next idea.
- `summary`: §5 now.

Backlog of issues instead of one metric → that is `meta-orchestrator`, not this skill; never invoke it from here. Live session status → `sitrep`.
