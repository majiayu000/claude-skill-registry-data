---
name: ingredient-knowledge
description: Reason about ingredient properties, functions, flavor roles, storage, and cooking behavior. Use when ingredient choice or behavior affects the culinary answer.
license: MIT
---

# Ingredient Knowledge

## Core Workflow

1. Identify the ingredient and its form, freshness, preparation state, and amount.
2. Determine its functional role in the dish: flavor, moisture, fat, acid, sweetness, salt, structure, starch, protein, aroma, color, or garnish.
3. Explain how heat, time, acidity, salt, cutting size, and storage affect the ingredient.
4. Flag safety, spoilage, allergy, or storage concerns when relevant.
5. Connect ingredient behavior to the user's goal rather than listing encyclopedia facts.

## Decision Rules

Ingredient categories are not automatically interchangeable. Evaluate function before recommending use, omission, or substitution.

When an ingredient affects troubleshooting or recovery, connect its function to the state gap. For example, explain whether the ingredient changes salt concentration, acidity, moisture, fat, starch, protein, aroma, structure, or perceived balance before recommending an adjustment.

## Output Contract

- Ingredient role
- Relevant properties
- Cooking or storage behavior
- Fit for the user's dish or goal
- Risks, tradeoffs, or constraints
- State effect and verification cue when used in troubleshooting
- Related substitution or technique implications

## References

- Read `references/ingredient-knowledge-checklist.md` when ingredient function, behavior, or storage changes the decision.
