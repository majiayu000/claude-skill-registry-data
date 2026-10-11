---
name: work-feedback
description: Periodic status-table check-ins while background sub-agents work, gated by credentials.json.
---

# Work Feedback

When an orchestrating agent spawns sub-agents that run **in the background** (e.g. `Agent` with `run_in_background: true`, or a `Workflow` run), the user loses visibility into progress until the final summary. This skill defines a periodic, table-only check-in that closes that gap.

---

## Configuration Gate

Before doing anything in this skill, read the two keys below from the first of these files that carries them, in order. Use the **Read** tool, not a shell command — the first file holds secrets next to these keys, and the credential guard hook stops a shell read of it:

1. `.dev-team-agents/credentials.local.json` of the main checkout — resolve the path exactly as `skills/shared/credentials/SKILL.md` § File Location does (linked worktrees share it).
2. `<credentials>/<project_id>.json`, then `<credentials>/global.json` — the credential reference files, where `devteam cred import` moves these two keys (and quarantines file 1). `<credentials>` is the `credentials` path in `devteam path --json`; `project_id` is in `.dev-team-agents/project.json`. These files hold no secret values.

Only these keys are read:

```json
{
  "work_feedback_active": true,
  "work_feedback_interval_minutes": 5
}
```

- `work_feedback_active: false` → **do not** run any part of this skill. No table, no scheduling. Proceed with the task silently as if this skill did not exist.
- `work_feedback_interval_minutes` → the polling interval in minutes. Convert to seconds and clamp to `[60, 3600]` (the `ScheduleWakeup` runtime limit) before use. A value outside that range after conversion is clamped, never rejected.
- If no file above carries a key, treat it as `active: true`, `interval_minutes: 5`. Nothing creates the file implicitly, so absence is the default, not an opt-out.

These two keys are the **only** source of truth for whether and how often this skill runs. Do not infer a different cadence from context, and do not skip the gate check because "it's probably fine."

---

## When To Apply

Applies only when sub-agents are running **in the background** and the task has a known, ordered set of steps (from an approved plan, a `/devteam:*` command's roster, or an explicit step list stated to the user). Does not apply to:
- Foreground/synchronous agent calls (the user already sees them run one at a time)
- Single-agent tasks with no parallel work to report on
- Tasks with no step list to render (nothing to put in the table)

---

## Loop Mechanics

1. Before the first background spawn, resolve the step list (ordered, from the plan/roster), note the version string (`installed_version` from `state.json` in the same state directory), and record the start timestamp — it is fixed for the whole run and never recomputed on later ticks.
2. After spawning, call `ScheduleWakeup` with `delaySeconds` = the clamped interval from the gate above, and a `reason` naming what is being polled.
3. On each wake-up, check the real status of in-flight sub-agents (`TaskList`/`TaskOutput`, or the workflow's own progress state) and update each step's status:
   - ✅ done
   - ⏳ in progress right now
   - 🕐 waiting (not started)
4. Emit **only** the table (see Format below) — no narration, no preamble, no trailing text in that turn.
5. If any step is still not ✅, call `ScheduleWakeup` again with the same interval. If all steps are ✅, emit the final all-✅ table and stop scheduling (`stop: true`) — do not keep polling a finished task.

6. **Cap it.** On each tick, apply `skills/architecture/orchestration/SKILL.md` § Spawn Integrity check 5 to any sub-agent that looks stalled (resume it with `SendMessage`, never re-spawn). After its two reactivation attempts for a sub-agent, emit the current table, stop scheduling, and surface that sub-agent to the user as a blocker — do not keep polling.

While the gate above is active, this loop is the **only** `ScheduleWakeup` loop for the round — the orchestration skill's check 5 does not schedule its own wakeup alongside it.

Never fire more than one wake-up cycle per interval, and never shorten the interval to "check sooner" — the interval is a user-controlled setting, not a suggestion.

**Relationship to `skills/shared/plan-mode/SKILL.md`'s Progress Reporting**: the two report at different granularities and do not replace each other. This skill fires **within** a plan step, on its own interval, only while that step's work is delegated to background subagents — it says nothing about the plan's other steps. Progress Reporting fires **between** steps, once per step, when a step finishes. A single background step can produce several of this skill's tables before it completes and produces exactly one Progress Reporting update. Keep emitting this skill's table on schedule even if a Progress Reporting update was just sent for an adjacent step — they are separate messages for separate audiences of the same work.

---

## Table Format

```
### 📋 DEVTEAM AGENTS v<installed_version> • WORK FEEDBACK
Started at <yyyy-mm-dd hh:mm> (duration: <Xh Ym Zs>)

| # | Step               | Status |
|---|--------------------|--------|
| 1 | <step 1 title>     | ✅     |
| 2 | <step 2 title>     | ⏳     |
| 3 | <step 3 title>     | 🕐     |
```

- Line 1 is a markdown heading (`###`) starting with the 📋 marker, then product name and installed version in upper case, `•`, `WORK FEEDBACK` in upper case — no extra separators or emphasis.
- Line 2: `Started at` followed by the fixed start timestamp recorded in Loop Mechanics step 1, then the elapsed duration since that timestamp in parentheses, formatted `<h>h <m>m <s>s` (omit a leading unit that is zero, e.g. `23m 4s` when under an hour).
- Steps appear in planned order, unchanged across ticks (only the Status column changes).
- No text before or after the table in that message.
