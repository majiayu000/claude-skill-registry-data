---
name: Odoo
slug: odoo
version: 1.0.0
description: Operate Odoo across CRM, sales, inventory, purchasing, and accounting with module-aware planning, read-before-write checks, and safe execution.
homepage: https://clawic.com/skills/odoo
changelog: Turns generic Odoo help into a module-aware workflow for safer reporting, imports, integrations, and business operations.
metadata:
  clawdbot:
    emoji: 🏢
    requires:
      bins: []
    os:
    - linux
    - darwin
    - win32
    configPaths:
    - ~/Clawic/data/odoo/
    displayName: Odoo
  openclaw:
    requires:
      config:
      - ~/Clawic/data/odoo/
---

# Odoo

Odoo operating workflow for live ERP systems. Use this when the agent must inspect, report on, reconcile, import, configure, or safely change data in Odoo Online, Odoo.sh, or self-hosted environments.

## When to Use

Use when the task clearly belongs to Odoo: CRM, quotations, sales orders, invoices, stock moves, purchase orders, manufacturing, projects, subscriptions, or accounting. Best fit when the user needs help across modules, environments, and hosting surfaces instead of only one narrow report or one raw API call.

Use this skill to turn vague business asks into safe, module-aware actions: identify the right records, choose the right interface, preview impact, and only then write or automate.

## Architecture

Memory lives in `~/Clawic/data/odoo/`. If `~/Clawic/data/odoo/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/Clawic/data/odoo/
├── memory.md     # companies, modules, approval boundaries, and stable preferences
├── instances.md  # instance URLs, environments, versions, and auth lanes
├── modules.md    # custom modules, renamed fields, and local conventions
└── incidents.md  # failed imports, access issues, broken automations, and recoveries
```

## Quick Reference

Use the smallest matching file instead of mentally loading the whole ERP every time.

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Hosting surface map | `surfaces.md` |
| Operating lanes by module | `operations.md` |
| Real request translations | `examples.md` |
| Safe writes and approval ladder | `safety.md` |
| Reporting and KPI scoping | `reporting.md` |
| API, imports, and automation choices | `integrations.md` |
| Common Odoo models and objects | `models.md` |
| Broken flow and access triage | `triage.md` |

## Requirements

- No credentials are required to install this skill.
- Runtime access depends on the Odoo instance, credentials, and tools the user already has.
- Detect the hosting surface early: Odoo Online, Odoo.sh, or self-hosted changes what is possible and what is safe.
- Prefer read-only review first, then the smallest write path that matches the job.
- Treat custom modules, record rules, fiscal locks, and warehouse operations as part of the system design, not annoying exceptions.
- Require explicit user confirmation before destructive writes, mass updates, imports that overwrite data, or changes to posted accounting and completed stock records.

## Core Rules

### 1. Identify the Lane Before Touching Records
- Classify the task first: report, operational write, configuration, import, reconciliation, integration, or upgrade triage.
- The lane and hosting surface change the safe interface, the validation steps, and who needs to confirm.
- If the lane is unclear, stay in discovery mode until the intent is explicit.

### 2. Resolve Module, Model, and Business Object Precisely
- Name the module and underlying model before proposing fields, filters, or automations.
- Similar nouns hide different records: lead vs opportunity, quotation vs sales order, product template vs product variant, invoice vs journal entry.
- If custom modules or renamed fields may exist, verify them before pretending the default schema applies.

### 3. Preview Before Any Write
- Preview with domains, sample rows, counts, target fields, and side effects before a write or import.
- For bulk work, explain the selection logic, duplicate risk, and rollback path first.
- Never move from natural-language intent straight to `create`, `write`, `unlink`, or import.

### 4. Respect Finality in Accounting, Inventory, and Procurement
- Posted journal entries, tax locks, stock valuation, landed costs, receipts, and vendor bills have downstream consequences.
- Prefer reversal, cancellation, compensating entry, or corrective follow-up over direct edits to finalized business documents.
- If the user asks for a shortcut that breaks auditability, say so plainly and propose the compliant path.

### 5. Choose the Lowest-Risk Interface
- Use the Odoo UI for one-off review and simple operational flows.
- Use CSV import for structured bulk changes with reviewable input.
- Use XML-RPC or JSON-RPC only when automation, repeatability, or cross-system orchestration justifies it.
- Do not recommend direct database writes unless the user is doing controlled backend repair and fully understands the blast radius.

### 6. Scope Business Context Before Giving Numbers
- Confirm company, timezone, currency, warehouses, fiscal period, and status filters before reporting.
- Odoo metrics are easy to misstate because draft, canceled, backordered, and multi-company data often coexist.
- If a dashboard answer depends on accounting policy or custom states, surface that dependency instead of hiding it.

## Quick Start

1. Detect the lane: reporting, operational change, import, config, or integration.
2. Identify the Odoo surface: hosting model, modules involved, environment, version if known, and any customizations.
3. Open the matching file:
   - `surfaces.md` for Odoo Online, Odoo.sh, or self-hosted constraints
   - `operations.md` for day-to-day business flows
   - `examples.md` for fast translation from user request to lane and safe first move
   - `reporting.md` for KPIs and reconciliation
   - `safety.md` for risky writes, corrections, and approvals
   - `integrations.md` for API, import/export, and automation design
   - `triage.md` for access, module, and workflow failures
4. Explain the impact before suggesting an operation that changes records or business state.

## Default Moves

Use these defaults when the request is underspecified or when multiple Odoo paths are possible. They are not shortcuts; they are the safest first move for each common situation.

| Situation | First move | Why |
|----------|------------|-----|
| Vague business request | Translate it into module, model, state, and output format | Prevents acting on the wrong object |
| Unknown hosting model | Classify as Odoo Online, Odoo.sh, or self-hosted before suggesting tools | UI, shell, logs, and API access differ sharply |
| Bulk update | Preview affected records, duplicates, required keys, and rollback plan | Imports and mass writes are easy to misapply |
| Reporting request | Lock company, period, timezone, status filters, and measures | Odoo numbers drift fast without scope |
| Automation request | Decide between server action, scheduled action, import, or external API | The cheapest automation is often already inside Odoo |
| Access error | Check groups, record rules, company scope, and environment first | Most "broken" actions are permissions or context |
| Broken inventory/accounting flow | Preserve traceability, then fix upstream document or post reversal | Direct edits often make audits worse |

## Common Traps

- Treating every request as CRUD when the real task is business process correction
- Mixing draft and posted documents in the same report without saying so
- Writing against `product.template` when the workflow actually needs variants on `product.product`
- Importing records without stable external IDs, natural keys, or duplicate handling
- Editing completed stock or posted accounting moves directly instead of using corrective flows
- Mixing advice for Odoo Online, Odoo.sh, and self-hosted as if all three exposed the same tools
- Assuming standard Odoo fields when the instance has custom modules, studio fields, or renamed states
- Recommending database surgery before exhausting safer UI, import, or API paths

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://<odoo-host>/web` | browser session data chosen by the user | interactive review and manual operations |
| `https://<odoo-host>/xmlrpc/2/common` | database name, username, password | authenticate and resolve user id |
| `https://<odoo-host>/xmlrpc/2/object` | model names, domains, field names, record payloads | read and write records via XML-RPC |
| `https://<odoo-host>/jsonrpc` | JSON-RPC payloads for auth or model calls | scripted integrations when JSON-RPC is available |
| user-chosen export target | report data explicitly requested by the user | deliver CSV, Excel, PDF, or downstream sync |

No other external endpoints should be used unless the user asks for a specific connected system.

## Security & Privacy

**Data that stays local:**
- environment notes in `~/Clawic/data/odoo/`
- known modules, company rules, and approval boundaries the user wants remembered
- reusable operating decisions such as preferred import format or reporting defaults

**Data that may touch external systems:**
- only the Odoo instance and export targets already involved in the user's task

**This skill does NOT:**
- bypass approvals for destructive writes or sensitive financial corrections
- store passwords, tokens, session cookies, or raw export payloads in memory
- assume a production write path when a safer review path exists
- make undeclared network requests by itself

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/<slug> (install if the user confirms):
- `crm` — customer pipeline workflows when the work is mainly around leads, deals, and sales motion
- `inventory` — stock-focused operating guidance when warehouse flows become the main problem
- `accounting` — accounting-first workflows for journals, reconciliation, close, and financial controls
- `powerpoint` — executive summaries and deck outputs from Odoo reporting work
- `word` — polished SOPs, proposals, and customer-facing documents built from Odoo context

## Feedback

- If useful, star it: https://clawic.com/skills/odoo
- Latest version: https://clawic.com/skills/odoo
