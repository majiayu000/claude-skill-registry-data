---
id: angular.forms.form-validation-contracts
name: Angular Form Validation Contracts
description: >
  Reviews Angular form validation contracts for enterprise workflows, focusing on synchronous and async validators, cross-field rules, error presentation, and reusable validation policy.
stack:
  - Angular
  - TypeScript
category: forms
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - form validation
  - angular validation
  - async validators
  - cross field validation
  - validation contract
  - error presentation
  - custom validator
  - form errors
compatibility:
  angular:
    min: "14"
    typedFormsFrom: "14"
    signalInputsFrom: "17"
    recommendedModern: "17+"
---

# Angular Form Validation Contracts

## Purpose

Use this skill to define validation contracts for Angular forms in enterprise applications.

Validation is part of the business contract. This skill helps define what should be validated, where the logic belongs, and how errors are exposed to the user and tests.

The core rule is simple:

```txt
Validation must be explicit, reusable, and user-facing.
```

## When to Use

Use this skill when:

- a form has custom business validation
- cross-field validation is needed
- async validation is required
- validation messages need a consistent policy
- enterprise forms have too much duplicated validation logic

## Do

Separate validation kinds:

```txt
required
format
cross-field
async uniqueness
server-side error mapping
```

Keep reusable validators pure where possible:

```ts
export function postalCodeValidator(
  control: AbstractControl,
): ValidationErrors | null {
  return /^\d{5}$/.test(control.value) ? null : { postalCode: true };
}
```

Expose errors consistently:

```txt
- show when touched or submitted
- prefer actionable messages
- map server errors into form state
```

Use async validators for remote checks, not for general orchestration.

## Do Not

Avoid hidden validation in submit handlers only.

Avoid business rules that exist only in template error blocks.

Avoid mixing transport errors and field errors without a mapping policy.

Avoid validators with side effects.

## Review Checklist

- [ ] Validation rules are explicit.
- [ ] Cross-field rules are handled correctly.
- [ ] Async validation is justified.
- [ ] Error presentation is consistent.
- [ ] Validation logic is testable in isolation.

## Expected Output

1. Identify validation rules and their scope.
2. Recommend reusable validators or policy helpers.
3. Define field, cross-field, and server error handling.
4. Clarify when async validation is appropriate.
5. Suggest validation tests and UI error behavior.
