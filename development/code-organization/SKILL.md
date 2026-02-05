---
name: code-organization
description: Ensure proper code organization with class names, directories, namespaces, and naming consistency following the principle "Directory X contains ONLY class type X (project)
---

# Code Organization Skill

This skill ensures proper code organization following the core principle: **Directory X contains ONLY class type X**.

## When to Use This Skill

Activate this skill when:

- Creating new classes
- Refactoring existing code
- Moving classes between directories
- Code review feedback about organization
- Renaming classes or methods

## Core Principle

**Directory X should contain ONLY class type X**

Examples:

- `Converter/` → Contains ONLY converters
- `Transformer/` → Contains ONLY transformers
- `Validator/` → Contains ONLY validators
- `Builder/` → Contains ONLY builders
- `Fixer/` → Contains ONLY fixers
- `Cleaner/` → Contains ONLY cleaners
- `Factory/` → Contains ONLY factories
- `Resolver/` → Contains ONLY resolvers

## Quick Reference: Where Does It Belong?

| Class Does                | Belongs In     | Examples             |
| ------------------------- | -------------- | -------------------- |
| Converts types            | `Converter/`   | UlidTypeConverter    |
| Transforms data (DB↔PHP) | `Transformer/` | UlidTransformer      |
| Validates values          | `Validator/`   | UlidValidator        |
| Builds/constructs         | `Builder/`     | ArrayResponseBuilder |
| Fixes/modifies            | `Fixer/`       | ContentPropertyFixer |
| Cleans/filters            | `Cleaner/`     | ArrayValueCleaner    |
| Creates objects           | `Factory/`     | UlidFactory          |
| Resolves values           | `Resolver/`    | ScalarResolver       |
| Serializes/normalizes     | `Serializer/`  | OpenApiNormalizer    |

## Organization Checklist

### 1. Class Location

✅ **CORRECT**:

```php
// File: src/Shared/Infrastructure/Converter/UlidTypeConverter.php
namespace App\Shared\Infrastructure\Converter;

final class UlidTypeConverter  // IS a Converter
{
    public function toUlid(...): Ulid { }
    public function fromBinary(...): Ulid { }
}
```

❌ **WRONG**:

```php
// File: src/Shared/Infrastructure/Transformer/UlidTypeConverter.php
namespace App\Shared\Infrastructure\Transformer;

final class UlidTypeConverter  // IS a Converter, NOT a Transformer!
{
    // This belongs in Converter/, not Transformer/
}
```

### 2. Class Name Consistency

✅ **CORRECT**:

- `UlidValidator` → validates ULIDs
- `UlidTransformer` → transforms for Doctrine
- `UlidTypeConverter` → converts between types
- `CustomerUpdateScalarResolver` → resolves scalar values

❌ **WRONG**:

- `UlidHelper` → Too vague
- `UlidConverter` → Not specific enough
- `UlidUtils` → Extract to specific classes

### 3. Namespace Consistency

Namespace MUST match directory structure:

✅ **CORRECT**:

```php
// File: src/Shared/Infrastructure/Validator/UlidValidator.php
namespace App\Shared\Infrastructure\Validator;
```

❌ **WRONG**:

```php
// File: src/Shared/Infrastructure/Validator/UlidValidator.php
namespace App\Shared\Infrastructure\Transformer;  // Wrong namespace!
```

## Refactoring Workflow

### Step 1: Identify What the Class Does

Ask yourself:

- What is the PRIMARY responsibility of this class?
- Does it convert? → `Converter/`
- Does it transform? → `Transformer/`
- Does it validate? → `Validator/`
- Does it build? → `Builder/`
- Does it fix? → `Fixer/`
- Does it clean? → `Cleaner/`
- Does it resolve? → `Resolver/`

### Step 2: Check the Directory

Current location matches responsibility?

- ✅ YES → Class is correctly placed
- ❌ NO → Move to appropriate directory

### Step 3: Update All References

1. Move the file:

   ```bash
   mv src/Path/OldDir/Class.php src/Path/NewDir/Class.php
   ```

2. Update namespace in the file:

   ```php
   namespace App\Path\NewDir;
   ```

3. Update all imports:

   ```bash
   # Find all files using this class
   grep -r "use.*OldDir\\ClassName" src/ tests/

   # Update them (or use IDE refactoring)
   sed -i 's|OldDir\\ClassName|NewDir\\ClassName|g' affected_files
   ```

4. Run quality checks:
   ```bash
   make phpcsfixer
   make psalm
   make unit-tests
   ```

### Step 4: Verify Consistency

Check that:

- [ ] Class is in correct directory
- [ ] Namespace matches directory
- [ ] Class name matches functionality
- [ ] Variable names are specific
- [ ] Parameter names are accurate
- [ ] All tests pass

## Essential Examples

### Example 1: UlidValidator

**Before**:

```php
// ❌ src/Shared/Infrastructure/Transformer/UlidValidator.php
namespace App\Shared\Infrastructure\Transformer;

final class UlidValidator { }  // It's a VALIDATOR, not a Transformer!
```

**After**:

```php
// ✅ src/Shared/Infrastructure/Validator/UlidValidator.php
namespace App\Shared\Infrastructure\Validator;

final class UlidValidator { }
```

### Example 2: CustomerUpdateScalarResolver

**Before**:

```php
// ❌ src/Core/Customer/Application/Factory/CustomerUpdateScalarResolver.php
namespace App\Core\Customer\Application\Factory;

final class CustomerUpdateScalarResolver  // It's a RESOLVER, not a FACTORY!
{
    public function resolveScalarValue(...) { }
}
```

**After**:

```php
// ✅ src/Core/Customer/Application/Resolver/CustomerUpdateScalarResolver.php
namespace App\Core\Customer\Application\Resolver;

final class CustomerUpdateScalarResolver
{
    public function resolveScalarValue(...) { }
}
```

## Variable and Parameter Naming

### Variable Names

✅ **CORRECT** (Specific):

```php
private UlidTypeConverter $typeConverter;
private CustomerUpdateScalarResolver $scalarResolver;
```

❌ **WRONG** (Vague):

```php
private UlidTypeConverter $converter;      // Converter of what?
private CustomerUpdateScalarResolver $resolver;  // Resolver of what?
```

### Parameter Names

✅ **CORRECT** (Accurate):

```php
public function toPhpValue(mixed $value): Ulid  // Accepts mixed
public function fromBinary(mixed $value): Ulid  // Accepts mixed despite name
```

❌ **WRONG** (Misleading):

```php
public function fromBinary(mixed $binary): Ulid  // Name suggests only binary
```

## Common Mistakes to Avoid

1. **Don't create "Helper" or "Util" classes**

   - These are code smells
   - Extract specific responsibilities into properly named classes

2. **Don't put multiple class types in one directory**

   - Converters don't belong in Transformer/
   - Validators don't belong in Converter/

3. **Don't use vague variable names**

   - `$converter` → `$typeConverter` (be specific)
   - `$data` → `$customerData` (be descriptive)

4. **Don't mismatch parameter names with types**
   - If parameter accepts `mixed`, don't name it after one type

## PHP Best Practices

### Use Constructor Property Promotion

✅ **CORRECT**:

```php
final readonly class CustomerUpdateFactory
{
    public function __construct(
        private CustomerRelationTransformerInterface $relationResolver,
        private CustomerUpdateScalarResolver $scalarResolver,
    ) {
    }
}
```

### Always Inject All Dependencies

✅ **CORRECT** (All dependencies injected):

```php
public function __construct(
    private readonly IriReferenceMediaTypeTransformerInterface $mediaTypeTransformer
) {
}
```

❌ **WRONG** (Default instantiation):

```php
public function __construct(
    ?IriReferenceMediaTypeTransformerInterface $mediaTypeTransformer = null
) {
    $this->mediaTypeTransformer = $mediaTypeTransformer
        ?? new IriReferenceMediaTypeTransformer();  // ❌ Direct instantiation!
}
```

For complete PHP best practices, see [php-best-practices.md](php-best-practices.md).

## Pre-Commit Checklist

Before committing code organization changes:

```bash
# 1. Check code style
make phpcsfixer

# 2. Check static analysis
make psalm

# 3. Run unit tests
make unit-tests

# 4. Verify consistency
grep -r "^namespace" src/ --include="*.php" | head -10
```

## Success Criteria

✅ Directory contains only the type of class it's named for
✅ Class name accurately describes functionality
✅ Namespace matches directory structure
✅ Variable names are specific and clear
✅ Parameter names match their actual types
✅ All tests pass
✅ No Psalm errors
✅ Code style compliant

## Related Skills

- **quality-standards**: Maintains code quality metrics
- **ci-workflow**: Runs comprehensive checks
- **code-review**: Handles PR feedback about organization
- **testing-workflow**: Ensures proper test coverage

## Additional Resources

- [php-best-practices.md](php-best-practices.md) - Complete PHP best practices guide
- [examples/refactoring-examples.md](examples/refactoring-examples.md) - Detailed before/after examples
- [reference/directory-structure.md](reference/directory-structure.md) - Layer-by-layer breakdown
- [reference/common-patterns.md](reference/common-patterns.md) - Pattern catalog
- [reference/troubleshooting.md](reference/troubleshooting.md) - Troubleshooting guide for common issues
- [../.claude/skills/SKILL-DECISION-GUIDE.md](../SKILL-DECISION-GUIDE.md) - When to use which skill
