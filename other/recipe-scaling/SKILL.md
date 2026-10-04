---
name: recipe-scaling
description: Scale recipes across portions, batch size, equipment, timing, heat transfer, seasoning, and service workflow without blindly multiplying every value. Use for recipe-scaling requests even when the recipe or original or target yield is missing, and for diagnosing a changed result after scaling a recipe.
license: MIT
---

# Recipe Scaling

## Core Workflow

1. Identify original yield, target yield, and scale factor.
2. Scale ingredients mathematically as a starting point.
3. Re-evaluate ingredients that should not scale linearly, especially salt, spices, leavening, thickeners, alcohol, heat, garnish, and reduction targets.
4. Re-evaluate vessel size, surface area, batch depth, heat transfer, evaporation, and stirring.
5. Adjust workflow, prep, batching, holding, and service timing.
6. Run safety review for cooling, holding, reheating, bulk prep, and vulnerable diners.

## Decision Rules

Scaling is not arithmetic alone. Larger batches often need different pans, staged cooking, longer heating, different reduction behavior, and more conservative seasoning adjustments.

## Output Contract

- Original yield, target yield, and scale factor
- Scaled ingredient quantities
- Nonlinear adjustments
- Equipment and vessel changes
- Timing, heat, and batch workflow changes
- Safety and holding notes
- Verification cues

## References

- Read `references/recipe-scaling-checklist.md` when changing yield, portions, batch size, or service scale.
