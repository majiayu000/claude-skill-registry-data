---
name: payroll
description: Payroll domain index for setup, pay components, pay structures, pay runs, formula configuration, proration, compliance exports, employee earnings, payslips, statutory schemes, tax schemes, and troubleshooting.
---

# Payroll Skill Tree

Use this guide to navigate payroll helpers in a SKILL-tree-first way.

## Available leaves
- skills/payroll/compliance_export_help/SKILL.md — Explain Payroll compliance exports, mappings, and validation correction.
- skills/payroll/generate_pay_component_setup/SKILL.md — Draft or revise a Payroll pay component setup.
- skills/payroll/get_my_end_of_service_estimate/SKILL.md — Estimate end-of-service benefits for self or an employee resolved by an authorized Admin or HR Manager.
- skills/payroll/my_earnings_help/SKILL.md — Help employees find their own earnings history.
- skills/payroll/pay_run_details_help/SKILL.md — Explain pay run results, review tabs, and approval checks.
- skills/payroll/pay_run_proration_help/SKILL.md — Explain prorated pay and the calculation audit.
- skills/payroll/payroll_formula_help/SKILL.md — Explain Payroll formulas, variables, calculation methods, and troubleshooting.
- skills/payroll/payroll_setup_help/SKILL.md — Guide the initial Payroll workspace setup and first run.
- skills/payroll/payroll_troubleshooting_help/SKILL.md — Troubleshoot Payroll setup, calculation, permissions, and edge cases.
- skills/payroll/payslip_view_download_help/SKILL.md — Help employees view and download their payslips.
- skills/payroll/statutory_schemes_help/SKILL.md — Explain statutory scheme setup, eligibility, and contributions.
- skills/payroll/tax_schemes_help/SKILL.md — Explain tax scheme setup, brackets, eligibility, and lifecycle.

## Suggested navigation
- Use `generate_pay_component_setup` when the user wants Lumi to draft or revise a payroll pay component, especially amount setup with fixed amount, manual input, or formula calculation.
- Use `get_my_end_of_service_estimate` for end-of-service benefit, gratuity, or settlement estimates for a planned or hypothetical resignation date. Read the leaf for both self and named-employee requests: it supports self-service and Admin/HR Manager access for other employees, including role verification and employee resolution. Do not reject a named-employee request at this index.
- If the user follows up on an end-of-service estimate by disputing the service length or saying they joined/hired on a different date, stay in `get_my_end_of_service_estimate`; that leaf explains the narrow profile-date verification path. Do not route to document search or generic payroll troubleshooting first.
- Use `my_earnings_help` when an employee asks where to see pay history.
- Use `pay_run_details_help` for pay run result tabs, net pay, earnings, deductions, statutory contributions, tax, and approval detail questions.
- Use `pay_run_proration_help` when the user asks why an amount was prorated or how to review proration audit details.
- Use `payroll_formula_help` when the user asks how Payroll formulas work, which calculation method to choose, which variables or operators are supported, or why a formula fails.
- Use `payroll_setup_help` when the user asks how to set up payroll, start payroll setup, finish payroll onboarding, or run payroll after initial configuration.
- Use `payslip_view_download_help` for self-service payslip preview and download guidance.
- Use `statutory_schemes_help` for statutory scheme setup, contribution types, programs, eligibility, and employee enrollment guidance.
- Use `tax_schemes_help` for tax scheme eligibility, relief rules, assigned employees, excluded employees, and delete/archive behavior.
- Use `compliance_export_help` for WPS/SIF-style exports, reusable mappings, and validation correction guidance.
- Use `payroll_troubleshooting_help` when setup is incomplete, a pay run cannot proceed, a calculation fails, a result looks unexpected, or a scheme/component cannot be changed.
- Payroll setup is a direct-answer help flow. Do not execute scripts unless a separate payroll action leaf explicitly declares one.

## Product boundaries

- Treat the current Payroll app behavior as the source of truth. Do not present design proposals or documentation-only concepts as available features.
- Retro Pay is not a current Payroll workflow. For a correction, explain whether the run can be recalculated or whether the payroll owner needs a later manual adjustment, based on the run state.
- Do not provide legal, tax, or statutory advice. Explain the configured product behavior and direct the user to their payroll or compliance owner for jurisdiction-specific decisions.
- Pay, tax, statutory, and employee data are sensitive. Never expose another employee's private amounts or suggest bypassing Payroll permissions.
