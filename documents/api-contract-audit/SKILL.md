---
name: api-contract-audit
description: 'Audit and secure HIVMeet frontend-backend contracts before and after implementation. Use when integrating endpoints, validating DTO mapping, handling 4xx/5xx responses, or diagnosing API mismatches. Includes endpoint checklist, payload validation, failure-path coverage, and backend escalation format.'
argument-hint: 'Describe module, endpoint(s), request/response contract, and current mismatch risk.'
user-invocable: true
---

# API Contract Audit

## Purpose
Reduce integration regressions by validating endpoint contracts end-to-end before merge.

This skill is project-scoped and specific to HIVMeet.

## Use When
- Integrating a new endpoint in Auth, Discovery, Messaging, Profile, Premium, or Resources
- Refactoring repository/data source layers
- Investigating API mismatch symptoms (unexpected nulls, missing fields, wrong status handling)
- Preparing a backend change request

## Mandatory Workflow

### 1. Define Contract Surface
- Identify endpoint method and path
- Identify required headers and auth mode
- Identify request body/query/path params
- Identify expected success and error shapes

### 2. Source Of Truth Verification
- Check API_DOCUMENTATION.md first
- Cross-check module docs in docs/FRONTEND_*_API.md when needed
- Flag any disagreement between specs and observed payloads

### 3. Hypothesis-First File Targeting
- Start with likely files only:
  - lib/data/datasources/remote/**
  - lib/data/repositories/**
  - lib/data/models/**
  - lib/domain/repositories/**
  - lib/domain/usecases/**
- Expand search only if evidence contradicts initial hypothesis

### 4. Request/Response Mapping Audit
- Validate request keys and value types
- Validate model parsing and null safety
- Ensure optional fields are safely defaulted
- Ensure enum and date parsing are consistent and reversible when required

### 5. Error Path Coverage
- Validate behavior for 400/401/403/404/409/422/429/5xx
- Ensure each known status maps to deterministic UX state
- Confirm no raw backend error leaks to user-facing text

### 6. Contract Decision
- If frontend mapping is wrong: fix frontend
- If contract doc is outdated: document discrepancy
- If backend behavior is incompatible: create BACKEND_[TYPE]_[DESCRIPTION].md with concrete request

### 7. Non-Regression Validation
- Re-test the audited endpoint happy path
- Re-test neighboring flows that share the same models/repositories
- Run analyzer/tests impacted by the change

### 8. Output Contract
1. Audited endpoints and status codes
2. Files verified/modified
3. Contract discrepancies found
4. Fixes applied and why
5. Backend action required (if any)
6. Residual risks and test recommendations

## Quality Gates
- No undefined JSON key access in audited code path
- No unchecked null parsing in required fields
- Explicit handling for expected error status families
- User messages remain i18n-ready and privacy-safe

## Notes
- Keep changes minimal and traceable to one contract risk at a time
- Language for responses: French
