---
name: api-testing-checklist
description: >
  A fast, ordered methodology for assessing an API end to end — REST/GraphQL/gRPC/SOAP — so nothing
  gets skipped. Load when the target is an API (or recon found one), on "test this API", "checklist",
  methodology triage, or to confirm coverage before reporting. Signals: /api, swagger/openapi.json,
  GraphQL /graphql, gRPC, JSON/XML endpoints, a mobile/SPA backend.
domain: api
type: checklist
stability: learning
modes: [bugbounty, pentest]
severity: info
schema_version: 1
---

# API testing methodology (work top to bottom)

Confirm scope first (`tradecraft-scope-roe`). Each phase links to the skill that goes deep — load it,
work its `cheatsheet.md` where present, and don't mark a phase `failed` until you've covered it
(house rule: fuzz every input/context/encoding, blind/OOB). This is your coverage map.

## 1 · Discover & map the surface
- [ ] Find the API: `/api`, subdomains, JS files (`recon-js-analysis`), mobile/SPA traffic (`recon-content-discovery`)
- [ ] Grab the spec: `swagger.json` / `openapi.json` / GraphQL introspection / `.proto` — enumerate every endpoint, method, param
- [ ] Note auth model (Bearer/JWT/API key/cookie/mTLS), versions (`/v1`,`/v2`), and content types
- [ ] Map roles: create **two accounts** (and an unauth client) — you need them for access-control tests

## 2 · Authentication
- [ ] Token flaws — JWT alg/kid/key confusion (`web-auth-jwt`), API-key leakage/predictability
- [ ] Auth attacks — credential stuffing, weak/OTP flows, token not expiring/rotating (`api-auth-attacks`)
- [ ] Unauthenticated endpoints that shouldn't be

## 3 · Authorization (the #1 API bug class — go deep)
- [ ] **BOLA/IDOR** — swap object IDs between the two accounts on every object-taking endpoint (`api-bola`, `web-idor`)
- [ ] **BFLA** — call admin/privileged functions as a low-priv user; try hidden methods (PUT/DELETE/PATCH)
- [ ] Path/verb tampering, `X-Original-URL`/method override, GraphQL field-level authz

## 4 · Input handling & injection
- [ ] Injection across params, JSON bodies, headers: SQLi (`web-sqli`), NoSQL (`api-mongo-agg-facet-bypass`), command (`web-command-injection`), SSTI (`web-ssti`)
- [ ] SSRF via URL params / webhooks / "fetch from URL" (`web-ssrf`), XXE on XML endpoints (`web-xxe`)
- [ ] Mass assignment — inject extra fields (`role`,`isAdmin`,`price`) (`api-mass-assignment`)

## 5 · Data exposure & business logic
- [ ] Excessive data exposure — endpoints returning more fields than the UI shows (PII, internal flags)
- [ ] Business-logic abuse — price/quantity tampering, negative values, replay, race conditions (`web-race-conditions`, `web-business-logic`)
- [ ] Mass assignment → privilege/state change; parameter pollution (`web-http-parameter-pollution`)

## 6 · Rate limiting & resource consumption
- [ ] Missing/bypassable rate limits (`web-rate-limit-bypass`) — brute, enumeration, cost
- [ ] Unbounded queries / pagination abuse; GraphQL depth/alias/batch amplification

## 7 · Protocol specifics
- [ ] **GraphQL** — introspection, batching, injection, field authz (`api-graphql`)
- [ ] **gRPC** — reflection, message tampering (`api-grpc`)
- [ ] **REST/SOAP** — verb tampering, content-type confusion, version drift (`api-versioning`); fuzz systematically (`api-fuzzing`)

## 8 · Before you report
- [ ] Re-prove each finding from a clean session; anonymise data (`reporting-triage-validation`)
- [ ] Score it (`reporting-cvss-scoring`), then write it up (`reporting-bug-bounty-writeup`)

## Coverage bar
Every endpoint × method exercised; BOLA/BFLA tried across accounts on every object; injection fuzzed
on every input; rate-limit and business-logic checked. A phase is `failed` only after that — else `open`.
