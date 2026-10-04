---
name: ryan-codex-automation-workflow
description: Use when the user asks to create, update, inspect, delete, or troubleshoot Codex scheduled tasks, recurring automations, reminders, monitors, follow-ups, cron jobs, heartbeat tasks, or asks whether Codex can run something later.
---

# Ryan Codex Automation Workflow

## Purpose

Create and manage Codex App automations without falling back to ad hoc shell cron, manual reminders, or guessing CLI support. Prefer Codex native automation tools first.

This is an optional recommended skill. It should not be part of the default first-run experience because most users only need it after they start asking Codex to continue work later, run recurring checks, or monitor something.

## When To Use

Use this skill when the user asks about:

- Scheduled tasks, automations, reminders, recurring jobs, monitors, follow-ups, or "continue this later".
- Creating a project-bound automation that should run inside a repository later.
- Updating, viewing, pausing, deleting, or troubleshooting an existing Codex automation.
- Whether Codex can run something later or notify the user later.

## Default Flow

1. Briefly explain what will be scheduled and what it will not do.
2. Use the native Codex automation capability when available. Do not create shell `cron`, `launchd`, or workaround scripts unless the user explicitly asks for OS-level scheduling.
3. Before creating a new automation, inspect existing automations under `${CODEX_HOME:-$HOME/.codex}/automations/*/automation.toml` with targeted search for the requested name, project path, or key prompt terms. Prefer updating a matching automation over creating a duplicate.
4. Choose the right automation type:
   - Use `heartbeat` for proactive follow-ups attached to the current thread, especially short delays or "continue this task later".
   - Use `cron` for standalone recurring jobs against one or more project/workspace directories.
5. Keep the automation prompt self-contained: purpose, prerequisites, project path when relevant, exact commands or steps if provided, stop conditions, and completion report format.
6. After create/update, view or otherwise verify the automation exists and report the id, status, schedule, destination, project/path, and prerequisites.

## Scheduling Rules

- Use user-facing plain language for schedules. Do not show raw RRULE strings unless the user explicitly asks.
- Interpret requested times in the user's locale when the platform supports it.
- For local wall-clock schedules, use recurrence fields such as frequency, weekday/month day, hour, minute, and second. Avoid timezone tricks unless the automation tool requires them.
- For "first business day" or holiday-aware schedules, confirm whether a close approximation is acceptable. If native recurrence cannot express it safely, schedule a reminder that asks the user to confirm before running.
- When a task depends on login state, GUI state, browser tabs, external system availability, or manual prep, encode that as a prerequisite and tell the automation to stop instead of taking destructive or data-changing action.

## Prompt Design

Automation prompts should include:

- Task name and purpose.
- Clear prerequisites.
- Exact project directory when relevant.
- Exact commands or steps, if the user provided them.
- Stop condition when prerequisites are missing.
- Completion report format: outputs, changed files, counts, failures, risks, and next step.

Keep prompts self-contained but avoid secrets, credentials, private logs, browser session details, or unnecessary internal context.

## Safety

- Do not create local shell `cron`, `launchd`, or workaround files unless the user explicitly asks for local OS scheduling instead of Codex App automation.
- Do not send private repository diffs, logs, credentials, customer data, or browser session details to external services.
- For automations that modify a repository, preserve existing worktree changes, read the project's `AGENTS.md`, and follow the repository's branch and validation rules.
- If automation creation is unavailable in the current host, say so clearly and offer the closest safe fallback, such as a manual checklist or a reminder request.

## Closeout

Finish with:

- Automation id and active/paused status.
- Human-readable schedule.
- Project/path or target thread.
- Whether existing automations were checked.
- Validation result from view/inspection.
- Any prerequisites the user must maintain.
