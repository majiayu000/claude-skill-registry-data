---
name: weekly-plan
description: Plan weekly P-Tasks with in-repo task triage and overplanning challenge
---

# Plan Weekly P-Tasks

You help plan the upcoming week's P-Tasks (3-5 meaty priorities) with an overplanning challenge and triage of the in-repo task list.

## Input

The user invokes this skill (typically Sunday evening or Monday morning) without arguments, or with context like "plan my week".

The user may:
- Let you suggest P-tasks based on context
- Propose their own P-task list for validation
- Provide calendar context (screenshot or text)

## Workflow

### 1. Review previous week

Read `Dashboard/Weekly P-Tasks.md`. Find the most recent week's P-tasks.

If last week's P-tasks don't have completion markers, prompt the user:

```
Let's review last week before planning this week:

P1: [Task]
- Status? (Completed / Partial / Not done)
- If completed: results?
- If partial or not done: what blocked it?

P2: [Task]
...
```

Wait for review, then update last week's entry with markers:
- `✅` completed (add a note about results)
- `🔄` partial / carry over (add a note about what's left)
- `❌` not started / deprioritized (add a note about why)

Compute last week's completion rate (completed / total) - used for the overplanning check.

### 2. Analyze recent daily notes

Read the last 7 days from `journals/YYYY/MM-Month/`.

Identify:
- Carryover items mentioned but not finished.
- **Energy/mood patterns** from frontmatter and content:
  - Declining trend (e.g., 7 → 5).
  - Mentions of overwork, burnout, feeling overwhelmed.
- Recurring themes or blockers.
- Weekly review notes (Friday entries).

Capacity adjustment:
- Energy < 6 or declining trend → suggest 3-4 P-tasks max.
- "Feeling overwhelmed" appears → reduce scope aggressively.

### 3. Calendar context

If the user hasn't shared their calendar, ask:
"Share your calendar for this week or highlight key deadlines."

Look for hard deadlines (presentations, demos, deliverables), meeting density, and time-sensitive milestones.

If calendar shows >50% meeting time: reduce P-task count and note reduced capacity.

### 4. Review recent meetings for follow-ups

Read the last 5 meeting notes from `Meetings/`. Extract action items assigned to the user that are still open and not yet in `Dashboard/tasks.md`. Flag them.

### 5. Read `Dashboard/tasks.md` - triage inputs

Read `Dashboard/tasks.md`. You now have three buckets:

- **This week** - items already committed to this week.
- **Next** - items intended soon but not this week.
- **Backlog** - unscheduled.

Flag items in "This week" that are stale carryovers (from prior weeks and still open). Flag items in "Backlog" older than 4 weeks that look stale.

### 5b. Triage - execute immediately

Goal: **Dashboard/tasks.md "This week" contains only what you truly commit to this week.**

Present a triage table:

```
This week leftovers (N tasks)
-> "Task A"       Keep - still relevant this week
-> "Old task X"   Move to Next / Backlog - deprioritized

Backlog promotions (top 5 relevant to this week's themes)
-> "Follow up with X"   Promote to This week - blocks work
-> "Scope workshop Y"   Stay in Backlog - not this week

Stale backlog (4+ weeks old, no notes)
-> "Old task"     Delete? - no recent activity
```

For each item, suggest an action. Wait for the user to confirm or override, then **execute the moves immediately** by editing `Dashboard/tasks.md`. Do not wait until the end.

After triage: confirm "Triage complete - X tasks kept, Y moved, Z deleted."

### 6. Suggest or validate P-Tasks + standalone tasks

Two outputs from this step: **P-Tasks** (with subtasks) and **standalone tasks** (no subtasks, specific day).

#### P-Tasks (3-5, each needs subtasks)

**If the user proposed tasks**: validate against context (completion rate, calendar, energy). Proceed to step 7.

**If the user wants suggestions**: draft 3-5 P-tasks based on:
- Carryover from last week
- Meeting follow-ups not yet in tasks.md
- Triage promotions
- Calendar deadlines

Prioritize P1-P5:
- **P1** critical, must be done this week (1-2 max)
- **P2** high priority, significant impact (1-2)
- **P3** medium priority, should be done (1-2)
- **P4** low priority, nice to have (0-1)
- **P5** optional, time permitting (0-1)

#### Standalone tasks (3-6, self-contained)

Suggest from:
- Triage promotions flagged "this week"
- Meeting follow-ups too small for a P-task
- Backlog candidates matched to this week's themes

Assign each standalone task a specific day based on calendar density and P-task load.

### 7. Validate task quality

Check each P-task against [quality-checklist.md](quality-checklist.md).

Good P-task qualities:
- Clear, measurable result (not vague)
- Specific action verb ("Draft", "Create", "Share")
- Noteworthy (not routine)
- Requires active effort
- Independently achievable

Red flags:
- Vague verbs: "work on", "think about", "look into"
- Too small: "send email", "schedule meeting"
- Grouped: "create X and Y" (split them)
- No clear completion: "improve X"

Suggest improvements and ask focused clarifying questions for unclear tasks.

### 8. Overplanning challenge

Flag if:
- P-tasks > 5 (target: 3-5)
- Standalone tasks > 8 (target: 3-6)
- Last week's completion rate < 60%
- Energy declining or < 6/10
- Calendar >50% meetings

If any flag triggers, present:

```
OVERPLANNING ALERT

Evidence:
- Last week completion: [X]%
- Current suggestion: [N] P-tasks
- Energy this week: [Y]/10 [declining/stable/improving]
- Calendar: [%] meeting time

Which 3-5 tasks are truly CRITICAL this week? What can move to Next or Backlog?
```

Wait for the user to trim before finalizing.

### 9. Break P-Tasks into subtasks

For each P-task, identify 2-5 concrete, actionable subtasks with action verbs. Assign due days spread across the week.

Mark stretch goals explicitly with "(stretch)" and lower priority.

### 10. Present for approval

**MANDATORY - do not proceed without explicit user approval.**

Present:
1. **P-Tasks + subtasks** - full breakdown with due days
2. **Standalone tasks** - with assigned days
3. **Weekly P-Tasks.md preview** - P-Tasks only, what goes into the Obsidian file
4. **Tasks.md preview** - subtasks + standalone tasks, what appends to "This week"
5. **Shareable summary** - P-Tasks only, no internal context, for sharing with your team

Ask: "Does this look good? I'll update Weekly P-Tasks.md and Dashboard/tasks.md once you confirm."

### 11. Write files

After approval:

**Dashboard/Weekly P-Tasks.md** - insert new week at the top:

```markdown
# Week of DD Month YYYY

P1: [Task] - [[related note or project]]
P2: [Task]
P3: [Task]
P4: [Task]

**Notes:**
- [Key deadlines]
- [Capacity note if reduced]
```

**Dashboard/tasks.md** - append subtasks and standalone tasks to the "This week" section:

```
- [ ] Subtask - source: [[Week of DD Month YYYY]] (P1 parent) - due: YYYY-MM-DD - priority: P2
- [ ] Standalone task - source: [[meeting or decision note]] - due: YYYY-MM-DD - priority: P3
```

### 12. Summary

```
Weekly planning complete!

- [N] P-Tasks with [M] subtasks + [K] standalone tasks
- Last week completion: [X]%
- Energy this week: [Y]/10
- Key deadlines: [list]
- Capacity note: [if reduced, state why]

Outputs:
1. Dashboard/Weekly P-Tasks.md - P-Tasks for this week
2. Dashboard/tasks.md - subtasks and standalone tasks in "This week"
3. Shareable summary (P-Tasks only, above) - ready to paste into your team's channel
```

## Error recovery

### Weekly P-Tasks.md unexpected format
- Do not overwrite existing content.
- Add the new week at the top.
- Preserve all previous weeks.

### No daily journals exist
- Skip energy/mood analysis.
- Ask the user directly about capacity.

### Dashboard/tasks.md missing
- Create it with three sections (This week / Next / Backlog) and proceed.

## Notes

- Spread task due dates across the week - don't dump everything on Monday.
- Calendar context is critical - deadlines change everything.
- This skill has no external dependencies - all writes are to in-repo files.
