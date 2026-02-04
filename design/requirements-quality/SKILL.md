---
name: requirements-quality
description: Requirements quality assessment and improvement. Use when evaluating requirements against INVEST criteria, improving clarity, detecting ambiguity, or ensuring completeness. Provides quality checklists, refinement patterns, and MoSCoW prioritization guidance.
allowed-tools: Read, Glob, Grep, Write, Edit, Task
---

# Requirements Quality

Requirements quality assessment, INVEST criteria validation, and refinement patterns.

## When to Use This Skill

**Keywords:** INVEST, requirements quality, clarity, ambiguity, completeness, testable, estimable, refinement, MoSCoW, prioritization, acceptance criteria, requirement validation, quality assessment

**Use this skill when:**

- Evaluating requirements against INVEST criteria
- Improving requirement clarity and precision
- Detecting and resolving ambiguity
- Ensuring requirements are complete
- Applying MoSCoW prioritization
- Refining requirements iteratively
- Validating acceptance criteria quality

## INVEST Criteria Overview

The INVEST acronym defines six quality criteria for well-formed requirements:

| Criterion | Question | Red Flag |
| --- | --- | --- |
| **I**ndependent | Can this be implemented alone? | "Requires X to be done first" |
| **N**egotiable | Is there room for discussion? | Over-specified implementation |
| **V**aluable | Does it deliver user value? | Technical-only benefit |
| **E**stimable | Can effort be estimated? | Vague or unbounded scope |
| **S**mall | Can it be done in one iteration? | Multi-sprint scope |
| **T**estable | Can we verify it's done? | Missing acceptance criteria |

## Quick Quality Assessment

### Rapid INVEST Check

For each requirement, score 0-2 on each criterion:

| Score | Meaning |
| --- | --- |
| 0 | Does not meet criterion |
| 1 | Partially meets criterion |
| 2 | Fully meets criterion |

**Interpretation:**

- 10-12: High quality, ready for implementation
- 7-9: Acceptable, minor improvements needed
- 4-6: Needs work, significant refinement required
- 0-3: Not ready, major rewrite needed

### Common Quality Issues

| Issue | Symptom | Fix |
| --- | --- | --- |
| Too vague | "Make it user-friendly" | Add measurable criteria |
| Too large | Multi-week estimate | Split into smaller requirements |
| Untestable | No clear success condition | Add acceptance criteria |
| Dependent | "After X is complete" | Decouple or combine |
| Technical | "Refactor database" | Reframe as user value |
| Over-specified | Implementation details | Focus on what, not how |

## MoSCoW Prioritization

### Priority Levels

| Priority | Meaning | Guidance |
| --- | --- | --- |
| **Must** | Critical for release | Without this, release fails |
| **Should** | Important but not critical | High value, schedule permitting |
| **Could** | Nice to have | Include if time allows |
| **Won't** | Out of scope (this time) | Explicitly deferred |

### Prioritization Questions

1. What happens if we don't include this?
2. Is there a workaround without this?
3. How many users are affected?
4. What's the business impact?
5. Are there dependencies on this?

## Clarity Enhancement Patterns

### Ambiguity Detection

**Ambiguous Words to Avoid:**

| Word | Problem | Better Alternative |
| --- | --- | --- |
| "should" | Unclear obligation | "SHALL" (mandatory) or "MAY" (optional) |
| "quickly" | Subjective timing | "within 200ms" |
| "user-friendly" | Subjective quality | Specific usability criteria |
| "etc." | Incomplete list | Exhaustive enumeration |
| "appropriate" | Vague standard | Specific criteria |
| "some" | Undefined quantity | Explicit count or range |
| "easy" | Subjective difficulty | Measurable steps |

### Clarity Checklist

- [ ] Uses specific, measurable terms
- [ ] Avoids ambiguous words
- [ ] Defines all acronyms on first use
- [ ] Includes units for all quantities
- [ ] Specifies actors clearly
- [ ] Defines success conditions

## Acceptance Criteria Quality

### Good Acceptance Criteria

Each acceptance criterion should be:

- **Atomic:** Tests one thing
- **Precise:** Clear pass/fail
- **Complete:** Covers the requirement
- **Independent:** Tests can run in any order

### Given/When/Then Format

```text
Given [precondition]
When [action]
Then [expected outcome]
```

**Quality Check:**

- [ ] Given establishes clear context
- [ ] When describes specific trigger
- [ ] Then defines observable outcome
- [ ] Covers happy path and error cases
- [ ] Each AC is independently testable

## Refinement Workflow

### Standard Refinement Process

```text
1. Draft Requirement
   ↓
2. INVEST Assessment (score each criterion)
   ↓
3. Identify Issues (low-scoring criteria)
   ↓
4. Apply Fixes (use patterns below)
   ↓
5. Re-assess (verify improvements)
   ↓
6. Add Acceptance Criteria
   ↓
7. Final Validation
```

### Iteration Patterns

**When Independent fails:**

- Extract dependencies into separate requirements
- Or combine tightly coupled requirements

**When Negotiable fails:**

- Remove implementation details
- Focus on outcomes, not methods

**When Valuable fails:**

- Reframe in user terms
- Connect to business goal

**When Estimable fails:**

- Add constraints and boundaries
- Define scope limits

**When Small fails:**

- Split by user type
- Split by scenario
- Split by CRUD operation

**When Testable fails:**

- Add acceptance criteria
- Define success metrics

## Completeness Validation

### Requirement Completeness

A complete requirement includes:

| Element | Description | Required? |
| --- | --- | --- |
| ID | Unique identifier | Yes |
| Title | Brief descriptive title | Yes |
| Description | Full requirement text | Yes |
| Priority | MoSCoW level | Yes |
| Acceptance Criteria | Testable conditions | Yes |
| Dependencies | Related requirements | If any |
| Assumptions | Underlying assumptions | If any |
| Constraints | Limitations | If any |

### Specification Completeness

A complete specification includes:

- [ ] All functional requirements identified
- [ ] Non-functional requirements included
- [ ] Edge cases considered
- [ ] Error handling specified
- [ ] Security requirements addressed
- [ ] Performance criteria defined
- [ ] Accessibility requirements included
- [ ] All requirements prioritized
- [ ] Dependencies mapped
- [ ] Assumptions documented

## Quick Commands

| Action | Command |
| --- | --- |
| Assess requirement quality | `/spec:validate <path>` |
| Refine requirements | `/spec:refine <path>` |
| Audit specification | `/spec:audit <path>` |

## Related Skills

- `ears-authoring` - EARS pattern authoring
- `gherkin-authoring` - Given/When/Then criteria
- `canonical-spec-format` - Canonical specification structure
- `spec-management` - Specification workflow hub

## References

**Detailed Documentation:**

- [INVEST Criteria](references/invest-criteria.md) - INVEST principles with examples
- [Refinement Patterns](references/refinement-patterns.md) - Refinement techniques
- [Completeness Checklist](references/completeness-checklist.md) - Validation checklist

---

**Last Updated:** 2025-12-24

## Version History

- **v1.0.0** (2025-12-26): Initial release

---
