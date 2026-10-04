---
name: anysite-crm-setup
description: Connect and configure the user's CRM (HubSpot or Pipedrive) for safe AI-driven enrichment through anysite MCP crm_* tools. Runs a short discovery - reads the CRM schema including custom properties, agrees a deterministic field mapping with the user in 3-5 questions, and saves a local CRM profile that all future enrichment sessions follow. Use when the user wants to connect their CRM, set up CRM enrichment, configure field mapping, re-run CRM discovery after schema changes, or asks why CRM writes are skipped. Also defines the mandatory rules every agent must follow when writing to CRM with crm_upsert_contacts / crm_upsert_companies.
---

# Anysite CRM Setup

Connect the user's CRM and produce a **local CRM profile** — a saved field mapping that makes every
future enrichment write deterministic: the same data always lands in the same CRM properties.

## When to use

- First-time setup: "connect my HubSpot", "connect my Pipedrive", "set up CRM enrichment"
- Re-discovery: CRM schema changed, mapping feels stale, or writes are being skipped unexpectedly
- Reference: the **Writing rules** section below applies to EVERY session that calls
  `crm_upsert_contacts` / `crm_upsert_companies`, even outside setup

## Prerequisites

The `crm_*` tools are visible only when the user has enabled CRM integration in their Anysite
dashboard (Profile → CRM Integration). If the tools are missing, ask the user to enable it there.
After they enable it, the tools do NOT appear instantly: the server flag takes up to a minute to
propagate, and the agent's tool list is cached per session — ask the user to reconnect the MCP
server (or start a new session), then retry. This is expected behavior, not an error.

## Setup flow

### 1. Ensure a connection

Call `crm_list_connections`.

- If there is an active connection — proceed to step 2.
- If not, ask which CRM the user wants (HubSpot or Pipedrive) if not obvious, then call
  `crm_connect(provider="hubspot")` or `crm_connect(provider="pipedrive")`, give the user the
  `connect_url` to open in a browser, then poll `crm_connect_status(pending_id)` every few seconds
  until `active`.
- Only ONE CRM can be connected at a time. If `crm_connect` returns a conflict, the user must
  disconnect the current CRM in the dashboard first — never disconnect for them without asking.

### 2. Read the schema

Call `crm_get_schema()`. You get:

- `properties.contacts` / `properties.companies` — every property with `label`, `type`,
  `options` (valid enum values), `read_only`, `custom`
- `lists` — the user's CRM lists (id, name, processing type)
- `protected_properties` — fields the server will never let you write

### 3. Classify and auto-map

Silently classify properties:

- **Standard equivalents** — map automatically, do not ask. HubSpot: `email→email`, `jobtitle`,
  `firstname`/`lastname`, `phone`, `city`, `country`, `company`, `website`, `domain`, `industry`,
  `numberofemployees`, `linkedin_url→hs_linkedin_url`. Pipedrive: `email→email`, `name`,
  `job_title`, `phone`, plus the `domain` alias on companies (backed by a custom Domain field the
  server manages automatically).
- **Custom enrichment targets** — custom properties whose name/label suggests enrichment
  (score, tier, segment, tech stack, intent, source): candidates for user questions. Pipedrive
  custom properties have hash-like names — rely on `label` to understand them.
- **Ignore** — `read_only: true`, calculated, `hs_*` system internals, protected fields.

Provider differences that change agent behavior:

- **Pipedrive matches contacts by email or record_id only** — `linkedin_url` matching is
  HubSpot-only. Records with only a linkedin_url will not match existing Pipedrive persons.
- **Pipedrive companies match by the `domain` alias** — the server maps it to the portal's
  Domain field. If company writes fail with a "no domain field" error, reconnect the CRM with
  admin access so the server can create the field.
- **Enum values are labels in both CRMs** — the server converts labels to Pipedrive option ids
  internally; always send the human-readable label from the schema options.

### 4. Ask 3-5 questions maximum

Ask ONLY about ambiguous or high-stakes decisions, one compact block, not an interview:

- Ambiguous targets: "Intent score → `Lead Score` or `ICP Fit Score`?"
- Overwrite policy for volatile fields: "Job titles: overwrite on change or fill blanks only?"
- Working list: "Which list do you enrich most — 'Inbound' or 'Outbound Q3'?" (only if lists exist)
- Creation policy: "May agents create new contacts, or update existing only?"
- Plan: "Are you on MCP Unlimited or a credit-based plan?" — future sessions use this to
  decide between credit estimates (credit plans) and time estimates (Unlimited) before bulk runs.
  Skip it when `anysite-gtm-profile` already records the plan.

Confirm the full mapping as ONE list for approval, then save.

### 5. Save the local profile

Write the agreed profile to `~/.claude/skills/anysite-crm-profile/SKILL.md` in Claude Code or
`~/.codex/skills/anysite-crm-profile/SKILL.md` in Codex (create the directory). Without file
access, give it as a block to paste into project or custom instructions. Use exactly this
structure:

```markdown
---
name: anysite-crm-profile
description: The user's saved CRM field mapping and write rules for CRM enrichment via anysite MCP. ALWAYS consult this before calling crm_upsert_contacts or crm_upsert_companies - it defines which CRM properties to write, which may be overwritten, and which list is the working list. Generated by /anysite-crm-setup - do not edit manually, re-run setup to change.
---

# CRM Profile (<provider> portal <portal_id>, connection <connection_id>)

Generated <date> by anysite-crm-setup from live schema. Do not edit manually.

## Field mapping — contacts
| Anysite data | CRM property | mode |
|---|---|---|
| job title | jobtitle | fill_blank |
| linkedin url | hs_linkedin_url | fill_blank |
| intent score | icp_fit_score | overwrite |

## Field mapping — companies
| Anysite data | CRM property | mode |
|---|---|---|
| industry | industry | fill_blank |
| employee count | numberofemployees | overwrite |

## Rules
- Working list: "<name>" (id <id>)
- allow_create: <true/false, as agreed>
- Never write (user protected, on top of server-enforced): <list or "-">
- Enum properties and their valid values: <property>: <values>
- MCP plan: <unlimited | credits>; bulk-run policy: <credit estimates | time estimates>
- crunchbase aliases cache: <name → alias, append as resolved — saves ~20cr/account/sweep>
```

Only include rows that were actually agreed or auto-mapped. Never invent mappings for data types
that were not discussed.

## Writing rules (every session, not only setup)

1. **Consult the profile first.** If the `anysite-crm-profile` exists (as a skill file or in the
   conversation's instructions), its
   mapping is law: write ONLY to properties listed there, in the listed mode. If a new data type
   has no mapping, ask the user once and suggest re-running setup — do not guess.
2. **Creating a new contact requires email.** record_id and linkedin_url only MATCH existing
   contacts; a record without email is skipped with `create_requires_email` when no match exists.
   Never invent or guess emails — if no verified work email is available, report the person as
   not imported and say why.
3. **No profile? Minimal safety.** Map only obvious standard properties; ask before writing
   anything to a custom property; recommend running `/anysite-crm-setup`.
4. **Dry-run before bulk.** For more than ~10 records, or any `overwrite_properties`, first call
   the upsert with `dry_run=true`, show the user the old → new diff, and write only after
   confirmation.
5. **Overwrite only per profile.** Pass a property in `overwrite_properties` only if the profile
   marks it `overwrite` (or the user explicitly asked in this session).
6. **Enum values must come from the schema.** Check `options` before writing enum properties;
   the server skips invalid values with an `enum_option_missing` warning — do not retry blindly.
   When sources disagree on an enum like industry (e.g. YC vertical vs LinkedIn category), pick the
   schema option closest to how the company describes itself and mention the choice to the user.
   Use `crm_get_schema(object_type=..., properties=[...])` to fetch just the enum you need — the
   unfiltered schema is very large.
7. **Report warnings honestly.** `fill_blank_skip` means the field already had a value — that is
   the policy working, not an error. Summarize results/skipped/warnings for the user after writes.
8. **Undo exists.** Every real write returns `run_id`. If the user is unhappy with a write,
   `crm_undo(run_id)` restores previous values (fields changed since are reported as conflicts).

## Tools reference

| Tool | Purpose |
|---|---|
| `crm_list_connections` | Connections and their status |
| `crm_connect` / `crm_connect_status` | OAuth connect flow |
| `crm_get_schema` | Properties (with enum options), lists, protected fields |
| `crm_query_records` | Read CRM: list members, by ids/emails, free-text search, paging |
| `crm_upsert_contacts` | Write contacts (match by email / record_id / linkedin_url) |
| `crm_upsert_companies` | Write companies (match by domain) |
| `crm_undo` | Revert a write run by run_id |

Property values are strings; numbers and booleans are accepted and coerced server-side.

Server-enforced regardless of anything in this skill: fill-blank by default, protected fields,
no empty writes, create only with `allow_create`, full write log.
