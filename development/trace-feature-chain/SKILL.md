---
name: trace-feature-chain
description: Trace a cross-layer feature failure from the real user scenario to the released artifact, find the first mismatch, and define the smallest safe repair. Use when a role, device, entry point, data shape, permission, API, shared contract, runtime, build, preview, upload, or re-entry result disagrees with expectation; do not load for ordinary UI polish, isolated syntax fixes, or general cleanup.
---

# Trace Feature Chain

Find the first place where the observed feature stops matching its intended contract. Preserve the original scenario, separate evidence by layer, and repair only the mismatched layer.

## Trigger boundary

Load this Skill when a feature is conditional on a role, device, entry point, permission, data shape, runtime, build, delivery channel, or re-entry path. It is also appropriate when a user wants root-cause tracing, a minimum safe fix, or an honest boundary between source, artifact, preview, upload, release, and acceptance.

Do not load it for a standalone rewrite, visual polish, one-line syntax correction, or a generic deployment task whose failure chain is not in question.

## Operating procedure

1. **Freeze the scenario predicate.** Record the generic role/account class, business goal, device/runtime, environment, real entry, page state, identity and permission facts, data conditions, exact action, unique failure, expected result, and non-goals. Use placeholders for private identifiers.
2. **Reproduce the real path.** Keep the original role class, device, entry point, data shape, and failure condition. Do not substitute an easier account, empty data, simulator, or alternate route and call the issue fixed.
3. **Walk the chain in order.** Check role → business goal → real entry → page state → permission and identity facts → command → API → backend/database/object storage → shared contract → runtime → build artifact → preview/upload/release → re-entry and recovery.
4. **Record evidence by link.** For each relevant link, write `expected`, `observed`, `evidence`, and `pass | fail | unknown`. Use [the evidence matrix](references/evidence-matrix.md) and read [the scenario model](references/scenario-and-chain-model.md) when the predicate is complex.
5. **Find the first mismatch.** Trace upstream from the symptom and stop at the first directly evidenced difference. Treat later error text, loading state, retry loop, and stale page as consequences until proven otherwise.
6. **Probe only meaningful contrasts.** Compare empty versus non-empty data, ordinary versus special role, simulator versus real device, fresh entry versus re-entry, and source versus delivered artifact only when they relate to the original predicate.
7. **Choose the narrow repair.** Fix the first mismatched layer. Repair shared behavior in the shared contract, policy in the policy layer, and data production in the producing layer. Do not add account-specific exceptions, speculative fallbacks, unrelated refactors, or an unaffected server deployment.
8. **Verify each claimed layer.** Run focused tests, the original scenario, relevant generation/build checks, and delivery or re-entry checks separately. Read [proof and release boundaries](references/proof-and-release-boundaries.md) before claiming that a fix reached a user.
9. **Report what is still unknown.** State changed files, intentionally untouched layers, evidence, missing proof, user or real-device checks, and retry/recovery behavior. Never turn an unrun check into `pass`.

## Required output

```text
Scenario predicate:
Scope and non-goals:
Chain status:
First mismatch:
Root cause and affected layer:
Minimal safe fix:
Evidence and verification:
Release boundary:
Remaining risks or user checks:
```

## Public-safe case

A role-specific real-device failure conditioned on a non-empty signed media URL can look like an API problem. If the API returns the expected shape and a shared client contract calls a browser-only runtime API, the first mismatch is the contract/runtime boundary. Fix the shared code, add the original data shape as a regression case, and do not redeploy an unrelated backend. See [the anonymized case](references/anonymized-case-study.md); its numbers are a single case record, not a benchmark.

## Composition

- Pair with `run-autonomous-workpacks` when an already-authorized repair spans diagnosis, implementation, tests, artifacts, and closeout.
- Pair with `reason-from-reality` when the software evidence must change a longer decision or learning loop.
- Do not load all three for a simple syntax fix, translation, visual polish, or isolated factual answer.
