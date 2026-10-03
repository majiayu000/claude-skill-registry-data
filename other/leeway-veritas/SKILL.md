---

name: leeway-veritas

description: Independent LeeWay verification authority that defines pre-gate, post-gate, acceptance-test, negative-test, recovery-test, and evidence-state requirements without treating model output or execution claims as proof.

license: MIT

metadata:

  authority: Creator/Human Authority > LeeWay Standards > Root of Trust

  mode: verification-authority

  stage: pre-execution-and-post-execution

---

# LeeWay Veritas

## Law

Execution is not verification. A PASS requires inspectable evidence against an explicit acceptance criterion.

## Pre-gate

Verify authority, target identity, expected state, dependencies, mutation scope, rollback/recovery, and acceptance test before consequential execution.

## Post-gate

Measure actual post-state, compare to expected state, run required negative/sibling/recovery checks, classify VERIFIED / OBSERVED / INFERRED / PROPOSED / UNVERIFIED / FAILED / BLOCKED, and reject unsupported promotion.

## Composition

Consumes desired result/acceptance gate from Agent Operating Loop; receives focal execution evidence from Skill Orchestrator/Tool Gateway; hands verified evidence to Receipt Authority and Learning Ledger. Veritas must remain independent enough to fail an execution path.