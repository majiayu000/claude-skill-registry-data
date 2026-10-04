---
name: ratchet-ops
description: Use when a policy-check ratchet row is failing, when triaging a blocking config-check regression, or when an improvement just shipped and needs a matching enforcement check landed in the same change (the Ledger-closure rule) - covers triage classification, the narrowest-control ladder for a noisy or contested row, and the counter-function contract for authoring a new row
---

# Ratchet Ops

A config-ratchet lane converts "someone remembered to run a check" into "a regression cannot
ship silently." This skill covers both directions: **remediating** a failing row and
**authoring** a new one.

## 30-Second Model

```
a policy-check runner --tier 3       # the engine: policy-check rows + hook-contract rows + INFO rows
  ^ a nightly timer runs it with --json --file-issues
  v writes a ratchet-run snapshot file
a session-start hook reads the snapshot -> "[Ratchet] FAIL: <ids>" (silent when green)
--file-issues (timer-only) files ONE deduped low-priority issue per failing check
```

Three check classes — do not confuse them:

| Class | Fails the blocking tier? | Examples |
| --- | --- | --- |
| policy-check row (`id\|op\|threshold\|counter-fn\|desc`) | YES | model-pin, fleet-rot, deferred-dialect, skill-descriptions-budget |
| hook-contract row (a declared-header walk over hook scripts) | YES | a hook-contract validator checking a `continueOnBlock`-style declared behavior |
| INFO rows (never fail, signal only) | NO | context-floor, orphan-skill, closure-gate, agent-dispatch-census, guard-installs, zero-invocation counters |

## Triage Procedure

1. **Read the snapshot first** — do not re-run blind. Load the JSON snapshot your runner writes
   and print every row where `level == "error"` before touching anything.
2. **Reproduce one row live** (fresh evidence, the snapshot may be a day old): invoke the
   policy-check runner's blocking tier directly, in quiet mode, and capture its exit code.
3. **Route via your project's own row runbook**, if one exists — a doc mapping each row id to
   what it asserts, where its counter function lives, the fix pattern, and known traps.
4. **Classify the failure** before editing anything:
   - *Real regression* (a rewrite dropped a key, a reference went stale) -> fix the artifact.
   - *Pre-existing debt the row was landed against* (a documented, expected-non-zero baseline) ->
     work the backlog down or confirm it matches the documented expected state; do NOT "fix" by
     narrowing the detector.
   - *Environment artifact* (a stale checkout, a missing local path) -> re-run from the primary
     checkout before concluding anything.
5. **Verify**: re-run step 2, paste the exit code. A fix without the pasted exit code is not done.
6. **Close the loop**: if the timer filed an issue for the row, close it with the commit ref.

## Narrowest-Control Ladder (failing or noisy row)

Applies once step 4 above classifies a row as pre-existing debt or a contested check, not a real
regression. Work the ladder top-down; stop at the first rung that actually resolves the row. Each
step is preceded by an **explain step**: read the row's own documented rationale (a checks-log,
CONTRIBUTING doc, or comment naming the incident it exists to catch) before touching it — "only
after you understand it should you change it."

1. **Fix the regression** — the default. If the row is asserting something real and currently
   false, make it true.
2. **`KNOWN_GAPS`-style exemption** — a documented, visible carve-out array beside the counter
   function for a genuine exception the row correctly flags but that a separate, deliberate
   decision defers. Visible in the row's own output, never hidden.
3. **Demote blocking -> INFO** — the row keeps measuring and reporting, it just stops failing
   the blocking tier. Reserved for a row whose signal is still useful but whose current baseline
   makes blocking premature.
4. **Delete the row** — last resort. Requires an inverted Ledger-closure rationale: state why the
   incident class the row was landed against can no longer recur (not just "it's noisy now").

Do not skip rungs — narrowing a detector or deleting a row because it is inconvenient, without
working the earlier steps first, is the same anti-pattern the Ledger-closure rule exists to
prevent (a row deleted without cause can regress silently, same as a row never landed).

## Authoring a New Row (Ledger-Closure Rule)

Any improvement recorded as *shipped* MUST, in the same change, add an enforcement artifact that
would fail if it regressed. Pick the mechanism by what the improvement is:

| Improvement shape | Mechanism |
| --- | --- |
| A config key a hook depends on | a declared-requirement header in the hook script (e.g. `# requires-settings: <key>=<value>`) |
| A hook that must actually fire | a declared liveness header (e.g. `# liveness: event=<E> matcher=<regex> window=<Nd>`), or an inline liveness marker for settings-only hooks |
| Any greppable/countable invariant in the repo | a policy-check row + a matching counter function |
| A count worth watching but not gating (operator-judgment calls) | an INFO row — emits data, never fails |

**Counter-function contract** (every counter function should follow it):
- Echoes a single number; **echoes `0` and never aborts on a read failure** (a broken counter
  must not take the lane down).
- Exclusions live in a bash array RIGHT BESIDE the function (a `KNOWN_GAPS`-style array) — data
  beside code, never a separate config file. A first-run genuine offender the change cannot fix
  gets a documented array entry + its own triage issue, not a fix-everything-first blocker.
- New rows landing against pre-existing debt are EXPECTED to fail on a fresh tree — say so in the
  row's documentation paragraph, mirroring the pattern used for other known pre-existing-debt
  rows.
- Day-one grace: liveness-style checks bound their window to `max(cutoff, artifact mtime)` so a
  just-landed hook reads "no data yet," not FAIL.

**Blocking vs INFO decision**: gate it only when a failure is unambiguously wrong (a dropped key,
a banned token, a budget breach). If the right response is an operator decision
(archive-vs-keep, dead-weight-vs-break-glass), it is an INFO row — a blocking row there trains
people to silence the lane.

**Document the row** in your project's checks-documentation file: one paragraph — what it
asserts, the root-cause incident, exemptions and why.

## NEVER

| Never | Why |
| --- | --- |
| Narrow a detector to make a row pass | Hides a real baseline; the Ledger-closure rule exists because silent drops have shipped before in practice |
| Delete a load-bearing registration to fix a quality/budget row | It can break a dependent system that hard-fails without it — check for downstream dependents first |
| Run the runner's interactive-file-issues flag interactively | Timer-only mode; interactive runs would double-file issues |
| Trim an auto-triggered check's description/trigger text to meet a budget | The description IS its match surface; trim explicit-only entries instead |
| Trim a vendored-external item's description | A re-vendor operation wipes the trim; exclude vendored content from the blocking row and track it separately |
| Treat INFO rows or a "STALE" ratchet status as failures | STALE means the timer has not run recently — fix the timer, not the rows |
| Audit detection scripts by grepping `exit 1` | Lexical audits false-positive on arg-parse and markdown-mode exits; verify by executing under a broken precondition |

## Verification

Done means: the policy-check runner's blocking tier invoked directly in quiet mode, with the
exit code pasted as `0` (or the specific row's counter pasted at its documented expected value),
plus the checks-documentation paragraph for any new row.
