---
name: governance/check-roc-compliance
description: Checks session compliance against a Rule of Constraints policy.
version: 0.1.0
status: experimental
family: governance
role: ProxyAuditor
allowed-tools:
  - view_file
  - write_to_file
policies:
  - E.16 RoC-Autonomy
  - A.15.1 U.Work
outputs:
  - RoCReport
---

# Governance: Check RoC Compliance

## 1. Context

This skill evaluates session activity against a Rule of Constraints policy and records a compliance report with violations and recommended outcomes.

## 2. Inputs

- **context** (required): Bounded context name (safe path segment).
- **session_id** (required): Session identifier (safe path segment).
- **roc_path** (required): Path to the RoC YAML file.
- **used_tools** (optional): Semicolon-delimited list of tools used.
- **approvals** (optional): Semicolon-delimited approval keys satisfied.
- **agent_type** (optional): Agent type performing the check.
- **agent_model** (optional): Agent model identifier.
- **role_assignment** (optional): RoleAssignment for U.Work logging (default: ProxyAuditor).
- **decisions** (optional): Semicolon-delimited DRR ids/paths.
- **timestamp_start** (optional): ISO-8601 timestamp for deterministic output.

## 3. Outputs

- `runtime/contexts/<context>/audits/roc/<session_id>.<timestamp>.roc.md`

## 4. Procedure

1. Validate inputs and load the RoC policy.
2. Compare used tools and approvals to RoC requirements.
3. Write a RoC compliance report.
4. Emit U.Work via `telemetry/log-work` when available.
