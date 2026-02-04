---
name: ridwell
description: Manage your Ridwell recycling account - check upcoming pickups, opt in/out of pickup events, view special/rotating categories, and answer questions about what items Ridwell accepts. Use when the user asks about Ridwell pickups, recycling categories, item classification, or wants to manage their Ridwell service.
version: 1.0.0
---

# Ridwell Integration

Your complete interface for managing Ridwell recycling pickups and understanding what they accept.

## What This Skill Does

1. **Pickup Management**: View upcoming pickups, opt in/out of events
2. **Special Categories**: See what rotating/featured categories are coming
3. **Item Classification**: Answer "does Ridwell take X?" questions
4. **Account Info**: Check account status and subscription details

## Quick Reference

**IMPORTANT**: The script uses a built-in virtual environment. Call the script directly (do NOT use `python` or `python3` prefix):

### Check Pickups
```bash
# Next pickup with items
~/.claude/skills/ridwell/scripts/ridwell_client.py next

# All upcoming pickups
~/.claude/skills/ridwell/scripts/ridwell_client.py pickups

# Featured categories for each pickup (with alternatives)
~/.claude/skills/ridwell/scripts/ridwell_client.py featured
```

### Opt In/Out
```bash
# First get the event ID from pickups command, then:
~/.claude/skills/ridwell/scripts/ridwell_client.py opt-in <event_id>
~/.claude/skills/ridwell/scripts/ridwell_client.py opt-out <event_id>
```

### Account Info
```bash
~/.claude/skills/ridwell/scripts/ridwell_client.py account
```

## Item Classification

When users ask "does Ridwell take X?", refer to [what-we-take.md](references/what-we-take.md).

### Core Categories (Always Accepted)
- **Plastics**: Multi-layer plastic, film, caps, clamshells, pill bottles, bread tags
- **Clothing**: Worn textiles, clothes, shoes
- **Electronics**: Small electronics, cables, batteries, lightbulbs
- **Household**: Corks, kitchenware, latex paint, styrofoam, glass

### Rotating Categories
Change quarterly. Run the `special` command to see current options.

### NOT Accepted
- Hazardous materials (chemicals, solvents, motor oil)
- Medical waste (needles, medications)
- Food waste
- Construction debris
- Large appliances

## Common User Questions

### "What's my next Ridwell pickup?"
Run the `next` command and summarize the date and items.

### "Opt me into the next pickup"
1. Run `next` to get the event_id
2. Run `opt-in <event_id>`
3. Confirm success

### "What special category is coming up?"
Run the `special` command and list the rotating categories with their dates.

### "Does Ridwell take [item]?"
1. Check [what-we-take.md](references/what-we-take.md)
2. If item is in a core category, yes
3. If unclear, suggest checking ridwell.com/what-we-take for their address

### "How do I [process question]?"
Refer to [faqs.md](references/faqs.md) for common procedures.

## Setup Requirements

**Environment Variables** (must be set in ~/.zshrc):
```bash
export RIDWELL_EMAIL="your@email.com"
export RIDWELL_PASSWORD="your-password"
```

**Python Package**: Already installed in the skill's virtual environment at `~/.claude/skills/ridwell/.venv/`. No additional installation needed.

## API Limitations

This skill CANNOT:
- Change which special/rotating category you've selected
- Modify item quantities
- Create new pickup events

These actions require the Ridwell website or app.

## Reference Files

- [what-we-take.md](references/what-we-take.md) - Items Ridwell accepts
- [faqs.md](references/faqs.md) - Common pickup questions
- [api-reference.md](references/api-reference.md) - Script command reference

## Examples

**User**: "When is my next Ridwell pickup?"
**Action**: Run `next` command, report date and items

**User**: "I want to skip the next pickup"
**Action**: Run `next` to get event_id, then `opt-out <event_id>`

**User**: "Can I recycle chip bags with Ridwell?"
**Answer**: Yes, chip bags are multi-layer plastics, a core category

**User**: "What's the featured category this month?"
**Action**: Run `featured` command, report the featured category for each upcoming pickup

**User**: "What are my next featured categories?"
**Action**: Run `featured` and summarize:
- Jan 6: Essential hygiene items
- Jan 20: Holiday lights
- Feb 3: Empty Play-Doh Containers
- etc.

**User**: "What alternatives can I choose instead?"
**Action**: The `featured` output shows alternatives like: Bottle caps, Cords/chargers, Portable devices, Corks, Pill bottles, Bread tags

**User**: "Does Ridwell take motor oil?"
**Answer**: No, Ridwell does not accept hazardous materials like motor oil
