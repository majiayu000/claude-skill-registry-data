---
name: your-skill-name
description: Use when <clear trigger condition for this skill>.
version: 1.0.0
authors:
  - your-name-or-org
tags:
  - category
  - education
status: draft
---

# Purpose

State the educational problem this skill solves and the intended outcome.

# Activation Logic

## Activate When

- Trigger 1
- Trigger 2
- Trigger 3

## Do Not Activate When

- Exclusion 1
- Exclusion 2

## Priority Rules

- If this skill conflicts with `<other-skill>`, prefer this skill when `<condition>`.

# Inputs

- Learner objective
- Learner level signals
- Repository or project context
- Relevant prior conversation state

# Workflow

1. **Orient**
   - Gather the minimum context required.
   - Confirm learner goal and level assumptions.
2. **Teach or Guide**
   - Deliver a concise step adapted to level.
   - Use one concrete example.
3. **Check**
   - Ask a reasoning-focused checkpoint question.
4. **Adapt**
   - Correct misconceptions or reduce complexity as needed.
5. **Advance**
   - Propose one next implementation action.

# Educational Rules

- Teach incrementally.
- Require active learner reasoning.
- Explain why a step matters.
- Prefer practical implementation over passive summary.

# Failure Modes and Guardrails

1. **Overload**
   - Symptom: long dense monologue.
   - Guardrail: limit to one core concept per step.
2. **Level Mismatch**
   - Symptom: learner confusion or overconfidence.
   - Guardrail: ask a checkpoint before increasing complexity.
3. **Answer Dumping**
   - Symptom: agent gives full solution immediately.
   - Guardrail: require learner attempt or prediction first.

# Output Structure

```markdown
## Context
<What we are solving and why>

## Guidance
<Step-by-step explanation>

## Checkpoint
<Question that forces reasoning>

## Next Step
<Concrete implementation action>
```

# Validation Checklist

- [ ] Activation triggers are explicit and testable.
- [ ] Workflow includes at least one adaptation branch.
- [ ] Educational rules are enforceable from output.
- [ ] Failure modes include actionable guardrails.
- [ ] Output structure is deterministic.
- [ ] `examples.md` includes beginner, advanced, and recovery scenarios.
