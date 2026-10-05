---
name: exm
description: Expense Management (EXM) domain index - employee expense claims and their approvals, expense categories and policies, expense reports, and personal development budget usage.
---

# Expense Management Skill Tree

Use this domain for the Expense Management app: expense claims submitted by employees, the approval
queue that acts on them, the categories and policies that constrain them, expense reports, and
employee expense budget usage.
Not this domain: company income, expenses, categories, burn rate, and runway (`finance_hub`);
HR request tickets (`employee_helpdesk`); approval-routing configuration itself (`workflow`).

## Choose the caller role first
- The user talks about "my expense", submitting, cancelling, or checking their own claim -> **employee leaves**. Never answer from an approval or report leaf about the caller's own expenses.
- The user acts as an approver (queue, approve, reject) -> **approver leaves**.
- The user acts as an admin (categories, policies, reports, permissions) -> **configuration and reporting leaves**. The backend enforces access; a `permission_denied` means stop, not switch leaf.

## Employee leaves
- `skills/exm/expenses_overview_help/SKILL.md` - Explain the app, its screens, and the expense lifecycle.
- `skills/exm/submit_expense_help/SKILL.md` - Explain how to submit an expense and what blocks submission.
- `skills/exm/expense_status_help/SKILL.md` - Explain expense statuses and which actions remain available.
- `skills/exm/expense_receipts_help/SKILL.md` - Explain receipts, file limits, and AI receipt scanning.
- `skills/exm/expense_multi_currency_help/SKILL.md` - Explain reimbursement currency and exchange rates.
- `skills/exm/list_my_expenses/SKILL.md` - List the caller's own expenses; resolve an expense name to its ID here.
- `skills/exm/get_expense/SKILL.md` - Read one expense in full, including receipts and policy warnings.
- `skills/exm/submit_expense/SKILL.md` - Submit an expense after category lookup, preview, and confirmation.
- `skills/exm/cancel_expense/SKILL.md` - Cancel one of the caller's pending expenses after confirmation.

## Approver leaves
- `skills/exm/expense_approvals_help/SKILL.md` - Explain the approval screen and where routing is configured.
- `skills/exm/list_expense_approvals/SKILL.md` - Read the pending queue, decision history, or counters.
- `skills/exm/manage_expense_approval/SKILL.md` - Approve or reject one expense, or approve the whole queue.

## Configuration and reporting leaves
- `skills/exm/expense_categories_help/SKILL.md` - Explain expense categories and their deletion rules.
- `skills/exm/expense_policies_help/SKILL.md` - Explain policy rule types, severities, and lifecycle.
- `skills/exm/expense_reports_help/SKILL.md` - Explain the expense report and its CSV export.
- `skills/exm/expense_permissions_help/SKILL.md` - Explain app access versus datablock permissions.
- `skills/exm/list_expense_categories/SKILL.md` - List categories; resolve a category name to its ID here.
- `skills/exm/manage_expense_category/SKILL.md` - Create, update, or delete a category after confirmation.
- `skills/exm/list_expense_policies/SKILL.md` - List policies, or read one with its eligibility and rules.
- `skills/exm/manage_expense_policy/SKILL.md` - Create, edit, enable, archive, or delete a policy; also runs the read-only conflict check and policy preview.
- `skills/exm/get_expense_report_overview/SKILL.md` - Read per-employee expense totals by currency, or the flat rows behind the CSV export.
- `skills/exm/get_employee_expense_report/SKILL.md` - Drill into one employee's expenses from the report.
- `skills/exm/get_personal_development_budget_usage/SKILL.md` - Report organization-wide personal development budget (PDB, learning or training budget) usage.

## Scripts
- Every executable leaf lives at `skills/exm/<leaf>/scripts/<leaf>.py` (for example `skills/exm/list_my_expenses/scripts/list_my_expenses.py`). There is no `skills/exm/scripts/` directory.
- Identity comes from request headers; never pass a company ID or an employee ID to identify the caller.
- Do not execute this directory as a script skill; execute only the script declared by the chosen leaf `SKILL.md`.

## Identifiers and enums
- Every `--expense-id`, `--category-id`, `--policy-id`, `--employee-id`, and `--department-id` is a UUID returned by a read tool. Resolve it first with `list_my_expenses`, `list_expense_approvals`, `list_expense_categories`, `list_expense_policies`, or the employee directory. Never construct, guess, or reuse a remembered UUID, and never print one in a reply.
- Expense status: `PENDING_APPROVAL`, `APPROVED`, `REJECTED`, `CANCELLED`, `REIMBURSED`. Policy status: `DRAFT`, `SCHEDULED`, `ACTIVE`, `ARCHIVED`. Always render these in plain language for the user.
- Expense actions come only from `availableActions` on the expense detail (`CANCEL`, `APPROVE`, `REJECT`). Do not offer an action that is not listed there.
- Scripts reject unknown flags; on `unknown_args`, `*_must_be_uuid`, or a validation error, fix the call once from the message instead of retrying variants.

## App surface and boundaries
- The app exposes: My Expenses (submit, cancel, detail, receipts), Approvals (queue, history, approve, reject, approve all), Reports (per-employee totals, employee drill-down, CSV export), Categories, Policies, and App Permissions.
- Receipt files cannot be uploaded or delivered through chat, and CSV export is downloaded by the browser. Hand those off to the app instead of inventing links or document IDs.
- Expense policies and the Reports screen are not enabled in every environment. When a tool reports `not_found` or `permission_denied` for them, say the feature is not available to the caller rather than describing a menu they cannot see.
- Approval routing is configured in the platform Workflows engine, not in this app's permissions.

## Safety and authorization
- Employee leaves are restricted by the service to the authenticated employee's own expenses.
- Reporting, category, and policy leaves are intended for authorized administrators and stay subject to the service's access checks.
- Before any write leaf, resolve identifiers, read the current state, show a parameter preview, and stop for explicit confirmation in a later turn. A request to preview, only check, or not submit yet means no write in that turn.
- After a backend validation error on a write, report it and ask the user; do not retry with altered payloads.
