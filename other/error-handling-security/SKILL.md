---
id: error-handling-security
version: "2.0.0"
title: "Error-Handling Security"
description: "Decide what an error tells the client and what stays server-side: no stack traces, SQL, or paths in responses, no silent suppression, and no distinction between outcomes that would reveal protected state. Use when generating HTTP, GraphQL, or RPC error handlers, exception, panic, or rescue blocks, or configuring production error pages."
category: prevention
severity: medium
applies_to:
  - "when generating HTTP / GraphQL / RPC error handlers"
  - "when generating exception / panic / rescue blocks"
  - "when configuring production error pages or an exception handler pipeline"
languages: ["*"]
token_budget:
  minimal: 760
  compact: 1100
  full: 1500
rules_path: "rules/"
related_skills: ["api-security", "auth-security", "logging-security"]
last_updated: "2026-08-12"
sources:
  - "OWASP Error Handling Cheat Sheet"
  - "RFC 9457 — Problem Details for HTTP APIs"
  - "CWE-209 — Generation of Error Message Containing Sensitive Information"
  - "CWE-755 — Improper Handling of Exceptional Conditions"
---

# Error-Handling Security

## Rules (for AI agents)

### ALWAYS
- Catch exceptions at the boundary — HTTP handler, RPC method, message consumer —
  and decide *there* what crosses to the client and what stays server-side. Record
  the failure with a correlation ID under `logging-security`'s policy; do not bypass
  its redaction rules to attach "full context", which is how request bodies, cookies
  and tokens end up in logs.
- Put only client-actionable information in an external error: a stable error code, a
  short human-readable message, and the correlation ID. Anything the caller cannot
  act on belongs in the log entry that shares that ID.
- Keep responses **consistent within an error class**, and make security-equivalent
  outcomes externally indistinguishable. Different classes may and should differ —
  `400 VALIDATION_FAILED`, `401`, `403`, `409`, `429` are not a finding. What must not
  differ is a pair of outcomes whose distinction reveals protected state: whether an
  account exists, whether a record the caller may not see is present.
  `auth-security` owns making the login paths cost the same; this rule owns what
  they return.
- Disable developer error pages and detailed exception rendering in every
  non-development environment, and route unhandled errors through the framework's
  production error handler. This is a wiring decision, not the same thing as an
  environment variable reading `production` — the setting and its name differ per
  framework, and `references/framework-error-pages.md` has them.
- Render every external error through one helper, so the sanitization rules live in a
  single place instead of being re-derived at each handler.
- Consult `api-security` for the status code and response envelope, `logging-security`
  for the internal record, and `auth-security` for making two authentication failures
  cost the same. This skill owns one decision — what crosses the boundary.

### NEVER
- Serialize exception or debug internals into an external response: stack traces, SQL
  fragments and constraint names, filesystem paths, internal hostnames, dependency or
  framework versions.
- Silently swallow an unexpected exception — a bare `except: pass`, `catch {}`,
  `rescue nil`. Let it reach the nearest designated error boundary, which logs it and
  converts it to a sanitized response. A narrowly-typed, commented suppression of an
  expected condition is fine; the finding is the broad or unexplained one.
- Withhold client-actionable validation detail in order to make the API harder to
  explore, or smuggle server state into it. Which field failed and why is the
  **public contract** — that is what RFC 9457 problem details and the GraphQL
  `errors` array are for — and it belongs in the response. Record existence,
  authorization state, and SQL or schema internals are **not** the contract and do
  not.

### KNOWN FALSE POSITIVES
- Developer diagnostics in an explicitly local development environment that no
  untrusted caller can reach. The safety comes from the deployment, not from the
  hostname: `localhost` and `*.local` are not security boundaries, and a debug
  console that executes code is dangerous wherever it is reachable.
- An authenticated, authorized diagnostic or admin endpoint returning more detail
  than a public one. It still may not return secrets, credentials or PII —
  authenticating the caller does not make that data less sensitive, and a health
  check should answer with status, not with internals.

## Context (for humans)

CWE-209 is small text with large consequences: it is how an attacker moves from "this
service exists" to "this service runs Spring 5.2 on Tomcat 9 with a PostgreSQL table
called `users` and a column called `email_normalized`". Every extra detail lowers the
cost of the next attack.

The line this skill draws is **client-actionable versus internal**, not
detailed-versus-generic. Those get confused, and the confusion is expensive in both
directions: an API that flattens every validation failure into an opaque `400` is
hostile to its own callers without being meaningfully safer, while one that returns a
database constraint name has handed over its schema. `email must be a valid address`
is the public contract. `users.email_normalized violates users_email_key` is not.

Ownership is deliberately narrow. What a log entry may contain belongs to
`logging-security`; making two authentication paths take the same amount of work
belongs to `auth-security`; HTTP status semantics and the response envelope belong to
`api-security`. This skill owns one decision — what crosses the boundary — and the
handler that enforces it.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/framework-error-pages.md` — turning off developer error pages per
  framework, and why the environment variable is not the switch
- `rules/error_response_template.json`
- [OWASP Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html).
- [RFC 9457 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html).
- [CWE-209](https://cwe.mitre.org/data/definitions/209.html) · [CWE-755](https://cwe.mitre.org/data/definitions/755.html).
