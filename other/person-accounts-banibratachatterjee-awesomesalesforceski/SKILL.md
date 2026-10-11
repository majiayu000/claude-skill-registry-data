---
name: person-accounts
description: "Use when enabling, configuring, or troubleshooting Person Accounts in a Salesforce org — includes B2C data model design, IsPersonAccount flag handling, Account-Contact behavior differences, reporting impact, migration planning, and integration requirements. NOT for standard B2B Account/Contact modeling. NOT for managing business accounts that share an org with Person Accounts."
category: data
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Scalability
  - User Experience
  - Security
triggers:
  - "how do I enable person accounts in Salesforce"
  - "my org has B2C customers — should I use person accounts or contacts"
  - "IsPersonAccount field is missing or returning false when I expect true"
  - "person account cannot have child contacts — getting an error"
  - "we are migrating from Contact-only B2C model to person accounts"
  - "Health Cloud or FSC individual records setup with person accounts"
  - "reports on Contacts are showing person account records I don't want"
  - "API integration is failing because it can't find the Contact for a person account"
tags:
  - person-accounts
  - B2C
  - account-contact
  - data-model
  - health-cloud
  - fsc
  - migration
  - IsPersonAccount
inputs:
  - "Whether Person Accounts is already enabled in the org or this is a new enablement request"
  - "Current org edition and existing Account/Contact record volumes"
  - "Whether the org is B2B-only, B2C-only, or mixed (B2B + B2C)"
  - "Integration systems and whether they query via Account or Contact objects"
  - "Whether Health Cloud, FSC, or another industry cloud is in use"
outputs:
  - "Person Account enablement prerequisites checklist"
  - "B2C data model design recommendation (Person Account vs standard Account+Contact)"
  - "IsPersonAccount handling guidance for Apex and API code"
  - "Reporting adjustment plan for Contact-based reports"
  - "Migration approach for converting existing Contact-only records to Person Accounts"
  - "Integration guidance for external systems consuming Person Account data"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# Person Accounts

This skill activates when a practitioner needs to enable, configure, build on, or troubleshoot Person Accounts — Salesforce's combined Account+Contact model for individual consumer (B2C) records. It covers the data model semantics, API behavior differences, reporting impact, migration considerations, and integration patterns unique to Person Accounts.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Enablement state**: Is Person Accounts already enabled in this org? Check Setup > Account Settings. Enablement is permanent and one-directional — once enabled it cannot be reversed. If not yet enabled, confirm prerequisites are met before proceeding.
- **Org model type**: Is the org B2C-only, B2B-only, or mixed? Mixed B2B+B2C orgs carry the most complexity — Person Accounts and Business Accounts coexist and must be kept clearly separated in all logic, reports, and integrations.
- **Existing data state**: If enablement is being planned (not yet done), check whether any Contacts without an AccountId exist. Contacts with no AccountId (private contacts) block Person Account enablement.
- **Common wrong assumption**: Practitioners frequently assume the underlying Contact record for a Person Account can be used directly via the Contact object in SOQL or API calls, the same way a standard contact is used. It cannot — the Person Contact is a system-managed record that must be accessed through the Account object or through the PersonContactId field.
- **Key limits in play**: Person Accounts cannot have child Contact records. Person Accounts cannot be the AccountId on an Opportunity in the same way a Business Account can — however Opportunities can be associated to a Person Account using the standard AccountId field. Some AppExchange packages do not support Person Accounts.

---

## Core Concepts

### What Person Accounts Are

A Person Account is a single Salesforce record that simultaneously represents both an Account and a Contact for an individual person (a consumer). When you view a Person Account in the UI or via API, the record is stored as an Account sObject. Behind the scenes, Salesforce automatically creates and maintains a shadow Contact record — called the **PersonContact** — that is linked to the Account record via the `PersonContactId` field.

The `IsPersonAccount` Boolean field on the Account sObject distinguishes Person Accounts from Business Accounts. When `IsPersonAccount = true`, the record is a person account; when `false` (or absent), it is a business account.

Person Account-specific fields (such as `PersonEmail`, `PersonPhone`, `PersonBirthdate`, `PersonMailingCity`) are surfaced on the Account object but are actually stored on the underlying PersonContact. These fields map to the standard Contact fields (`Email`, `Phone`, `Birthdate`, `MailingCity`) on the PersonContact record.

**Person Accounts are designed for B2C use cases** — retail customers, insurance policyholders, healthcare patients, financial services clients — where the customer is an individual person, not an organization.

### Enabling Person Accounts

Enabling Person Accounts is a **one-way, permanent operation**. Once enabled in an org, it cannot be disabled. This makes the decision consequential for org design.

Prerequisites before contacting Salesforce to enable:
1. The org must be Enterprise Edition or higher (or a supported industry cloud edition).
2. All Contacts in the org must have an AccountId — there must be no "private contacts" (Contacts with no parent Account). Run `SELECT Id FROM Contact WHERE AccountId = null` to verify.
3. At least one Account Record Type must exist or be created, which will be designated as the Person Account record type.
4. Review all existing Apex, Flows, integrations, and AppExchange packages for Person Account compatibility.

The actual enablement is performed by Salesforce Support (a support case in production orgs) or via Setup > Account Settings in some sandbox environments. After enablement, at least one Account Record Type must be designated as a Person Account record type in Setup > Account Settings.

**After enablement, you cannot go back.** If your org has B2B records, those Business Accounts will remain Business Accounts — but you now have both models coexisting.

### Data Model and API Behavior

When Person Accounts is enabled:

- Person Accounts are created via the **Account** sObject in the API — not via Contact.
- To create a Person Account via API, specify `RecordTypeId` of a Person Account record type; do not include a LastName on a Contact record separately.
- The `PersonContactId` field on the Account record holds the Id of the automatically-created PersonContact.
- Contact-like fields (PersonEmail, PersonPhone, PersonMobilePhone, PersonBirthdate, PersonMailingStreet, PersonMailingCity, etc.) are accessible directly on the Account record when `IsPersonAccount = true`.
- **SOQL on Contacts returns PersonContact records** — a `SELECT Id FROM Contact` will include the system-managed PersonContact records. Filters that need to exclude them should use `WHERE IsPersonAccount = false` on Account queries, or be aware that Contact queries may include person account contacts.
- Person Accounts are **not accessible via Contact Id** in standard API calls the same way a regular Contact is — the canonical Id is the Account Id.

### Record Types and the Person Account Record Type

After enablement, at least one Account Record Type must be designated as a Person Account record type. This designation:
- Controls which page layouts are shown for Person Accounts vs Business Accounts.
- Determines which Account records can be created as Person Accounts.
- Cannot be un-designated once Person Account records exist with that record type.

Separate Record Type sets are required for Person Accounts and Business Accounts — fields, picklist values, and page layouts differ significantly between the two models.

### Limitations of Person Accounts

- **No child Contacts**: You cannot create a Contact with its AccountId pointing to a Person Account. Person Accounts are individuals — they do not have child contacts.
- **No Contact Roles on Opportunities through the PersonContact**: Standard Opportunity Contact Role behavior works, but the PersonContactId (not a new Contact record) is used.
- **AppExchange compatibility**: Many AppExchange packages were built assuming standard Account+Contact structure and do not handle `IsPersonAccount = true` correctly. Always verify package compatibility before enabling.
- **Merge behavior**: When merging Person Accounts, Salesforce applies different merge rules than for Business Accounts. Person Accounts can only be merged with other Person Accounts.
- **SOQL contact queries**: Any code that queries `SELECT Id FROM Contact` without awareness of Person Accounts will return PersonContact records mixed in with regular Contacts.

### Reporting Impact

Enabling Person Accounts changes the behavior of Contact-based reports:
- Standard **Contacts & Accounts** reports will include Person Account records, since each Person Account has an underlying PersonContact.
- Reports that are intended for B2B contacts will need filters to exclude Person Account contacts: filter on `Account: Is Person Account = False`.
- Reports intended only for Person Accounts should filter on `Account: Is Person Account = True`.
- Some standard report types behave unexpectedly when both Business Accounts and Person Accounts exist — test all Contact-based reports after enablement.

### Health Cloud and Financial Services Cloud

Health Cloud and Financial Services Cloud (FSC) extensively use Person Accounts to represent individual patients, clients, and policyholders. In these industry clouds:
- Person Account enablement is typically mandatory or strongly recommended.
- Industry-specific objects (e.g., `HealthCloudGA__EhrPatient__c`, FSC `FinancialAccount`) relate to Person Accounts via AccountId.
- Standard identity and relationship management features (Household model in FSC, Care Program in Health Cloud) are built on top of Person Accounts.

---

## Common Patterns

### Pattern: Checking IsPersonAccount Before Processing in Apex

**When to use:** Any Apex trigger, batch, or service class that operates on Account records in a mixed B2B+B2C org. Without this check, logic built for Business Accounts will silently execute against Person Accounts and vice versa.

**How it works:**

```apex
trigger AccountTrigger on Account (before insert, before update) {
    for (Account acc : Trigger.new) {
        if (acc.IsPersonAccount) {
            // Person Account-specific logic
            // Use PersonEmail, PersonPhone, PersonBirthdate
            processPersonAccount(acc);
        } else {
            // Business Account logic
            processBusinessAccount(acc);
        }
    }
}
```

Note: `IsPersonAccount` is a formula field on Account. In `before insert` triggers it may not yet be set — check if a Person Account Record Type Id is being assigned instead.

**Why not skip the check:** Business Account logic often accesses child Contacts (which Person Accounts cannot have), and Person Account logic accesses Person-prefixed fields (which are null on Business Accounts). Mixing the two without branching causes null pointer errors and data corruption.

### Pattern: Querying Person Accounts via the Account Object

**When to use:** When an integration or report needs to retrieve all individual consumers (Person Accounts) from a mixed org.

**How it works:**

```soql
SELECT Id, Name, PersonEmail, PersonPhone, PersonBirthdate, PersonContactId
FROM Account
WHERE IsPersonAccount = true
ORDER BY Name
```

To also access Contact-model fields through the PersonContact relationship:

```soql
SELECT Id, Name, PersonEmail, PersonContact.OtherCity
FROM Account
WHERE IsPersonAccount = true
```

**Why not query Contact:** Querying Contact returns PersonContact records mixed with regular Contacts. The Contact record for a Person Account is system-managed and not the canonical record — the Account Id is the canonical identifier.

### Pattern: Excluding Person Accounts from B2B Contact Queries

**When to use:** Existing code or reports that query Contacts and must not include Person Account PersonContact records.

**How it works:**

```soql
SELECT Id, FirstName, LastName, Email, AccountId
FROM Contact
WHERE Account.IsPersonAccount = false
```

Or in Apex trigger on Contact, skip PersonContact records:

```apex
for (Contact c : Trigger.new) {
    if (c.Account.IsPersonAccount) {
        continue; // skip Person Account system contacts
    }
    // standard Contact logic
}
```

**Why this matters:** Without this filter, automations that iterate over Contacts will process PersonContact records — which are system-managed and should not be directly modified or deleted by custom logic.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Org is pure B2C (all customers are individual people) | Enable Person Accounts, use Person Account record type for all Account records | Unified model; all consumer fields on one record |
| Org is pure B2B (all accounts are organizations) | Do not enable Person Accounts | No benefit; adds complexity to reports and code |
| Org has both organizations and individuals as customers | Enable Person Accounts; use separate Account Record Types for Person vs Business | Coexistence requires strict branching in all code and reports |
| External system sends one record per person (no separate account) | Map to Person Account via Account API; use PersonEmail/PersonPhone fields | Person Account is the canonical single-record consumer model |
| External system sends separate Account and Contact records | Map to standard Business Account + Contact | Person Accounts do not support child contacts |
| Org runs Health Cloud or FSC | Enable Person Accounts (required or strongly recommended by industry cloud) | Industry cloud relationships are built on Person Account model |
| AppExchange package does not support Person Accounts | Evaluate package compatibility before enablement; contact ISV if needed | Some packages break when `IsPersonAccount = true` records exist |
| Need to report on consumers only (no business accounts) | Add `Account: Is Person Account = True` filter to all relevant reports | Without this filter, Business Accounts appear in consumer reports |
| Need to convert existing individual Contacts to Person Accounts | Plan a data migration; there is no automatic conversion | No out-of-box tool converts Business Account+Contact pairs to Person Accounts |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on Person Accounts:

1. **Confirm prerequisites and scope**: Check if Person Accounts is already enabled. If not, run the query `SELECT Id FROM Contact WHERE AccountId = null` to confirm no private contacts exist. Confirm org edition eligibility. Document whether this is a pure B2C org or a mixed B2B+B2C org.
2. **Assess impact before enablement**: Audit all Apex classes, triggers, Flows, and AppExchange packages for Person Account compatibility. Specifically look for code that queries Contacts without an `IsPersonAccount` filter, or that creates Contacts with a Business Account parent.
3. **Configure Record Types**: Ensure at least one Account Record Type is designated (or will be designated) as a Person Account record type. Design separate page layouts for Person Accounts vs Business Accounts.
4. **Request enablement**: Open a Salesforce Support case for production orgs, or enable via Setup in sandbox. Verify the `IsPersonAccount` field appears on Account after enablement.
5. **Update code and reports**: Add `IsPersonAccount` checks to all Apex that processes Account or Contact records. Update Contact-based SOQL queries to filter out PersonContact records where needed. Update reports to add `Is Person Account` filters.
6. **Test integrations**: Run integration tests against sandbox. Confirm external systems correctly set `RecordTypeId` to a Person Account record type when creating individuals. Confirm `IsPersonAccount` flag is handled in inbound and outbound payloads.
7. **Validate and document**: Run `scripts/check_person_accounts.py` against exported metadata. Confirm all checklist items pass. Document the B2B/B2C model decision and any integration contract changes.

---

## Review Checklist

Run through these before marking Person Accounts work complete:

- [ ] No private Contacts (Contacts with null AccountId) exist in the org
- [ ] At least one Account Record Type is designated as a Person Account record type
- [ ] All Apex triggers/classes that process Account or Contact records branch on `IsPersonAccount`
- [ ] All SOQL queries against Contact that should not return PersonContact records include `Account.IsPersonAccount = false` filter
- [ ] Contact-based reports that should be B2B-only have `Is Person Account = False` filter applied
- [ ] Consumer-only reports have `Is Person Account = True` filter applied
- [ ] All AppExchange packages in the org have been verified as compatible with Person Accounts
- [ ] Integrations creating individual records use a Person Account record type, not a separate Contact insert
- [ ] Integrations reading person data query Account (with `IsPersonAccount = true`), not Contact
- [ ] Health Cloud / FSC industry cloud relationships correctly use AccountId pointing to Person Account

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Person Account enablement is permanent and irreversible** — Once enabled, Person Accounts cannot be disabled. If the org later decides the B2C model is not needed, there is no rollback. All related data, record types, and code changes persist. This decision must be made deliberately with full stakeholder alignment.

2. **SOQL on Contact includes PersonContact records** — Any existing `SELECT ... FROM Contact` query will silently include the system-managed PersonContact records for each Person Account. Automations or integrations that process Contact query results will encounter these records and may behave incorrectly — updating, deleting, or re-syncing system-managed records they were not designed to handle.

3. **Person Accounts cannot have child Contacts** — A common mistake when migrating a B2C org is trying to link a Contact to a Person Account via `AccountId`. Salesforce blocks this with an error. Person Accounts represent individual people and do not model an organization with employees.

4. **IsPersonAccount is null (not false) in before insert context** — In a `before insert` trigger on Account, `IsPersonAccount` has not yet been set by the platform. Do not rely on this field in `before insert` logic; instead check whether the `RecordTypeId` being assigned is a Person Account record type.

5. **AppExchange packages silently fail or error on Person Account records** — Many older AppExchange packages were built before Person Accounts were common and assume all Accounts have child Contacts. When these packages run actions on Person Accounts, they may throw errors, silently skip records, or corrupt data by creating orphan Contacts attached to Person Accounts (which then fails the platform constraint).

6. **Merging Person Accounts with Business Accounts is blocked** — Salesforce only allows merging records of the same type. You cannot merge a Person Account with a Business Account. Duplicate detection rules need to be segmented separately for Person Accounts and Business Accounts to avoid false merge suggestions.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| `person-accounts-template.md` | Work template for Person Account enablement or migration projects — captures prerequisites, record type design decisions, Apex impact assessment, and integration changes |
| `check_person_accounts.py` | stdlib Python checker that scans Salesforce metadata XML for common Person Account issues: Apex classes missing IsPersonAccount checks, Contact SOQL without person account filters |

---

## Related Skills

- `data-model-design-patterns` — use for general object relationship design decisions (lookup vs master-detail, junction objects) that apply to B2B models or to objects related to Person Accounts
- `record-types-and-page-layouts` — use when configuring the separate Record Types and page layouts required for Person Account vs Business Account records
- `data-migration-planning` — use when planning the conversion of an existing Contact-only B2C model to Person Accounts, including data transformation and cutover strategy
- `soql-query-optimization` — use when debugging slow SOQL queries on Account or Contact objects in orgs with large Person Account volumes
