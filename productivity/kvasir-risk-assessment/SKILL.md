---
name: kvasir-risk-assessment
description: Identify, evaluate, and mitigate technical, operational, and strategic risks in proposed plans.
---

# Risk Assessment

## Purpose

Identify potential failure modes in a proposed plan or approach, evaluate their likelihood and impact, and recommend mitigation strategies. Ensure that risks are surfaced before execution begins, not discovered mid-flight.

## When to Use

- Before committing to an execution plan.
- When a task involves unfamiliar technology, breaking changes, or security-sensitive areas.
- When multiple approaches exist and risk is a deciding factor.
- When a plan has long dependency chains where early failures cascade.

## Workflow

1. **Enumerate risks.**
   - Scan the plan for technical, operational, security, and strategic risks.
   - Consider unfamiliar technology, breaking changes, and sensitive areas.
   - Capture each risk specifically, not as a vague concern.

2. **Evaluate impact and likelihood.**
   - Assess how severe the consequences would be if each risk materialized.
   - Estimate the probability that each risk actually occurs.
   - Combine severity and probability into an overall risk rating.

3. **Identify cascade effects.**
   - Trace which downstream subtasks depend on the at-risk work.
   - Determine which failures would block or invalidate later steps.
   - Flag risks that sit early in long dependency chains.

4. **Recommend mitigations.**
   - For each significant risk, propose a concrete mitigation or contingency.
   - Prefer mitigations that reduce likelihood or contain the blast radius.
   - Note any residual risk that remains after mitigation.

5. **Prioritize.**
   - Rank risks by combined impact and likelihood.
   - Direct attention to high-impact, high-probability risks first.
   - Avoid over-analyzing low-impact risks at the expense of progress.

## Quality Criteria

- Risks are specific and actionable, not vague.
- Each significant risk has a mitigation or contingency.
- Cascade effects on downstream work are identified.
- Risk prioritization is clear and justified.

## Anti-Patterns

- **Vague risks**: "This might break" without specifying what, how, or why.
- **No mitigations**: Listing risks without proposing how to handle them.
- **Ignoring cascades**: Failing to identify how a failure in one subtask affects others.
- **Paralysis**: Over-analyzing low-impact risks at the expense of progress.
