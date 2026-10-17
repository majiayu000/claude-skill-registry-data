---
name: poc-validation
description: Validate ideas with proof-of-concept work — hypothesis, success/kill criteria, timebox, evidence, decision.
version: 1
triggers: proof of concept, poc, validate an idea, kill criteria, timebox, pilot
category: Thinking & decisions
blurb: Validate ideas with a proof of concept — a hypothesis, success and kill criteria, and evidence.
archetype: knowledge
example: Design a two-week proof of concept for this idea.
---

# POC Validation

A POC exists to reduce uncertainty, not to ship. Define the question, the kill criteria, and the timebox — before writing code.

## When to use
- A new technology, approach, or integration needs de-risking.
- "Can this even work?" questions whose answer changes the plan.
- Evaluating vendors/tools against the house stack.

## Method
1. **The question**: one hypothesis, written down ("X can do Y under constraints Z").
2. **Criteria upfront**: success AND kill criteria — agreed by the decision owner before the build.
3. **Timebox**: hard limit (days, not weeks); scope is the critical path, nothing more.
4. **Disposable by default**: POC code is throwaway unless explicitly slated for hardening — say which it is.
5. **Evidence**: measurements, tests, a demo — numbers over impressions; record what was stubbed or mocked.
6. **Decision**: adopt / adapt / abandon with written rationale referencing the criteria; log it (`delivery-planning`).
7. **If adopting**: it goes through the full team process (spec → build → test → review). POCs never slide into prod.

## Quality gates
- [ ] Hypothesis + success/kill criteria written before start.
- [ ] Timebox enforced; scope creep refused politely.
- [ ] Findings memo with decision + evidence.
- [ ] Clear "not tested / not included" list.

## Red lines
- No silent POC-to-production gradient; no unbounded POCs.
- "It worked in the POC" is never production evidence.

## Related
`architecture-decisions` (decisions from findings) · `test-design` · `delivery-planning` (timeboxing).
