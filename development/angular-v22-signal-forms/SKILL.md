---
id: angular.forms.angular-v22-signal-forms
name: Angular v22 Signal Forms
description: >
  Use this skill when an Angular 22 app is adopting Signal Forms or needs to align form code with stricter template and validation rules.
stack:
  - Angular
  - TypeScript
category: forms
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Signal Forms
  - reactive forms
  - template type checking
  - validation
compatibility:
  angular:
    min: "22"
---

# Angular v22 Signal Forms

## Purpose

Use this skill when an Angular 22 app is adopting Signal Forms or needs to align form code with stricter template and validation rules.

## When to Use

Use this skill when:

- The app is moving to Signal Forms in v22.
- Form validation or template bindings need review after the upgrade.
- Angular Material or Angular Aria integration matters for the form flow.

## When Not to Use

Do not use this skill when:

- The issue is purely async resource state.
- The change does not touch forms.
- Another migration skill is a tighter fit for the specific form API.

## Required Inputs

- form model
- validation rules
- template diagnostics
- Material or Aria integration

## Procedure

1. Decide whether the form should remain reactive or move to Signal Forms.
2. Update validation and bindings to match v22 template strictness.
3. Preserve the observable behavior of submit and error display.

## Do

- Use Signal Forms when the app is ready for the signal-native model.
- Keep validation intent explicit.
- Check compile-time template errors as part of the change.

## Do Not

- Do not mix form migration with unrelated template cleanups.
- Do not keep a half-migrated form model without a clear reason.
- Do not ignore Material or Aria behavior if the form depends on it.

## Review Checklist

- [ ] The form model choice is explicit.
- [ ] Validation still behaves correctly.
- [ ] Templates compile cleanly under v22 rules.

## Expected Output

1. A form migration summary.
2. The chosen form model.
3. Any remaining diagnostics.
