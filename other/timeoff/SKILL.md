---
name: timeoff
description: Handle Time Off workflows and guidance including leave balances, policies, accrual calculations, carry-over, retroactive recalculation, maternity leave, leave requests, planning, approvals, cancellations, and troubleshooting.
---

# Time Off Skill Tree

Navigate Time Off helpers categorized by functional domains:

## 1. Personal Leave & Balances (My Time Off)
- `skills/timeoff/submit_my_leave_request/SKILL.md` — Apply/submit personal leave with date range, leave type, and day type.
- `skills/timeoff/get_my_leave_balances_and_types/SKILL.md` — View caller's available, used, pending leave balances and available types.
- `skills/timeoff/get_requestable_timeoff_types/SKILL.md` — List the caller's date-scoped requestable leave types, including exhausted-balance gates.
- `skills/timeoff/get_my_timeoff_entitlement/SKILL.md` — Check one leave type's finite or unlimited entitlement and usage.
- `skills/timeoff/get_leave_request/SKILL.md` — Search and inspect personal or team leave requests.
- `skills/timeoff/cancel_request/SKILL.md` — Cancel one or more pending leave requests, or approved leave requests that start after today in the user's timezone, after confirmation.
- `skills/timeoff/plan/SKILL.md` — Plan time off and inspect holiday impacts without submitting.
- `skills/timeoff/cancel_approved_leave_help/SKILL.md` — (Direct-answer only) Guidance on cancelling already-approved leave.
- `skills/timeoff/request_time_off_help/SKILL.md` — (Direct-answer only) General help on requesting time off.
- `skills/timeoff/maternity_leave_help/SKILL.md` — (Direct-answer only) Policy guidance for maternity and paternity leave.

## 2. Who's Out & Public Holidays
- `skills/timeoff/get_whos_out/SKILL.md` — Query who is out of office today, this week, or in a date range across departments.
- `skills/timeoff/get_public_holidays/SKILL.md` — List company public holidays and non-working days for a given year.

## 3. Approval Queue & Request Management
- `skills/timeoff/get_pending_requests/SKILL.md` — List all time-off requests waiting for manager or admin approval.
- `skills/timeoff/approve_request/SKILL.md` — Approve a specific leave request after confirmation.
- `skills/timeoff/reject_request/SKILL.md` — Reject a pending leave request with a mandatory reason note.
- `skills/timeoff/approve_all_pending_requests/SKILL.md` — Bulk approve all pending requests in the queue.

## 4. Reports & Analytics
- `skills/timeoff/get_timeoff_reports/SKILL.md` — View time-off metrics, total days taken, and employee breakdown across date ranges.
- `skills/timeoff/get_department_absence_report/SKILL.md` — Find the department with the most absence requests and show the leave-type breakdown as a chart.
- `skills/timeoff/diagnose_timeoff/SKILL.md` — Diagnose confusing balances, accruals, policies, requests, carry-over, and report results without making changes.

## 5. Configuration: Types, Policies & Balances
- `skills/timeoff/get_timeoff_types/SKILL.md` — List all configured leave types (paid, unpaid, code, color).
- `skills/timeoff/create_timeoff_type/SKILL.md` — Create a new leave type with color, paid status, and requirement settings.
- `skills/timeoff/update_timeoff_type/SKILL.md` — Update leave type name, color, or requirement settings.
- `skills/timeoff/delete_timeoff_type/SKILL.md` — Permanently delete a leave type after confirmation.
- `skills/timeoff/get_timeoff_policies/SKILL.md` — List leave policies and their finite or unlimited entitlement mode.
- `skills/timeoff/create_timeoff_policy/SKILL.md` — Create a finite or unlimited time-off policy.
- `skills/timeoff/update_timeoff_policy/SKILL.md` — Update policy allowance days, name, or frequency.
- `skills/timeoff/archive_timeoff_policy/SKILL.md` — Archive a policy so it is no longer assigned to new staff.
- `skills/timeoff/delete_timeoff_policy/SKILL.md` — Permanently delete a time-off policy after confirmation.
- `skills/timeoff/get_employee_leave_balances/SKILL.md` — View leave balances for any employee across all leave types.
- `skills/timeoff/get_timeoff_ledger_entries/SKILL.md` — View finite balance logs and unlimited approval or reversal history.
- `skills/timeoff/adjust_leave_balance/SKILL.md` — Manually credit or deduct an employee's leave balance with a reason note.
- `skills/timeoff/generate_timeoff_policy/SKILL.md` — AI assistant to draft or generate compliant time-off policies.
- `skills/timeoff/configure_time_off_help/SKILL.md` — (Direct-answer only) Guidance on configuring time-off settings and rules.
- `skills/timeoff/timeoff_carryover_help/SKILL.md` — (Direct-answer only) Guidance on leave carryover rules and expiration.
- `skills/timeoff/timeoff_retroactive_policy_help/SKILL.md` — (Direct-answer only) Guidance on retroactive policy recalculation.

## Universal Design & Confirmation Principles (MANDATORY)
1. **No Implicit Assumptions**: If a user request is vague or lacks specific entities (e.g. "cancel leave", "reject request", "approve request"), **DO NOT guess, assume, or automatically select all requests**. List available options and ask the user to explicitly select target requests or parameters.
2. **Mandatory Input Verification & Preview**: Before calling ANY write/mutation script (submit, approve, reject, cancel, adjust balance, create/update/delete type or policy), ALWAYS present a clear, structured summary of all resolved parameters to the user.
3. **Mandatory Turn Boundary (STOP & Wait for User Confirmation)**: The agent MUST NOT call the execution script in the same turn as presenting the preview. The agent MUST ask for explicit confirmation (e.g., "Do you confirm ...?") and END its turn, waiting for the user's explicit approval (e.g., "yes", "confirm", "đồng ý") in a subsequent turn before executing.

## User-facing explanation rules
- Explain outcomes in business language. Do not show API paths, UUIDs, database terms, class names, SQL, scheduled-job details, or internal error codes to end users.
- Prefer "balance history" or "activity history" over internal implementation terms when explaining why a balance changed.
- Distinguish the current balance, pending requests, and available balance. A pending request reduces what can be requested even before approval.
- Do not promise that an accrual, recalculation, correction, or approval happened unless a tool result confirms it.
- When diagnosing a problem, use read-only lookups first and state the evidence, likely cause, and safe next step.

## Suggested Navigation & Resolution Flows
- **Caller Entitlement Check**: Resolve the leave type and run `python skills/timeoff/get_my_timeoff_entitlement/scripts/get_my_timeoff_entitlement.py --time-off-type-id <UUID>` to check whether it is finite or unlimited. For a finite type, use the balance tool for detailed available days.
- **Employee Balance Check**: When checking another employee, run `python skills/timeoff/get_employee_leave_balances/scripts/get_employee_leave_balances.py --employee-id <UUID>`.
- **Troubleshooting**: For "why" questions, use `skills/timeoff/diagnose_timeoff/SKILL.md` and combine read-only balance, history, policy, request, holiday, and report evidence before suggesting a correction.
- **Request Resolution**: When `request_id` is unknown, run `python skills/timeoff/get_leave_request/scripts/get_leave_request.py` or `python skills/timeoff/get_pending_requests/scripts/get_pending_requests.py` first.
- **Type Resolution**: Run `python skills/timeoff/get_timeoff_types/scripts/get_timeoff_types.py` to resolve valid `time_off_type_id`.
- **Policy Resolution**: Run `python skills/timeoff/get_timeoff_policies/scripts/get_timeoff_policies.py` to resolve valid `policy_id`.
