---
name: llmn
description: Interactive meal planning wizard. Use when user wants to create a meal plan, optimize their diet, set up nutritional constraints, or find foods that meet their goals. Triggers on requests like "create a meal plan", "optimize my diet", "help me plan meals", "I want to lose weight", "high protein diet".
---

# Meal Planning Wizard

This skill guides users through creating an optimized meal plan using the `llmn` CLI tool. It uses quadratic programming to find diverse food combinations that satisfy nutritional constraints.

## Optimization Modes

Choose the right mode based on user needs:

| Mode | Command | Best For |
|------|---------|----------|
| **Template-based** (recommended) | `--template --pattern X` | Realistic meals with proper structure |
| Multi-period | `--multiperiod` | Exact per-meal nutrient control |
| Single-period | (default) | Daily totals only |

**Template-based is recommended** for most users because it produces meals that look like what humans actually eat (1 protein + 1 legume + vegetables per meal).

## Workflow

### Step 0: Check for Existing User Profile

Before gathering goals, check if the user has an existing profile:

```bash
uv run llmn user show --json
```

**If profile exists with goal set** (e.g., `goal: "fat_loss:185:165"`):
- Extract current weight and target weight from the goal
- Offer to use stored targets: "I see you have a profile for fat loss (185 lbs → 165 lbs). Should I use those targets?"
- If user agrees, skip to Step 2 and use `--use-profile` flag in Step 4
- If user wants different targets, continue to Step 1

**If profile exists without goal:**
- Use profile's age, sex, height, weight, activity for calculations
- Ask only about goal type and calorie/protein targets

**If no profile exists:**
- Continue to Step 1 to gather all information
- After optimization, suggest creating a profile: `llmn user create`

### Step 1: Gather User Goals

**IMPORTANT: Always confirm calorie and protein targets with the user BEFORE running any optimization.**

Ask the user about their dietary goals. Use the AskUserQuestion tool to collect:

1. **Diet type** (one of):
   - Omnivore (eats everything)
   - Pescatarian (fish + eggs, no meat)
   - Vegetarian (eggs + dairy, no meat/fish)
   - Vegan (plant-based only)

2. **Diet style** (one of):
   - Standard (balanced macros)
   - Slow-carb (legumes as carbs, no white carbs/fruit)
   - Low-carb (reduced carbohydrates)
   - High-protein (muscle building focus)
   - Mediterranean (olive oil, fish, vegetables)

3. **Goal** (one of):
   - Weight loss / Cutting (1600-1800 cal, 150g protein)
   - Muscle gain / Bulking (2800-3200 cal, 180g protein)
   - Maintenance (2200-2400 cal, 120g protein)
   - Custom (user specifies)

4. **Calorie range**: Get min/max daily calories

5. **Protein target**: Get minimum daily protein in grams

### Step 2: Check Available Foods

Search for foods that match the user's diet type:

```bash
# Check what staple foods are already tagged
uv run llmn tags list --tag staple --json
```

If few staples are tagged, suggest running the tagging workflow or offer to tag common foods for their diet type.

### Step 3: Create Constraint Profile

Create a YAML profile file at `/tmp/llmn_profile.yaml`:

```yaml
name: user_custom_plan
description: "Custom plan - [diet_type] [diet_style] [goal]"

calories:
  min: <cal_min>
  max: <cal_max>

nutrients:
  protein:
    min: <protein_min>
  fiber:
    min: 30
  sodium:
    max: 2300

include_tags:
  - staple

exclude_tags:
  - exclude

options:
  max_grams_per_food: 500
```

For low-carb diets, add:
```yaml
  carbohydrate:
    max: 100
```

### Step 4: Run Optimization

**Recommended: Template-based optimization** (produces realistic meals):

```bash
# Map diet type to pattern
# - Pescatarian → --pattern pescatarian
# - Vegetarian → --pattern vegetarian
# - Vegan → --pattern vegan
# - Omnivore → --pattern mediterranean (or paleo)

# Map diet style to additional pattern
# - Slow-carb → --pattern slow_carb
# - Low-carb/Keto → --pattern keto
```

**If user has a profile with goal set (from Step 0):**
```bash
# Use --use-profile to auto-derive calorie/protein targets from stored user data
uv run llmn optimize --pattern pescatarian --template --use-profile --json
```

**If no profile or user wants custom targets:**
```bash
# Use explicit --goal flag with weight info
uv run llmn optimize --pattern pescatarian --template --goal "fat_loss:185lbs:165lbs" --json
```

**Alternative: YAML profile-based optimization** (most control):

```bash
uv run llmn optimize --file /tmp/llmn_profile.yaml --json
```

### Step 5: Present Results

Parse the JSON output and present to the user:
- List of foods with amounts in grams
- Total calories and protein achieved
- Any binding constraints (at their limits)
- Suggestions from the optimizer

If optimization fails (infeasible), explain which constraints conflict and suggest relaxations.

### Step 6: Iterate

Ask if the user wants to:
- Adjust constraints and re-run
- Exclude specific foods they don't like
- Add more foods to their staples
- Generate a recipe prompt for Claude

## Key Commands Reference

```bash
# Search for foods
uv run llmn search "chicken" --json

# Get food nutrient details
uv run llmn info <fdc_id> --json

# Tag a food as staple
uv run llmn tags add <fdc_id> staple

# Template-based optimization (recommended)
uv run llmn optimize --pattern pescatarian --template --json
uv run llmn optimize --pattern pescatarian --pattern slow_carb --template --seed 42 --json

# Profile-based optimization
uv run llmn optimize --file /tmp/profile.yaml --json

# What-if analysis
uv run llmn explore whatif --base latest --add "protein:min:200" --json

# Export for recipe generation
uv run llmn export-for-llm latest
```

## Available Patterns

| Pattern | Description |
|---------|-------------|
| `pescatarian` | Fish + eggs, no meat |
| `vegetarian` | Eggs + dairy, no meat/fish |
| `vegan` | Plant-based only |
| `keto` | High fat, very low carb |
| `mediterranean` | Olive oil, fish, vegetables |
| `paleo` | No grains/legumes/dairy |
| `slow_carb` | Legumes as carbs, no white carbs |

Patterns can be combined: `--pattern pescatarian --pattern slow_carb`

## Common Food IDs for Quick Tagging

### Proteins
- 175167: Salmon (Atlantic, raw)
- 175159: Tuna (bluefin, raw)
- 171287: Eggs (whole, raw)
- 171077: Chicken breast (raw)
- 172421: Lentils (cooked)
- 173757: Chickpeas (cooked)

### Vegetables
- 168462: Spinach (raw)
- 169967: Broccoli (raw)
- 168421: Kale (raw)
- 170108: Bell peppers (raw)

### Fats
- 171705: Avocado (raw)
- 748608: Olive oil
- 170567: Almonds (raw)

## Example Session

User: "I want to lose weight, I'm pescatarian"

1. Ask: calorie target? (suggest 1600-1800 for weight loss)
2. Ask: protein target? (suggest 150g for satiety)
3. Run template-based optimization:
   ```bash
   uv run llmn optimize --pattern pescatarian --pattern slow_carb --template --goal "fat_loss:185lbs:165lbs" --json
   ```
4. Show results with per-meal breakdown:
   - Breakfast: Eggs 150g, Edamame 100g, Kale 100g
   - Lunch: Cod 235g, Kidney beans 216g, Zucchini 161g
   - Dinner: Salmon 170g, Lentils 113g, Carrots 149g
   - Snack: Peanuts 30g
5. Offer to: adjust constraints, exclude foods, or generate recipes
