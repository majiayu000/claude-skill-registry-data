---
name: health-cloud-apis
description: "Use this skill when working with Health Cloud APIs: querying healthcare-specific SObjects (CarePlan, ClinicalEncounter, HealthCondition) via standard SObject API, using the FHIR R4-aligned Healthcare API, handling FHIR bundle limits, and understanding API authentication differences between the two layers. NOT for generic REST API development or standard Salesforce SObject API patterns unrelated to Health Cloud clinical objects."
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
tags:
  - health-cloud
  - fhir-api
  - healthcare-api
  - clinical-objects
  - rest-api
  - bundle-limits
inputs:
  - Health Cloud org with FHIR R4 Support Settings enabled
  - Connected App with correct OAuth scopes for FHIR Healthcare API
  - Target clinical objects identified (CarePlan, ClinicalEncounter, HealthCondition, etc.)
outputs:
  - Correct API endpoint selection (SObject API vs. FHIR Healthcare API)
  - FHIR bundle request structure with correct size limits
  - Authentication configuration for Healthcare API OAuth scopes
  - HTTP 424 dependency failure handling pattern
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-10
---

# Health Cloud APIs

Use this skill when working with Health Cloud APIs: querying healthcare-specific SObjects via the standard SObject REST/SOAP API, using the FHIR R4-aligned Healthcare API for FHIR operations, handling FHIR bundle constraints, and understanding authentication and endpoint differences between the two API layers. This skill covers Health Cloud-specific API patterns. It does NOT cover generic REST API development, standard Salesforce SObject API patterns for non-Health Cloud objects, or platform API integration architecture.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm the FHIR-Aligned Clinical Data Model org preference is enabled in Setup > FHIR R4 Support Settings. FHIR R4-aligned objects are unavailable for API operations until this is enabled.
- Identify whether the operation requires the **standard SObject API** (for clinical SObjects like CarePlan, ClinicalEncounter, HealthCondition using standard REST/SOQL/SOAP patterns) or the **FHIR Healthcare API** (for FHIR R4-conformant operations using FHIR bundle structures).
- For FHIR Healthcare API calls: confirm the Connected App is configured with the `healthcare` OAuth scope (in addition to the standard `api` scope). FHIR Healthcare API rejects requests with only the standard `api` scope.
- Understand the FHIR bundle limits: maximum 30 entries per bundle, maximum 10 read/search operations per bundle. Failed dependent entries return HTTP 424 (Failed Dependency) rather than the individual entry error code.

---

## Core Concepts

### Two Distinct API Layers

Health Cloud exposes two API layers:

1. **Standard SObject API** — Healthcare-specific SObjects (CarePlan, ClinicalEncounter, HealthCondition, PatientImmunization, etc.) available via API v51.0+ are accessible through all standard Salesforce API mechanisms: REST, SOAP, Bulk API, SOQL. These are platform-standard objects with no special authentication or endpoint requirements. Access requires the HealthCloudICM permission set.

2. **FHIR R4-aligned Healthcare API** — A separate API layer that exposes seven FHIR R4 modules (Patient, Condition, Observation, etc.) via a dedicated FHIR endpoint. This API requires:
   - A different base URL: `/services/data/vXX.0/healthcare/fhir/R4/` instead of `/services/data/vXX.0/sobjects/`
   - The `healthcare` OAuth scope in addition to standard scopes
   - FHIR R4-aligned Clinical Data Model enabled in Setup

These two layers are not interchangeable. Using the standard SObject endpoint for FHIR operations or the FHIR endpoint for standard SOQL queries will fail.

### FHIR Bundle Limits

FHIR Healthcare API bundle requests have specific limits:
- **Maximum 30 entries per bundle** — bundles with more than 30 entries are rejected
- **Maximum 10 read/search operations per bundle** — bundles mixing reads/writes are limited to 10 read/search entries
- **HTTP 424 for dependent entry failures** — if a bundle entry fails and a later entry depends on it (via fullUrl reference), the dependent entry returns HTTP 424 (Failed Dependency) rather than propagating the original error code

These limits require chunking logic for bulk clinical data operations.

### FHIR vs. SObject Authentication

| Auth Requirement | Standard SObject API | FHIR Healthcare API |
|---|---|---|
| OAuth scope | `api` | `api` + `healthcare` |
| Base URL | `/services/data/vXX.0/sobjects/` | `/services/data/vXX.0/healthcare/fhir/R4/` |
| Access required | HealthCloudICM perm set | HealthCloudICM perm set + FHIR R4 perm |
| Experience Cloud | Standard EC user | FHIR R4 for Experience Cloud perm set |

---

## Common Patterns

### Querying Clinical SObjects via Standard REST API

**When to use:** Reading or writing clinical data (CarePlan goals, patient conditions, clinical encounters) using standard REST API patterns from an external integration.

**How it works:**
1. Use the standard REST SObject endpoint: `GET /services/data/v60.0/sobjects/HealthCondition/{id}`
2. For SOQL: `GET /services/data/v60.0/query?q=SELECT+Id,ConditionSeverity+FROM+HealthCondition+WHERE+PatientId='{patientId}'`
3. Ensure the integration user has the HealthCloudICM permission set assigned.
4. Use API v51.0 or later for all Health Cloud healthcare-specific objects.

**Why not the alternative:** The FHIR Healthcare API is needed for FHIR-conformant operations but adds complexity (bundle structures, special scopes, different error handling). For internal integrations that do not need FHIR R4 compliance, the standard SObject API is simpler and more performant.

### FHIR Bundle Read with Error Handling

**When to use:** Reading a patient's clinical data set via the FHIR Healthcare API in a FHIR-conformant response structure.

**How it works:**
1. Make a GET request to `/services/data/v60.0/healthcare/fhir/R4/Patient/{patientId}/$everything`
2. The response is a FHIR Bundle with up to 30 entries.
3. Check each bundle entry's `response.status` field. Failed entries have status 4xx or 5xx.
4. Dependent entries that reference a failed entry have `response.status = "424 Failed Dependency"`.
5. Process each entry independently and implement retry logic for 424 entries after fixing the root cause.

---

## Decision Guidance

| Situation | API Layer | Reason |
|---|---|---|
| SOQL query on clinical objects | Standard SObject API | Simpler, supports all SOQL features |
| FHIR-conformant read/write for interoperability | FHIR Healthcare API | Required for FHIR R4 compliance |
| Bulk load of clinical data | Standard Bulk API | Better throughput than FHIR bundle limits |
| External FHIR server reading Salesforce data | FHIR Healthcare API | Provides FHIR R4 bundle responses |
| Integration requires FHIR $everything operation | FHIR Healthcare API | Only available in FHIR layer |

---

## Recommended Workflow

1. **Confirm FHIR R4 prerequisites** — enable FHIR R4 Support Settings if not already done. Identify target API layer (standard SObject vs. FHIR Healthcare API) based on interoperability requirements.
2. **Configure Connected App** — for FHIR Healthcare API: add `healthcare` OAuth scope to the Connected App. For standard SObject API: standard `api` scope is sufficient.
3. **Assign required permission sets** — HealthCloudICM for all API users accessing clinical objects. FHIR R4 for Experience Cloud perm set if portal users need FHIR access.
4. **Implement bundle chunking** — for FHIR Healthcare API batch operations, implement request chunking at a maximum of 30 entries per bundle and 10 read/search operations per bundle.
5. **Handle HTTP 424 errors** — implement dependent entry error detection: identify which bundle entry failed and process dependent entries separately after fixing the root failure.
6. **Test with representative data volume** — FHIR bundle limits become apparent only at production data volumes. Test with real bundle sizes before go-live.

---

## Review Checklist

- [ ] FHIR R4 Support Settings enabled (if using FHIR Healthcare API)
- [ ] Connected App has `healthcare` OAuth scope (if using FHIR Healthcare API)
- [ ] HealthCloudICM permission set assigned to all API users
- [ ] Bundle size chunking implemented (max 30 entries, max 10 reads per bundle)
- [ ] HTTP 424 dependent entry error handling implemented
- [ ] API version is v51.0+ for all Health Cloud SObjects

---

## Salesforce-Specific Gotchas

1. **FHIR Healthcare API and standard SObject API use different base URLs** — Calls to healthcare-specific objects via the standard SObject endpoint return the object data as plain SObject JSON. FHIR Healthcare API calls require the `/healthcare/fhir/R4/` path and return FHIR bundle structures. Using the wrong endpoint returns unexpected response formats, not an error.

2. **FHIR bundle failures use HTTP 424 for dependent entries** — When a bundle entry fails, all subsequent entries that reference the failed entry via fullUrl return HTTP 424 rather than the original error code. Code that checks only for 2xx/4xx status may misinterpret 424 as a different error. Always check for 424 specifically and trace back to the root failed entry.

3. **`healthcare` OAuth scope required for FHIR Healthcare API** — A Connected App with only the standard `api` scope cannot call the FHIR Healthcare API endpoints. The request returns a 403 Forbidden. Add the `healthcare` scope explicitly to the Connected App configuration.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| API endpoint selection matrix | Table mapping clinical operations to the correct API layer (SObject vs. FHIR) |
| Connected App configuration | OAuth scope requirements for each API layer |
| Bundle chunking implementation | Logic for splitting operations into correctly-sized FHIR bundles |
| Error handling pattern | HTTP 424 detection and dependent entry retry pattern |

---

## Related Skills

- apex/fhir-integration-patterns — FHIR R4 integration patterns including CDS Hooks and SMART on FHIR
- admin/clinical-data-requirements — FHIR R4 object activation and data model requirements
- admin/health-cloud-data-model — Health Cloud object reference
