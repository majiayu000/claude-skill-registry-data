---
name: brain-dump
description: Stream-of-consciousness recipe capture. David talks, AI structures it into a recipe with ingredients, steps, and yield. No precision required on first pass. Use when user says "brain dump", "let me tell you a recipe", "I make this dish", or starts describing how to cook something.
user-invocable: true
---

# Brain Dump - Recipe Capture

David has 500+ recipes in his head. This skill gets them out, fast. No precision needed on first pass.

## Trigger Conditions

Auto-fire when:

- User says "brain dump", "let me tell you about a recipe"
- User starts describing how to cook something
- User says "I make this...", "for the [dish], I..."
- User wants to document a recipe from memory

## How It Works

The Remy Brain Dump Pipeline already exists (`lib/ai/remy-brain-dump-pipeline.ts`). It handles:

1. Chunking free text
2. Extracting intents (events, clients, menus, recipes)
3. Resolving entities
4. Building action plans
5. Executing actions

For RECIPE-SPECIFIC brain dumps, we streamline: capture the stream, structure it, save it.

## Step 1: Prompt for the Dump

If user hasn't already started talking, prompt:

```
BRAIN DUMP MODE
━━━━━━━━━━━━━━
Talk about the dish. Stream of consciousness. Include whatever comes to mind:
- What it's called
- Rough ingredients (amounts don't need to be exact)
- How you make it (your way, not a textbook)
- How many it serves
- Any tricks or variations
- What you serve it with

Go. I'll structure it after.
```

## Step 2: Receive and Parse

Take whatever the user says (could be messy, incomplete, chef shorthand) and use the brain dump pipeline or local Ollama to extract:

- **Name**: dish name
- **Category**: appetizer, main, dessert, side, sauce, etc.
- **Yield**: servings or portions
- **Ingredients**: name + approximate quantity (parse chef shorthand: "a couple lbs", "handful", "splash")
- **Steps**: ordered preparation steps (translate chef-speak to readable instructions)
- **Notes**: tricks, variations, pairings, storage tips
- **Tags**: cuisine type, dietary flags, season, difficulty

## Step 3: Structure and Confirm

Show the structured recipe back:

```
CAPTURED: Chocolate Lava Cake
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Category: Dessert
Yield: 6 individual cakes

INGREDIENTS:
  8 oz   dark chocolate (70%+)
  1 cup  butter (2 sticks)
  4      eggs
  4      egg yolks
  1/2 c  sugar
  2 tbsp flour
  pinch  salt

STEPS:
  1. Melt chocolate and butter together, let cool slightly
  2. Whisk eggs, yolks, and sugar until thick
  3. Fold chocolate mixture into eggs
  4. Add flour and salt, fold gently
  5. Pour into buttered ramekins (3/4 full)
  6. Bake 425F for 12-14 min (edges set, center jiggles)
  7. Rest 1 min, invert onto plate

NOTES:
  - Can prep ramekins night before, refrigerate, add 2 min to bake time
  - Center should be molten. If it's set through, it's overcooked.

TAGS: dessert, chocolate, French, impressive, date-night

Save this recipe? [y/n]
```

## Step 4: Save

On confirmation, save via the recipe creation actions:

- Use `lib/recipes/actions.ts` to create the recipe
- Link ingredients via ingredient parser (`lib/recipes/ingredient-parser.ts`)
- If PIE can price the ingredients, auto-cost it

```
Saved: Chocolate Lava Cake
  -> 7 ingredients linked
  -> Estimated cost: $4.82/serving (via PIE)
  -> Ready for menu assignment
```

## Batch Mode Hint

If user wants to dump multiple recipes fast, tell them about `/recipe-blitz`:

```
Want to keep going? Say "/recipe-blitz" for rapid-fire mode (bare minimum fields, flesh out later).
```

## Key Files

- Brain dump pipeline: `lib/ai/remy-brain-dump-pipeline.ts`
- Brain dump schema: `lib/ai/brain-dump-intent-schema.ts`
- Entity resolver: `lib/ai/brain-dump-entity-resolver.ts`
- Action planner: `lib/ai/brain-dump-action-planner.ts`
- Recipe actions: `lib/recipes/actions.ts`
- Ingredient parser: `lib/recipes/ingredient-parser.ts`
- Recipe scaling: `lib/recipes/recipe-scaling.ts`

## Rules

- NEVER demand precision. "A couple pounds" is fine. "Some butter" is fine. Structure it best you can.
- Chef shorthand is expected: "brunoise the mire", "mount with butter", "deglaze with wine". Keep the language.
- If critical info is missing (no dish name, no ingredients at all), ask. Otherwise, fill gaps with reasonable defaults.
- Always offer to save. Never auto-save without confirmation.
- If the recipe already exists (by name match), ask if this is a variation or replacement.
