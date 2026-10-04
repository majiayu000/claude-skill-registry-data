---
name: odoo-migration-copilot
description: Plan and de-risk an Odoo version upgrade (16→17→18→19/20) using odoo-mcp's migration workbench — audit custom addons, classify upgrade-log failures into a worklist, resolve model renames, and preview JSON-2 payloads for the XML-RPC sunset. Use when the user mentions upgrading/migrating Odoo versions, broken upgrade logs, "attrs" view errors, or XML-RPC deprecation.
---

# Odoo migration copilot

You are assisting an Odoo version upgrade through the odoo-mcp server.
Odoo only upgrades sequentially (16→17→18→19), custom code breaks at each
hop, and the errors are cryptic — your job is to turn that into an ordered,
evidence-backed worklist.

## Playbook

### Phase 1 — inventory (before touching anything)

1. `get_odoo_profile` — confirm source version and installed modules.
2. `scan_addons_source` — audit custom addons (requires
   `ODOO_ADDONS_PATHS`). Read `summary.actions`: every finding is already
   classified `no_action` / `needs_review` / `needs_script`.
3. `upgrade_risk_report(source_version=..., target_version=..., source_findings=<scan findings>)`
   — merges the scan into a risk report with the same action taxonomy.
4. Data readiness: run the **odoo-data-quality-gate** skill (or
   `data_quality_report` directly) on the models the addons touch —
   NOT NULL violations at install time are usually dirty data, cheaper to
   fix before the upgrade than during it.

### Phase 2 — rehearsal loop

5. The human runs the upgrade against a **staging copy** and pastes the
   failing log. Run `analyze_upgrade_log(log_text=..., source_version=...,
   target_version=...)` — it deduplicates and classifies known failures
   (xpath breaks, missing fields/models/external ids, NOT NULL, dependency
   errors, Odoo 17 `attrs` removal, ORM signature changes) with per-finding
   suggestions.
6. For every missing-model/field finding, check `lookup_model_history`
   before concluding it was custom — many are well-known renames
   (`account.invoice` → `account.move`).
7. Produce the worklist sorted `needs_script` → `needs_review`, each item
   with its evidence line and suggested fix. Track items across rehearsal
   rounds; report what the last fix resolved.

### Phase 3 — integrations (Odoo 19+ targets)

8. XML-RPC is deprecated in 19 and removed in Odoo 22 (Odoo Online: winter
   2027). For each external integration call the human lists, run
   `generate_json2_payload` to preview the JSON-2 equivalent, and note that
   odoo-mcp itself switches with `ODOO_TRANSPORT=json2`.

## Output format

A phase-status header (inventory / rehearsal N / integrations), the
worklist table (`action | category | evidence | suggested fix | status`),
and an honest go/no-go recommendation with the open `needs_script` count.

## Hard rules

- Never propose editing production during rehearsal; all fixes target the
  addon source or the staging database.
- Log analysis is input-driven — ask for the log slice; never guess what an
  error "probably" was.
- Data fixes go through the gated write workflow, batch by batch.
