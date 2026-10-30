---
name: unsafe-api-consumption
description: Detects code that consumes third-party API responses without type validation
  or sanitization. Use when writing code that calls third-party APIs, parses
  responses from external services, or integrates with webhooks and callbacks
  from external systems. Also invoke when deserializing or acting on data
  received from partner or vendor APIs without validation.
---

# Unsafe API Consumption Check (API10:2023)

## What this checks

Protects against blindly trusting data from third-party APIs. External API responses
can be tampered with (via MITM, compromised provider, or supply-chain attack), contain
unexpected types or malicious payloads, or change without notice. Treating external
data as trusted leads to injection, deserialization attacks, and business logic bypass.

## Vulnerable patterns

- External API response fields flowing directly into SQL, shell, template, or code-execution sinks via string interpolation
- Rendering third-party HTML or markdown without a sanitization step
- Merging unvalidated external response objects into internal models
- Following redirect URLs returned by an external API without re-validating against the same allowlist
- Calling external APIs without size limits or timeouts, allowing a partner to stream gigabytes or hang the caller

## Fix immediately

Flag the vulnerable code, explain the risk, and suggest a fix establishing these
properties. Translate to the HTTP client, schema library, and template engine of the
audited file — use that stack's documented validation, sanitization, and redirect
controls; do not import a recipe from a different stack.

1. **Every response is validated against an explicit schema** — typed struct, schema validator, JSON Schema, protobuf message, or equivalent — before any field reaches business logic. Optional fields get defaults; unexpected fields are rejected or ignored, not silently propagated.
2. **External data never reaches injection sinks via string interpolation.** SQL goes through parameterized queries; HTML goes through an auto-escaping template engine; shell goes through argv arrays. Validation does not exempt the sink.
3. **Response size is bounded and the request has a timeout.** A partner API can stream gigabytes or hang forever; both eat resources and can DoS the caller.
4. **Redirects are not followed blindly.** Either disable redirects, or re-validate each hop against the same allowlist used for the initial URL. Partner-controlled 3xx responses can redirect to SSRF targets or attacker-controlled hosts.

## Verification

- [ ] Every response from an external API is validated against a schema before any field is used in queries, rendering, or business logic
- [ ] External API data never reaches SQL, shell, template, or code-execution sinks via string interpolation — only through parameterized/auto-escaping interfaces
- [ ] HTTP responses from external APIs are size-limited and the request has a timeout
- [ ] Redirects from external API responses are either disabled or re-validated at each hop against the same allowlist used for the initial URL

## References

- CWE-20 ([Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html))
- CWE-502 ([Deserialization of Untrusted Data](https://cwe.mitre.org/data/definitions/502.html))
- [OWASP API10:2023 Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/)
