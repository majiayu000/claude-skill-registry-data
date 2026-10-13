---
name: release-readiness
description: 'Prepare HIVMeet frontend changes for release with a structured readiness gate. Use for pre-release checks, quality validation, privacy safety review, and deployment confidence reporting. Includes build/analyze/test gates, contract risk review, and release decision checklist.'
argument-hint: 'Describe release scope, target platform(s), and blockers already known.'
user-invocable: true
---

# Release Readiness

## Purpose
Standardize final verification before delivery to reduce production incidents and rollback risk.

This skill is project-scoped and specific to HIVMeet.

## Use When
- Preparing a sprint/demo/release candidate
- Merging high-impact features across modules
- Closing a hotfix batch requiring confidence report

## Readiness Gates
- Code quality gate
- Functional gate
- Integration gate
- Privacy and content safety gate
- Build gate

## Mandatory Workflow

### 1. Define Release Scope
- List included features/fixes
- List explicitly excluded items
- Identify affected modules and risk hotspots

### 2. Run Code Quality Gate
- flutter analyze
- Formatting consistency on changed code
- No unresolved TODO linked to critical behavior

### 3. Run Functional Gate
- Validate critical user journeys for impacted modules
- Validate main error states and empty states
- Validate i18n coverage for new visible strings (FR/EN)

### 4. Run Integration Gate
- Verify backend contract alignment for touched endpoints
- Verify failure handling for key API statuses
- Verify no unintended dependency break between layers

### 5. Run Privacy And Safety Gate
- No PII logging introduced
- Sensitive flows preserve secure storage requirements
- User-facing wording remains respectful and non-stigmatizing

### 6. Run Build Gate
- Debug build feasibility for target platform(s)
- Release build feasibility for target platform(s)
- Record build blockers if any

### 7. Produce Release Decision
- Ready: all critical gates passed
- Conditionally ready: non-critical residual risks documented
- Not ready: blocker list with owner and next action

### 8. Output Contract
1. Release scope and impacted modules
2. Gate-by-gate pass/fail summary
3. Critical blockers and mitigations
4. Residual risks
5. Final decision with rationale

## Notes
- Prefer explicit evidence over optimistic assumptions
- If backend changes are required, attach precise BACKEND_*.md references
- Language for responses: French
