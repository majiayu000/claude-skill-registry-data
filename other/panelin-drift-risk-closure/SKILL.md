---
name: panelin-drift-risk-closure
description: Closes remaining GPT-Cloud drifts and go-live risks for Panelin as one system. Use when endpoints are partially deployed, Builder points to wrong service, auth keys drift, quote validation is inconsistent, or user asks to finish pending risks end-to-end.
---

# Panelin Drift & Risk Closure

## Purpose

Resolve all remaining drifts/risks between GPT configuration and Cloud runtime, and leave an operationally verifiable go-live state.

## Mandatory Rule

Treat GPT + Cloud as one system. No task is complete unless both layers are validated.

## Inputs Expected

- Active service URLs (legacy and target)
- Current Action OpenAPI in Builder
- Runtime auth mode and secret source
- Current blocker list (404/401/business inconsistencies)

## Workflow

Copy and keep updated:

```text
Drift Closure Progress:
- [ ] 1. Snapshot current drift matrix
- [ ] 2. Select canonical live profile
- [ ] 3. Align GPT artifacts to canonical runtime
- [ ] 4. Align Cloud runtime to contract
- [ ] 5. Run cross-layer smoke + business checks
- [ ] 6. Publish closure report and mandatory follow-ups
```

### 1) Snapshot current drift matrix

Capture:

- GPT Action server URL vs deployed service URL
- operationIds in Builder vs operationIds available in runtime
- auth behavior (public endpoints and protected endpoints)
- business consistency (`unit_price`, `total`)

### 2) Select canonical live profile

Choose one production profile only:

- `live-legacy` OR `keyword-first target`

Mark all other profiles as non-canonical until migrated.

### 3) Align GPT artifacts

Update together:

- OpenAPI file used by Builder
- builder instructions file
- routing/state/required-fields files
- setup checklist

Ensure operationIds and payloads match runtime exactly.

### 4) Align Cloud runtime

Ensure:

- required endpoints exist
- required env vars exist
- auth key/token is configured
- error responses are JSON

### 5) Cross-layer tests (required)

Minimum:

1. Health endpoint -> 200
2. Protected endpoint without auth -> 401
3. Protected endpoint with auth -> 200
4. Core quote flow -> positive totals
5. GPT conversational tool call path -> no schema/runtime mismatch

### 6) Closure report

Return exactly:

1. GPT changes applied
2. Cloud changes applied
3. Cross-layer test results (PASS/FAIL)
4. Remaining drift/risk
5. Next mandatory action

## Guardrails

- Never expose secrets in files/prompts/logs.
- Do not declare ready if quote totals are zero for valid products.
- Do not keep multiple conflicting production URLs in active artifacts.
