---
name: npsp-custom-rollups
description: "Use this skill when configuring, troubleshooting, or extending NPSP Customizable Rollups (CRLP) — including rollup definitions, filter groups, batch job modes, and the one-way migration from legacy NPSP rollups. Trigger keywords: CRLP, customizable rollups, rollup definition, filter group, rollup batch job, NPSP gift totals, NPSP recalculate rollups. NOT for standard Salesforce roll-up summary fields, Nonprofit Cloud (NPC) native aggregation, or Rollup Helper third-party solutions."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Operational Excellence
  - Performance
triggers:
  - "NPSP rollup fields are not updating after new gifts are entered"
  - "How do I configure customizable rollups or filter groups in NPSP?"
  - "CRLP batch job is showing stale totals on Contact or Account records"
  - "We need to enable CRLP — what will break if we do that?"
  - "Rollup definition not calculating correctly for fiscal year gifts"
tags:
  - npsp
  - crlp
  - customizable-rollups
  - filter-groups
  - batch-jobs
  - nonprofit
inputs:
  - "NPSP version installed in the org (verify under Installed Packages)"
  - "Whether CRLP has already been enabled (one-way migration — cannot revert)"
  - "List of rollup fields that must be populated (e.g., Total Gifts, Last Gift Date, Number of Gifts)"
  - "Existing formula fields or automations that read NPSP rollup summary fields"
  - "Business rules for time-based filtering (fiscal year vs. calendar year, membership windows)"
outputs:
  - "Rollup Definition configuration checklist (object, field, operation, date range, filter group)"
  - "Filter Group design with field-level filter criteria and name length verified"
  - "Batch job schedule recommendation (Incremental vs. Full vs. Scheduled)"
  - "Pre-migration impact assessment for legacy rollup fields"
  - "Rollup recalculation runbook"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-11
---

# NPSP Custom Rollups (CRLP)

This skill activates when a practitioner needs to configure, repair, or extend NPSP Customizable Rollups (CRLP). It covers rollup definition setup, filter group design, batch job modes, and the irreversible migration from legacy NPSP rollups.

---

## Before Starting

Gather this context before working on anything in this domain:

- **CRLP enabled status:** Open NPSP Settings > Customizable Rollups and confirm whether CRLP is already enabled. Enabling CRLP is a one-way migration — it removes all user-defined legacy NPSP rollup configurations permanently with no rollback path.
- **Legacy rollup dependencies:** Audit formula fields, validation rules, flows, and Apex that read NPSP rollup summary fields (e.g., `npo02__TotalOppAmount__c`, `npo02__LastCloseDate__c`). These fields continue to exist after migration but will only populate if equivalent CRLP rollup definitions are created.
- **NPSP managed package version:** CRLP was introduced in NPSP 3.112. Verify the installed version under Setup > Installed Packages before referencing features from recent releases.

---

## Core Concepts

### Rollup Definitions

A Rollup Definition is a custom metadata record (type: `Customizable_Rollup__mdt`) that describes a single aggregation operation. Each definition specifies:

- **Summary Object** — the parent record that receives the rollup value (Contact, Account, or Opportunity for hard credits; also supports GAU Allocations and Partial Soft Credits).
- **Detail Object** — the child records being rolled up (Opportunity, Payment, or related objects).
- **Field to Aggregate** — the field on the detail object used for the calculation.
- **Field to Store** — the target field on the summary object where the result is written.
- **Aggregate Operation** — Sum, Count, Largest, Smallest, Average, First, Last, Days Ago, or Years Ago.
- **Amount/Date Field** and **Fiscal vs. Calendar Year** — controls how time-based filters are applied.

CRLP ships with a set of default Rollup Definitions that replicate the standard NPSP rollup fields. Practitioners can clone these defaults or create entirely new definitions for custom fields.

### Filter Groups

A Filter Group is a named set of field-level criteria that can be attached to one or more Rollup Definitions. For example, a "Major Gift" filter group might restrict the rollup to Opportunities with `Amount >= 10000`. Rules:

- Filter group names are limited to **40 characters**. Names that exceed this limit cause a save error that is not clearly surfaced in the UI.
- A single filter group can include multiple filter rows combined with AND/OR logic.
- Large filter groups (many rows) can cause the NPSP Settings page to time out on save. Deploy via Metadata API for complex configurations.
- Filter groups are referenced by Rollup Definitions — one filter group can be shared across many rollup definitions, which keeps configuration DRY.

### Batch Job Modes

CRLP rollups are **not real-time**. They require a batch job to recalculate values on summary records. NPSP provides three modes, accessible under NPSP Settings > Batch Processing:

| Mode | Behavior | When to Use |
|---|---|---|
| **Incremental** | Recalculates only records flagged as needing update (dirty records) | Default scheduled run; low overhead for active orgs |
| **Full** | Recalculates all summary records regardless of dirty flag | After bulk data loads, rollup definition changes, or suspected stale data |
| **Scheduled** | Runs the Full recalculation on a user-defined schedule | Nightly or weekly maintenance window |

The dirty flag is set automatically when a related Opportunity is inserted, updated, or deleted. Bulk data loads via Data Loader or Bulk API may bypass the dirty flag mechanism — always run a Full recalculation after any significant data import.

### One-Way CRLP Migration

Enabling CRLP removes all user-defined legacy NPSP rollup configurations. The platform does not warn about downstream formula fields or automations that read those rollup fields. Before enabling:

1. Export the current list of legacy rollup fields from the NPSP Rollups tab.
2. Identify every formula field, validation rule, flow, and Apex class that reads those fields.
3. Create equivalent CRLP Rollup Definitions before enabling CRLP, or document the gap explicitly.
4. After enabling CRLP, run a Full recalculation batch immediately to populate values.

---

## Common Patterns

### Pattern: Custom Gift Rollup With Date Range Filter Group

**When to use:** The org tracks a specific giving window (fiscal year, membership year, or campaign period) and needs a rollup that totals only gifts within that window.

**How it works:**
1. Create a Filter Group named after the window — keep the name to 40 characters or fewer (e.g., "FY25 Unrestricted Gifts" is fine; "Current Fiscal Year Unrestricted Gifts Only" is too long at 43 characters).
2. Add filter rows: `CloseDate >= [start date]` and `CloseDate <= [end date]`. NPSP supports relative date tokens for rolling windows.
3. Create a Rollup Definition: Summary Object = Contact, Aggregate Operation = Sum, Amount Field = Amount, Store Field = a custom currency field on Contact, and attach the filter group.
4. Run a Full recalculation batch to populate all historical values.
5. Schedule Incremental recalculation nightly to keep current data fresh.

**Why not the alternative:** Standard Salesforce roll-up summary fields do not support cross-object date-relative filters without additional formulas, and they do not work across lookup relationships — only master-detail.

### Pattern: Sandbox-to-Production Deployment of CRLP Configuration

**When to use:** CRLP configuration is being built in a sandbox and the org needs a reliable, reviewable deployment path to production.

**How it works:**
1. Build and test all Rollup Definitions and Filter Groups in the sandbox NPSP Settings UI.
2. Verify values on spot-checked Contact and Account records match expected figures after a Full recalculation batch.
3. Export definitions as custom metadata records using the Metadata API (type: `CustomMetadata`).
4. Deploy using a change set or SFDX deployment package. CRLP definitions are custom metadata and deploy cleanly through standard tooling.
5. After deploying to production, run a Full recalculation immediately — production values will be stale until the batch completes.
6. Monitor the batch job logs under NPSP Settings > Batch Processing for errors or partial failures.

**Why not the alternative:** Manually recreating rollup definitions in production is error-prone, cannot be peer-reviewed as code, and introduces version drift between environments.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| CRLP not yet enabled; legacy rollups active | Audit all dependencies first, then enable CRLP | Migration is one-way and silently breaks downstream formula fields |
| Rollup values are stale after a bulk data load | Run Full recalculation batch | Incremental only processes dirty-flagged records; bulk loads may bypass the dirty flag |
| New rollup definition created; values not populating | Run Full recalculation, verify batch completed without errors | Definitions do not self-populate; a batch run is always required |
| Filter group name exceeds 40 characters | Shorten the name before saving | The 40-char limit is not enforced visually until submit, causing confusing save errors |
| Rollup needed for Partial Soft Credit amounts | Use the Partial Soft Credit rollup definition type | Standard CRLP does not roll up PSC amounts automatically; a separate definition type is required |
| Large filter group times out on NPSP Settings save | Deploy via Metadata API instead of the UI | The NPSP Settings page has a browser timeout limit that complex filter groups exceed |

---

## Recommended Workflow

1. **Audit the current state** — check whether CRLP is already enabled (NPSP Settings > Customizable Rollups). If not enabled, export legacy rollup fields and identify all formula fields, flows, Apex, and validations that read them before proceeding.
2. **Design rollup definitions and filter groups** — draft each rollup in a planning document: summary object, detail object, aggregate operation, amount/date field, date range type (calendar vs. fiscal), store field, and any filter criteria. Verify filter group names are 40 characters or fewer.
3. **Build and validate in sandbox** — create Rollup Definitions and Filter Groups in the sandbox NPSP Settings UI. Run a Full recalculation batch and compare output values to expected figures on representative test records.
4. **Deploy to production via Metadata API** — export custom metadata records and deploy with a change set or SFDX deployment package. Never recreate manually in production.
5. **Enable CRLP in production if not already enabled** — only after all dependent formula fields and automations have been verified or updated. Enabling is irreversible.
6. **Run Full recalculation and verify** — trigger Full recalculation immediately after any major configuration change or data load. Monitor under NPSP Settings > Batch Processing until the job completes successfully.
7. **Schedule ongoing recalculation** — set up a Scheduled Full recalculation for nightly or weekly maintenance. Use Incremental recalculation for higher-frequency intraday syncs if the org has high transaction volume.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] All Rollup Definitions have Summary Object, Detail Object, Aggregate Operation, Amount/Date Field, and Store Field populated
- [ ] Filter group names are 40 characters or fewer
- [ ] A Full recalculation batch has been run and completed without errors
- [ ] Formula fields and automations that read legacy rollup fields have been audited and updated if necessary
- [ ] Rollup values on spot-checked Contact and Account records match expected figures
- [ ] Rollup Definitions are deployed via Metadata API (not manually recreated in production)
- [ ] Scheduled batch job is configured for ongoing recalculation

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Enabling CRLP permanently removes legacy rollup configurations** — There is no undo. User-defined legacy rollup overrides are deleted, and no warning is shown about dependent formula fields or flows that read those fields. Always perform a full dependency audit before enabling.
2. **CRLP values are not real-time** — A newly created opportunity will not update Contact or Account rollup fields until the next batch run. Any process that expects rollup fields to be current immediately after an opportunity save will read stale data.
3. **Filter group names have a 40-character hard limit** — The UI does not clearly enforce this constraint before submission. A name over 40 characters either silently truncates or returns a generic error. Always count characters before saving.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Rollup Definition configuration checklist | Table listing each rollup: summary object, detail object, operation, amount/date field, store field, filter group, and fiscal vs. calendar setting |
| Filter Group design | Named filter groups with each row's field, operator, and value; names verified under 40 characters |
| Batch job schedule recommendation | Job mode (Incremental / Full / Scheduled) with run frequency and monitoring guidance |
| Pre-migration impact assessment | List of legacy rollup fields, their dependent formula fields / flows / Apex, and migration readiness status |
| Rollup recalculation runbook | Step-by-step instructions for triggering and monitoring a Full recalculation batch |

---

## Related Skills

- npsp-vs-nonprofit-cloud-decision — use when evaluating whether to stay on NPSP or migrate to NPC; CRLP definitions do not migrate to NPC automatically
- npsp-program-management — use when aggregating Program Management Module data; CRLP is not the correct tool for PMM service delivery aggregation
