---
name: change-maintenance-specification
description: Specifies bugs, upgrades, refactors, and behavioral changes as explicit deltas against existing feature specifications, preserving original intent while defining what changes, what remains unchanged, and how correctness is verified.
---

# Change & Maintenance Specification

## Purpose

This skill produces a **change specification** for work that modifies **existing behavior**.

It is used when a feature, workflow, or system capability already exists and must be:

- corrected (bug),
- improved without changing behavior (upgrade/refactor), or
- intentionally altered (behavioral change).

This skill **does not replace** existing feature specifications.  
It defines a **delta** against them.

---

## When to Use This Skill

Use this skill when:

- A bug is reported in an existing feature
- A refactor or upgrade is required without changing user-visible behavior
- An intentional change modifies how an existing feature behaves
- Regression risk must be explicitly controlled

Do **not** use this skill to:

- define new features
- rewrite PRDs
- decompose features
- create implementation plans or code
- manage workflows or execution

---

## Core Principle (Non-Negotiable)

**Existing feature specifications define intended behavior.  
Change specifications define deviations and corrections.**

A bug or upgrade **must not silently rewrite intent**.

---

## Supported Change Types

This skill supports all of the following change types.

### 1. Bug Fix

- Current behavior is incorrect
- Intended behavior already exists or is implied by the feature specification

### 2. Upgrade / Refactor

- Behavior is correct
- Internal structure, safety, performance, or maintainability changes
- User-visible behavior must remain unchanged

### 3. Behavioral Change

- Existing behavior is intentionally modified
- User-visible outcomes may change
- Change must be explicit and auditable

### 4. Feature Flag Lifecycle

- **Flag Removal**: Removing a temporary flag once exit criteria are met.
- **Flag Promotion**: Converting a temporary flag to a permanent one based on new justification.
- **Flag Behavior Modification**: Changing how an existing flag controls logic.

---

## Delta-Based Thinking

Every change specification must clearly distinguish:

- **Baseline** — what exists today according to the feature specification (including current flag state)
- **Current Reality** — what actually happens (if different)
- **Target Behavior** — what should happen after the change (including flag removal or promotion)
- **Unchanged Behavior** — what must remain exactly the same

Flag changes are treated as **DELTAS**. Do not allow silent flag changes.

This separation prevents regression and scope creep.

---

## Change Specification Structure

The output of this skill must follow the structure below.

# Change Specification

## 1. Change Summary

## 2. Baseline Reference

## 3. Current Behavior

## 4. Target / Expected Behavior

## 5. Scope of Change

## 6. Unchanged Behavior

## 7. Out of Scope

## 8. Impacted Areas

## 9. Risk & Regression Considerations

## 10. Scenarios

## 11. Acceptance Criteria

### 1. Change Summary

Briefly describe:

- what is changing
- why the change is required
- the type of change (bug, upgrade, behavioral change)

### 2. Baseline Reference

Explicitly reference the existing feature specification or documentation that defines the intended behavior.

This establishes the contract against which the change is evaluated.

### 3. Current Behavior

Describe:

- what actually happens today
- when the issue occurs
- observable incorrect or undesirable outcomes

Be factual and neutral.

### 4. Target / Expected Behavior

Describe:

- the behavior that should exist after the change
- alignment with the baseline specification (for bugs/upgrades)
- intentional differences (for behavioral changes)

Avoid proposing implementation details.

### 5. Scope of Change

Clearly state:

- what behavior is being modified
- what components or flows are affected conceptually

This defines the blast radius.

### 6. Out of Scope

Explicitly state what this change does not affect.

This is critical for preventing accidental expansion.

### 7. Impacted Areas

List:

- features
- workflows
- data paths
- user experiences
that could be affected by the change.

This is informational, not a task list.

### 8. Risk & Regression Considerations

Identify:

- potential regressions
- user trust risks
- data consistency risks
- compatibility concerns

Do not include mitigation plans—only awareness.

### 9. Scenarios

Provide scenarios that illustrate:

- the problematic behavior (before)
- the corrected or changed behavior (after)
- confirmation that unchanged behavior remains intact

Scenarios may use Gherkin format when helpful:

```gherkin
### Scenario: [Description]
Given ...
When ...
Then ...
```

Scenarios should emphasize contrast, not completeness.

### 10. Acceptance Criteria

Define objective conditions that confirm the change is complete.

Acceptance criteria must:

- be verifiable
- map to scenarios
- include regression confirmation where relevant

Avoid vague or subjective language.

---

## Important Boundaries

This skill **must not**:

- rewrite feature specifications wholesale
- propose implementation approaches
- assign tasks, owners, or timelines
- decide rollout or deployment strategy
- create or modify files or issues
- control execution or workflow state

All orchestration belongs to the calling agent.

---

## Output Expectations

The output of this skill should be:

- concise but precise
- explicitly delta-focused
- auditable over time
- safe to use in long-lived systems
- deterministic for the same inputs

Assume the output will be reviewed by engineers, reviewers, and future maintainers to understand what changed and why.
