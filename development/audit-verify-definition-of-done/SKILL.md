---
name: audit/verify-definition-of-done
description: Verifies Definition of Done checks and generates a DoD report.
version: 0.1.0
status: experimental
family: audit
role: ProxyAuditor
allowed-tools:
  - run_command
  - view_file
  - write_to_file
policies:
  - E.19 Definition of Done
  - A.15.1 U.Work
outputs:
  - DoDReport
---

# Audit: Verify Definition of Done

## 1. Context

This skill verifies Definition of Done checks for a session and emits a DoD report under the runtime context.

## 2. Inputs

- **context** (required): Bounded context name (safe path segment).
- **session_id** (required): Session identifier (safe path segment).
- **required_artifacts** (optional): Semicolon-delimited required artifact paths.
- **allow_empty_diff** (optional): Allow empty git diff (`true`/`false`).
- **test_command** (optional): Override test command (default: `bun test`).
- **check_command** (optional): Override fpf check command (default: `bun packages/fpf/bin/fpf check`).
- **agent_type** (optional): Agent type performing the DoD check.
- **agent_model** (optional): Agent model identifier.
- **role_assignment** (optional): RoleAssignment for U.Work logging (default: ProxyAuditor).
- **decisions** (optional): Semicolon-delimited DRR ids/paths.
- **timestamp_start** (optional): ISO-8601 timestamp for deterministic output.

## 3. Outputs

- `runtime/contexts/<context>/audits/dod/<session_id>.<timestamp>.dod.md`

## 4. Procedure

1. Validate inputs and resolve required artifacts (including the session record).
2. Run git diff, tests, and fpf check (unless overridden).
3. Write a DoD report with pass/fail status.
4. Emit U.Work via `telemetry/log-work` when available.
