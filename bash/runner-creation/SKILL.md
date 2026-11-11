---
name: runner-creation
description: Creates or hardens an unattended runner, the wrapper, pre-flight gate, permission profile, ledger, watchdog, and caps around a headless agent run. Use when asked to "schedule this", "run it every N hours", "make a headless sweep", or "why does the runner waste tokens", or when a runner double-launches, runs idle, dies silently, or invents data. Not for one-off scripts or interactive sessions.
argument-hint: "[job name] [create | harden]"
---

# Runner creation

Turn "run this unattended" into a runner whose cheap decisions are made by scripts before a model starts, whose outcome is derived from facts, and whose failures are visible. A runner is any agent CLI run non-interactively with nobody watching: a scheduled job or a batch or eval sweep. This file names no vendor; the agent CLI, scheduler, ledger store, and permission mechanism come from the project settings. When the settings lack the agent CLI or trigger line, read [references/platforms.md](references/platforms.md) for the per-platform form before asking.

## Inputs

- **The plan.** A new runner enters through the plan stage, so the plan file, `.claude/shipyard/plans/<branch>.md` with `/` in the branch name written as `-`, usually answers the seven questions below. Ask what it lacks in one grill round (H2), each question with a recommended answer so "yes" accepts it. Run unattended, list the gaps as open questions in the report and use the defaults in [references/overlay-example.md](references/overlay-example.md).
  1. The work unit, and the fact that proves one unit done (a row, a file, a receipt) that a script can read.
  2. The trigger and host: exactly one of OS scheduler, desktop app task, hosted routine, or CI cron, and whether the host must be awake or an app open.
  3. Dependencies to pre-check: browser, network, credentials, stop flag, repo freshness.
  4. Caps: turns, spend, and wall-clock per run; daily and per-target caps; subagent budget; yield threshold.
  5. Side effects: which are irreversible, their idempotency keys, and which writes never happen without a fact.
  6. The agent CLI, its auth mode, model and effort, and how it reports a machine-readable result.
  7. The needs-you channel and the age at which an unanswered item escalates.
- **Project settings.** On every invocation, read `.claude/shipyard/runner-creation.md` in the project root if it exists; its values win over anything inferred. It names the job, the agent CLI command and result format, the scheduler, the ledger store and path, the lock, the dependency checks, the caps, the permission profile, and the escalation channel. Its shape and defaults are in [references/overlay-example.md](references/overlay-example.md).

## Output

Files written into the project for the user to commit, filled from the templates named here, plus a report in the shape of [references/acceptance.md](references/acceptance.md) saying which gates passed.

| Piece | What it does | Template |
|---|---|---|
| launch wrapper | lease, pre-flight gate, idle row or headless run under caps, outcome from state, ledger row, dead-man pings | [references/wrapper.md](references/wrapper.md) |
| permission profile | deny by default; allows committed scripts only; proven by a dry run with 0 denials | wrapper.md |
| prompt file | idle fast path first, stable prefix, state read from scripts, no background work | wrapper.md |
| ledger and needs-you table | one row per launch with store-side timestamps, status, cost, units, `lesson` | [references/ledger.md](references/ledger.md) |
| watchdog and policies | reaper, bounded retries with quarantine, per-target cooldown, needs-you ageing, yield governor, take validator | [references/policies.md](references/policies.md) |

Ledger status is one of: `ok` (facts confirm the claimed units), `ok-flagged` (work was done, but the claim and the facts disagree, or an invariant check didn't run), `idle` (nothing takeable, no model call), `skipped` (lease held, stop flag, cap reached, or dependency down), `failed` (non-zero exit, error result, or a failed helper), `limit` (usage, billing, or auth limit message), `killed` (wall-clock deadline or reaper), `needs-check` (state couldn't be read, so no outcome can be derived).

## Rules

- **Lease before model.** The wrapper takes a lease with a TTL first and skips, never waits, when it's held: a skipped launch costs a row, a double launch costs a session and can write twice. Only the reaper breaks a stale lease.
- **Nothing to do costs nothing.** The pre-flight gate is plain script: stop flag, caps left, dependencies up, lock free, repo synced, takeable work. "Pending" means takeable: under its retry cap, not quarantined, not cooling down, not before its time. No work means an `idle` row and exit before any model call, because a launch that pays full startup to learn there's nothing to do is the commonest waste in unattended runs.
- **The model asserts; scripts decide.** Timestamps come from the store's default or the wrapper's clock, caps live in code, counts come from the fact that proves a unit done, read before and after the run. The model's result is a claim: `ok` only when the facts match it, `ok-flagged` when they don't. A cap or count the model proposes is recorded as a `lesson`, never applied.
- **A failed helper fails the run.** A non-zero exit from any committed script, or an invariant that doesn't hold, makes the row `failed` even when the model said ok.
- **Every launch leaves a trace.** The wrapper writes the row even when the agent CLI dies, and pings a dead-man switch at start and at the end, so a launcher that never ran shows up as a missing ping within the grace time.
- **One scheduler per job.** Exactly one trigger references the wrapper. A second trigger is removed before the first is enabled.
- **Commands are committed one-op scripts.** Headless runs deny anything not pre-approved, and compound or quoted shell is what gets denied, so the prompt runs committed scripts by path and the profile allows those paths only. Glue is written once, tested, and committed, not rewritten by the model each run.
- **Caps are enforced outside the prompt**, at the wrapper or runtime, and include subagents, with headroom because spend can overshoot by a response. A yield governor stops a batch when new units per token fall under the threshold.
- **Needs-you items wait for a fact.** A question only a person can answer goes to the needs-you table with its first-seen time; it's never requeued until the answer exists, and it escalates at the settings' age through the digest (H10).
- **Nothing is scheduled until the gates pass.** Enabling the schedule starts unattended spend, so it waits for the user.

## Steps

```
- [ ] 1 Read settings and plan
- [ ] 2 Fill the gaps (one round)
- [ ] 3 Generate the pieces
- [ ] 4 Dry run headless
- [ ] 5 Force the failures
- [ ] 6 Gates report (gate)
- [ ] 7 Enable and watch five runs
```

1. **Read settings and plan.** Collect the seven inputs from the plan file and the settings; list which are still open.
2. **Fill the gaps.** Ask the open ones in one grill round (H2), recommendation first, then **STOP — WAIT**. Unattended: record them as open questions and apply the defaults.
3. **Generate the pieces** from the templates, in the host's shell, with paths and caps from the settings. For an eval or batch sweep, add the take validator.
4. **Dry run headless** with the real permission profile and the real agent CLI, from the wrapper, not by hand: the result must show 0 denials and the ledger must hold the row. Fix the profile or the prompt and repeat until it does.
5. **Force the failures**, each through the wrapper: nothing takeable (expect `idle`, no model call), a second launch during the first (expect `skipped`), a kill at the deadline (expect `killed`), the CLI's simulated limit message (expect `limit` and a fail ping), a dependency down (expect `skipped` or a fail ping). Each check names its expected row before it runs, so the result can't be fitted afterwards.
6. **Gates report.** Fill the table in [references/acceptance.md](references/acceptance.md) from steps 4 and 5. **STOP — WAIT**: show it with the exact scheduler entry to be enabled and the caps it runs under, and ask the user to enable it.
7. **Enable and watch five runs.** **HUMAN TRIGGER**: the user enables the schedule. After that, report cost per productive unit after the first five runs, with the `lesson` column, as a review prompt.

Steps are agent-owned unless marked.

The generic failure classes this skill prevents, and which piece prevents each, are in [references/failures.md](references/failures.md); read it when hardening an existing runner, to map its symptom to the missing piece.

## Handoff

`next:` verify live: run the headless dry run and the forced-failure checks against the real agent CLI, then land the wrapper and the schedule through the land stage.
