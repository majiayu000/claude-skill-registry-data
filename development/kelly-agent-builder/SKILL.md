---
name: kelly-agent-builder
description: Busabase-backed App-in-Skill low-code agent configuration and governance console for a platform team. Use when the user invokes $kelly-agent-builder or /kelly-agent-builder, wants to review or edit a catalog of mock LLM agent configs, check quota usage, find configs that need attention, move a draft to live, pause a live agent, or archive an agent. Mock config/governance console only — it never provisions or calls any real agent.
metadata:
  category: platform
  tags:
    - risk:sandbox
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-agent-builder
    resources:
      - agents
      - settings
    risk: sandbox

---

# Agent Builder & Governance Console

## Overview

Kelly Agent Builder is a Busabase Cloud App-in-Skill. Its canonical product
surface is the AirApp in Busabase, not a separate local-data product. The
same Hono source supports an explicitly requested local preview with OAuth
connection bootstrap. It is a platform team's governance console for a
catalog of **mock** agent configs. It never provisions or calls a real agent —
every action reads or writes a Busabase Base record. This is a generic,
brand-free tool: teams define a name, a trigger/intent description, a set of
allowed tools (from a fixed catalog), an approval flag, and a monthly call
quota, and this console tracks status and usage and gates the risky
transition (draft → live) behind required-field validation.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, update Busabase directly and give the user the clickable AirApp
URL. Start localhost only when local preview/debugging is explicitly
requested; it uses the same Busabase resources and never offers another data
provider.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-agent-builder-app/` artifact.
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
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Agent Builder overview"></td>
    <td width="50%"><img src="assets/screenshots/catalog.webp" alt="Agent Builder catalog"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Governance summary: live agent count, aggregate quota usage, and a list of agents that need attention with reasons.</td>
    <td><strong>Catalog</strong><br>Sortable, searchable table of every agent config with status badges, owning team, and quota usage.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/agent-detail.webp" alt="Agent Builder agent detail"></td>
    <td width="50%"></td>
  </tr>
  <tr>
    <td><strong>Agent detail / edit</strong><br>Tool checklist, quota input, approval toggle, owning team field, trigger/intent textarea, status, and lifecycle actions (activate / pause / archive).</td>
    <td></td>
  </tr>
</table>

## Boundary

- This is a **mock** governance console. It never provisions, deploys, or
  calls any real agent, model, or external tool. The "allowed tools"
  checklist is a fixed local catalog (`content/kelly-agent-builder-app/app/js/tool-catalog.js`) used only
  for governance bookkeeping — selecting a tool here does not grant or invoke
  it anywhere.
- The AirApp reads and writes Busabase records only; it must not call any
  other remote system.
- No brand-specific integration exists or is implied.

## Busabase Resources

Two Bases under one application Folder (`kelly-agent-builder`), declared in
`content/kelly-agent-builder-app/app/js/config.js` and the generated template sidecars under `content/`:

- `agents`: `agent-id`, `name`, `trigger-description`, `allowed-tools` (JSON
  array), `approval-required`, `monthly-quota`, `calls-this-month`,
  `owning-team`, `status`, `created-at`, `updated-at`.
- `settings`: one row per `kind` — `kelly-agent-builder-onboarding` (presence
  marks setup complete; this skill has no external accounts or secrets to
  configure) and `kelly-agent-builder-lock`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/agent-config-schema.md`
for exact field shapes and governance rules.

## Authentication

Busabase authentication is ambient inside the deployed AirApp, which must not
show OAuth, API-key, Base URL, provider, hosting, or Space controls.
Standalone loopback preview uses browser OAuth without exposing tokens; after
OAuth it auto-selects a single/open-source Space or requires a native
selector when several Spaces are accessible.

## Demo Mode

- `?demo=1` opens a deterministic, fully offline mock catalog (8 agent
  configs spanning draft/live/paused/archived, one over-quota, one missing an
  owning team) for documentation and screenshots.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Demo mode never reads or writes Busabase.

## Governance Rules

Read `references/agent-config-schema.md` before editing the app or its
domain logic. In short:

- **Draft → live** is only allowed when `name`, `trigger_description`, at
  least one `allowed_tools` entry, non-empty `owning_team`, and
  `monthly_quota > 0` are all present. This is enforced in
  `content/kelly-agent-builder-app/app/js/providers/busabase-provider.js#activateAgent` — the browser
  form disables the button too, but the provider is the source of truth.
- **Archive** is allowed from any status. Archived agents become read-only.
- **Pause** is only allowed from `live`.
- **Needs attention** = a draft with missing required fields, OR an agent
  (any status) with no owning team, OR a quota-reached live agent
  (`calls_this_month >= monthly_quota` — reached, not strictly exceeded), OR
  `approval_required: true` with no owning team assigned.
- **Update validation**: an edit that would leave an already-`live` agent
  missing any required field (e.g. clearing `owning_team` or
  `allowed_tools`) is rejected, the same gate `activate` uses. Draft agents
  remain freely editable.

## Local App

- `content/kelly-agent-builder-app/app/index.html` + `content/kelly-agent-builder-app/app/app.js` + `content/kelly-agent-builder-app/app/styles.css` +
  `content/kelly-agent-builder-app/app/i18n/messages.js`: zero-build vanilla frontend with hash routing
  (`#/overview`, `#/catalog`, `#/agent/:id`, `#/agent/new`, `#/settings`).
- `content/kelly-agent-builder-app/app/js/agent-model.js`: pure governance rules
  (`missingRequiredFields`, `isQuotaReached`, `deriveAgent`, `summarize`,
  lifecycle transitions) shared by the busabase and demo providers.
- `content/kelly-agent-builder-app/app/js/providers/`: `busabase-provider.js` (reads/writes via
  `busabase-sdk`) and `demo-provider.js` (deterministic, read-only).
- `content/kelly-agent-builder-app/app/js/tool-catalog.js`: the fixed tool catalog (`web_search`,
  `code_exec`, `file_read`, `file_write`, `send_email`, `calendar`,
  `crm_lookup`, `db_query`, `slack_post`, `http_request`).
- `content/kelly-agent-builder-app/server.js`: thin Hono OAuth bootstrap + same-origin `/api/v1` proxy to
  Busabase — no business logic.

## Safety

- Never provision or call a real agent, tool, or external system from this
  skill's app.
- Keep `owning_team` values as free text; do not validate against a real
  directory service.

## Completion Criteria

Finish only when:

- the skill contains the complete canonical `content/kelly-agent-builder-app/` project and
  `pnpm --dir content/kelly-agent-builder-app dev` remains supported;
- all persistent config and agent data use `busabase-sdk` and the declared
  resource map — no local JSON, browser storage, or provider choice;
- local setup offers Cloud/custom URL OAuth plus the explicit Demo path,
  while a deployed AirApp uses its ambient session;
- Overview, Catalog, Agent detail, and Help & Settings render on desktop and
  phone widths;
- `pnpm --dir content/kelly-agent-builder-app run check` and `node --test` pass.
