---
name: fec-refactoring-catalog
description: Use when selecting or composing behavior-preserving refactoring techniques after structural evidence is known, especially when multiple candidate transformations, preconditions, or ordering choices must be compared.
---

# Refactoring Catalog Selection

## Overview
Use the complete catalog as a decision aid, not as a list of automatic recipes. Select the smallest technique whose preconditions fit the evidence and behavior contract.

## Workflow
1. Locate the standard technique in [the catalog index](references/catalog-index.md).
2. If starting from a smell or symptom, use [the selection guide](references/selection-guide.md) to compare causes and alternatives.
3. If several transformations are needed, use [the composition guide](references/composition-guide.md) to order only the prerequisites that fit the current code.
4. Load the referenced family detail only when the technique is selected.

## Selection Rules
- A smell can have several valid candidates; determine the actual cause first.
- Prefer reversible, local transformations over broad redesign.
- Check public API, routing, state ownership, async/lifecycle, persistence, and SSR boundaries before execution.
- Treat composition edges as conditional relationships, never mandatory pipelines.

## Quick Reference
| Need | Reference |
| --- | --- |
| All 61 techniques | [Catalog index](references/catalog-index.md) |
| Choose by symptom/cause | [Selection guide](references/selection-guide.md) |
| Order related techniques | [Composition guide](references/composition-guide.md) |
