---
name: self-scheduler
description: Schedule your own future runs as a recurring agent. Use when you need to run periodically (daily, weekly, hourly) to accomplish long-term objectives, monitor changes, or perform maintenance tasks. Creates persistent scheduled jobs that survive session restarts.
version: 1.0.0
allowed-tools: Bash, Read, Write
metadata:
  requires: teamday-spaces
  context: Runs within a TeamDay space environment
---

# Self-Scheduler Skill

Enable autonomous agents to schedule their own future executions for long-term objectives.

## Overview

This skill allows you to:
1. **View** your existing scheduled jobs
2. **Create** new scheduled jobs with cron expressions
3. **Update** existing schedules or prompts
4. **Disable/Enable** jobs without deleting them
5. **Terminate** scheduling when objectives are complete

## CRITICAL: System Prompt Replication

**You are running in an interactive session with a system prompt. Scheduled jobs do NOT automatically receive your system prompt.**

When creating a scheduled job, you MUST:
1. Capture your current system prompt (from your session context)
2. Include it in the scheduled job's `system_prompt` section
3. This ensures your scheduled executions maintain the same personality, capabilities, and instructions

## Working Directory Discovery

First, determine your working directory:

```bash
pwd
```

Expected format: `/data/sandbox/{orgId}/spaces/s-{spaceId}/`

Store these values for use in scheduled job configuration.

## Scheduled Jobs Location

All scheduled jobs are stored in:
```
.claude/scheduled/{job-name}.md
```

This directory is monitored by the TeamDay scheduler service.

## View Existing Scheduled Jobs

```bash
# List all scheduled jobs
ls -la .claude/scheduled/ 2>/dev/null || echo "No scheduled jobs directory found"

# View a specific job
cat .claude/scheduled/{job-name}.md
```

## Create a Scheduled Job

Create a markdown file in `.claude/scheduled/` with the following structure:

```markdown
---
# Job Configuration (YAML frontmatter)
name: daily-monitoring
schedule: "0 9 * * *"           # Cron expression (9 AM daily)
enabled: true
timezone: America/Los_Angeles   # Optional, defaults to UTC
max_turns: 25                   # Max agent turns per execution
model: claude-sonnet-4-20250514 # Optional model override

# Context Discovery (filled by you during creation)
space_id: s-{your-space-id}
organization_id: {your-org-id}
created_at: 2025-01-20T10:00:00Z
created_by: self-scheduler
---

# System Prompt

> **IMPORTANT**: Copy your current system prompt here verbatim.
> This ensures scheduled executions maintain your identity and capabilities.

{PASTE YOUR SYSTEM PROMPT HERE}

---

# Session Instructions

These instructions will be provided as the prompt for each scheduled execution.

## Objective

{Describe the long-term objective this scheduled job serves}

## Tasks for This Run

1. {Task 1}
2. {Task 2}
3. {Task 3}

## Success Criteria

- {Criterion 1}
- {Criterion 2}

## Continuation Instructions

After completing tasks:
- If objective achieved: Update this file to set `enabled: false` and use notify-user skill
- If blocked: Document the blocker, consider disabling, and notify user
- If continuing: Update the "Tasks for This Run" section with next steps

## Session State

{Any state or context that should persist between runs}

Last run: {timestamp}
Last status: {success/failed/pending}
Notes: {observations from last run}
```

## Cron Expression Reference

| Expression | Description |
|------------|-------------|
| `0 9 * * *` | Daily at 9:00 AM |
| `0 9 * * 1` | Weekly on Monday at 9:00 AM |
| `0 */6 * * *` | Every 6 hours |
| `0 * * * *` | Every hour |
| `*/15 * * * *` | Every 15 minutes |
| `0 9 * * 1-5` | Weekdays at 9:00 AM |
| `0 0 1 * *` | Monthly on the 1st at midnight |

Format: `minute hour day-of-month month day-of-week`

## Update a Scheduled Job

Simply edit the `.claude/scheduled/{job-name}.md` file:

```bash
# Read current state
cat .claude/scheduled/daily-monitoring.md

# Update using the Edit tool or Write tool
# The scheduler service will pick up changes automatically
```

## Disable a Scheduled Job

Set `enabled: false` in the frontmatter:

```yaml
---
name: daily-monitoring
schedule: "0 9 * * *"
enabled: false  # <-- Job is paused
---
```

## Delete a Scheduled Job

```bash
rm .claude/scheduled/{job-name}.md
```

## Termination Protocol

When your long-term objective is complete OR you encounter an obstacle preventing future work:

1. **Update the scheduled job**:
   ```yaml
   enabled: false
   termination_reason: "Objective completed" # or "Blocked by {reason}"
   terminated_at: {current timestamp}
   ```

2. **Notify the user** (requires notify-user skill):
   ```
   Use the notify-user skill to send an email informing the user that:
   - The scheduled job has been terminated
   - Reason for termination
   - Summary of work completed
   - Any follow-up actions needed
   ```

3. **Document final state**:
   Update the Session State section with final observations.

## Example: Create a Daily Monitoring Job

```bash
# 1. Discover your context
pwd
# Output: /data/sandbox/org-abc123/spaces/s-space456/

# 2. Create the scheduled directory
mkdir -p .claude/scheduled

# 3. Write the scheduled job file
```

Then write to `.claude/scheduled/daily-docs-monitor.md`:

```markdown
---
name: daily-docs-monitor
schedule: "0 9 * * *"
enabled: true
timezone: America/Los_Angeles
max_turns: 25
space_id: s-space456
organization_id: org-abc123
created_at: 2025-01-20T10:00:00Z
created_by: self-scheduler
---

# System Prompt

You are a documentation monitoring agent for TeamDay. Your role is to:
- Monitor official documentation for changes
- Summarize updates in daily-notes/
- Alert the team to breaking changes

{Continue with your full system prompt...}

---

# Session Instructions

## Objective

Monitor Anthropic documentation for API changes and updates.

## Tasks for This Run

1. Fetch https://docs.anthropic.com/changelog
2. Compare with previous run's snapshot (stored in .cache/docs-snapshot.json)
3. If changes detected, create summary in daily-notes/{date}.md
4. Update snapshot for next run

## Success Criteria

- Documentation checked
- Changes summarized (if any)
- Snapshot updated

## Continuation Instructions

- Continue daily until manually disabled
- If API access blocked: disable and notify user
- Major breaking changes: notify user immediately

## Session State

Last run: pending
Last status: pending
Notes: Initial setup
```

## Best Practices

1. **Always include your system prompt** - Scheduled jobs don't inherit context
2. **Set reasonable max_turns** - Prevent runaway executions
3. **Use clear termination criteria** - Know when to stop
4. **Update session state** - Track progress between runs
5. **Notify on completion/failure** - Keep users informed
6. **Use descriptive job names** - Easy to identify in logs

## Integration with Other Skills

- **notify-user**: Send emails when jobs complete or encounter issues
- **credential-activation**: Some jobs may need API credentials configured

## Troubleshooting

### Job not running?
1. Check `enabled: true` in frontmatter
2. Verify cron expression syntax
3. Check `.claude/scheduled/` directory exists
4. Review scheduler service logs

### Job running but failing?
1. Check Session State for error notes
2. Verify system prompt is complete
3. Check if required credentials are configured
4. Review max_turns limit

### Need to run immediately?
The scheduler service will execute jobs based on their cron schedule. For immediate execution, ask the user to trigger a manual run from the TeamDay UI.
