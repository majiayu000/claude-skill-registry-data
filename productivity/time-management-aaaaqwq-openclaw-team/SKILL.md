---
name: Time Management
slug: time-management
version: 1.0.0
homepage: https://clawic.com/skills/time-management
description: Plan days, prioritize tasks, and protect focus time with time blocking, weekly reviews, and energy-aware scheduling.
metadata: {"clawdbot":{"emoji":"⏰","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Setup

On first use, read `setup.md` silently and start the conversation naturally. Never mention "setup" or file names to the user.

## When to Use

User needs help planning their day, prioritizing tasks, or protecting time for important work. Agent handles time blocking, weekly reviews, and schedule optimization.

## Architecture

Memory lives in `~/time-management/`. See `memory-template.md` for structure.

```
~/time-management/
├── memory.md          # Preferences + current commitments
├── weekly-review.md   # Last review notes
└── templates/         # User's custom templates
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| Time blocking method | `time-blocking.md` |
| Prioritization frameworks | `prioritization.md` |
| Weekly review process | `weekly-review.md` |
| Common time traps | `traps.md` |

## Core Rules

### 1. Default to Time Blocking
When user asks "how should I organize my day?":
1. Identify their 1-3 most important tasks (MITs)
2. Assign specific time blocks (not just "morning")
3. Add buffer time between blocks (15-30 min)
4. Protect the first deep work block

Example response:
```
Your day:
09:00-11:00 — [MIT #1] (deep work, no meetings)
11:00-11:30 — Buffer/email
11:30-12:30 — [MIT #2]
12:30-13:30 — Lunch
13:30-15:00 — Meetings/calls
15:00-16:30 — [MIT #3 or admin tasks]
16:30-17:00 — Plan tomorrow
```

### 2. Energy-Aware Scheduling
Match task type to energy levels:

| Time | Energy | Best for |
|------|--------|----------|
| Morning (first 2-4h) | Peak | Creative work, hard problems, writing |
| Mid-day | Moderate | Meetings, collaboration, admin |
| Afternoon | Lower | Routine tasks, email, planning |

If user's peak time differs → ask and adapt.

### 3. Protect Deep Work
When scheduling:
- First block of day = deep work (no exceptions)
- Minimum 90 minutes for meaningful progress
- No meetings before 11am (suggest as default)
- If user has back-to-back meetings → flag the problem

### 4. Weekly Review Habit
Suggest weekly review on Sunday evening or Monday morning:
1. What worked last week?
2. What didn't?
3. Top 3 priorities for this week
4. Any time blocks to protect?

Store notes in `~/time-management/weekly-review.md`.

### 5. Say No by Default
When user considers adding commitments:
- Ask: "What will you NOT do to make time for this?"
- If answer is unclear → suggest declining
- Protect existing commitments over new ones

### 6. Batch Similar Tasks
Group similar activities:
- All calls in one block
- All email in 2-3 daily slots (not constant checking)
- All admin tasks together
- Context switching = time lost

### 7. Plan Tomorrow Tonight
End-of-day ritual:
1. Review what got done
2. Move incomplete tasks
3. Set top 3 for tomorrow
4. Write first block explicitly

## Time Traps

| Trap | Why it fails | Alternative |
|------|--------------|-------------|
| "I'll do it when I have time" | That time never comes | Schedule it or decline |
| 30-minute meeting blocks | No deep work possible | 90-min minimum for real work |
| Checking email first | Reactive mode hijacks your day | Deep work first, email at 11am |
| No buffer time | Delays cascade | 15-min buffers between blocks |
| Planning in your head | Forgotten and overwhelming | Write it down, one place |
| "I work better under pressure" | Usually stress, not quality | Start earlier, same deadline |

## Scope

This skill ONLY:
- Provides time management advice when asked
- Helps plan days and weeks
- Stores preferences user explicitly provides
- Reads included reference files

This skill NEVER:
- Accesses calendar, email, or any external service
- Tracks or monitors user activity
- Makes network requests
- Modifies files without explicit user request

## External Endpoints

This skill makes NO external network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

## Security & Privacy

**Data that stays local:**
- Preferences you explicitly ask to save
- Stored in `~/time-management/`
- You can delete anytime

**This skill does NOT:**
- Access any external service
- Track your behavior
- Infer preferences without asking

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `productivity` — energy management and focus systems
- `schedule` — recurring tasks and reminders
- `habits` — building consistent routines

## Feedback

- If useful: `clawhub star time-management`
- Stay updated: `clawhub sync`
