---
name: food-analyzer
description: >
  Analyze food photos, nutrition labels, and ingredient lists. Trigger on food images,
  nutrition label scans, macro questions, glycemic questions, medication interaction checks,
  and similar food-analysis requests.
version: 1.3.0
---

# Food Analyzer

## Intent

Analyze food photos, labels, meals, and ingredient lists with nutrition, fitness, glycemic, processing, and interaction context.

## Do Not Use When

- Do not use for diagnosis, treatment, allergy clearance, medication changes, or exact nutrition claims from unclear images.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Workflow

1. Identify the exact task and available source material.
2. Apply the domain rules and output format in this skill.
3. State assumptions, uncertainty, and missing inputs clearly.
4. Return the requested artifact, recommendation, or review in a practical format.
5. Check the result against the validation checklist before finishing.

## Constraints

- Do not fabricate missing facts, measurements, dates, sources, or user context.
- Keep output aligned with Mick's direct, practical communication style unless the skill says otherwise.
- Preserve safety, legal, medical, financial, and operational boundaries stated in this file.
- Prefer concise, usable output over broad explanation.

Analyze images of food, plated meals, nutrition labels, or ingredient lists and return a
structured nutritional breakdown with fitness, glycemic, processing, and interaction context.

## Trigger When

- The user starts with `fa` or `food`
- The user uploads an image of food, a meal, a label, or an ingredient list
- The user asks to analyze food, scan a label, estimate calories or macros, check blood sugar impact, or check medication compatibility
- The user wants two foods or meals compared
- The user wants repeated meal patterns reviewed across multiple analyses

## Input Modes

Detect which mode applies from the visible input:

| Mode | What Claude Sees | Behavior |
| --- | --- | --- |
| Meal or Plate | Actual food, plated dish, restaurant item | Estimate calories and macros from visual portion heuristics |
| Nutrition Label | FDA-style Nutrition Facts panel | Extract exact values from the label |
| Ingredient List | Text ingredients | Flag allergens, additives, and processing red flags |
| Mixed | Label and product both visible | Prefer label data over visual estimates |
| Comparison | Two foods, two labels, or two meals visible or described | Compare tradeoffs side by side before giving a recommendation |
| History Review | Multiple prior meals or repeated food summaries provided | Find patterns across repeated analyses rather than analyzing one item only |

If no image is attached and the request depends on visual inspection, ask for a photo before proceeding.

## Output Sections

Include the sections that apply to the identified food:

- Quick Summary
- Nutrition Estimate
- Fitness Alignment
- Ingredient Flags
- NOVA Ultra-Processed Food Score
- Blood Sugar Impact
- Meal Timing Assessment
- Medication and Supplement Interactions
- Notes
- Healthier Alternatives when the food scores poorly

## Goal Aware Modes

Infer the best mode unless the user explicitly gives one:

- `fat loss`
- `endurance fueling`
- `muscle gain`
- `blood sugar control`

Use the selected goal to change the emphasis:

- `fat loss`: satiety, calories, protein density, hidden calorie load, and appetite control
- `endurance fueling`: digestibility, carb availability, sodium, hydration fit, and workout timing
- `muscle gain`: protein quality, total calories, carb support, recovery fit, and meal composition
- `blood sugar control`: glycemic load, fiber, meal pairing, ultra-processed signals, and timing caution

## Core Rules

- Use visible label data when available
- Estimate visually only when label data is not available
- State confidence clearly
- Separate obvious observations from low confidence guesses when the image or label is incomplete
- Use the FDA 2,000 kcal reference diet for percent daily values unless the user provides custom targets
- Keep medication and supplement warnings factual and end that section with a pharmacist and physician disclaimer
- Omit swap suggestions when the food scores well overall

## Output Expectations

The analysis should be structured, readable, and practical. It should cover:

- calories, protein, carbs, fat, fiber, sugar, and sodium
- percent daily values where applicable
- additive and allergen flags when ingredients are visible
- NOVA classification and the factors that drove it
- glycemic index or load estimates when relevant
- timing fit for pre-workout, post-workout, before bed, with medication, or general use
- clinically significant medication or supplement interactions
- practical supplement stacking cautions when the meal plus supplement combination could create issues
- quantified healthier swaps when needed

Start with a short quick summary that is easy to scan before the deeper analysis.

Use a structure like:

```text
Quick Summary
- Overall fit: [short line]
- Best use case: [short line]
- Biggest concern: [short line]
- Confidence: [high, medium, low]
```

## Confidence Levels

- High: label clearly readable and values extracted directly
- Medium: recognizable dish and portion size reasonably visible
- Low: partial view, obscured label, layered dish, or unusual item

When confidence is not high:

- label direct observations as `Observed`
- label uncertain inferences as `Lower confidence estimate`
- do not present guesses as facts

## Reference Standards

Use these as defaults unless the user provides custom targets:

- Calories: 2,000 kcal
- Total Fat: 78g
- Saturated Fat: 20g
- Cholesterol: 300mg
- Sodium: 2,300mg
- Total Carbohydrate: 275g
- Dietary Fiber: 28g
- Total Sugars: 50g
- Protein: 50g
- Vitamin D: 20mcg
- Calcium: 1,300mg
- Iron: 18mg
- Potassium: 4,700mg

## NOVA Guidance

Classify foods by processing level:

- NOVA 1: unprocessed or minimally processed
- NOVA 2: processed culinary ingredients
- NOVA 3: processed foods
- NOVA 4: ultra-processed foods

When ingredients are visible, scan for marker additives such as emulsifiers, artificial sweeteners, artificial colors, preservatives, industrial thickeners, flavor compounds, and modified starches. If uncertain between two NOVA groups, prefer the higher group and note the uncertainty.

## Ingredient Risk Grouping

When ingredients are visible, group concerns under clearer buckets:

- additives and preservatives
- sweeteners
- seed oils and refined fats
- ultra-processed signals
- allergen or sensitivity flags

Use the grouping to make the ingredient section easier to scan instead of listing everything as one flat set of warnings.

## Glycemic Guidance

Use:

- Low GI: under 55
- Medium GI: 56 to 69
- High GI: 70 and above

Estimate glycemic load as `(GI x net carbs per serving) / 100` and consider modifiers such as fiber, fat, protein, vinegar, cooking method, particle size, ripeness, and food form.

## Comparison Mode

When the user provides two foods or meals:

- compare them side by side
- identify the practical tradeoffs instead of pretending one is universally best
- call out which one fits better for the inferred goal mode
- end with a short recommendation based on the stated or inferred goal

## Meal Timing Guidance

Adjust meal timing guidance based on likely use:

- `pre workout`: lighter digestion, lower GI burden when needed, accessible carbs, and tolerance
- `post workout`: protein support, carb refeed potential, sodium and hydration fit when relevant
- `bedtime`: digestion load, satiety, blood sugar steadiness, and sleep disruption risk
- `general daily use`: overall quality, portion fit, and repeatability

If timing is not stated, infer the most relevant use case and say so briefly.

## Supplement Stacking Cautions

When the user mentions supplements, pre-workout, vitamins, minerals, protein powders, energy drinks, or fortified foods, check whether the meal plus supplement combination raises practical issues.

Flag only realistic cautions. Do not invent supplement use that was not shown or stated.

Common stacking issues to check:

- caffeine stacking from coffee, energy drinks, pre-workout, fat burners, or highly caffeinated foods
- stimulant plus high sugar combinations that may worsen jitters, reflux, appetite swings, or blood sugar swings
- calcium, magnesium, iron, zinc, or high fiber meals that can interfere with absorption when taken together
- fat-soluble supplements such as vitamins A, D, E, K, or fish oil that may fit better with a meal containing fat
- high sodium meals plus electrolyte supplements when total sodium may be excessive
- protein powder plus a high protein meal when the result is redundant rather than useful
- creatine, pre-workout, or electrolyte timing around training when the meal timing makes the stack less practical
- alcohol plus sedating supplements, sleep aids, or blood sugar sensitive supplements

Use a concise output when relevant:

```text
Supplement Stacking Caution
- Issue: [meal + supplement combination]
- Practical concern: [absorption, stimulant load, GI tolerance, redundancy, sodium load, blood sugar, or sleep]
- Better timing: [short adjustment]
- Confidence: [high, medium, low]
```

End this section with the same pharmacist and physician disclaimer used for medication and supplement interaction notes.

## Portion Scaling

When the user asks for a different serving size, or the analysis is for meal prep:

- scale calories and macros linearly for half, double, or N-serving batches and show the per-serving and total lines
- do not scale glycemic load advice linearly without comment; portion size changes the practical impact, so note when a doubled portion moves the meal into a different GI burden category
- for meal prep batches, give the per-container numbers and a note on how many containers the batch yields

## Logging Export

When the user wants the analysis saved to notes or a tracker, output a compact log entry after the analysis:

```text
food_log:
  date: [date]
  meal: [name]
  serving: [size]
  calories: [kcal]
  protein_g: / carbs_g: / fat_g: / fiber_g: / sugar_g: / sodium_mg:
  nova: [1-4]
  goal_fit: [short line]
  confidence: [high/medium/low]
```

Use Markdown bullets instead when the user mentions Obsidian or notes. Keep field names stable across exports so entries can be aggregated later.

## Restaurant Ordering Guidance

When the user is choosing from a menu or describes a restaurant meal with no label:

- treat all estimates as medium confidence at best and say so
- give category-level guidance: grilled protein plus a vegetable side beats fried or sauced defaults in most fat loss and blood sugar contexts; pasta and rice bowls are the usual hidden-calorie leaders; dressings and sauces on the side cut the largest unknown
- when the user names the cuisine, give the 2 to 3 best-fit orders for their goal mode and the one trap order to avoid
- skip moralizing; the output is which order fits the goal, not whether eating out is good

## Meal History Review

When the user provides repeated meals or multiple prior analyses:

- look for patterns in protein intake, carb quality, processed food load, sugar load, sodium, and timing fit
- identify recurring wins and recurring issues
- keep the review evidence based and practical
- end with 2 to 3 focused adjustments rather than a giant rewrite of the whole diet

## User Preference Memory

When the user gives stable preferences or recurring issues, carry them forward within the conversation:

- favorite foods
- foods they tolerate well
- foods that repeatedly cause problems
- sensitivities
- recurring supplement interactions

Use those preferences to refine later recommendations, but say when a conclusion still has low confidence.

## Validation Checklist

- [ ] Label data takes precedence over estimates when visible
- [ ] Quick summary appears before deeper sections
- [ ] Confidence labels separate direct observations from weaker guesses
- [ ] Goal mode changes the analysis emphasis appropriately
- [ ] Percent daily values use the correct reference unless custom targets were provided
- [ ] Comparison mode highlights tradeoffs instead of forcing one winner
- [ ] Meal timing guidance matches the likely use case
- [ ] Ingredient flags are grouped cleanly
- [ ] Meal history review finds patterns across repeated analyses
- [ ] NOVA classification includes rationale
- [ ] Blood sugar impact is explained, not just labeled
- [ ] Medication and supplement warnings stay factual and include a disclaimer
- [ ] Supplement stacking cautions are included when a stated meal and supplement combination creates a practical issue
- [ ] Healthier swaps appear only when the food scores poorly

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A food photo, label, meal description, or two items to compare.

Example prompts:

- `Use food-analyzer to compare these two lunches for protein, calories, and satiety.`
- `Analyze this meal and tell me whether it fits a lean mass gain day.`
- `Show me an example prompt for using this skill with a food photo or nutrition label.`

