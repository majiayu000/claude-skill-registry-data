---
name: ci-doctor
description: >-
  Diagnose CI health and, when needed, benchmark a config change side by side —
  without re-deriving either from scratch each time. Use when the operator asks
  "why is CI slow", "diagnose our CI", "is our CI healthy", "what's the
  bottleneck", or wants to compare wall-clock across two or more `runs-on` (or
  other config) variants — e.g. GitHub-hosted vs. a paid runner vendor, or a
  small vs. large runner tier. Not for writing new workflows from scratch, not
  for non-GitHub-Actions CI systems, not for security/posture audits (a
  separate free skill, `ci-secure`, from the same catalog, covers that).
---

# ci-doctor — reusable CI diagnosis + benchmark harness

Born from GH-161: diagnosing and benchmarking this repo's CI was ad-hoc every
time — the same dispatch/poll/watch/tabulate loop hand-written three separate
times in one session, and one silent trap (a push-triggered run classified
into a "fast lane" that skips the real test suite, reporting a meaningless
wall-clock number) that nothing prevented from recurring.

## What this is NOT

Diagnosis is a solved problem — don't rebuild it. StarSling's free,
open-source `ci-speedup` skill already measures the real wall-clock critical
path from run history and identifies the dominant bottleneck step, with an
internal adversarial-verification gate. Verified against this repo in GH-152:
its finding (a specific test step eating ~89% of a job's wall time) matched
independent manual measurement exactly. `ci-doctor` leans on it rather than
duplicating that engineering.

## Step 1 — always diagnose first

```bash
npx skills use "https://github.com/starslingdev/skills" --skill "ci-speedup"
```

Follow the generated instructions verbatim (they are self-contained — repo
target confirmation, the `gh`-auth gate, the scan, and a plain-English close).
This answers "why is CI slow" for the common case: a single repo's existing
run history, no new runs needed.

## Step 2 — only if a side-by-side comparison is needed

`ci-speedup` analyzes *existing* history — it does not orchestrate *new*
comparison runs across config variants. That's the one real gap this skill
fills, with [`benchmark-runners.sh`](benchmark-runners.sh):

```bash
skills/4-occasional/ci-doctor/benchmark-runners.sh \
  --repo OWNER/REPO --workflow .github/workflows/ci.yml --base development \
  --find 'runs-on: ubuntu-latest' \
  --variant 'github-hosted=runs-on: ubuntu-latest' \
  --variant 'bigger-runner=runs-on: ubuntu-latest-8-cores' \
  --job 'the job display name shown in the Actions UI'
```

Run from inside a local clone of the target repo (plain `git` — branch, patch,
commit, push, dispatch; no API workarounds needed, unlike a read-only
diagnostic session that must avoid touching someone else's checkout).

**Always forces `workflow_dispatch`, never a push/PR event** — this is the
fix for the fast-lane trap above. Prints a wall-clock + conclusion table
across every named variant. Branches are deleted after each run unless
`--keep-branches` is passed; nothing is ever merged automatically.

## Optional: a paid runner vendor is one more --variant, never a dependency

This skill has **zero** vendor-specific code. `--variant` takes any
`runs-on` value verbatim — a bigger GitHub-hosted runner, a self-hosted
label, or (as one option among many, and the one this project was born
testing — see GH-152) a managed vendor like StarSling, whose sized tiers
(`starsling-ubuntu-24.04-2/-8/-16/...`, see docs.starsling.dev) are just
another string to pass in. **Nothing here requires an account with, a
GitHub App install for, or knowledge of any specific vendor.** GitHub-hosted
runners alone are a fully supported, first-class case — comparing against a
vendor is opt-in, not the point of the tool.

## What this does NOT do

- Does not pick a winner or auto-adopt a variant — it reports, the operator
  decides.
- Does not touch branch protection, required checks, or the target
  workflow's default `runs-on` — every change lives on a disposable
  benchmark branch.
- Does not replace `ci-secure` (security posture) or a real load-bearing
  CI/CD review — it answers "how slow, and why", nothing else.
