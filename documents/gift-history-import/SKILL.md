---
name: gift-history-import
description: "Use when migrating donation or gift history into Salesforce NPSP using the NPSP Data Importer (BDI) — covers DataImport__c staging, payment mapping, soft credit creation via Opportunity Contact Roles, GAU allocation, and campaign attribution. NOT for standard Opportunity import via Data Loader, NPC gift records, or recurring donation setup."
category: data
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Reliability
triggers:
  - "How do I import historical donation records into NPSP with soft credits and GAU allocations?"
  - "Gifts are missing OCRs and payment records after Data Loader import to Opportunity in NPSP"
  - "How to use NPSP Data Importer for bulk gift history migration with campaign attribution"
  - "Custom payment fields not mapping when importing gifts using NPSP BDI"
  - "GAU allocations missing after bulk gift import into NPSP"
tags:
  - gift-import
  - npsp
  - BDI
  - DataImport__c
  - soft-credits
  - GAU-allocation
inputs:
  - "Source gift data: amount, close date, donor contact/account, payment method, campaign, GAU split"
  - "NPSP Advanced Mapping configuration status (required for custom payment and GAU fields)"
  - "Volume of records per batch (max 50,000 per file, 100 MB max)"
outputs:
  - "DataImport__c staging record CSV specification"
  - "BDI field mapping documentation for payment, OCR, GAU, and campaign fields"
  - "Import validation checklist and post-import verification queries"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-16
---

# Gift History Import

This skill activates when a practitioner needs to migrate historical donation or gift records into a Salesforce NPSP org in a way that creates the full NPSP gift data structure: Opportunity, OppPayment records, Opportunity Contact Roles (soft credits), GAU Allocations, and Campaign Members in a single coordinated pass.

---

## Before Starting

Gather this context before working on anything in this domain:

- NPSP gift history must be imported through the NPSP Data Importer (Batch Data Import / BDI), not through direct Data Loader inserts to the Opportunity object. Direct Opportunity inserts bypass all BDI automation, leaving OCRs, GAU allocations, payment records, and household rollups missing.
- Confirm whether NPSP Advanced Mapping is enabled (Setup > NPSP Settings > Data Import > Advanced Mapping). Without it, custom payment fields and custom GAU allocation fields will silently go unmapped even if they appear in the CSV.
- The staging object is `npsp__DataImport__c` (abbreviated as DataImport__c in community docs). Each row in this object represents one gift transaction and can drive creation of multiple related records.
- File limits: 50,000 records per batch file, 100 MB maximum file size per upload.

---

## Core Concepts

### The DataImport__c Staging Object (BDI)

The NPSP Data Importer uses `npsp__DataImport__c` as a staging table. Each row in DataImport__c maps:
- **Contact1** and/or **Contact2** — donor and secondary donor (household member)
- **Account1** — organizational donor (for org gifts)
- **Home Address** — address fields that flow to Contact's mailing address
- **Opportunity** fields — Amount, Close Date, Stage, Record Type, Campaign
- **Payment** fields — Payment Method, Check/Reference Number, Paid Date
- **Soft Credit** fields — Contact2 becomes a soft credit OCR automatically with the correct Role
- **GAU Allocation** fields — up to 5 GAU splits per row using numbered field sets (GAU_Allocation_1__c through GAU_Allocation_5__c)

After staging rows are inserted, the BDI batch process creates all related records in a coordinated transaction that respects NPSP trigger logic.

### Opportunity Contact Roles (Soft Credits)

Soft credits in NPSP are created as Opportunity Contact Roles (OCRs) on the Opportunity. The BDI creates OCRs automatically from the Contact2 fields on DataImport__c. If you import Opportunities directly via Data Loader without staging through DataImport__c, no OCRs are created — the soft credit is permanently missing from the gift record unless manually added.

The NPSP OCR Role picklist values are managed by NPSP: `Soft Credit`, `Household Member`, `Matched Donor`. Verify the correct role value before staging.

### GAU Allocations

General Accounting Unit (GAU) Allocations are the mechanism for splitting a gift across multiple funds or programs. Each BDI row supports up to 5 GAU allocation records using numbered field pairs:
- `npsp__GAU_Allocation_1_GAU__c` — lookup to the GAU record (by name or ID)
- `npsp__GAU_Allocation_1_Amount__c` or `npsp__GAU_Allocation_1_Percent__c` — split amount or percentage

GAU Allocation fields beyond the standard 5 require custom field mapping via Advanced Mapping. Without Advanced Mapping enabled, these fields are silently ignored even if populated in the CSV.

### Advanced Mapping Requirement

Advanced Mapping is a toggle in NPSP Settings that enables custom field mapping between DataImport__c source fields and target object fields. Without it:
- Custom payment fields (e.g., a custom `Check_Memo__c` field on Payment) will not map
- Custom GAU allocation fields will not map
- Only standard NPSP-shipped field mappings are active

After enabling Advanced Mapping, field maps must be explicitly configured in NPSP Settings > Data Import > Field Mappings before they take effect on the next BDI run.

---

## Common Patterns

### Pattern 1: Standard Gift Migration with Soft Credits and GAU Splits

**When to use:** Migrating 5,000–50,000 historical gifts with donor, payment, soft credit, and fund allocation data from a legacy system.

**How it works:**
1. Prepare CSV with DataImport__c staging columns: Contact1 matching fields, Opportunity fields, Payment fields, Contact2 (soft credit) fields, and GAU allocation field pairs
2. Insert rows to DataImport__c via Data Loader (use the NPSP Batch Data Import API name)
3. Navigate to NPSP Data Importer in App Launcher and run the batch
4. Monitor batch results — each staging row shows success or failure status with error details
5. Run SOQL validation queries to confirm OCRs, GAU Allocations, and payment records were created

**Why not Data Loader directly to Opportunity:** Direct Opportunity inserts bypass the BDI Apex batch. NPSP rollup triggers, payment record creation, GAU allocation logic, and household rollup updates all depend on BDI processing. Bypassing BDI creates orphaned Opportunities with no payment records, no OCRs, and stale household rollup totals.

### Pattern 2: Large Volume Migration — Staged Batch Processing

**When to use:** Migrating more than 50,000 gift records where file size or volume exceeds a single BDI batch.

**How it works:**
1. Split source data into chunks of 50,000 records or 100 MB (whichever is reached first)
2. Insert each chunk to DataImport__c in sequence
3. Run a BDI batch for each chunk before inserting the next to avoid staging table bloat
4. Implement donor deduplication logic before staging — BDI uses NPSP Contact Matching Rules to find or create Contacts; duplicate gifts from the same donor will create separate Opportunity records without deduplication

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| < 50,000 gifts, standard NPSP fields | Single BDI batch via NPSP Data Importer UI | Simplest path; all standard field mappings active |
| > 50,000 gifts | Chunked DataImport__c inserts + sequential BDI batches | File and volume limits per batch |
| Custom payment fields needed | Enable Advanced Mapping first, configure field maps, then import | Without Advanced Mapping, custom fields silently go unmapped |
| Soft credits required | Use Contact2 fields on DataImport__c — BDI creates OCRs automatically | Direct OCR insert bypasses NPSP role assignment logic |
| GAU allocation splits > 5 per gift | Enable Advanced Mapping for custom GAU fields | Standard BDI only supports 5 GAU fields per row |
| Direct Data Loader to Opportunity | Do NOT use for NPSP gift import | Bypasses all BDI automation; OCRs, GAU, and payments will be missing |

---

## Recommended Workflow

1. **Confirm Advanced Mapping status** — Check NPSP Settings > Data Import > Advanced Mapping. If custom payment or GAU fields are in scope, enable Advanced Mapping and configure field mappings before staging any data.
2. **Map source fields to DataImport__c columns** — Create a field mapping document correlating each source system field to the appropriate DataImport__c staging column, including Contact matching fields, Opportunity fields, Payment fields, GAU pairs, and soft credit Contact2 fields.
3. **Prepare and validate the staging CSV** — Validate that Contact matching fields (first name, last name, email, or external ID) are populated so BDI can find or create the correct donor records. Confirm GAU record names or IDs are valid before staging.
4. **Insert staging records to DataImport__c** — Use Data Loader with the DataImport__c API name. Load in chunks of ≤50,000 rows. Do not insert more rows than a single BDI batch can process before running.
5. **Run the BDI batch** — From NPSP Data Importer in App Launcher, select the batch and run. Monitor the status field on each DataImport__c row — errors are reported at the row level with descriptive messages.
6. **Validate results with SOQL** — After each batch: confirm Opportunity count matches expected, confirm OCR records exist for each soft credit contact, confirm GAU Allocations were created, confirm payment records (npe01__OppPayment__c) exist.
7. **Reconcile errors** — Review failed DataImport__c rows, correct data, and re-run only failed records. Do not delete and re-insert all rows — BDI tracks processed status and will skip already-imported rows.

---

## Review Checklist

- [ ] Advanced Mapping enabled before attempting to map custom fields
- [ ] DataImport__c used as staging table — not direct Opportunity insert
- [ ] Contact matching fields populated so BDI can deduplicate donors
- [ ] GAU Allocation field pairs populated correctly (both name/ID and amount/percent)
- [ ] Soft credit Contact2 fields populated for secondary donors
- [ ] Post-import SOQL validation: OCR count, GAU allocation count, payment record count
- [ ] Household rollup totals verified on sample donor Contacts after import

---

## Salesforce-Specific Gotchas

1. **Direct Opportunity insert bypasses all BDI automation** — Loading Opportunities directly via Data Loader skips NPSP trigger-based creation of payment records, OCRs, and GAU allocations. The result is a set of Opportunities with no payment records, no soft credits, and stale household totals. This is the single most common gift migration error in NPSP.
2. **Advanced Mapping must be enabled before staging data** — If you stage DataImport__c records before enabling Advanced Mapping and configuring field maps, the custom fields are silently ignored. The BDI batch completes successfully with exit status OK but the custom field data is lost. You must re-import those records with Advanced Mapping active.
3. **GAU Allocation amounts vs. percentages cannot be mixed in the same row** — If a DataImport__c row mixes Amount and Percent fields across its GAU allocation pairs, BDI will use one type and ignore the other. Standardize on amount or percent for the entire import.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| DataImport__c field mapping spec | CSV column list with DataImport__c API names and data type expectations |
| BDI validation SOQL set | Queries to verify OCR, GAU, payment, and household rollup counts post-import |
| Import execution log | Batch run results with error summary by DataImport__c row |

---

## Related Skills

- `data/constituent-data-migration` — For migrating Contact and Household Account records before gifts
- `data/nonprofit-data-architecture` — For NPSP data model design including GAU, payment, and OCR structure
- `apex/npsp-api-and-integration` — For Apex-level BDI processing and NPSP trigger extension
