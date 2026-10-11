---
name: fhir-data-mapping
description: "Use this skill when mapping FHIR R4 clinical resources (Patient, Observation, Condition, CarePlan, CodeableConcept) to Salesforce Health Cloud objects. Triggers: 'how do I map FHIR patient to Salesforce', 'FHIR Condition to Health Cloud object', 'FHIR R4 Support Settings', 'CodeableConcept to CodeSetBundle', 'HL7 FHIR integration Health Cloud'. NOT for general EHR integration design, HL7 v2 message parsing, outbound FHIR API exposure, or non-clinical Salesforce data migration."
category: data
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Reliability
  - Operational Excellence
triggers:
  - "how do I map a FHIR patient resource to a Salesforce Health Cloud record"
  - "FHIR Condition or Observation not showing up after import into Health Cloud"
  - "CodeableConcept codings exceed the 15-field limit on CodeSetBundle"
tags:
  - fhir
  - health-cloud
  - clinical-data-model
  - fhir-r4
  - data-migration
inputs:
  - FHIR R4 resource bundle or individual resources (Patient, Observation, Condition, CarePlan)
  - Org metadata export or knowledge of whether FHIR-Aligned Clinical Data Model preference is enabled
  - List of CodeableConcept codings per resource (to assess truncation risk)
outputs:
  - Field-level mapping table from FHIR resource elements to Salesforce Health Cloud object fields
  - Middleware transformation logic recommendations for cardinality mismatches
  - Pre-load checklist confirming org prerequisite configuration
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-11
---

# FHIR Data Mapping

This skill activates when a practitioner needs to translate FHIR R4 clinical resources into Salesforce Health Cloud's FHIR-aligned object model. It covers the five primary resource mappings (Patient, Observation, Condition, CarePlan, CodeableConcept), prerequisite org configuration, cardinality differences, and the structural patterns (Person Account, Case Teams, CodeSetBundle) that replace direct FHIR references in the platform.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Org preference status:** The FHIR-Aligned Clinical Data Model org preference must be enabled under Setup > FHIR R4 Support Settings before any FHIR-aligned clinical objects (CareObservation, HealthCondition, etc.) become available. If this preference is off, the objects simply do not appear in the schema — no error, just absence.
- **Most common wrong assumption:** Practitioners assume FHIR Patient maps to standard Account/Contact fields. It does not. Patient maps to a Person Account with child PersonName, ContactPointPhone, and ContactPointAddress records. Writing directly to Account.FirstName or Contact.Email bypasses the correct model and breaks downstream clinical queries.
- **CodeableConcept limit:** FHIR allows unlimited codings on a CodeableConcept. Salesforce Health Cloud supports a maximum of 15 coding references per CodeSetBundle (fields CodeSet1Id through CodeSet15Id). Any source with more than 15 codings must be truncated in middleware before load — the platform does not auto-truncate and will error or silently drop data depending on the load path.
- **Condition.code cardinality:** FHIR defines condition.code as 0..1 (optional). Health Cloud's HealthCondition object requires a code reference — it is effectively 1..1. A FHIR Condition without a code will fail to load unless middleware supplies a default or placeholder code.

---

## Core Concepts

### The FHIR-Aligned Clinical Data Model Org Preference

Salesforce Health Cloud ships with a FHIR-aligned object model that must be explicitly activated. Navigate to Setup > FHIR R4 Support Settings and enable "FHIR-Aligned Clinical Data Model." This preference gates the visibility of the clinical object schema: CareObservation, HealthCondition, CarePlan, CarePlanDetail, CarePlanActivity, PersonName, ContactPointPhone, and ContactPointAddress. Activating it is not reversible in most orgs without Salesforce support involvement, so confirm this step with the org owner before proceeding.

### Person Account as the FHIR Patient Target

FHIR Patient demographics do not map to the standard Account or Contact SObjects. They map to a Person Account (a single SObject that merges Account and Contact fields) plus three associated child records:

- **PersonName** — stores given name, family name, use (official, nickname, maiden)
- **ContactPointPhone** — stores phone numbers with use and rank
- **ContactPointAddress** — stores home, work, and mailing addresses

Middleware must construct all four records and link them with the correct lookup fields. Do not write patient name or address data directly to Account.Name, Account.BillingStreet, or Contact.Phone.

### CodeableConcept to CodeSetBundle Flattening

FHIR CodeableConcept carries an array of Coding objects (system + code + display), each representing the same clinical concept in a different terminology (SNOMED CT, ICD-10, LOINC, CPT, etc.). Health Cloud flattens this into a CodeSetBundle record that holds up to 15 CodeSet reference fields (CodeSet1Id–CodeSet15Id). Each CodeSet record holds one coding. If the source FHIR resource carries more than 15 codings, middleware must select the highest-priority codings before writing to Salesforce. Standard priority order: SNOMED CT > LOINC > ICD-10-CM > CPT > local codes.

### CarePlan and careTeam Structural Split

FHIR CarePlan includes a careTeam element that references CareTeam resources. Health Cloud does not model this as a direct object reference on CarePlan. Instead:

- CarePlan maps to the CarePlan SObject, with child CarePlanDetail and CarePlanActivity records for each activity element.
- The careTeam is implemented as a **Case Team** on the parent Case record that the CarePlan is related to.

Middleware must resolve FHIR CareTeam member references into Salesforce User or Contact records and add them to the Case Team — not into a field on CarePlan.

---

## Common Patterns

### Pattern: Staged Clinical Load with Prerequisite Validation

**When to use:** Any initial data load of FHIR resources into a Health Cloud org, including sandbox loads before production migration.

**How it works:**
1. Validate org preference via metadata query: confirm `FhirR4SupportSettings.isFhirAlignedClinicalDataModelEnabled = true`.
2. Load CodeSet master records first (before CodeSetBundle, since bundle references them by ID).
3. Load PersonName, ContactPointPhone, ContactPointAddress after Person Accounts.
4. Load HealthCondition only for Conditions that include a condition.code; queue code-less Conditions for manual review.
5. Load CareObservation and CareObservationComponent for Observation resources.
6. Load CarePlan + CarePlanDetail + CarePlanActivity.
7. Resolve careTeam members and add to the parent Case's Case Team.

**Why not the alternative:** Loading all resources in a single pass without ordering causes FK constraint failures (CodeSetBundle before CodeSet) and leaves orphaned clinical records.

### Pattern: Middleware Normalization for CodeableConcept Truncation

**When to use:** Source FHIR resources include Conditions, Observations, or Medications with CodeableConcept arrays containing more than 15 codings.

**How it works:**
1. Parse the codings array from the FHIR resource.
2. Sort codings by a priority map keyed on `coding.system` URI (e.g., `http://snomed.info/sct` = 1, `http://loinc.org` = 2, `http://hl7.org/fhir/sid/icd-10-cm` = 3).
3. Keep the top 15 by priority rank.
4. Log the discarded codings to an audit file for clinical review.
5. Write the retained codings to CodeSet records, then write CodeSetBundle with CodeSet1Id through CodeSetNId populated.

**Why not the alternative:** Attempting to write more than 15 CodeSet references will fail at the DML layer or silently truncate depending on load mechanism; the audit step is required for clinical governance.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| FHIR Patient with name, phone, and address | Create Person Account + PersonName + ContactPointPhone + ContactPointAddress child records | Platform model requires child records; writing to Account/Contact fields bypasses clinical data model |
| FHIR Condition without a condition.code | Queue for manual review; do not load with a blank code | HealthCondition.Code is required (1..1 in HC vs 0..1 in FHIR); a null code will fail validation |
| FHIR Observation with components | Load CareObservation as parent, one CareObservationComponent per component element | Observation.component maps to child CareObservationComponent records, not inline fields on CareObservation |
| FHIR CarePlan with careTeam references | Resolve CareTeam members to Salesforce Users or Contacts; add to Case Team on parent Case | Health Cloud has no direct careTeam object on CarePlan; Case Teams implement the clinical team relationship |
| CodeableConcept with more than 15 codings | Truncate to top 15 by terminology priority in middleware; audit discards | CodeSetBundle supports CodeSet1Id–CodeSet15Id only; excess codings cannot be stored |
| org preference not yet enabled | Enable FHIR-Aligned Clinical Data Model in Setup before any schema or data work | Clinical SObjects are not visible until this preference is active; no warning is shown — objects simply absent |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Confirm org prerequisite:** Verify that FHIR R4 Support Settings > FHIR-Aligned Clinical Data Model is enabled in the target org. Check via Setup UI or by querying the `FhirR4SupportSettings` metadata. Do not proceed until confirmed.
2. **Audit the source FHIR bundle:** Identify which FHIR resource types are present (Patient, Observation, Condition, CarePlan, Medication, etc.), note cardinality of CodeableConcept codings arrays, and flag any Conditions lacking a code element.
3. **Design the load sequence:** Plan the order of record creation — CodeSet records before CodeSetBundle, Person Account before child PersonName/ContactPointPhone/ContactPointAddress, CareObservation before CareObservationComponent, CarePlan before CarePlanDetail and CarePlanActivity.
4. **Build middleware transformation logic:** For each resource type, write transformation logic that handles: CodeableConcept truncation to 15 codings, condition.code defaulting/quarantine policy, and careTeam resolution to Case Team membership.
5. **Execute load in stages with rollback checkpoints:** Load in dependency order. After each stage, validate record counts and spot-check FK integrity before proceeding. Log all discarded codings and quarantined resources.
6. **Validate clinical data integrity:** After load, run queries to confirm that HealthCondition.Code is populated on all loaded records, CareObservationComponent parent links are correct, and PersonName records are linked to the correct Person Account.
7. **Review against checklist and document deviations:** Use the review checklist below. Document any source data quality issues (code-less Conditions, oversized CodeableConcepts) in a migration exceptions log for clinical stakeholder sign-off.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] FHIR-Aligned Clinical Data Model org preference confirmed enabled in target org
- [ ] All loaded HealthCondition records have a non-null Code lookup populated
- [ ] No FHIR patient demographics were written directly to Account or Contact fields; Person Account + child records used
- [ ] CodeSetBundle records have no more than 15 CodeSet references; truncation audit log produced for any source codings beyond 15
- [ ] CarePlan careTeam members resolved to Case Team members on parent Case, not to a field on CarePlan
- [ ] CareObservationComponent records linked to correct CareObservation parent
- [ ] Quarantined resources (code-less Conditions, oversized CodeableConcepts) documented and reviewed by clinical stakeholder

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Missing clinical objects with no error message** — If FHIR-Aligned Clinical Data Model org preference is not enabled, objects like CareObservation and HealthCondition are simply absent from the schema. Queries against them return "entity type not found" or equivalent. There is no setup warning that the preference is off. Practitioners frequently spend hours debugging what appears to be a permission issue before discovering the preference is the root cause.
2. **condition.code silent failure on load** — FHIR specifies condition.code as 0..1 (optional). Health Cloud enforces it as required. If a middleware layer omits the code field and the load path is a batch API call without strict validation, the record may be partially written or fail silently depending on error handling. Always enforce a pre-load validation step that rejects code-less Condition resources before they reach the DML layer.
3. **careTeam member resolution on Person Account vs. User** — FHIR CareTeam members are practitioners (FHIR Practitioner resource). When resolving to Salesforce, some practitioners will have Salesforce User records; others may only have Contact records without User accounts. The Case Team member type differs between User and Contact. Middleware must handle both cases and cannot assume all practitioners are Salesforce Users — failing to do so silently omits team members without error.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| FHIR-to-HC mapping table | Field-level mapping from FHIR resource elements to Health Cloud SObject fields and child records |
| Load sequence plan | Ordered list of object loads with FK dependency notation |
| CodeableConcept truncation log | Audit file of codings discarded during the 15-coding limit enforcement |
| Quarantine list | Source FHIR resources rejected from load due to missing required fields (e.g., code-less Conditions) |

---

## Related Skills

- patient-data-migration — use alongside this skill when migrating patient records at scale from EHR systems; covers Bulk API load patterns and rollback strategies
- health-cloud-data-model — use for understanding the broader Health Cloud clinical object model beyond the five primary FHIR mappings
- consent-data-model-health — use when FHIR Consent resources are part of the integration bundle
