---
name: host-stack-infrastructure
description: Use when adding or changing how a browser or memory-leak suite is executed — a host-built export instead of the Docker prod stack, a new executor mode, or a Makefile switch. Triggers on "run e2e without Docker", unexplained visual-baseline diffs, an unreachable Docker daemon, or any proposal to key test behaviour off the ambient `CI` variable.
---

# Host Stack Infrastructure

## Profile keys consumed

- `make.test_e2e`
- `make.test_visual`
- `make.test_memory_leak`
- `make.start_prod`
- `capabilities.visual_testing`

Every suite runs through the profile's `make` target map; skip a dependent
step with a recorded note when its key maps to `null`, and skip the
baseline-drift reasoning entirely when `capabilities.visual_testing` is
`false`. The browser-install and baseline-update targets have no logical
key — name them by purpose and resolve them in the repository's Makefile.

## Overview

A new execution environment gets its own explicit switch. Never derive one from an ambient variable
and never overload an existing one: visual baselines are environment-bound, so a silent mode change
moves a suite off the containers its snapshots came from and produces diffs that are pure
environment drift.

## When to use

- Adding a way to run the browser suites without a Docker daemon.
- Introducing or renaming a Makefile switch that selects an executor or a stack.
- Wiring a workflow to a second execution context.
- Investigating visual diffs that appear locally but not in the pipeline, or the reverse.
- Not for: picking which suite to run, or triaging an ordinary spec failure.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate
  CI target): partial — the same principle, spelled `ENV ?= prod` with an `ENV=dev` branch on the
  targets mapped by `make.test_e2e` / `make.test_visual`; dev-mode snapshots live in
  `tests/visual/__snapshots__-dev/` under a separate `chromium-dev` project so they can never
  overwrite the production baselines produced against `make.start_prod`.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — `HOST_STACK`
  (default `0`, accepting `1`/`true`/`TRUE`) drives a host-stack shell script; `EXEC_MODE`
  (`container` default, `host` opt-in) is a second, independent switch.
- **Component-library shape** (Storybook-first, no bootable app, published package): no — every
  suite runs in Docker Compose; no host mode exists.

## Core pattern

The ambient `CI` variable is exported into every step by the runner, so a switch derived from it is
on in the pipeline whether or not anyone asked. Two separate concerns each get their own name — the
spellings below are the Next.js shape's:

```bash # profile-example
make test-e2e                        # make.test_e2e — default: the Docker prod stack, everywhere
HOST_STACK=1 make test-e2e           # explicit opt-in, per invocation, no daemon needed
HOST_STACK=1 make playwright-install # fetch the browsers the host mode needs (no logical key)
```

Design rules that make the switch safe:

- **One switch, one concern.** Selecting the executor for lint/test tooling and selecting the stack
  the browser suites hit are different questions; a single flag answering both is ambiguous.
- **Enum, not boolean, when there are named alternatives**, and an unrecognised value is a hard
  `$(error)`. An escape hatch that can be mistyped into silence is the same defect as deriving it
  from `CI`.
- **Accept the truthy spellings** (`1`, `true`, `TRUE`) so a workflow writing `true` does not
  silently take the default path.
- **Refuse, do not degrade.** Baseline-writing targets — the repository's visual-baseline update
  target — stay unavailable in the alternate mode. Host font rasterisation differs from the pinned
  Playwright image, so a snapshot update run there would rewrite every baseline and red the
  container-run gate behind `make.test_visual`; the target exits with an explanatory error before
  its prerequisite builds anything.
- **Turn an unreachable daemon into the hint.** The first target that touches Docker on every
  browser path — including the memory-leak lane mapped by `make.test_memory_leak` — prints the exact
  opt-in command instead of a raw connection error.

## Quick reference

- The container image stays the baseline source of truth; the alternate mode is opt-in only.
- Pin any value the container build bakes in (a served URL, a port) into the alternate build too, or
  specs asserting on it diverge between modes.
- Leave unrelated environment variables alone in the alternate branch — changing one can un-skip
  specs that the default mode skips.
- Exercise both modes locally before proposing the change.

## Common mistakes

- Deriving a mode from `CI` — the runner sets it everywhere, so the pipeline silently takes the
  alternate path.
- Reusing an executor switch to also mean "different stack" — split them.
- Allowing snapshot updates in the alternate mode — the resulting baselines fail the gate that owns
  them.
- Accepting only `1` and treating `true` as the default — a workflow spelling it that way gets the
  wrong stack with no signal.
