---
name: max-tasks
description: Create, list, inspect, update, enable/disable, delete, and run your own Max automated tasks from the `max` CLI. Max tasks are automations or routines that run inside the user's personal Max agent — either Scheduled (cron) or Event-based (fired by an integration trigger like a new email, a calendar event starting, or a deal stage change). Use when managing Max's own recurring/triggered work, NOT customer-facing agents, and NOT user to-dos (those are `frontline user-tasks` for the personal inbox or `frontline object task` for a record's "To-do's" tab — see the notes-and-tasks skill).
allowed-tools: Bash(max:*)
---

# Max Tasks (automated tasks)

Max tasks are automations that run **inside your own Max agent**. Two kinds:

- **Scheduled (⏰ cron)** — run on a schedule (e.g. a daily 8am brief). Set with `--cron`.
- **Event-based (🔔 trigger)** — fire when something happens in a connected integration
  (new Gmail message, calendar event starting soon, HubSpot deal stage change, …). Set with `--trigger-slug`.

A task has `instructions` (what Max does when it runs) and may request access to extra connected integrations via `--integrations` (the agent will only have access to the integrations you select here). Max tasks execute inside an isolated sandbox with access to all database record-types, system tools, and custom tools. When the task runs, Max executes the instructions, and if notifications are enabled, it will send the final output of the task run directly to you (e.g. by email, WhatsApp, or Slack).

> **Not** the same as:
>
> - `frontline user-tasks` (the account "to-dos" inbox) — those are human to-dos.
> - `frontline object task` (tasks attached to a CRM record).
>
> Those are managed with the `frontline` CLI. Max tasks steer **Max itself** and live on the `max` CLI.

Auth is the same per-user API key the `frontline` CLI uses (`max auth login <key>`).

## Task Output & Notifications (Crucial)

When Max executes a task:

1. **Direct Notification Mapping:** The final answer or text output returned by the agent at the end of its run is **EXACTLY** what gets sent to you via the selected notification channels (`--notify-email`, `--notify-whatsapp`, or `--notify-slack`).
2. **No Tools Needed for Sending Reports:** You do **NOT** need to write instructions telling Max to call separate tools (like email sending, Slack message posting, etc.) to deliver the summary or report. The system automatically intercepts the agent's output and dispatches it according to your notify settings.
3. **Formatting:** Max respects Markdown formatting, so structuring the final output using headers, lists, and tables will translate directly into a cleanly formatted email or message.

## Integrations & Tool Scoping (Crucial)

Although Max tasks execute inside an isolated sandbox with access to all CRM record-types, custom API tools, and system tools, **the agent will only have access to the specific connected integrations (e.g. `"gmail"`, `"googlecalendar"`, `"hubspot"`) that you explicitly select via the `--integrations` flag**. If you need the agent to read emails or manage events, you MUST explicitly select them; otherwise, the agent will not have access to those tools/services.

## Discovery first (look up the IDs you'll need)

Before creating a task, gather the related IDs/slugs:

```bash
# Event triggers: valid --trigger-slug values, their config fields, and which integrations you have connected.
# The response also lists `connectedToolkits` — the valid values for --integrations.
max tasks triggers --pretty

# Starter templates (default cron/trigger/config you can copy).
max tasks templates list
max tasks templates get 3
```

`max tasks triggers` tells you a trigger needs e.g. a `spreadsheet_id` — but not which one.
To turn "my Q3 budget sheet" into the actual ID, resolve it with the `frontline` CLI
(see the `integrations` skill):

```bash
frontline integrations resources googlesheets spreadsheets --query "Q3 budget" --table
frontline integrations resources googledrive folders --query Invoices
frontline integrations resources salesforce sobjects
```

## List & inspect

```bash
max tasks list --pretty
max tasks list --enabled true --name "brief"
max tasks get <taskId>
```

## Create

`--name` and `--instructions` are required, plus **exactly one** of `--cron` or `--trigger-slug`
(a task is either scheduled or event-based, never both). Tasks are enabled by default; pass
`--inactive` to create one paused.

**Scheduled task:**

```bash
max tasks create \
  --name "Morning brief" \
  --instructions "Summarize today's calendar and any overnight emails that need a reply." \
  --cron "0 8 * * 1-5" \
  --notify-email true
```

**Event-based task** (run `max tasks triggers` first to find the slug + config fields, and to
confirm the integration is connected):

```bash
max tasks create \
  --name "Meeting prep" \
  --instructions "Prepare a one-page brief on the attendees and recent threads." \
  --trigger-slug GOOGLECALENDAR_EVENT_STARTING_SOON \
  --trigger-config '{"minutes_before":15}'
```

Optional flags (all take JSON where noted):

- `--integrations '["gmail","hubspot"]'` — toolkits the run may use (must be connected).
- `--notify-email|--notify-whatsapp|--notify-slack <true|false>`, `--slack-channel <id>` (omit for DM).

## Update, enable/disable

`update` is a **merge**: it fetches the task's current state, applies the flags you pass, and
re-sends the full definition — so you only specify what changes.

```bash
max tasks update <taskId> --instructions "New instructions ..."
max tasks update <taskId> --cron "0 9 * * 1-5"          # change schedule
max tasks update <taskId> --trigger-slug GMAIL_NEW_GMAIL_MESSAGE   # switch CRON → event (clears cron)
max tasks update <taskId> --notify-slack true --slack-channel C0123
```

Toggling is its own shortcut (also a merge under the hood):

```bash
max tasks enable <taskId>
max tasks disable <taskId>
```

> `--cron` and `--trigger-slug` are mutually exclusive — setting one clears the other.

## Run now

Manually execute a task immediately. **Scheduled (cron) tasks only** — event-based tasks can't be
run on demand (they wait for their trigger) and are rejected.

```bash
max tasks run <taskId>
```

## Delete

```bash
max tasks delete <taskId>
```

---

## See also

- Reusable instruction sets for Max: the `max-playbooks` skill.
- Chatting with Max: the `max-chat` skill. Auth: the `max-auth` skill.
- Full reference: <https://docs.getfrontline.ai/cli>. App walkthroughs: <https://help.getfrontline.ai>.
