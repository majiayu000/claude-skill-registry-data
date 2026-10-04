---
name: test-strategy-reviewer
description: Assess verification scope, regression protection, and risk-based test coverage for changes under review or implementation.
metadata:
  short-description: Define the minimum safe verification bar
---

# test-strategy-reviewer

## Purpose During Development

Use this skill when Codex and similar AI coding agents need to assess whether a change has adequate verification, regression protection, and test scope.

This is a reusable development-time reasoning framework. It is not runtime code and must not be coupled into the product being reviewed.

## When To Apply

- any risky feature or refactor
- PR review where coverage is unclear
- bug fixes that need recurrence prevention
- contract, safety, or LLM behavior changes

## What To Inspect

- existing unit, integration, and end-to-end tests
- the diff’s risk profile
- code paths that can regress silently
- fixtures and golden data
- observed gaps between behavior and verification

## Rules To Enforce

- tests should reflect risk, not just code movement
- boundary behavior deserves explicit verification
- bug fixes should add recurrence protection when practical
- contract changes should verify both producer and consumer expectations
- performance and safety claims need dedicated validation, not implicit trust

## Common Anti-Patterns To Catch

- only testing happy paths for risky code
- no regression test for a claimed bug fix
- relying on manual verification for repeatable logic
- adding a contract without fixture or schema coverage
- treating unchanged tests as proof of low risk

## Expected Output From The Agent

- coverage gaps
- risk-based test recommendations
- minimal acceptable verification bar
- follow-up test debt notes

## Output Structure

- Summary
- Key Findings
- Risks
- Affected Files
- Coverage Gaps
- Suggested Improvements
- Suggested Tests
- Skills applied

## Example Usage

"Review this PR for missing regression coverage and verification blind spots."

"Use this skill to define the minimum test plan for a high-risk refactor."
