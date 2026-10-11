---
name: clinical-data-quality
description: "Use this skill when configuring duplicate detection for Health Cloud patient records, managing Person Account merges in a clinical org, or designing pre-merge clinical record reassignment strategies. Trigger keywords: patient deduplication, MPI, duplicate patients, merge person accounts Health Cloud, clinical record orphan, EpisodeOfCare orphan, PatientMedication orphan. NOT for generic Salesforce data quality or standard deduplication outside Health Cloud."
category: data
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Security
triggers:
  - "How do I detect and merge duplicate patient records in Health Cloud?"
  - "Clinical records are orphaned after merging Person Accounts — how do I fix it?"
  - "Does Health Cloud have a Master Patient Index (MPI) built in?"
tags:
  - health-cloud
  - data-quality
  - duplicate-management
  - mpi
  - patient-records
  - person-accounts
inputs:
  - Health Cloud org with Person Accounts enabled
  - List of clinical objects in scope (EpisodeOfCare, PatientMedication, ClinicalEncounter, etc.)
  - Volume estimate of potential duplicate patient records
  - Whether a third-party MPI or ISV solution is in scope
outputs:
  - Duplicate Rule and Matching Rule configuration guidance for Person Account
  - Pre-merge Apex batch class to reassign clinical records before account merge
  - "Decision table: native duplicate rules vs. third-party MPI"
  - Review checklist for safe patient record merge in Health Cloud
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-11
---

# Clinical Data Quality

Use this skill when working with duplicate patient detection, Person Account merges, or clinical record integrity in a Salesforce Health Cloud org. It activates whenever a practitioner needs to configure Duplicate/Matching Rules for patients, perform Account merges while preserving clinical data, or evaluate MPI alternatives.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm Person Accounts are enabled in the org — Health Cloud requires Person Accounts for its clinical components; the standard Contact merge flow does not apply.
- Identify which clinical objects are in scope: EpisodeOfCare, PatientMedication, ClinicalEncounter, CarePlanTemplate assignments, and any custom objects with Account lookups pointing to patient records.
- Confirm whether a third-party MPI or ISV deduplication solution is licensed. Salesforce Health Cloud has no native Master Patient Index — all deduplication relies on standard Duplicate Rules and Matching Rules configured for the Account (Person Account) object.
- Clarify merge volume. The platform enforces a two-at-a-time limit for Account merges via the standard UI/merge API. Bulk merge scenarios require Apex orchestration that calls the merge DML statement in batches of pairs.

---

## Core Concepts

### No Native Master Patient Index (MPI)

Health Cloud does not ship with a native MPI. There is no out-of-the-box enterprise patient identity resolution engine. Duplicate detection relies entirely on standard Salesforce Duplicate Management: Duplicate Rules scoped to the Account object (which covers Person Accounts) backed by fuzzy or exact Matching Rules on fields such as FirstName, LastName, BirthDate, and SSN-equivalent custom fields. For healthcare organizations at enterprise scale or with complex identity-matching requirements (probabilistic matching, cross-system record linkage), a third-party ISV — such as Veeva, ReltioConnect, or Informatica MDM for Salesforce — is the only path to true MPI capability.

### Person Account Merge Is Account Merge, Not Contact Merge

Person Accounts are Accounts with IsPersonAccount = true. The merge flow for Person Accounts is the **Account merge flow**, not the Contact merge flow. Attempting to invoke a Contact merge on the underlying Contact record of a Person Account is unsupported and will produce errors. The standard Salesforce UI (and the Merge Accounts API) merges exactly two Account records at a time: you select a master record, and the losing record is deleted after related records are reparented. This two-at-a-time constraint is a hard platform limit for the standard merge action.

### Clinical Records Are NOT Automatically Reparented on Merge

This is the highest-risk behavior in Health Cloud deduplication work. When two Person Account records are merged, standard Salesforce reparenting logic moves related records that belong to the **winning** record. However, Health Cloud clinical objects — including `EpisodeOfCare`, `PatientMedication`, `ClinicalEncounter`, and custom objects with explicit Account lookup fields — are **not** automatically reparented. They remain associated with the losing (deleted) Account and become orphaned records. Orphaned clinical records are not surfaced on the winning patient's timeline, care plan, or clinical summary, creating silent patient data loss that is difficult to detect post-merge without explicit audit queries.

---

## Common Patterns

### Pattern 1: Configure Matching and Duplicate Rules for Person Account Patient Detection

**When to use:** Every Health Cloud org that stores patient records should have at least one Matching Rule and one Duplicate Rule scoped to the Account object to detect potential duplicates at record creation time.

**How it works:**
1. Navigate to Setup > Duplicate Management > Matching Rules.
2. Create a new Matching Rule on the **Account** object (not Contact — Person Account deduplication runs on Account).
3. Add match criteria on `FirstName`, `LastName`, `PersonBirthdate`, and any identity field (e.g., `MedicalRecordNumber__c`). Use Fuzzy matching for name fields to catch typos. Use Exact matching for identifier fields.
4. Activate the Matching Rule.
5. Navigate to Setup > Duplicate Management > Duplicate Rules.
6. Create a Duplicate Rule on Account, reference the Matching Rule, and set the action for matching records to **Alert** (not Block) during the initial rollout to avoid disrupting intake workflows. Switch to **Block** after validating match quality.
7. Test by creating two Person Account records with overlapping fields and confirming the duplicate alert fires.

**Why not the alternative:** Applying a Duplicate Rule to the Contact object instead of Account does not cover Person Accounts. Person Account deduplication must be targeted at Account.

---

### Pattern 2: Pre-Merge Clinical Record Reassignment via Apex Batch

**When to use:** Before merging any two Patient (Person Account) records, reassign all clinical records from the losing account to the winning account. This must happen before the merge DML — not after — because after the merge the losing Account ID no longer exists.

**How it works:**
1. Identify all clinical objects with Account/Patient lookups (see references/examples.md for a full list).
2. Write a pre-merge Apex batch that queries each clinical object for records pointing to the losing Account ID and updates them to point to the winning Account ID.
3. Call the batch synchronously (or chain it) before invoking the merge DML statement.
4. After batch completion, execute `merge masterAccount duplicateAccount;` in Apex.
5. Run post-merge audit queries to confirm zero records remain on the deleted Account ID.

**Why not the alternative:** Performing the merge first and trying to reassign clinical records afterward is not possible — the losing Account record no longer exists after merge, and its ID is tombstoned. Queries against the deleted Account ID will return no rows.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Small org, low duplicate volume, single source of truth | Native Duplicate Rules + Matching Rules on Account | Sufficient for controlled intake; no ISV cost |
| Enterprise scale, multi-source patient data, probabilistic matching needed | Third-party MPI ISV (ReltioConnect, Veeva, Informatica) | Native rules only support field-level exact/fuzzy; no cross-system record linkage |
| Merging 2 known duplicates interactively | Standard Account Merge UI or Apex `merge` DML | Supported path for Person Accounts |
| Bulk merge of hundreds of duplicate pairs | Apex Batch with pre-reassignment loop + `merge` DML pairs | Only way to handle volume; two-at-a-time limit applies per DML call |
| Clinical records already orphaned post-merge | Apex data fix script querying by known losing Account IDs | No platform-native fix; must reassign via code |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Identify clinical objects in scope.** Query the org schema for all objects that have a lookup to Account (or a field named PatientId, MemberId, or IndividualId). Include Health Cloud standard objects: EpisodeOfCare, PatientMedication, ClinicalEncounter, CareObservation, CoveredBenefit, and any custom objects. This list drives the pre-merge reassignment batch.
2. **Configure Duplicate and Matching Rules on Account.** Build at minimum one Matching Rule on Account covering FirstName, LastName, and PersonBirthdate. Attach a Duplicate Rule set to Alert mode. Activate both. Do NOT target the Contact object for Person Account deduplication.
3. **Build and test the pre-merge clinical record reassignment batch.** The batch must accept a losing Account ID and a winning Account ID, query each clinical object in scope, and bulk-update the lookup fields before merge. Test in a sandbox with realistic patient data including all clinical object types.
4. **Execute merge in the correct order.** Run pre-merge reassignment batch first — confirm zero errors and zero remaining records on losing Account — then execute the Account merge DML. Never reverse this order.
5. **Run post-merge audit queries.** For each clinical object, confirm record count on the winning Account equals the expected sum of both pre-merge counts. If any discrepancy exists, investigate before releasing the patient record as clean.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] Duplicate Rule and Matching Rule are scoped to the Account object, not Contact
- [ ] Matching Rule covers at minimum FirstName, LastName, and PersonBirthdate
- [ ] All clinical objects with Account lookups are included in the pre-merge reassignment batch
- [ ] Pre-reassignment batch runs and completes with zero errors before merge DML is invoked
- [ ] Post-merge audit queries confirm zero orphaned clinical records on deleted Account IDs
- [ ] Merge approach uses Account merge flow (not Contact merge) for Person Accounts
- [ ] If volume is >100 duplicate pairs, a third-party MPI or bulk merge orchestration pattern is in place

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Clinical records orphaned silently on merge** — Health Cloud clinical objects (EpisodeOfCare, PatientMedication, ClinicalEncounter) are NOT reparented when Person Accounts are merged. They remain on the deleted Account ID and disappear from the winning patient's record permanently unless explicitly reassigned before the merge DML executes.
2. **Person Account merge is two-at-a-time only** — The standard Salesforce merge operation (UI and Apex `merge` DML) merges exactly two Account records per call. There is no bulk merge API. Attempting to merge three-way or pass a list of duplicates to a single merge call will throw a compile or runtime error.
3. **Duplicate Rules on Contact do not cover Person Accounts** — Person Accounts are hybrid records. Their deduplication must be configured on the Account object, not the Contact object. A practitioner who creates a Contact Duplicate Rule expecting it to catch duplicate Person Account patients will find it has no effect.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Matching Rule + Duplicate Rule configuration | Account-scoped matching with fuzzy name + exact identifier fields, set to Alert mode for initial rollout |
| Pre-merge clinical record reassignment batch | Apex batch class that accepts losing/winning Account IDs and reassigns all clinical object records before merge |
| Post-merge audit SOQL queries | Per-object queries to confirm zero orphaned records after a merge operation |

---

## Related Skills

- data/large-scale-deduplication — for high-volume duplicate resolution patterns and bulk merge orchestration strategies applicable when the clinical dedup list is in the thousands
- data/record-merge-implications — for the general Salesforce record merge model, reparenting rules, and field-value winner logic
- admin/health-cloud-patient-setup — for Person Account configuration prerequisites that must be in place before deduplication rules are meaningful
