---
name: kelly-crm
description: Busabase-backed App-in-Skill CRM operator for contacts, companies, deals, and agent-drafted follow-ups in a reviewable follow-up queue. Use when the user invokes $kelly-crm or /kelly-crm, mentions CRM, pipeline, contacts, companies, deals, follow-ups, relationship management, meeting-note capture, outreach drafts, next steps, or wants to review/approve agent-drafted follow-up messages before they are sent through other channels.
metadata:
  category: sales-crm
  tags:
    - risk:gated-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-crm
    resources:
      - companies
      - contacts
      - deals
      - interactions
      - followups
      - settings
    risk: gated-write

---

# Kelly CRM

## Overview

Kelly CRM is a Busabase Cloud App-in-Skill. Its canonical product surface is the
AirApp in Busabase, not a separate local-data product. The same Hono source
supports an explicitly requested local preview with OAuth connection bootstrap.
It keeps a Busabase-backed dashboard over contacts, companies, deals, and
interactions, plus a review queue of agent-drafted follow-up messages. The
skill gathers and updates CRM data from whatever Kelly feeds it — emails,
meeting notes, chat asks — drafts follow-ups, and hands off an approved
follow-up to another channel skill (for example `kelly-email`) only after
explicit approval.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, update Busabase directly and give the user the clickable AirApp
URL. Start localhost only when local preview/debugging is explicitly
requested; it uses the same Busabase resources and never offers another data
provider. Use chat-only mode only when the user says "纯聊天", "chat only",
"不要打开 UI", or similar; in that mode present numbered follow-ups
(`Follow-up #1`) and take verdicts in the conversation, still writing them
through Busabase.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-crm-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and report
the exact missing dependency. Do not invent a second data backend.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly CRM overview"></td>
    <td width="50%"><img src="assets/screenshots/deals.webp" alt="Kelly CRM deal pipeline"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>CRM command desk with pipeline totals by stage, follow-ups due, recent activity, and network counts.</td>
    <td><strong>Deals</strong><br>Pipeline table across stages with amounts, probability, next steps, and a per-deal interaction timeline.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/contacts.webp" alt="Kelly CRM contacts"></td>
    <td width="50%"><img src="assets/screenshots/followups.webp" alt="Kelly CRM follow-up queue"></td>
  </tr>
  <tr>
    <td><strong>Contacts</strong><br>Contact list with relationship strength, last touch, and per-contact interaction history and open deals.</td>
    <td><strong>Follow-up queue</strong><br>Agent-drafted follow-up messages with editable drafts, risk badges, and approve/request-changes/block decisions.</td>
  </tr>
</table>

## Boundary

- The AirApp reads Busabase records, drafts follow-up messages, and records
  human decisions only through Busabase writes. It must never send emails or
  messages, call external APIs, or perform any external side effect.
- Outbound follow-up messages are always approval-required. Sending is
  delegated to other skills (for example `kelly-email`) and happens only
  after the user approves the specific follow-up. `scripts/execute_decisions.mjs`
  only marks an approved followup `done` with handoff metadata; it performs no
  sending itself.
- Treat all contact and deal data as sensitive. Never commit real contact
  details, tokens, or Busabase credentials.

## Busabase Resources

Six Bases under one application Folder (`kelly-crm`), declared in
`content/kelly-crm-app/app/js/config.js` and the generated template sidecars under `content/`:

- `companies`: name, domain, industry, size, location, notes.
- `contacts`: name, company, role, email, relationship strength, tags, last
  touch, next follow-up, agent notes, channels.
- `deals`: name, company, primary/linked contacts, stage, amount, currency,
  probability, next step, owner, dates, status, agent-suggested next action.
- `interactions`: contact, company, deal, type, direction, summary, source.
- `followups`: the review queue — contact, deal, channel, reason, risk
  badges, due date, workflow `status`, editable `suggested_reply`, and the
  human verdict fields `decision_comment` / `decided_at` / `decided_by`
  written directly onto the record (there is no separate decisions file).
- `settings`: operator profile, pipeline stages, channels, and the agent
  lock, one row per `kind`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/crm-schema.md` for exact
field shapes.

## Authentication

Busabase authentication is ambient inside the deployed AirApp, which must not
show OAuth, API-key, Base URL, provider, hosting, or Space controls.
Standalone loopback preview uses browser OAuth without exposing tokens; after
OAuth it auto-selects a single/open-source Space or requires a native
selector when several Spaces are accessible. It performs no app-resource read
or initialization before selection. `scripts/execute_decisions.mjs` (a
trusted process, not the AirApp) uses `BUSABASE_BASE_URL` /
`BUSABASE_API_KEY` / `BUSABASE_SPACE_ID` from the environment.

## Review Workflow

Follow-ups use the standard workflow states: `needs_review`,
`changes_requested`, `approved`, `done`, `blocked`. A human verdict
(`approve` / `request_changes` / `block` / `revise`) writes the new `status`
plus `decision_comment` / `decided_at` / `decided_by` directly onto the
followup record through `busabase-sdk`. From a standalone local preview the
write merges immediately (trusted operator); from the deployed AirApp it
creates a pending ChangeRequest for the trusted process to merge, per the
AirApp boundary in `$busabase-app-creator`.

1. When Kelly feeds new material (emails, meeting notes, chat asks): upsert
   companies/contacts/deals by stable domain id (`company_id`, `contact_id`,
   `deal_id`), append interactions, and draft new followups with
   `status: "needs_review"`, a clear `reason`, risk badges, and a
   `suggested_reply` draft — all as Busabase writes.
2. Give Kelly the AirApp URL (or local preview URL) to review the pipeline
   and the follow-up queue.
3. For a followup moved to `changes_requested`, re-draft it per the review
   comment and write it back to `needs_review`.
4. On "execute" / "send approved follow-ups": run
   `node scripts/execute_decisions.mjs --apply` to re-read approved
   followups from Busabase and mark them `done` with handoff metadata, then
   perform the actual send only through the corresponding skill (for example
   `$kelly-email`) with the approved, possibly user-edited draft, one
   follow-up at a time.
5. Never send anything for a followup without an explicit `approve` decision,
   and never re-send a followup already `done`.

## Demo Mode

`?demo=1` opens a deterministic, read-only mock CRM for documentation and
screenshots (`content/kelly-crm-app/app/js/providers/demo-provider.js`). `?demo=overview`,
`?demo=deals`, `?demo=contacts`, `?demo=followups`, and `?demo=detail` select
named mock scenes; `detail` deep-links to a deal detail. `lang=en` or
`lang=zh` forces UI chrome language. Demo mode never reads or writes
Busabase and never claims a real connection.

## Completion Criteria

Finish only when:

- the skill contains the complete canonical `content/kelly-crm-app/` project and
  `pnpm --dir content/kelly-crm-app dev` remains supported;
- all persistent config, state, decisions, and domain data use `busabase-sdk`
  and the declared resource map — no local JSON, browser storage, or
  provider choice;
- Vault values and API credentials never reach browser-visible surfaces;
- local setup offers Cloud/custom URL OAuth plus the explicit Demo path,
  while a deployed AirApp uses its ambient session;
- Overview, Deals, Contacts, Follow-ups, and Help & Settings render on
  desktop and phone widths;
- `pnpm --dir content/kelly-crm-app run check` and `node --test` pass.

## Stop Conditions

Stop before consequential Busabase mutation when the target Space is
ambiguous, the current user lacks permission, or a same-slug resource is not
application-owned. Never send, publish, or otherwise mutate an external
system directly from the AirApp.
