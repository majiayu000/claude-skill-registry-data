---
name: i18n-integrity
description: 'Maintain HIVMeet FR/EN localization integrity with fast checks and targeted fixes. Use when adding UI text, refactoring screens, or reviewing translation regressions. Includes hardcoded-string detection, ARB key hygiene, fallback checks, and localization-ready output rules.'
argument-hint: 'Describe changed UI files, new user-facing messages, and module scope.'
user-invocable: true
---

# i18n Integrity

## Purpose
Improve development efficiency by preventing localization regressions early and avoiding late translation rework.

This skill is project-scoped and specific to HIVMeet.

## Use When
- Adding or editing user-facing text in Flutter widgets/pages
- Refactoring screens with existing translation keys
- Auditing FR/EN consistency before merge
- Fixing missing translation or fallback issues

## Mandatory Workflow

### 1. Scope Localization Surface
- List changed UI files with visible text
- List new, edited, or removed messages
- Identify impacted modules and flows

### 2. Detect Hardcoded Strings
- Identify visible literals in widgets/dialogs/toasts/errors
- Replace literals with localization keys
- Keep developer logs and internal debug strings out of i18n scope

### 3. Validate Key Hygiene
- Ensure keys are explicit and stable
- Avoid duplicate semantic keys for identical meaning
- Keep naming consistent by feature/screen intent

### 4. Verify FR/EN Coverage
- Confirm each new key exists in both locales
- Confirm placeholders and variable interpolation are equivalent
- Confirm pluralization and formatting semantics are aligned

### 5. Runtime Fallback Checks
- Confirm no raw key leakage in UI
- Confirm locale switch keeps screen semantics intact
- Confirm error/empty/loading texts remain localized

### 6. Non-Regression Checks
- Revisit nearby screens sharing same key families
- Recheck critical user journeys touched by text changes
- Ensure no UX wording became stigmatizing or unclear

### 7. Output Contract
1. Files audited/modified
2. New/updated localization keys
3. Hardcoded strings removed
4. FR/EN coverage status
5. Residual wording risks and suggested follow-ups

## Notes
- Prefer concise, respectful, non-stigmatizing wording
- Keep key naming stable to reduce translation churn
- Language for responses: French
