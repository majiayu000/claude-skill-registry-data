---
name: issue-to-plan
description: Turn issues, bug reports, feature requests, and engineering tasks into implementation plans. Use when Codex is asked to analyze an issue, clarify scope, propose code changes, define acceptance criteria, identify affected areas, or plan tests before implementation.
license: MIT
---

# Issue To Plan

## Core Workflow

1. Restate the requested behavior, current behavior, user impact, and success
   criteria.
2. Identify missing reproduction details, environment, data, permissions,
   dependencies, and constraints.
3. Inspect or request the relevant code, docs, logs, tickets, and tests before
   proposing risky changes.
4. Break the work into small implementation steps with affected modules,
   interfaces, migrations, configuration, or documentation.
5. Define acceptance criteria and verification before coding starts.
6. Flag assumptions, sequencing risks, and decisions that need owner approval.

## Safety Rules

- Do not claim a bug is fixed before implementation and validation.
- Do not recommend broad rewrites when a smaller change can satisfy the issue.
- Do not edit protected branches, merge, deploy, or close issues without
  explicit approval.
- Escalate when requirements conflict, reproduction is missing, security risk
  appears, or the change touches data, billing, auth, or production operations.

## Deliverable Shape

For engineering plans, provide:

- Issue summary
- Known facts and missing information
- Affected areas
- Proposed implementation steps
- Acceptance criteria
- Test and verification plan
- Regression risks
- Open questions or approvals needed

## References

- Read `references/issue-to-plan-checklist.md` when converting an issue, bug
  report, or feature request into an engineering plan.
