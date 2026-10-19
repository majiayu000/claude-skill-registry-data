---
name: acceptance-harness
description: "Design acceptance scenarios with PASS/FAIL/BLOCKED semantics, collect per-scenario evidence, and inject faults to prove resilience. Use when defining what 'done' means, writing acceptance criteria, or proving failure recovery."
license: MIT-compat
compatibility: "framework-agnostic; any test runner; Linux"
metadata: {}
allowed-tools: []
---

Standard: name/description/length rules — [agentskills.io standard](../references/agentskills-standard.md).
# Acceptance Harness Skill (body <500 lines)

Full procedure: references/acceptance-harness-procedure.md
Sources: references/SOURCES.md
Evals: references/EVALS.md
Helpers: scripts/ (shipped: `check_audit_selectors.py`, `report_result.py`,
`make_harness.sh` — all offline, deterministic, self-tested).

> Cross-links: `check_keyboard.py` and `check_axe_evidence.py` live in
> `../playwright-a11y-e2e/scripts/` (keyboard and axe evidence are E2E concerns,
> not acceptance-harness concerns). Call them with the relative path above.

## When to use this skill (trigger)
- Defining what "done" means for a feature or change.
- Writing scenarios that must produce PASS, FAIL, or BLOCKED.
- Collecting evidence that a requirement is actually met.
- Proving failure paths and recovery (fault injection).
- A reviewer asks "what would break this, and how do we know?"

## Disambiguation
- Fires: defining what 'done' means, writing PASS/FAIL/BLOCKED scenarios, fault injection, collecting evidence a requirement is met.
- Does NOT fire for: a unit test (that is a test, not an acceptance gate), a code-review checklist, or a release checklist.

## When NOT to use this skill
- Exploratory testing without a defined scenario (use a QA session).
- Pure performance or load testing (use a benchmark harness).
- Scenarios whose PASS criteria are opinions, not observable facts.
- A unit test that asserts one function — that is a unit test, not an acceptance scenario; the harness governs end-to-end behaviour with evidence.
- A "it works on my machine" claim — the harness asks for a runnable pointer, not a story.
- Retesting something that has not changed — re-run only if the evidence pointer is missing or older than the code it points at.

## Decision table — scenario outcome
| Requirement type | Outcome | Evidence to attach |
|-----------------|---------|--------------------|
| Functional happy path | PASS | test log + screenshot/trace |
| Functional error path | FAIL (expected) | error log + recovery action |
| Non-functional (perf, security) | PASS | metric report (p95, count) |
| Blocked by external dependency | BLOCKED | blocker note + ticket/owner |
| Fault tolerance / recovery | FAIL then PASS | fault injection log |
| Ambiguous / not yet specified | BLOCKED | open question + owner |

## Numbered procedure (summary; full recipe in references/acceptance-harness-procedure.md)
1. Enumerate every requirement; one scenario per requirement, never two requirements per scenario.
2. Write the PASS criteria as an observable assertion, not a feeling.
3. Choose the evidence type: log, screenshot, metric, or trace.
4. Write the rollback plan: how to undo the scenario's effects.
5. Run the scenario; record the outcome (PASS/FAIL/BLOCKED) and the evidence pointer.
6. If FAIL, distinguish "system under test failed" from "scenario is wrong"; fix the scenario, not the claim, only if the requirement genuinely changed.
7. Inject a fault on a passing scenario; the system must recover and the scenario must return to PASS.
8. Commit the scenario file, evidence, and outcome; re-run on every change.

## Worked examples
Good (one requirement, one scenario, one evidence type, one rollback):
```yaml
# scenarios/rls-tenant-isolation.yml
id: rls_tenant_isolation
requirement: "A tenant's rows are invisible to another tenant"
expected: PASS
evidence: logs/rls-tenant-isolation.log
rollback: "revert migration r3-07; no data written"
assertion: "SELECT count(*) FROM orders WHERE tenant_id = 'other' = 0"
```
Bad (scenario with no discriminating power — always passes):
```yaml
id: ui_renders
requirement: "The page renders"
expected: PASS
assertion: "page loads"          # not observable; every run passes
```
Bad (two requirements in one scenario — hides which one failed):
```yaml
id: mixed
requirement: "Create order AND send email"
# if email fails, is it the create or the send that broke? Unknown.
```

## Pitfalls from research
- Scenarios without a concrete PASS criterion drift into opinion; every scenario needs a checkable assertion.
- Evidence not attached to a scenario is unverifiable; a pointer must open in under 60 seconds.
- Fault injection that crashes the system without recovery is destructive, not resilience proof: require recovery and a return to PASS.
- A scenario that always passes is not a scenario; it has no discriminating power.
- Reusing one scenario for two requirements hides which requirement failed.

## Near-miss triggers (act before the incident)
- "I'll just eyeball the result" — write the assertion first, then look.
- "This scenario is probably fine" — run the fault-injection variant.
- "The evidence is in my head" — put it in a file; a pointer must open in <60s.
- "Let's bundle three checks into one scenario" — split them; one scenario = one requirement.

## Verification checklist (all must pass before you finish)
- [ ] 1 scenario = 1 requirement = 1 expected outcome = 1 evidence type = 1 rollback plan.
- [ ] Every PASS has a runnable evidence pointer.
- [ ] Every FAIL names the failing assertion and the recovery step.
- [ ] Every BLOCKED names an owner and a concrete next question.
- [ ] At least one fault-injection scenario proves recovery.

## Related skills
- [honest-status](../honest-status/SKILL.md) — PASS/FAIL/BLOCKED outcomes are status buckets.
- [problem-json-contracts](../problem-json-contracts/SKILL.md) — a failure in a scenario is a problem-detail payload.
- [module-contract-first](../module-contract-first/SKILL.md) — a scenario's criteria are module contracts: enumerate them, do not hand-wave the API surface.
- [long-test-discipline](../long-test-discipline/SKILL.md) — a scenario that takes minutes is a long test; schedule it in the foreground with a recorded seed.
- [shared-tree-git](../shared-tree-git/SKILL.md) — the scenario file, evidence and outcome are committed with a task-id prefix.
