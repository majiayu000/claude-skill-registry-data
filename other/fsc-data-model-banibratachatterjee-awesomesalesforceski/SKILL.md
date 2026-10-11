---
name: fsc-data-model
description: "Use when designing, querying, or troubleshooting the Financial Services Cloud data model — including managed-package (FinServ__ namespace) and Core FSC (standard objects, no namespace) object structures, household relationship modeling, financial account ownership, and the FSC rollup framework. Trigger keywords: FSC data model, FinancialAccount, FinancialHolding, FinancialAccountRole, FinancialAccountParty, FinServ namespace, household rollup, AssetsAndLiabilities, FinancialGoal, LifeEvent, AccountContactRelation FSC. NOT for standard Salesforce data model or non-FSC financial objects."
category: data
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Performance
triggers:
  - "How do I query financial account data in FSC and which namespace do my objects use?"
  - "Why are household financial totals not updating after I added a new financial account?"
  - "How does FSC model the relationship between a client and their household, and which objects are involved?"
tags:
  - fsc
  - data-model
  - financial-objects
  - finserv
  - rollups
  - financial-services
inputs:
  - Whether the org is managed-package FSC (FinServ__ namespace) or Core FSC (standard objects, no namespace)
  - The financial domain being modeled (banking, wealth, insurance, mortgage)
  - Existing Account and Contact structure (Person Accounts enabled or not)
  - Whether household rollups need to reflect real-time or near-real-time data
outputs:
  - Object relationship map for the relevant FSC deployment type
  - SOQL query patterns that correctly reference namespace-prefixed or standard objects
  - Rollup configuration guidance (async FSC rollup engine vs. native roll-up summary)
  - Data model design decisions with rationale for managed-package vs. Core FSC
dependencies:
  - data/person-accounts
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-11
---

# FSC Data Model

Activate this skill when a practitioner needs to understand, design, or query the Financial Services Cloud (FSC) data model — covering the managed-package deployment with `FinServ__` namespace objects and the platform-native Core FSC deployment using standard objects with no namespace. The skill covers the full object hierarchy from financial accounts through household relationships to rollup aggregation.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Deployment type:** Is the org using managed-package FSC (check Setup > Installed Packages for "Financial Services Cloud" or "Salesforce Industries") or Core FSC (platform-native, standard objects, no `FinServ__` prefix)? This determines every object name and SOQL query used.
- **Person Accounts:** Is Person Accounts enabled? FSC relies on Person Accounts to represent individual clients. Without it, the household and client relationship model does not work as documented.
- **Rollup awareness:** Practitioners assume native Salesforce roll-up summary fields aggregate financial data to household accounts. They do not. FSC uses its own async rollup engine configured in FSC Admin settings.
- **Core FSC vs managed-package cutover:** Orgs that went live before Winter '23 are almost certainly on managed-package FSC. New orgs provisioned after Winter '23 should evaluate Core FSC before defaulting to managed-package.

---

## Core Concepts

### Managed-Package FSC vs. Core FSC

FSC was originally delivered as a managed package under the `FinServ__` namespace. Every custom object, field, and relationship carries that prefix: `FinServ__FinancialAccount__c`, `FinServ__FinancialHolding__c`, etc. Starting with Winter '23, Salesforce began shipping a platform-native version called Core FSC. Core FSC uses standard (no-namespace) objects: `FinancialAccount`, `FinancialHolding`, `FinancialGoal`. Core FSC eliminates package upgrade dependencies and gives full Metadata API control, but it is a different deployment architecture that cannot be retrofitted onto an existing managed-package org without migration work.

**Choosing between them:**
- New org with no existing FSC deployment → evaluate Core FSC as the default.
- Existing org already running managed-package FSC → stay on managed-package; a data and metadata migration to Core FSC is a large project.
- Hybrid or ISV package dependencies → managed-package may be required.

### Key FSC Objects

| Object (managed-package) | Object (Core FSC) | Purpose |
|---|---|---|
| `FinServ__FinancialAccount__c` | `FinancialAccount` | Represents a bank account, investment account, loan, or policy |
| `FinServ__FinancialAccountRole__c` | `FinancialAccountParty` | Links a Contact or Account to a FinancialAccount with an ownership/role type |
| `FinServ__FinancialHolding__c` | `FinancialHolding` | Represents individual securities, positions, or assets held inside a FinancialAccount |
| `FinServ__AssetsAndLiabilities__c` | `AssetsAndLiabilities` | Standalone asset or liability record linked to a client or household |
| `FinServ__ContactContactRelation__c` | Standard `ContactContactRelation` | Peer relationship between two contacts (e.g., spouses, dependents) |
| `FinServ__AccountAccountRelation__c` | Standard `AccountAccountRelation` | Relationship between two accounts (e.g., subsidiary, group hierarchy) |
| `FinServ__FinancialGoal__c` | `FinancialGoal` | Client financial goal with target amount, timeline, and progress tracking |
| `FinServ__LifeEvent__c` | `LifeEvent` | Tracks life events (retirement, marriage, home purchase) tied to a contact |

### Financial Account Ownership Model

**Managed-package:** `FinServ__FinancialAccount__c` has two hardcoded ownership lookups — `FinServ__PrimaryOwner__c` (required) and `FinServ__JointOwner__c` (optional). Only two owners are supported without custom workarounds.

**Core FSC:** The `FinancialAccountParty` junction object replaces the two-lookup pattern. It supports unlimited owners with named roles (Primary Owner, Joint Owner, Beneficiary, Power of Attorney, etc.). This is a significant architectural advantage for complex ownership scenarios such as trusts or investment partnerships.

### Household Relationship Model

FSC models clients and households using standard Salesforce junction objects:

- `AccountContactRelation` (ACR) — links a Contact (individual client) to an Account (the household). The `Roles` field on ACR carries the FSC-specific role (e.g., "Member", "Primary Member").
- `AccountAccountRelation` — links two Accounts. Used when a household account is part of a larger financial group or when corporate account hierarchies need lateral relationships.

The household Account record is typically a Business Account with `RecordType` = "Household." The individual clients are Person Account records linked to the household via ACR. This is distinct from the NPSP household model, which uses a separate `npe01__OOHousehold__c` object or Household Account without Person Accounts.

### FSC Rollup Framework

FSC aggregates financial data (total assets, total liabilities, net worth) to the household Account using its own async rollup engine — **not** Salesforce native roll-up summary fields. The rollup engine is configured in FSC Admin Settings under "Rollup Configuration." Key behaviors:

- Rollups run asynchronously via a scheduled or triggered batch process.
- Rollup values are written to fields on the household Account (e.g., `FinServ__TotalAssets__c`, `FinServ__TotalLiabilities__c`).
- Creating or updating a financial account record does not immediately update the household total — the rollup batch must run.
- In Core FSC, rollup configuration moves to Industries Common Resources rollup framework settings.
- Do not create native roll-up summary fields on the Account object expecting them to aggregate FSC financial data — they have no relationship to the FSC rollup engine.

---

## Common Patterns

### Pattern: Querying a Client's Financial Portfolio

**When to use:** Any time you need to retrieve the financial accounts and holdings associated with a specific client contact.

**How it works (managed-package):**

```soql
-- Get all financial accounts where a contact is primary owner
SELECT Id, Name, FinServ__FinancialAccountType__c, FinServ__Balance__c,
       FinServ__PrimaryOwner__r.Name
FROM FinServ__FinancialAccount__c
WHERE FinServ__PrimaryOwner__c = :contactId

-- Get holdings inside those accounts
SELECT Id, Name, FinServ__Shares__c, FinServ__Price__c, FinServ__FinancialAccount__r.Name
FROM FinServ__FinancialHolding__c
WHERE FinServ__FinancialAccount__r.FinServ__PrimaryOwner__c = :contactId
```

**How it works (Core FSC):**

```soql
-- Get financial accounts via FinancialAccountParty junction
SELECT FinancialAccount.Id, FinancialAccount.Name, FinancialAccount.Balance,
       Role
FROM FinancialAccountParty
WHERE RelatedPerson.Id = :contactId

-- Get holdings
SELECT Id, Name, Quantity, Price, FinancialAccountId
FROM FinancialHolding
WHERE FinancialAccount.Id IN (
    SELECT FinancialAccountId FROM FinancialAccountParty WHERE RelatedPersonId = :contactId
)
```

**Why not the alternative:** Querying directly on `FinancialAccount` without the party junction in Core FSC misses joint owners and named roles. In managed-package, querying only `PrimaryOwner__c` misses joint accounts.

### Pattern: Household Financial Summary via ACR

**When to use:** You need to display aggregated financial data for a household and all its member contacts.

**How it works:**

```soql
-- Find all contacts in a household via AccountContactRelation
SELECT ContactId, Contact.Name, Roles
FROM AccountContactRelation
WHERE AccountId = :householdAccountId AND IsActive = TRUE

-- Read rollup values from the household Account (managed-package)
SELECT Id, Name, FinServ__TotalAssets__c, FinServ__TotalLiabilities__c,
       FinServ__NetWorth__c
FROM Account
WHERE Id = :householdAccountId
```

**Why not the alternative:** Do not aggregate financial account balances in SOQL at query time for household totals in production — this does not scale for households with many accounts. Read the pre-computed rollup fields on the Account and ensure rollup batches are scheduled.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| New org, no existing FSC data | Core FSC (platform-native) | No namespace overhead, unlimited FinancialAccountParty owners, full Metadata API control |
| Existing org on managed-package FSC | Stay on managed-package | Migration to Core FSC requires full data and metadata migration; no in-place upgrade path |
| Complex multi-owner accounts (trusts, partnerships) | Core FSC FinancialAccountParty | Managed-package is limited to PrimaryOwner + JointOwner only |
| ISV or AppExchange package depends on FinServ__ objects | Managed-package | Third-party packages built against managed-package namespace; Core FSC incompatible |
| Household financial totals appear stale after data load | Trigger FSC rollup batch via Admin Settings | FSC rollups are async; totals do not update synchronously on record save |
| Need to query financial accounts across all owners | FinancialAccountParty (Core) or both owner lookups (managed) | Managed-package PrimaryOwner__c alone misses joint accounts |

---

## Recommended Workflow

1. **Identify the FSC deployment type** — check Setup > Installed Packages. If "Financial Services Cloud" or "Salesforce Industries" is listed as a managed package, all object names require the `FinServ__` prefix. If no such package is found but FSC features are available, the org is on Core FSC.
2. **Map the relevant object graph** — identify which objects are in scope: start from `FinancialAccount` (or `FinServ__FinancialAccount__c`), trace ownership via `FinancialAccountParty` or `PrimaryOwner__c`/`JointOwner__c`, and identify the household Account linked via `AccountContactRelation`.
3. **Verify rollup configuration** — for any task that reads household financial totals, confirm the FSC rollup batch is scheduled and the rollup configuration covers the account types involved. Do not assume totals are current.
4. **Write namespace-correct SOQL** — prefix all custom object and field API names with `FinServ__` in managed-package orgs; use no prefix in Core FSC orgs. Test queries in Developer Console or Data Loader against the actual org before finalizing.
5. **Validate ownership completeness** — for multi-owner scenarios, query `FinancialAccountParty` (Core FSC) or both `PrimaryOwner__c` and `JointOwner__c` (managed-package) to ensure all owners are captured; a query on `PrimaryOwner__c` alone misses joint account holders.

---

## Review Checklist

- [ ] Deployment type confirmed (managed-package with `FinServ__` prefix vs. Core FSC standard objects)
- [ ] All SOQL and Apex references use the correct namespace for the org type
- [ ] Household totals are read from pre-computed rollup fields, not aggregated in SOQL
- [ ] FSC rollup batch is scheduled and covers the relevant financial account types
- [ ] Multi-owner scenarios use `FinancialAccountParty` (Core) or both lookup fields (managed-package)
- [ ] `AccountContactRelation` is used for household-to-client membership, not a custom relationship object
- [ ] FSC household model is not confused with NPSP household model

---

## Salesforce-Specific Gotchas

1. **Native ROLLUP summary fields do not aggregate FSC financial data** — Salesforce roll-up summary fields on the Account object have no knowledge of the FSC rollup engine. Adding a native ROLLUP summary field to aggregate `FinServ__Balance__c` values will not work because `FinServ__FinancialAccount__c` is not a detail of Account in the standard master-detail sense for ROLLUP purposes. FSC maintains its own batch-computed rollup fields.

2. **FinServ__ namespace is absent in Core FSC orgs** — Code or queries written against managed-package FSC will fail entirely in a Core FSC org. The object `FinServ__FinancialAccount__c` does not exist; the equivalent is `FinancialAccount`. Always confirm org type before writing any FSC SOQL, Apex, or Flow references.

3. **Managed-package FinancialAccountRole limits ownership to two parties** — `FinServ__FinancialAccountRole__c` exists in managed-package FSC but the primary and joint ownership model is enforced through lookup fields directly on `FinServ__FinancialAccount__c` (`FinServ__PrimaryOwner__c`, `FinServ__JointOwner__c`). Adding a third owner requires a custom junction object or workaround. Core FSC's `FinancialAccountParty` removes this constraint entirely.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Object relationship map | Diagram or table of FSC objects with namespace-correct names, relationship types, and cardinality |
| SOQL query patterns | Namespace-correct SOQL for common financial data access patterns (portfolio, household summary, ownership) |
| Rollup configuration checklist | Steps to verify FSC rollup batch schedule and rollup configuration for household financial totals |

---

## Related Skills

- `data/person-accounts` — FSC relies on Person Accounts for individual client representation; see this skill for Person Account setup and implications
- `admin/financial-account-setup` — FSC Admin Settings configuration for rollups, account types, and financial account record type setup
- `architect/fsc-architecture-patterns` — higher-level architecture decisions including managed-package vs. Core FSC selection, sharing model, and integration patterns
