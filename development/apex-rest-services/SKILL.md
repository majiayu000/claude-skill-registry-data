---
name: apex-rest-services
description: "Use when building, reviewing, or debugging inbound Apex REST resources, request/response handling, status codes, versioned URL mappings, or JSON serialization in `@RestResource` classes. Triggers: 'Apex REST', '@RestResource', 'HttpGet/HttpPost', 'RestContext', 'versioned endpoint', 'services/apexrest', 'urlMapping', 'RestRequest requestBody', 'RestResponse statusCode'. NOT for outbound callouts — use apex/callouts-and-http-integrations. NOT for a deprecation and sunset policy across many endpoints — use integration/api-versioning-strategy."
category: apex
salesforce-version: "Spring '25+; verified against Apex Developer Guide and Apex Reference Guide v67.0, Summer '26"
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
  - "expose an Apex class at /services/apexrest for an external system"
  - "apex rest endpoint returns 404 but the class is deployed"
  - "my RestResponse statusCode 422 comes back as a 500"
  - "requestBody is null in my HttpPost apex rest method"
  - "write a test class that sets RestContext.request and asserts the status code"
  - "apex rest call returns 403 for the integration user"
  - "apex rest returns 200 with a truncated json body"
  - "two RestResource classes with the same urlMapping"
  - "apex rest url changed after packaging into a managed package"
inputs:
  - "resource use case and whether a custom endpoint is really necessary"
  - "authentication, caller identity, and sharing expectations"
  - "request schema, response schema, and versioning plan"
  - "the apiVersion pinned in the class's .cls-meta.xml"
outputs:
  - "Apex REST design recommendation"
  - "review findings for endpoint security, versioning, and response handling"
  - "resource scaffold with explicit status and JSON patterns"
  - "deployable resource + service + test class, `.cls-meta.xml`, `package.xml`, and a cURL contract probe"
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-09-05
---

Use this skill when Salesforce itself is exposing a custom HTTP contract through Apex. The point is to keep the REST resource thin, explicit about sharing and validation, and predictable in its status codes and JSON behavior. A custom endpoint should be a deliberate choice, not the default substitute for standard APIs or internal Apex calls.

---

## Before Starting

- Is custom Apex REST actually required, or would the standard REST API, Composite API, or an invocable/action pattern be simpler?
- What authentication model and sharing behavior should the caller get? Apex REST "supports these authentication mechanisms: OAuth 2.0, Session ID" (apexdev L18402–18404) — there is no third option to design, only the two to configure.
- How will the URL, payload schema, and response schema evolve without breaking clients?
- What `apiVersion` will the class's `.cls-meta.xml` carry? That number, not the org's release, decides the sharing and user-mode defaults (apexdev L18735–18739).
- Will this class ever ship inside a managed package? If so its public URL grows a namespace segment (apexdev L18465–18470), and the contract has to be published as configuration, not as a constant.

## Questions to Ask Before Configuring

Ask these before writing the class; the answers decide the contract, and an LLM that skips them ships an endpoint that deploys, passes its tests, and returns `200` on failure.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "What is the exact URL, including the version segment, and who else may claim it?" | Overlapping mappings resolve to whichever class was saved first, not to the more specific one (gotcha: wildcard/save order) — and the mapping is case-sensitive | One mapping string, published verbatim, that no other `@RestResource` in the org can also match |
| "What is the complete list of status codes this endpoint may return, ours and the platform's?" | A code outside the documented `statusCode` table becomes a `500`; unhandled exceptions become a platform `400`/`500` that never reaches your envelope (gotchas: status-code whitelist; unhandled exceptions) | A status table the client can code against, splitting codes you set from codes the platform sets |
| "What does the caller need to see when it fails — a field name, a retryable flag, a support reference?" | Decides the error envelope's fields; a raw exception message leaks internals, and without a correlation id a client complaint cannot be resolved to a log row (gotcha: unhandled exceptions bypass the envelope) | The envelope schema, plus the `Application_Log__c` query that resolves a client-quoted request id |
| "Which permission set grants Apex Class Access, and to which class?" | Class security is checked at the entry point only; without it every call is `403` before your code runs (gotcha: Apex Class Access) | A permission set shipped in the same `package.xml`, granting the resource class and not the service class |
| "Is the response bounded — one record, a page, or 'all of them'?" | Heap exhaustion during serialization returns `200` with a truncated body, so an unbounded collection endpoint fails invisibly (gotcha: heap/200) | A page size in the contract and a decision to return `void` + `RestResponse` rather than an sObject collection |
| "Does any method need the raw body — for a signature check, replay, or an idempotency key?" | Declaring method parameters empties `RestRequest.requestBody` (gotcha: parameters vs requestBody), and the two styles cannot be mixed in one method | A per-method decision: parameterless + explicit `JSON.deserialize`, or parameter-based deserialization |
| "What is the slowest realistic call, and how large is the largest payload?" | Requests over 20 seconds consume a concurrency slot capped at 25 (5 in DE); body is capped at 6 MB sync, and URI+headers at 16,384 bytes (gotcha: size ceilings) | A published maximum batch size, filters moved into the POST body, and an async fallback if p99 approaches 20 s |

What a proper configuration adds over just writing a `@RestResource` class: the client can branch on the status code instead of parsing prose, a support ticket resolves to one log row through the request id, the endpoint's access posture is readable in the source rather than implied by an `apiVersion` pin, and the failure modes the platform decides for you are documented alongside the ones you decided.

---

## Core Concepts

### `@RestResource` Is An Adapter Layer

A REST resource should parse the request, validate inputs, delegate to a service, and shape the response. It should not become the only place business logic lives. Thin resources are easier to version, easier to secure, and easier to test by setting `RestContext.request` and `RestContext.response`.

The smallest resource that keeps the contract in its own hands looks like this — `global` class, `global static void` verb method, no parameters, and every exit path writing both halves of the response:

```apex
@RestResource(urlMapping='/v1/cases/*')
global with sharing class CaseApiV1 {
    @HttpGet
    global static void doGet() {
        RestResponse res = RestContext.response;
        res.statusCode  = 200;                      // never left at the default
        res.addHeader('Content-Type', 'application/json');
        res.responseBody = Blob.valueOf(JSON.serialize(
            new Map<String, Object>{ 'id' => '500...', 'status' => 'New' }, true
        ));
    }
}
```

The platform constrains the shape of that adapter:

| Constraint | Grounded statement |
|---|---|
| Class must be `global` | "To use this annotation, your Apex class must be defined as global" (apexdev L6352) |
| Methods must be `global static` | "To use this annotation, your Apex method must be defined as global static" (apexdev L6388, restated per verb) |
| One method per verb | "A single Apex class annotated with `@RestResource` can't have multiple methods annotated with the same HTTP request method" (apexdev L18446–18448) |
| `@HttpGet` / `@HttpDelete` take no parameters | "GET and DELETE requests have no request body, so there's nothing to deserialize" (apexdev L18442–18443) |
| `@HttpGet` also answers HEAD | "Methods annotated with `@HttpGet` are also called if the HTTP request uses the HEAD request method" (apexdev L6389) |
| Mapping is relative and slash-prefixed | "The URL mapping is relative to `https://instance.salesforce.com/services/apexrest/`"; "The path must begin with a forward slash (/)"; "The path can be up to 255 characters long" (apexdev L6348, L6357–6358) |
| No `multipart/form-data` | "Apex REST currently doesn't support requests of Content-Type `multipart/form-data`" (apexdev L18449) |

Allowed parameter and return types are a closed list: "Apex primitives (excluding sObject and Blob) · sObjects · Lists or maps of Apex primitives or sObjects (only maps with String keys are supported) · User-defined types that contain member variables of the types listed above" (apexdev L18425–18437). For a user-defined type, "Apex REST deserializes request data into public, private, or global class member variables of the user-defined type, unless the variable is declared as `static` or `transient`" (apexdev L18488–18490) — and "the names of the Apex parameters matter, although the order doesn't" (apexdev L18570).

### Status Codes And Error Bodies Are Part Of The Contract

If an endpoint always returns `200` with a loosely structured body, clients cannot behave reliably. Set explicit status codes, return consistent JSON error shapes, and distinguish validation failures, not-found cases, and server-side exceptions.

Two halves of the status contract are not yours. The platform sets these before or around your code (apexdev L18680–18696):

| Code | Platform meaning |
|---|---|
| `400` | An unhandled *user* exception occurred |
| `403` | You don't have access to the specified Apex class |
| `404` | The URL is unmapped in an existing `@RestResource` annotation / the extension is unsupported / the namespaced class couldn't be found |
| `405` | The request method doesn't have a corresponding Apex method |
| `406` | `Content-Type` set to something other than JSON or XML, or an unsupported header |
| `415` | Unsupported XML parameter type or `Content-Type` |
| `500` | An unhandled Apex exception occurred |

And the codes you may set are a whitelist, not a range: 200, 201, 202, 204, 206, 300, 301, 302, 304, 400, 401, 403, 404, 405, 406, 409, 410, 412, 413, 414, 415, 417, 500, 503 (apexrefguide L228772–228820). `422` and `429` are not on it.

### Version The URL Mapping Deliberately

Versioning should be visible and explicit, often in the URL mapping or path contract. This keeps older consumers from being broken by incompatible payload changes. Versioning is an operational strategy, not just a naming convention.

Mapping resolution is deterministic but unintuitive: "An exact match always wins. If no exact match is found, find all the patterns with wildcards that match, and then select the longest (by string length) of those. If no wildcard match is found, an HTTP response status code 404 is returned" (apexdev L6362–6364). A wildcard is not restricted to the tail — "unless the wildcard is the last character in the path, it must be followed by a forward slash (/)" (apexdev L6360–6361) — so `/v1/cases/*/comments` is legal. Where two classes still overlap, save order decides (apexdev L18589–18591).

### Security Must Be Declared And Enforced

REST classes still need explicit sharing decisions and secure data access patterns. Authentication into Salesforce is only one half of the problem; the Apex code must still enforce the right record, object, and field boundaries. Never infer that boundary from the org's release: what a resource class does with no sharing keyword and no query clause is set by the `apiVersion` in its `.cls-meta.xml`, and it inverted at 67.0 (Summer '26). Read [`agents/_shared/AGENT_CONTRACT.md`](../../../agents/_shared/AGENT_CONTRACT.md) § *Apex security idiom by API version* before scoring an endpoint's posture.

The guide states both halves of the 67.0 change and the Apex-REST-specific default:

- "Custom Apex REST web service methods run in user mode by default. In user mode, the current user's object permissions, field-level security, and sharing rules are enforced" (apexdev L18724–18726).
- "In API version 67.0 and later, Apex runs in user context by default… In API version 66.0 and earlier, system mode is the default" (apexdev L18735–18737).
- "In API version 67.0 and later, classes without an explicit sharing declaration run in `with sharing` mode. In API version 66.0 and earlier, the default sharing mode of classes without an explicit sharing declaration is `without sharing`" (apexdev L18738–18739).
- "With API version 67.0 and later, you cannot use the `WITH SECURITY_ENFORCED` clause in SOQL SELECT queries in Apex code. Instead… use the `WITH USER_MODE` clause" (apexdev L44500–44502).

Bypassing is now the thing that must be explicit: "To bypass object or field-level security while using SOQL SELECT statements in Apex, you must use the `WITH SYSTEM_MODE` clause"; "To bypass sharing rules for Apex REST API methods, you must explicitly declare the class that contains these methods with the `without sharing` keyword" (apexdev L18727–18732).

---

## Common Patterns

### Thin Resource + Service Layer

**When to use:** A custom endpoint handles business logic on Salesforce data.

**How it works:** Parse request data in the resource class, delegate the real workflow to a service, then set `RestContext.response` deliberately. Worked end to end in `references/code-examples.md` (`CaseApiV1` + `CaseApiService`), with `templates/apex/BaseService.cls` supplying the savepoint and logging contract.

**Why not the alternative:** Fat resource classes are hard to version and tend to hide security mistakes. There is also a permissions reason: class security is checked at the entry point, so the resource is the class that goes in the permission set and the service is the class that does not (apexdev L12323–12329).

### Consistent Error Envelope

**When to use:** Consumers need stable machine-readable errors.

**How it works:** Return a simple JSON structure with code, message, and optional correlation ID. Use `System.Request.getCurrent().getRequestId()` as that ID — it is "the same as in the event log files of the Apex Execution event type used in Event Monitoring" (apexrefguide L228153), so one value joins the client's complaint, the org's log row, and the Event Monitoring record.

**Why not the alternative:** A prose message forces every client to string-match, and string-matching breaks on the first wording change.

### Versioned URL Mapping

**When to use:** The API contract may evolve incompatibly.

**How it works:** Include versioning in the URL contract and keep old behavior stable until clients migrate. One class per version, each with a mapping no other class can match, so a v2 rollout is a new class rather than an edit to a live one.

### `void` Method + Explicit `RestResponse`

**When to use:** Any endpoint with a published contract — which is all of them.

**How it works:** Declare the method `global static void`, take no parameters, read `RestContext.request.requestBody`, and write `res.statusCode` and `res.responseBody` yourself.

**Why not the alternative:** A non-void return type hands serialization to the platform, which drops null fields (apexdev L18463–18465), emits the sObject `attributes` envelope with a version-pinned URL (apexdev L18818–18828), and — on a large collection — can exhaust heap after the `200` header has already gone out (apexdev L18474–18477).

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| External system needs a custom business API in Salesforce | Apex REST | Salesforce exposes a deliberate custom contract |
| Consumer only needs standard data CRUD/query access | Prefer standard Salesforce APIs | Less code and less custom maintenance |
| Contract may change incompatibly over time | Versioned URL mapping and payload contract | Safer client evolution |
| Endpoint updates Salesforce data | Thin REST resource + secure service layer | Better maintainability and security review |
| Endpoint returns a collection that could grow | `void` + explicit `RestResponse` + a page size in the contract | Heap exhaustion mid-serialization returns `200` with a truncated body (apexdev L18474–18477) |
| Validation failure needs its own status | `400` with a `code` in the envelope — never `422` | `422` is absent from the `statusCode` table and is converted to `500` (apexrefguide L228768–228770) |
| Read-only reporting endpoint over a very large table | `@ReadOnly` on the method | Raises the returned-row limit to 1,000,000, but "blocks… DML operations, calls to `System.schedule`, and enqueued asynchronous Apex jobs" (apexdev L6162–6164) |
| Caller needs to upload a binary file | Parameterless method reading `req.requestBody` as a `Blob` | The guide's attachment sample does exactly this (apexdev L18867–18886); `multipart/form-data` is unsupported (apexdev L18449) |
| Payload will exceed a few MB or the call will run past 20 s | Move to Bulk API 2.0 or an async pattern | 6 MB sync / 12 MB async request-or-response cap (apexdev L18396–18397); 25 concurrent long-running requests (App Limits L481–493) |
| Outbound call from Salesforce to another system | `apex/callouts-and-http-integrations` | This skill is inbound only |

---

## Recommended Workflow

1. **Answer the questions above and freeze the contract.** Fix the mapping string (version segment included), the verb-to-method map, the request and response DTOs, the error envelope fields, and the full status table — yours *and* the platform's from Core Concepts.
2. **Check the mapping is unclaimed.** Grep the source tree for `urlMapping` and confirm nothing else matches the path, including the `/x` vs `/x/*` overlap; the resolution rules are in `references/gotchas.md`.
3. **Write the pair from `references/code-examples.md`.** Copy `CaseApiV1.cls` and `CaseApiService.cls`, keep every method `global static void` with no parameters, and route CRUD/FLS through `templates/apex/SecurityUtils.cls` and failure logging through `templates/apex/ApplicationLogger.cls` rather than hand-rolling either.
4. **Wire the deployment artifacts.** Take the `*.cls-meta.xml` (`<apiVersion>67.0</apiVersion>`) and the `package.xml` from the same file. The `package.xml` must include the permission set granting Apex Class Access on the resource class — without it every call is `403`.
5. **Write the test from the same file.** `CaseApiV1Test` builds `RestRequest` / `RestResponse`, assigns `RestContext.request` and `RestContext.response`, and asserts on `statusCode`, on the envelope's `code`, and on the `Location` header — not just on the record count.
6. **Run the checker.** `python3 skills/apex/apex-rest-services/scripts/check_apex_rest_services.py --manifest-dir force-app` — it flags a non-`global` resource class or non-`global static` verb method, duplicate verb annotations, an illegal or duplicated `urlMapping`, a missing sharing declaration graded against the `.cls-meta.xml`, `@HttpGet`/`@HttpDelete` with parameters, a status code outside the documented table, a `catch` block that sets no status code, and a resource with no test class touching `RestContext`.
7. **Deploy, then probe the contract.** `sf project deploy start -x manifest/package.xml`, `sf apex run test -n CaseApiV1Test -r human -w 20 -c -y`, then the cURL probes in `references/code-examples.md` § 7 — including the two that must return `405` and `404`, which prove the mapping is what you think it is.

---

## Review Checklist

- [ ] A custom Apex REST endpoint is justified over standard APIs.
- [ ] The resource class is thin and delegates business logic.
- [ ] Status codes and JSON error bodies are explicit and consistent.
- [ ] Sharing and data-access enforcement are deliberate, not assumed.
- [ ] URL mapping or payload versioning is defined.
- [ ] Tests set `RestContext.request` and `RestContext.response` explicitly.
- [ ] Every verb method is `global static void` and takes no parameters, so the class owns its own response body.
- [ ] Every status code the class sets appears in the documented `statusCode` table — no `422`, no `429`.
- [ ] Every `catch` block sets a status code before returning; none allows the default `200` to stand.
- [ ] The mapping string is unique in the org, and no sibling class maps `/x` where this one maps `/x/*`.
- [ ] The `.cls-meta.xml` `apiVersion` is recorded in the review, and the sharing keyword is declared regardless of it.
- [ ] The permission set granting Apex Class Access ships with the class.
- [ ] Any collection response has a bounded page size, and no method returns an sObject collection directly.

## Salesforce-Specific Gotchas

The full list with **What happens / When it occurs / How to avoid** is in `references/gotchas.md`. The four that most often survive review:

1. **`RestContext` is only populated in REST execution or tests that set it** — do not assume it exists in ordinary Apex contexts. `RestRequest()` and `RestResponse()` are public constructors and `RestContext.request` / `.response` are read-write properties, which is the whole test mechanism (apexrefguide L228308–228340, L228428, L228696).
2. **Apex REST security is not automatic beyond authentication** — data access still needs explicit review, and the class's `apiVersion` decides the default.
3. **Returning raw exceptions as response bodies leaks internals** — map failures to stable error contracts, and remember that unhandled exceptions bypass your envelope entirely as a platform `400` or `500` (apexdev L18684, L18693).
4. **Resource classes become brittle fast if business logic lives directly inside them** — versioning pain follows, and the permission-set boundary blurs.

## Output Artifacts

| Artifact | Description |
|---|---|
| REST endpoint review | Findings on contract design, status handling, security, and versioning |
| Resource scaffold | Thin `@RestResource` class with explicit request parsing and response shaping |
| Service class | The business half, extending `templates/apex/BaseService.cls`, with CRUD/FLS via `templates/apex/SecurityUtils.cls` |
| Test class | `RestContext`-driven coverage asserting status codes, envelope `code`, and response headers |
| `*.cls-meta.xml` + `package.xml` | Deployment metadata at `<apiVersion>67.0</apiVersion>`, including the Apex Class Access permission set |
| Contract probe script | cURL calls that assert the happy path plus the platform's `404`/`405` for unmapped URL and missing verb |
| Versioning notes | Guidance for evolving the endpoint without breaking consumers |

---

## Reference Files

| File | Read it when |
|---|---|
| `references/code-examples.md` | You are writing the endpoint — resource + service + DTOs + test class, `.cls-meta.xml`, `package.xml`, `sf apex run test`, and the cURL contract probes |
| `references/gotchas.md` | An endpoint deployed but 404s, returns `500` for a code you set, returns `200` on failure, or works in the dev org and not after packaging — 15 grounded platform behaviours |
| `references/examples.md` | You want the narrative walk-through of a versioned GET and a typed POST before writing code |
| `references/llm-anti-patterns.md` | You are reviewing AI-generated `@RestResource` code, or self-checking your own output |
| `references/well-architected.md` | You are justifying a custom endpoint over the standard APIs, or need the source list |
| `templates/apex-rest-services-template.md` | You are filling in the contract worksheet before any code exists |

## Related Skills

- `apex/apex-security-patterns` — use when the main risk is the sharing or CRUD/FLS posture of the endpoint.
- `apex/exception-handling` — use when the error contract and internal failure mapping need refinement.
- `apex/test-class-standards` — use when REST resource tests are weak or missing request/response assertions.
- `apex/callouts-and-http-integrations` — the outbound mirror of this skill; use when Salesforce is the caller, not the callee.
- `integration/api-versioning-strategy` — use when the question is a deprecation and sunset policy across many endpoints rather than one class's mapping.
- `integration/rest-api-pagination-patterns` — use when the response is a collection that has to be paged rather than returned whole.
- `integration/oauth-flows-and-connected-apps` — use when the open question is how the caller obtains the token in the `Authorization: Bearer` header.
