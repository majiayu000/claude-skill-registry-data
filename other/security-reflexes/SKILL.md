---
name: security-reflexes
description: Security reflexes that fire while writing ordinary code — parameterize at trust boundaries, allowlist inputs, authorize per object, keep secrets out of logs, bundles and errors. Use when writing or reviewing code that touches user or LLM-generated input, login/session/permission checks, tokens or API keys, file paths, URLs the server will fetch, shell or subprocess calls, SQL, HTML rendering, webhooks, or third-party APIs. Not for full penetration tests or threat modelling.
---

# Security Reflexes

Not a pentest methodology — these are the reflexes that fire while writing ordinary code. Weak security work is a generic "sanitize inputs" pass after the code is written. Strong security work names each trust boundary the diff crosses before writing, applies the matching control at the sink, and reports which control went where.

## Step 0: name the boundaries

Before writing, list every value in the diff that originates outside the process — user, client, LLM output, webhook, file, environment, external API — as one line each: `source → sink` (e.g. `query param id → SQL WHERE`, `model output → shell arg`). Every line must end with a control from the sections below. A value with no line is a value you have not thought about.

## Input crossing a trust boundary

- **Parameterize, never concatenate**: SQL via placeholders; shell via array-arg APIs, no string-built commands; paths via join + canonicalize + prefix check against the allowed root (traversal: `../`, absolute paths, symlinks).
- **Validate at the boundary, by allowlist**: enums, slugs, sort/filter fields mapped through a server-side allowlist — especially LLM-generated values headed into external APIs. Reject unexpected keys, not just missing ones. If you are writing a deny-list regex to "clean" input, stop: allowlist, or encode at the sink.
- **HTML**: rendering user or model text as raw HTML is an XSS. Keep markdown renderers raw-HTML-off; escape by default. Any raw-HTML sink or "mark safe" escape hatch on non-constant input needs a written justification in the report.
- **URLs the server will fetch**: validate scheme + host against an allowlist before fetching (SSRF reaches internal services and cloud metadata endpoints).
- **Deserialization of external input**: try/catch plus shape validation, and never a format that can instantiate arbitrary types.

## AuthN / AuthZ

- Every mutating endpoint answers two questions in code: WHO is calling (authentication) and MAY they touch THIS object (authorization — an ownership or membership check on the specific row, not just "is logged in"). Point at the line where each is answered.
- Never trust client-supplied identity or scope fields: user IDs, account IDs, role flags, prices, approved parameters. The server derives them from the session or its own records.
- Approval flows: bind execution to a server-recorded intent; the client conveys a reference, never the parameters.
- Incoming webhooks: verify the signature before parsing the body.

## Secrets

- Secrets come from env or a secret manager only: never hardcoded, never in client bundles (watch framework prefixes that expose env to the browser), never in logs, never in error messages echoed to users.
- Before reporting done, grep the diff for log/print/debug lines that dump a whole request, response, headers, or config object; remove or redact them.
- External API errors: wrap and sanitize before showing users — raw provider errors leak internal detail.
- Never ask for or accept credentials that identify a human irreversibly (private keys, seed phrases), even "just to test".

## Dangerous defaults to catch in review

- Comparing tokens or signatures with `==` where a constant-time compare exists.
- Missing rate limiting or size caps on endpoints that do expensive work, send messages, or accept uploads.
- CORS `*` on authenticated routes; cookies without httpOnly/secure/sameSite decided.
- Temp files or predictable paths for sensitive data; world-readable permissions.

## When the change is security-relevant by nature

If the diff touches auth flows, crypto, session handling, token generation, or permission checks: stop and find the existing pattern in the codebase or the standard library, and match it exactly. Bespoke crypto, session, or token logic is almost always the bug. In your report, state which security property you preserved and the exact test or request you ran to verify it.

## Escalate, don't improvise

Discovering an existing vulnerability mid-task: report it (what, where, how exploitable) rather than silently fixing beyond scope or ignoring it. Destructive proof-of-concepts and exploit tooling need explicit authorization context.

## Reporting

For each boundary line from Step 0, one line in the report: source, sink, control applied, where. A boundary with no control is a finding, not an omission. This holds when the deliverable is a findings list: walk every path that reads or mutates a record and ask who is calling and whether they may touch this object; an identifier accepted from the request without an ownership check is a finding even when the code works.
