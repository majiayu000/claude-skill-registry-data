---
name: ci-single-check-validation
description: Use when exactly one CI check on a pull request is red while the rest are green — a code-quality or code-scanning check, one Playwright shard, one lint or mutation job — and the failure looks transient (timeout, plugin crash, post-analysis upload error) rather than caused by the diff. Covers how to prove that locally before escalating or asking for a re-run.
---

# CI Single-Check Validation

## Profile keys consumed

- `ci.required_checks`
- `make.lint`
- `make.test_unit_client`
- `make.test_unit_server`
- `make.test_e2e`
- `make.test_mutation`

## Overview

One red check among greens is ambiguous: it can be a real finding in the diff, pre-existing debt the
check happens to surface, or an infrastructure failure that never looked at the code. Running the
same gate locally and attributing every finding to a file settles which, in minutes, with evidence.

## When to use

- A single check in `ci.required_checks` fails while the rest of the pipeline is green.
- The failure text reads like infrastructure — timeout, upload failure, plugin crash, exit code from
  a wrapper rather than from the tool.
- A decision is needed on whether to fix, re-run, or file an infrastructure issue.
- Not for: a failure repeating across several branches or pull requests, which is an infrastructure
  incident and belongs in the
  [ci-infrastructure-failure-diagnosis skill](../ci-infrastructure-failure-diagnosis/SKILL.md).

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — the aggregate mapped by `make.lint` (the one the static workflow runs), the split
  unit targets `make.test_unit_client` / `make.test_unit_server`, `make.test_e2e`, and
  `make.test_mutation`; a parallel lint-aggregate target runs the same lint targets concurrently.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — same mapped targets
  plus the parallel lint aggregate; a host run needs the host execution mode and a host install
  through the project package manager.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial — same
  `make.lint`, `make.test_e2e`, and `make.test_mutation`, but there is a single unit target
  (`make.test_unit_client`, with `make.test_unit_server` `null`), and there is no parallel
  lint-aggregate target.

## Procedure

1. Identify the exact tool behind the check, not the check's display name. A cloud check name maps
   to a plugin set; a shard name maps to one suite and one project.
2. Run the full local equivalent — the aggregate, not a narrowed invocation. Narrowing to the
   changed files is what makes a local run disagree with CI for the wrong reason. Resolve each one
   through its profile key and skip with a recorded note when the key maps to `null`:

   ```bash # profile-example
   make lint
   make test-e2e
   make test-mutation
   ```

3. Attribute every finding to a file and compare against the diff:

   ```bash
   git diff --name-only origin/main...HEAD
   ```

4. Read the result off the table below, and record the evidence — command, exit code, finding count,
   and the attribution — in the pull-request thread. That record is what makes a re-run request or
   an infrastructure issue actionable rather than a guess.

| Local outcome              | Meaning                                                    |
| -------------------------- | ---------------------------------------------------------- |
| Clean run                  | The failure is environmental; gather logs and re-run       |
| Findings in changed files  | A real finding; fix the cause before asking for anything   |
| Findings only in untouched | Pre-existing debt the run surfaced; fix or file separately |

## Escalation

Escalate to the
[ci-infrastructure-failure-diagnosis skill](../ci-infrastructure-failure-diagnosis/SKILL.md) when
the same check fails again on a fresh run with no code change, when it fails on other branches too,
or when the local equivalent also fails but only under the container path. File with both sides of
the evidence: the local command and exit code, and the runner's step name, exit code, and error
text.

## Common mistakes

- Concluding "transient" without running the gate — the local run is the proof, not the hypothesis.
- Running a narrowed command (one spec, one rule) and calling a clean result a clean gate.
- Blaming infrastructure before attributing findings to files — most single-check reds are real.
- Re-running until green and merging; the check is still telling you something.
- Making the check pass by lowering its threshold, narrowing its scope, or excluding the file it
  flagged — fix what it reports instead.
