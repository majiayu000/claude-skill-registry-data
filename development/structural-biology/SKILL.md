---
name: structural-biology
description: Structural biology analysis including protein structure validation, AlphaFold interpretation, and structural comparisons
---

# Structural Biology Analysis

## When to Use This Skill

- When analyzing protein or molecular structures
- When interpreting AlphaFold predictions
- When comparing experimental vs predicted structures
- When validating crystallographic or cryo-EM models

## Core Topics

This skill covers:

1. **AlphaFold Confidence Interpretation** - Understanding pLDDT scores and prediction reliability
2. **Structure Comparison** - Methods for comparing and aligning structures
3. **Validation Metrics** - Assessing model quality (R-factors, Ramachandran, clashscores)
4. **Interpreting Discrepancies** - Understanding differences between predicted and experimental structures

## Reference Files

For detailed guidance on specific topics, see:

- [alphafold-confidence.md](alphafold-confidence.md) - Interpreting AlphaFold confidence scores
- [comparing-structures.md](comparing-structures.md) - Structure alignment and comparison methods
- [validation-metrics.md](validation-metrics.md) - Quality metrics for structural models
- [interpreting-discrepancies.md](interpreting-discrepancies.md) - Analyzing structural differences

## Key Principles

**Structure quality matters**: Always check validation metrics before drawing biological conclusions.

**Context is crucial**: A "bad" region in a structure might be genuinely disordered, not a modeling error.

**Multiple methods**: Use multiple validation approaches; no single metric tells the whole story.
