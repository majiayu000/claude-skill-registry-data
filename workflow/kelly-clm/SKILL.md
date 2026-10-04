---
name: kelly-clm
description: Lightweight contract lifecycle management App-in-Skill (Busabase App-in-Skill) for contract inventory, lifecycle status, owners, obligations, renewal notices, and simple approval reminders. Use when the user invokes $kelly-clm or /kelly-clm, mentions CLM, contract lifecycle management, 合同管理, 合同台账, contract repository, obligation tracking, renewal reminders, notice deadlines, contract owners, signature readiness, or wants a simple UI to review contract status without doing detailed legal redlines.
metadata:
  category: legal
  tags:
    - risk:gated-write
    - industry:legal
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-clm
    resources:
      - contracts
      - obligations
      - approvals
    risk: gated-write

---

# Kelly CLM

## Overview

Kelly CLM is a Busabase Cloud App-in-Skill. Its canonical product surface is
the AirApp in Busabase, not a separate local-data product. The same Hono
source supports an explicitly requested local preview with OAuth connection
bootstrap. It is a lightweight contract lifecycle desk: contract inventory,
lifecycle stage, owner assignment, renewal/notice dates, obligations, and a
simple approval/reminder queue.

This skill is intentionally simpler than `kelly-legal-contracts`: use
`kelly-clm` for contract operations and reminders; use `kelly-legal-contracts`
when the user needs detailed legal clause review, fallback language, redline
positions, or legal issue lists.

This is a direct-manipulation control panel, not a review-then-approve
queue: creating or editing a contract, marking an obligation done,
acknowledging a renewal notice, and recording an approval decision are all
direct writes made straight through `busabase-sdk` from the browser — the
same way `kelly-lead-funnel`'s kanban stage moves and
`kelly-revshare-simulator`'s scenario CRUD work. There is no separate
decisions/handoff-log bucket; a decision writes directly onto the item's own
Busabase record. Obligations and approval reminders themselves enter
Busabase through an external process (the operator or an agent workflow
adding them directly in Busabase) — the AirApp only ever decides on them
(mark done / acknowledge / approve), it never creates them; only contracts
are created/edited through the browser.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, give the user the clickable AirApp URL. Start localhost only
when local preview/debugging is explicitly requested; it uses the same
Busabase resources and never offers another data provider. Use chat-only
mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar.

Read `references/clm-notes.md` before changing scope. The app borrows only
common CLM patterns: central repository, lifecycle status, owner assignment,
obligation tracking, renewal reminders, simple workflow approvals, and
handoff records.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-clm-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's artifact and product
contracts, stop before the unavailable Busabase operation, and report the
exact missing dependency. Do not invent a second data backend.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly CLM overview"></td>
    <td width="50%"><img src="assets/screenshots/contracts.webp" alt="Kelly CLM contract inventory"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Lifecycle dashboard with stage pipeline, upcoming renewals, and at-risk obligations.</td>
    <td><strong>Contracts</strong><br>Searchable contract inventory with owner, stage, value, and dates; create/edit directly.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/obligations.webp" alt="Kelly CLM obligations"></td>
    <td width="50%"><img src="assets/screenshots/renewals.webp" alt="Kelly CLM renewals"></td>
  </tr>
  <tr>
    <td><strong>Obligations</strong><br>Owner-assigned obligation tracker with due dates, status, and a mark-done action.</td>
    <td><strong>Renewals</strong><br>Renewal board with notice deadlines and a renewal-notice acknowledgement action.</td>
  </tr>
  <tr>
    <td colspan="2" width="100%"><img src="assets/screenshots/approvals.webp" alt="Kelly CLM approvals"></td>
  </tr>
  <tr>
    <td colspan="2"><strong>Approvals</strong><br>Approval/reminder queue for renewal notices and obligation owners, with approve / request-changes / block written directly onto the record.</td>
  </tr>
</table>

## Boundary

- This skill is an operations tracker, not legal advice.
- The app never sends emails, starts e-signature, updates a remote CLM,
  accepts terms, signs contracts, or contacts counterparties.
- The AirApp reads and writes its own Busabase Bases only; there is no
  execution/merge step beyond the direct write itself. There is no delete
  operation anywhere in this skill's UI (create/edit a contract, mark an
  obligation done, acknowledge a renewal notice, and record an approval
  decision are all create/update writes), so unlike
  `kelly-revshare-simulator`'s scenario delete, no Busabase
  review-before-merge step is ever needed here.
- Keep contract text, counterparties, prices, and notes out of committed
  files. Use demo data for screenshots.

## Busabase Resources

Three Bases under one application Folder (`kelly-clm`), declared in
`content/kelly-clm-app/app/js/config.js` and the generated template sidecars under `content/`:

- `contracts`: one row per contract — counterparty, type, lifecycle stage,
  owner, business owner, value, start/end dates, renewal date, notice
  deadline, next action, risk, and renewal-notice acknowledgement timestamp.
  Created/edited directly by the operator through the browser.
- `obligations`: one row per contract obligation/milestone — linked contract,
  title, owner, due date, status, and evidence note. Status is toggled
  directly by the operator (mark done / reopen).
- `approvals`: one row per approval/reminder handoff linked to a contract —
  title, summary, and status. The operator's decision (approve / request
  changes / block) is written directly onto this row.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space.

## Views

- `#/overview`: lifecycle pipeline, key metrics, upcoming renewals, and
  at-risk obligations.
- `#/contracts`: searchable contract inventory.
- `#/contracts/new`: new contract form (direct create).
- `#/contracts/<id>`: contract detail with dates, owners, obligations, and
  an inline edit form (direct update).
- `#/obligations`: obligation tracker by owner, due date, and status, with a
  mark-done/reopen action per row.
- `#/renewals`: renewal and notice-deadline board, with an acknowledge
  action per contract carrying a notice deadline.
- `#/approvals`: approval/reminder queue; approve / request-changes / block
  write the decision directly onto the approval record.
- `#/settings`: boundary and demo/config summary.

## Demo Mode

- `?demo=1` opens a deterministic, fully offline mock of four contracts
  (Nimbus Analytics MSA, Orbit Processor DPA, Luma Implementation SOW, Acme
  Mutual NDA), four obligations, and two approvals. It never reads or writes
  Busabase; demo create/edit/mark-done/acknowledge/decision actions only
  update the in-memory snapshot already rendered in the browser tab.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-clm-app dev` only when local preview/debugging is explicitly
requested.

## Completion Criteria

Finish only when:

- the skill contains the complete canonical `content/kelly-clm-app/` project and
  `pnpm --dir content/kelly-clm-app dev` remains supported;
- all persistent config, state, and domain data use `busabase-sdk` and the
  declared resource map — no local JSON, browser storage, or provider
  choice;
- Vault values and API credentials never reach browser-visible surfaces;
- local setup offers Cloud/custom URL OAuth plus the explicit Demo path,
  while a deployed AirApp uses its ambient session;
- Overview, Contracts, Obligations, Renewals, Approvals, and Help & Settings
  render on desktop and phone widths;
- `pnpm --dir content/kelly-clm-app run check` and `node --test` pass.

## Stop Conditions

Stop before consequential Busabase mutation when the target Space is
ambiguous, the current user lacks permission, or a same-slug resource is not
application-owned. Never perform e-signature, counterparty contact, or any
other external side effect from the AirApp.
