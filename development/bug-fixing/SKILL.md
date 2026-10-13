---
name: bug-fixing
description: 'Diagnose and fix HIVMeet frontend bugs, errors, anomalies, and performance issues. Use when debugging compilation/runtime failures, state bugs, API integration mismatches, and regressions. Includes hypothesis-first file targeting, root-cause validation, backend escalation rules, and non-regression checks.'
argument-hint: 'Describe the bug, reproduction steps, observed behavior, expected behavior, and module.'
user-invocable: true
---

# Bug Fixing and Error Resolution

## Purpose
Provide a consistent, high-quality remediation workflow for HIVMeet issues while protecting user privacy and maintaining functional stability.

This skill is project-scoped and specific to HIVMeet.

## Use When
- A feature behaves incorrectly compared to expected behavior
- Flutter/Dart compilation or runtime errors appear
- State management is inconsistent (BLoC/Cubit/UI desync)
- API responses or contracts create integration failures
- Performance degradations are reported

## Problem Types
- Bugs: functional dysfunctions
- Errors: compile/runtime/exceptions/crashes
- Anomalies: unexpected behavior
- Performance issues: latency, slow UI, excess resource usage

## Mandatory Workflow

### 1. Reproduce The Problem
- Confirm exact reproduction steps
- Capture observed versus expected behavior
- Record scope (screen, module, environment)

### 2. Collect Evidence
- Gather logs and relevant traces
- Capture screenshots/video if useful
- Record deterministic repro conditions

### 3. Build File Hypothesis (Do Not Scan Whole Project First)
- Propose a short list of likely files by module and layer
- Validate this list quickly
- If incorrect, move to focused search

Example hypothesis for a like counter issue:
- lib/presentation/blocs/discovery/discovery_bloc.dart
- lib/presentation/blocs/discovery/discovery_state.dart
- lib/domain/usecases/match/like_profile.dart
- lib/data/repositories/match_repository_impl.dart
- lib/data/datasources/remote/matching_api.dart
- lib/presentation/pages/discovery/discovery_page.dart

### 4. Analyze Root Cause
- Trace data flow from UI to domain to data layers
- Identify the first incorrect state, transformation, or contract mismatch
- Distinguish symptom from root cause

### 5. Validate Hypothesis
- Confirm suspected file and logic path with concrete evidence
- Reject and revise hypothesis if evidence does not fit

### 6. Propose And Apply Minimal Fix
- Choose smallest safe change that resolves root cause
- Preserve architecture boundaries and existing conventions
- Avoid broad refactors unless explicitly required

### 7. Classify Resolution Path
- Frontend compilation/runtime/logic issue:
  - Fix directly in code
- Backend API/data issue (4xx/5xx, missing endpoint, response schema mismatch, database-side issue):
  - Create BACKEND_[ERROR_TYPE]_[SHORT_DESCRIPTION].md only after validating the issue cannot be resolved in frontend
  - Include observed issue, root cause hypothesis, impact, and concrete backend request
- Integration mismatch:
  - Adjust frontend safely and document backend coordination needs

### 8. Validate Non-Regression
- Re-test original scenario
- Re-test related flows in the same module
- Run analyzer/tests/format checks as appropriate
- Ensure no new errors introduced by the fix

### 9. Provide Completion Output
For each bug fix task, report:
1. Exact files modified
2. Complete fix content (no pseudocode)
3. Before/after behavior summary
4. Non-regression verification
5. Suggested test coverage (mandatory section)
6. Problem -> cause -> solution summary

## Decision Matrix
| Category | Typical Signal | Action |
|---|---|---|
| Frontend - Compilation | Dart errors, missing imports | Fix directly |
| Frontend - Runtime | Null/type/state exceptions | Fix directly |
| Frontend - Logic | Wrong condition or stale state | Fix directly |
| Backend - API | 4xx/5xx, endpoint mismatch | Create BACKEND_*.md |
| Backend - Data | Invalid schema/payload shape | Create BACKEND_*.md |
| Integration | Contract mismatch | Adjust frontend + document |

## Security and Privacy Rules
- Never log PII (email, token, user ID, phone, exact location)
- Use flutter_secure_storage for tokens
- Sanitize logs and evidence artifacts
- Keep wording respectful and non-stigmatizing for HIVMeet context

## Diagnostic Toolkit
- flutter analyze
- flutter test
- dart format lib/
- flutter run -d <device_id>
- flutter build apk --debug
- flutter build apk --release

## Validation Checklist
### Phase 1: Diagnostic
- Problem reproduced
- Evidence collected
- Suspect files identified (hypothesis)
- Hypothesis validated

### Phase 2: Fix
- Root cause identified
- Solution implemented
- Code compiles/analyzes cleanly

### Phase 3: Validation
- Problem resolved
- No regressions introduced
- Tests executed
- Backend documentation created when needed

## Notes
- Prioritize minimal-risk corrections
- For backend issues, produce precise, actionable documentation rather than vague requests
- Language for responses: French
