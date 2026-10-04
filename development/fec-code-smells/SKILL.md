---
name: fec-code-smells
description: Use when diagnosing structural maintainability problems in existing frontend code before deciding how to refactor it, especially when evidence, false-positive checks, and candidate transformations are needed without editing business code.
---

# Code Smell Diagnosis

## Overview
Diagnose structural problems from concrete evidence. A smell is a prompt to investigate, not proof that code must change.

## Procedure
1. Establish the requested scope and project facts.
2. Collect concrete structural and change-coupling evidence.
3. Match evidence against [the smell catalog](references/smell-catalog.md).
4. Apply [false-positive checks](references/detection-guide.md).
5. Report confidence, impact, and candidates from [the mapping guide](references/smell-to-refactoring-map.md).
6. If the request is diagnosis-only, do not modify business code.

## Finding Contract
Every finding states location, evidence, smell ID/name, impact, confidence (`HIGH`, `MEDIUM`, `LOW`), candidate refactorings, priority, and material false-positive considerations. `LOW` confidence is never an automatic-edit signal.

## Quick Reference
| Need | Reference |
| --- | --- |
| Standard 24-smell model | [Smell catalog](references/smell-catalog.md) |
| Evidence and false positives | [Detection guide](references/detection-guide.md) |
| Candidate refactorings | [Smell-to-refactoring map](references/smell-to-refactoring-map.md) |

## Common Mistakes
- Treating a metric threshold as proof.
- Reporting a smell without a file/symbol and evidence.
- Treating every loop, switch, comment, wrapper, or pipeline as defective.
- Editing code when the user asked for diagnosis only.
