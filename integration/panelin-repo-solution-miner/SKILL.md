---
name: panelin-repo-solution-miner
description: Audits Panelin repositories to find already-implemented solutions and convert them into a concrete reuse plan for GPT Builder integration and go-live. Use when the user asks to analyze GPT-Panelin-Calc, Panelin1103, mercadolibre-connector, compare implementations, avoid rework, or unblock full GPT integration.
---

# Panelin Repo Solution Miner

## Purpose

Identify what is already implemented across related Panelin repos, avoid duplicate work, and produce an execution-ready reuse plan for OpenAI GPT Builder integration.

## Inputs Expected

- Target repos (default):
  - `Panelin1103` (master GPT config/governance)
  - `Calculadora-BMC-GPT`
  - `GPT-Panelin-Calc` (legacy architecture patterns)
  - `mercadolibre-connector` (OAuth/token layer)
- Goal context:
  - full GPT Builder integration (calc + ML + Wolf)
  - blockers to resolve (URLs, auth, endpoint status)

If a repo is not available locally, fetch public docs/README from GitHub and mark confidence as "medium".

## Mandatory Rules

1. Prefer reuse over re-implementation.
2. Do not invent endpoint URLs, secrets, or auth modes.
3. Distinguish clearly between:
   - implemented in code
   - documented but not deployed
   - placeholder/stub
4. Validate claims with file evidence before recommending.
5. Keep output concise and operational.

## Workflow

Copy and maintain this checklist:

```text
Solution Mining Progress:
- [ ] 1. Inventory candidate repos and key files
- [ ] 2. Extract reusable implemented capabilities
- [ ] 3. Map gaps/blockers for full integration
- [ ] 4. Propose reuse-first implementation path
- [ ] 5. Produce execution checklist with owners/inputs
```

### 1) Inventory candidate repos and key files

Prioritize:

- `gpt/actions/*.yaml`
- `gpt/instructions/*.md`
- `gpt/config/*.json`
- `docs/builder-setup-checklist.md`
- `docs/secret-contract.md`
- runtime validation scripts (`scripts/*health*`, `scripts/*smoke*`)

### 2) Extract reusable implemented capabilities

Classify each finding:

- **Implemented**: code + runnable path present
- **Reusable Pattern**: architecture/documented flow proven elsewhere
- **Placeholder**: contract exists but runtime not live

Examples of high-value reusable assets:

- consolidated OpenAPI for single Builder Action
- instruction packs under Builder character limits
- auth/token contract and env-variable policy
- health/smoke automation and release evidence artifacts

### 3) Map gaps/blockers for full integration

Report blockers by category:

- **Runtime**: endpoints return 404/5xx, service not deployed
- **Contract**: placeholder URLs, missing auth config
- **Builder**: schema warnings, action constraints, save failures
- **Operational**: missing secrets, unknown ownership

For each blocker include:

- exact symptom
- evidence file or test
- minimum input needed to unblock

### 4) Propose reuse-first implementation path

Default strategy order:

1. Use `Panelin1103` as canonical config/governance baseline.
2. Use one consolidated Action in GPT Builder when domains collide.
3. Reuse `mercadolibre-connector` for ML OAuth/token lifecycle.
4. Keep Wolf behind explicit bearer-token contract until URL is live.
5. Certify with existing health/smoke scripts before go-live.

### 5) Produce execution checklist with owners/inputs

Generate a short plan with:

- exact files to adopt/update
- environment variables/secrets required
- deployment verifications
- go/no-go criteria

## Final Output Format

Return exactly:

1. Reusable solutions already implemented
2. Confirmed blockers (with evidence)
3. Reuse-first action plan (ordered)
4. Required inputs from user/team
5. Definition of done for 100% GPT integration
