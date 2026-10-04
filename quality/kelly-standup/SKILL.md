---
name: kelly-standup
description: Team standup board (Busabase App-in-Skill) for team leads. Use when the user invokes $kelly-standup or /kelly-standup, or asks for standup, daily standup, 晨会, daily check-in, team status board, 团队日报, blockers, who's working on what, team digest, check-in streaks, missing check-in reminders, or collecting async updates from Slack/WeCom/Discord/WhatsApp/docs into one board.
metadata:
  category: comms
  tags:
    - risk:local-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-standup
    resources:
      - members
      - days
      - checkins
      - blockers
      - reminders
      - settings
    risk: local-write

---

# Kelly Standup

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Standup today board"></td>
    <td width="50%"><img src="assets/screenshots/blockers.webp" alt="Kelly Standup blockers"></td>
  </tr>
  <tr>
    <td><strong>Today board</strong><br>Daily standup at a glance: team digest, participation count, and per-member yesterday/today/blockers cards with source badges.</td>
    <td><strong>Blockers</strong><br>All blockers across the team with severity, age, and agent-suggested next actions.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/members.webp" alt="Kelly Standup members"></td>
    <td width="50%"><img src="assets/screenshots/reminders.webp" alt="Kelly Standup reminders"></td>
  </tr>
  <tr>
    <td><strong>Members</strong><br>Team roster with check-in streaks, 30-day participation, open blockers, and per-member update timelines.</td>
    <td><strong>Reminders</strong><br>Approval-gated nudges for missing check-ins — drafted by the agent, sent only after review.</td>
  </tr>
</table>

## Overview

Use this skill as Kelly's team standup desk: see at a glance what everyone is
working on each day. Team members post async updates wherever they already
talk — Slack, WeCom, Discord, WhatsApp, a shared doc, or pasted text. Turning
that raw material into structured updates (yesterday / today / blockers /
mood) is LLM work the agent does in conversation;
`scripts/ingest_updates.mjs` is the trusted step that validates the resulting
payload and writes it into Busabase (no browser can read a chat export or
call a chat API with secrets). The AirApp shows today's per-member cards,
participation, the blocker list, past days, and a reminder review queue for
chasing missing check-ins. `scripts/execute_decisions.mjs` turns approved
reminders into a concrete send plan; it never sends anything itself.

There is deliberately **no scheduling or cron inside this skill**. It is
invoked on demand: when the user asks for standup, the agent collects
whatever updates exist at that moment, ingests them, and opens the board.
Recurring behavior belongs to the user's own habits or external schedulers,
never to this skill.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, collect and ingest the latest updates and give the user the
clickable AirApp URL (or the local preview URL when local preview is
explicitly requested). Use chat-only mode only when the user says "纯聊天",
"chat only", "不要打开 UI", or similar; then present the board as text and
reminders as numbered items (`Reminder #1`) directly in the conversation.

**The AirApp itself never talks to Slack/WeCom/Discord/WhatsApp/email.** It
reads and writes Busabase records only. Both external-input directions are
genuinely trusted-process-only, since a browser cannot parse an arbitrary
chat export or hold chat-platform credentials: `scripts/ingest_updates.mjs`
writes the agent-parsed check-ins/blockers/reminders into Busabase, and
`scripts/execute_decisions.mjs` is the one place that plans an approved
reminder's send operation — sending the actual message stays outside the app,
via kelly-messenger / kelly-email, after human approval.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-standup-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and report
the exact missing dependency. Do not invent a second data backend.

## Boundary

- The skill may read team-consented channels only (kelly-messenger snapshots, chat exports the user provides, shared docs, pasted text), parse them, and write the resulting structured updates and drafted reminders to Busabase via `scripts/ingest_updates.mjs`.
- Ingestion parses only what the team has agreed to share for standup. Store the minimum: structured items plus a short `raw-excerpt` for provenance — never whole chat logs, and no member PII beyond name/role/timezone/channel that the team shares.
- The AirApp reads and writes Busabase records only. It must never send messages, call a chat/email API, or perform any other external side effect.
- Reminders (nudges for missing check-ins, blocker escalations) are approval-required: the agent drafts them, the human approves in the app, `scripts/execute_decisions.mjs` plans the send operation, and sending happens outside the app via kelly-messenger / kelly-email. Member contacts live only in env vars referenced by `contact-env` on the member record — the AirApp never reads or displays the value, only whether the name is configured.
- Treat chat exports, member contact values, and Busabase credentials as sensitive. Never commit them.

## Busabase Resources

Six Bases under one application Folder (`kelly-standup`), declared in
`content/kelly-standup-app/app/js/config.js` and the generated template sidecars under `content/`:

- `members`: team roster — name, role, timezone, channel, active, `contact-env` (an env var *name*, never a value), notes.
- `days`: one row per recorded standup day — digest paragraph and who is on leave.
- `checkins`: one row per member per day — yesterday/today lists, blockers (nested JSON, matching the per-update blocker shape used across the team board), mood, submitted-at, source, raw excerpt.
- `blockers`: the blocker registry, deduplicated across days by content hash — severity, status, suggested action, raised/resolved dates.
- `reminders`: the review queue — type, target member, channel, title, reason, editable draft, workflow `status`, the human verdict fields (`decision-action`/`decision-note`/`decided-at`), and the execution plan (`execution-status`/`execution-operations`/`execution-detail`) written by `scripts/execute_decisions.mjs`.
- `settings`: one row (`record-id: "team"`) with team name/timezone/workdays, digest style, and standup questions.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/standup-schema.md` for
exact field shapes. Streaks, 30-day participation, per-day participation,
and the missing-today/open-blockers metrics are all recomputed client-side
from these Bases on every read — never stored.

## First Run And Onboarding

On invocation, check the `settings` Base for a `team` row. If it is absent,
guide setup before collecting real updates: ask, turn by turn, for the team
profile (name, timezone, workdays), members (name, role, timezone, and which
channel each posts standups in, plus which env var holds their contact for
reminders), the standup questions (default: yesterday / today / blockers),
and digest style. Never ask the user to paste contact values or secrets into
chat; they belong only in local env files, referenced by `contact-env` names.
Write the team profile and roster with:

```bash
node skills/kelly-standup/scripts/ingest_updates.mjs onboarding-payload.json --apply
```

where `onboarding-payload.json` carries `team`, `members`, and a `date` (any
recent workday — the payload shape always requires one; `updates`/`reminders`
can be empty on this first run). See `references/standup-schema.md`.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-standup-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/today` (default): today's board — human-attention panel (missing check-ins, open blockers, reminders awaiting approval), the agent-written team digest paragraph, participation stat (e.g. `6/8 submitted`) with an inline bar, then per-member cards: avatar initial, name + role, submitted time + source badge, Yesterday / Today / Blockers sections (blockers highlighted by severity), mood dot. Missing members get a visually distinct "not submitted" card with their last check-in date and a link to the drafted reminder; on-leave members get an on-leave card.
- `#/members` and `#/members/<id>`: roster — name, role, timezone, channel, check-in streak, 30-day participation, open blocker count, last submission. Detail shows a day-by-day timeline of recent updates, the member's open blockers, and notes.
- `#/blockers`: all blockers across the team — severity badge, owner, raised date, age, status (`open`/`resolved`, filterable), the linked day, and the agent-suggested next action per blocker.
- `#/reminders`: the review queue with workflow states `needs_review / changes_requested / approved / done / blocked`. Each card shows the stable ref (`Reminder #1`), type badge (missing check-in / blocker escalation), target member, channel badge, the reason, an editable message draft, a `Review note`, and approve / request changes / revise (save note) / block buttons that write the verdict directly onto the reminder record. Approved items are planned by `scripts/execute_decisions.mjs` and sent by the agent outside the app via kelly-messenger / kelly-email.
- `#/history` and `#/history/<date>`: recent days with an inline-SVG participation bar and one-line digest; selecting a date shows that day's full board (same card layout as today).
- `#/settings`: sanitized config — team profile, members with `contact-env` readiness booleans, standup questions, workdays, digest style, and onboarding state. Never exposes contact values or secrets.

Demo mode:

- `?demo=today`, `?demo=members`, `?demo=blockers`, `?demo=history`, and `?demo=detail` (a member's update timeline) select named mock scenes.
- `lang=en` or `lang=zh` forces UI chrome language; with `lang=zh` the demo content itself (中文姓名、角色、日报内容、阻塞、摘要、提醒草稿) is meaningfully localized for Chinese screenshots.
- Deep links such as `/?demo=today&lang=zh#/today` must work.
- Demo mode never reads or writes Busabase.

UI language: English and Chinese chrome with `Auto` default (browser language), plus an explicit selector persisted locally. Keep real member names and update content in their original language.

## Collection Workflow

Invoked on demand — there is NO cron and NO scheduler in this skill. Each run:

1. Ask where today's updates live (or use what the user already provided): the kelly-messenger local snapshot, a Slack/WeCom/Discord/WhatsApp export, a shared doc, or text pasted into chat. Raw material stays outside git.
2. Parsing is LLM work: split the raw material into one update per member, mapped to existing `member-id`s on the roster — `yesterday[]`, `today[]`, `blockers[]` (each with severity, and `status: "resolved"` when a member says a previous blocker is cleared), optional `mood`, `submitted_at`, `source`, and a short `raw_excerpt`. Note members on leave in `on_leave[]`.
3. Write the digest: a short agent-written paragraph summarizing the day (what shipped, what is blocked, who is missing), included as `digest` in the payload.
4. Draft reminders for missing check-ins or aging high blockers as `reminders[]` payload items (`needs_review` by default).
5. Merge deterministically with `node scripts/ingest_updates.mjs <payload.json> --apply`. The script validates against the roster, upserts checkins by member + date (re-ingesting is idempotent), dedupes blockers by content hash and applies resolve transitions, upserts reminders with stable content-hash ids (resetting to `needs_review` only when a reminder's content actually changed, preserving a human's pending decision otherwise), and upserts the day's digest/on_leave list. Omit `--apply` first to see a dry-run validation summary.
6. Give the user the AirApp URL (or local preview URL) pointed at `#/today`.

## Reminder Workflow

1. The user reviews drafted reminders in `#/reminders` and decides via approve / request changes / revise (save note) / block — written directly onto the reminder record through `busabase-sdk`. From a standalone local preview the write merges immediately (trusted operator); from the deployed AirApp it creates a pending ChangeRequest for the trusted process to merge.
2. For a reminder moved to `changes_requested`, re-draft the message per the review note and re-ingest with `scripts/ingest_updates.mjs --apply` so the item returns to `needs_review`.
3. On "execute" / "send approved reminders": run `node scripts/execute_decisions.mjs --apply` to re-read approved reminders from Busabase and write a concrete `send_reminder` plan (channel, target, contact-env readiness, message draft) onto each — it performs no external side effect. Then send the actual messages via kelly-messenger / kelly-email using the `contact-env` referenced contacts, and record the outcome back onto the reminder (e.g. via a follow-up `ingest_updates.mjs` note, or by editing the record directly).
4. Never send a reminder that is not `approved`, and never plan/send an already-`done` reminder twice — `scripts/execute_decisions.mjs` only acts on `status: "approved"`.

## Safety Defaults

- Treat every outbound nudge as approval-required, human-visible communication: friendly tone, no shaming, no manager-speak the user did not approve.
- Store only structured updates and short excerpts; keep raw exports outside git and outside Busabase.
- Expose only `contact-env` names (never contact values) in UI state, logs, and reports; `scripts/execute_decisions.mjs` is the only process that checks whether the referenced env var is actually set.
- Keep merges idempotent: stable member ids, blocker content hashes, reminder content-hash ids, so repeated ingests do not duplicate work.
- If the UI and schema disagree, stop and fix the schema or UI before executing anything.

## Useful Commands

```bash
node skills/kelly-standup/scripts/ingest_updates.mjs payload.json
node skills/kelly-standup/scripts/ingest_updates.mjs payload.json --apply
node skills/kelly-standup/scripts/execute_decisions.mjs
node skills/kelly-standup/scripts/execute_decisions.mjs --apply
pnpm --dir skills/kelly-standup/content/kelly-standup-app dev
```

In normal use, invoke `/kelly-standup`, let the skill ingest today's updates, and open the AirApp.
