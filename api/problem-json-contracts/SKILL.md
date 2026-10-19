---
name: problem-json-contracts
description: "RFC 9457 problem+json error contracts for Ottili APIs: error catalogue, retry semantics, versioned schemas, and validators that fail on malformed or non-idempotent error responses. Use when designing an HTTP API endpoint that returns errors, adding an error code, or investigating 'client cannot parse the error' / 'retry loop hammered us' incidents."
license: MIT-compat
compatibility: "Any HTTP API; RFC 9457 (2023); JSON Schema draft 2020-12"
metadata: {}
allowed-tools: []
---

Standard: name/description/length rules — [agentskills.io standard](../references/agentskills-standard.md).
# Problem JSON Contracts Skill — Quick Reference (body <500 lines; full procedure in references/problem-procedure.md)

## When to use this skill (trigger)
Any of these fires it:
- Designing an HTTP API endpoint that returns errors.
- A migration adds a new error code or changes a field name in an error response.
- An incident report says "client cannot parse the error" or "retry loop hammered us".
- Code review mentions `{"error": "..."}` without type/instance/status fields.
- Adding a new language SDK and needing stable error shapes.

## Disambiguation
- Fires: designing or reviewing an HTTP API's >=400 responses, adding an error code, or
  investigating "client cannot parse the error" / "retry loop hammered us" incidents.
- Does NOT fire for: in-process module boundaries (use module-contract-first — that skill
  governs internal signatures and export snapshots, not HTTP envelopes); status reporting
  (use [honest-status](../honest-status/SKILL.md) — an unhandled error is a status item, but
  the *shape* of the error is this skill's job); or a success response (2xx), which this skill
  does not govern.

## When NOT to use this skill
- Internal CLI-only tools with no HTTP transport.
- Health-check endpoints that return plain text 200.
- A success response (2xx) — the skill governs the >=400 shape, not the happy path.
- An error that is logged but never returned to the client — that is a logging concern, not a problem-detail contract.
- A one-off script that emits one error shape and is never called again — still validate it, but the catalogue is overkill; use the schema only.

## Decision table — error shape
| Pattern | When to pick | Pitfall |
|---------|-------------|---------|
| RFC 9457 `application/problem+json` with type URI | Default for all public HTTP APIs | `type` must be an absolute URI; use `about:` or `urn:` for internal codes |
| Versioned JSON Schema (`$id` with version path) | Multiple client versions in the wild | Never break existing `$id`; add a new schema version instead |
| Error catalogue enum (machine code + human message) | Every error must be machine-searchable by ops | Do not put stack traces in the catalogue response; log separately |

## Decision table — retry strategy
| Error status | Retryable | `retry_after` | Client behaviour | Pitfall |
|-------------|-----------|---------------|------------------|---------|
| 429 Too Many Requests | yes | integer seconds | back off from `retry_after`, double on each failure | Missing `retry_after` → clients hammer |
| 503 Service Unavailable | yes | integer seconds | same as 429 | Transient; do not treat as permanent |
| 504 Gateway Timeout | yes | integer seconds | same; raise after 5 attempts | Timeout is often a timeout, not a fault |
| 4xx (other) | no | absent | surface immediately to the user | Retrying a 400 wastes a request |
| 5xx (other) | no | absent | surface with `trace_id` for support lookup | Do not retry blindly |

## Worked examples
Good (RFC 9457 shape, retriable, no internals):
```json
{ "type": "https://problems.ottili.one/rate-limit-exceeded",
  "title": "Rate limit exceeded",
  "status": 429,
  "detail": "60 requests per minute allowed; 120 received.",
  "instance": "/orders/abc123",
  "retry_after": 60,
  "trace_id": "req-9f3c" }
```
Bad (envelope — the #1 client-parse failure):
```json
{ "status": 404, "detail": "No user with id 42." }
```
Bad (5xx leakage — connection string in `detail`):
```json
{ "type": "about:ottili:db:connection", "status": 503,
  "detail": "connection refused at 10.0.0.5:5432", "trace_id": "abc" }
```
Bad (retry_after as HTTP-date — most clients ignore it):
```json
{ "type": ".../rate-limit-exceeded", "status": 429,
  "retry_after": "Wed, 21 Oct 2026 07:28:00 GMT" }
```

## Pitfalls from research
- Envelopes with a nested `status` are the #1 client-parse failure; `status` MUST equal the HTTP status code.
- `type` as a relative URI is unresolvable; public APIs use absolute URIs, internal services use `about:`.
- Stack traces and connection strings in `detail` on 5xx are a data-leak incident; use `trace_id` only.
- `retry_after` in HTTP-date format is ignored by most clients; always use integer seconds.
- Reusing one `type` URI for two different semantics conflates them; one type per meaning.

## Near-miss triggers (act before the incident)
- An endpoint returns a 200 envelope with a nested `status` → the #1 client-parse failure; reject envelopes.
- `type` is a bare string or a relative URI → clients cannot resolve it; require an absolute URI.
- A 5xx response leaks connection strings or SQL in `detail` → replace with `trace_id` only.
- `retry_after` is missing on 429/503 → clients hammer the server; emit seconds, never HTTP-date.
- Two catalogue entries share one `type` URI → silently conflates two semantics; one type per meaning.
- A catalogue code has no OpenAPI response entry → CI must fail (`scripts/check_problem_catalogue.py`).

## Verification checklist (all must pass before merge)
- [ ] Every endpoint returns `application/problem+json` on >=400
- [ ] Catalogue YAML has no duplicate codes
- [ ] Schema validates all examples in `references/examples/` (status field included)
- [ ] `retry_after` present on all retriable errors
- [ ] No internal fields leaked on 5xx responses
- [ ] `scripts/check_problem_catalogue.py` passes in CI

## Verification
- Run the offline gate: `python3 scripts/check_problem_catalogue.py --catalogue <cat> --openapi <spec> --schema-dir <dir>` — must exit 0.
- Run the RFC 9457 shape validator: `python3 scripts/validate_problem_examples.py --schema-dir references/examples/schemas --catalogue references/examples/catalogue.json` — must print OK.
- Run the catalogue checker against every fixture: `python3 scripts/check_problem_catalogue_test.py` — must print ok (1 good, 6 bad, 1 malformed).
- Run the standard validator: `python3 scripts/validate_skills.py` — must report OK.
- Full procedure, version table, worked examples, and pitfalls: `references/problem-procedure.md`.
- Eval prompts with expected behaviour and failure signs: `references/EVALS.md`.
- Primary sources with URLs and retrieval dates: `references/SOURCES.md`.

## Related skills
- [honest-status](../honest-status/SKILL.md) — an unhandled error is a status item; mark it VERIFIED only after the validator ran green.
- [long-test-discipline](../long-test-discipline/SKILL.md) — the validator and the schema self-test run in the foreground with a recorded seed.
- [shared-tree-git](../shared-tree-git/SKILL.md) — the catalogue and schema are committed with a task-id prefix.
