---
name: scope-safety-guard
description: Review or plan changes that affect permissions, security boundaries, sensitive operations, external effects, or safety constraints.
metadata:
  short-description: Enforce safety and external-effect boundaries
---

# scope-safety-guard

## Purpose During Development

Use this skill as a mandatory safety review layer whenever a change can affect permissions, security boundaries, external effects, sensitive operations, or generated guidance that could drive unsafe behavior.

This is a reusable development-time reasoning framework. It is not runtime code and must not be coupled into the product being reviewed.

## When To Apply

- changes to auth, authorization, policy, permissions, or safety checks
- changes that add or alter network access, file writes, execution, or other side effects
- changes that generate recommended actions for users or downstream agents
- PR review for any security-sensitive path

## What To Inspect

- repository safety and compliance guidance in `AGENTS.md`
- the policy or guard modules touched by the change
- integration points that can bypass safety checks
- fallback paths and error paths
- tests for denied, out-of-scope, or unsafe scenarios

## Rules To Enforce

- safety checks must be explicit and consistently applied
- side effects must respect repository boundaries and permissions
- fallback behavior must not weaken safety guarantees
- generated action guidance must remain conservative and bounded
- convenience must not override policy

## Common Anti-Patterns To Catch

- adding a new side-effect path without the standard guardrails
- validating safety in the happy path but not in fallback or retry paths
- loosening scope or permission checks during refactors
- generated recommendations that exceed the repository’s safety model
- performance-driven shortcuts that skip security or safety controls

## Expected Output From The Agent

- mandatory safety findings
- guardrail gaps
- risk analysis
- required fixes before merge
- targeted tests for denied and boundary scenarios

## Output Structure

- Summary
- Key Findings
- Risks
- Affected Files
- Affected Areas
- Suggested Improvements
- Suggested Tests
- Skills applied

## Example Usage

"Review this PR for permission, safety, and side-effect regressions."

"Use this skill to verify that a new automated action path stays within repo policy."
