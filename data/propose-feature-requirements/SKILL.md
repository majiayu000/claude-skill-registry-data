---
name: propose-feature-requirements
description: Create or update feature requirements specification using EARS notation with examples and appendices
---

# Propose Feature Requirements Skill

## Purpose

Create a formal requirements specification for a feature using EARS notation. This translates the concept into testable, specific requirements.

## When to Use

- Feature concept exists and is approved
- Need to specify exactly what the system must do
- Ready to define functional and non-functional requirements

## Prerequisites

- Feature concept document exists in `docs/features/NNNN-feature-name/concept.md`
- Concept has been reviewed and approved
- User understands the feature scope

## Procedure

### 1. Verify Concept Exists

```bash
# Check that concept exists
ls ./docs/features/NNNN-feature-name/concept.md
```

If it doesn't exist, use `propose-feature-concept` skill first.

### 2. Check for Idea Honing Document

```bash
ls ./planning/NNNN-feature-name/idea-honing.md 2>/dev/null
```

If it exists, review it for insights that inform requirements. The Q&A may reveal edge cases and constraints.

### 3. Copy Requirements Template

```bash
cp ./docs/features/0000-templates/requirements.md ./docs/features/NNNN-feature-name/
```

### 4. Determine Requirements Prefix

Choose a short prefix (2-5 characters) for requirement IDs:
- Should be descriptive of the feature
- Examples: `SEM` for semantic-search, `REG` for registry-management
- Will be used like `SEM-1`, `SEM-2`, etc.

### 5. Fill in Overview

Write a brief description of what this specification covers. Reference the concept document.

### 6. Define Functional Requirements

For each requirement, use EARS format:

```
**WHILE** [state or condition]
**WHEN** [trigger or event]
**THEN** the system **SHALL** [required behavior]
```

Add inline examples only if truly small (1-3 lines):
```
key = "value"
```

For larger examples, note them for appendices.

### 7. Define Non-Functional Requirements

Add performance, usability, security, or other quality requirements:

```
**WHILE** [operating condition]
**THEN** the system **SHALL** [performance requirement]
```

**Scalability prompts** (ask these for each major operation):
- What happens when there are 1000x more items? 1M files? 10M rows?
- Should memory usage scale with data size, or stay constant?
- What's the acceptable latency? Does it degrade with scale?

These questions surface constraints that will become Critical Constraints in the design phase.
If an operation must be O(1) memory or O(log n) time, state it here.

### 8. Define Error Handling

Specify how errors should be handled:

```
**WHILE** [operation in progress]
**WHERE** [error condition occurs]
**THEN** the system **SHALL** [error handling behavior]
```

### 9. Add Appendices

For larger examples that would clutter requirements:
- API response schemas
- Configuration file formats
- Data structures
- Protocol specifications

Each appendix should be clearly labeled:
```
## Appendix A: API Response Schema
## Appendix B: Configuration File Format
```

### 10. Review for Completeness

Ensure:
- All requirements use EARS keywords
- Requirements are testable and specific
- Inline examples are truly small
- Larger examples are in appendices
- Requirements have unique IDs with the chosen prefix

## Validation

Verify the requirements document:

```bash
# Check file exists
ls ./docs/features/NNNN-feature-name/requirements.md

# Verify it has content
head -50 ./docs/features/NNNN-feature-name/requirements.md

# Check for EARS keywords
grep -E "WHILE|WHEN|WHERE|THEN|SHALL" ./docs/features/NNNN-feature-name/requirements.md
```

## Common Issues

**Missing EARS keywords**: Every requirement should use WHILE/WHEN/WHERE/THEN/SHALL.

**Too vague**: Requirements should be specific enough to test.

**Inline examples too large**: Move anything over 3 lines to an appendix.

**Inconsistent prefix**: All requirement IDs should use the same prefix.

## Next Steps

After creating requirements:
1. Review for completeness and testability
2. Get feedback from implementors
3. Once requirements are solid, move to design using `propose-feature-design` skill
