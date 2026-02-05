---
name: workflow/respond-to-approval
description: Records a response to an approval request.
version: 0.1.0
status: experimental
family: workflow
role: Strategist
allowed-tools:
  - view_file
  - write_to_file
policies:
  - E.16 RoC-Autonomy
  - A.15.1 U.Work
outputs:
  - ApprovalResponse
---

# Workflow: Respond to Approval

## 1. Context

This skill records an approval decision linked to a prior approval request for auditability and gating.

## 2. Inputs

- **context** (required): Bounded context name (safe path segment).
- **session_id** (required): Session identifier (safe path segment).
- **approval_id** (required): Approval identifier (safe path segment).
- **decision** (required): Approval decision (`approved`, `denied`, `needs-review`).
- **responded_by** (optional): Responder label.
- **notes** (optional): Response notes or conditions.
- **agent_model** (optional): Agent model identifier.
- **role_assignment** (optional): RoleAssignment for U.Work logging (default: Strategist).
- **decisions** (optional): Semicolon-delimited DRR ids/paths.
- **timestamp_start** (optional): ISO-8601 timestamp for deterministic output.

## 3. Outputs

- `runtime/contexts/<context>/approvals/<session_id>.<approval_id>.<timestamp>.response.md`

## 4. Procedure

1. Validate inputs and confirm the approval request exists.
2. Write the approval response record with the decision.
3. Emit U.Work via `telemetry/log-work` when available.
