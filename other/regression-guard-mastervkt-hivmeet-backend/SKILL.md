---
name: regression-guard
description: 'Run high-impact non-regression validation for HIVMeet frontend changes. Use before merge after bug fixes or feature work to verify critical user journeys, state transitions, and API interactions. Includes targeted regression matrix, risk scoring, and go/no-go summary.'
argument-hint: 'Describe changed files, affected modules, and desired confidence level (quick/standard/strict).'
user-invocable: true
---

# Regression Guard

## Purpose
Prevent functional regressions by running targeted, risk-based checks on critical HIVMeet flows.

This skill is project-scoped and specific to HIVMeet.

## Use When
- After any bug fix in Discovery, Auth, Messaging, Profile, Premium
- Before merging multi-file refactors
- After API contract or state management changes
- Before release candidate validation

## Confidence Modes
- Quick: core happy paths only
- Standard: happy paths + key error paths
- Strict: cross-module regression sweep + edge cases

## Mandatory Workflow

### 1. Build Change Risk Map
- List changed files by layer (presentation/domain/data)
- Identify touched modules and shared dependencies
- Assign risk level: low/medium/high

### 2. Generate Targeted Regression Matrix
For each affected module, define checks:
- Entry point and navigation
- Main user action
- State update and UI consistency
- API success and failure handling
- Persistence/session behavior if relevant

### 3. Execute Priority Flows
Always include:
- Auth session continuity (token, logout safety)
- Discovery interaction integrity (swipe/like/pass counters and state)
- Messaging stability (conversation open/send/refresh)
- Profile read/edit consistency

### 4. Validate Technical Signals
- flutter analyze clean for impacted files
- Relevant tests pass for impacted scope
- No new runtime exceptions in inspected logs

### 5. Evaluate Regressions
- Confirm or reject each matrix check with evidence
- Mark blockers versus acceptable residual risk
- If blocker exists, return to bug-fixing workflow

### 6. Output Contract
1. Risk map and confidence mode used
2. Regression matrix with pass/fail per flow
3. New regressions detected (if any)
4. Residual risks and monitoring suggestions
5. Merge recommendation: go / no-go

## Check Heuristics
- Prioritize modules with shared models and repositories
- Prioritize flows with asynchronous state transitions
- Prioritize screens with recent backend contract changes

## Notes
- Keep checks realistic and tied to actual changed scope
- Language for responses: French
