---
name: qlty-transient-build-error
description: >-
  Use when a Qlty check reports state failure with "Build errored. Check the log for more
  information." while its inline analysis comment reports no findings or "All good", every other
  check is green, and the run duration is near zero — the passing-analysis / failing-status mismatch
  that suggests a Qlty Cloud outage rather than a code defect.
---

# Qlty transient cloud build error

## Profile keys consumed

- `make.format`
- `ci.required_checks`

## Overview

Qlty Cloud sometimes fails to complete its pipeline and reports a red status while the inline
analysis comment shows a clean run. That mismatch is a candidate signal for an infrastructure
failure — but it is not proof, because a linter that crashes at rule-load time produces the same
status text. The build log is what separates them, and a retry is a single, evidence-backed attempt,
never a habit.

## When to use

- Qlty status is `failure` with `Build errored. Check the log for more information.`
- Qlty's inline analysis comment shows no findings, and the reported duration is near zero.
- Every other check listed in `ci.required_checks` on the same head commit is green.
- Not for: a red Qlty status whose build log contains linter stderr — that is a runtime-version
  mismatch and is fixed by pinning, not by retrying.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): partial — `.qlty/qlty.toml` is present but untracked, and the only Makefile entry points
  are a qlty formatting target and the target mapped by `make.format` that calls it; the cloud check
  behaves as described where it is enabled.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — `.qlty/qlty.toml` is
  tracked and, per its own header, drives both the Qlty CLI and Qlty Cloud.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes —
  `.qlty/qlty.toml` is tracked (via a `.gitignore` negation) and drives the same cloud check.

## Telling the two failure modes apart

| Evidence in the cloud build log | Verdict          | Action                      |
| ------------------------------- | ---------------- | --------------------------- |
| Linter stderr plus a stack      | Real crash       | Fix the cause (pin runtime) |
| Findings listed                 | Real findings    | Fix the code                |
| No tool output, pipeline aborts | Candidate outage | One retry, then escalate    |
| Log unavailable                 | Unknown          | Get the log; do not guess   |

Never infer the verdict from the status text alone: it is byte-identical across all four rows.

## Re-triggering once

The cloud analysis is driven by a push, so a fresh commit is the trigger. The commit header must
still satisfy commitlint, which requires `type(#N): subject` with a real task number in all three
shapes — a bare "retrigger" header is rejected by the commit-msg hook, and the fix is to write a
conforming header, not to bypass the hook.

```bash
git commit --allow-empty -m 'ci(#N): re-run the cloud analysis build'
git push
```

Cap this at one attempt. If the second run reports the same status, the cause is not transient: read
the log, and treat what it shows as the defect.

## Common mistakes

- Reading a red status as broken code before opening the inline comment and the log.
- Writing code changes to "fix" an aborted pipeline — there is nothing in the diff to fix.
- Repeating the empty-commit retry — a repeated identical failure is evidence against the outage
  hypothesis, not a reason to push again.
- Waiting indefinitely for self-correction — a genuinely aborted run needs a new trigger.
