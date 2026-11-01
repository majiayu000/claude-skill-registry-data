---
name: cozi
description: Interact with Cozi Family Organizer (shopping lists, todo lists, item management). Unofficial API client for family organization.
metadata:
  openclaw:
    emoji: 📋
    requires:
      bins: [node]
      env: [COZI_EMAIL, COZI_PASSWORD]
  minis:
    originalSource: "https://clawskills.sh/skills/angusthefuzz-cozi"
    convertedAt: "2026-10-31T22:10:29.492Z"
    license: "Unknown"
---

# Cozi Skill

Unofficial client for Cozi Family Organizer API. Manage shopping lists and todo lists.

⚠️ **Important:** This uses an unofficial API (reverse-engineered). Cozi may change it at any time.

## Environment Variables

Set these in your agent's `.env` (`~/.openclaw/.env`) or create a skill-level `.env` at `~/.openclaw/skills/cozi/.env`:

- `COZI_EMAIL` — Your Cozi account email
- `COZI_PASSWORD` — Your Cozi account password

The script only reads `COZI_EMAIL` and `COZI_PASSWORD` from `.env` files — other variables are ignored.

## Commands

```bash
# Lists
node ~/.openclaw/skills/cozi/scripts/cozi.js lists                    # Show all lists
node ~/.openclaw/skills/cozi/scripts/cozi.js list <listId>            # Show specific list
node ~/.openclaw/skills/cozi/scripts/cozi.js add <listId> "item text"  # Add item
node ~/.openclaw/skills/cozi/scripts/cozi.js check <listId> <itemId>   # Mark complete
node ~/.openclaw/skills/cozi/scripts/cozi.js uncheck <listId> <itemId> # Mark incomplete
node ~/.openclaw/skills/cozi/scripts/cozi.js remove <listId> <itemId>  # Remove item
node ~/.openclaw/skills/cozi/scripts/cozi.js new-list "title" [type]   # Create list (shopping|todo)
node ~/.openclaw/skills/cozi/scripts/cozi.js delete-list <listId>      # Delete list

# Calendar
node ~/.openclaw/skills/cozi/scripts/cozi.js calendar [year] [month]   # Show month (defaults to current)
node ~/.openclaw/skills/cozi/scripts/cozi.js cal [year] [month]         # Alias
node ~/.openclaw/skills/cozi/scripts/cozi.js add-appt YYYY-MM-DD HH:MM HH:MM "subject" [location] [notes]
node ~/.openclaw/skills/cozi/scripts/cozi.js remove-appt <year> <month> <apptId>
```

## Examples

```bash
# See all lists and their items
node ~/.openclaw/skills/cozi/scripts/cozi.js lists

# Add milk to the shopping list
node ~/.openclaw/skills/cozi/scripts/cozi.js add abc123 "Organic milk"

# Mark item as bought
node ~/.openclaw/skills/cozi/scripts/cozi.js check abc123 item456

# Create a new todo list
node ~/.openclaw/skills/cozi/scripts/cozi.js new-list "Weekend chores" todo

# View this month's calendar
node ~/.openclaw/skills/cozi/scripts/cozi.js cal

# View specific month
node ~/.openclaw/skills/cozi/scripts/cozi.js cal 2026 3

# Add an appointment
node ~/.openclaw/skills/cozi/scripts/cozi.js add-appt 2026-02-20 14:00 15:30 "Doctor appointment" "Rochester General"
```

## Session Caching

The script caches your session token in `~/.openclaw/skills/cozi/.session.json` to avoid re-authenticating every call. Tokens expire — it will re-auth when needed.

## API Details

- Base URL: `https://rest.cozi.com/api/ext/2207`
- Auth: Bearer token from username/password login
- Lists endpoint: `/api/ext/2004/{accountId}/list/`

Based on [cozi-api-client](https://github.com/BrandCast-Signage/cozi-api-client) and [py-cozi](https://github.com/Wetzel402/py-cozi).