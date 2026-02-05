---
name: order-daycare-lunch
description: Manage school lunch ordering for preschool with catered meals. Analyzes menus based on preferences (avoid rice, prefer BBQ and mac & cheese), helps select meals, processes orders from any source (PDF/screenshot/browser/verbal), and generates calendar reminders for days when lunch needs to be packed. Use when discussing school meals, menu selection, or packing lunch.
allowed-tools: Bash, Read, mcp__claude-in-chrome__*
---

# Preschool Lunch Ordering

Help manage lunch ordering for a preschool student who receives catered lunches. This includes analyzing menus, helping select meals based on preferences, processing orders, and generating calendar reminders for days when lunch needs to be packed.

## Quick Reference

**Key Preferences:**

- **Avoid**: Rice-based meals (100% avoidance)
- **Avoid**: Pasta dishes (except mac & cheese and Alfredo)
- **Prefer**: BBQ items, mac & cheese, chicken nuggets, Alfredo pasta, pizza, breakfast items

For complete preferences, see [references/PREFERENCES.md](references/PREFERENCES.md).

## Site Information

- **Service**: Boonli (ChefAdvantage)
- **URL**: https://chefadvantage.boonli.com/home

## Browser Automation Flow

1. **Landing**: Navigate to home URL, click month button (e.g., "JAN: PRESCHOOL")
2. **Builder**: Use Previous/Next Day arrows; select "Daily Feature - (PS)" under Combos
3. **Quick Pick**: Click star icon in Review Selections panel to order multiple days at once
   - If coordinate click fails: `document.querySelector('.fa-star').click()`
4. **Checkout**: Click "Add and Go To Cart" then "CHECKOUT"
   - **Stop at payment** - user enters payment details

## Workflow

### 1. Menu Analysis

When user shares a menu (PDF, screenshot, browser, photo, or verbally):

1. Identify meals to **skip** based on preferences
2. Highlight **recommended** meals
3. Flag new items that might contain rice
4. Note when favorite items appear

**Proactively warn** about rice-based meals - this is the primary constraint.

**Output as a full-month table** showing every school day with action (ORDER/PACK/CLOSED) and menu item:

```
| Date | Day | Action | Menu Item |
|------|-----|--------|-----------|
| Dec 1 | Mon | ORDER | Mac 'n Cheese |
| Dec 2 | Tue | PACK | Rice dish (avoid) |
| Dec 3 | Wed | CLOSED | Holiday |
```

This format makes it easy to order and audit the full month at a glance.

### 2. Order Processing

After order placement, extract from confirmation (any format):
- Order month and year
- List of dates food was ordered

### 3. Generate Calendar File

Once you have ordered dates:

1. Calculate skipped days = School days (Mon-Fri, excluding holidays) - Ordered days
2. Generate calendar reminders:
   ```bash
   python scripts/generate_ics.py -m [MONTH] -y [YEAR] -d [SKIPPED_DAYS] --child-name "[NAME]"
   open pack-lunch-[month]-[year].ics
   ```

Creates "Pack [Name]'s Lunch" events for each skipped day.

## Notes

- **Timezone**: America/New_York
- Exclude major holidays (Thanksgiving, July 4, MLK Day, etc.)
