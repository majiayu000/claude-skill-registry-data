---
name: schema-implementation
description: Step-by-step procedure for implementing a new schema.org type in this library, including class structure, enum creation, test writing, and code style.
---

# Implement a Schema.org Type

Step-by-step procedure for implementing a new schema.org type in this library.

## Step 1: Understand the type

- Read the Google Rich Results docs URL from the issue
- Read the schema.org spec URL from the issue
- Identify required, recommended, and optional properties
- Identify property types: string, int, float, bool, array, enum, or nested schema

## Step 2: Check for dependencies

- Does this type reference other TypedSchema classes?
- Are they already implemented in `php/src/v1/Schema/`?
- If not, they need to be created too (or the issue should specify using a simpler type like `string` temporarily)

## Step 3: Create the schema class

File: `php/src/v1/Schema/{TypeName}.php`

Template:
```php
<?php

declare(strict_types=1);

namespace EvaLok\SchemaOrgJsonLd\v1\Schema;

use EvaLok\SchemaOrgJsonLd\v1\TypedSchema;

class {TypeName} extends TypedSchema {
    public const A_SCHEMA_TYPE = '{TypeName}';

    public function __construct(
        // Required properties first (no default value)
        public string $requiredProp,
        // Optional properties last (default to null)
        public null|string $optionalProp = null,
    ) {
    }
}
```

Rules:
- Extend `TypedSchema` (or a parent schema class if the type inherits — see below)
- Set `A_SCHEMA_TYPE` to the exact schema.org type name
- Use constructor promotion for ALL properties
- Required properties have no default value
- Optional properties default to `null` with `null|Type` syntax
- For array properties, add `/** @var ElementType[] $propName */` doc comment
- Do NOT add any methods — no toArray(), no serialize(), nothing

### Class inheritance variant

If the schema type extends another schema type (not `TypedSchema` directly), use the inheritance pattern:

```php
class FoodEstablishment extends LocalBusiness {
	public const A_SCHEMA_TYPE = 'FoodEstablishment';

	public function __construct(
		string $name,
		PostalAddress $address,
		// ... all parent params passed through ...
		public null|bool|string $acceptsReservations = null,  // new param
	) {
		parent::__construct(
			name: $name,
			address: $address,
			// ... pass all parent params via named arguments ...
		);
	}
}
```

Key rules:
- Extend the parent class, not `TypedSchema`
- Override `A_SCHEMA_TYPE` with the child's type name
- Pass all parent params through via `parent::__construct()` with named arguments
- Add child-specific params as promoted properties (with `public`) at the end
- Parent params are NOT promoted in the child (no `public` keyword)

Check the PHP codebase for existing inheritance: `FoodEstablishment extends LocalBusiness`, `Store extends LocalBusiness`, `BlogPosting extends Article`, `NewsArticle extends Article`, `MobileApplication extends SoftwareApplication`, `WebApplication extends SoftwareApplication`, `Restaurant extends FoodEstablishment`.

## Step 4: Create enum types (if needed)

File: `php/src/v1/Enum/{EnumName}.php`

Template:
```php
<?php

declare(strict_types=1);

namespace EvaLok\SchemaOrgJsonLd\v1\Enum;

enum {EnumName}: string {
    case CaseName = 'https://schema.org/CaseName';
}
```

Rules:
- Backed string enum with full schema.org URLs as values
- PascalCase for case names matching schema.org names

## Step 5: Write tests

File: `php/test/unit/{TypeName}Test.php`

Must test:
1. **Minimal construction**: Only required properties, verify JSON output has @context, @type, and required fields
2. **Null omission**: Optional properties when null are NOT present in JSON output
3. **Full construction**: All properties set, verify they all appear in JSON output
4. **Nested schemas**: If the type contains other TypedSchema instances, verify they serialize correctly
5. **Enums**: If the type uses enums, verify they serialize to schema.org URLs

Always use `JsonLdGenerator::SchemaToJson(schema: $instance)` for serialization in tests.

## Step 6: Add sample JSON (optional)

File: `php/test/samples/{TypeName}.json`

Create if the type is complex. Match the expected JSON-LD output format. Used for test assertions via `json_decode(file_get_contents(...))`.

## Step 7: Fix code style

```bash
composer run cs-fix
```

Run the auto-fixer before committing. This handles all formatting (tabs, braces, imports, whitespace). Do NOT manually fix style issues — just run this command.

## Step 8: Run tests

```bash
composer run test-unit
```

All existing tests plus new tests must pass. PHP 8.3 and composer dependencies are pre-installed in your environment. You MUST run tests and confirm they pass before finishing your work.

## Step 9: Run static analysis

```bash
composer run phpstan
```

PHPStan must pass cleanly before finishing your work.

## Common mistakes to avoid

1. Adding a `toArray()` method — don't do this, JsonLdGenerator uses reflection
2. Using `?Type` instead of `null|Type` — the codebase uses `null|Type`
3. Forgetting `A_SCHEMA_TYPE` — this determines the @type in JSON-LD output
4. Adding `@context` manually — JsonLdGenerator adds this automatically
5. Manual null filtering — JsonLdGenerator handles this automatically
6. Modifying JsonLdGenerator.php or TypedSchema.php — never modify these
