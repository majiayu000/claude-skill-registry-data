---
name: fec-refactoring-inheritance
description: Use when behavior-preserving frontend refactoring focuses on legacy OO hierarchies, subtype responsibilities, superclass extraction/collapse, or delegation, and the selected technique needs family-specific mechanics, risks, and JavaScript/TypeScript/React/Vue adaptation.
---

# Inheritance Refactorings

## Overview
Use this family after evidence identifies a fitting structural transformation. Apply one primary technique at a time and verify immediately.

## Procedure
1. Confirm the selected technique and its preconditions in [Inheritance Refactorings](references/inheritance-refactorings.md).
2. Record affected behavior and a diff budget.
3. Apply only the selected technique's smallest viable step.
4. Verify the step before composing another transformation.
5. Stop and reassess when public contracts, lifecycle, state identity, or actual scope exceed expectations.

## Quick Reference
The family reference contains 11 canonical techniques with intent, signals, avoid conditions, mechanics, preservation checkpoints, smell links, composition hints, JavaScript/TypeScript notes, React/Vue notes, adaptation guidance, and original frontend examples.

## Common Mistakes
- Choosing a technique by name without checking its preconditions.
- Combining several structural intentions in one diff.
- Assuming a classical class-based form is mandatory in modern frontend code.
- Treating passing tests as proof when the relevant behavior is not covered.
