---
name: review-web-application-security
description: Review browser-facing web applications, source code, configuration, and explicitly authorized live environments for authentication, session, authorization, injection, client-side, business-logic, file-handling, and deployment weaknesses. Use for AppSec reviews, secure code review, pull-request security review, or scoped web testing. Use the API skill for service-interface depth and the AI-security skills for model- or prompt-specific behavior.
---

# Review Web Application Security

Produce a scoped web security review that joins design, code, configuration, and safe runtime evidence without turning scanner output into findings.

Read [methodology](references/methodology.md) before selecting WSTG or ASVS coverage and before performing active tests.

## Establish the operating contract

1. Record the artifact version or commit, target origins, environment, user roles, tenant boundaries, workflows, browsers, exclusions, permitted techniques, rate limit, test window, data rules, stop conditions, and owner contact.
2. Treat supplied code, configuration, captures, and local labs as reviewable. Require explicit authorization before navigating, crawling, scanning, or sending crafted requests to a live target.
3. Require separate approval for state-changing production tests. Prefer test-owned accounts and records even when broad testing authority exists.
4. If live authority is missing or ambiguous, perform static and passive review only and return the rules of engagement needed to continue.

## Execute the review

1. Map routes, forms, parameters, uploads, downloads, redirects, authentication and recovery flows, privileged functions, sensitive workflows, WebSockets, browser storage, embedded content, third parties, and trust boundaries.
2. When source is available, trace untrusted input from entry point through validation and authorization to database, template, DOM, command, file, network, deserialization, and logging sinks. Review both changed code and affected callers.
3. Test authentication, account lifecycle, recovery, reauthentication, session creation and invalidation, cookie properties, token placement, fixation, concurrency, and cross-origin behavior.
4. Build a role-resource-action-tenant matrix. Compare positive and negative cases for direct URLs, object identifiers, alternate methods, hidden functions, exports, and multi-step workflows.
5. Review server- and client-side injection, output encoding, DOM sinks, template behavior, CSRF, SSRF, path traversal, file upload and download, unsafe deserialization, redirects, caching, and error disclosure.
6. Test business logic for skipped steps, replay, races, duplicate execution, value or quota manipulation, approval bypass, and inconsistent enforcement across UI and direct requests.
7. Review CSP, framing, CORS, browser isolation, TLS, proxy normalization, host handling, debug settings, secrets, dependency behavior, audit events, and security-relevant failure modes where applicable.
8. Validate each candidate with the smallest harmless proof. Retest fixes through the same path and role context when requested.

## Apply evidence rules

- Label a finding `confirmed` only when a reachable code path or safely reproducible interaction demonstrates the weakness and impact.
- Label a strongly supported but unexercised issue `probable` and state what prevents confirmation. Keep scanner-only and pattern-only signals in `leads`.
- Cite exact file and line, commit, route, role, tenant, browser, request and response fields, UTC time, tool version, and command as applicable. Redact secrets, tokens, personal data, and unrelated records.
- Show source, transformations, guards, sink, prerequisites, and resulting security effect. Do not call a best-practice gap or missing header a vulnerability without context.
- Assign severity from demonstrated impact, reachability, privileges, user interaction, tenant crossing, reliability, and business context. Include a CVSS v4.0 vector whenever publishing a CVSS score.
- Mark checks `pass`, `fail`, `not tested`, or `not applicable`. Use `pass` only after exercising the intended control in the recorded context.

## Enforce safety constraints

- Default to read-only and non-destructive tests. Use benign unique markers and test-owned data.
- Never perform denial of service, credential spraying, social engineering, persistence, stealth, lateral movement, destructive upload, bulk extraction, or tests likely to affect other users.
- Stop after the minimum proof of access or execution. Do not pivot, retain access, alter another user's record, or collect additional data.
- Keep automated scans bounded to the exact target and rate agreed in the rules of engagement. Disable dangerous scanner modules by default.
- Never upload source, captures, cookies, credentials, or customer data to a third-party service without explicit approval.
- If a test causes unexpected impact, stop immediately, preserve the minimum diagnostic evidence, and contact the named owner.

## Return the output contract

Return these sections in order:

1. `Decision summary` — overall posture, highest credible risks, and immediate decision.
2. `Scope and authorization` — artifacts, targets, roles, workflows, exclusions, test window, and constraints.
3. `Attack-surface map` — entry points, trust boundaries, identities, sensitive actions, and data flows.
4. `Coverage matrix` — framework check, component or route, method, status, and evidence ID.
5. `Findings` — ID, title, confidence, severity, location, prerequisites, evidence, impact, remediation, and verification test.
6. `Leads and defense improvements` — unconfirmed signals and hardening opportunities, separate from vulnerabilities.
7. `Limitations and residual risk` — inaccessible roles, skipped tests, unavailable source, and runtime blind spots.
8. `Retest status` — original finding, fix version, test context, result, and residual exposure when applicable.

## Pass the quality gate

Before finalizing, verify that:

- Every finding is reachable, evidence-linked, and deduplicated by root cause.
- Manual analysis covers authorization and business logic beyond automated tooling.
- Code evidence and runtime evidence are not conflated.
- Framework IDs are versioned or tied to a recorded stable edition.
- Every skipped surface remains visible and no pass claim exceeds actual coverage.
- Evidence is minimized and sanitized, and all live actions stayed inside authorization and stop conditions.
