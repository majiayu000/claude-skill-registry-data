---
name: adversarial-verifier
description: Stress-test an implementation with adversarial inputs, boundary cases, contract violations, and security probes, then produce an evidence-backed report. Use.
---

# Adversarial Verifier

Act as an independent breaker. Find reproducible failures; do not inflate hypotheses into findings and do not fix the implementation unless the user separately asks.

## Safety Boundary

- Test only code, environments, endpoints, and accounts the user placed in scope.
- Prefer unit tests, local fixtures, mocks, or an isolated staging environment.
- Do not run destructive payloads, credential attacks, high-volume denial-of-service, persistence, or data exfiltration against a live service without explicit authorization and a bounded test plan.
- Replace dangerous probes with inert canaries when they can prove the same weakness.
- Preserve unrelated worktree changes and secrets. Never place real credentials or personal data in tests or reports.

## Workflow

### 1. Establish the baseline

Record the requested scope, expected behavior, current test command, environment, and repository state. Run the smallest relevant existing test set first. If the baseline already fails, separate pre-existing failures from adversarial findings.

### 2. Map the attack surface

Inventory entry points, trust boundaries, privileged operations, persistent state, parsers, queues, retries, and external dependencies. Rank them by impact and exposure.

| ID | Entry point | Input source | Trust | State or privilege | Priority |
|---|---|---|---|---|---|
| E-1 | function, route, job, or file parser | user, API, file, env, queue | untrusted, mixed, trusted | data changed or privilege used | high, medium, low |

### 3. Derive adversarial cases

Select cases that fit the code instead of blindly running every category:

- boundaries: empty, zero, negative, maximum, overflow, truncation, duplicate, stale, expired;
- types and encodings: null, wrong type, Unicode normalization, null bytes, malformed structured data;
- injection and traversal: SQL, command, template, header, path, archive, and deserialization boundaries;
- authorization and state: cross-tenant identifiers, replay, missing ownership checks, invalid transitions;
- concurrency and resilience: duplicate delivery, cancellation, timeout, race, partial failure, retry storms;
- resource bounds: deeply nested or large inputs tested with explicit local limits;
- contracts: violated preconditions, invariants, postconditions, schema, and compatibility promises.

### 4. Write proof tests

For each candidate, create the smallest test that distinguishes safe from unsafe behavior. A confirmed finding needs all of:

1. a documented expected invariant;
2. a reproducible input and environment;
3. an assertion that fails on the current implementation for the intended reason;
4. a control or neighboring case when ambiguity is possible;
5. captured command and relevant output.

Do not write an assertion that merely expects the buggy value. Assert the correct behavior so the test fails before the fix and passes after it.

### 5. Run and classify

- **Confirmed**: the proof test fails for the claimed reason and is repeatable.
- **Not vulnerable**: the proof test passes; record only when useful for coverage.
- **Inconclusive**: the environment, fixture, or oracle is insufficient. Do not assign vulnerability severity.
- **Pre-existing failure**: baseline failure unrelated to the probe.

Re-run flaky or concurrency-sensitive cases enough times to support the claim, but keep load bounded.

### 6. Assess severity

Use impact plus realistic exploitability, not dramatic payload names:

- P0 critical: credible unauthorized access, systemic data loss, or catastrophic compromise;
- P1 high: significant data corruption, privilege breach, or practical denial of service;
- P2 medium: limited exposure, incorrect behavior, or reliability failure with meaningful impact;
- P3 low: narrow, low-impact edge case or hardening opportunity.

Lower confidence when prerequisites are unverified. Refer security exploitability questions to the relevant security-analysis skill when available.

### 7. Report

Write `ADVERSARIAL-REPORT.md` only when the task authorizes creating an artifact; otherwise report in chat.

```markdown
# Adversarial Verification Report

## Scope and baseline
- Target:
- Environment:
- Baseline command/result:

## Summary
| Surface | Cases run | Confirmed | Inconclusive |

## Confirmed findings
### AF-1: Title (P1, confidence: high)
- Invariant:
- Impact and exploitability:
- Reproduction command:
- Proof test:
- Observed result:
- Expected result:
- Suggested remediation direction:

## Tested but not vulnerable
## Inconclusive or untested areas
## Verdict
PASS / CONDITIONAL PASS / FAIL, with merge recommendation and conditions.
```

## Independence and Model Policy

Use a fresh reviewer or session when available and avoid leaking the implementer's conclusions. A different provider or named model is optional, not required. Choose from capabilities already available in the active host; never switch providers, spend money, or select a fixed model automatically.

## Completion Gate

- Baseline and scope are recorded.
- Every reported vulnerability has a reproducible failing proof test.
- Dangerous probes stayed within the authorization boundary.
- False positives, inconclusive cases, and pre-existing failures are separated.
- Test artifacts contain no secrets and can be removed or retained intentionally.
