---
name: weekly-planning
description: Weekly review and planning. Reviews past week accomplishments, plans upcoming week focus areas. Auto-triggers on phrases like "weekly review", "planera veckan", "veckans planering", "how was my week".
allowed-tools: Bash, Read, Write
---

# Weekly Planning Skill

## Purpose

Provides weekly review and planning workflows that help users reflect on the past week's accomplishments and plan focus areas for the upcoming week. Designed for users with ADHD/AuDHD neurotypes to maintain momentum and perspective.

## Triggers

- **Command**: `/weekly [review|plan]`
- **Auto-triggers**: "weekly review", "planera veckan", "veckans planering", "how was my week", "veckoöversikt", "plan my week", "veckoplanering"

## Critical Rules

- **ALL database operations MUST use `aida-cli.ts`** - See "How to Query Database" section below
- **NEVER use direct SQL queries**
- **NEVER run query modules directly** (e.g., `bun run src/database/queries/tasks.ts`)
- **Use Swedish** for user-facing output (questions, confirmations, summaries)
- **Always use** `getTimeInfo()` for date/time context
- **Read user profile** from `<pkm>/.aida/context/personal-profile.json` via template variables

## Tool Contract

**Allowed CLI Operations:**
- **tasks**: getWeekTasks, getOverdueTasks, getStaleTasks, getTasksByRole (READ ONLY)
- **roles**: getActiveRoles, getRoleById (READ ONLY)
- **journal**: getEntriesByDateRange, createEntry (types: weekly_review, weekly_plan)
- **profile**: getProfile, getAttribute (READ ONLY)

**Forbidden Operations:**
- Creating tasks
- Modifying task status
- Updating profile
- Accessing daily plan (PLAN.md)
- Any delete operations

**Journal Entry Types Allowed:**
- `weekly_review` (review mode)
- `weekly_plan` (planning mode)

**File Access:**
- **Read**: `personal-profile.json`
- **No file writes** - All operations via CLI

## How to Query Database

**ONLY use the `aida-cli.ts` tool for ALL database operations:**

```bash
# CORRECT - Always use this pattern:
bun run src/aida-cli.ts <module> <function> [args...]

# WRONG - NEVER do this:
bun run src/database/queries/tasks.ts getWeekTasks  # ❌ NO!
sqlite3 <pkm>/.aida/data/aida.db "SELECT..."        # ❌ NO!
```

**Available modules:** `tasks`, `roles`, `projects`, `journal`, `journalMd`, `plan`

**Example queries you will need:**
```bash
# Get tasks for a specific week (requires YYYY-MM-DD dates for weekStart and weekEnd)
bun run src/aida-cli.ts tasks getWeekTasks "2025-12-16" "2025-12-22"

# Get overdue tasks
bun run src/aida-cli.ts tasks getOverdueTasks

# Get stale tasks (captured but not activated)
bun run src/aida-cli.ts tasks getStaleTasks

# Get journal entries for date range
bun run src/aida-cli.ts journal getEntriesByDateRange "2025-12-16" "2025-12-22"

# Create journal entry (with JSON argument)
bun run src/aida-cli.ts journal createEntry '{"entry_type":"weekly_review","content":"Weekly reflection"}'

# Get active roles
bun run src/aida-cli.ts roles getActiveRoles
```

## Workflow

### 1. Determine Context

**Get current time via bash:**
```bash
bun run src/aida-cli.ts time getTimeInfo
```

This returns JSON with current time info including `hour`, `minute`, `date`, `weekday`, `weekOfYear`, etc.

Check:
- Current weekday (from `weekdayName` field in JSON output)
- Week of year (from `weekOfYear` field)
- Whether weekly journal entry exists for this week

**Mode Selection:**

If user provides explicit argument to `/weekly`:
- `review` → Force Review Flow
- `plan` → Force Planning Flow

Otherwise, auto-detect based on day of week:
- **Review mode**: Friday, Saturday, or Sunday
- **Planning mode**: Monday, Tuesday, Wednesday, or Thursday

### 2. Review Flow (End of Week)

See [REVIEW-FLOW.md](REVIEW-FLOW.md) for detailed procedure.

**Summary:**
1. Calculate past week date range (Monday-Sunday)
2. Query completed tasks via `tasks.getWeekTasks(weekStart, weekEnd)`
3. Query journal entries via `journal.getEntriesByDateRange(weekStart, weekEnd)`
4. Summarize accomplishments by role
5. Identify patterns (energy levels, productivity peaks)
6. Note what worked well and what challenges occurred
7. Create weekly journal entry (type='weekly_review')
8. Celebrate wins

### 3. Planning Flow (Start of Week)

See [PLANNING-FLOW.md](PLANNING-FLOW.md) for detailed procedure.

**Summary:**
1. Calculate upcoming week date range (next Monday-Sunday)
2. Query overdue tasks via `tasks.getOverdueTasks()`
3. Query stale tasks via `tasks.getStaleTasks()`
4. Query tasks with deadlines this week
5. Review role balance targets
6. Suggest 3-5 weekly focus areas
7. Set realistic expectations per role
8. Create weekly journal entry (type='weekly_plan')
9. Provide motivation

## Query Scripts Available

**From `tasks.ts`:**
- `getWeekTasks(weekStart, weekEnd)` - Get tasks for specific week (requires YYYY-MM-DD dates)
- `getOverdueTasks()` - Get tasks past their deadline
- `getStaleTasks(options?)` - Get tasks captured but not activated
- `getTasksByRole(roleId, options?)` - Get tasks for specific role
- `getTodayTasks()` - Get all tasks relevant for today (grouped by role)

**From `journal.ts`:**
- `getEntriesByDateRange(startDate, endDate)` - Get journal entries for date range (requires YYYY-MM-DD dates)
- `createEntry(input)` - Create new journal entry
- `getTodayEntries()` - Get all journal entries for today

**From `roles.ts`:**
- `getActiveRoles()` - Get all active roles
- `getRoleById(id)` - Get specific role details

## Supporting Documentation

- [REVIEW-FLOW.md](REVIEW-FLOW.md) - Detailed weekly review procedure
- [PLANNING-FLOW.md](PLANNING-FLOW.md) - Weekly planning procedure

## Design Principles

1. **Reflection over judgment** - Celebrate what worked, learn from challenges (no guilt)
2. **Pattern recognition** - Help user see their own productivity patterns
3. **Realistic planning** - Set achievable weekly goals based on past patterns
4. **Role balance** - Ensure attention across all active roles
5. **Energy-aware** - Consider energy patterns when planning week
6. **Non-overwhelming** - Suggest 3-5 focus areas max, not exhaustive list

## Example Invocation

**User**: "Hur gick veckan?"

**Response**:
```
Låt mig granska veckan som gick...

[Queries database via aida-cli.ts]

# Vecka 51 - Sammanfattning

## Accomplishments 🎉

**Developer-rollen** (3 uppgifter färdiga)
- Färdigställde API-dokumentation
- Implementerade ny autentiseringsflow
- Fixade 5 kritiska buggar

**Personal-rollen** (2 uppgifter färdiga)
- Tränade 4 av 5 planerade gånger
- Läste 2 kapitel i "Atomic Habits"

## Patterns jag noterar

- Mest produktiv: Måndag-tisdag förmiddag
- Energidippar: Onsdagar efter lunch
- Bäst för fokusarbete: 08:00-11:00

## Vad fungerade bra?

- Morgonrutinen med /checkin hjälpte dig starta dagen
- 5-minutersregeln fick dig igång när du körde fast

Vill du planera för nästa vecka nu?
```
