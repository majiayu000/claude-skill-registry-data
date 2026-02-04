---
name: updating-dawncaster-filters
description: Use when updating filter options in Dawncaster card/talent browser after game expansions release - systematically checks ALL filter types (categories, rarities, types, banners, expansions) across both HTML dropdowns and JavaScript arrays to prevent missing updates
---

# Updating Dawncaster Filters

## Overview

Systematic workflow for updating filter dropdowns when Dawncaster releases new expansions. Prevents common failure mode: updating only what user mentioned while missing other filter changes.

## When to Use

Use when:
- Dawncaster releases a new expansion
- User requests filter updates on cards.html or talents.html
- Blightbane API has new filter values

Do NOT skip checking all filter types just because user only mentioned one.

## The Iron Law

**Check ALL filter types for EVERY update, even if user only mentions expansion.**

Expansions often add new categories, rarities, and other filter types. Checking only what's mentioned = incomplete update.

## Required TodoWrite Checklist

YOU MUST create TodoWrite items for each filter type. This makes skipping structurally impossible.

```markdown
- [ ] Check categories filter for changes
- [ ] Check types filter for changes
- [ ] Check rarities filter for changes
- [ ] Check banners filter for changes
- [ ] Check expansions filter for changes
- [ ] Update cards.html dropdowns and arrays
- [ ] Update talents.html dropdowns and arrays
```

## Discovery Workflow

### 1. Find Current Filter Options

First, get the current bundle filename:

```bash
# Find the current bundle version
curl -s 'https://blightbane.io' | grep -o 'index.bundle.js?v=[0-9.]*'
```

Then query that bundle to get authoritative filter arrays:

```bash
# Replace VERSION with actual version from above
VERSION="0.20.3"
BUNDLE_URL="https://blightbane.io/js/index.bundle.js?v=${VERSION}"

# Get all filter arrays
curl -s "$BUNDLE_URL" | grep -oP '"Core","Metaprogress"[^]]*\]' | head -1  # Expansions
curl -s "$BUNDLE_URL" | grep -oP '"Action","Item"[^]]*\]' | head -1         # Categories
curl -s "$BUNDLE_URL" | grep -oP '"Common","Uncommon"[^]]*\]' | head -1     # Rarities
curl -s "$BUNDLE_URL" | grep -oP '"Melee","Magic"[^]]*\]' | head -1         # Types
curl -s "$BUNDLE_URL" | grep -oP '"Green","Blue","Red","Purple"[^]]*\]' | head -1  # Banners
```

### 2. Compare Against Current Files

Read cards.html and talents.html to find what's currently there.

cards.html has: categories, types, rarities, banners, expansions
talents.html has: tier (uses rarity API param), expansions

### 3. Identify Differences

For EACH filter type, note:
- What values exist in Blightbane
- What values exist in your files
- What's missing

## Update Pattern

For each new filter value, update TWO places:

### HTML Dropdown
```html
<select id="category">
  <option value="">Category</option>
  <!-- existing options -->
  <option value="20">Mantra</option>  <!-- NEW -->
</select>
```

### JavaScript Mapping Array
```javascript
const getCategoryName = (categoryId) => {
  const categories = [
    "Action",
    // ... existing ...
    "Offering",
    "Mantra",     // NEW - same position as dropdown value
  ];
  return categories[categoryId] || "Unknown";
};
```

**Critical**: Array index MUST match dropdown value.

## Files to Update

- **cards.html**: All five filter types (categories, types, rarities, banners, expansions)
- **talents.html**: Only expansions (talent tier uses rarity param but displays differently)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Only update what user mentioned | Check ALL five filter types every time |
| Update dropdown, forget array | Both must be updated for display to work |
| Time pressure → skip verification | Verification takes 30 seconds, prevents broken site |
| Update cards.html, forget talents.html | talents.html needs expansion updates too |
| Assume user knows what changed | Systematically check Blightbane source |

## Red Flags - You're About to Make a Mistake

- "User only mentioned expansion so I'll just update that"
- "Checking everything is overkill"
- "Time pressure justifies skipping verification"
- "I'll update the dropdown quickly"
- "Probably just expansion changed"

**All of these mean: STOP. Check all filter types systematically.**

## Complete Workflow Example

```bash
# 1. Discover current Blightbane filters (all types)
# 2. Read cards.html and talents.html
# 3. Compare each filter type
# 4. Update HTML dropdowns
# 5. Update JavaScript arrays
# 6. Verify both files updated
```

## Why This Matters

Incomplete updates = users can't filter new content = site appears broken.

Systematic checking takes 2 extra minutes. Debugging "why aren't new cards showing?" takes 20.
