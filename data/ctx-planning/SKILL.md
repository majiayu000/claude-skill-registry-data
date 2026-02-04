---
name: ctx-planning
description: Generate daily and weekly planning reports from backlog and carryover state, applying WIP limits and priority rules from BaseContext.yaml, with automatic git commit/push.
---

# ctx-planning

## Purpose

Generate structured daily and weekly planning reports based on prioritized backlog and carryover tasks. This skill applies work-in-progress (WIP) limits, priority ordering, and tie-breaker rules from `BaseContext.yaml` to create focused, actionable plans stored as Markdown reports.

## When to Use This Skill

Use this skill when:
- User requests daily plan generation (e.g., `/ctx.daily`)
- Closing out the day and updating progress (e.g., `/ctx.eod`)
- Generating weekly review summaries (e.g., `/ctx.weekly`)
- Monthly retrospective planning (e.g., `/ctx.monthly`)
- Updating planning configuration (e.g., `/ctx.update`)

Do not use this skill when:
- User wants to modify individual tasks (use task files directly)
- Backlog hasn't been scanned yet (run `/ctx.scan` first)
- User is querying task status without planning

## How It Works

### Daily Planning Workflow (`/ctx.daily`)

Generate a focused daily plan following these steps:

1. **Load configuration** from `BaseContext.yaml`:
   - `wip_limits.daily_tasks_max`: Maximum tasks per day (default: 5)
   - `wip_limits.weekly_projects_max`: Maximum projects per week (default: 3)
   - `prioritization.order`: Priority sequence (default: P1 → P2 → P3)
   - `prioritization.tie_breakers`: Tie-breaking rules (e.g., `unblocker_first`, `short_first`)
   - `goals.month`: Current monthly objectives for alignment

2. **Load state files**:
   - `state/backlog.yaml`: All tasks from projects
   - `state/carryover.yaml`: Tasks carried over from previous day (if exists)

3. **Select tasks** respecting constraints:
   - Carryover tasks take precedence
   - Fill remaining slots from backlog by priority
   - Limit to `daily_tasks_max` total tasks
   - Cover at most `weekly_projects_max` distinct projects
   - Apply tie-breakers when multiple tasks have same priority:
     - `unblocker_first`: Prioritize tasks that unblock others
     - `short_first`: Favor smaller, quick-win tasks

4. **Generate report** at `reports/daily/YYYY-MM-DD.md` using `templates/daily.md`:
   ```markdown
   # Daily — 2025-10-22 (Tuesday)

   ## Carryover from Yesterday
   - [ ] Task from yesterday (project/repo • T101)

   ## Today's Focus (≤5 tasks)
   - [ ] High priority task (project/repo • T250 • P1)
   - [ ] Second task (project/repo • T251 • P1)

   ## Blockers/Risks
   - ...

   ## EoD — Summary
   **Completed:**
   - ...

   **Decisions/Insights:**
   - ...

   **Carry to Tomorrow:**
   - ...
   ```

5. **Commit and push** changes using `scripts/commit_and_push.sh`:
   ```bash
   bash scripts/commit_and_push.sh "chore(context): daily plan YYYY-MM-DD"
   ```

### End-of-Day Workflow (`/ctx.eod`)

Close out the day and prepare for tomorrow:

1. **Open current daily report** at `reports/daily/YYYY-MM-DD.md`

2. **Update EoD section** with:
   - **Completed**: Check off done tasks
   - **Decisions/Insights**: Document key learnings or decisions
   - **Carry to Tomorrow**: List incomplete tasks for carryover

3. **Generate carryover file** at `state/carryover.yaml`:
   ```yaml
   date: "YYYY-MM-DD"
   items:
     - uid: "org/repo#T101"
       title: "Incomplete task"
       project: "org/repo"
       priority: "P1"
       reason: "blocked_by_external" # or "needs_more_time", "deprioritized"
   ```

4. **Commit and push** updated daily report and carryover state

### Weekly Review Workflow (`/ctx.weekly`)

Generate weekly summary and align with monthly goals:

1. **Collect daily reports** from last 7 days (`reports/daily/`)

2. **Extract achievements** per project:
   - Count completed tasks by project
   - Identify completed milestones or features
   - Calculate completion rate vs. planned

3. **Align with monthly goals** from `BaseContext.yaml`:
   - For each goal, assess progress based on completed tasks
   - Identify tasks contributing to each goal
   - Flag goals at risk or ahead of schedule

4. **Generate weekly report** at `reports/weekly/YYYY-WW.md` using `templates/weekly.md`:
   ```markdown
   # Weekly — 2025-W43 (Oct 22–28)

   ## Achievements by Project
   - org/repo-1: 8 tasks completed, feature X shipped
   - org/repo-2: 3 tasks completed, blocked on external dependency

   ## Monthly Goals Progress
   - Goal 1: 60% complete (on track)
   - Goal 2: 30% complete (at risk, needs acceleration)

   ## Top 5 Priorities Next Week
   1. Unblock dependency for repo-2
   2. Complete feature Y for repo-1

   ## Risks and Mitigation
   - Risk: External dependency delayed
     Action: Implement workaround by Tuesday
   ```

5. **Commit and push** weekly report

### Monthly Review Workflow (`/ctx.monthly`)

Generate monthly retrospective (draft format):

1. **Aggregate weekly reports** for the month
2. **Assess monthly goals** completion status
3. **Identify patterns**: productivity trends, common blockers, wins
4. **Draft next month's goals** based on learnings
5. Create `reports/monthly/YYYY-MM.md` (manual editing expected)

### Configuration Update Workflow (`/ctx.update`)

Modify planning parameters without regenerating plans:

1. **Edit `BaseContext.yaml`** for requested changes:
   - Adjust WIP limits
   - Update monthly goals
   - Modify priority rules or tie-breakers

2. **Validate changes**: Ensure YAML syntax is correct

3. **Optionally regenerate** current plans if user requests immediate effect

## Task Selection Logic

### Priority Ordering

Tasks are selected in this order:
1. **P1** (High priority): Critical tasks, blockers, urgent items
2. **P2** (Medium priority): Normal development tasks
3. **P3** (Low priority): Nice-to-have, refactoring, tech debt

### Tie-Breaking Rules

When multiple tasks have the same priority, apply tie-breakers in order:

- `unblocker_first`: Tasks that unblock other work (look for keywords like "unblock", "prerequisite")
- `short_first`: Smaller tasks that can be completed quickly (estimate based on title/scope)
- `least_recent_project`: Rotate focus across projects to maintain progress
- `oldest_first`: Tasks created/opened earliest (when timestamp available)

### WIP Limits

Enforce limits to maintain focus:
- `daily_tasks_max` (default: 5): Prevents overcommitment
- `weekly_projects_max` (default: 3): Maintains project focus, reduces context switching

## Template Variables

Templates support Handlebars-style placeholders:

### Daily Template Variables
- `{{date}}`: Date in YYYY-MM-DD format
- `{{weekday}}`: Day of week
- `{{daily_tasks_max}}`: Max tasks from config
- `{{carryover}}`: Array of carryover task objects
- `{{focus_tasks}}`: Array of selected task objects

### Weekly Template Variables
- `{{iso_week}}`: ISO week number (YYYY-WW)
- `{{date_start}}`, `{{date_end}}`: Week start/end dates
- `{{achieved}}`: Map of project → achievement summary
- `{{month_goals}}`: Array of {goal, progress} objects
- `{{priorities}}`: Array of next week's priority items

## Constraints

- **Local files only**: No network access except git push
- **Single repository**: Only modifies files within `context/` repo
- **Idempotent operations**: Running multiple times produces consistent results
- **Template-driven**: Output format controlled by `templates/*.md`

## Related Skills

- `ctx-collector`: Generates `state/backlog.yaml` consumed by this skill
- Use `BaseContext.yaml` to configure behavior without modifying skill

## Troubleshooting

If planning produces unexpected results:
- Verify `state/backlog.yaml` exists and is current (run `/ctx.scan`)
- Check `BaseContext.yaml` for correct WIP limits and priority order
- Ensure `templates/*.md` files are valid and have required placeholders
- Verify git repository is configured for push access
- Check `state/carryover.yaml` format matches expected structure
