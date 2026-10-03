---
name: api-security-automation
description: API security automation skill for REST, GraphQL, gRPC, and WebSocket APIs. Covers OpenAPI/AsyncAPI ingestion, authenticated fuzzing, OWASP API Top 10 (BOLA, BFLA, mass assignment, SSRF), schema diffing, GraphQL introspection abuse, JWT and OAuth misuse, rate-limit and replay testing. Use to automate API assessments with safe, scoped, evidence-backed findings.
---

# API Security Automation

## Authorization Boundary

- Require base URL, environment label (lab/staging/prod), scoped credentials, and rate ceiling.
- Avoid production write endpoints unless explicitly authorized; prefer idempotent or staging traffic.
- Strip tokens and PII from artifacts.

## Testing Workflow

1. Ingest spec: OpenAPI, GraphQL SDL, gRPC `.proto`, Postman collection, HAR; otherwise crawl with `katana`/`hetty`.
2. Build a request matrix per endpoint × role × parameter class (id, enum, nested object, file).
3. Auth tests: token tampering, alg=none, kid confusion, audience swap, refresh replay, scope downgrade.
4. Object-level auth: enumerate IDs across roles to detect BOLA/IDOR.
5. Function-level auth: invoke admin/owner endpoints with low-privilege tokens.
6. Mass assignment: inject unexpected fields; observe persisted state changes.
7. Input handling: type confusion, prototype pollution, SSRF via URL params, path traversal, deserialization.
8. GraphQL: introspection, alias-based rate bypass, batched queries, depth/complexity DoS.
9. Rate and replay: nonce reuse, idempotency-key collisions, race conditions on state.

## Tooling

- `ffuf`, `wfuzz`, `nuclei` (api templates), `kiterunner`, `mitmproxy`, `hetty`, `graphql-cop`, `clairvoyance`, `jwt_tool`, `restler`, `schemathesis`.

## Output Contract

- `spec/`: normalized spec snapshot.
- `requests/`: replayable HAR per finding.
- `findings.jsonl`: `{endpoint, method, role, class, severity, evidence, cwe, remediation}`.
- `report.md`: business impact, top fixes, regression tests as CI hooks.
