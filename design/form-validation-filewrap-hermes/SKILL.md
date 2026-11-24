---
name: form-validation
description: "Errors that name the fix and keep entered data."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, forms]
    category: web
    related_skills: [web-design, form-design, microcopy]
    web_designer_stages: [components, build]
---

# Form Validation and Error Recovery Skill

This skill makes validation behave so errors name the fix and entered data is never lost: validate on blur, clear errors immediately on correction, keep entered data after an error, and write specific, actionable errors linked to their fields. It covers validation timing, error wording, and recovery. It does not cover form layout, labels, or field choice — the form-design skill owns those. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- For every form, on every field that can fail.
- When a form already exists and its errors are vague, late, or destructive.
- When an error currently clears a field the user already filled.

It is NOT for:

- Form layout, label placement, or which fields to ask — that is form-design.
- Success messages or confirmation copy — that is microcopy.
- Server-side validation rules themselves; it governs how validation is presented and recovered from.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage(s).
- The form's fields are recorded in the components inventory, so each field's error behaviour can be attached to the right component.
- The build stage is in progress or complete, so validation behaviour can be checked in the built form.

## How to Run

1. For each field, decide when it validates: on blur, not while typing, and not only on submit.
2. After the first error on a field, validate it live as the user corrects it, and clear the error immediately on correction.
3. Write each error as a specific, actionable instruction — 'Email must contain @', not 'Invalid input'.
4. Link each error to its field with aria-describedby and aria-invalid, so a screen reader announces the error with the field.
5. On submit with errors, scroll to the first error and move focus to it.
6. Never clear a field the user already filled, even when it failed validation; entered data is kept after an error.
7. Record the validation behaviour in the components inventory and the build log, then hand the work to the judger; do not grade it here.

## Quick Reference

- Validation timing: on blur, not while typing, not only on submit. Blur is ~7s faster than typing-time validation on simple fields (Wroblewski).
- After first error: validate live, clear the error immediately on correction.
- Keep entered data after an error (WCAG 3.3.7).
- Errors linked via aria-describedby and aria-invalid (WCAG 3.3.1/3.3.3; Baymard 2024).
- Error wording: specific and actionable — 'Email must contain @', never 'Invalid input'.
- On submit: scroll to the first error.

## Procedure

### 1. What it is

Validate on blur (not while typing, not only on submit — Wroblewski: blur is ~7s faster than typing-time on simple fields), clear errors immediately on correction, keep entered data after an error (WCAG 3.3.7), and write specific, actionable errors linked via aria-describedby and aria-invalid (WCAG 3.3.1/3.3.3; Baymard 2024).

### 2. How Hermes applies it

Hermes validates on blur then live after first error, scrolls to the first error on submit, writes errors as 'Email must contain @' not 'Invalid input', and never clears a field the user already filled.

### 3. What it returns to the stage

- `components` stage — `inventory`: each form field component records its validation timing (blur, then live after first error), its error text, and its aria-describedby and aria-invalid linkage.
- `build` stage — `files`: the built form carries the validation behaviour. `build_log`: notes the validation rules applied per field. `token_drift`: nothing new; validation adds no tokens.

### 4. Good looks like

An error tells the user exactly what to fix, where, and how; the fix is confirmed the moment it is typed; no data is lost.

## Pitfalls

- Validating while typing, which flags a half-typed answer as wrong before the user has finished.
- Validating only on submit, so the user discovers every error at once, far from the fields that caused them.
- Clearing a filled field on error — the user must retype work they already did.
- Generic errors ('Invalid input') that name no fix.
- Errors shown only in colour, or not linked to the field, so a screen-reader user never hears them.
- Leaving the error visible after the user has corrected the field.

## Verification

- Every field validates on blur, then live after its first error; no field validates only on submit.
- Every error names the exact fix; no generic 'Invalid input' survives.
- Errors are linked with aria-describedby and aria-invalid, and submit scrolls to the first error.
- No filled field is cleared by an error; entered data survives.
- The a11y judger checks the ARIA linkage and the error identification; the content judger checks the error wording. The skill does the work and the judgers check it. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: components, build. Returns: `components` — `inventory`; `build` — `files`, `build_log`, `token_drift`. Judger boundary: a11y judger checks ARIA linkage and error identification; content judger checks error wording.
