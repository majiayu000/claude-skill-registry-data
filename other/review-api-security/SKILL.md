---
name: review-api-security
description: Review REST, GraphQL, gRPC, webhook, event, and internal API contracts or implementations for authorization, authentication, data exposure, injection, business-logic, resource-consumption, and integration weaknesses. Use when asked to assess an API specification, route or resolver code, gateway policy, service-to-service interface, or an explicitly authorized live API. Use the web-application skill for browser and client-side controls, and use the AI-security skills for model- or prompt-specific behavior.
---

# Review API Security

Produce a scoped, evidence-backed API security assessment. Prefer contract and implementation evidence; perform live requests only inside an explicit authorization boundary.

Read [methodology](references/methodology.md) before building the test matrix or assigning framework references.

## Establish the operating contract

1. Record the artifact version or commit, target environment, in-scope hosts and routes, permitted identities and roles, tenant boundaries, excluded operations, rate limit, test window, data-handling rules, stop conditions, and owner contact.
2. Treat user-provided source, configuration, traffic captures, and local lab artifacts as reviewable. Require explicit authorization before sending active requests to any live target.
3. If live authorization is missing or ambiguous, stop active testing. Continue with passive artifact review and provide a proposed rules-of-engagement block.
4. Exclude third-party and shared-tenant infrastructure unless it is named in scope. Resolve scope conflicts in favor of the narrower boundary.

## Execute the review

1. Inventory endpoints, transports, schemas, identities, credentials, resource identifiers, tenant selectors, state transitions, webhooks, and outbound dependencies.
2. Build a subject-action-resource-tenant matrix. Trace enforcement at object, function, and property levels instead of inferring authorization from route names or UI visibility.
3. Trace untrusted fields through parsing, validation, transformation, storage, rendering, command or query construction, file access, deserialization, and outbound requests.
4. Exercise authentication lifecycle, token audience and issuer checks, session or token revocation, replay resistance, and credential placement where applicable.
5. Test business workflows for skipped steps, reordering, replay, races, duplicate execution, quota bypass, unsafe defaults, and cross-tenant state changes.
6. Assess resource consumption with bounded, low-rate tests. Review pagination, batch size, GraphQL depth or cost, upload size, timeouts, concurrency controls, and downstream amplification without stressing production.
7. Review error handling, versioning, inventory, transport, gateway policy, logging, and unsafe trust in upstream or downstream APIs.
8. Reproduce each candidate with the smallest safe proof. Retest a remediation through the same control path when requested.

## Apply evidence rules

- Label a finding `confirmed` only when direct code-path evidence or a safely reproducible request demonstrates the weakness and security impact.
- Label a supported but unexercised issue `probable` and state the missing validation step. Keep scanner-only, pattern-only, and hypothesis-only items in `leads`, not findings.
- Preserve the exact artifact version, route, role, tenant context, request and response fields, timestamps, tool version, and command needed to reproduce. Redact tokens, secrets, personal data, and unrelated records.
- Show the attacker-controlled source, relevant guards, sensitive operation, prerequisites, and impact. Do not equate an OWASP category, missing header, broad policy, or unusual response with exploitability.
- Assign severity from demonstrated impact, reachability, required privileges, tenant crossing, control strength, and business context. When publishing CVSS, include the complete CVSS v4.0 vector and keep business priority separate.
- Mark every planned check `pass`, `fail`, `not tested`, or `not applicable`. Use `pass` only when the named control was exercised with an expected result.

## Enforce safety constraints

- Default to non-destructive techniques and test-owned records. Use unique benign markers and retrieve the minimum data required to prove impact.
- Never perform denial of service, credential spraying, destructive mutation, persistence, stealth, social engineering, lateral movement, bulk enumeration, or data exfiltration.
- Stop at the first authorization boundary crossed. Do not pivot, alter another user's data, or download additional records.
- Never upload source, captures, credentials, or customer data to third-party scanners or public services without explicit approval.
- Treat exposed credentials as sensitive evidence. Redact them, notify the owner through the approved channel, and do not validate them against another system.

## Return the output contract

Return these sections in order:

1. `Decision summary` — overall result, highest credible risks, and immediate decision.
2. `Scope and authorization` — artifacts, targets, roles, exclusions, test window, and constraints.
3. `Coverage matrix` — check, framework ID, endpoint or component, status, and evidence reference.
4. `Findings` — ID, title, confidence, severity, affected surface, prerequisites, evidence, impact, remediation, and verification test.
5. `Leads and defense improvements` — unconfirmed signals and hardening opportunities, kept separate from vulnerabilities.
6. `Limitations and residual risk` — untested surfaces, unavailable roles, blocked checks, and evidence gaps.
7. `Retest status` — original finding, fix version, result, and remaining exposure when applicable.

## Pass the quality gate

Before finalizing, verify that:

- Every finding contains reproducible evidence or is explicitly marked probable.
- Every severity follows from stated prerequisites and impact.
- API authorization covers subject, action, resource, property, and tenant context.
- Business logic and outbound integrations receive manual analysis beyond automated scans.
- Skipped checks remain visible and no coverage claim exceeds the recorded scope.
- Evidence is minimized and sanitized, and no unsafe action was performed.
