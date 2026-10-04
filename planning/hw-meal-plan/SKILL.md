---
name: hw-meal-plan
version: 1.0.0
description: Build a balanced, preference-aware meal plan for a stated wellness goal using general nutrition principles.
author: matrixx0070
tags: [nutrition, meal-plan, wellness, diet, planning]
capabilities: []
---

This is general wellness information, not medical diagnosis or treatment. Consult a licensed healthcare professional or registered dietitian for symptoms, conditions, medications, allergies, pregnancy, or before major diet changes.

## When to use

Use this when someone gives you a concrete goal (fat loss, muscle gain, maintenance, more energy), their food preferences, and any hard constraints, and wants a structured multi-day eating plan.

**Not for:** clinical diets for diagnosed disease (diabetes, kidney disease, eating disorders), prescribing supplements or macros for a medical condition, or extreme/very-low-calorie protocols. Refer those to a clinician or RD.

## Method

1. Collect inputs: goal, bodyweight, activity level, dietary pattern (omnivore/vegetarian/vegan/etc.), allergies/dislikes, meals per day, budget, cooking time.
2. Estimate an energy target. Decision point: cutting → modest deficit (~10-20% below maintenance); gaining → modest surplus (~10%); maintaining → maintenance. If any input is missing, state the assumption you used.
3. Set protein first: ~1.6-2.2 g/kg bodyweight for active goals, lower for sedentary maintenance. Fill remaining calories with fats (~20-35% of total) and carbs.
4. Decision point: if allergy/dislike conflicts with a staple, swap for an equivalent (protein↔protein, carb↔carb) before proceeding.
5. Distribute across meals; anchor each around a protein, a fiber-rich carb, vegetables, and a fat source.
6. Add hydration and a flexible "free choice" slot so the plan survives real life.
7. Provide 2-3 swap options per meal so it is repeatable, not a one-off.

## Example

Goal: fat loss, 70 kg lightly active, omnivore, no shellfish, 3 meals + 1 snack. Assumed maintenance ~2,300 kcal → target ~1,950 kcal, protein ~140 g. Breakfast: Greek yogurt + oats + berries. Lunch: chicken, rice, mixed veg, olive oil. Snack: cottage cheese + fruit. Dinner: salmon, potatoes, salad. Swap: chicken↔turkey, salmon↔tofu.

## Pitfalls

- Setting an aggressive deficit that kills adherence — slower is more sustainable.
- Under-shooting protein, then wondering why hunger and muscle loss appear.
- Building a rigid plan with zero swaps; boredom breaks it within days.
- Ignoring stated allergies/budget/time — the "perfect" plan they can't follow is worthless.

## Output format

```
GOAL: <goal> | TARGET: ~<kcal> kcal, ~<g> protein/day
ASSUMPTIONS: <maintenance estimate, missing inputs>

DAY TEMPLATE
- Breakfast: <meal>  (swap: <a> / <b>)
- Lunch: <meal>      (swap: <a> / <b>)
- Snack: <meal>      (swap: <a> / <b>)
- Dinner: <meal>     (swap: <a> / <b>)
Hydration: <target>  | Free slot: <note>

GROCERY LIST: <items>
NOTE: General wellness info, not medical advice — see an RD/clinician before major changes.
```
