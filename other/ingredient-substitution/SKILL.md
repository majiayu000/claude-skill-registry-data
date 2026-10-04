---
name: ingredient-substitution
description: Evaluate ingredient substitutions and adaptations by function, flavor, texture, chemistry, dietary constraint, and side effects.
license: MIT
---

# Ingredient Substitution

## Core Workflow

1. Identify the missing, unwanted, or constrained ingredient.
2. Determine its function in the dish.
3. Separate flavor match from structural, moisture, acidity, leavening, emulsification, starch, fat, sweetness, and salt functions.
4. Recommend the best available substitute with ratio or adjustment when possible.
5. Explain expected tradeoffs and any technique changes.
6. Activate `food-safety` for allergen, medical diet, spoilage, or unsafe substitution issues.

## Decision Rules

Do not treat ingredients as interchangeable only because they share a category. Buttermilk in pancakes, marinades, and salad dressing may need different replacements.

## Output Contract

- Original ingredient and function
- Recommended substitute
- Ratio or adjustment
- Flavor, texture, moisture, acidity, and structure tradeoffs
- Technique changes
- Safety or dietary cautions

## References

- Read `references/ingredient-substitution-checklist.md` when substituting, omitting, or adapting ingredients.
