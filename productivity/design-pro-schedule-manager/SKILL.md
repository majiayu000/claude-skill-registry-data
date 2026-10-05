---
type: Skill
name: design-pro-schedule-manager
description: Manage NV oOS Pro Schedules — create, update, delete, list, dry-run, view run history, and plan schedules from workflows. Covers all 7 Pro Schedule Manager MCP tools with usage patterns, cross-references, and operational troubleshooting. Use when creating recurring tasks, debugging schedule failures, pausing vs deleting schedules, converting Action Scheduler jobs to managed schedules, or bridging workflow outputs to timed execution.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# NV oOS Pro Schedule Manager

The Pro Schedule Manager provides a management UI and MCP tool layer for scheduled
tasks in the NV oOS ecosystem. It sits *above* WordPress's native cron and Action
Scheduler — it does not replace them, but provides CRUD, history, dry-run testing,
and workflow-to-schedule planning on top.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for pipeline automation. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai cron` | Inspect scheduled tasks, debug late/duplicate cron events |
| `wp mcp-ai queue` | View background job queues, retry failed tasks |
| `wp mcp-ai bulk` | Bulk operations — useful for batch schedule management |
| `wp mcp-ai health` | Verify system health before enabling new schedules |
| `wp mcp-ai log` | View execution logs for debugging schedule failures |

## When to use this skill

Trigger when ANY of the following is true:

- Creating, updating, or deleting a scheduled task via the Pro Schedule Manager.
- Listing active schedules to audit what's running.
- Checking the run history of a specific schedule (success/failure logs).
- Dry-running a schedule to validate its configuration before activation.
- Planning schedules from a workflow — converting workflow outputs into timed tasks.
- Debugging "my schedule didn't fire" or "fired but produced wrong results" issues
  at the management layer.
- Deciding whether a task should be a Pro Schedule vs a raw Action Scheduler job.

## Mental model — Pro Schedules are managed wrappers

Pro Schedules are managed entities that wrap lower-level scheduling primitives
(WP-Cron events or Action Scheduler actions). Think of them as:

```
Pro Schedule (management record)
  └── schedule config (hook, recurrence, args, timing)
  └── run history (timestamp, status, output/logs)
  └── workflow association (optional link to source workflow)
```

The underlying execution still happens through WP-Cron or Action Scheduler.
The Pro Schedule layer adds:

- **CRUD management** — create/update/delete without writing PHP code.
- **Run history** — track every execution, status, and output.
- **Dry-run** — test without side effects.
- **Workflow integration** — plan schedules from workflow outputs.

## Available Tools (7)

### 1. `create_pro_schedule`

Create a new managed schedule.

```json
{
  "name": "create_pro_schedule",
  "arguments": {
    "title": "Daily Product Sync",
    "hook": "myplugin/daily_product_sync",
    "recurrence": "daily",
    "args": { "batch_size": 50 },
    "first_run": "2026-08-12T04:00:00Z",
    "enabled": true
  }
}
```

Key parameters:
- `title` — human-readable name displayed in the admin UI.
- `hook` — the WordPress action hook that fires. Must match a registered callback.
- `recurrence` — interval: `hourly`, `twicedaily`, `daily`, `weekly`, or a custom cron schedule slug.
- `args` — optional arguments passed to the hook callback (JSON-serializable).
- `first_run` — ISO 8601 timestamp for the first execution.
- `enabled` — whether the schedule is active immediately.

### 2. `update_pro_schedule`

Modify an existing schedule. All fields are optional — only provided fields change.

```json
{
  "name": "update_pro_schedule",
  "arguments": {
    "schedule_id": 42,
    "title": "Product Sync (increased batch)",
    "args": { "batch_size": 100 },
    "enabled": true
  }
}
```

Use this to:
- Toggle a schedule on/off without deleting it (preserves history).
- Adjust arguments (e.g., batch size, timeout).
- Rename for clarity.
- Change recurrence timing.
- **Edit workflow steps in place** — `workflow_steps` replaces the whole ordered
  tool chain on `workflow`-type schedules, so a step's arguments can be
  corrected without recreating the schedule (rejected with
  `invalid_schedule_type` on non-workflow schedules, `invalid_workflow_steps`
  when no valid step survives sanitisation):

```json
{
  "name": "update_pro_schedule",
  "arguments": {
    "schedule_id": "abc123…",
    "workflow_steps": [
      {
        "tool_slug": "search_upwork_jobs",
        "arguments": { "query": "wordpress developer", "sort": "recency", "limit": 20 },
        "label": "Search for new matching jobs"
      }
    ]
  }
}
```

### 3. `delete_pro_schedule`

Permanently remove a schedule and its run history.

```json
{
  "name": "delete_pro_schedule",
  "arguments": {
    "schedule_id": 42
  }
}
```

**⚠️ Warning:** This deletes the management record AND all run history. If you
only want to pause execution, use `update_pro_schedule` with `enabled: false` instead.

Before deleting, consider:
- Export run history if needed for auditing.
- Verify no workflows depend on this schedule.
- Check that the underlying cron/Action Scheduler event is also cleaned up.

### 4. `list_pro_schedules`

List all managed schedules with optional filtering.

```json
{
  "name": "list_pro_schedules",
  "arguments": {
    "status": "active",
    "search": "sync",
    "per_page": 20,
    "page": 1
  }
}
```

Filter options:
- `status` — `active`, `inactive`, or `all`.
- `search` — free-text search across title and hook.
- `per_page` / `page` — pagination.

Use this to:
- Audit all active schedules across the site.
- Find schedules by hook name or keyword.
- Check what's enabled vs disabled.

### 5. `get_schedule_run_history`

Retrieve the execution history for a specific schedule.

```json
{
  "name": "get_schedule_run_history",
  "arguments": {
    "schedule_id": 42,
    "per_page": 25,
    "page": 1
  }
}
```

Returns for each run:
- Timestamp (scheduled and actual execution time).
- Status: `success`, `failed`, `running`, `timeout`.
- Output/logs from the callback.
- Duration (execution time in seconds).

Use this to:
- Debug failures — find the exact error from the callback output.
- Identify performance issues — runs that take unusually long.
- Audit execution patterns — is a "daily" schedule actually firing daily?
- Detect silent failures — callbacks that return without error but produce wrong results.

### 6. `dry_run_pro_schedule`

Execute the schedule's callback once, immediately, **without persisting side effects**
(where supported) or recording it as an official run.

```json
{
  "name": "dry_run_pro_schedule",
  "arguments": {
    "schedule_id": 42
  }
}
```

Use this to:
- Validate a new schedule before enabling it.
- Test argument changes without affecting production data.
- Reproduce a failure from the run history in a controlled way.
- Verify that recent code changes don't break an existing schedule.

**Note:** Dry-run behavior depends on the callback implementation. Callbacks that
use `wp_get_environment_type()` or similar checks can gate side effects during
dry-runs. The Pro Schedule Manager sets an environment flag that callbacks can
inspect.

### 7. `plan_schedules_from_workflow`

Convert a workflow's output into one or more scheduled tasks. This is the bridge
between the workflow engine and the schedule manager.

```json
{
  "name": "plan_schedules_from_workflow",
  "arguments": {
    "workflow_id": 7,
    "schedule_pattern": "daily",
    "first_run_offset_hours": 2
  }
}
```

Key parameters:
- `workflow_id` — the source workflow to derive schedules from.
- `schedule_pattern` — recurrence pattern for generated schedules.
- `first_run_offset_hours` — delay before the first run.

Use this when:
- A content workflow produces tasks that need to run on a schedule.
- You want to automate schedule creation from workflow templates.
- A multi-step workflow needs staggered execution timing.

The tool analyzes the workflow structure and produces one or more schedule
records, each mapped to a workflow step that benefits from scheduled execution.

## Common workflows

### Creating a new scheduled task

```
1. Define the callback hook (register via add_action in your plugin).
2. Use create_pro_schedule to wrap it in a managed schedule.
3. Use dry_run_pro_schedule to validate.
4. Check get_schedule_run_history after the first real run.
```

### Debugging a failed schedule

```
1. Use list_pro_schedules to find the schedule.
2. Use get_schedule_run_history to see the failure details.
3. Use dry_run_pro_schedule to reproduce the issue.
4. Fix the callback or configuration.
5. Use update_pro_schedule if you need to adjust args/timing.
6. Check run history again after the next execution.
```

### Pausing vs deleting

```
PAUSE:    update_pro_schedule(schedule_id, enabled: false)
RESUME:   update_pro_schedule(schedule_id, enabled: true)
DELETE:   delete_pro_schedule(schedule_id)
          — also clean up the underlying cron/Action Scheduler event
```

Always prefer pausing over deleting when:
- You may need the schedule again.
- You want to preserve run history.
- Other workflows or schedules reference this one.

### Converting a raw Action Scheduler job to a managed schedule

```
1. Identify the existing Action Scheduler hook.
2. Use create_pro_schedule with the same hook and args.
3. This adds management UI, run history, and dry-run support.
4. The underlying Action Scheduler event continues to run as before.
```

## Integration with wp-plugin-cron and wp-action-scheduler

The Pro Schedule Manager does NOT replace these. It delegates to them:

| Layer | What it does |
|---|---|
| **Pro Schedule Manager** (this skill) | Manage, audit, dry-run, plan schedules. |
| **Action Scheduler** (`wp-action-scheduler`) | Queue semantics, status tracking, retries, admin UI. Backend for most Pro Schedules. |
| **WP-Cron** (`wp-plugin-cron`) | Simple periodic events without queue overhead. Used for lightweight Pro Schedules. |

When creating a Pro Schedule, the manager selects the appropriate backend based
on the schedule's characteristics (recurrence, expected load, need for retries).

**Cross-reference flow:**

- If the question is about **scheduling mechanics** (recurrence, cron intervals,
  multisite, idempotency): → `wp-plugin-cron`
- If the question is about **queue behavior** (status tracking, retries, batch
  size, WP-CLI debugging): → `wp-action-scheduler`
- If the question is about **managing schedules** (CRUD, history, dry-run,
  workflow planning): → **this skill**

## Critical rules

- **Prefer pausing (`enabled: false`) over deleting** — preserves history and allows resumption.
- **Always dry-run new or modified schedules** before enabling to catch config errors.
- **Check run history after the first real execution** — don't assume it worked.
- **Keep args JSON-serializable and small** — same constraint as Action Scheduler.
- **The hook must be registered before the schedule fires** — otherwise the event is silently ignored.
- **Deleting a Pro Schedule may not clean up the underlying cron/Action Scheduler event** — verify and clean up manually if needed.
- **Workflow-planned schedules are derived, not linked** — updating the source workflow does not auto-update derived schedules.

## Common mistakes

```json
// WRONG — deleting a schedule without checking if others depend on it
{ "name": "delete_pro_schedule", "arguments": { "schedule_id": 7 } }

// RIGHT — pause first, audit dependencies, then delete
{ "name": "update_pro_schedule", "arguments": { "schedule_id": 7, "enabled": false } }
// ... audit ...
{ "name": "delete_pro_schedule", "arguments": { "schedule_id": 7 } }

// WRONG — enabling a schedule without dry-running after argument changes
{ "name": "update_pro_schedule", "arguments": { "schedule_id": 42, "args": { "mode": "aggressive" }, "enabled": true } }

// RIGHT — dry-run first
{ "name": "dry_run_pro_schedule", "arguments": { "schedule_id": 42 } }
// verify output...
{ "name": "update_pro_schedule", "arguments": { "schedule_id": 42, "enabled": true } }

// WRONG — assuming the schedule fired at the exact configured time
// Check get_schedule_run_history for the actual execution timestamp.

// WRONG — creating a schedule with a hook that isn't registered yet
// The event will fire but the callback won't run.
// Register the callback first, then create the schedule.
```

## Cross-references

- Run `wp-plugin-cron` for scheduling mechanics: cron intervals, multisite, idempotent callbacks, `wp_next_scheduled` guards.
- Run `wp-action-scheduler` for queue semantics: status tracking, retries, batch processing, WP-CLI commands.
- Run `wp-plugin-lifecycle` for activation/deactivation scheduling patterns.
- Run `wp-security-audit` on schedule callbacks — they run with no current user, so capability checks don't work.
- Run `design-pro-workflow-builder` to design workflows that produce scheduled tasks via `plan_schedules_from_workflow`.
- Run `design-crm` to schedule recurring CRM tasks — pipeline reviews, lead scoring, follow-up reminders.
- Run `design-campaign-orchestration` to schedule recurring campaign content publication and monthly reports.

## What this skill does NOT cover

- Writing the actual hook callbacks — that's your plugin code.
- WP-Cron or Action Scheduler internals — covered by `wp-plugin-cron` and `wp-action-scheduler`.
- Workflow engine design — this skill only covers the `plan_schedules_from_workflow` bridge.
- Server-level cron daemon configuration.

## References

- NV oOS Pro Schedule Manager admin page: `/wp-admin/admin.php?page=nvoos-pro-schedule-manager`
- WordPress Cron Handbook: [developer.wordpress.org/plugins/cron/](https://developer.wordpress.org/plugins/cron/)
- Action Scheduler: [actionscheduler.org](https://actionscheduler.org)
