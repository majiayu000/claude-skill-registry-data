---
name: Morning Brief Generator
description: Generate User's daily morning brief when he asks for "morning brief", "daily brief", "brief", or "what's my day look like". Compiles weather, calendar, priorities, project status, YourPet care checklist, and Cabinet quick check.
---

# Morning Brief Generator

Generate a comprehensive morning brief for User to start his day with clarity and focus.

## When to Use This Skill

Auto-invoke when User says any of:
- "morning brief"
- "daily brief"
- "generate brief"
- "what's my day look like"
- "brief for today"

## What to Generate

Create a structured daily briefing document in `reflections/daily/YYYY-MM-DD.md` with:

### 1. Header
- Date and day of week
- Week number of year

### 2. Weather & Environment
- Check for Austin, TX weather (use web search if needed)
- Temperature and conditions
- Air quality index

### 3. Calendar
- Read User's calendar if available
- List meetings and time blocks
- Note any conflicts or travel time

### 4. Priority Stack (Top 3)
- Read `projects/INDEX.md` to identify:
  - Primary project (🔴 highest priority)
  - Secondary project (🟠 medium priority)
  - Maintenance project (🟡 lower priority)
- For each: name, next milestone, current status, any blockers

### 5. Project Status
- Parse all projects from `projects/INDEX.md`
- Show status, next milestone, blockers for each

### 6. YourPet Care Checklist
- Morning walk (30 min)
- Evening walk (30 min)
- Training session (if applicable)
- Vet/grooming (if scheduled)

### 7. Cabinet Quick Check
- **Atlas (Operations):** System health, capacity check
- **Banker (Finance):** Any financial decisions today
- **Strategist (Career):** Career actions or networking
- **Spartan (Defense):** Workout scheduled, physical goals

### 8. Notes Section
- Yesterday's carry-over tasks
- Today's intention (one thing to make today great)
- Blockers to clear

### 9. Art Practice
- Session planned (yes/no and time)
- Focus area (anatomy, gesture, perspective, etc.)
- NMA course progress

## Implementation Approach

**Option 1: Use existing Python script**
- Execute `python .system/scripts/morning_brief.py`
- This generates the base structure
- Then enhance with web search for weather and additional context

**Option 2: Generate directly**
- Read `projects/INDEX.md` for project data
- Use web search for Austin weather
- Create markdown file directly in `reflections/daily/`

**Recommended:** Use Option 1 (Python script) for consistency, then enhance with real-time data.

## Output Format

Save to: `reflections/daily/YYYY-MM-DD.md`

Use markdown with clear sections, emoji for visual parsing, and task checkboxes where appropriate.

## Context Files to Reference

- `projects/INDEX.md` - Project priorities and status
- `.system/context/preferences.md` - User's working style and priorities
- Previous daily notes in `reflections/daily/` - Yesterday's carry-over

## Tone

- Direct and actionable
- Focused on User's top priorities
- No fluff or generic advice
- Synthesize data, don't just list it
