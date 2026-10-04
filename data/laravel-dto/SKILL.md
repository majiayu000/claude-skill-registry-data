---
model_tier: medium
name: laravel-dto
description: "Use when creating a Laravel/PHP DTO with the SimpleDto base class and attribute mapping. For DTOs in other stacks, use the stack-native skill (TypeScript, Python, Rust, Go)."
domain: engineering
framework: laravel
workspaces:
  - engineering
packs:
  - laravel
trust:
  level: professional
install:
  default: false
  removable: true
---

# laravel-dto

## When to use

Use this skill when creating a new DTO for data transfer between layers (DB ↔ PHP, API ↔ Service, etc.).

## Procedure: Create a DTO

1. **Read the project's DTO docs** — check `agents/reference/docs/dto.md` (if it exists) for project-specific conventions.
2. **Check the base class** — search for the DTO base class in the project (e.g., `SimpleDto`, `LiteDto`, or a custom base).
   Check `composer.json` for DTO-related packages.
3. **Check existing DTOs** — look at neighboring DTOs in the same directory to match the style.
4. **Understand the model** — if the DTO maps to a Model, read the model's properties and DB columns.

## DTO conventions

### Base class

- Use the project's standard DTO base class (typically `SimpleDto` or `LiteDto`).
- Never create plain PHP classes for DTOs that map to models — always extend the base class.

### Property mapping

- Use `#[Map('db_column')]` attributes to map between DB column names and PHP properties.
- PHP properties: `camelCase`, English names.
- DB columns: `snake_case`, may be German (legacy) — match what's in the database.

### Type casting

- Use typed properties (`int`, `string`, `float`, `bool`, `Carbon`, etc.).
- The base class handles casting from DB strings to PHP types automatically.

### Validation

- Use validation attributes where appropriate: `#[Length(50)]`, `#[Email]`, `#[Decimal(10,2)]`, `#[Unsigned]`.
- Add `#[ConvertEmptyToNull]` at class level if empty strings should become null.

### Model linkage

- Add `#[HasModel(ModelClass::class)]` on the DTO.
- Add `#[HasDto(DtoClass::class)]` and `DtoMappingTrait` on the Model (if not already present).

## Structure

```php
<?php

declare(strict_types=1);

namespace App\DTO;

use Vendor\DataHelpers\SimpleDto;
use Vendor\DataHelpers\SimpleDto\Attributes\HasModel;
use Vendor\DataHelpers\SimpleDto\Attributes\Map;

#[HasModel(MyModel::class)]
class MyModelDto extends SimpleDto
{
    #[Map('id_column')]
    public ?int $id = null;

    #[Map('name_column')]
    public string $name = '';

    #[Map('amount_column')]
    public float $amount = 0.0;
}
```

## Project detection

The DTO pattern varies by project:

- **Projects with a DTO package**: Use the package's base class with attribute mapping.
  Read `agents/reference/docs/dto.md` for full details (if it exists).
- **Projects without a DTO package**: Check existing DTOs for the local pattern.
  Some projects use plain `readonly` classes, others have custom base classes.

Always check `composer.json` for DTO-related packages before choosing the approach.

## Rules

- **Match existing patterns** — if the project already has DTOs, follow their style.
- **Do NOT create DTOs for trivial data** — if a simple array or typed parameter suffices, don't over-engineer.
- **Use `Math` helper** for any calculated properties — never raw PHP arithmetic.
- **`declare(strict_types=1)`** in every new file.


## Output format

1. DTO class extending SimpleDto with typed properties
2. Static factory method(s) for construction from common sources

## Gotcha

- DTOs must extend `SimpleDto` — don't create plain PHP classes as DTOs.
- The model forgets to add the model linkage (`$modelClass`) when the DTO maps to an Eloquent model.
- Attribute names in the DTO must match the database column names (snake_case), not the PHP property names.

## Do NOT

- Do NOT add business logic to DTOs — they are data containers only.
- Do NOT use arrays when a DTO can provide type safety.
- Do NOT skip validation when creating DTOs from external input.

## Auto-trigger keywords

- DTO
- data transfer object
- SimpleDto
- attribute mapping
