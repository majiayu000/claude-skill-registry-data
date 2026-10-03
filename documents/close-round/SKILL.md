---
name: close-round
description: Spawn docs-updater to close the current round, then check whether a strategy review should fire.
invocation: /close-round
---

# /close-round

## Step 0 — Spec-status drift gate (added 2026-07-25 after the tracker audit)

Before anything else, grep every spec for unflipped statuses:

```
grep -rE '^\*\*?Status:?\*?\*?.*(pending|in review|PR #[0-9]+)' .astroray_plan/packages/
```

For each hit naming a PR, check `gh pr view <N> --json state`. If the PR is
MERGED or CLOSED and the spec still reads pending/in-review, **the closeout
fails until the spec is flipped** to `done (PR #N, date — headline numbers)`
(or superseded/held as appropriate). This gate exists because the spec-flip
step was skipped in two consecutive rounds (2026-07-23/24), causing 30 specs
of drift on the owner's tracker (fixed in `07ac576`). The pr-merger also
flips specs at merge time; this gate is the backstop.

## Step 1 — Spawn docs-updater

Spawn the `docs-updater` agent. Pass it the list of PRs merged since the
last STATUS.md update. Wait for it to return and confirm the doc PR is
open or merged.

## Step 2 — Check for strategy review trigger

After docs-updater returns, check whether any of these conditions are met:

| Condition | Action |
|---|---|
| 3 or more packages have deferred targets (measurement-vs-spec divergence events) since the last architect review | Spawn architect in `state+refine` mode |
| This is the 3rd round since the last architect review | Spawn architect in `state+refine` mode |
| Every round | Spawn architect in `state+refine` mode (light pass: current-state surface + one question) |

A "light" state+refine pass is: read the current render output + status,
ask one short question, accept "no changes needed" as a complete answer.

## Step 3 — Report to user

After docs-updater and (if triggered) the architect return:

- Confirm the doc PR is open/merged
- Summarise what the architect decided (if it ran)
- State what the next dispatch will pick up (top of NEXT_STAGE_REPORT.md §2)
