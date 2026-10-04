---
name: kelly-tickets
description: Complaint/ticket triage-and-dispatch App-in-Skill (Busabase App-in-Skill) for property managers, facilities teams, and helpdesk leads. Use when the user invokes $kelly-tickets or /kelly-tickets, or asks for complaint triage, ticket dispatch, 投诉, 工单, 派单, property management complaints, helpdesk queue, intake from WeChat exports/call logs/front-desk forms, crew assignment, SLA board, dispatch approval, or ticket resolution tracking.
metadata:
  category: sales-crm
  tags:
    - risk:gated-write
    - industry:property-management
    - surface:busabase
    - surface:wechat
  busabase:
    template: true
    folderSlug: kelly-tickets
    resources:
      - crews
      - intake
      - tickets
      - proposals
      - sync-log
      - settings
    risk: gated-write

---

# Kelly Tickets

## Overview

Use this skill as Kelly's complaint triage-and-dispatch desk. Complaints and requests arrive scattered across WeChat group exports, phone-call logs, front-desk forms, and email — reading those local exports is a genuine external operation a browser cannot perform, so `scripts/ingest_intake.mjs` is the only place a complaint enters the system. The agent classifies each ticket (category, urgency, unit/location) and proposes a dispatch (crew, priority, SLA) via `scripts/apply_triage.mjs`; the human reviews dispatch proposals in a Busabase-backed App-in-Skill review queue and approves or edits; a board tracks every ticket to resolution with an auditable history trail. `scripts/execute_decisions.mjs` prints the crew-notification plan for approved dispatches — the AirApp itself never sends a message or mutates a remote system. The demo persona is residential property management, but the same flow fits facilities, IT helpdesk, or any dispatch workflow.

Default behavior is AirApp-first. Unless the user explicitly asks only for explanation, ingest/triage what's due and give the user the clickable AirApp URL (or the local preview URL when local preview is explicitly requested). Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar; then present numbered proposals (`Dispatch #1`) directly in the conversation.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Tickets overview"></td>
    <td width="50%"><img src="assets/screenshots/board.webp" alt="Kelly Tickets board"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Dispatch command desk with SLA risk, weekly intake by channel, category distribution, and crew load.</td>
    <td><strong>Board</strong><br>Tickets tracked across open, assigned, in-progress, waiting, and resolved with SLA indicators and history timelines.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/dispatch.webp" alt="Kelly Tickets dispatch queue"></td>
    <td width="50%"><img src="assets/screenshots/intake.webp" alt="Kelly Tickets intake"></td>
  </tr>
  <tr>
    <td><strong>Dispatch queue</strong><br>Agent-proposed crew assignments with priority, SLA target, reasoning, and an editable note to the crew.</td>
    <td><strong>Intake</strong><br>Raw complaints from WeChat, phone, forms, and email with classification fields and convert-to-ticket controls.</td>
  </tr>
</table>

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-tickets-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## Boundary

- Intake parsing is local: `scripts/ingest_intake.mjs` reads WeChat exports, call logs, and mailbox dumps the user provides and writes normalized rows to Busabase. It never fetches complaints from remote systems on its own.
- The AirApp reads and writes Busabase records only. It never sends messages, calls crews, replies to residents, or mutates remote systems.
- Any outbound crew notification or resident reply is approval-required through the dispatch queue and executed by the agent OUTSIDE the app via other skills (messenger/email/WeChat) after `scripts/execute_decisions.mjs` produces the plan. `scripts/execute_decisions.mjs` never performs these operations itself — it only writes an execution marker onto the proposal.
- Crew contacts are env-var references (`contact_env`) only — never store phone numbers or webhook URLs in Busabase. Resident PII stays masked in the UI (`contact_masked`); `scripts/ingest_intake.mjs` re-masks long digit runs defensively.
- Treat all complaint/resident data as sensitive. Never commit local export files or env files.

## Busabase Resources

Six Bases under one application Folder (`kelly-tickets`), declared in `content/kelly-tickets-app/app/js/config.js` and the generated template sidecars under `content/`:

- `crews`: crews that tickets can be dispatched to (name, skills, `contact_env`).
- `intake`: raw complaints/requests as they arrived on a channel, before or after triage, plus the human decision (convert to ticket / ignore) on the same row.
- `tickets`: tickets tracked from classification through resolution, with an append-only history timeline.
- `proposals`: the dispatch review queue — proposed crew/priority/SLA, the human decision, and the execution marker on the same row.
- `sync-log`: append-only history of ingest/triage/execute runs.
- `settings`: one row (`record-id: "config"`) with property profile, channels, categories, and SLA rules.

Resources provision lazily through an idempotent Busabase ChangeRequest the first time the app runs in a Space; see `references/tickets-schema.md` for exact field shapes. SLA state and crew load are recomputed client-side from the stored rows on every read (`content/kelly-tickets-app/app/js/tickets-model.js`'s `buildSnapshot`), so the desk is always fresh regardless of when a browser session loads it relative to the last ingest/triage run. The browser has no access to the agent's environment variables, so the Settings view shows each crew's `contact_env` name only, not a live readiness boolean.

## First Run And Onboarding

On invocation, check the `intake`/`tickets` Bases. If both are empty, guide setup before ingesting real complaints: ask, turn by turn, property profile (name, buildings, timezone), complaint categories, crews (name, skills, and which env var holds each crew's contact), SLA rules per category+urgency, and which intake channels are in use. Never ask the user to paste contact values or secrets into chat; they belong only in local env files, referenced by `contact_env` names. Write the answers onto the Settings row and the Crews Base, then ingest:

```bash
node skills/kelly-tickets/scripts/ingest_intake.mjs /path/payload.json --apply
```

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL. Start `pnpm --dir content/kelly-tickets-app dev` only when local preview/debugging is explicitly requested.

Required app views (hash routes):

- `#/overview`: dispatch command desk — human-attention panel (proposals to approve, unclassified intake, SLA-breaching tickets), KPI cards (open tickets, avg resolution, SLA at risk, this week's intake with channel badges), category distribution bars, and crew load.
- `#/intake` and `#/intake/<id>`: raw intake stream — channel badge (WeChat/phone/form/email/walk-in), reporter, unit/location, complaint text, urgency guess, triage state. Detail shows the full text, attachments note, editable classification (category/urgency/unit), and convert-to-ticket or ignore actions.
- `#/dispatch`: the review queue with workflow states `needs_review / changes_requested / approved / done / blocked`. Each card shows the stable ref (`Dispatch #1`), ticket summary, proposed crew/assignee, priority, SLA target, the reason, an editable note to the crew, and approve / request changes / block buttons. Decisions write directly onto the proposal record through `busabase-sdk`.
- `#/board` and `#/board/<ticket_id>`: tickets grouped by status (`open / assigned / in_progress / waiting / resolved`) with category badge, unit, crew, age, and color-coded SLA indicator. Detail shows the full history timeline (intake → classification → dispatch → crew updates → resolution), masked reporter contact, and a resolution note field.
- `#/settings`: sanitized config — property profile, channels, categories, crews with `contact_env` names, SLA rules, data provider, and onboarding state. Never expose contact values or secrets.

Demo mode:

- `?demo=overview`, `?demo=intake`, `?demo=dispatch`, `?demo=board`, and `?demo=detail` (a ticket history) select named mock scenes.
- `lang=en` or `lang=zh` forces UI chrome language; with `lang=zh` the demo content itself (property name, complaints, crews, reasons) is meaningfully localized for Chinese screenshots.
- Deep links such as `/?demo=dispatch&lang=zh#/dispatch` must work.
- Demo mode never reads or writes Busabase. Decision buttons still work but act on in-memory state only.

UI language: English and Chinese chrome with `Auto` default (browser language), plus an explicit selector persisted locally. Keep real resident/complaint data in its original language.

## Intake Workflow

1. Ask the user for the export/log location (WeChat group export, call log CSV/notes, front-desk forms, mailbox). Raw files stay outside git.
2. Parse the raw material into the ingest payload shape (see `references/tickets-schema.md`): one item per complaint — channel, channel-native `external_id` when available, reporter, contact (will be masked), unit/location, verbatim text, received time, plus first-pass `category_guess`/`urgency_guess`.
3. Write the payload JSON to a temp path and run `node scripts/ingest_intake.mjs <payload.json> --apply`. The script validates, dedupes by `channel + external_id` (falling back to a content hash), masks contacts, writes new rows into the Intake Base, and appends a Sync Log entry.
4. Re-ingesting the same export is safe: duplicates are skipped and reported. Without `--apply` it is a dry run.

## Triage And Dispatch Workflow

1. Classification is LLM work: read `intake` items in `new`/`classified` state (and any with `decision_action: "convert_to_ticket"`, the Busabase-only equivalent of a queued agent task), decide category, urgency, unit/location, and a ticket title; decide which crew fits and why (use crew skills, prior tickets for the same unit, and SLA pressure in the `reason`).
2. Merge deterministically with `node scripts/apply_triage.mjs <payload.json> --apply`: creates tickets (`T-1001`-style ids), computes `sla_due_at` from the Settings row's `sla_rules` (category+urgency, `*` wildcard, `sla_default_hours` fallback), assigns stable proposal refs, appends ticket history, and writes it all straight to Busabase. `ticket_updates[]` in the same payload records crew progress, status transitions, and resolutions.
3. Send the user to `#/dispatch` to review. Decisions write directly onto the proposal record; from a standalone local preview the write merges immediately (trusted operator), from the deployed AirApp it creates a pending ChangeRequest for the trusted process to merge.
4. Poll the `intake` Base for rows with `decision_action: "convert_to_ticket"` where `triage_state` is not yet `ticketed`: classify using the human-provided `decision_fields` and create the ticket via `apply_triage.mjs`. Poll the `proposals` Base for `status: "changes_requested"`: redraft the proposal per `decision_note` and re-run `apply_triage.mjs`.
5. After approvals, run `node scripts/execute_decisions.mjs` (dry-run) and show the plan; with user confirmation run `--apply`, then perform the real crew notifications via other skills (messenger/email), record outcomes back through `apply_triage.mjs`'s `ticket_updates[]`, and keep the board honest.
6. Re-read the `proposals` Base immediately before executing, and never execute items without an `approved` status.

## Board Semantics

- `open`: classified, no crew accepted yet (dispatch pending or unapproved).
- `assigned`: an approved dispatch reached a crew; nobody started work yet.
- `in_progress`: the crew reported starting work.
- `waiting`: blocked on residents, parts, weather, or vendors — not on the crew.
- `resolved`: work confirmed done; `resolved_at` set and a resolution note recorded.

SLA states are derived, never hand-set: `ok`, `at_risk` (under 25% of the SLA window left), `breached`, and `met` for resolved tickets — computed fresh on every read by `content/kelly-tickets-app/app/js/tickets-model.js`'s `computeSlaState`. History events are append-only — the timeline is the audit trail; never rewrite past events.

## Decisions And Execution Workflow

1. The user reviews at `#/dispatch`: approve, request changes (with a note), save an edited note-to-crew (revise), or block. Decisions write directly onto the proposal record.
2. On explicit user request to execute, run `scripts/execute_decisions.mjs` (dry-run by default; `--apply` writes `execution_status: "ready_for_agent"` onto each approved proposal with the concrete `notify_crew` + `update_board` operations and a message draft). No external side effects either way.
3. The agent then performs the approved crew notification outside the app (via messenger/email/WeChat) and records the real result via `apply_triage.mjs`'s `ticket_updates[]`. A second `--apply` run of `execute_decisions.mjs` finalizes the proposal's `execution_status` to `"executed"` and promotes its workflow `status` to `"done"` — this script never flips the workflow status on the first run itself.

## Safety Defaults

- Treat crew notifications, resident replies, fines/fees, lock-outs, towing, and anything customer-visible as approval-required.
- Mask resident contacts everywhere in UI state and logs; expose only `contact_env` names for crew contacts, never values.
- Keep merges idempotent: stable intake hashes, ticket ids, and proposal refs so repeated ingests and triage runs do not duplicate work.
- Never expose secrets through the settings view or logs; it shows column names and rules only.
- If the UI and schema disagree, stop and fix the schema or UI before executing anything.

## Useful Commands

```bash
node skills/kelly-tickets/scripts/ingest_intake.mjs payload.json --apply
node skills/kelly-tickets/scripts/apply_triage.mjs payload.json --apply
node skills/kelly-tickets/scripts/execute_decisions.mjs
node skills/kelly-tickets/scripts/execute_decisions.mjs --apply
pnpm --dir skills/kelly-tickets/content/kelly-tickets-app dev
```

In normal use, invoke `/kelly-tickets`, let the skill ingest/triage what's due, and open the AirApp.
