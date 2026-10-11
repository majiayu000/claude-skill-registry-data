---
name: external-id-strategy
description: "Use this skill when designing, selecting, or troubleshooting external ID fields on Salesforce objects for upsert operations, cross-system record correlation, or idempotent data loads. Trigger keywords: external ID field design, upsert key strategy, cross-system record matching, source system ID mapping, composite key for uniqueness, duplicate insert on upsert, relationship resolution by external ID. NOT for data migration steps (use data-migration-planning), NOT for REST API upsert endpoint wiring (use rest-api-patterns), NOT for general data model field decisions (use data-model-design-patterns)."
category: data
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Performance
  - Operational Excellence
triggers:
  - "how do I prevent duplicate inserts when loading data from an external system"
  - "upsert is inserting new records instead of updating existing ones"
  - "how to match Salesforce records to source system records without storing Salesforce IDs"
  - "what field type should I use for an external ID to avoid case sensitivity issues"
  - "child records need to reference parents by source system key not Salesforce ID"
tags:
  - external-id
  - upsert
  - data-integration
  - idempotency
  - bulk-api
  - cross-system
  - indexing
  - composite-key
inputs:
  - "Source system object model and natural key fields used to identify records"
  - "List of Salesforce objects that need upsert support or cross-system correlation"
  - "Integration pattern in use (Bulk API 2.0, REST API, Data Loader, Apex DML upsert)"
  - "Expected data volume per object and load frequency"
  - "Whether parent-child relationships need to be resolved by external ID rather than Salesforce Id"
outputs:
  - "External ID field design recommendation per object (field type, uniqueness, case sensitivity setting)"
  - "Upsert key selection rationale and composite key formula if needed"
  - "Completed external-id-strategy-template.md documenting the per-object strategy"
  - "Checklist of indexing and uniqueness constraints to verify before go-live"
dependencies:
  - data-migration-planning
  - rest-api-patterns
  - data-model-design-patterns
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# External ID Strategy

This skill activates when a practitioner needs to design or troubleshoot how Salesforce objects carry source-system identity for upsert operations, cross-system record correlation, or idempotent integration and migration patterns. It covers external ID field type selection, uniqueness and case sensitivity semantics, indexing behavior, composite key design, parent-child relationship resolution by external ID, and the Bulk API 2.0 and REST API upsert mechanics that depend on these choices.

---

## Before Starting

Gather this context before working on anything in this domain:

- What is the source system's natural key for each target object? Is it numeric, alphanumeric, or a composite of multiple fields? Does the source system treat case as significant in its key values?
- What integration pattern will consume the external ID — REST API upsert (PATCH), Bulk API 2.0 upsert job, Apex `Database.upsert`, or Data Loader?
- How many external ID fields already exist on each target object? The platform supports up to 25 external ID fields per object (all indexed automatically). Confirm current count before adding fields.
- Are parent-child object relationships involved? If child records must reference parents by source key rather than Salesforce `Id`, the parent object must have an external ID field populated before children are loaded.
- Is the source key guaranteed unique in the source system? A non-unique external ID field will cause upsert operations to error on any row where multiple Salesforce records share the same value.

---

## Core Concepts

### What an External ID Field Is

An external ID field is a custom field on a Salesforce object marked with the `External ID` attribute in the field definition. Marking a field as External ID has two automatic platform effects:

1. **Automatic indexing** — Salesforce creates a database index on the field without a Support case. This makes upsert match lookups efficient even on large objects (millions of records).
2. **Upsert key exposure** — The field becomes available as a match key for REST API upsert (`PATCH /sobjects/{SObject}/{ExternalIdField__c}/{value}`), Bulk API 2.0 upsert jobs (the `externalIdFieldName` job parameter), Apex `Database.upsert(records, Schema.SObjectField)`, and Data Loader upsert operations.

Upsert matching behavior is deterministic:
- **0 matches** — Salesforce inserts a new record with all provided field values.
- **1 match** — Salesforce updates the matched record with the provided field values.
- **2+ matches** — Salesforce returns an error for that row or request. This is per-row in Bulk API (partial success), not a job-level abort.

This insert-or-update behavior makes upsert inherently idempotent when the external ID is unique: running the same load twice produces the same end state without creating duplicates.

### Field Type Selection and Case Sensitivity

External ID fields can be of type **Text**, **Number**, **Email**, or **Auto Number**. The choice affects uniqueness enforcement and case sensitivity:

- **Text** — Stores alphanumeric values up to 255 characters. The `Unique` checkbox enforces uniqueness; the default uniqueness behavior is **case-insensitive** (meaning `ORDER-001` and `order-001` are treated as the same value). A separate "Treat 'ABC' and 'abc' as different values (case-sensitive)" option is available during field creation. If the source system distinguishes case in key values, enable this option and normalize all input values to a consistent case in the ETL layer.
- **Number** — Stores numeric values with configurable decimal places. Case is not applicable. Use when the source key is a pure integer or numeric sequence (e.g., ERP item ID, legacy account number without alpha characters). Uniqueness is always exact numeric equality.
- **Email** — Stores email addresses with built-in format validation. Useful when the natural key for a person record is their primary email address. Uniqueness is case-insensitive (standard email semantics).
- **Auto Number** — Salesforce assigns the value automatically on record creation. An integration cannot set this value. Use when Salesforce generates a formatted sequence number (e.g., `CASE-{00001}`) that downstream systems will use as a reference key.

### Composite Key Strategy

When no single source field is globally unique across all records, a composite key must be constructed before loading. The standard approach is to concatenate two or more source fields with a stable separator and store the result in a single Text external ID field.

Design rules:
- Choose a separator that cannot appear in any component field value. Pipe (`|`) and tilde (`~`) are common choices; avoid comma (conflicts with CSV) and slash (conflicts with URL paths).
- Apply the concatenation in the integration/ETL layer before staging the data. Keep the exact formula documented in the integration spec — it must be reproduced identically on every future load.
- Validate that the combined length does not exceed 255 characters (the Text field limit).
- Treat composite key values as immutable after first insert. Changing the formula mid-integration produces orphaned records that will never match on subsequent upserts.

### Parent Relationship Resolution via External ID

When loading child records that reference a parent, it is possible to avoid a two-pass load (load parents, query back Salesforce IDs, embed IDs in child CSV) by using the parent's external ID field in a relationship reference column.

In Bulk API 2.0 CSV format, relationship resolution uses the syntax `RelationshipName__r.ExternalIdField__c` as the column header. For standard relationships:
- `Account.Legacy_CRM_Id__c` — resolves an Account lookup using the Account's external ID field
- `Account__r.Legacy_CRM_Id__c` — resolves a custom Account lookup relationship

Salesforce resolves the parent Salesforce `Id` row-by-row at ingest time using the indexed external ID field. Requirements:
- The parent object must have the external ID field populated with the correct values before children are loaded.
- The column header must use the exact relationship API name followed by `.ExternalIdField__c` syntax.
- If a parent cannot be resolved (no matching value found), the child row errors — not silently skipped.

---

## Common Patterns

### Pattern: Source System ID as External ID (Single-Object Correlation)

**When to use:** A single source system owns authoritative records for a Salesforce object type, and each source record has a stable unique identifier (e.g., ERP customer number, legacy CRM contact ID, warehouse SKU code).

**How it works:**
1. Create a custom field on the Salesforce object (e.g., `Legacy_CRM_Id__c` of type Text or Number). Mark it as External ID and Unique. For Text fields with alphanumeric source keys, decide case sensitivity based on the source system's behavior.
2. On initial load, use Bulk API 2.0 upsert (or Data Loader upsert) with this field as the external ID key. Every source record inserts as a new Salesforce record.
3. On all subsequent loads, reuse the same upsert — new source records insert, existing records update, no manual deduplication needed.
4. In downstream queries and reports, use the external ID field as a stable cross-system join key without storing Salesforce `Id` values in the source system.

**Why not use Name or another non-external-ID field:** Non-external-ID fields are not exposed as upsert keys. The upsert API rejects them as the match field. Name values are also frequently non-unique and will generate errors.

### Pattern: Multi-System Composite External ID

**When to use:** Records originate from multiple source systems, and no single field is globally unique across all sources (e.g., order numbers restart per region, account IDs repeat across acquired-company datasets).

**How it works:**
1. Define the composite key formula: `<SystemCode>|<SourceId>` (e.g., `ERP|10042`, `CRM2|A-9871`, `LEGACY|00001`).
2. Create a Text external ID field (e.g., `Source_Composite_Key__c`), marked External ID and Unique. Enable case-sensitive option if source codes can differ by case.
3. Produce the composite value in the ETL layer for every record before staging. Validate that no component field is null (null + separator + value produces an inconsistent key).
4. Load via upsert using `Source_Composite_Key__c` as the upsert key across all source systems.
5. Document the formula in the integration spec and enforce it in data quality validation.

**Why not create one external ID field per source system:** Each object supports up to 25 external ID fields, but proliferating per-source fields complicates upsert logic and wastes the indexed field budget. A single composite key field unifies the strategy and keeps the object model clean.

### Pattern: External ID-Based Relationship Resolution (Parent-Child Load)

**When to use:** Loading related objects (e.g., Account + Contact, Order + Order Line Item) where children reference parents by source system key, and a two-pass load (load parents, query IDs, embed in child file) is impractical or fragile.

**How it works:**
1. Ensure the parent object has its external ID field populated before the child load begins.
2. In the child CSV file, include a column using the relationship syntax as the header: for a standard Account lookup on Contact, use `Account.Legacy_CRM_Id__c`; for a custom lookup, use `ParentCustom__r.Legacy_CRM_Id__c`.
3. Populate the column with the parent's source system key value (not the Salesforce `Id`).
4. Submit the Bulk API 2.0 ingest job for children with the appropriate upsert key set on the child object.
5. Salesforce resolves each parent reference using the indexed external ID field at ingest time — no pre-query required.

**Why not query Salesforce IDs first:** A two-pass approach works but introduces fragility — pagination errors on large parent queries, Salesforce IDs that differ across sandboxes, and stale ID references if records are deleted and recreated. Relationship resolution via external ID is fully idempotent and sandbox-portable.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Source key is a pure integer | Number external ID field | No case-sensitivity concerns; numeric equality is unambiguous; avoids text padding issues |
| Source key is alphanumeric, source is case-insensitive | Text external ID, Unique (case-insensitive default) | Prevents duplicate variants differing only by case from being inserted |
| Source key is alphanumeric, source treats case as significant | Text external ID, Unique, case-sensitive option enabled; normalize to consistent case in ETL | Preserves case distinctions while avoiding accidental mismatches from inconsistent input casing |
| Records come from multiple source systems | Composite key in one Text external ID field (`SystemCode\|SourceId`) | Single upsert key per object; avoids per-source field proliferation |
| Child records must reference parents without knowing Salesforce IDs | Parent external ID populated first; child CSV uses `RelationshipName__r.ExternalIdField__c` syntax | Single-pass child load; idempotent and sandbox-portable |
| Source key is an email address (person record) | Email type external ID | Built-in format validation; case-insensitive uniqueness matches standard email semantics |
| No natural key exists in source system | Generate a stable UUID or hash at ETL layer before first load; store in source system | Assign once at migration time; use as external ID on all subsequent loads |
| Object already at 25 external ID fields | Consolidate using composite key pattern or remove unused external ID fields | 25 is the platform limit; exceeding it requires removing an existing external ID field |
| Need to load the same dataset into multiple sandboxes and production | Use external ID-based loads throughout; never embed Salesforce IDs in load files | Salesforce IDs differ between orgs; external IDs are portable across all org copies |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Inventory source keys** — For each Salesforce object that needs upsert support or cross-system correlation, document the source system's natural key field(s): data type, uniqueness guarantee, maximum length, and case sensitivity behavior. Flag any object where no single field is globally unique.

2. **Select field type and uniqueness settings** — Based on the key type and case sensitivity requirements, choose Text, Number, or Email. Always mark External ID and Unique when the field will serve as an upsert key. For Text fields, decide whether to enable the case-sensitive option. Confirm the current external ID field count on each object does not approach the 25-field limit.

3. **Design composite key formula if needed** — If no single source field is globally unique, define the composite formula, separator character, and maximum combined length. Validate length does not exceed 255 characters. Document the formula in the integration spec before creating the field.

4. **Create the field via Setup or metadata deployment** — Create the custom field through Setup > Object Manager, or deploy it via Salesforce DX metadata (CustomField with `externalId: true` and `unique: true`). Confirm the field appears in the object's indexed fields list after creation.

5. **Test upsert behavior end-to-end before full load** — Run a small test batch (10–100 records) through the intended upsert path. Verify: (a) first run inserts all records, (b) second run with same data updates all records and creates no duplicates, (c) introducing a row with a duplicate external ID value in the org returns an expected error, not a silent duplicate.

6. **Verify parent relationship resolution if applicable** — If child records use relationship column syntax, confirm the parent external ID field is populated, run a small child batch, and verify parent lookups are set correctly on the inserted child records.

7. **Document the strategy and commit** — Complete the external-id-strategy-template.md with field API names, types, case-sensitivity settings, composite key formulas, and integration path references. This documentation is required for integration spec audits and onboarding future maintainers.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] External ID field created with correct type (Text / Number / Email) and Unique constraint enabled
- [ ] Case-sensitivity setting on Text external ID fields matches source system behavior and ETL normalization practice
- [ ] Composite key formula (if used) is documented in the integration spec and validated against 255-character length limit
- [ ] External ID field count per object is within the 25-field platform limit
- [ ] Parent objects have external ID fields populated before child records are loaded
- [ ] Child CSV uses correct relationship column syntax (`RelationshipName__r.ExternalIdField__c`)
- [ ] Small test batch confirms insert on first run, update on second run, and error on duplicate value introduction
- [ ] External ID field API names are consistent across all integration tooling references (ETL configs, Data Loader, Apex, Flow)
- [ ] external-id-strategy-template.md completed and committed to the project integration spec

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Text external IDs enforce case-insensitive uniqueness by default** — Unless the case-sensitive option is explicitly checked at field creation, `ORDER-001` and `order-001` are treated as identical external ID values. If the source system generates keys that differ only by case for different logical records, inserting the second variant will fail with a duplicate error, even though the integration author expected two distinct records. Normalize keys to a consistent case in the ETL layer regardless of the uniqueness setting.

2. **Upsert errors on duplicate values are per-row, not per-job** — In Bulk API 2.0, if two Salesforce records already share the same external ID value (possible when the Unique constraint was not set, or was removed after records were created), any upsert attempt for that value returns an error for that specific row while other rows in the batch continue processing. The job status shows partial success. These silent partial failures are easy to miss in large loads — always inspect the job's error file after every bulk upsert run, not just the overall job status.

3. **External ID alone does not prevent duplicates — Unique is a separate checkbox** — Creating a field as External ID gives it an index and exposes it as an upsert key, but does not enforce uniqueness. The `Unique` checkbox must be checked separately. Omitting it means duplicate external ID values can be inserted through the UI, Data Import Wizard, or non-upsert DML. Once duplicates exist, any upsert on that value errors. Always set both External ID and Unique together when the field is intended as an upsert key.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| external-id-strategy-template.md (completed) | Per-object external ID field design decisions, composite key formulas, and integration path references |
| CustomField metadata XML | Deployable field definition with `externalId: true` and `unique: true` (example in templates/) |
| Integration spec section | Documents field API name, type, case-sensitivity setting, composite key formula, and the integration path that uses it for all team members |

---

## Related Skills

- data-migration-planning — Use alongside this skill when planning a full data migration; that skill covers load sequencing, error handling, and cutover mechanics that depend on external ID decisions made here
- rest-api-patterns — Covers REST API upsert endpoint mechanics; the external ID field chosen here is the key used in `PATCH /sobjects/{SObject}/{ExternalIdField__c}/{value}` calls
- data-model-design-patterns — Covers broader object and field design decisions including indexing strategy; the External ID for Integration Upsert pattern there is a summary; this skill provides the complete decision framework
- admin/data-import-and-management — Covers Data Loader and Data Import Wizard usage; external ID fields are central to upsert configuration in both tools
