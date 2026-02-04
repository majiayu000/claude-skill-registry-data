---
name: laravel-data-writer
description: Skill for creating and editing Spatie Laravel Data classes following Prowi conventions. Use when working with Data classes, DTOs, or data transfer objects. Enforces proper constructor-based properties, annotation-based validation, and Collection usage.
---

# Laravel Data Class Writer Skill

You are an expert at working with Spatie Laravel Data classes in the Prowi application. Your role is to create clean, validated Data classes that follow established patterns.

## 🚨 CRITICAL: Define Properties in Constructor, NOT Outside!

**This is the #1 mistake to avoid!** Data classes use constructor property promotion - all properties MUST be defined in the constructor.

### ❌ WRONG - Properties Outside Constructor

```php
class UserData extends Data
{
    // BAD - Don't define properties here!
    public string $name;
    public string $email;
    public int $age;

    public function __construct()
    {
        // Properties should be here instead
    }
}
```

### ✅ CORRECT - Properties in Constructor

```php
class UserData extends Data
{
    public function __construct(
        public string $name,
        public string $email,
        public int $age,
    ) {}
}
```

**Why constructor property promotion:**
- Required by Spatie Laravel Data
- Automatic property initialization
- Works with validation annotations
- Type-safe and clean

## File Organization Convention

**Data classes should be organized by their usage context, NOT in a flat directory structure.**

### Nested Structure Pattern

Place Data classes in nested directories that mirror where they are used:

```
app/Data/
├── Http/
│   └── Controllers/
│       └── Api/
│           ├── AgentController/
│           │   ├── AgentData.php
│           │   └── AgentListData.php
│           └── ConversationController/
│               ├── ConversationData.php
│               └── MessageData.php
├── Inertia/
│   ├── ConversationListItemData.php
│   └── DashboardData.php
└── Mcp/
    └── Tools/
        ├── SendMessageResult/
        │   └── SendMessageResultData.php
        └── ListAgents/
            └── AgentListData.php
```

### Examples:

**For API Controller Responses:**
- Controller: `app/Http/Controllers/Api/AgentController.php`
- Data class: `app/Data/Http/Controllers/Api/AgentController/AgentData.php`
- Namespace: `App\Data\Http\Controllers\Api\AgentController`

**For Inertia Props:**
- Data class: `app/Data/Inertia/ConversationListItemData.php`
- Namespace: `App\Data\Inertia`

**For MCP Tool Results:**
- Tool: `app/Mcp/Tools/SendMessageTool.php`
- Data class: `app/Data/Mcp/Tools/SendMessageTool/SendMessageResultData.php`
- Namespace: `App\Data\Mcp\Tools\SendMessageTool`

### Benefits:

- ✅ Clear ownership and usage context
- ✅ Easier to find related Data classes
- ✅ Prevents naming conflicts
- ✅ Scales better as project grows
- ✅ Groups related data structures together

### Shared Data Classes:

If a Data class is used across multiple contexts, consider placing it in a shared location:
- `app/Data/Shared/UserData.php`
- `app/Data/Common/PaginationData.php`

## Class Structure

### Basic Structure

```php
<?php

namespace App\Data;

use Spatie\LaravelData\Data;
use Spatie\LaravelData\Attributes\Validation\Required;
use Spatie\LaravelData\Attributes\Validation\StringType;

class UserData extends Data
{
    public function __construct(
        #[Required]
        #[StringType]
        public string $name,

        #[Required]
        #[StringType]
        public string $email,
    ) {}
}
```

### Key Requirements:

- ✅ Extend `Spatie\LaravelData\Data`
- ✅ All properties in constructor with `public` visibility
- ✅ Use validation annotations (attributes) above each property
- ✅ Each annotation on its own line
- ✅ Optional: Add `messages()` method for custom error messages
- ✅ Optional: Add static factory methods for convenience
- ✅ Optional: Add PHPDoc block with property descriptions

## 🔥 Use Annotations for Validation, NOT Manual Rules

**Do NOT manually write validation rules!** Use annotations instead.

### ❌ WRONG - Manual Rules

```php
class UserData extends Data
{
    public function __construct(
        public string $name,
        public string $email,
    ) {}

    // BAD - Don't manually define rules!
    public function rules(): array
    {
        return [
            'name' => ['required', 'string'],
            'email' => ['required', 'email'],
        ];
    }
}
```

### ✅ CORRECT - Use Annotations (Each on New Line)

```php
use Spatie\LaravelData\Attributes\Validation\Required;
use Spatie\LaravelData\Attributes\Validation\StringType;
use Spatie\LaravelData\Attributes\Validation\Email;

class UserData extends Data
{
    public function __construct(
        #[Required]
        #[StringType]
        public string $name,

        #[Required]
        #[Email]
        public string $email,
    ) {}
}
```

### Common Validation Annotations

```php
use Spatie\LaravelData\Attributes\Validation\Required;
use Spatie\LaravelData\Attributes\Validation\Nullable;
use Spatie\LaravelData\Attributes\Validation\StringType;
use Spatie\LaravelData\Attributes\Validation\IntegerType;
use Spatie\LaravelData\Attributes\Validation\BooleanType;
use Spatie\LaravelData\Attributes\Validation\Email;
use Spatie\LaravelData\Attributes\Validation\Min;
use Spatie\LaravelData\Attributes\Validation\Max;
use Spatie\LaravelData\Attributes\Validation\Present;

public function __construct(
    #[Required]
    #[StringType]
    public string $name,

    #[Nullable]
    #[StringType]
    public ?string $description,

    #[Required]
    #[IntegerType]
    #[Min(0)]
    #[Max(100)]
    public int $age,

    #[BooleanType]
    public bool $isActive = false,

    #[Required]
    #[Email]
    public string $email,

    #[Present]
    #[Nullable]
    public mixed $data,
) {}
```

**Important:** Each annotation should be on its own line for better readability and maintainability.

## 🔥 Use Collection, NOT Array for Data Collections

**Always use `Illuminate\Support\Collection` with `#[DataCollectionOf]` annotation, NOT arrays!**

### ❌ WRONG - Using Array

```php
class AlbumData extends Data
{
    public function __construct(
        // BAD - Don't use array!
        public array $songs,
    ) {}
}
```

### ✅ CORRECT - Using Collection

```php
use Illuminate\Support\Collection;
use Spatie\LaravelData\Attributes\DataCollectionOf;

class AlbumData extends Data
{
    public function __construct(
        #[DataCollectionOf(SongData::class)]
        public Collection $songs,
    ) {}
}
```

**Why Collection over array:**
- Better type safety
- Proper transformation of nested Data objects
- Refactoring-friendly (IDE support)
- Collection helper methods available
- Recommended by Spatie

## Enums

**Always use `#[WithCast(EnumCast::class)]` for enum properties:**

```php
use App\Enums\UserStatusEnum;
use Spatie\LaravelData\Attributes\WithCast;
use Spatie\LaravelData\Casts\EnumCast;
use Spatie\LaravelData\Attributes\Validation\Required;

class UserData extends Data
{
    public function __construct(
        #[Required]
        #[WithCast(EnumCast::class)]
        public UserStatusEnum $status,
    ) {}
}
```

## Optional Fields

**Use `Optional|null|Type $prop = new Optional` pattern:**

```php
use Spatie\LaravelData\Optional;

class UserData extends Data
{
    public function __construct(
        // Required field
        #[Required]
        #[StringType]
        public string $name,

        // Optional field - can be omitted, null, or string
        public Optional|null|string $nickname = new Optional,

        // Optional integer
        public Optional|null|int $age = new Optional,
    ) {}
}
```

**Why this pattern:**
- Allows field to be omitted entirely
- Allows `null` value
- Doesn't break `#[RequiredIf]` annotations
- No IntelliSense complaints

## Custom Validation Messages

**Use static `messages()` method for custom error messages:**

```php
use App\Data\LaravelData\Attributes\Validation\VariableKey;

class ObjectDefinitionData extends Data
{
    public function __construct(
        #[Required]
        #[StringType]
        public string $name,

        #[Required]
        #[VariableKey]
        public string $data_key,
    ) {}

    public static function messages(): array
    {
        return [
            'name.required' => 'The name is required.',
            'name.string' => 'The name must be a string.',
            'data_key.required' => 'The data key is required.',
            'data_key.regex' => VariableKey::getErrorMessage(),
        ];
    }
}
```

## TypeScript Export

**Add `#[TypeScript()]` attribute to export to frontend:**

```php
use Spatie\TypeScriptTransformer\Attributes\TypeScript;

#[TypeScript()]
class UserData extends Data
{
    public function __construct(
        public string $name,
        public string $email,
    ) {}
}
```

This generates TypeScript types in `resources/js/types/generated.d.ts`.

## PHPDoc Documentation

**Add PHPDoc blocks to describe properties with proper Collection typing:**

```php
/**
 * Filter data for querying data objects
 *
 * @property LogicalOperatorsEnum $preOperator The logical operator (AND/OR)
 * @property Collection<int, SentenceData> $sentences The filter sentences
 */
class FilterData extends Data
{
    public function __construct(
        #[Required]
        #[WithCast(EnumCast::class)]
        public LogicalOperatorsEnum $preOperator,

        #[Required]
        #[DataCollectionOf(SentenceData::class)]
        public Collection $sentences,
    ) {}
}
```

**Important:** For Collection properties in PHPDoc, always specify both key and value types: `Collection<int, ValueType>`

```php
/**
 * @property Collection<int, UserData> $users List of users
 * @property Collection<int, ObjectDefinitionColumnData> $columns The columns
 */
```

## Static Factory Methods

**Add convenience factory methods for common use cases:**

```php
class ObjectDefinitionColumnData extends Data
{
    public function __construct(
        #[Required]
        #[StringType]
        public string $column_key,

        #[Required]
        #[StringType]
        public string $column_name,

        #[Required]
        #[WithCast(EnumCast::class)]
        public ColumnTypeEnum $column_type,

        #[BooleanType]
        public bool $is_required = false,
    ) {}

    /**
     * Create a string column
     */
    public static function stringColumn(
        string $column_key,
        ?string $column_name = null,
        bool $is_required = false,
    ): self {
        return self::from([
            'column_key' => $column_key,
            'column_name' => $column_name ?? $column_key,
            'column_type' => ColumnTypeEnum::STRING,
            'is_required' => $is_required,
        ]);
    }

    /**
     * Create an integer column
     */
    public static function integerColumn(
        string $column_key,
        ?string $column_name = null,
        bool $is_required = false,
    ): self {
        return self::from([
            'column_key' => $column_key,
            'column_name' => $column_name ?? $column_key,
            'column_type' => ColumnTypeEnum::INTEGER,
            'is_required' => $is_required,
        ]);
    }
}
```

## Complete Example

```php
<?php

namespace App\Data\ObjectDefinition;

use App\Data\LaravelData\Attributes\Validation\UniqueInCollection;
use App\Data\LaravelData\Attributes\Validation\VariableKey;
use App\Enums\ObjectDefinition\ColumnTypeEnum;
use Illuminate\Support\Collection;
use Spatie\LaravelData\Attributes\DataCollectionOf;
use Spatie\LaravelData\Attributes\Validation\BooleanType;
use Spatie\LaravelData\Attributes\Validation\IntegerType;
use Spatie\LaravelData\Attributes\Validation\Nullable;
use Spatie\LaravelData\Attributes\Validation\Required;
use Spatie\LaravelData\Attributes\Validation\StringType;
use Spatie\LaravelData\Attributes\WithCast;
use Spatie\LaravelData\Casts\EnumCast;
use Spatie\LaravelData\Data;
use Spatie\LaravelData\Optional;
use Spatie\TypeScriptTransformer\Attributes\TypeScript;

/**
 * Represents an object definition in the system
 *
 * @property string $name The display name
 * @property string $data_key The unique data key (lowercase, alphanumeric, underscores)
 * @property Collection<int, ObjectDefinitionColumnData> $columns The columns in this definition
 * @property UserAssociationConfigData $user_association_config User association configuration
 */
#[TypeScript()]
class ObjectDefinitionData extends Data
{
    public function __construct(
        #[Required]
        #[StringType]
        public string $name,

        #[Required]
        #[VariableKey]
        public string $data_key,

        #[DataCollectionOf(ObjectDefinitionColumnData::class)]
        public Collection $columns,

        public UserAssociationConfigData $user_association_config,

        #[BooleanType]
        public bool $belongs_to_customer_user = false,

        #[BooleanType]
        public bool $can_be_deleted = true,

        #[BooleanType]
        public bool $can_be_updated = true,

        #[BooleanType]
        public bool $is_system_definition = false,

        #[Nullable]
        #[StringType]
        public ?string $primary_title = null,

        #[Nullable]
        #[StringType]
        public ?string $description = null,

        #[IntegerType]
        public int|Optional $customer_id = new Optional,

        #[Nullable]
        #[IntegerType]
        public ?int $id = null,
    ) {}

    /**
     * Get a column by its key
     */
    public function getColumnWithKey(string $key): ?ObjectDefinitionColumnData
    {
        return $this->columns->first(
            fn (ObjectDefinitionColumnData $column) => $column->column_key === $key
        );
    }

    /**
     * Convert to array suitable for Eloquent model
     */
    public function toModelArray(): array
    {
        return collect($this->toArray())
            ->except('columns')
            ->toArray();
    }

    /**
     * Custom validation error messages
     */
    public static function messages(): array
    {
        return [
            'name.required' => 'The object definition name is required.',
            'name.string' => 'The object definition name must be a string.',
            'data_key.required' => 'The data key is required.',
            'data_key.regex' => VariableKey::getErrorMessage(),
            'columns.unique_in_collection.column_name' => 'Column names must be unique.',
            'columns.unique_in_collection.column_key' => 'Column keys must be unique.',
        ];
    }
}
```

## Anti-Patterns Summary

### ❌ Don't Do This

```php
// 1. Properties outside constructor
class UserData extends Data
{
    public string $name;  // WRONG!

    public function __construct() {}
}

// 2. Using array instead of Collection
class AlbumData extends Data
{
    public function __construct(
        public array $songs,  // WRONG!
    ) {}
}

// 3. Manual rules() method
class UserData extends Data
{
    public function __construct(
        public string $name,
    ) {}

    public function rules(): array  // WRONG!
    {
        return ['name' => 'required'];
    }
}

// 4. Wrong Optional pattern
class UserData extends Data
{
    public function __construct(
        public ?string $nickname = null,  // WRONG - breaks RequiredIf
        // OR
        public string|Optional $nickname,  // WRONG - IntelliSense complains
    ) {}
}

// 5. Missing enum cast
class UserData extends Data
{
    public function __construct(
        public UserStatusEnum $status,  // WRONG - Missing #[WithCast(EnumCast::class)]
    ) {}
}

// 6. Wrong PHPDoc Collection format
/**
 * @property Collection<UserData> $users  // WRONG - Missing key type
 */

// 7. Annotations on same line
class UserData extends Data
{
    public function __construct(
        #[Required, StringType]  // WRONG - Should be on separate lines
        public string $name,
    ) {}
}
```

### ✅ Do This Instead

```php
use Illuminate\Support\Collection;
use Spatie\LaravelData\Attributes\DataCollectionOf;
use Spatie\LaravelData\Attributes\Validation\Required;
use Spatie\LaravelData\Attributes\Validation\StringType;
use Spatie\LaravelData\Attributes\WithCast;
use Spatie\LaravelData\Casts\EnumCast;
use Spatie\LaravelData\Optional;

// 1. Properties in constructor
class UserData extends Data
{
    public function __construct(
        #[Required]
        #[StringType]
        public string $name,
    ) {}
}

// 2. Use Collection with annotation
class AlbumData extends Data
{
    public function __construct(
        #[DataCollectionOf(SongData::class)]
        public Collection $songs,
    ) {}
}

// 3. Use annotations (no rules() method)
class UserData extends Data
{
    public function __construct(
        #[Required]
        #[StringType]
        public string $name,
    ) {}
}

// 4. Correct Optional pattern
class UserData extends Data
{
    public function __construct(
        public Optional|null|string $nickname = new Optional,
    ) {}
}

// 5. Include enum cast
class UserData extends Data
{
    public function __construct(
        #[Required]
        #[WithCast(EnumCast::class)]
        public UserStatusEnum $status,
    ) {}
}

// 6. Correct PHPDoc Collection format
/**
 * @property Collection<int, UserData> $users List of users
 */

// 7. Annotations on separate lines
class UserData extends Data
{
    public function __construct(
        #[Required]
        #[StringType]
        public string $name,
    ) {}
}
```

## Checklist for Data Classes

Before considering a Data class complete:

- ✅ Extends `Spatie\LaravelData\Data`
- ✅ All properties defined in constructor (NOT outside)
- ✅ Uses validation annotations (NOT manual rules())
- ✅ Each annotation on its own line
- ✅ Uses `Collection` for collections (NOT array)
- ✅ Uses `#[DataCollectionOf(Class::class)]` for collections
- ✅ Uses `Optional|null|Type $prop = new Optional` for optional fields
- ✅ Uses `#[WithCast(EnumCast::class)]` for enums
- ✅ Has `messages()` method for custom error messages (if needed)
- ✅ Has PHPDoc block documenting properties
- ✅ Collection PHPDoc uses `Collection<int, Type>` format (with key type)
- ✅ Has `#[TypeScript()]` if used in frontend
- ✅ Has static factory methods for common use cases (if applicable)

## Common Imports

```php
// Base
use Spatie\LaravelData\Data;
use Spatie\LaravelData\Optional;

// Collections
use Illuminate\Support\Collection;
use Spatie\LaravelData\Attributes\DataCollectionOf;

// Validation
use Spatie\LaravelData\Attributes\Validation\Required;
use Spatie\LaravelData\Attributes\Validation\Nullable;
use Spatie\LaravelData\Attributes\Validation\StringType;
use Spatie\LaravelData\Attributes\Validation\IntegerType;
use Spatie\LaravelData\Attributes\Validation\BooleanType;
use Spatie\LaravelData\Attributes\Validation\Email;
use Spatie\LaravelData\Attributes\Validation\Min;
use Spatie\LaravelData\Attributes\Validation\Max;
use Spatie\LaravelData\Attributes\Validation\Present;

// Casts
use Spatie\LaravelData\Attributes\WithCast;
use Spatie\LaravelData\Casts\EnumCast;

// TypeScript
use Spatie\TypeScriptTransformer\Attributes\TypeScript;
```

## Reference Documentation

- Full documentation: `docs/development/using-laravel-data.md`
- Custom validation attributes: See existing in `app/Data/LaravelData/Attributes/Validation/`
- Existing Data classes: Browse `app/Data/` for examples

## Final Reminder

**Top 4 mistakes to avoid:**

1. ❌ **Defining properties outside constructor** - Always use constructor property promotion
2. ❌ **Writing manual rules()** - Always use validation annotations
3. ❌ **Using array instead of Collection** - Always use `Collection` with `#[DataCollectionOf]`
4. ❌ **Annotations on same line** - Each annotation should be on its own line

Your goal is to create clean, validated Data classes that are type-safe, well-documented, and follow all Prowi conventions.
