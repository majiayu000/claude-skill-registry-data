---
name: bulk-api-patterns
description: "Use when implementing Bulk API 2.0 REST calls, choosing between Bulk API 2.0 and legacy Bulk API v1, handling CSV format requirements for bulk ingest, paginating query job results with locators, or constructing multipart job requests. Triggers: bulk api 2.0 endpoint, ingest job REST call, query job locator, bulk CSV format, hard delete bulk, v1 vs v2 bulk api. NOT for Data Loader UI steps (use data-import-and-management), NOT for strategic load-size decisions or concurrency mode selection (use bulk-api-and-large-data-loads)."
category: data
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Scalability
  - Reliability
triggers:
  - "How do I make the actual REST API calls to create and run a Bulk API 2.0 ingest job?"
  - "What CSV format does Bulk API 2.0 require — headers, line endings, encoding, delimiter?"
  - "How do I paginate through query job results using the Sforce-Locator header?"
  - "What is the difference between Bulk API 2.0 and legacy Bulk API v1 — when should I use each?"
  - "How do I perform a hard delete with Bulk API to bypass the Recycle Bin?"
tags:
  - bulk-api
  - bulk-api-2
  - data-loading
  - async
  - rest-api
  - csv
inputs:
  - Operation type (insert, update, upsert, delete, hardDelete, query)
  - Object API name
  - External ID field name (upsert only)
  - CSV data file or SOQL query string
  - Target API version
outputs:
  - REST endpoint call sequence for ingest or query jobs
  - CSV format specification for the upload
  - Job state polling pattern
  - Result retrieval pattern (successfulResults, failedResults, unprocessedRecords)
  - Locator-based pagination pattern for query results
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# Bulk API Patterns

This skill activates when a practitioner needs to implement the actual REST API calls for Bulk API 2.0 ingest or query jobs, understand CSV format requirements, paginate through large query results, or choose between Bulk API 2.0 and legacy Bulk API v1. It covers the endpoint-level mechanics of bulk operations. It does not cover Data Loader UI steps or the strategic decision of when to use Bulk API vs. REST Composite — see related skills for those.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Which API version are you targeting?** Bulk API 2.0 is REST-based, uses OAuth 2.0 bearer tokens, and requires no WSDL. Legacy Bulk API v1 uses SOAP-based session tokens and requires WSDL knowledge. Prefer v2.0 for all new implementations unless a specific v1 capability is required (e.g., serial concurrency mode, XML/JSON content types, binary attachments for Document/ContentVersion).
- **Most common wrong assumption.** Developers assume `concurrencyMode: Parallel` in Bulk API 2.0 is a meaningful configuration choice. It is not — Bulk API 2.0 only supports parallel mode, and the `concurrencyMode` field is reserved for future use. Serial mode is exclusively a Bulk API v1 feature.
- **Key constraints in play.** Each upload request to a Bulk API 2.0 ingest job must not exceed 150 MB after base64 encoding (approximately 100 MB of raw CSV per PUT). Salesforce automatically creates one internal batch per 10,000 records, up to a daily maximum of 150,000,000 records per org. A multipart job creation request handles datasets up to 100,000 characters and auto-completes the upload step.

---

## Core Concepts

### Bulk API 2.0 vs. Legacy Bulk API v1

Bulk API 2.0 (released in API version 41.0 / Winter '18) is the current recommended API for all new bulk operations.

| Feature | Bulk API 2.0 | Bulk API v1 |
|---|---|---|
| Protocol | REST (no WSDL) | SOAP (requires WSDL) |
| Authentication | OAuth 2.0 bearer token | Session ID via SOAP login |
| Content types | CSV only | CSV, XML, JSON, binary attachments |
| Batching | Automatic (10,000 records/batch) | Manual (developer creates batches) |
| Concurrency modes | Parallel only (serial not available) | Parallel and Serial |
| Query PK chunking | Automatic | Manual invocation required |
| Result endpoints | Unified: successfulResults, failedResults, unprocessedRecords | Per-batch result retrieval |
| Multipart create | Supported (single-call create + upload) | Not supported |

Use Bulk API v1 only when: (1) serial concurrency mode is required to prevent lock contention and Bulk API 2.0 batching cannot be reorganized to avoid it, or (2) the data format is XML/JSON or includes binary attachment fields (Document, ContentVersion Attachment).

### Ingest Job Lifecycle

Every Bulk API 2.0 ingest job follows a strict state machine:

1. **Open** — Job created via `POST /jobs/ingest/`. Accepts CSV data uploads.
2. **UploadComplete** — Caller sends `PATCH /jobs/ingest/{jobId}` with `{"state": "UploadComplete"}`. This is mandatory — Salesforce will not begin processing without it. A multipart job creation request bypasses this step by transitioning automatically.
3. **InProgress** — Salesforce auto-creates internal batches (one per 10,000 records) and processes them asynchronously.
4. **JobComplete** — All internal batches have been attempted. Individual records may still have failed — this state means processing is done, not that all records succeeded.
5. **Failed** — Salesforce could not complete the job (repeated batch timeouts after 20 retries per batch).
6. **Aborted** — Job manually canceled by the creator or a user with the Manage Data Integrations permission.

After reaching `JobComplete`, `Failed`, or `Aborted`, retrieve results from three separate endpoints:
- `GET .../successfulResults/` — records written successfully, with `sf__Id` and `sf__Created` columns.
- `GET .../failedResults/` — records that failed at the record level, with `sf__Error` column describing the cause.
- `GET .../unprocessedRecords/` — records never attempted (batch-level timeout or job aborted).

### CSV Format Requirements

Bulk API 2.0 ingest jobs accept CSV data only. The format must conform to these requirements:

- **Encoding:** UTF-8.
- **Line endings:** Specified at job creation time using the `lineEnding` field. Values: `LF` (default, Unix/macOS) or `CRLF` (Windows/DOS). Mismatch between the declared `lineEnding` and the actual file causes parse errors.
- **Column delimiter:** Default is `COMMA`. Alternatives: `BACKQUOTE`, `CARET`, `PIPE`, `SEMICOLON`, `TAB`. Declared at job creation via `columnDelimiter`.
- **First row:** Column headers matching Salesforce field API names. Relationship fields use dot notation: `Account.Name`, `Owner.Email`.
- **Null values:** To null out a field, use `#N/A` as the cell value.
- **Boolean fields:** Use `true` / `false` (case-insensitive).
- **Date/time fields:** ISO 8601 format: `2024-01-15T10:30:00.000Z`.

### Query Job and Locator Pagination

Query jobs return results as paginated CSV. The result set is not available as a single download for large queries.

Pagination pattern:
1. `GET .../jobs/query/{jobId}/results` — returns the first page of results (up to 50,000 records by default) and a `Sforce-Locator` response header.
2. If `Sforce-Locator` is not `null`, there are more pages. Use the locator value in the next request: `GET .../results?locator={locatorValue}`.
3. Repeat until `Sforce-Locator` is `null`.
4. The `maxRecords` query parameter controls page size (default: 50,000; max: 50,000).

The locator value is stable for the lifetime of the job. You can retrieve pages out of order or re-fetch a page using its locator. Bulk API 2.0 query jobs also automatically apply PK chunking for large queries, splitting the query into sub-queries by primary key range.

---

## Common Patterns

### Pattern 1: Standard Ingest Job — Create, Upload, Signal, Poll, Retrieve

**When to use:** Any insert, update, upsert, delete, or hardDelete operation on >2,000 records using a pre-built CSV file.

**How it works:**

```
Step 1 — Create the job
POST /services/data/v66.0/jobs/ingest/
Authorization: Bearer {token}
Content-Type: application/json

{
  "object": "Account",
  "operation": "insert",
  "contentType": "CSV",
  "lineEnding": "LF"
}

Response: { "id": "{jobId}", "state": "Open", "contentUrl": "..." }

Step 2 — Upload CSV data (repeat for each chunk, max 150 MB base64 per request)
PUT /services/data/v66.0/jobs/ingest/{jobId}/batches
Authorization: Bearer {token}
Content-Type: text/csv

Name,Industry,Phone
Acme Corp,Technology,415-555-0100
...

Step 3 — Signal upload complete (MANDATORY — job never starts without this)
PATCH /services/data/v66.0/jobs/ingest/{jobId}
Content-Type: application/json

{ "state": "UploadComplete" }

Step 4 — Poll until terminal state
GET /services/data/v66.0/jobs/ingest/{jobId}
(Poll every 15–30 seconds; stop when state is JobComplete, Failed, or Aborted)

Step 5 — Retrieve all three result endpoints
GET /services/data/v66.0/jobs/ingest/{jobId}/successfulResults/
GET /services/data/v66.0/jobs/ingest/{jobId}/failedResults/
GET /services/data/v66.0/jobs/ingest/{jobId}/unprocessedRecords/

Integrity check: count(successful) + count(failed) + count(unprocessed) == total uploaded records
```

**Why not synchronous REST:** Synchronous REST Composite maxes at 25 sub-requests per call. At 2,000+ records the call volume hits API limits and response times become unacceptable. Bulk API 2.0 offloads processing to Salesforce's async infrastructure.

### Pattern 2: Multipart Job Creation (Small Datasets)

**When to use:** Datasets up to 100,000 characters of CSV where you want to create the job and upload data in a single HTTP call, and avoid the manual `UploadComplete` PATCH.

**How it works:**

```
POST /services/data/v66.0/jobs/ingest/
Content-Type: multipart/form-data; boundary="BOUNDARY"
Authorization: Bearer {token}

--BOUNDARY
Content-Disposition: form-data; name="job"
Content-Type: application/json; charset=UTF-8

{
  "object": "Contact",
  "operation": "upsert",
  "externalIdFieldName": "Integration_Id__c",
  "contentType": "CSV",
  "lineEnding": "LF"
}
--BOUNDARY
Content-Disposition: form-data; name="content"
Content-Type: text/csv

FirstName,LastName,Integration_Id__c
Jane,Smith,EXT-001
...
--BOUNDARY--
```

A multipart job transitions directly to `UploadComplete` state on creation. No separate PATCH is required. Poll and retrieve results the same way as the standard pattern.

### Pattern 3: Query Job with Locator Pagination

**When to use:** Extracting large record sets (>50,000 records, or any query that would time out synchronously).

**How it works:**

```
Step 1 — Create query job
POST /services/data/v66.0/jobs/query
{
  "operation": "query",
  "query": "SELECT Id, Name, Industry FROM Account WHERE CreatedDate > 2024-01-01T00:00:00Z"
}

Step 2 — Poll until JobComplete
GET /services/data/v66.0/jobs/query/{jobId}

Step 3 — Retrieve first page of results
GET /services/data/v66.0/jobs/query/{jobId}/results
Response headers include: Sforce-Locator: MTAwMDA

Step 4 — Retrieve subsequent pages while Sforce-Locator != "null"
GET /services/data/v66.0/jobs/query/{jobId}/results?locator=MTAwMDA
GET /services/data/v66.0/jobs/query/{jobId}/results?locator=MjAwMDAw
...
(Continue until Sforce-Locator header is the literal string "null")
```

Use `maxRecords` parameter to control page size (up to 50,000 per page). The locator value is stable — safe to save and resume if the download is interrupted.

### Pattern 4: Hard Delete

**When to use:** Permanently removing records without leaving them in the Recycle Bin — typically for compliance/data purging or when Recycle Bin bloat causes query degradation.

**Requirements:** The running user must have the "Bulk API Hard Delete" permission (or System Administrator profile). This permission is separate from standard delete permission.

**How it works:** Use operation `hardDelete` instead of `delete` in the job creation body. All other steps in the standard ingest pattern are identical. Records bypassed from the Recycle Bin cannot be recovered via standard Recycle Bin restore — ensure data is verified before submitting a hardDelete job.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| New bulk implementation, any volume | Bulk API 2.0 | Simpler, no WSDL, auto-batching, unified results |
| Serial concurrency required | Bulk API v1 with concurrencyMode: Serial | v2.0 only supports parallel; serial is v1-only |
| Binary attachment fields (ContentVersion) | Bulk API v1 with ZIP content type | v2.0 supports CSV only |
| Dataset < 100,000 characters | Multipart job creation | Single HTTP call; auto-completes UploadComplete |
| Large extract (>50,000 records) | Query job with locator pagination | Auto PK chunking; stable paginated results |
| Permanent deletion, no Recycle Bin | hardDelete operation | delete soft-deletes; hardDelete removes permanently |
| Upsert with external ID | Bulk API 2.0 ingest, upsert operation | Handles insert + update in one pass; specify externalIdFieldName |
| XML/JSON data format required | Bulk API v1 | v2.0 accepts CSV only |

---


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] API version confirmed — Bulk API 2.0 for new implementations, v1 only when serial mode or non-CSV format is required
- [ ] `lineEnding` field in job creation matches the actual line endings in the CSV file (LF vs CRLF)
- [ ] `columnDelimiter` declared if not using the default COMMA
- [ ] Upload chunk size stays under 150 MB after base64 encoding (approximately 100 MB raw CSV)
- [ ] `UploadComplete` PATCH is sent (or multipart creation used) — job remains in Open state indefinitely without it
- [ ] Poll loop handles all three terminal states: `JobComplete`, `Failed`, `Aborted`
- [ ] All three result endpoints retrieved after every job: `successfulResults`, `failedResults`, `unprocessedRecords`
- [ ] Integrity check performed: record counts across three endpoints sum to total uploaded
- [ ] For query jobs: locator pagination loop terminates when `Sforce-Locator` header value is the literal string `"null"`
- [ ] `hardDelete` permission verified on running user before submitting hardDelete jobs

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **`concurrencyMode: Parallel` in v2.0 is a no-op — serial mode is not available** — The `concurrencyMode` field appears in Bulk API 2.0 job creation and always returns `Parallel`. It is reserved for future use only. If you need serial processing to avoid lock contention, you must use legacy Bulk API v1. Attempting to pass `concurrencyMode: Serial` in a v2.0 request either returns an error or is silently ignored, depending on API version.

2. **Multipart job auto-completes UploadComplete — do NOT send a second PATCH** — When you create a job via the multipart endpoint, the job transitions directly from creation to `UploadComplete`. Sending a redundant `PATCH {"state": "UploadComplete"}` after a multipart creation will return an error because the job is already past the `Open` state. Check the `state` field in the creation response before deciding whether to send the PATCH.

3. **`Sforce-Locator: null` is a string, not JSON null — comparison must be string equality** — When paginating query results, the `Sforce-Locator` response header contains the literal string `"null"` (not a JSON null, not an empty string, not absence of the header) to signal the last page. Code that checks `if locator is None` or `if not locator` will fail to detect the last page and loop indefinitely. Use `if locator == "null"` or `if locator.strip() == "null"`.

4. **`#N/A` is the only way to null a field in CSV — empty string sets an empty value, not null** — In Bulk API 2.0 CSV uploads, leaving a cell empty (`,,`) sets the field to an empty string for text fields, which is not the same as null and will fail required-field validation for non-text fields. To explicitly clear a field to null, use the value `#N/A` in that cell. This is a common source of upsert failures when migrating records with intentionally blank fields.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Ingest job REST call sequence | Step-by-step HTTP calls for create, upload, signal, poll, and result retrieval |
| CSV format specification | Encoding, line ending, delimiter, null value, and header row requirements |
| Query job pagination pattern | Locator-based loop to exhaust all result pages |
| API version selection rationale | v2.0 vs v1 decision with justification for the chosen approach |

---

## Related Skills

- data/bulk-api-and-large-data-loads — for strategic decisions on when to use Bulk API, record volume thresholds, concurrency mode selection, and failed-record retry strategy
- data/data-migration-planning — for end-to-end migration planning including pre-load validation and post-load verification
- data/soql-query-optimization — for optimizing the SOQL query used in a query job to minimize processing time
- admin/data-import-and-management — for Data Loader UI steps and declarative import tooling
