---
name: npsp-data-model
description: "Use this skill when working with NPSP (Nonprofit Success Pack) objects, namespace prefixes, GAU allocations, recurring donation objects, relationship and affiliation objects, or the NPSP data dictionary. Trigger keywords: npe01__, npe03__, npe4__, npe5__, npsp__, OppPayment__c, Recurring_Donation__c, Allocation__c, General_Accounting_Unit__c, NPSP data model. NOT for standard Salesforce data model, Financial Services Cloud data model, or Program Management Module (PMM) data model."
category: data
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Operational Excellence
  - Security
triggers:
  - "What namespace prefix does NPSP use for recurring donations or payments?"
  - "SOQL query against NPSP objects is returning no results even though records exist"
  - "How do GAU allocations relate to Opportunities in NPSP and what happens when I delete an Opportunity?"
  - "Creating installment Opportunities directly for a recurring donation and rollup fields on Contact are wrong"
  - "What are all the NPSP managed package objects and their correct API names?"
tags:
  - npsp
  - data-model
  - namespaces
  - gau-allocations
  - recurring-donations
  - nonprofit
inputs:
  - "Confirmation that the org has NPSP (Nonprofit Success Pack) installed"
  - "The specific NPSP object or feature area being queried or designed for"
  - "NPSP version installed (check npe01__Households_Settings__c or the Installed Packages list)"
outputs:
  - "Correct namespace-prefixed API names for all relevant NPSP objects and fields"
  - "SOQL query patterns using accurate NPSP object and field names"
  - "Data model diagram or relationship description for the requested NPSP object area"
  - "Guidance on safe data operations that preserve rollup integrity"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-11
---

# NPSP Data Model

Activate this skill when a practitioner needs to understand, query, or design around the Nonprofit Success Pack (NPSP) managed-package data model — covering the five distinct namespace prefixes, their objects, and the cross-object relationships that govern donations, payments, recurring gifts, relationships, affiliations, and fund allocations. NOT for the standard Salesforce data model, Financial Services Cloud, or Program Management Module (PMM).

---

## Before Starting

Gather this context before working on anything in this domain:

- **Confirm NPSP is installed**: check the Installed Packages list for "Nonprofit Success Pack" or query `npe01__Households_Settings__c`. If absent, none of the namespace-prefixed objects exist.
- **Most common wrong assumption**: practitioners and LLMs both assume all NPSP objects use the `npsp__` prefix. In reality NPSP uses five distinct namespace prefixes and using the wrong one silently returns zero rows from SOQL without an error.
- **Key limits in play**: GAU Allocation records are not owned by the Opportunity via a master-detail; they are lookup-related, so deleting an Opportunity does NOT cascade-delete its allocations. Orphaned `npsp__Allocation__c` records cause reconciliation and reporting errors.

---

## Core Concepts

### The Five Namespace Prefixes

NPSP ships as a set of related managed packages, each with its own namespace:

| Namespace | Package area | Key objects |
|---|---|---|
| `npe01__` | Households and Payments | `npe01__OppPayment__c`, `npe01__Contacts_And_Orgs_Settings__c`, `npe01__Households_Settings__c` |
| `npe03__` | Recurring Donations | `npe03__Recurring_Donation__c`, `npe03__Custom_Field_Mapping__c` |
| `npe4__` | Relationships | `npe4__Relationship__c`, `npe4__Relationship_Settings__c` |
| `npe5__` | Affiliations | `npe5__Affiliation__c`, `npe5__Affiliation_Settings__c` |
| `npsp__` | Core NPSP (GAU, Allocations, Triggers, Settings) | `npsp__Allocation__c`, `npsp__General_Accounting_Unit__c`, `npsp__Trigger_Handler__c`, `npsp__Batch_Data_Entry_Settings__c` |

Every Apex, SOQL, or metadata reference must use the exact namespace prefix for the object being referenced. Using `npsp__OppPayment__c` instead of `npe01__OppPayment__c` returns no results and no error.

### GAU Allocations Are Lookups, Not Master-Detail

`npsp__Allocation__c` records relate to `Opportunity` via a lookup field (`npsp__Opportunity__c`), not a master-detail relationship. This has two important consequences:

1. Deleting an Opportunity does NOT cascade-delete its associated `npsp__Allocation__c` records. Orphaned allocations remain and can distort GAU reporting.
2. When cloning or migrating Opportunities, allocation records must be explicitly cloned or deleted. The standard Salesforce clone operation does not copy related lookup records.

When writing delete or migration logic touching Opportunities, always query and handle related `npsp__Allocation__c` records explicitly.

### Recurring Donations and Installment Opportunities

`npe03__Recurring_Donation__c` drives a schedule-based process that auto-creates child Opportunity "installments." These installment Opportunities carry a lookup back to the parent `npe03__Recurring_Donation__c` via the `npe03__Recurring_Donation__c` lookup field on Opportunity (a custom field added by NPSP).

Direct creation of installment Opportunities without a parent recurring donation bypasses NPSP's schedule-tracking logic and breaks rollup fields on Contact (`npe03__TotalOppAmount__c`) and Account. Always create the parent `npe03__Recurring_Donation__c` first and let NPSP generate installments, or use NPSP's provided Apex APIs to create them programmatically with the correct parent reference.

### Relationship and Affiliation Objects

`npe4__Relationship__c` is a junction object between two Contacts. It carries reciprocal relationship types (e.g., Spouse, Colleague). NPSP auto-creates mirror relationship records in both directions; deleting one mirror record triggers deletion of the other.

`npe5__Affiliation__c` links a Contact to a non-household Account, tracking role, dates, and primary affiliation status. It is distinct from the standard `AccountContactRelationship` object; the two coexist but serve different purposes.

---

## Common Patterns

### Querying GAU Allocations for a Set of Opportunities

**When to use:** Reporting or migration tasks that need to know how an Opportunity's revenue is split across General Accounting Units.

**How it works:**

```soql
SELECT Id, npsp__Amount__c, npsp__Percent__c,
       npsp__General_Accounting_Unit__c,
       npsp__General_Accounting_Unit__r.Name,
       npsp__Opportunity__c
FROM npsp__Allocation__c
WHERE npsp__Opportunity__c IN :opportunityIds
```

**Why not the alternative:** A subquery from Opportunity does not work because the relationship is a lookup (not master-detail). You must query `npsp__Allocation__c` directly and filter by Opportunity.

### Querying Active Recurring Donations and Their Installments

**When to use:** Auditing open recurring gifts, identifying donors with active giving schedules, or migrating recurring donation data.

**How it works:**

```soql
-- Step 1: Get active recurring donations
SELECT Id, Name, npe03__Amount__c, npe03__Date_Established__c,
       npe03__Installment_Period__c, npe03__Contact__c,
       npe03__Organization__c
FROM npe03__Recurring_Donation__c
WHERE npe03__Open_Ended_Status__c = 'Open'

-- Step 2: Get installment Opportunities for a recurring donation
SELECT Id, Name, Amount, StageName, CloseDate,
       npe03__Recurring_Donation__c
FROM Opportunity
WHERE npe03__Recurring_Donation__c = :rdId
ORDER BY CloseDate ASC
```

**Why not the alternative:** Do not query Opportunities by a naming convention or date range alone to find installments. Always use the `npe03__Recurring_Donation__c` lookup field to anchor the query to the parent record.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Need to write SOQL for an NPSP object | Look up the exact namespace prefix from the five-prefix table above | Wrong prefix returns zero rows with no error |
| Deleting Opportunities in bulk | Query and delete or reassign `npsp__Allocation__c` records first | Lookup relationship means no cascade delete |
| Creating installment Opportunities programmatically | Create parent `npe03__Recurring_Donation__c` first; use NPSP APIs or set the lookup field | Bypassing parent breaks Contact/Account rollups |
| Tracking a contact's organizational relationships | Use `npe5__Affiliation__c` for Account affiliations, `npe4__Relationship__c` for Contact-to-Contact | Each object has a distinct purpose and schema |
| Migrating NPSP data to a new org | Export each namespace's objects separately; preserve all lookup IDs; handle allocations explicitly | Cross-namespace relationships are not visible to standard export tools |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Confirm NPSP installation** — verify the org has NPSP installed by checking the Installed Packages list or running `SELECT Id FROM npe01__Households_Settings__c LIMIT 1`. Do not proceed with namespace-prefixed references in an org without NPSP.
2. **Identify the correct namespace prefix** — use the five-prefix reference table to confirm which namespace owns the object you are working with. Never assume `npsp__` is correct for all objects.
3. **Check for cross-object lookup relationships** — for GAU Allocations, confirm that deleting or migrating the parent Opportunity requires explicit handling of related `npsp__Allocation__c` records.
4. **For recurring donation work** — confirm whether the task involves the parent `npe03__Recurring_Donation__c`, its child installment Opportunities, or both. Always maintain the parent-child lookup to preserve rollup integrity.
5. **Write and test SOQL with exact API names** — use Workbench or Developer Console to validate the query returns expected results before embedding it in Apex or a flow.
6. **Review output artifacts** — confirm all generated API names, field references, and relationship traversals use the correct namespace and match the actual org schema.
7. **Run the checker script** — execute `python3 scripts/check_npsp_data_model.py --manifest-dir <path>` to scan metadata files for namespace errors and missing parent relationships.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] All NPSP object API names use the correct namespace prefix (not uniformly `npsp__`)
- [ ] Any code or query touching `Opportunity` deletion also handles related `npsp__Allocation__c` records
- [ ] Installment Opportunities are created with a valid `npe03__Recurring_Donation__c` parent reference
- [ ] Relationship and affiliation objects (`npe4__`, `npe5__`) are not confused with each other or with standard `AccountContactRelationship`
- [ ] SOQL queries are validated against actual org metadata before use in production Apex or flows
- [ ] GAU allocation percentages or amounts are confirmed to sum correctly per Opportunity before deployment

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Wrong namespace prefix returns zero rows silently** — using `npsp__OppPayment__c` instead of `npe01__OppPayment__c` in SOQL produces no error and returns an empty result set. This is the most common source of "why is my query returning nothing?" bugs in NPSP orgs.
2. **Opportunity delete does not cascade to GAU Allocations** — `npsp__Allocation__c` is linked via a lookup, not master-detail. Orphaned allocations continue to accumulate and corrupt GAU reporting until explicitly cleaned up.
3. **Direct installment Opportunity creation breaks rollups** — NPSP rolls up total giving to Contact and Account via fields like `npe01__TotalOppAmount__c`. Creating Opportunities without the `npe03__Recurring_Donation__c` lookup populated bypasses the recurring donation schedule and produces incorrect rollup values.
4. **Mirror relationship deletion is bidirectional** — deleting one `npe4__Relationship__c` record triggers NPSP automation to delete the reciprocal mirror record. Bulk deleting relationship records via Data Loader can cause double-count errors on delete batches.
5. **Affiliation primary flag is org-wide scoped per Contact** — `npe5__Primary__c` on `npe5__Affiliation__c` is managed by NPSP automation. Setting it directly in DML during data loads can trigger NPSP's affiliation process, which sets and unsets primary flags on other affiliations for the same contact.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| NPSP namespace prefix reference table | Quick-lookup table of all five namespaces, the objects they own, and common field API names |
| SOQL query patterns | Correct namespace-prefixed queries for payments, recurring donations, GAU allocations, relationships, and affiliations |
| Data migration checklist | Checklist for handling NPSP cross-object lookups and allocation orphan cleanup during Opportunity migrations |

---

## Official Sources Used

- NPSP Data Model Gallery — https://developer.salesforce.com/docs/nonprofit/npsp/guide/npsp-data-model.html
- NPSP Objects and Fields Data Dictionary — https://help.salesforce.com/s/articleView?id=sfdo.NPSP_Objects_and_Fields_Data_Dictionary.htm&type=5
- Trailhead: Explore the NPSP Data Model — https://trailhead.salesforce.com/content/learn/modules/nonprofit-success-pack-basics/explore-the-npsp-data-model

---

## Related Skills

- admin/npsp-household-accounts — household account configuration and the npo02__ namespace for household rollup fields
- admin/npsp-program-management — PMM data model (ServiceDelivery__c, Program__c); distinct from NPSP donation objects
- data/fsc-data-model — Financial Services Cloud data model; FinServ__ namespace is entirely separate from NPSP namespaces
