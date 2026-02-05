---
name: evaluation
description: Use when creating or updating agent evaluation suites. Defines eval structure, rubrics, and validation patterns.
---

# Evaluation Skill

Guidelines for creating comprehensive evaluation suites.

## When to Use This Skill

Use this skill when:
- Creating a NEW evaluation suite for a feature
- Updating an EXISTING evaluation suite
- Understanding the evaluation framework patterns
- Writing spec.md, rubric.md, or evaluation files

## Evaluation Framework Overview

All evaluations in `evals/` follow a consistent structure with both **code-based** and **LLM-as-judge** validations.

## spec.md Template

Use this template for all spec.md files:

```markdown
# [Feature Name] Evaluation Specification

## Requirements
Format: `[IS-EVAL-IMPLEMENTED] IDENTIFIER: example case`
- G = matches ground truth
- C = implemented via code
- L = implemented via LLM as judge using rubric
- O = not yet implemented

### [Category Name 1]
- [G] REQ-EVAL-XX-001: Description of first code-based requirement
- [C] REQ-EVAL-XX-002: Description of second code-based requirement

### [Category Name 2]
- [L] REQ-EVAL-XX-003: Description of LLM-judged requirement
- [O] REQ-EVAL-XX-004: Description of LLM-judged requirement

```

**Template Rules:**
- **Identifier Format**: `REQ-EVAL-XX-NNN`
  - `XX` = 2-3 letter eval abbreviation (e.g., AG for action_generation, AS for action_scenarios)
  - `NNN` = Sequential 3-digit number starting at 001
- **Implementation Types**:
  - `[G]` = Ground truth validation (matches expected output)
  - `[C]` = Code-based validation (deterministic checks)
  - `[L]` = LLM-as-judge validation (quality assessment)
  - `[O]` = Not yet implemented (planned for future)
- **Categories**: Group related requirements logically

## rubric.md Template

Use this template for all rubric.md files:

```markdown
# [Feature Name] Reasoning Trace Rubric

## Format
`[PASS/FAIL] RUBRIC-ID: Criterion description`

## Based on: [Concrete example with specific values]

### [Category Name]
- [ ] RUB-XX-001: Specific, objective criterion
- [ ] RUB-XX-002: Another specific criterion
```

**Template Rules:**
- **Identifier Format**: `RUB-XX-NNN` (matches spec.md abbreviation)
- **Categories**: Organize criteria into logical groups
- **Criteria**: Write concrete, objectively verifiable rules, not subjective assessments
- **Specificity**: Reference actual values, fields, or behaviors that can be checked
- **Checkboxes**: Use `- [ ]` format for LLM judge to mark pass/fail
- **Avoid subjective language**: Do not use vague terms; state exactly what to verify