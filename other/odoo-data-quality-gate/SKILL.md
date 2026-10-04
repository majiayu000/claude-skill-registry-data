---
name: odoo-data-quality-gate
description: Audit an Odoo database's data quality with evidence before trusting AI answers, importing, or migrating — duplicates, missing required values, orphaned references, format anomalies — and drive remediation through odoo-mcp's gated write workflow. Use when the user asks to "check data quality", "clean up data", "prepare for migration", "find duplicates", or when aggregate answers look suspicious.
---

# Odoo data-quality gate

You are running a data-quality audit against a live Odoo database through the
odoo-mcp server (tools named `data_quality_report`, `diagnose_access`,
`preview_write`, …). Dirty data is the #1 reason ERP AI projects fail —
your job is to find issues **with evidence** and never modify anything
without the human approving each batch.

## Prerequisites

- odoo-mcp connected (any Odoo 16+; check with `health_check`).
- Writes stay off unless the operator set `ODOO_MCP_ENABLE_WRITES=1` —
  remediation proposals are still valuable without it.

## Playbook

1. **Scope with the human.** Which models matter? Default set for a general
   audit: `res.partner`, `product.template`, `account.move`. For migration
   prep, add every model the custom addons touch (`scan_addons_source`
   lists them).
2. **Run the report per model:** `data_quality_report(model=...)`. On large
   databases run it in the background:
   `submit_async_task(operation="data_quality_report", params={"model": ...})`
   then poll `get_async_task`.
3. **Read `summary.checks_with_issues` and show evidence.** Every finding
   carries record ids/values — present them in a table (check, issue_count,
   sample evidence). Never summarize away the ids; the human needs them.
4. **Verify orphans before judging.** `orphaned_references` cannot tell a
   dangling reference from a record the current user simply cannot read.
   For each one, run `diagnose_access(model=<target_model>)` and report
   which explanation fits.
5. **Propose remediation as batches, not actions.** Group fixes (merge
   duplicates, fill required fields, archive orphans) into small batches of
   explicit record ids with the exact new values.
6. **Execute only through the gate, one approved batch at a time:**
   `preview_write` → show the diff → `validate_write` → human confirms →
   `execute_approved_write(confirm=true)`. Never call `execute_method` for
   writes; it is blocked by design.
7. **Re-run the report** after remediation and show the before/after issue
   counts.

## Output format

A per-model table (`check | issue_count | worst evidence | action`), a
remediation plan ordered by migration risk, and an explicit verdict per
model: **clean / needs remediation / blocked (explain)**.

## Hard rules

- Read-only by default; every write needs a fresh approval token and the
  human's explicit confirmation for that batch.
- Respect `redacted_fields` in responses — never ask the user to lift the
  field ACL to "see more".
- If a check errored (`summary.checks_errored`), say so — do not present a
  partial audit as complete.
