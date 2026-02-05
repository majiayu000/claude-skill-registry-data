---
name: workflow/request-approval
description: Requests approval for a constrained action or change.
version: 0.1.0
status: experimental
family: workflow
role: Strategist
allowed-tools:
  - write_to_file
policies:
  - E.16 RoC-Autonomy
  - A.15.1 U.Work
outputs:
  - ApprovalRequest
---

# Workflow: Request Approval

## 1. Context

This skill records a structured approval request for actions that require human review under a Rule of Constraints policy.

## 2. Inputs

- **context** (required): Bounded context name (safe path segment).
- **session_id** (required): Session identifier (safe path segment).
- **approval_id** (required): Approval identifier (safe path segment).
- **summary** (required): Short approval request summary.
- **details** (optional): Request details or justification.
- **required_for** (optional): Semicolon-delimited approval requirement keys.
- **approver_role** (optional): Approver role label.
- **requested_by** (optional): Requester label.
- **due_by** (optional): Due date for the approval request.
- **artifacts** (optional): Semicolon-delimited artifact paths.
- **notes** (optional): Freeform notes.
- **agent_model** (optional): Agent model identifier.
- **role_assignment** (optional): RoleAssignment for U.Work logging (default: Strategist).
- **decisions** (optional): Semicolon-delimited DRR ids/paths.
- **timestamp_start** (optional): ISO-8601 timestamp for deterministic output.

## 3. Outputs

- `runtime/contexts/<context>/approvals/<session_id>.<approval_id>.approval.md`

## 4. Procedure

1. Validate inputs and resolve the approval request path.
2. Write the approval request record with status pending.
3. Emit U.Work via `telemetry/log-work` when available.
