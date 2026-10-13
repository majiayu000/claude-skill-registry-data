---
name: backend-testing-strategy
description: 'Plan and execute high-value backend tests for HIVMeet. Use to select unit/integration/API tests by risk, enforce non-regression, and keep feedback loops fast with evidence-based coverage.'
argument-hint: 'Describe changed backend files, impacted endpoints/services, and required confidence level.'
user-invocable: true
---

# Backend Testing Strategy

## Purpose
Maximize confidence per minute by targeting tests to changed behavior while preserving strong regression coverage.

## Use When
- After backend code changes
- Before merge of risky endpoint/service modifications
- During hotfix validation
- When full suite is too slow for iteration

## Confidence Modes
- Quick: direct unit and critical smoke tests
- Standard: quick plus endpoint integration paths
- Strict: standard plus cross-module and failure-path coverage

## Mandatory Workflow

### 1. Change Surface Mapping
- List changed files by app and layer (view, serializer, service, model, task)
- Map each file to behaviors/endpoints affected
- Mark shared dependencies and high-blast-radius components

### 2. Risk Classification
- Low: localized refactor without behavior changes
- Medium: serializer/service/view logic changes
- High: auth, permissions, contracts, migrations, async side effects

### 3. Test Selection
- Unit tests for changed business logic
- API tests for modified endpoints and status mapping
- Integration tests for cross-layer behavior
- Add one regression test reproducing the original bug if applicable

### 4. Failure-Path Coverage
- Validate expected 4xx paths
- Validate expected 5xx containment behavior where relevant
- Validate permissions/auth boundaries

### 5. Execution and Escalation
- Run selected tests and collect failures
- If failures indicate broader risk, escalate mode (quick -> standard -> strict)
- Report explicit residual risk for unexecuted scopes

### 6. Output Contract
1. Selected tests with rationale
2. Confidence mode used
3. Results summary
4. Escalation decisions
5. Remaining untested risk

## Quality Gates
- No high-risk change without at least one failure-path test
- No endpoint change without API-level validation
- No bug fix closed without a regression test recommendation
