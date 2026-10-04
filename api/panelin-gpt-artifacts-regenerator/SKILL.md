---
name: panelin-gpt-artifacts-regenerator
description: Regenerates GPT configuration artifacts so instructions, actions, routing, checklists, and knowledge packaging remain aligned with current business objectives and deployed Cloud contracts. Use when objectives change, operationIds drift, OpenAPI changes, quote flow fails, or GPT behavior diverges from runtime.
---

# Panelin GPT Artifacts Regenerator

## Purpose

Regenerate and align GPT artifacts as a coherent package:

- Instructions
- OpenAPI profile(s)
- Action routing
- Builder setup checklist
- Safe knowledge upload set

Always align with live Cloud behavior and target business workflow.

## Inputs Expected

- Functional objectives (intake, qualification, quote, persistence, supervision, ML mode).
- Active runtime contract (base URL, auth mode, live paths/operationIds).
- Canonical repo context:
  - `Calculadora-BMC-GPT`
  - `Panelin1103` (when needed for reference consistency)

## Mandatory Rules

1. Regenerate artifacts as a bundle, never one file in isolation.
2. Do not invent endpoints, operationIds, auth schemes, or field names.
3. If runtime and docs conflict, treat runtime as live truth and mark drift explicitly.
4. Keep legacy/live and target-state profiles separated when both are needed.
5. Block "ready" status if quote totals or unit prices are zero/invalid.

## Workflow

Copy and track:

```text
Artifact Regen Progress:
- [ ] 1. Capture objective + runtime contract
- [ ] 2. Validate live endpoints and auth behavior
- [ ] 3. Regenerate GPT artifacts bundle
- [ ] 4. Apply safety guards and consistency checks
- [ ] 5. Produce rollout + verification report
```

### 1) Capture objective + runtime contract

Collect:

- required business flow states
- required outputs (sheet updates, drive artifacts, PDF/share link, ML response mode)
- live auth mode (`X-API-Key`, bearer, etc.)
- active endpoint family (`/calculate_quote` vs `/calc/cotizar`, etc.)

### 2) Validate live endpoints and auth behavior

Minimum checks:

- public health endpoint
- protected endpoint without auth (must fail with auth error)
- protected endpoint with auth (must execute)

### 3) Regenerate GPT artifacts bundle

Regenerate/update together:

- `gpt/actions/openapi-*.{yaml,json}`
- `gpt/instructions/*builder*.md`
- `gpt/config/action-routing*.json`
- `docs/builder-setup-checklist*.md`

If dual profile is required:

- create explicit `live` profile (current deployment)
- keep `target-state` profile separately documented

### 4) Apply safety guards and consistency checks

Enforce in instructions/checklist:

- exact SKU passthrough from search to quote
- no final quote if `unit_price <= 0` or `total <= 0`
- one-missing-field-at-a-time qualification loop
- explicit human supervision gate before "sent"
- ML mode: compliant short response to maximize engagement before contact data

### 5) Produce rollout + verification report

Include:

- files regenerated
- runtime checks executed (with status)
- known drifts and blockers
- go-live recommendation (ready/not ready)

## Safe Knowledge Packaging Policy

Upload to GPT Knowledge only stable process/context files:

- instruction/playbook files
- state machine / required fields / gating policies
- payload/reference docs

Do not upload pricing-master sources that can diverge from runtime pricing authority.

## Final Output Format

Return exactly:

1. Objective alignment summary
2. Artifacts regenerated (by file path)
3. Runtime compatibility checks (PASS/FAIL)
4. Remaining drift and risk
5. Next mandatory action
