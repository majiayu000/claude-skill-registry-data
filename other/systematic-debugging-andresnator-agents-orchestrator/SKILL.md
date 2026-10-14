---
name: systematic-debugging
description: "Trigger: debug, debugging, root cause, root-cause analysis, why does this fail, intermittent failure, shotgun fixes. Root-cause debugging loop: reproduce, gather evidence, one falsifiable hypothesis, minimal verified fix."
license: MIT
metadata:
  author: obra
  adapted_by: andresnator
  source: obra/superpowers
  version: "1.0.0"
  status: testing
---

# Systematic Debugging

Debug by finding the cause, not by trying fixes. One loop: reproduce → evidence → hypothesis → minimal fix. Skip a phase only when you can state why its output is already known.

## Phase 1 — Reproduce

- Get a failing reproduction before changing anything: the exact command or interaction, its full output, and the exit status.
- Shrink it to the smallest input and scope that still fails.
- If the failure is intermittent, record the observed frequency and conditions instead of pretending it is deterministic.
- No reproduction yet means the work is still investigation, not fixing.

## Phase 2 — Gather Evidence

- Read the actual error, stack trace, and logs before forming opinions; quote the relevant lines, not a paraphrase.
- Compare against a known-working state: recent diffs, a passing sibling case, another environment.
- Evidence stays boundary-safe: never dump environment variables, credentials, tokens, or full config files into output or logs. For sensitive values, log names, lengths, or shapes — not contents.
- Locate the failure boundary: the last point where state is known good and the first point where it is wrong.

## Phase 3 — One Hypothesis, Tested Minimally

- State exactly one falsifiable hypothesis: "X causes this; if true I will observe A, if false I will observe B."
- Test it with the smallest probe that can refute it (a log line, a focused test, a narrowed input) — not a speculative code change.
- Record the result before moving on. A refuted hypothesis is progress; an untested one is noise.
- After three consecutive refuted hypotheses, stop and reassess: question the layer you are looking at, widen the evidence, or surface what you know and ask the user. Do not keep guessing.

## Phase 4 — Fix the Cause Once

- Fix the verified cause, not the symptom, with one coherent change.
- Re-run the original reproduction and cite its fresh result; the fix claim needs the same evidence standard as any completion claim.
- Add a regression test when feasible; when it is not (no harness, out-of-scope infrastructure), say so explicitly.
- Revert experiment leftovers: probes, temporary logging, disabled checks.

## Anti-Patterns

- Shotgun debugging: changing several things at once and re-running to "see if it helps."
- Stacking a second speculative fix on top of an unverified first one.
- Silencing the symptom (catch-and-ignore, retry loops, widened timeouts) while the cause is unknown.
- Declaring "fixed" without a fresh run of the original reproduction.
