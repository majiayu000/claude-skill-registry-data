---
name: health-cloud-apis
description: "Use this skill when working with Health Cloud APIs: querying healthcare-specific SObjects (CarePlan, ClinicalEncounter, HealthCondition) via the standard SObject API, calling the Health Cloud Business APIs under /connect/health, using the FHIR R4 Salesforce Healthcare API, handling FHIR bundle limits, and the authentication differences between those layers. NOT for choosing or enabling the clinical objects — use data/health-cloud-data-model. NOT for EHR integration design, CDS Hooks, or SMART on FHIR — use apex/fhir-integration-patterns."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Performance
triggers:
  - "How do I call the Salesforce FHIR Healthcare API to read or write Health Cloud clinical data?"
  - "What is the difference between the standard SObject API and the Health Cloud FHIR Healthcare API?"
  - "FHIR bundle request failing with HTTP 424 for dependent entries in Health Cloud API"
  - "Health Cloud FHIR API bundle capped at 30 entries and max 10 read/search requests"
  - "What authentication scope is required for Health Cloud FHIR Healthcare API calls?"
  - "call the Health Cloud medication statement Connect API from an integration"
  - "set up OAuth custom scopes for the Salesforce Healthcare API"
tags:
  - health-cloud
  - fhir-api
  - healthcare-api
  - clinical-objects
  - rest-api
  - bundle-limits
inputs:
  - Health Cloud org with FHIR R4 Support Settings enabled
  - External client app with the OAuth custom scopes the Healthcare API resources require
  - Target clinical objects identified (CarePlan, ClinicalEncounter, HealthCondition, etc.)
outputs:
  - Correct API layer selection (SObject API vs. Business API vs. Healthcare API)
  - FHIR bundle request structure with correct size limits
  - OAuth custom scope configuration for Healthcare API resources
  - HTTP 424 dependency failure handling pattern
dependencies: []
version: 1.0.1
author: Pranav Nagrecha
updated: 2026-10-03
---

# Health Cloud APIs

Use this skill when an integration reads or writes Health Cloud (now branded Agentforce Health) data and must pick the right API surface: the standard SObject API on the clinical data model, the Health Cloud Business APIs that wrap multi-step business logic, or the FHIR R4 Salesforce Healthcare API for interoperability. Generic REST API patterns for non-health objects belong to `integration/rest-api-patterns`.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm the FHIR-Aligned Clinical Data Model org preference is enabled in Setup > FHIR R4 Support Settings. Many clinical objects (AllergyIntolerance, ClinicalEncounter, and others) are unavailable until it is on.
- Identify the consumer: an internal integration that wants records (standard SObject API), a workflow that needs a business operation such as enrolling a patient or recording a medication statement (Business APIs), or an external FHIR client that needs FHIR R4 resources (Healthcare API).
- For the Healthcare API: confirm the org accepted the Industry APIs terms, holds the Salesforce Healthcare API SKU, and has an external client app with the OAuth custom scopes for each resource plus the `refresh_token` scope.
- Know the bundle limits before designing batch writes: up to 30 entries per Bundle call, of which up to 10 can be read or search requests, and only Bundle type `batch` is supported.

---

## Questions to Ask Before Configuring

| Question | Why it matters | What a good answer adds | What proper configuration adds over just doing it |
|---|---|---|---|
| "Does the consumer need FHIR R4 resources, Salesforce records, or a business operation?" | The three layers use different hosts, payloads, and auth | The API layer per use case | No FHIR plumbing where plain records would do, and no record-level code where a Business API already enforces the process |
| "Which FHIR resources, and read or write, per consumer?" | Each Healthcare API resource and method maps to its own custom scope, such as `system_condition_read` or `user_carePlan_write` | The exact custom scope list for the external client app | Least-privilege tokens instead of `system_all_write` everywhere |
| "Which region and environment hosts the org: US, EU, CA, or AU, production or sandbox?" | The Healthcare API domain differs per region, and sandboxes use the `/sandBox/` path | The base URL per environment | Calls that reach the right data center on the first try |
| "How many records per run, and how many parallel callers?" | Bundles cap at 30 entries; Salesforce recommends at most five concurrent Healthcare API requests per org | A chunk size and a concurrency cap | A load that completes instead of failing under throttling |
| "Who owns code validity: does the source system send correct CPT, SNOMED, or LOINC codes?" | The Healthcare API does not do FHIR semantic (code set) validation | A named upstream owner for code quality | Clean clinical data instead of silently stored invalid codes |
| "Is the FHIR R4 data model already enabled, and which permission sets do integration and portal users hold?" | Objects are hidden until the org preference is on; Experience Cloud users need the FHIR R4 for Experience Cloud Sites permission set | A prerequisite checklist signed off before build | No late 404s or "not supported" errors in UAT |

What a proper configuration adds over "just calling the endpoint": each consumer uses the layer that fits it, tokens carry only the scopes their resources need, bundles are sized and retried by dependency, and code-set quality has an owner because the platform will not check it.

---

## Core Concepts

### Three API Layers

| Layer | Endpoint shape | Auth | Use for |
|---|---|---|---|
| **Standard SObject API** | `https://{MyDomain}.my.salesforce.com/services/data/vXX.X/sobjects/HealthCondition/{id}` and `/query` | Standard OAuth access token for the org | Internal integrations, reporting, bulk loads on clinical objects (API 51.0+ for objects such as HealthCondition and ClinicalEncounter) |
| **Health Cloud Business APIs** | `https://{MyDomain}.my.salesforce.com/services/data/vXX.X/connect/health/...`, for example `/connect/health/clinical/patients/{patientId}/medication-statement` | Standard OAuth access token; follows Connect REST API conventions | Business operations that touch several objects in one call (care program enrollment, medication statements, appointments, referrals); some also exist as Apex, such as `HealthCloudGA.PatientService.createPatient` |
| **Salesforce Healthcare API (FHIR R4)** | `https://api.healthcloud.salesforce.com/{FHIR module}/fhir-r4/v1/{Resource}`, for example `.../clinical-summary/fhir-r4/v1/Condition`; regional hosts `eu.`, `ca.`, `au.`; sandboxes add `/sandBox/` after the host | External client app with OAuth custom scopes per resource, plus `refresh_token` | FHIR R4 interoperability with EHRs, payers, and other FHIR systems |

An earlier version of this skill placed the Healthcare API under `/services/data/vXX.0/healthcare/fhir/R4/` on the org instance and required an OAuth scope named `healthcare`. Neither appears in the Salesforce Healthcare API guide; see [`references/gotchas.md`](references/gotchas.md) Gotchas 1 and 2.

### Healthcare API Modules and Resources

| Module (URL segment) | Resources |
|---|---|
| Administration (`admin`) | Patient, Practitioner, PractitionerRole, Encounter, Organization, Location, RelatedPerson |
| Bundle (`bundle`) | Bundle (type `batch` only) |
| Care Management (`care_management`) | CarePlan, Goal |
| Clinical Diagnostics (`clinical-diagnostics`) | DiagnosticReport, DocumentReference, Observation |
| Clinical Summary (`clinical-summary`) | AllergyIntolerance, Condition, Procedure |
| Clinical Workflow (`clinical-workflow`) | ServiceRequest, MedicationRequest |
| Medications (`clinical-medications`) | Medication, Immunization, MedicationStatement |
| Forms (`forms`) | Questionnaire, QuestionnaireResponse |
| Prior Authorization (`prior-auth`) | Claim and prior authorization resources |

### FHIR Bundle Limits

- Up to **30 entries** in a single Bundle call; up to **10** of them can be read or search requests.
- Only Bundle type **`batch`** is supported. There is no all-or-nothing `transaction` bundle.
- Entries can depend on each other through `urn:uuid:` placeholders in `fullUrl` and references. When a dependent action meets an error, the API cancels the dependent requests and returns **HTTP 424** for them.
- Deeper dependency chains increase response time; the documented typical response time is about 3 seconds per call.

---

## Common Patterns

### Querying Clinical SObjects via Standard REST API

**When to use:** Reading or writing clinical records from an internal integration that does not need FHIR R4 conformance.

**How it works:**
1. Use the SObject endpoint: `GET /services/data/v67.0/sobjects/HealthCondition/{id}`.
2. For SOQL: `GET /services/data/v67.0/query?q=SELECT+Id,ConditionSeverity+FROM+HealthCondition+WHERE+PatientId='{patientId}'`.
3. Give the integration user the Health Cloud permission set licenses and object permissions the data model requires; the developer guide names the Health Cloud and Health Cloud Platform permission set licenses for several data models. UNVERIFIED (2026-10-03): an earlier version of this skill required a `HealthCloudICM` permission set for every API user; the Summer '26 developer guide does not name it.
4. Use API 51.0 or later for the FHIR-aligned clinical objects.

**Why not the alternative:** The Healthcare API adds custom scopes, regional hosts, and bundle semantics. Internal consumers that want records do not need any of that.

### FHIR Read and Batch Write With Dependency Handling

**When to use:** An external FHIR client reads or writes clinical data in FHIR R4 form.

**How it works:**
1. Call a resource directly, for example `GET https://api.healthcloud.salesforce.com/clinical-summary/fhir-r4/v1/Condition` with a bearer token that carries `system_condition_read` (or a broader read scope).
2. For writes of related resources, send a `batch` Bundle of at most 30 entries, linking entries with `urn:uuid:` placeholders.
3. Read every entry's response status. Entries that returned 424 depend on an entry that failed.
4. Fix the root failure and resend only the failed root plus its dependents.

Worked request bodies and the custom scope metadata are in [`references/healthcare-api-examples.md`](references/healthcare-api-examples.md).

---

## Decision Guidance

| Situation | API Layer | Reason |
|---|---|---|
| SOQL query on clinical objects | Standard SObject API | Supports all SOQL features |
| Record a medication statement or enroll a patient with business rules applied | Business API (`/connect/health/...`) | One call wraps the multi-object logic |
| FHIR-conformant read/write for interoperability | Healthcare API | FHIR R4 resource shapes |
| Bulk load of clinical data | Bulk API 2.0 on the SObjects | Bundles cap at 30 entries and five concurrent requests are recommended |
| External FHIR server reading Salesforce data | Healthcare API | Returns FHIR R4 resources |

---

## Recommended Workflow

1. **Confirm prerequisites:** FHIR-Aligned Clinical Data Model org preference on; for the Healthcare API, Industry APIs terms accepted and the Healthcare API SKU present.
2. **Choose the layer per consumer** using the Decision Guidance table; record the base URL per environment (region and sandbox path for the Healthcare API).
3. **Configure auth:** for the Healthcare API, create the OAuth custom scopes the resources need, assign them and `refresh_token` to the external client app, and pick the OAuth flow; for the other two layers, a standard org access token is enough.
4. **Assign access:** permission set licenses and object permissions for the integration user; the FHIR R4 for Experience Cloud Sites permission set for community users who touch clinical objects.
5. **Build bundles and retries:** chunk at 30 entries with at most 10 reads, cap concurrency at five, and resolve 424 entries back to their root failure.
6. **Run the checker:** `python3 skills/apex/health-cloud-apis/scripts/check_health_cloud_apis.py --manifest-dir <project>` and fix every ERROR before UAT.

---

## Review Checklist

- [ ] FHIR R4 Support Settings: FHIR-Aligned Clinical Data Model enabled
- [ ] Healthcare API base URL matches region and environment (`/sandBox/` for sandboxes)
- [ ] External client app has the resource-specific custom scopes and `refresh_token`; no invented `healthcare` scope
- [ ] Bundles use type `batch`, at most 30 entries, at most 10 read/search entries
- [ ] HTTP 424 handling traces dependents to their root entry
- [ ] Concurrency to the Healthcare API capped at five
- [ ] Source system owns FHIR code-set validity

---

## Salesforce-Specific Gotchas

One-line summaries; the full entries are in [`references/gotchas.md`](references/gotchas.md).

| Gotcha | Short form |
|---|---|
| Wrong host | The Healthcare API is on `api.healthcloud.salesforce.com` (regional variants), not under `/services/data` |
| Scopes | Resource-level custom scopes such as `user_condition_read`; `refresh_token` is required on the app |
| Bundles | `batch` only, 30 entries, 10 reads, 424 for dependents of a failed entry |
| Validation | No FHIR semantic (code set) validation |
| Concurrency | Keep to five concurrent requests per org |

---

## Output Artifacts

| Artifact | Description |
|---|---|
| API layer selection matrix | Each consumer mapped to SObject API, Business API, or Healthcare API |
| Custom scope plan | Resource and method to custom scope mapping, with the `OauthCustomScope` metadata |
| Bundle chunking implementation | Logic for 30-entry `batch` bundles with at most 10 reads |
| Error handling pattern | 424 dependency tracing and partial resend |

---

## Related Skills

- apex/fhir-integration-patterns — FHIR R4 integration patterns including CDS Hooks and SMART on FHIR
- admin/clinical-data-requirements — FHIR R4 object activation and data model requirements
- admin/health-cloud-data-model — Health Cloud object reference
