---
id: angular.forms.reactive-forms-patterns
name: Angular Reactive Forms Patterns
description: >
  Designs and reviews Angular reactive forms for enterprise features, focusing on typed form models, validation architecture, DTO mapping, state separation, and testable form workflows.
stack:
  - Angular
  - TypeScript
category: forms
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - reactive forms
  - angular forms
  - form group patterns
  - form builder
  - typed forms
  - form workflow
  - form architecture
  - enterprise forms
compatibility:
  angular:
    min: "14"
    typedFormsFrom: "14"
    signalInputsFrom: "17"
    recommendedModern: "17+"
---

# Angular Reactive Forms Patterns

## Purpose

Use this skill to design or review Angular reactive forms in enterprise applications.

Reactive forms should model workflow state explicitly, keep validation testable, and avoid embedding business logic in templates. Typed forms are the baseline when the project version supports them.

The core rule is simple:

```txt
Form state should be explicit, typed, and testable.
```

## When to Use

Use this skill when:

- a feature uses complex or dynamic forms
- validation rules matter
- DTO mapping must be controlled
- forms need unit or integration tests
- typed reactive forms are available
- form state is becoming hard to maintain

## Do

Model the form around the workflow:

```txt
field state
validation state
submission state
server error state
disabled state
reset state
```

Prefer typed reactive forms where supported:

```ts
readonly form = this.fb.group({
  name: this.fb.nonNullable.control('', { validators: [Validators.required] }),
  email: this.fb.nonNullable.control('', { validators: [Validators.required, Validators.email] }),
});
```

Keep DTO mapping separate:

```ts
function toRequest(form: FormValue): CreateUserRequest {
  return {
    name: form.name,
    email: form.email,
  };
}
```

Use custom validators for reusable rules and group validators for cross-field constraints.

## Do Not

Avoid putting business logic only in the template.

Avoid binding API DTOs directly to the form when a view model is needed.

Avoid overusing template-driven forms for enterprise workflows.

Avoid side effects in validators.

## Review Checklist

- [ ] The form is reactive when workflow complexity justifies it.
- [ ] Typed forms are used when the Angular version supports them.
- [ ] Validation is testable and explicit.
- [ ] DTO mapping is separate from form state.
- [ ] The form does not own unrelated business orchestration.

## Expected Output

1. Inspect the form workflow and state shape.
2. Recommend a reactive form structure.
3. Separate validation, mapping, and orchestration concerns.
4. Provide typed form examples when possible.
5. Suggest tests for validation and submission behavior.
