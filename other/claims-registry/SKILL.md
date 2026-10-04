---
name: claims-registry
description: How a number becomes publishable in this repository — the claims registry, its baselines, thresholds and reproduction command. Use whenever a change would put a number into docs/design, a README, a commit message or a pull request description, whenever a benchmark is added or changed, and whenever a claim goes red.
---

# Claims

A number without a named baseline, a published workload and a one-command
reproduction is an anecdote. `claims/README.md`, and layer 7 of
`docs/design/proving-ground.html`.

Every number in `docs/design/` has an entry in `claims/`. The documents render
from the registry rather than restating it, so that a claim which stops holding
cannot quietly persist in prose.

## Writing an entry

Copy an existing file — `claims/0001-ring-submit-latency.toml` is the reference
shape. What each part is for:

- `status` — `pending` (registered before it is measurable), `tracked` (recorded,
  does not gate), `gating` (a regression fails the build). Muting a claim is a
  status change in a reviewable diff, never a comment in CI config.
- `[baseline]` — versioned with the claim, and configured by somebody trying to
  win. This is what stops a tuned-Linux comparison decaying into a stock-Linux
  comparison as the baseline ages.
- `[workload]` — a path in `bench/`, plus repeat and batch counts. Not a
  description.
- `[metrics]` — distributions, not summaries. Keep the full histogram; a mean
  computed at collection time destroys what cannot be recovered, and
  under-reports exactly the stalls this architecture exists to eliminate.
  Report `instructions_per_op` and `joules_per_op` alongside nanoseconds: they
  survive a hardware change and are far less noisy.
- `[hardware]` — the runner class. Shared cloud instances cannot produce
  defensible tail latency, so a claim measured on one is not a claim.
- `[reproduce]` — `cargo xtask claim <name>`, and it has to actually run.
- `[diagnosis]` — what a red result probably means, written while the system is
  understood rather than at 2 a.m. when it is not.

## Registering before measuring

Registering a claim at `status = "pending"`, with the threshold written down
before there is a number, is the point. It puts the target on record before
anybody can be tempted by what the machine happens to produce. Do this at the
milestone where the work is planned, not when the measurement lands.

## When a claim goes red

Regression detection is change-point, not threshold — thresholds either miss
real regressions or fire until everyone mutes them. So a red claim means the
distribution moved, and the first move is to read `[diagnosis]`, not to adjust
the threshold. Changing a threshold to make a build pass is the single change
this registry exists to make visible.

A toolchain bump invalidates every claim and requires a full re-run.
`rust-toolchain.toml` says so; treat a toolchain change and a measurement change
as the same kind of event.
