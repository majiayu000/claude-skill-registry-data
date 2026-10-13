---
name: backend-incident-hotfix
description: 'Handle production backend incidents and urgent hotfixes in HIVMeet with controlled risk. Use for outage response, rapid diagnosis, minimal safe patching, rollback planning, and post-fix validation.'
argument-hint: 'Describe incident symptom, affected endpoint/service, severity, and time constraints.'
user-invocable: true
---

# Backend Incident Hotfix

## Purpose
Restore service quickly without creating secondary regressions or security/privacy violations.

## Use When
- Production incident affects availability, correctness, or security
- Critical endpoint is failing for users
- Emergency patch is required under time pressure

## Severity Modes
- Sev1: Major outage or critical security exposure
- Sev2: High-impact feature unavailable/degraded
- Sev3: Limited-scope issue with workaround

## Mandatory Workflow

### 1. Stabilize and Scope
- Define impacted user journeys, endpoints, and modules
- Assess severity and current blast radius
- Decide immediate mitigation (feature flag, rate reduction, temporary disable)

### 2. Evidence-First Diagnosis
- Capture exact error signatures and timestamps
- Correlate logs, recent changes, and failing requests
- Confirm root cause candidate before patching

### 3. Minimal Safe Patch
- Implement smallest change that restores critical behavior
- Preserve API contract unless incident mitigation requires temporary controlled deviation
- Avoid unrelated refactors

### 4. Security and Privacy Guard
- Ensure patch does not expose sensitive data
- Keep authentication/permission checks intact
- Ensure logs remain token/PII safe

### 5. Validation Under Time Constraints
- Validate primary failing scenario first
- Validate at least one adjacent critical flow
- Run targeted tests for changed area

### 6. Rollback and Forward Plan
- Define rollback trigger and command path
- Document follow-up hardening tasks if hotfix is tactical
- Create post-incident action list

### 7. Output Contract
1. Severity and impact scope
2. Root cause evidence
3. Hotfix diff summary
4. Validation evidence
5. Rollback plan and follow-up items

## Quality Gates
- No hotfix merged without explicit rollback path
- No emergency change that bypasses critical authz controls
- No closure without at least minimal non-regression evidence
