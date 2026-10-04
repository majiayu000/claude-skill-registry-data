---
name: debug
description: "Investigate and fix bugs, failing tests, regressions, build failures, or unexpected behavior using boundary localization, evidence, and bounded hypotheses."
---

# Debug

Find the causal mechanism, then fix it with the least risky change. Be systematic without forcing a four-phase ceremony onto an obvious compiler error.

A debug request restores the verified existing or requested contract. It does not authorize adjacent features, fallback systems, broad refactors, or extra infrastructure merely because they might make the system more robust.

## 1. Define the failure

Capture:

- Observed behavior
- Expected behavior
- The required outcome independent of the current implementation mechanism
- Reproduction path
- Environment or data conditions
- Exact error plus transport, status, and capability provenance when the failure crosses a boundary
- First known bad version or recent relevant changes, when available

Read the complete error, stack trace, failed assertion, logs, or browser console output. Do not summarize away the line that identifies the failing boundary.

Do not group failures merely because the UI renders the same red box. A route `404`, template admission rejection, asset-plane failure, playback capability failure, and download capability failure are separate boundary hypotheses until evidence connects them.

If the failure is already precise and local, move directly to tracing it.

## 2. Reproduce or gather evidence

Prefer the cheapest reliable reproducer:

- A focused existing test
- A new regression test
- A minimal command or script
- A deterministic UI sequence
- A targeted log or state inspection

Choose the experiment for the causal claim, and keep final acceptance on the actual user surface. A mechanism surrogate may use another device, process, or local seam when it preserves the conditions material to the tested claim: the relevant path, configuration, protocol, and load, plus any identity the claim itself concerns. The surrogate need not reproduce attributes the claim does not depend on. State the material equivalence and its limits; a surrogate that omits a suspected host-specific condition cannot exclude that cause. The affected device need not reproduce every shared mechanism.

For a cross-boundary failure, check where each decisive probe starts, which relevant boundaries it traverses, and under what conditions. A green check that bypasses the suspected boundary cannot establish that boundary's health. Inspect inputs and outputs where they distinguish hypotheses; retain temporary instrumentation only when it remains useful observability.

Before a speculative repair, identify the predicted observation and a comparable baseline. Prefer deterministic reproduction. For intermittent failures, use bounded repeated trials with frequency and conditions; an authorized diagnostic intervention may itself establish reproducibility. Do not wait for a perfect harness or treat one successful run as proof.

If a material boundary still lacks a useful experiment, establish—or hand off as one bounded structural slice—the smallest executable seam or diagnostic that can reveal it. Avoid further patch/deploy attempts that do not narrow the hypothesis space. Do not duplicate production or create an unrelated testing programme; local evidence cannot close a named-host or owner-experience claim.

## 3. Trace the cause

Trace bad state backward:

- Where is the incorrect value or transition first observable?
- Which caller, event, mutation, or external response produced it?
- What assumption changed?
- Is there a nearby working path to compare?
- Could several visible failures share one upstream cause?

For an unclear cross-boundary failure, sketch only the shortest relevant path. At each boundary, name the assumption about input shape, identity, version, configuration, state, ordering, availability, or output. Compare cheap boundary evidence with a known-good case when available, and stop at the first violated assumption. Do not map the whole architecture before inspecting the failing path.

State the causal claim being tested:

> Under conditions C, X causes Y; observation Z would distinguish it from the alternatives.

Test one discriminating change or observation at a time while retaining other independently observed defects. Avoid changing several variables at once. Prefer isolating a directly observed boundary violation over another speculative setting change, unless stronger evidence or urgent mitigation justifies the priority.

## Hypothesis budget

- Interpret each trial as supporting, contradicting, or leaving the tested claim inconclusive. Before treating no improvement as counterevidence, establish that the intervention took effect on the intended target and that the relevant conditions and measurements were comparable.
- Failure to restore the whole user experience does not by itself refute one contributing mechanism. Rolling back a trial does not erase an independently observed defect; retain it and choose a better discriminator.
- Reset the diagnosis before another speculative patch when a direct boundary violation remains untested or successive trials no longer distinguish causes. Do not wait for a numeric budget to be exhausted.
- After two failed repairs on the same user-visible surface, reconsider the boundary and hidden assumptions; no later than a third materially different failed fix, use the reset below. A cascade across owners, transports, or state boundaries also warrants a reset.

Counts are a backstop against thrashing. Continue a justified investigation when successive experiments yield discriminating evidence; do not restart mechanically.

Do not delegate a vague symptom. A bounded investigation may be one worker lane before localization when the failure, expected behavior, entry evidence, return contract, and verification are already fixed and clean context or coordinator attention has material value; otherwise delegate only after localization reveals distinct evidence questions. Treat dispatch as a phase change and apply the `delegate` reference, then verify returned claims against the primary artifacts.

## Reset the diagnosis before expanding the repair

1. Pause speculative patches and restate the required outcome independently of the chosen implementation.
2. Sketch the shortest failure path. For each relevant boundary, identify its owner, current identity or state, fresh observations, and which existing probes actually cross it. Preserve confirmed defects and mark unknowns.
3. Identify the untested violation or confounded trial with the most useful discriminator. Run that bounded experiment before changing another setting; a reset need not change the architecture.
4. If evidence also challenges the necessity of the implementation mechanism, verify the assumption that ruled out a simpler supported route using current source, runtime help, a bounded probe, or authoritative documentation. Compare that route against the complete contract; retain the extra boundaries only with a reason grounded in evidence.

Debugging need not preserve optional implementation choices. Sunk cost and passing component tests do not establish that the topology is sound, but an inconclusive experiment alone does not justify a redesign.

## 4. Fix the source

Prefer the narrowest change that restores the intended invariant.

- Fix the origin of invalid state. Scope the repair to the component and lifecycle that create the failed condition, not automatically to the affected user, device, or input sample. A client-specific trial can isolate a mechanism without becoming the permanent exception.
- Avoid opportunistic refactors unless the current design prevents a safe fix.
- Add validation at boundaries when it prevents recurrence.
- Preserve compatibility unless the user approved a change.
- Before exposing an optional host action, check its capability. When absent, omit the action and preserve an honest useful degradation instead of rendering a button that must fail.
- Replace the canonical path coherently. Remove superseded helpers, flags, tests, and documentation claims once no evidenced caller needs them; do not layer the fix beside a dead implementation.
- For an external or environmental cause, improve diagnostics or error handling first. Add retries or fallback behavior only when the observed failure and product contract justify them.

## 5. Prove the fix

Use a regression test when practical. Prefer strict red-green when the failure sharpens a behavior contract; use test-alongside when the change is mostly styling, configuration, or simple wiring.

Verify:

- The same mechanism reproducer improves under comparable conditions, including the relevant successful outcome. A disappearing error counter alone can hide dropped work or a bypassed path; also check completion, delivery, or latency as appropriate.
- The regression test fails against the old behavior when that can be demonstrated safely.
- Nearby behavior remains intact.
- Optional-capability behavior distinguishes absent, rejected, cancelled, and policy-denied outcomes where the host exposes them; do not collapse their provenance into one generic error.
- Temporary diagnostics and experimental changes are removed.
- The final diff contains one understandable causal fix.

Before declaring the issue fixed, rerun the original reproducer after the final relevant edit, run the focused regression checks, and broaden verification when shared state, public contracts, data, security, or multiple consumers changed.

For a host-specific fix, deployment of the latest code is part of the experiment, not a ceremony that can be postponed indefinitely. The external or production mutation still requires applicable authorization; once that exact deployment is authorized and needed to test the fix, do not invent an additional repository gate. Require fresh acceptance on the named host after the final relevant deployment. Close claims in this order: source contract -> process-level test -> built artifact or image identity -> activated runtime identity -> exact named-host surface -> owner-observed behavior; each rung proves only itself and the next investigation step.

## Confidence labels

Use precise language:

- **Confirmed root cause:** direct evidence links cause to failure and the reproducer is fixed.
- **Probable cause:** evidence is strong but the environment prevents full reproduction.
- **Unknown:** investigation narrowed the space but did not establish causality.

Name the failure and conditions each label covers. A confirmed contributing mechanism can coexist with residual symptoms; keep overall recovery pending until the required user-surface acceptance. Do not turn a probable explanation into a certainty.

## Avoid

- “It is probably X” followed immediately by a patch
- Re-running the same command without changing evidence
- Broad dependency upgrades as a first move
- Multiple unrelated fixes in one attempt
- Fixing a timeout with a longer arbitrary timeout when a condition can be observed
- Declaring a flaky issue solved after one passing run
