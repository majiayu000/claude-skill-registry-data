---
name: spec-reviewer
description: |
  Quality gate for product specifications before stakeholder review. Use this skill when:
  - A spec draft is ready and you want to validate it before sending to Engineering, Design, and QA
  - You want to check a spec against your template's completeness rules
  - You need to catch vague language, missing sections, or gaps before review
  - You want a pass/fail scorecard with specific fix suggestions
---

# Spec Reviewer

Validate a product specification against quality standards. Outputs a pass/fail scorecard with actionable fix suggestions — designed to run before sending specs for cross-functional review.

## Workflow

1. **Read the spec** — Read the target spec file
2. **Read the template** — Cross-reference against your spec template
3. **Run all checks** — Apply every check category below
4. **Generate scorecard** — Output results table with pass/fail per check
5. **List fixes** — For each FAIL, provide a specific, actionable fix suggestion

## Check Categories

### 1. Section Completeness
Verify every required section exists and is not empty or placeholder-only. Common required sections:
- Objective/Problem Statement
- Scope (in-scope AND out-of-scope)
- User Personas
- Functional Requirements
- User Stories (all 4 paths: happy, edge, error, empty)
- Non-Functional Requirements
- Success Metrics

### 2. Vague Language Detection
Flag these patterns (each is a WARN):

**Vague adjectives/adverbs:**
- "fast", "quick", "slow" -> specify milliseconds
- "user-friendly", "intuitive" -> specify interaction steps
- "soon", "later" -> specify date or phase
- "large", "small", "many" -> specify quantities
- "etc.", "and so on" -> enumerate all items

**Vague verbs:**
- "handle", "process", "manage" -> specify the exact operation
- "support" -> specify what exactly and how
- "improve", "enhance" -> specify the metric and target

### 3. Requirement IDs
- Every user story has a unique ID
- Every acceptance criterion has a unique ID
- No duplicate IDs
- Sequential numbering

### 4. Story Coverage
Each functionality block should have stories covering:
- Happy path
- Edge cases
- Error states
- Empty states

### 5. Consistency Checks
- Same concept uses same term throughout
- Referenced sections actually exist
- Date format is consistent

## Scorecard Output Format

```markdown
# Spec Review Scorecard

**Spec:** {file path}
**Reviewed:** {date}
**Overall:** {PASS / FAIL / PASS WITH WARNINGS}

## Results

| # | Check | Section | Status | Details |
|---|-------|---------|--------|---------|
| 1 | Completeness | Objective | PASS | Answers who, what, why |
| 2 | Completeness | Scope | FAIL | Out-of-scope table empty |
| 3 | Vague language | Requirements | WARN | "fast response" needs ms target |

## Summary
- **Total checks:** {N}
- **PASS:** {N}
- **FAIL:** {N}
- **WARN:** {N}

## Fix List (Ordered by Severity)

### FAIL — Must Fix
1. **{Section} — {Issue}**
   {Specific fix instruction}

### WARN — Should Fix
1. **{Section} — {Issue}**
   {Specific fix instruction}
```

## Grading Rules

- **PASS**: Zero FAILs, zero or more WARNs
- **PASS WITH WARNINGS**: Zero FAILs, 1+ WARNs
- **FAIL**: 1+ FAILs

## Anti-Patterns

- Don't pass specs with empty out-of-scope sections — scope creep follows
- Don't accept "TBD" in critical sections — flag as FAIL
- Don't ignore vague language — it causes misalignment during build

## Quality Checklist

- [ ] All required sections checked
- [ ] Vague language scan completed
- [ ] Story coverage verified (4 paths)
- [ ] Requirement IDs validated
- [ ] Fix list is specific and actionable
