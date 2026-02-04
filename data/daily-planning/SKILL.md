---
name: daily-planning
description: Context-aware daily check-ins for morning planning, midday adjustments, and evening reviews. Use when the user wants to plan their day, check in on progress, or review their evening. Auto-triggers on phrases like "plan my day", "morning planning", "let's check in", "how's my day going", "evening review".
allowed-tools: Bash, Read, Write
---

# Skill: daily-planning

## Purpose

Provides context-aware daily check-ins that adapt based on time of day, existing plan, and user energy. Helps structure the day with minimal cognitive overhead through morning planning, midday adjustments, and evening reviews.

## Trigger Conditions

- **Slash command:** `/checkin`
- **Natural phrases:** ["plan my day", "morning planning", "morgonplanering", "let's check in", "how's my day going", "kolla läget", "evening review", "kvällsreflektion", "day review"]
- **Auto-trigger:** Time-based (morning/midday/evening detection)

## Required Context (gather BEFORE starting workflow)

1. Time period via `profile getCurrentTimePeriod` → returns "morning"|"midday"|"evening"
2. Plan exists via `plan planHasContent` → returns true|false
3. Today's check-ins via `journal getTodayEntries` → filter for entry_type="checkin"
4. Today's tasks via `tasks getTodayTasks` → returns Map<roleId, Task[]>
5. Energy level via `profile getCurrentEnergyLevel` → returns "high"|"medium"|"low"
6. Overdue tasks via `tasks getOverdueTasks` → returns Task[]

**How to gather context:**
```bash
# Get time period
bun run src/aida-cli.ts profile getCurrentTimePeriod

# Check if plan exists
bun run src/aida-cli.ts plan planHasContent

# Get today's journal entries
bun run src/aida-cli.ts journal getTodayEntries

# Get today's tasks
bun run src/aida-cli.ts tasks getTodayTasks

# Get current energy level
bun run src/aida-cli.ts profile getCurrentEnergyLevel

# Get overdue tasks
bun run src/aida-cli.ts tasks getOverdueTasks
```

## Workflow Steps

### Flow Selection (first match wins)

| Condition | Flow |
|-----------|------|
| time >= 18:00 AND plan exists AND has check-in | Evening |
| time 11:00-17:59 AND plan exists | Midday |
| Otherwise (morning OR no plan OR first check-in) | Morning |

### Morning Flow

See [MORNING-FLOW.md](MORNING-FLOW.md) for detailed procedure.

**Summary:**
1. Action: Display task summary by role
2. Output: Energy-matched focus suggestions (1-3 items)
3. Wait for: User confirms focus items and scheduled events
4. Action: Create plan via `plan createDailyPlan {...}`
5. Action: Log check-in via `journal createEntry {"entry_type":"checkin",...}`
6. Output: First action suggestion

### Midday Flow

See [MIDDAY-FLOW.md](MIDDAY-FLOW.md) for detailed procedure.

**Summary:**
1. Review progress vs morning plan
2. Query completed tasks since morning
3. Ask about current energy level
4. Adjust remaining priorities if needed
5. Update journal entry (type='checkin')
6. Suggest next action

### Evening Flow

See [EVENING-FLOW.md](EVENING-FLOW.md) for detailed procedure.

**Summary:**
1. Summarize day's accomplishments
2. Note what rolled over (not completed)
3. Create reflection journal entry (type='reflection')
4. Archive plan to log via `plan archivePlanToLog`
5. Clear daily plan via `plan clearDailyPlan`
6. Optionally prepare tomorrow's focus

## Output Format

- **Language:** Swedish (default)
- **Style:** Concise, encouraging, non-judgmental
- **Focus items:** 1-3 maximum, never full task list
- **Energy awareness:** Match suggestions to current energy level

**Example morning output:**
```
God morgon! ☀️

Idag ser jag tre fokusområden baserat på din energi:

1. **Färdigställ arkitekturdokumentation** (Developer)
   - Hög energi på morgonen - perfekt för detta
   - Deadline: idag

2. **Team standup 09:00** (Work)
   - Förberedelsetid: 10 minuter

3. **Träning** (Personal)
   - Schemalagt: 18:00

Vad ska vi börja med först?
```

## Error Handling

- **If `profile getCurrentTimePeriod` returns null:** Default to "morning" flow
- **If `tasks getTodayTasks` returns empty:** Show message "Inga uppgifter för idag. Vill du lägga till någon?" and suggest task-capture
- **If `plan planHasContent` fails:** Assume no plan exists, run Morning flow
- **If `journal createEntry` fails:** Log error to console, continue workflow, inform user that logging failed but plan was created
- **If no roles exist:** Guide user to profile-management skill to set up roles first
- **If profile doesn't exist:** Guide user to profile-management skill with message "Du behöver först skapa en profil. Vill du göra det nu?"

## Anti-patterns

- **NEVER create tasks directly** - use task-capture skill
- **NEVER modify task status** - use task-activation skill or let user do it
- **NEVER show all tasks** - always filter to 1-3 focus items based on energy and priority
- **NEVER skip energy matching** when suggesting tasks
- **NEVER write directly to** `0-JOURNAL/1-DAILY/*.md` (auto-generated from database)
- **NEVER delete data** - only archive or clear as specified in workflow
- **NEVER use direct SQL** - always use aida-cli.ts
- **NEVER run query modules directly** (e.g., `bun run src/database/queries/tasks.ts`)

## Tool Contract

**Allowed CLI Operations:**
- **plan:** planHasContent, readDailyPlan, createDailyPlan, archivePlanToLog, clearDailyPlan
- **tasks:** getTodayTasks, getOverdueTasks, getTaskById (READ ONLY)
- **roles:** getActiveRoles, getRoleById (READ ONLY)
- **journal:** getTodayEntries, createEntry (types: checkin, reflection)
- **profile:** getCurrentTimePeriod, getCurrentEnergyLevel, getProfile (READ ONLY)

**Forbidden Operations:**
- Creating tasks (use task-capture skill)
- Modifying task status (user action or task-activation skill)
- Updating profile (use profile-management skill)
- Deleting any data

**File Access:**
- **Read:** `0-JOURNAL/PLAN.md`, `personal-profile.json`
- **Write:** `0-JOURNAL/PLAN.md` only (overwritten morning, cleared evening)
- **Never write:** `0-JOURNAL/1-DAILY/*.md` (generated from database)

## Supporting Documentation

- [MORNING-FLOW.md](MORNING-FLOW.md) - Detailed morning check-in procedure
- [MIDDAY-FLOW.md](MIDDAY-FLOW.md) - Midday adjustment procedure
- [EVENING-FLOW.md](EVENING-FLOW.md) - Evening closure procedure
- [ENERGY-MATCHING.md](ENERGY-MATCHING.md) - How to match tasks to energy levels

## Design Principles

1. **Activation over perfection** - Help START the day, not just plan it
2. **One thing at a time** - Suggest 1-3 focus items max, never the full list
3. **Energy-aware** - Match task suggestions to user's energy patterns
4. **Non-judgmental** - Frame progress positively, deferrals as rescheduling
