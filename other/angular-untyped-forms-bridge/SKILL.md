---
id: angular.forms.angular-untyped-forms-bridge
name: Angular Untyped Forms Bridge
description: >
  Use untyped form controls as a temporary bridge while migrating to typed forms in Angular. Use when a large forms codebase cannot be converted safely in one pass.
stack:
  - Angular
  - TypeScript
category: forms
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - UntypedFormGroup
  - UntypedFormControl
  - typed forms bridge
compatibility:
  angular:
    min: "14"
---

# Angular Untyped Forms Bridge

## Purpose

Use untyped forms as a temporary bridge.

## When to Use

- Typed forms migration is too large for one pass.

## When Not to Use

- The forms slice can be typed safely now.

## Required Inputs

- reactive forms
- migration plan

## Procedure

1. Keep the slice untyped.
2. Document follow-up migration.

## Do

- Keep the bridge explicit.

## Do Not

- Do not let the bridge become permanent.

## Review Checklist

- [ ] Bridge usage is documented.

## Expected Output

1. Bridge summary.

## Exit Criteria

- Bridge is temporary.
