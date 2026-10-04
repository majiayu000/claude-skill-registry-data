---
name: domain-validator
description: Validate agent output against declared domain rules and ground truth before trusting it downstream. Trigger after any agent produces output that will be used in a decision, stored persistently, or passed to another agent.
---

# Domain Validator

> **Agent output is a hypothesis. Domain validation is the test.**

An agent that produces output without validation is a system that produces hallucinations at scale. The domain validator is the check that separates "the agent said so" from "it is true."

## When to use

- After an agent produces output that feeds a downstream system or human decision
- When an agent has reasoned over domain-specific data (financial figures, medical records, legal clauses, system configurations)
- Before persisting agent-generated content to a database or document store
- When an agent output will be presented to an end user as factual

## Procedure

1. **Declare the domain rules** — before running any validation, the domain rules must be explicit:
   - What are the invariants? (e.g. "a date range must have start < end", "a price must be positive", "a configuration must reference an existing resource")
   - What are the allowed value ranges or enumerations?
   - What is the ground truth source? (database record, API response, regulatory document, schema definition)

2. **Extract the claims** — identify the specific assertions in the agent output that are subject to validation. Not every word in the output is a claim; focus on structured data, named values, and factual assertions.

3. **Validate each claim against the domain rules**:
   - **Structural validation**: does the output conform to the expected schema or format?
   - **Range and constraint validation**: are values within allowed bounds?
   - **Referential integrity**: do referenced entities exist in the ground truth source?
   - **Logical consistency**: are the claims internally consistent? (e.g. no contradictory figures)
   - **Freshness**: is the ground truth source current, or could it be stale?

4. **Classify findings**:
   - **PASS**: claim is valid against all domain rules
   - **WARN**: claim is plausible but cannot be fully verified (e.g. ground truth unavailable)
   - **FAIL**: claim violates a domain rule or contradicts ground truth

5. **Produce a validation report** — for each claim: status (PASS/WARN/FAIL), the rule checked, and the evidence.

6. **Gate downstream use** — FAIL findings block downstream use of the output. WARN findings require explicit human acknowledgement before proceeding. PASS findings may proceed automatically.

## Outputs

- Validation report: claim | status | rule checked | evidence
- Overall verdict: PASS / WARN / FAIL
- List of FAIL and WARN findings for human review

## Guardrails

- **Domain rules must be declared before validation runs.** Validating against implicit rules produces false confidence.
- **WARN is not PASS.** A WARN finding means uncertainty, not safety.
- **Ground truth must be identified.** If there is no ground truth source, the output cannot be validated — flag this explicitly rather than assuming it is correct.
- **Validation is not proofreading.** Grammar and style are not domain rules. Focus on factual and structural correctness.

## Anti-rationalization table

| Excuse | Counter |
|---|---|
| "The model is reliable enough" | Reliability is a statistical claim. Domain validation is a deterministic check. Run it. |
| "We'll catch errors in review" | Human review misses structured errors that automated validation catches. Both are needed. |
| "The domain rules aren't defined yet" | Then the output cannot be trusted yet. Define the rules before relying on the output. |
