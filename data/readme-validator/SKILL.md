---
name: readme-validator
description: Validates that skills in this repository are accurately documented in the README. Use when verifying skill documentation or during pre-commit validation.
---

# README Skill Validator

## Purpose

This skill validates that the README.md accurately documents all skills in the repository.

## Validation Process

When asked to validate a skill's documentation:

1. **Read the skill's SKILL.md** to understand:
   - The skill's `name` from frontmatter
   - The skill's `description` from frontmatter
   - What the skill actually does (from the body)

2. **Read the README.md** and find the skill's entry in the "Our Skills" section

3. **Verify the documentation**:
   - The skill name must appear in the README
   - The README description should accurately reflect what the skill does
   - Key capabilities should be mentioned

4. **Output format** (IMPORTANT: follow exactly):
   - If valid: Output only the word `VALID`
   - If invalid: Output `INVALID:` followed by a brief explanation of what needs to be fixed

## Examples

### Valid output
```
VALID
```

### Invalid output
```
INVALID: The README says this skill "generates reports" but the SKILL.md shows it only formats existing data.
```

```
INVALID: Skill "data-processor" is not documented in the README "Our Skills" section.
```
