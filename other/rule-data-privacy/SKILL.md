---
name: rule-data-privacy
description: MANDATORY when editing files matching ["api/src/**/*.py", "frontend/src/**/*.{ts,tsx}", "infra/**/*.tf"]. PII classification, redaction, retention, and FedRAMP-aligned data privacy controls
---

# Data Privacy Rules

## Classification

ALWAYS classify data at the column, field, and log level as one of: Public, Internal, Confidential, or PII. ALWAYS annotate SQLAlchemy columns that hold PII with a project-standard marker (comment or Enum) so auditing tools can flag them. NEVER introduce a new column that may contain PII without updating the data dictionary.

PII includes: legal names, SSN, date of birth, home address, personal phone, personal email, financial account numbers, application answers containing the above. Grants.gov-sourced applicant data MUST be treated as PII by default.

## Logging

NEVER log PII. ALWAYS reference records by opaque identifiers (UUIDs) in logs. When an error must include context, log the ID only and fetch the record separately for secure audit storage. See `api-logging.mdc`.

Correct:
```python
logger.info("Application submitted", extra={"application_id": app.application_id})
```

Incorrect:
```python
logger.info("Application submitted", extra={"email": user.email, "ssn": user.ssn})
```

## API Responses

ALWAYS minimize PII in API responses — return only the fields the caller is authorized for. ALWAYS enforce field-level authorization in service functions, not only in Marshmallow schemas. NEVER expose PII in list endpoints or search results beyond what the caller owns.

## Frontend Handling

NEVER store PII in `localStorage`, `sessionStorage`, cookies (other than session cookies), or URL query strings. NEVER include PII in analytics events, error tracking (e.g., Sentry) payloads, or client-side logs. ALWAYS scrub user input before sending to third-party services.

## Retention and Deletion

ALWAYS implement user-facing deletion as soft delete (`is_deleted = True`) with a scheduled hard-delete job that honors the retention policy. ALWAYS document retention windows per data category in the data dictionary. NEVER hard-delete audit records.

## Cross-Border & Third Parties

NEVER send PII to a third-party service unless it is in the FedRAMP Moderate boundary and documented in the SSP. ALWAYS route outbound data through approved adapters.

## Grants.gov Coexistence

ALWAYS treat data synchronized from Grants.gov as authoritative for applicants in scope of that system — do not mutate PII that originated there without an explicit bidirectional sync contract.

---

## Related Rules

- **`api-logging.mdc`** — redacted logging patterns
- **`security.mdc`** — encryption, secrets, authentication
- **`fedramp.md`** — FedRAMP Moderate control mappings
- **`api-database.mdc`** — column definitions and soft deletes
- **`cross-domain.mdc`** — structured logging and PII prohibitions

## Specialist Validation

**Simple (add non-PII field):** None.
**Moderate (new endpoint returning user data, new column):** Invoke `security-sentinel` and `codebase-conventions-reviewer`.
**Complex (new integration, new PII category, retention policy change):** Invoke `security-sentinel`, `architecture-strategist`, and `compliance-auditor` in parallel.
