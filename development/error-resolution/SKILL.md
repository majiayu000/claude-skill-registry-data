---
name: Error Resolution
description: Systematic error diagnosis and resolution for test failures, build errors, and validation issues. Invoke when tests fail or pre-commit blocks.
allowed-tools: [Bash, Read, Edit, Write]
---

# Error Resolution

## Invocation Context

When: test failure, pre-commit block, build error, PHPStan error, architecture violation, layer violation

## Systematic Flow

```
composer test → categorize errors
composer fix:style + composer fix:types (auto-fix)
composer test (rerun)
manual fixes for remaining (see patterns below)
composer test + composer analyze:architecture (verify)
```

## Fix Priority

1. Syntax - `composer test:syntax`
2. Style - `composer fix:style` → `composer test:style`
3. Types - `composer fix:types` + manual types → `composer test:types`
4. Architecture - manual refactor → `composer test:architecture`
5. Layers - manual refactor → `composer analyze:architecture`
6. Logic - fix implementation → targeted test → full suite

## Error Patterns → Actions

### Naming Violation (PSR-1)

**Pattern:** `NamingConventionsTest ... PascalCase/camelCase/SCREAMING_SNAKE_CASE`

**Action:**
- Class/Interface/Trait/Enum: `PascalCase`
- Method: `camelCase`
- Constant: `SCREAMING_SNAKE_CASE`

**Verify:** `composer test:architecture`

### Style Violation

**Pattern:** `(ordered_imports, trailing_comma_in_multiline, ...)`

**Action:** `composer fix:style` → `composer test:style`

### Type Safety (PHPStan L9)

**Pattern:** `has no return type/parameter type/property type`

**Action:**
- Add `declare(strict_types=1)` top of file
- Add param types: `public function find(int $id)`
- Add return types: `public function find(int $id): ?User`
- Add property types: `private UserRepository $repository`
- Run: `composer fix:types` + manual additions

**Verify:** `composer test:types`

### Forbidden Patterns

**Patterns:** trait usage, superglobal, static state, dangerous functions

**Actions:**
- Traits → composition/dependency injection
- `$_GET/$_POST/$_SESSION` → Http\Request abstractions
- Static methods/properties → dependency injection
- `eval/exec/shell_exec` → remove (never use)

**Verify:** `composer test:architecture`

### Complexity Limits

**Pattern:** `GodObject/ComplexityLimits ... max N exceeded`

**Actions:**
- Split class into multiple services
- Reduce public methods (max 10)
- Reduce constructor params (max 4)
- Reduce method lines (max 150)
- Reduce class lines (max 500)

**Verify:** `composer test:architecture`

### Layer Violations (Deptrac)

**Pattern:** `Controllers must not depend on Repositories`

**Action:**
Enforce flow: Controller → Service → Repository

```php
// Wrong: Controller → Repository
class UserController {
    public function __construct(private UserRepository $repo) {}
}

// Correct: Controller → Service → Repository
class UserController {
    public function __construct(private UserService $service) {}
}
```

**Verify:** `composer analyze:architecture`

### Pre-commit Blocked

**Pattern:** `Pre-commit hook failed: PHPStan/CS/Deptrac...`

**Action:**
```
composer test (identify all)
composer fix:style
composer fix:types
manual arch/layer fixes
composer test (verify)
commit
```

### Logic Failure (Unit/Integration)

**Pattern:** `Failed asserting that ...`

**Action:**
```
Read failing test → identify expectation
Read implementation → find logic error
Fix implementation
composer test:unit (or test:integration)
composer test (full verification)
```

## Commands Index

**Syntax:** `composer test:syntax`
**Style:** `composer fix:style`, `composer test:style`
**Types:** `composer fix:types`, `composer test:types`
**Architecture:** `composer test:architecture`
**Layers:** `composer analyze:architecture`
**Suites:** `composer test:unit`, `composer test:integration`, `composer test`
**Coverage:** `composer test:coverage`, `composer test:coverage-report`

## Common Mistakes

- Bypassing pre-commit: `git commit --no-verify` (never do this)
- Ignoring architecture tests when app/ empty (9 tests should still pass)
- Using `@phpstan-ignore` instead of fixing types
