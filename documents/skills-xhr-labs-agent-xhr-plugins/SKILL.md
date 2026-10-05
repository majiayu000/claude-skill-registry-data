---
name: skills-root
description: Root navigation catalog for locating the correct X-HR skill domain and executable leaf, especially when the user's latest request is outside a client-selected context. Read this index before changing domains; never execute from the root.
---

# Skills root index

Use this file as the primary domain-discovery entrypoint for the skill tree. It gives the agent a small, stable catalog for finding the correct domain index without loading every leaf skill into the prompt.

## Navigation contract
- This file is an index only.
- Use the user's latest explicit intent to choose exactly one best-matching domain entrypoint whenever possible.
- Start here when no retrieved or selected leaf covers the latest request, including when the client-selected context belongs to a different domain.
- A client-selected skill remains primary while the latest request is still within its scope. A clear cross-domain request must be routed through this catalog instead of being forced into the selected skill.
- To navigate deeper, read the chosen domain `SKILL.md`, then read the smallest sufficient child leaf `SKILL.md` before answering or executing.
- Treat domain descriptions as routing hints, not as permission to invent a leaf path, script path, command, or arguments.
- If two domains remain genuinely plausible after reading their indexes, ask one focused clarification question instead of guessing.
- Do not execute this file or this directory as a script skill.
- Execute only scripts that are explicitly declared by a leaf `SKILL.md`.

## Child entrypoints
- skills/access_control/SKILL.md — Read or change who can open an installed app and which relations can read or write each app data block. Not for organization roles, per-object sharing, or approver setup.
- skills/allocation_management/SKILL.md — Plan project allocations; review utilization, allocation dashboards, timesheet variance, and resource or project allocation reports.
- skills/appstore/SKILL.md — Install, remove, manage, or build X-HR apps and answer App Store marketplace questions.
- skills/asset_inventory/SKILL.md — Find or manage employee assets, requests, approvals, lifecycle records, vendors, categories, bundles, and register exports.
- skills/attendance/SKILL.md — Handle attendance, shifts, timesheets, approvals, overtime policies, and attendance reporting.
- skills/calendar/SKILL.md — Book appointments or meetings, manage share links and Google Calendar integration, and work with public-holiday calendars.
- skills/combine/SKILL.md — Use only for workflows that explicitly require coordinated actions or checks across multiple X-HR domains.
- skills/company/SKILL.md — Find or manage company profile data, organization structure, departments, statistics, and work locations.
- skills/document_generator/SKILL.md — Generate employee documents from DOCX templates, merge employee data, preview versions, and export DOCX or PDF files. Not for asking HR to issue a salary or employment certificate (that is an Employee Helpdesk request).
- skills/documents/SKILL.md — List, search, access, store, and explain authorized company documents and document-management behavior. Not for files attached to an HR request ticket (Employee Helpdesk).
- skills/compensation_benefits/SKILL.md — Handle reward elements, compensation packages, component setup, benefits, and payroll-integration guidance.
- skills/employee/SKILL.md — Find employee profiles and managers or handle employee lifecycle, organization, reporting, and profile actions.
- skills/employee_helpdesk/SKILL.md — Employee Helpdesk / Employee Requests: HR request tickets (ER-…) such as salary or employment certificates, payroll questions, personal-information changes; request submission forms and their attachments; HR inbox and case handling; request-type configuration (drafts, versions, publish/activate, archive/restore of HR request types); HR request reports.
- skills/employment_records/SKILL.md — Handle employment contracts, employee changes, attachments, activity logs, company decisions, and record permissions.
- skills/exm/SKILL.md — Expense Management (EXM): submit, cancel, and track employee expense claims and reimbursements; approve or reject expense requests; configure expense categories and expense policies (spending limits); expense reports by employee; personal development budget (PDB), learning, or training budget usage. Not for company income, expenses, or burn rate (Finance Hub).
- skills/final_settlement/SKILL.md — Explain the Final Settlement / EOS app setup, settlement items, EOSG schemes, process, access, payroll handoff readiness, and permissions. Use for prompts like "How to setup EOS". Not for estimating how much an employee would receive when resigning (that is a Payroll end-of-service estimate).
- skills/finance_hub/SKILL.md — Review financial dashboards, income and expenses, categories, burn rate, runway, currencies, and finance reports.
- skills/forms/SKILL.md — Create, publish, secure, version, troubleshoot, review, and manage standalone company forms, submissions, email sharing, audit logs, review forms, and onboarding forms. Not for Employee Helpdesk request types or their draft versions.
- skills/greeting/SKILL.md — Answer greetings and questions about the assistant's identity or name.
- skills/helpdesk/SKILL.md — Answer general X-HR how-to questions, including language, timezone, and regional settings, plus setup, billing, compliance, mobile, Lumi AI, support, and integrations.
- skills/language/SKILL.md — Check supported languages or change the user's X-HR interface language.
- skills/payroll/SKILL.md — Configure payroll and pay components or handle earnings, payslips, pay runs, tax, proration, compliance, statutory schemes, and end-of-service, gratuity, or resignation settlement estimates for self or other employees with Admin/HR Manager access.
- skills/support_ticket/SKILL.md — Collect details and submit an X-HR support request or product feature request.
- skills/timeoff/SKILL.md — Check leave balances and types; plan, submit, approve, cancel, or review leave requests; configure policies, accrual, carry-over, and troubleshooting.
- skills/utils/SKILL.md — Resolve dates and run other shared, low-risk utility operations required by executable domain leaves.
- skills/vdr/SKILL.md — Manage Virtual Data Rooms, files, sharing, access requests, stakeholders, activity analytics, and audit logs.
- skills/workbench/SKILL.md — Find or manage Workbench projects, tasks, priorities, statuses, pages, wiki content, dashboards, and project overviews.
- skills/workflow/SKILL.md — Build and manage workflows, approvals, Task Hub tasks, form tasks, triggers, actions, and date-based automation.
