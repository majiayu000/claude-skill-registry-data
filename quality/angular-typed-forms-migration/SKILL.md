---
id: angular.forms.angular-typed-forms-migration
name: Angular Typed Forms Migration
description: >
  Migrate Angular reactive forms to typed forms in bounded slices after Angular 14+. Use when converting FormControl, FormGroup, FormArray, and FormBuilder usage incrementally.
stack:
  - Angular
  - TypeScript
category: forms
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - typed forms
  - FormControl
  - FormGroup
  - FormArray
compatibility:
  angular:
    min: "14"
---

# Angular Typed Forms Migration

## Purpose

Migrate reactive forms to typed forms.

## When to Use

- The app has reactive forms.
- The app is ready for typed migration in a slice.

## When Not to Use

- The forms slice is too large or unstable.

## Required Inputs

- reactive form usage
- validators
- tests

## Procedure

1. Select a bounded form slice.
2. Add explicit types.
3. Validate behavior.

## Do

- Keep runtime behavior stable.

## Do Not

- Do not convert the whole app in one pass.

## Review Checklist

- [ ] Typed forms slice is bounded.
- [ ] Tests pass.

## Expected Output

1. Typed forms summary.

## Exit Criteria

- Typed forms slice is migrated.
