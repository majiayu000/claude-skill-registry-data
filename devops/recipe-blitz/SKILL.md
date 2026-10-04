---
name: recipe-blitz
description: Rapid-fire batch recipe capture. Bare minimum fields per recipe, flesh out later. Capture 5-10 recipes in one session. Use when user says "recipe blitz", "let me dump a bunch of recipes", "batch recipes", or wants to capture multiple recipes quickly.
user-invocable: true
---

# Recipe Blitz - Batch Recipe Capture

David has 500+ recipes in his head. Brain Dump captures one at a time with full detail. Recipe Blitz captures many with bare minimum fields, fast.

## Trigger Conditions

Auto-fire when:

- User says "recipe blitz", "batch recipes", "dump a bunch of recipes"
- User wants to capture multiple recipes in one sitting
- `/brain-dump` ends and user wants to keep going fast

## How It Works

Uses the same infrastructure as `/brain-dump` (`lib/ai/remy-brain-dump-pipeline.ts`, `lib/recipes/actions.ts`, `lib/recipes/ingredient-parser.ts`) but in minimal-field mode.

## Step 1: Enter Blitz Mode

```
RECIPE BLITZ MODE
━━━━━━━━━━━━━━━━
Rapid capture. Bare minimum per recipe:
  - Name
  - Category (app/main/dessert/side/sauce/other)
  - Key ingredients (rough list, no amounts needed)
  - 1-2 sentence method summary

Go as fast as you want. Say "done" when finished.
I'll number them as we go.

Recipe #1:
```

## Step 2: Capture Loop

For each recipe the user dumps:

1. Parse the stream (name, category, ingredients, brief method)
2. Confirm with a compact one-liner:
   ```
   #1: Chocolate Lava Cake (dessert) - 7 ingredients - Got it.
   Recipe #2:
   ```
3. Do NOT show full structured output (that's brain-dump's job)
4. Do NOT ask for clarification on amounts, steps, or details
5. Keep the loop tight. Minimum friction.

If user gives more detail than minimum, capture it. But never demand it.

## Step 3: Batch Summary

When user says "done", "that's it", or "finished":

```
BLITZ COMPLETE
━━━━━━━━━━━━━
Captured 8 recipes:

  #1  Chocolate Lava Cake         dessert    7 ingredients
  #2  Truffle Risotto             main       9 ingredients
  #3  Burrata Salad               app        5 ingredients
  #4  Lobster Bisque              soup       11 ingredients
  #5  Creme Brulee                dessert    5 ingredients
  #6  Pan-Seared Halibut          main       6 ingredients
  #7  Chimichurri                 sauce      6 ingredients
  #8  Roasted Beet Salad          salad      8 ingredients

Save all 8? [y/n/pick numbers]
```

## Step 4: Batch Save

On confirmation, save all via `lib/recipes/actions.ts`:

- Create each recipe with minimal fields
- Link ingredients via `lib/recipes/ingredient-parser.ts` (best-effort matching)
- If PIE can price any ingredients, auto-cost them
- Mark recipes as "draft" or "needs detail" so they show up in a refinement queue

```
Saved 8 recipes (draft). 47 ingredients linked. 31 priced via PIE.
Flesh out later with /brain-dump [recipe name].
```

## Refinement Mode

If user says "flesh out #3" or "detail the burrata":

- Switch to full `/brain-dump` mode for that single recipe
- Pre-fill what was captured in blitz
- Ask for amounts, detailed steps, notes

## Speed Tips

- If user rattles off ingredients comma-separated, parse them all
- Chef shorthand is expected: "mire, fond, chiffonade, brunoise"
- "The usual suspects" for a cuisine = infer common base ingredients but mark as [inferred]
- If user gives a recipe that sounds like a variation of an existing one, note it: "Similar to #2 Truffle Risotto. Variation or separate?"

## Key Files

- Brain dump pipeline: `lib/ai/remy-brain-dump-pipeline.ts`
- Brain dump schema: `lib/ai/brain-dump-intent-schema.ts`
- Entity resolver: `lib/ai/brain-dump-entity-resolver.ts`
- Recipe actions: `lib/recipes/actions.ts`
- Ingredient parser: `lib/recipes/ingredient-parser.ts`
- Recipe scaling: `lib/scaling/recipe-scaling-engine.ts`

## Rules

- NEVER demand precision. This is speed mode. "Chicken, lemon, herbs, garlic" is enough.
- NEVER show full structured output per recipe. That kills the flow.
- NEVER ask "are you sure?" per recipe. Batch confirm at the end.
- Keep the loop under 2 lines of response per recipe.
- If user gives a dish name only with zero ingredients, accept it. Name-only recipes are valid drafts.
- Always offer to flesh out individual recipes after blitz via `/brain-dump`.
