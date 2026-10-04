---
name: panelin-gpt-cloud-system
description: Operates Panelin as a single production system, always synchronizing GPT Builder configuration with Google Cloud runtime changes. Use when working on prompts, actions, OpenAPI, backend routes, auth, deploy, or any issue that can diverge GPT and Cloud behavior.
---

# Panelin GPT + Cloud System

**Before working:** Read `docs/team/knowledge/GPTCloud.md` if it exists.

## Purpose

Treat Panelin as one end-to-end system. Every change must consider both:

- GPT layer (instructions, actions, operationIds, builder config)
- Cloud layer (runtime endpoints, auth, env vars, deploy health)

## Propagation

Si el cambio afecta a Integrations, Design o Networks: actualizar `docs/team/PROJECT-STATE.md` y consultar tabla de propagación en `docs/team/PROJECT-TEAM-FULL-COVERAGE.md` §4.

## Mandatory Rule

Never close a task as done if only one layer was touched.

If GPT changed, validate Cloud compatibility.
If Cloud changed, validate GPT compatibility.

## Workflow

Copy this checklist and keep it updated:

```text
System Sync Progress:
- [ ] 1. Define scope (GPT, Cloud, or both)
- [ ] 2. Audit current GPT configuration
- [ ] 3. Audit current Cloud runtime
- [ ] 4. Apply coordinated changes
- [ ] 5. Run cross-layer smoke tests
- [ ] 6. Publish sync report
```

### 1) Define scope

Identify change type:

- GPT-only request
- Cloud-only request
- Incident/debug
- Full rollout

Then expand to include the missing counterpart layer.

### 2) Audit GPT layer

Check at minimum:

- active OpenAPI spec loaded in Builder
- operationIds expected by instructions
- auth type configured in Actions
- instruction behavior for error handling and qualification

### 3) Audit Cloud layer

Check at minimum:

- base URL and path availability
- auth enforcement behavior (`401` vs public routes)
- required env vars present
- runtime health and readiness

### 4) Apply coordinated changes

When updating contracts:

- keep operationIds stable, or update instructions + routing together
- keep schema names and payload fields consistent with runtime
- avoid placeholder URLs in production profile

### 5) Cross-layer smoke tests

Minimum required:

1. Public health test
2. Protected endpoint auth test
3. Core quote flow test
4. Persistence test (sheet/KB/artifact path if applicable)
5. GPT conversational test that calls real tools

### 6) Sync report format

Return exactly:

1. GPT changes applied
2. Cloud changes applied
3. Cross-layer test results (PASS/FAIL)
4. Remaining drift/risk
5. Next mandatory action

## Guardrails

- Do not expose secrets in prompts, files, or logs.
- Do not mark production-ready with placeholder endpoints.
- If backend returns inconsistent business values (e.g., zero totals), flag as backend defect and block final quote output.
- Prefer one canonical "live profile" for Builder aligned to currently deployed Cloud contracts.
