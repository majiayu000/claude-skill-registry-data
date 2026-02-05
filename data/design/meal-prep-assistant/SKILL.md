---
name: meal-prep-assistant
description: Weekly meal prep and shopping assistant that selects 3 recipes with varied proteins, generates categorized shopping lists, and creates meal prep plans distinguishing Sunday prep from weeknight cooking. Use when planning weekly meals or creating shopping lists.
allowed-tools: Read, find_by_name, write_to_file
---

# Meal Prep & Shopping Assistant

This skill helps you plan your weekly meals by selecting recipes, generating organized shopping lists, and creating actionable meal prep plans.

## Instructions

When asked to create a weekly meal plan:

1. **Find Recipes**: Use find_by_name to locate all `.md` files in the `recipes/` folder
2. **Analyze Recipes**: Read each recipe and identify:
   - Recipe name
   - Protein type (vegetarian/vegan, chicken, fish, beef, pork, seafood, etc.)
   - Serving size (default to 4 if not specified)
   - Ingredients with quantities
   - Cooking steps
3. **Select 3 Recipes**: Choose recipes with protein variety
   - Aim for different protein types (e.g., 1 vegetarian, 1 chicken, 1 fish)
   - Vary cooking methods and cuisines when possible
4. **Generate Shopping List**: Combine and organize ingredients by category:
   - **Produce**: Fresh vegetables, fruits, herbs
   - **Proteins**: Meat, poultry, fish, tofu
   - **Dairy & Eggs**: Milk, cheese, yogurt, eggs, butter
   - **Pantry Staples**: Oils, vinegars, spices, dried goods (usually on hand)
   - **Other**: Specialty items, condiments
   - Combine quantities intelligently (e.g., "2 eggs + 3 eggs = 5 eggs")
5. **Create Meal Prep Plan**: For each recipe, identify:
   - **Sunday Prep**: Steps that can be done in advance
     - Chopping vegetables
     - Making marinades/sauces
     - Pre-measuring ingredients
     - Marinating proteins
   - **Weeknight Cooking**: Steps that must be done fresh
     - Final cooking/grilling
     - Plating and serving
     - Time-sensitive preparations
6. **Output Format**: Create a clean, printable markdown file named `weekly-meal-plan-[date].md`

## Output Template

The generated meal plan should follow this structure for optimal printing (fits on 1 sheet, front and back):

```markdown
# Weekly Meal Plan - [Week of Date]

## 📋 This Week's Recipes

### Recipe 1: [Name] (Vegetarian)
- **Servings**: 4
- **Weeknight**: Monday or Tuesday

### Recipe 2: [Name] (Chicken)
- **Servings**: 4
- **Weeknight**: Wednesday or Thursday

### Recipe 3: [Name] (Fish)
- **Servings**: 4
- **Weeknight**: Friday

---

## 🛒 Shopping List

### Produce
- [ ] Item (quantity)
- [ ] Item (quantity)

### Proteins
- [ ] Item (quantity)

### Dairy & Eggs
- [ ] Item (quantity)

### Pantry Staples (Check if you have)
- [ ] Item
- [ ] Item

### Other
- [ ] Item (quantity)

---

## 🍳 Sunday Meal Prep Plan

### Recipe 1: [Name]
**Prep Steps** (30 mins):
1. Step description
2. Step description
**Storage**: How to store prepped items

### Recipe 2: [Name]
**Prep Steps** (20 mins):
1. Step description
**Storage**: How to store

### Recipe 3: [Name]
**Prep Steps** (15 mins):
1. Step description
**Storage**: How to store

**Total Prep Time**: ~1.5 hours

---

## 👩‍🍳 Weeknight Cooking Guide

### Monday/Tuesday: [Recipe 1]
**Cooking Time**: 20-30 mins
1. Take out prepped ingredients
2. Final cooking steps
3. Serve

### Wednesday/Thursday: [Recipe 2]
**Cooking Time**: 25 mins
1. Steps
2. Serve

### Friday: [Recipe 3]
**Cooking Time**: 20 mins
1. Steps
2. Serve
```

## Ingredient Categorization Guidelines

### Produce
- Fresh vegetables (onions, peppers, tomatoes, lettuce, etc.)
- Fresh herbs (parsley, cilantro, basil, etc.)
- Fresh fruits (lemons, limes, apples, etc.)
- Fresh aromatics (garlic, ginger, scallions)

### Proteins
- Meat (beef, pork, lamb)
- Poultry (chicken, turkey)
- Seafood (fish, shrimp, etc.)
- Plant-based proteins (tofu, tempeh, legumes as main protein)

### Dairy & Eggs
- Milk, cream, half-and-half
- Cheese (all types)
- Yogurt, sour cream
- Eggs
- Butter

### Pantry Staples
These are items typically already in the kitchen:
- Oils (olive oil, vegetable oil, sesame oil)
- Vinegars (balsamic, rice, white, apple cider)
- Dried spices and seasonings
- Salt and pepper
- Flour, sugar, baking supplies
- Dried herbs
- Soy sauce, fish sauce, hot sauce
- Canned goods (tomatoes, beans, stock if recipe calls for it)

### Other
- Specialty sauces or condiments
- Wines or spirits for cooking
- Specialty items not in other categories
- Fresh-baked goods (if needed)

## Meal Prep Step Identification

### Can Prep Sunday:
- Chopping vegetables (store in airtight containers)
- Washing and drying lettuce/greens
- Making marinades, dressings, sauces
- Marinating proteins (up to 12-24 hours)
- Pre-measuring dry ingredients
- Making spice blends
- Preparing components that hold well

### Must Do Weeknight:
- Final cooking (grilling, sautéing, roasting)
- Frying or searing (best done fresh)
- Adding delicate herbs or garnishes
- Tossing salads
- Reheating and plating
- Time-sensitive steps that affect texture or freshness

## Best Practices

1. **Recipe Selection**: Aim for variety in:
   - Protein types (vegetarian, chicken, fish, beef, etc.)
   - Cooking methods (grilled, baked, stovetop, etc.)
   - Cuisine styles (Italian, Asian, Mexican, etc.)
   - Complexity (mix simple and elaborate dishes)

2. **Shopping List**: 
   - Combine quantities across recipes
   - Use standard units (cups, tablespoons, pounds, etc.)
   - Include approximate amounts for "to taste" items
   - Note if specialty stores needed

3. **Meal Prep Timing**:
   - Allocate realistic time estimates
   - Batch similar tasks (all chopping together)
   - Note storage containers needed
   - Consider prep order (aromatics last to preserve freshness)

4. **Formatting**:
   - Use clear headers and sections
   - Include checkboxes [ ] for shopping lists
   - Keep it concise for easy printing
   - Use emojis sparingly for visual organization

## Example Usage

**User Request**: "Create my weekly meal plan"

**Process**:
1. Find all recipes in `recipes/` folder
2. Review recipes and identify: 
   - 1 vegetarian option
   - 1 chicken dish
   - 1 fish recipe
3. Parse ingredients and create categorized shopping list
4. Identify Sunday prep steps vs weeknight cooking
5. Generate `weekly-meal-plan-[date].md` file
6. Confirm creation and provide overview

## Version History

- v1.0.0 (2025-11-21): Initial release with recipe selection, shopping list generation, and meal prep planning
