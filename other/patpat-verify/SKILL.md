---
name: patpat-verify
description: Prove an implementation or repository claim against its authoritative artifact or user surface. Use after code changes, during acceptance checks, or whenever tests and builds are insufficient evidence of real behavior.
---

# Patpat Verify

For a bounded local proof, use this skill and its relevant references. Read the [operating protocol](../patpat-loop/references/operating-protocol.md) in full for uncertainty, security, auth, billing, secrets, architecture, cross-cutting work, or delivery intent. Do not load the router or reread unchanged instructions already loaded in this session.

Read [proof over proxy](../patpat-loop/principles/proof-over-proxy.md) and [preserve safety](../patpat-loop/principles/preserve-safety.md).

## The Iron Law of Verification

```text
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If the verification command was not executed in the current turn, you are strictly forbidden from declaring that tests pass, the issue is fixed, or the change is verified.

### The 5-Step Gate Function

1. **IDENTIFY**: Specify the authoritative command or check that proves the claim.
2. **RUN**: Execute the full command freshly on the authoritative surface.
3. **READ**: Inspect raw stdout, stderr, and exit code directly (sanitizing tokens and secrets via available sanitizers or inline credential masking).
4. **VERIFY**: Confirm the observed output strictly satisfies the expected criteria.
5. **ONLY THEN**: Make the claim and attach the raw evidence.

## Build the proof

1. Reconcile the requested outcomes with the proof contract using proof over proxy; name missing requirements before running checks.
2. Identify the authoritative artifact or user surface.
3. Capture a baseline or reproduce the prior state when relevant.
4. Run the smallest targeted automated check.
5. For behavioral claims, exercise the changed logic through the authoritative interface under representative conditions when safe and practical. For static claims, use the strongest deterministic check on the authoritative artifact.
6. Observe visible output and material side effects directly.
7. Inspect the final diff and version-control state for unrelated changes.
8. Record the command or action, observed result, cleanup, and limitation for each material claim; do not mark the whole request verified with uncovered outcomes.

For every test or evaluator used as evidence, apply the behavioral oracle from [proof over proxy](../patpat-loop/principles/proof-over-proxy.md). A mock-call assertion, copied constant, self-referential expected value, or fixture-only agreement cannot prove user-observed behavior; use a concrete input and observed output/effect. If a behavioral claim has no observable oracle, report `INCONCLUSIVE`; use static evidence only for requirements that are static from the outset.

## Claim-adaptive verification and proxy rejection

Match verification depth to the claim and risk:

- **Behavioral claims**: Vary material inputs, relevant error branches, or state transitions when safe and practical. Call the subject through the authoritative interface and assert the literal observed result or material effect. A mock interaction, call count, truthiness check, copied constant, or clean compilation does not prove the behavior by itself.
- **Static claims**: Use deterministic structure, schema, type, or content checks when that is the authoritative surface. Do not manufacture runtime theater for a non-runtime claim.
- **Proxy evidence**: Fixtures and mocks may isolate a contract, but they do not replace the real system when the claim concerns that system. Reject narrative summaries, hardcoded fixture answers, and clean compilation as sole behavioral proof.
- **Fresh binding**: Bind evidence to the exact candidate revision or a reproducible working-tree snapshot, plus material inputs, environment, and oracle. Require the committed head for commit-, push-, PR-, or delivery-bound claims. Reject stale, cached, or transferred logs.

Do not accept an implementing agent's report as evidence. Inspect the artifact and results directly. For high-risk boundaries, obtain an independent review without leaking the intended conclusion.

Classify the outcome using exactly one label:

- `verified`: The claimed behavior was observed on the authoritative surface and relevant checks passed.
- `partially verified`: Some required evidence passed, but a named surface or condition could not be checked.
- `implemented but not verified`: The change exists, but no meaningful behavioral proof ran.
- `not implemented`: No implementation change was made.

If a check fails, classify the failure before retrying. Change the hypothesis, implementation, verifier, or environment; never loop the same attempt.

## Mutation boundary

Remain read-only with respect to repository implementation and external delivery. Limit incidental verifier artifacts to the declared proof contract, clean them up, and hand any authorized mutation back to `patpat-loop`.
