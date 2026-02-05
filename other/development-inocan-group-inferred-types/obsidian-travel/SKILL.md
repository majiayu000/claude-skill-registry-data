---
name: obsidian-travel
description: Create or update a travel plan in the Obsidian vault Travel folder
---

# Obsidian Travel Planning

Manage travel plans in `~/dev/personal/obsidian/trobrock/Travel/`.

## Create New Trip

When asked to plan a trip:

1. **Gather details** (if not provided):
   - Trip name/destination
   - Purpose (Personal or Business)
   - Approximate dates
   - Who's traveling
   - Budget considerations

2. **Create the file** at `~/dev/personal/obsidian/trobrock/Travel/{Trip Name}.md`

3. **Use this template:**

```markdown
---
status: Planning
purpose: Personal
date_start: YYYY-MM-DD
date_end: YYYY-MM-DD
url: ""
---

# {Trip Name} {emoji}

## Trip Overview

| Detail | Info |
|--------|------|
| **Travelers** | {who} |
| **Destination** | {where} |
| **Duration** | {X days/weeks} |
| **Dates** | {Month DD - Month DD, YYYY} |
| **Budget** | {amount or TBD} |

## To Do

- [ ] Book flights
- [ ] Book accommodations
- [ ] Research activities
- [ ] Pack

## ✈️ Flights

*To be booked*

## 🏨 Accommodations

*To be booked*

## 📅 Itinerary

### Day 1 - {Date}
- 

### Day 2 - {Date}
- 

## 📝 Notes

```

## Trip Status Workflow

```
Planning → Booked → Done
```

- `Planning` - Still figuring out details, not fully committed
- `Booked` - Flights/hotels are reserved
- `Done` - Trip completed

## Best Practices

1. **Use emoji** in headings for visual scanning (✈️ 🏨 📅 🚗 🍽️)
2. **Tables** for structured info like trip overview
3. **Checklists** for to-do items and packing lists
4. **Sections** for flights, accommodations, each day's itinerary
5. **Date format** - Always YYYY-MM-DD in frontmatter, but human-readable in content

## Research Support

When helping research a trip, gather and organize:
- Flight options and points strategies
- Hotel recommendations
- Activities and attractions
- Restaurant suggestions
- Local tips

Add research findings directly to the appropriate sections.

## Verification

- [ ] File is in `Travel/` folder
- [ ] Frontmatter has status, purpose, date_start, date_end, url
- [ ] Dates are YYYY-MM-DD format
- [ ] Status is one of: Planning, Booked, Done
- [ ] Purpose is one of: Personal, Business
