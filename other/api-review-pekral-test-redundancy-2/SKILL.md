---
name: api-review
description: "Use when reviewing HTTP API design in a PR or change set — endpoints, routes, HTTP methods, status codes, idempotency, and input validation. Treats the API as a consumer-facing contract and flags resource-orientation, method-semantics, status-code, and trust-boundary violations. Read-only."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/api/general.md` — this skill is the focused review lens for that rule.
- Apply `@rules/php/core-standards.md`
- Apply `@rules/security/backend.md` — for the error-text and authorization-leak surface of API responses (401/403/404 wording, no internal-detail leak).
- If the current project uses Laravel, also apply `@rules/laravel/architecture.md` and `@rules/laravel/laravel.md` — validation belongs in FormRequest / Data Validator, controllers stay slim.
- Apply `@rules/reports/general.md` — when the findings are folded into the **GitHub PR comment** by a CR wrapper they stay in canonical English per the rule's *Exception — technical CR findings on the GitHub PR*; a non-technical mirror on a linked issue / JIRA ticket follows the language of the source assignment. A manifest `language.github` overrides both on GitHub (the rule's *Project override — `language.github` in the manifest*). HTTP verbs, status codes, header names, and code identifiers stay verbatim regardless of the surrounding prose language.
- Output findings only — no praise, no summary of what was checked.
- **Read-only skill** — never modify code, never stage / commit / push, and never run any git write operation. Switching to the relevant branch and `git pull` to read the latest diff are allowed; mutating the working tree or pushing is not.

## Use when
- A PR or change set adds or modifies HTTP endpoints, routes, controllers, API Resources, request/response payloads, or status-code handling.
- Run as part of every code review via `@skills/code-review/SKILL.md` (Specialized Reviews → Always run).
- A consumer-facing API contract needs a design check before release.

## Scope
Review only the API surface on the **diff** — never untouched endpoints. Detect the surface from any of: route definitions, controller/`__invoke` request handlers, API Resources / DTOs serialized into responses, FormRequests, `response()` / `abort()` / status-code calls, and `Idempotency-Key` handling. If the diff touches no API surface, return no findings.

**This lens owns the generic HTTP contract of an MPP-gated endpoint, never the protocol behind it.** When the CR's payment trigger fires on the same diff on a project that implements MPP (`@skills/code-review/references/specialized-reviews.md` *Specialized Reviews*), `@skills/machine-payments-protocol/SKILL.md` with `MODE=cr` runs alongside this lens and owns protocol conformance — the challenge and receipt shape on the wire, single-use proof, request and body binding, expiry, no side effect before payment, idempotent settlement, and server-side pricing. This lens keeps status-code choice outside the `402` challenge itself, the response envelope, versioning, and idempotency-key mechanics, and never restates a protocol finding in its own words.
The two divide the *dimensions* of a payment change, never its lines: a gated endpoint that both settles a replayed receipt a second time and answers a client retry with no `Idempotency-Key` handling carries one protocol finding from the payment lens and one idempotency finding here — a different defect, never this lens's finding restated.

## Core Checks
Walk the diff against each pillar of `@rules/api/general.md` and raise one finding per match.

### 1. Contract & consumer orientation
- Response leaks internal DB structure — raw column names, surrogate/internal keys, join tables, enum integers, or storage-only fields serialized without a DTO / API Resource boundary.
- Inconsistent contract shape for the same concept across endpoints (field casing, date format, pagination shape, error envelope).

### 2. Resource-oriented REST
- Action/verb in the endpoint path (`/getUser`, `/createUser`, `/users/{id}/delete`, `/doPayment`) instead of a resource noun + HTTP method.

### 3. HTTP methods & idempotence
- Method whose side effects violate its contract — `GET` that mutates state, `PUT`/`DELETE` not idempotent on repetition.
- `PUT` used for a partial update or `PATCH` used for a full replacement.

### 4. Idempotency keys
- Critical, retry-prone, state-changing operation (payment, transfer, order placement) with no `Idempotency-Key` handling, so a client retry can double-execute.

### 5. Status codes
- Imprecise success code — `200` for a creation (`201`), for an async hand-off (`202`), or where `204` (no body) is correct; a body returned alongside `204`.
- Error code collapsed into a generic one where a narrower code applies (`400`/`401`/`403`/`404`/`409`/`422`/`429`).
- 401-vs-403 inversion — `401` for an authorization failure or `403` for a missing/invalid credential.

### 6. Validation at the trust boundary
- Input reaching business logic or the database before schema/business validation runs (trust-boundary bypass).
- Validation inlined in the action/controller/model instead of the dedicated boundary layer (FormRequest / Data Validator).
- Authorization check missing or running before the input is known to be well-formed.
- Error responses that leak identity, resource existence, or internal detail — defer to `@rules/security/backend.md` *Safe Validation & Error Messages* and do not duplicate a finding `@skills/security-review/SKILL.md` already owns.

## Prioritization
- Focus on contract defects a consumer would feel: double-charges, wrong status branching, breaking payload shapes, bypassed validation.
- Do not report purely cosmetic naming nits. The review has no tier below Moderate (`@rules/code-review/general.md` *Minor findings are not detected*).
- Do not propose API features the current scope does not require (YAGNI per `@rules/php/core-standards.md`).

## Report

### Real-Code Grounding for Every Finding (issue #97)
Apply the contract in `@rules/code-review/general.md` *Real-Code Grounding for Every Finding (issue #97)* to every finding — **Critical and Moderate alike; no severity is exempt**. On this skill's surface the context to re-read is the enclosing route / controller / FormRequest / API Resource, plus any Service or DTO the Suggested Fix depends on — a contract claim is grounded only when the real route definition and the real response shape were both read. The requirement holds equally for a standalone run (e.g. a pre-release API design check).

Findings from this skill fold into the core CR's severity buckets; the Assignment-Declared Test-Only Conditions — Exclusion Gate (`@rules/code-review/general.md` *Assignment-Declared Test-Only Conditions — Exclusion Gate (issue #17)*) is applied by `@skills/code-review/SKILL.md`, not here — trust-boundary / authorization findings from Core Check 6 fall under the gate's security carve-out and are never excludable.

Use the severity scale of `@skills/code-review/SKILL.md` so findings fold cleanly into the code review:

- **Critical** / **Moderate** — apply the severity declared in `@rules/api/general.md` *CR Severity Rules*. An entry that rule grades below Moderate is not reported.

Each finding includes:
- location (`file:line`)
- risk/impact (the consumer-facing consequence)
- the cited rule reference (e.g. `@rules/api/general.md#Resource-Oriented REST`)
- concrete fix

Each **Critical** and **Moderate** finding additionally includes:
- **Faulty Example** — minimal endpoint / route / payload snippet that reproduces the issue (redact secrets/PII)
- **Expected Behavior** — single assertable statement (status code, response shape, idempotent outcome, rejection before side effect)
- **Test Hint** — one sentence pointing at the test layer (feature/HTTP, integration) and the entry point
- **Suggested Fix** — minimal corrected snippet that complies with `@rules/api/general.md`, `@rules/php/core-standards.md`, and on Laravel projects `@rules/laravel/architecture.md`. Use `n/a — <reason>` only when a snippet adds nothing over the one-line fix.

These fields exist so `@skills/process-code-review/SKILL.md` can turn each finding into a reproducer test and apply the fix without re-deriving context.

## Output Format
Use the template defined in `templates/review-output.md`. Omit any severity section that has no findings; never emit `None.` / `n/a` placeholders.

## Done when
- Every API-surface change on the diff has been walked against the six Core Checks.
- Findings are grouped by severity with the mandatory reproducer fields on every Critical and Moderate item.
- Every published finding was re-grounded in the real, current file per Real-Code Grounding (issue #97).
- No code, git, or remote state was modified (read-only).

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
