---
name: form-requests
description: Use Laravel Form Requests for non-trivial validation and authorization while keeping controllers thin and testable.
tags:
  - laravel
  - php
---

# Form Requests

Use Form Requests for HTTP validation and request-bound authorization when rules are complex, reused, sensitive, or likely to grow.

Inline controller validation is acceptable for tiny prototypes or legacy maintenance, but it is not the global standard for new or heavily edited workflows.

## Responsibilities

A Form Request may:

- authorize the HTTP operation;
- normalize input in `prepareForValidation()`;
- return validation rules;
- use custom messages and attribute labels;
- expose small helper methods for typed validated data.

It should not:

- perform database writes;
- send external requests;
- dispatch jobs;
- contain long business workflows.

## Input Normalization

Normalize human-formatted inputs before applying numeric/date/boolean rules. Keep locale assumptions explicit.

```php
final class StoreRecordRequest extends FormRequest
{
    protected function prepareForValidation(): void
    {
        $this->merge([
            'amount' => NumberInput::normalize($this->input('amount')),
        ]);
    }

    public function rules(): array
    {
        return [
            'amount' => ['required', 'numeric', 'min:0'],
            'status' => ['required', Rule::enum(RecordStatus::class)],
        ];
    }
}
```

Shared parsers should be small helpers or value objects with unit tests.

## Authorization

Use `authorize()` when the decision depends on request context or validated input. Use Policies when the decision depends on model state.

```php
public function authorize(): bool
{
    return $this->user()?->can('create', Record::class) === true;
}
```

## Array And Conditional Rules

Use the simplest Laravel-native validation rule set that fully matches the actual input shape and behavior. Reuse the existing Form Request structure when safe. Do not introduce complex nested rules, helper abstractions, or additional validation structures unless the behavior actually requires them.

Validate nested arrays explicitly.

```php
public function rules(): array
{
    return [
        'items' => ['required', 'array', 'min:1'],
        'items.*.name' => ['required', 'string', 'max:120'],
        'items.*.quantity' => ['required', 'integer', 'min:1'],
    ];
}
```

Prefer named custom rule objects when validation has reusable domain meaning.

## Testing

Test validation failures and authorization failures. Cover request normalization when human-formatted values are accepted.

## Context Efficiency

Layer: 3 (Implementation)

Load this skill only when validation or request authorization is nontrivial. Inline tiny validation in controllers only for prototypes or legacy maintenance. Keep Form Requests focused: rules, authorize, prepareForValidation, no database writes or business workflows.
