---
name: triggers
description: "Create and manage condition-based Manus automations using provider events, webhooks, or scheduled JavaScript monitoring. Also use to inspect executions and debug saved script Triggers. For reminders or recurring instructions without a monitored condition, use manus-config ScheduleTask instead."
compatibility: opencode
---

# Triggers

Prefer a discovered event with filters. Consider a scheduled script only when the event catalog cannot express the requested condition—not to bypass unavailable resources, missing authorization, or validation errors. Scripts cannot receive webhook or mail input. Do not monitor by polling in an Agent loop; a recurring ScheduleTask that asks an Agent to check a condition is such a loop. When neither an event nor an approved script can express the condition, report the limitation. Never edit connector configuration or account authorization to make a Trigger succeed; report the authorization failure instead. Call Trigger tools only as native MCP tool calls; `manus-mcp-cli` in the terminal cannot authorize them.

When talking to the user, describe what the Trigger does: an event trigger (runs when a connected service reports an event), a webhook trigger, or a scheduled script trigger. Tool field names such as `fixed`, `script`, entries, and bindings are for tool calls only; do not use them or internal service names in replies.

## Discover and configure an event

1. Call `triggers.list_events` with a focused `query` (one string or up to 10 OR terms). It returns a compact, ranked index; source and event matches come first, and events matched only through settings or filter fields list `matched_fields` (or `matched_field_count` when capped). Search is local and case-insensitive; broaden or remove the query before concluding that an event is unsupported. `omitted_events` means the index was capped: narrow the query rather than treating the missing events as absent. The same broaden-first rule applies to `triggers.list_data_apis`.
2. Call `triggers.list_events` again with the chosen `source` and `event_type` to get its full definition, then read `settings`, `filter_fields`, and availability. Each filter field names an `operator_set`; look it up in `operator_sets` for the operators, `operand_kind`, and `value_schema`. If the definition is too large it arrives as an outline, with `values_count` instead of `values`; call again with `field_keys` naming the settings and filter fields you need to read them in full. An outline still means the event is supported. These live definitions govern supported fields, operators, operands, and polling cadence; do not invent a local catalog.
3. Resolve required settings using `triggers.list_event_options`. Pass the setting or filter field's key and declared dependencies, using setting keys such as `account_uid`, not dotted paths. Select stable option values, then place settings at their declared `value_path`. Acquisition settings belong in `params`/bindings; business conditions belong in `filter`.
4. Refresh discovery after selecting resources that determine available fields. For Google Forms, request the exact source/event with `dependencies: { account_uid, form_uid }` before using the returned question fields. Discard stale options and pagination tokens when dependencies change.

Follow option pagination. For Slack `channel_uid`, instead supply a non-empty `query` and omit `page_token`: the tool searches every page itself. A timeout or overly broad search is an error, not an empty result. `is_member` says whether the user has joined the channel; channel-scoped events require it. Options with `unavailable_code` are listed for guidance but must not be selected: `provider_reauthentication_required` means the account or workspace needs to be reconnected in Manus (for example an expired token that can no longer refresh) before it can be used. Tell the user which account to reconnect; do not silently pick another resource.

Combine `binding.connector.*` settings into one binding; omit account/resource selections not exposed by discovery. For mailbox values such as `mail_user:42`, split at the first colon into `binding.mailbox = { kind, mailbox_uid }`.

### Filters

```text
filter.groups[]                    OR between groups
  .conditions[]                    AND within a group
    { field_key, operator, value?, case_sensitive? }
```

Use only advertised operators and their `operand_kind` / `value_schema`. Omit `value` for operand-free operators, preserve exact decimal strings, and set `case_sensitive` only when supported. Missing or incomplete values are unknown, including under negation; they are not explicitly empty values.

Omit the filter to accept every event. Groups cannot be empty, nested, or negated. Use one entry per listening identity; represent alternative conditions with OR groups rather than duplicate listeners. Multiple entries are also OR—not cross-event AND or event-order correlation.

## Create

Use `triggers.create_trigger` for event-based entries. If a script fallback is needed, explain the event limitation and propose what the script would monitor and how often. Ask the user to approve that alternative and wait for explicit approval before starting script creation; a general monitoring request is not consent to use a script. Once approved, use `triggers.create_script_trigger` with one schedule. If the user explicitly asks for a script but a discovered event can express the condition, explain the event option and let the user choose.

Both tools create an enabled Trigger immediately; there is no draft or pre-create test.

- Supply a concise `title` and an actionable `instruction` for the receiving Agent, including context needed in a new session. Place `{{payload}}` where the event data should appear; without it the data follows the instruction. Event triggers supply the event's data; script triggers supply the payload they return. The receiving Agent sees that data as untrusted content, not instructions. Keep the user's wording; tell the user about any text you add to it.
- Generate one `create_request_uid` per intended configuration. Reuse it only for retries of that same configuration, including uncertain outcomes.
- Omit `target` for the current session. Select another destination and connector accounts only from verified user context.
- For each fixed entry, send its discovered `source` and `event_type`; omit `entry_uid` for new entries. Provider polling uses the catalog cadence, not a user-supplied schedule.
- Return the service-confirmed resource link and state. Distinguish an enabled definition from a source that is pending synchronization or credential setup.

### Schedules

Use `triggers.preview_schedule` before creating or replacing a timed entry. Choose exactly one schedule branch: `interval`, `cron`, or `once`. Use decimal-string milliseconds, IANA timezones, and timestamps with explicit offsets.

Recurring schedules on event triggers require at least 10 minutes; script triggers require at least 15 minutes on free plans or 5 minutes on paid plans. Once schedules have no recurring minimum. Preview checks only the most permissive (5-minute) minimum, so creation or update can still fail the mode- and plan-specific check.

### Webhooks

Use `source: "webhook"` with an `event_type` discovered through `triggers.list_events`, without a binding or schedule. The event type belongs to the configuration; senders do not add it to HTTP payloads. Filter only on fields exposed by discovery.

Events that receive requests get a webhook URL: omit `webhook_suffix` for new entries (the tool generates it) and preserve it when updating existing entries. `webhook.retrieve_poll` polls a JSON URL instead and never has a webhook URL or `webhook_suffix`; an existing entry cannot switch between polling and receiving. Bearer credentials and `auto_confirm` are managed in Manus, never tool inputs or instruction content. If authentication is required but no credential is configured, direct the user to the Triggers page in Manus.

### Scripts

Pass the script in the `code` argument of a native MCP tool call even when it is long, not through a file.

Before authoring a script, read [Connector runtime](references/connector-runtime.md): its **Script runtime** section is the complete `ctx` contract (KV, Data APIs, AI, connectors, return value, limits). Use only the APIs it documents—do not guess names such as `ctx.data_api`. The script is an async function body receiving `ctx`; return `{ payload: string }` to trigger, otherwise `null`/`undefined`. Keep state idempotent and bound external reads, pagination, KV, and payload size.

`triggers.dry_run_script` accepts a saved `trigger_uid` only. It neither injects the instruction nor advances production KV, but can perform real external operations and consumes Data API budgets. Inspect the saved code and confirm authorization for those effects before running it. Dry runs are limited to 6 per user per minute, and a dry run waits only about 50 seconds: a timeout (`code` `deadline_exceeded`) means the script is too slow to dry-run, not that it failed, so do not retry it; check the first real execution with `triggers.get_execution` instead. Dry runs are not a creation gate, but for a read-only script that finishes quickly run one after creation and fix any failure before reporting the Trigger as working.

## Manage existing Triggers

- **Find:** Paginate `triggers.list_triggers`. Results are summaries, not update templates.
- **Edit:** Read `triggers.get_trigger`, then send the complete configuration to `triggers.update_trigger` with the exact decimal-string `expected_revision`. This is full replacement: preserve unrelated fields, title, existing `entry_uid` values, and webhook suffixes. Omitted entries are deleted; mode cannot change. Exclude read-only entry display data.
- **Pause, resume, or delete:** Use `triggers.set_trigger_enabled` or `triggers.delete_trigger` for the user's requested operation with the current revision. Re-enabling rechecks source/target/resource authorization and the enabled-trigger limit; re-enabling a disabled script trigger also rechecks its recurring schedule against the minimum gap of the current plan (for example after a downgrade), so update the schedule if that fails. Re-enabling a `once` schedule whose time has passed does not run it again; update `fire_at` to a future time instead.
- **Enabled-trigger limit:** When creating or re-enabling fails on the enabled-trigger limit, report the limit and let the user choose which Trigger to disable, delete, or merge. Never disable, delete, update, or merge another Trigger to make room unless the user explicitly chose that change, even one the user mentioned or one that watches the same resource.
- **Inspect:** Use `triggers.list_executions` and `triggers.get_execution` for history and attachment links; do not poll history or expect raw event bodies.

On a revision conflict, re-read and apply the user's change to the latest configuration. For validation errors, use `field_errors` to locate the invalid field. A `field_errors` code `provider_reauthentication_required` means the selected account or workspace must be reconnected by the user; an entry paused with `last_error_code` `provider_reauthentication_required` resumes only after reconnecting and then disabling and re-enabling the Trigger. Report authorization or source-confirmation failures as such; do not blindly retry, switch accounts, or switch to a script.

### Debug a failed script

`triggers.get_execution` reports `status`, `error_code`, and a bounded `error_message` (exception name and message). Codes:

| `error_code` | Meaning |
| --- | --- |
| `script_failed` | Uncaught error or non-zero exit (including `process.exit(1)`); `error_message` names the exception. |
| `script_timeout` | The run exceeded its time limit. A dry run cannot reproduce it; reduce the work per run (smaller pages, batches carried in KV). |
| `invalid_return` | The value was not `null`/`undefined`/`{ payload: string }`, the script wrote to stdout, or it called `process.exit(0)` before returning. |
| `runtime_unreachable` | No result from the execution runtime; usually transient. |

`console.*` output is not stored. A failed dry run returns only the first 2 KiB of stderr—console output first, the stack last—so when `error_message` is insufficient, reproduce with one dry run and keep diagnostic logging short. Correct the saved code with one `triggers.update_trigger`, then dry-run again; do not iterate edits on a live Trigger without telling the user.

### Debug a paused or silent event entry

When an event Trigger does not fire, read `triggers.get_trigger` first: each entry reports `runtime_status` and `last_error_code`, and `triggers.list_executions` with the `entry_uid` shows the failed run (`failed_stage`, `error_code`, `error_message`). An entry in `needs_attention` stops polling and does not resume on its own, even after the cause is fixed: the user must disable and re-enable the Trigger (or change its listening scope), which starts from a new baseline and does not deliver events from the paused period. Tell the user this when reporting a fix.

- Run `triggers.dry_run_entry({trigger_uid, entry_uid})` to reproduce the next scheduled check. It supports only connected-account polling entries: Gmail, Google Calendar, Google Workspace, Outlook Mail/Calendar, Shopify, Meta Ads, Instagram, Google Ads, GitHub and Notion events with `poll_interval_seconds > 0` in `list_events`. RSS, webhook entries (including `webhook.retrieve_poll`), Slack, X and push events are rejected with `failed_precondition`; for those, read `error_message` from `triggers.list_executions` / `triggers.get_execution` or wait for the next real execution. It reads from where that check would start and applies the current filter; a provider failure returns `error` as `<error_code>: <detail>`, and matches return the payload a real run would deliver. It makes real provider reads but never advances the entry, delivers, records an execution, or clears `needs_attention`.
- Entry dry runs share the 6-per-minute limit with `triggers.dry_run_script`. A dry run waits only about 50 seconds; a timeout (`code` `deadline_exceeded`) means the read (for example a large Notion data source scan) is too slow to dry-run and the entry was not changed. It is not a failure: do not retry it; inspect `error_message` in `triggers.list_executions` / `triggers.get_execution` or wait for the next real execution instead.
- Prefer a dry run over writing test rows into the watched resource. Do not add test data to shared or team-owned resources without the user's agreement, and remove any test data you did add.
- `provider_response_invalid` means the provider returned something the reader does not accept; the detail names the failed check (for example a property or row). Report it with the trigger and entry UIDs as a product issue; do not retry it or switch accounts.
- `triggers.update_trigger` and re-enabling can return an entry to `ready` without the cause being fixed. Confirm a fix with `triggers.dry_run_entry` or the next real execution before reporting that the error is resolved.
