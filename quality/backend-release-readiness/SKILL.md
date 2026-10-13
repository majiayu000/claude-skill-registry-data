---
name: backend-release-readiness
description: 'Run a backend-focused release gate for HIVMeet. Use to validate API contract stability, security posture, migration safety, test confidence, and operational readiness before deployment.'
argument-hint: 'Describe release scope, affected apps/endpoints, and known blockers.'
user-invocable: true
---

# Backend Release Readiness

## Purpose
Prevent production incidents by applying a consistent, evidence-based go/no-go process for backend deployments.

## Use When
- Preparing release candidate or hotfix deploy
- Validating high-impact backend merges
- Performing final readiness review before production

## Readiness Gates
- Contract gate
- Security gate
- Data/migration gate
- Testing gate
- Operations/observability gate

## Mandatory Workflow

### 1. Release Scope and Risk
- List included changes by app/module
- Mark high-risk areas (auth, payments, matching, messaging)
- List explicit exclusions and deferred items

### 2. Contract Gate
- Validate modified endpoints against API documentation
- Validate success/error payload stability
- Validate status code consistency

### 3. Security Gate
- Validate permissions and object access controls
- Validate PII-safe logs and sensitive data handling
- Validate relevant HTTPS/CORS/JWT settings posture

### 4. Data and Migration Gate
- Validate migration ordering and reversibility strategy
- Validate data backfill integrity checks
- Validate rollback instructions for risky changes

### 5. Testing Gate
- Run required tests by risk level
- Verify bugfix regressions are covered
- Record untested risk explicitly

### 6. Operations and Monitoring Gate
- Confirm logging/alerts for changed critical paths
- Confirm runbooks for failure recovery exist
- Confirm deployment and post-deploy verification steps

### 7. Release Decision
- Ready: no critical blockers
- Conditionally ready: non-critical residual risks accepted
- Not ready: blockers with owner and immediate action

### 8. Output Contract
1. Gate-by-gate pass/fail matrix
2. Blockers and mitigations
3. Residual risks
4. Final recommendation and rationale

## Quality Gates
- No release approval without explicit contract and test evidence
- No high-risk migration without rollback/recovery clarity
- No critical path change without observability confirmation
