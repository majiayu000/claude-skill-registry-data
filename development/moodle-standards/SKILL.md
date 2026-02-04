---
name: moodle-standards
description: Apply Moodle coding standards (PSR-12 with exceptions) to PHP code. Validates style, naming conventions, PHPDoc, and type hints.
---

# Moodle Standards Skill

Apply Moodle coding standards (PSR-12 + exceptions) to PHP code.

## Trigger
- PHP files in Moodle plugin directories
- User requests code review or formatting
- New file creation in Moodle context

## Actions

### 1. Validate Code Style
Check code against Moodle standards:
- Line length (132 ideal, 180 max)
- Array syntax (`[]` only)
- `else if` not `elseif`
- No closing `?>` tag
- 4-space indentation

### 2. Fix Naming
Ensure proper naming:
- Variables: `$lowercase` (no underscores between words)
- Functions: `component_function_name()` (Frankenstyle)
- Classes: `lowercase_with_underscores`
- Constants: `COMPONENT_CONSTANT_NAME`

### 3. Add PHPDoc
Generate required documentation:
- File header with GPL
- `@package` tag (MANDATORY)
- `@param` with types
- `@return` description

### 4. Type Hints
Add mandatory type declarations:
- Parameter types
- Return types
- Nullable types (`?type`)

## Validation Command
```bash
vendor/bin/phpcs --standard=moodle path/to/file.php
```

## Quick Fixes

### Missing Package Tag
```php
/**
 * @package    mod_myplugin
 */
```

### Wrong Array Syntax
```php
// Before
$arr = array('a', 'b');
// After
$arr = ['a', 'b'];
```

### Wrong Else If
```php
// Before
} elseif ($x) {
// After
} else if ($x) {
```
