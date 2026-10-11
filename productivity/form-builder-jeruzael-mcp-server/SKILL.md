---
name: form-builder
description: Build, review, or update reliable frontend forms that collect clean data and connect correctly to backend behavior. Use when Codex needs to create or modify registration forms, login forms, booking forms, payment forms, staff creation forms, customer profile forms, shop profile forms, rider onboarding forms, settings forms, search/filter forms, admin input pages, report filters, inventory forms, order update forms, address forms, contact forms, feedback forms, file upload forms, approval/rejection forms, validation rules, default values, disabled states, API submission, payload mapping, loading/submitting behavior, success messages, server validation errors, duplicate submission protection, edit forms, and form tests.
---

# Form Builder

Use this skill when a task involves user input that creates, updates, filters, uploads, or submits application data.

## Core Rule

A form is not just input fields. Define fields, validation, defaults, disabled states, payload mapping, submission behavior, success behavior, error handling, permissions, and edge cases before implementing.

## Workflow

1. Understand the form purpose:
   - form name, user role, business purpose, data collected, record created or updated, endpoint involved, success behavior, error behavior, permission requirement, and business criticality
2. Inspect existing form patterns:
   - form components, inputs, selects, date pickers, file uploads, validation helpers, schema libraries, error messages, submit buttons, loading states, success toasts/messages, API utilities, styling, and tests
3. Define every field:
   - name, label, input type, required/optional, default value, placeholder, help text, validation rule, backend field mapping, editability, visibility, and role rules
4. Define validation:
   - required fields, formats, length, ranges, dates, enums, file type/size, password rules, matching fields, uniqueness, and business rules
5. Set safe defaults:
   - avoid defaults that create incorrect business data, such as paid status before payment confirmation
6. Define disabled and read-only states:
   - submitting, invalid form, insufficient permission, immutable edit fields, finalized records, loaded options unavailable, or payment confirmed states
7. Build layout from existing conventions:
   - field grouping, section headings, required indicators, help text, responsive layout, mobile spacing, primary/secondary actions, and error summaries for large forms
8. Connect to the API using existing project patterns:
   - endpoint, method, payload, headers, auth, authorization, response format, error format, cache refresh, and navigation behavior
9. Map frontend values to backend payload explicitly.
10. Handle submission state:
   - disable submit, prevent duplicate submits, show loading feedback, preserve entered values, and avoid navigation until success
11. Handle success behavior:
   - toast, inline message, redirect, close modal, reset form, refresh data, update cache, clear dirty state, or advance workflow
12. Handle error behavior:
   - frontend validation, backend field errors, duplicate records, unauthorized, expired session, network failure, invalid file, business rule violations, and friendly fallback messages
13. Handle special form types:
   - edit forms, search/filter forms, file upload forms, and approval/rejection forms each have different behavior and risks
14. Add or update tests where practical.
15. Run relevant checks discovered from project scripts or docs.
16. Summarize fields, validation, API integration, states, edge cases, files changed, checks, risks, and follow-up recommendations.

Read `references/form-builder-checklist.md` for field planning tables, validation categories, API/error mapping, special form guidance, test ideas, and the final report format.

## Non-Negotiable Rules

- Do not build a form before defining required and optional fields.
- Do not rely only on frontend validation.
- Do not skip backend error handling.
- Do not allow duplicate submission.
- Do not leave users without feedback after submitting.
- Do not expose raw technical errors to users.
- Do not hardcode API URLs when an API client pattern exists.
- Do not ignore authentication or permission requirements.
- Do not overwrite existing data accidentally in edit forms.
- Do not add unnecessary fields.
- Do not create inconsistent form styling.
- Do not ignore loading, success, error, empty-options, or unauthorized states.
- Do not ignore mobile or responsive behavior when the app supports it.
- Do not claim the form is complete if it is not connected to the backend or clearly marked as UI-only.

## Output Contract

When using this skill, provide:

1. Form created or updated.
2. User role and use case.
3. Field list with types, required status, defaults, and notes.
4. Validation rules.
5. API integration and payload mapping.
6. UI states: default, submitting, success, validation error, server error, unauthorized.
7. Edge cases handled.
8. Files changed.
9. Tests/checks or manual verification.
10. Risks and follow-up recommendations.
