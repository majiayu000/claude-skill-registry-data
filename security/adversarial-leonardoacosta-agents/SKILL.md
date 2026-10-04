---
name: adversarial
description: "Routes adversarial engineering work to the right review or testing method. Use when the user asks to red-team, adversarially review, break, stress-test, challenge assumptions, audit release readiness, try to break an app, review a diff skeptically, or write negative/failure-path tests. Detects whether the target is a repository/PR, product/deployment, or executable code path, then routes to adversarial-code-review, rate-my-code, or tests-adversarial. Do not use for routine code review, ordinary bug fixing, happy-path tests, or generic security advice unless adversarial treatment is requested."
---

# Adversarial Engineering — Decision Router and Challenge Mentor

Adversarial work is not hostility for its own sake. It is a disciplined attempt to disprove a claim, expose an assumption, or demonstrate a failure with evidence. First identify the claim being challenged and the safest observable surface that can falsify it.

## Step 1: Identify the adversarial target

Ask what the user wants to break or disprove:

| User intent | Primary route |
|---|---|
| Review working-tree changes, staged changes, commits, PRs, or AI-generated code before merge | `/adversarial-code-review` |
| Decide whether an app, product, repository, or deployment is shippable; try real user journeys; inspect release readiness | `/rate-my-code` |
| Write tests that violate assumptions, exercise failure paths, probe boundaries, or stress concurrency and recovery | `/tests-adversarial` |
| Explicitly request a cross-model opposing review | `/adversarial-review` if installed and the opposite CLI is available |
| Explicitly request hostile reviewer personas | Use `/adversarial-reviewer` only as a lightweight supplementary lens |

If more than one target applies, separate the passes. A static diff review does not prove runtime release readiness, and a passing negative-test suite does not prove the product journey works.

## Step 2: State the claim and evidence boundary

Before acting, write:

```text
Target: [exact artifact, diff, product, endpoint, or module]
Claim under challenge: [what is supposed to be true]
Attack surface: [public API, user journey, diff, persisted state, or deployment]
Evidence allowed: [read-only inspection, safe runtime, sandbox account, tests, logs]
Unsafe actions excluded: [production mutation, payments, deletion, credential changes]
Success condition: [what would disprove the claim, and what evidence supports survival]
```

Treat implementation descriptions, existing tests, completion claims, and documentation as claims, not proof. Prefer a concrete reproduction or fresh command output over intuition.

## Step 3: Choose the smallest effective challenge

- For a diff or merge decision, use the evidence-grounded review contract. Preserve the exact snapshot, establish requirements before judging code, inspect the full context, route risk domains, verify tests, and keep the review read-only unless fixes are separately authorized.
- For an app or deployment, resolve one coherent artifact first, then choose a review role and degree. Exercise the golden path, one realistic failure, one retry or refresh, one concurrent burst where state changes, one identity or ownership boundary, and the lifecycle boundary most relevant to the promise. Record unknowns instead of assuming them away.
- For code-level hardening, enumerate assumptions before writing tests. Violate inputs, ordering, timing, state lifecycle, resources, and protocol behavior through the public API. Test both sides of boundaries and verify error quality, not merely that an exception occurred.

Do not run destructive or financial tests against production without explicit authorization and a safe sandbox. Do not treat a clean burst as proof of race safety without locating the compensating constraint, idempotency key, transaction, lock, or equivalent guard.

## Step 4: Adversarial test design

Use this attack matrix:

| Dimension | Plausible violations |
|---|---|
| Data | null, empty, negative, maximum, malformed, Unicode, duplicate, oversized |
| State | half-initialized, repeated event, double-close, recovery after failure, stale result |
| Time | timeout, cancellation, delayed response, clock skew, expiry during operation |
| Concurrency | duplicate submission, interleaving, out-of-order delivery, retry overlap |
| Resources | missing file, denied permission, full disk, exhausted pool, dropped connection |
| Boundaries | unauthorized identity, tenant mismatch, version mismatch, partial write |

Every proposed finding must include the trigger, actual behavior, expected behavior, impact, and evidence. If evidence is insufficient, record an unknown or an unverified coverage item rather than inventing a defect.

## Anti-patterns

- **NEVER manufacture a finding** merely because an adversarial persona is required to speak. A forced issue can be a residual risk or unknown, not a fabricated defect.
- **NEVER equate coverage with challenge quality.** Happy-path tests, line coverage, and a clean linter do not exercise violated assumptions.
- **NEVER review only changed lines** when interaction with surrounding code can alter behavior.
- **NEVER let the implementation redefine the requirement.** Reconcile the original intent and accepted decisions first.
- **NEVER call a static inspection runtime proof.** Mark behavior as unverified when the product, service, dependency, or environment could not be exercised.
- **NEVER mutate the target during a report-only review.** Fixes, installs, snapshot rewrites, merges, and durable external changes require separate authorization.
- **NEVER use private internals to create a test scenario** when the public API can express it. If only private access works, report the abstraction leak.
- **NEVER claim a race is safe from a serial retry.** Exercise overlap and identify the durable guard.
- **NEVER let a stale report survive a changed snapshot.** Reinspect the final diff and rerun affected checks.

## Routing notes

Load the selected domain skill immediately after this routing step. Keep this skill as the general modeling and boundary layer rather than duplicating the detailed review contract, release ledger, or language-specific testing guidance.

When a candidate route is unavailable, retain the same target/claim/evidence structure and perform the narrowest safe fallback in the current context. State the missing tool or reference explicitly.
