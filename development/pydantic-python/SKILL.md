---
name: pydantic-python
description: Use for writing, reviewing, debugging, migrating, or testing Python code built on Pydantic v2. Trigger for BaseModel, RootModel, Field or Annotated constraints, validators, serializers, TypeAdapter, discriminated unions, aliases, JSON Schema, and ValidationError. Do not use for pydantic-settings source resolution, plain dataclasses, attrs, generic typing, or environment-variable tasks.
argument-hint: "[Pydantic model, payload, migration, or validation failure]"
---

# Pydantic validation and serialization

Produce version-grounded boundaries whose input source, conversion policy,
validated output type, invariants, and serialized shape are explicit and tested.

## Boundary

Use this skill when the project uses Pydantic or the user
explicitly requests them. Do not introduce runtime validation for a trusted
internal record that only needs a dataclass or `TypedDict`. Route BaseSettings,
environment, dotenv, secrets-directory, or settings-source work to the
`pydantic-settings-python` skill. Preserve public validation errors and
serialized schemas unless the task explicitly changes them.

## Know the two compiled paths

Pydantic builds a core schema from annotations, field metadata, configuration,
and decorators. Validation and serialization use that schema but are different
contracts:

```text
Python / JSON / string input -> validator -> typed value or ValidationError
typed value -> serializer (python or json mode) -> dict / JSON-compatible data / JSON
```

| Object | Runtime meaning | Use it for |
|---|---|---|
| `BaseModel` class | A named object schema plus class validation/JSON Schema APIs. | Domain or boundary objects with named fields. |
| Model instance | Validated typed state; not the original input mapping. | Internal typed work and explicit serialization. |
| `Field` / `Annotated` metadata | Constraints, defaults, aliases, exclusion, and schema details attached to a type. | Rules expressible without custom code; reusable constrained types. |
| Field/model validator | User code inserted before, after, plain, or around core validation. | Only invariants or normalization the schema cannot express clearly. |
| Field/model serializer | User code inserted into output conversion. | Output rules that differ from validation; never use validators as serializers. |
| `TypeAdapter[T]` | A compiled validator/serializer for any supported type `T` without an artificial model. | Collections, unions, `TypedDict`, dataclasses, and standalone types. Reuse it. |
| `RootModel[T]` | A named model whose payload is one root value. | A true root-value public type that needs model behavior. |

Read [the core object model](references/object-model.md) when choosing an
abstraction or reasoning about validation versus serialization.

## Ordered workflow

1. Recover the boundary: input source and shape, trust, desired output type,
   accepted coercions, extra-data policy, aliases, and serialized contract.
2. Confirm the installed Pydantic version from project locks and the active environment.
3. Choose `BaseModel`, `TypeAdapter`, or `RootModel` from the
   required runtime object—not from habit.
4. Express structure and constraints in types/fields. Add the narrowest
   deterministic validator only for remaining rules.
5. Choose the entrypoint matching Python, JSON, or string-mapping input.
6. Design serialization separately: mode, aliases, exclusions, subclass policy,
   and sensitive fields.
7. Test valid, invalid, conversion, extra-key, alias, invariant, and serialized
   cases.

## Choose by intent

| Intent | Use |
|---|---|
| Validate a Python mapping/object as a model | `Model.model_validate(...)` |
| Validate JSON text/bytes as a model | `Model.model_validate_json(...)` |
| Validate a nested string-key/string-value mapping in JSON mode | `Model.model_validate_strings(...)` only when that source contract fits |
| Validate `list[Item]`, a union, `TypedDict`, or another standalone type | Create and reuse `TypeAdapter(type)` |
| Represent a named single root payload | `RootModel[T]` |
| Constrain one field | `Annotated[T, Field(...)]` or `Field(...)` |
| Reuse a custom constraint/normalizer | A named `Annotated` type with functional metadata |
| Select one tagged variant predictably | A discriminated union with `Literal` tags and `Field(discriminator=...)` |
| Normalize raw input before typing | a `mode="before"` validator that accepts arbitrary input safely |
| Enforce a typed field rule | an after field validator |
| Enforce a cross-field invariant | an after model validator |
| Emit Python-native objects | `model_dump(mode="python")` (the default) |
| Emit JSON-compatible Python values | `model_dump(mode="json")` |
| Emit JSON text | `model_dump_json()` |
| Use external names on input only | `validation_alias` |
| Use external names on output only | `serialization_alias` plus `by_alias=True` |

Read [the intent-to-API map](references/api-map.md) for aliases, unions,
attribute loading, JSON Schema, dataclasses, call validation, and dynamic models.

## Canonical strict boundary

```python
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter


PositiveMoney = Annotated[Decimal, Field(gt=0, strict=True)]


class CardPayment(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    kind: Literal["card"]
    amount: PositiveMoney
    currency: str = Field(pattern=r"^[A-Z]{3}$")


payments = TypeAdapter(list[CardPayment])
validated = payments.validate_python(payload)
wire_value = payments.dump_python(validated, mode="json")
```

Pydantic may coerce in lax mode, sometimes with information loss. Strictness can
be chosen per call, field, or configuration, and JSON strict behavior can differ
from Python strict behavior. Test the actual input modes; do not infer one from
the other. Read [validation boundaries](references/validation.md).

## Validator rules

- Prefer types, `Field` constraints, tagged unions, and configuration over
  validators. They compose and generate schemas more predictably.
- A before validator receives arbitrary raw input; do not assume its type or
  mutate a value that may later flow to another union branch.
- An after validator receives the typed value. Return the value/model on every
  success path.
- Use a model validator only for genuinely cross-field invariants. Do not rely
  on field order for cross-field logic.
- Raise documented validation failures such as `ValueError` for bad user data.
  Keep I/O, database access, clocks, randomness, and remote lookups outside.
- Catch `ValidationError` at the boundary that can translate it. Assert stable
  `errors()` fields needed by callers, not whole human-formatted messages.

## Serialization is a separate contract

- Choose Python mode, JSON mode, or JSON text deliberately. `dict(model)` leaves
  nested model objects intact; it is not a substitute for `model_dump()`.
- Name input and output aliases independently. `alias` affects both directions;
  `validation_alias` and `serialization_alias` express asymmetric contracts.
- Use `exclude_unset`, `exclude_defaults`, or `exclude_none` only when that
  omission policy is part of the wire contract and is tested.
- By default, a field annotated as a base model serializes fields declared on
  that annotation, limiting accidental subclass-secret exposure. Treat any
  serialize-as-runtime-type option as security-sensitive and version-ground it.
- Add serializers only when the output rule cannot be expressed by normal
  modes/configuration. Test their return shape; serialization does not revalidate
  arbitrary post-construction mutation.

Read [serialization and aliases](references/serialization.md).

## Version grounding and completion

If code uses v1-shaped `parse_obj`, `.dict()`, `.json()`, `@validator`,
`@root_validator`, `class Config`, or `orm_mode`, inspect the declared version
and read [v1-to-v2 grounding](references/v1-v2.md). Do not mechanically rename:
optional-field requirements, aliases, equality, attribute loading, validators,
and serialization can change.

Run `python scripts/inspect_pydantic.py` from the installed skill directory for
installed versions, API availability, and signatures. Read [API grounding](references/api-grounding.md).

Do not declare completion until input mode, output type, coercion, extras,
aliases, invariants, and serialization are tested; sensitive fields cannot leak; validation bypasses
are absent from untrusted paths; version-supported APIs are used; and project
checks pass or skipped evidence and consequences are reported. Use [the testing
matrix](references/testing.md).

## References

- [Validation and serialization recipes](references/recipes-contracts.md)
- [Core object model](references/object-model.md)
- [Intent-to-API map](references/api-map.md)
- [Validation boundaries](references/validation.md)
- [Serialization and aliases](references/serialization.md)
- [V1-to-v2 grounding](references/v1-v2.md)
- [Testing matrix](references/testing.md)
- [API grounding](references/api-grounding.md)
