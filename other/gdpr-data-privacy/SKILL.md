---
name: gdpr-data-privacy
description: "Use this skill when implementing GDPR or CCPA data privacy controls in Salesforce: Individual sObject linkage, consent tracking, Right to Be Forgotten (RTBF) requests, data subject request handling, and Privacy Center configuration. Trigger keywords: GDPR, data privacy, consent management, right to erasure, Individual object, ContactPointConsent, ShouldForget, data subject request, Privacy Center, data portability. NOT for general data quality cleanup, duplicate management, field-level encryption (see platform-encryption skill), or sandbox data masking (see sandbox-data-masking skill)."
category: security
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
triggers:
  - "how do I handle a GDPR right to erasure request in Salesforce"
  - "customer asked to be forgotten — what do I set on their Contact record"
  - "how does the Individual object work and where do I store consent"
  - "setting up consent tracking with ContactPointTypeConsent and ContactPointConsent"
  - "do I need Privacy Center or can I do RTBF with just Apex"
  - "data subject access request — how to export all data for a Contact in Salesforce"
  - "ShouldForget field is set to true but nothing got deleted"
tags:
  - gdpr
  - ccpa
  - data-privacy
  - consent-management
  - right-to-erasure
  - individual-object
  - privacy-center
  - data-subject-requests
inputs:
  - "Which regulation applies: GDPR, CCPA, or both"
  - "Whether Privacy Center is licensed in the org"
  - "Objects that store personal data (Contact, Lead, PersonAccount, custom objects)"
  - "Consent channels in scope (email, phone, direct mail, advertising)"
  - "Expected volume of data subject requests per month"
  - "Retention schedules if Privacy Center retention policies are needed"
outputs:
  - "Individual sObject linkage design (IndividualId field mapping)"
  - "Consent object model: ContactPointTypeConsent + ContactPointConsent records"
  - "Right to Be Forgotten implementation approach (Privacy Center vs. custom Batch Apex)"
  - "Data Subject Request handling workflow (intake, verification, fulfillment, audit trail)"
  - "Anonymization/tokenization pattern for hard-delete avoidance"
  - "Review checklist for GDPR compliance posture"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# GDPR Data Privacy

Use this skill when a practitioner needs to implement GDPR or CCPA data privacy controls inside Salesforce: linking personal data to the Individual sObject, tracking consent through the native consent model, handling Right to Be Forgotten (RTBF) requests, processing data subject requests, or evaluating whether Privacy Center is required.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm whether Privacy Center is licensed. RTBF policy automation and data portability exports are only available through Privacy Center (a separately purchased add-on). Without it, all erasure logic requires custom Batch Apex.
- Identify every object that stores personal data in the org — Contact, Lead, PersonAccount, and any custom objects with PII fields. Erasure must cover all of them, not just Contact.
- Confirm the API version. The Individual sObject and IndividualId field on Contact/Lead/PersonAccount were introduced in API version 42.0 (Winter '18). Older managed packages may not expose IndividualId.
- Determine consent channels in scope. The native consent model is channel-aware: email, phone, fax, direct mail, social, and advertising are separate consent points with independent records.

---

## Core Concepts

### The Individual sObject (API v42+)

The Individual sObject (`Individual`) is a first-party Salesforce object that acts as the privacy and consent container for a natural person. It stores privacy preference flags at the person level rather than duplicating them on every related record.

Key fields on Individual:
- `ShouldForget` (Boolean) — signals that the data subject has invoked their right to erasure. **This is a flag only. Setting it to `true` does not automatically delete or anonymize any data.** Your org must respond to this flag through Privacy Center policies or custom Batch Apex.
- `HasOptedOutOfSolicit` — general solicitation opt-out.
- `SendIndividualData` — whether data may be shared with third parties.
- `CanStorePiiElsewhere` — whether personal data may be stored outside the org's primary region.

Contact, Lead, and PersonAccount each carry an `IndividualId` lookup field. Set this field to associate a person record with their Individual privacy container. One Individual record should represent one natural person; do not share a single Individual across multiple people.

### Native Consent Model: ContactPointTypeConsent and ContactPointConsent

Salesforce provides two objects for fine-grained consent tracking:

**ContactPointTypeConsent** — channel-level consent. Represents a person's blanket opt-in or opt-out for a communication channel (e.g., "opted out of all email"). Key fields:
- `ContactPointType` — channel: Email, Phone, Fax, Web, MailingAddress, Social, or EngagementChannel.
- `OptInStatus` — `OptIn`, `OptOut`, `PendingOptIn`, or `Unknown`.
- `EffectiveFrom`, `EffectiveTo` — the consent window. These allow time-bounded consent (e.g., consent valid until a specific date or renewed at re-opt-in).
- `PartyId` — lookup to the Individual record.

**ContactPointConsent** — contact-point-specific consent. Represents consent for a specific email address, phone number, or other contact point. Key fields:
- `ContactPointId` — polymorphic lookup to the specific contact point (e.g., a Contact's email address via ContactPointEmail).
- `OptInStatus`, `EffectiveFrom`, `EffectiveTo` — same semantics as ContactPointTypeConsent.
- `DataUsePurposeId` — optional link to a DataUsePurpose record describing why data is processed (maps to GDPR Article 6 lawful basis).

Use ContactPointTypeConsent for channel-level blanket preferences. Use ContactPointConsent when you need per-address granularity or need to track consent for a specific processing purpose.

### Right to Be Forgotten: Platform Behavior vs. Automation

RTBF (right to erasure) under GDPR Article 17 requires that personal data be deleted or anonymized when a data subject requests it and no legitimate retention basis overrides the request.

Salesforce does not automatically respond to `ShouldForget = true`. You need one of:

1. **Privacy Center** (licensed add-on): Provides a no-code policy engine. You define Erasure Policies that specify which objects and fields to delete or anonymize, and Privacy Center runs the erasure asynchronously when triggered by a Data Subject Request (DSR) record. Also provides Data Portability (export all data for a subject).

2. **Custom Batch Apex**: Without Privacy Center, you must write a `Database.Batchable` class that queries for records linked to Individuals where `ShouldForget = true`, then deletes or anonymizes them. This path requires careful handling of referential integrity and governor limits.

**Anonymization over hard delete**: In most orgs, hard-deleting a Contact breaks Opportunity, Case, and Order foreign keys. The recommended pattern is to anonymize (tokenize) the personal data fields — replace name, email, phone, and address with non-identifying tokens — while keeping the record shell for relational integrity. Delete only records that have no referential dependencies.

---

## Common Patterns

### Pattern 1: Individual Linkage and Consent Setup

**When to use:** Initial implementation of the privacy data model for contacts or leads who are EU/EEA residents, or any org adopting explicit consent tracking.

**How it works:**
1. Create an `Individual` record for each natural person. Set `HasOptedOutOfSolicit`, `ShouldForget`, and other flags as appropriate.
2. Set `IndividualId` on the related Contact, Lead, or PersonAccount to point to the Individual record.
3. For each communication channel the person has consented to or opted out of, create a `ContactPointTypeConsent` record linked via `PartyId` to the Individual.
4. For specific email addresses or phone numbers with their own consent events, create `ContactPointConsent` records linked to the ContactPointEmail or ContactPointPhone record.
5. Store `EffectiveFrom` and `EffectiveTo` on each consent record to represent the consent window.

**Why not the alternative:** Storing opt-out flags directly on Contact (e.g., `HasOptedOutOfEmail`) provides only a binary current state. It cannot represent time-bounded consent, per-purpose consent, or consent history. The native consent model supports audit trails and multi-channel granularity that Contact fields alone cannot provide.

### Pattern 2: Right to Erasure via Batch Apex (No Privacy Center)

**When to use:** Orgs without Privacy Center that must respond to RTBF requests.

**How it works:**

```apex
// BatchForgotIndividuals.apex
// Queries Individuals with ShouldForget=true and anonymizes linked records.
// Run manually or schedule via System.scheduleBatch().

global class BatchForgotIndividuals implements Database.Batchable<SObject>, Database.Stateful {

    global Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator(
            'SELECT Id FROM Individual WHERE ShouldForget = true'
        );
    }

    global void execute(Database.BatchableContext bc, List<Individual> scope) {
        Set<Id> individualIds = new Map<Id, Individual>(scope).keySet();

        // Anonymize linked Contacts
        List<Contact> contacts = [
            SELECT Id, FirstName, LastName, Email, Phone, MailingStreet
            FROM Contact
            WHERE IndividualId IN :individualIds
        ];
        String token = 'ANON-' + System.now().getTime();
        for (Contact c : contacts) {
            c.FirstName     = 'ANON';
            c.LastName      = token;
            c.Email         = null;
            c.Phone         = null;
            c.MailingStreet = null;
        }
        update contacts;

        // Anonymize linked Leads
        List<Lead> leads = [
            SELECT Id, FirstName, LastName, Email, Phone, Street
            FROM Lead
            WHERE IndividualId IN :individualIds
                AND IsConverted = false
        ];
        for (Lead l : leads) {
            l.FirstName = 'ANON';
            l.LastName  = token;
            l.Email     = null;
            l.Phone     = null;
            l.Street    = null;
        }
        update leads;
    }

    global void finish(Database.BatchableContext bc) {
        // Optionally: send confirmation email, update DSR audit record
    }
}
```

**Why not the alternative:** Deleting Contact records breaks Opportunity, Case, and Order foreign keys, producing orphaned records or DML errors. Anonymization preserves referential integrity while fulfilling the erasure obligation for personal data fields.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Org is licensed for Privacy Center | Use Privacy Center RTBF Policies + DSR object | No-code, auditable, handles data portability too |
| No Privacy Center, low DSR volume (<20/month) | Manual Batch Apex triggered per request | Proportionate; avoids over-engineering |
| No Privacy Center, high DSR volume | Scheduled Batch Apex polling ShouldForget=true | Prevents backlog; runs nightly or weekly |
| Need channel-level consent (email, phone) | ContactPointTypeConsent per channel | Native model; integrates with Marketing Cloud consent sync |
| Need per-address consent with use-purpose tracking | ContactPointConsent + DataUsePurpose | Required for GDPR Article 6 lawful-basis documentation |
| Personal data in custom objects | Extend Batch Apex or Privacy Center policy to custom objects | Erasure obligation covers all personal data regardless of object type |
| Hard delete required (no referential dependencies) | Delete record after verifying no FK references | Check lookup fields; use Database.delete with allOrNone=false |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Assess licensing and scope**: Confirm whether Privacy Center is licensed. Identify all objects storing personal data (Contact, Lead, PersonAccount, custom objects). Determine which regulations apply (GDPR, CCPA, both) and whether the org processes EU/EEA residents' data.

2. **Implement the Individual data model**: For each natural person, create or ensure an `Individual` record exists. Set `IndividualId` on Contact, Lead, and PersonAccount records to link them. Define a trigger or flow to create an Individual automatically when a Contact or Lead is created for a regulated person.

3. **Build the consent model**: Create `ContactPointTypeConsent` records for each channel and each person, capturing `OptInStatus`, `EffectiveFrom`, and `EffectiveTo`. For specific contact points needing per-address or per-purpose consent, create `ContactPointConsent` records linked via `DataUsePurposeId` to a DataUsePurpose record that names the lawful basis.

4. **Implement RTBF handling**: If Privacy Center is available, configure an Erasure Policy for each object containing personal data and create a Data Subject Request workflow. If not, write and test Batch Apex that queries `Individual WHERE ShouldForget = true`, anonymizes linked records on all in-scope objects, and records fulfillment in a custom audit object or custom DSR record.

5. **Handle data subject access requests (DSAR)**: Build an intake process (Experience Cloud form, email-to-case, or manual) that captures the data subject's identity and request type. Verify identity before processing. For data portability, Privacy Center exports a package; without it, write a report or export job across all related objects.

6. **Test and validate**: In a sandbox, set `ShouldForget = true` on test Individual records and execute the batch or Privacy Center policy. Verify all PII fields are anonymized or deleted across Contact, Lead, and custom objects. Confirm no broken foreign keys or orphaned records.

7. **Document retention schedules**: If any personal data must be retained beyond the erasure request (e.g., legal hold, financial records), document the lawful basis and configure Privacy Center retention rules or exception logic in Batch Apex. Do not silently skip erasure without a documented basis.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] Every Contact, Lead, and PersonAccount representing an EU/EEA natural person has `IndividualId` populated
- [ ] `ContactPointTypeConsent` records exist for each consent channel per person, with `EffectiveFrom` and `OptInStatus` populated
- [ ] RTBF mechanism (Privacy Center policy or Batch Apex) covers all objects storing personal data — not just Contact
- [ ] Anonymization is used instead of hard delete for records with FK dependencies
- [ ] DSR intake, verification, fulfillment, and audit-trail workflow is documented and tested
- [ ] Audit trail records each RTBF execution (who requested, when fulfilled, which records affected)
- [ ] Retention exceptions (legal hold, financial records) are documented with lawful basis
- [ ] Batch Apex is governor-limit safe: uses `Database.QueryLocator`, processes in batches of 200 or fewer

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **ShouldForget=true does nothing on its own** — Setting `Individual.ShouldForget = true` is a data flag, not a system action. Salesforce does not automatically delete, anonymize, or suppress any record. If your RTBF implementation relies on setting this flag without responding automation, erasure never happens.
2. **IndividualId is not auto-populated** — Creating a Contact does not automatically create or link an Individual. Your org must implement a trigger or flow; Contacts created before this automation exists will have null `IndividualId` and be invisible to privacy-model queries.
3. **Anonymization must cover all objects** — Leads, PersonAccounts, and custom objects may all hold PII. Batch jobs scoped only to Contact are incomplete; a full data model audit must precede implementation.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Individual linkage design | Mapping of which Contact/Lead/PersonAccount populations need Individual records and how IndividualId will be populated |
| Consent object model | List of ContactPointTypeConsent and ContactPointConsent records with channel, OptInStatus, and EffectiveFrom/To per person |
| RTBF implementation | Privacy Center policy configuration or Batch Apex class covering all in-scope objects |
| DSR workflow | Intake, verification, fulfillment, and audit-trail steps for Data Subject Requests |
| Anonymization token pattern | Convention for replacing PII fields (e.g., `ANON-<timestamp>`) consistent across objects |
| Retention exception register | Table of object/field combinations retained beyond erasure, with documented lawful basis |

---

## Related Skills

- `platform-encryption` — use alongside this skill when fields must be encrypted at rest; encryption does not substitute for erasure
- `sandbox-data-masking` — use to prevent real PII from entering non-production orgs; complements RTBF but is a separate concern
- `data-classification-labels` — use to tag fields containing personal data, a prerequisite for building a complete erasure scope
