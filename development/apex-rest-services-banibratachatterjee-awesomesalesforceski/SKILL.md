---
name: apex-rest-services
description: "Use when building, reviewing, or debugging inbound Apex REST resources, request/response handling, status codes, versioned URL mappings, or JSON serialization in `@RestResource` classes. Triggers: 'Apex REST', '@RestResource', 'HttpGet/HttpPost', 'RestContext', 'versioned endpoint'. NOT for outbound HTTP callouts or standard Salesforce REST API usage as a consumer."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Reliability
  - Operational Excellence
tags:
  - apex-rest
  - restresource
  - restcontext
  - json-serialization
  - versioning
triggers:
  - "how do I build an Apex REST endpoint"
  - "RestContext request and response pattern"
  - "Apex REST status codes and error body"
  - "versioning strategy for Apex REST"
  - "HttpGet HttpPost HttpPatch in Apex"
inputs:
  - "resource use case and whether a custom endpoint is really necessary"
  - "authentication, caller identity, and sharing expectations"
  - "request schema, response schema, and versioning plan"
outputs:
  - "Apex REST design recommendation"
  - "review findings for endpoint security, versioning, and response handling"
  - "resource scaffold with explicit status and JSON patterns"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

Use this skill when Salesforce itself is exposing a custom HTTP contract through Apex. The point is to keep the REST resource thin, explicit about sharing and validation, and predictable in its status codes and JSON behavior. A custom endpoint should be a deliberate choice, not the default substitute for standard APIs or internal Apex calls.

## Before Starting

- Is custom Apex REST actually required, or would the standard REST API, Composite API, or an invocable/action pattern be simpler?
- What authentication model and sharing behavior should the caller get?
- How will the URL, payload schema, and response schema evolve without breaking clients?

## Core Concepts

### `@RestResource` Is An Adapter Layer

A REST resource should parse the request, validate inputs, delegate to a service, and shape the response. It should not become the only place business logic lives. Thin resources are easier to version, easier to secure, and easier to test by setting `RestContext.request` and `RestContext.response`.

### Status Codes And Error Bodies Are Part Of The Contract

If an endpoint always returns `200` with a loosely structured body, clients cannot behave reliably. Set explicit status codes, return consistent JSON error shapes, and distinguish validation failures, not-found cases, and server-side exceptions.

### Version The URL Mapping Deliberately

Versioning should be visible and explicit, often in the URL mapping or path contract. This keeps older consumers from being broken by incompatible payload changes. Versioning is an operational strategy, not just a naming convention.

### Security Must Be Declared And Enforced

REST classes still need explicit sharing decisions and secure data access patterns. Authentication into Salesforce is only one half of the problem; the Apex code must still enforce the right record, object, and field boundaries.

## Common Patterns

### Thin Resource + Service Layer

**When to use:** A custom endpoint handles business logic on Salesforce data.

**How it works:** Parse request data in the resource class, delegate the real workflow to a service, then set `RestContext.response` deliberately.

**Why not the alternative:** Fat resource classes are hard to version and tend to hide security mistakes.

### Consistent Error Envelope

**When to use:** Consumers need stable machine-readable errors.

**How it works:** Return a simple JSON structure with code, message, and optional correlation ID.

### Versioned URL Mapping

**When to use:** The API contract may evolve incompatibly.

**How it works:** Include versioning in the URL contract and keep old behavior stable until clients migrate.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| External system needs a custom business API in Salesforce | Apex REST | Salesforce exposes a deliberate custom contract |
| Consumer only needs standard data CRUD/query access | Prefer standard Salesforce APIs | Less code and less custom maintenance |
| Contract may change incompatibly over time | Versioned URL mapping and payload contract | Safer client evolution |
| Endpoint updates Salesforce data | Thin REST resource + secure service layer | Better maintainability and security review |


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

- [ ] A custom Apex REST endpoint is justified over standard APIs.
- [ ] The resource class is thin and delegates business logic.
- [ ] Status codes and JSON error bodies are explicit and consistent.
- [ ] Sharing and data-access enforcement are deliberate, not assumed.
- [ ] URL mapping or payload versioning is defined.
- [ ] Tests set `RestContext.request` and `RestContext.response` explicitly.

## Salesforce-Specific Gotchas

1. **`RestContext` is only populated in REST execution or tests that set it** — do not assume it exists in ordinary Apex contexts.
2. **Apex REST security is not automatic beyond authentication** — data access still needs explicit review.
3. **Returning raw exceptions as response bodies leaks internals** — map failures to stable error contracts.
4. **Resource classes become brittle fast if business logic lives directly inside them** — versioning pain follows.

## Output Artifacts

| Artifact | Description |
|---|---|
| REST endpoint review | Findings on contract design, status handling, security, and versioning |
| Resource scaffold | Thin `@RestResource` class with explicit request parsing and response shaping |
| Versioning notes | Guidance for evolving the endpoint without breaking consumers |

## Related Skills

- `apex/apex-security-patterns` — use when the main risk is the sharing or CRUD/FLS posture of the endpoint.
- `apex/exception-handling` — use when the error contract and internal failure mapping need refinement.
- `apex/test-class-standards` — use when REST resource tests are weak or missing request/response assertions.
