---
name: test-validator
description: Validates PHP test files for CakePHP projects, ensuring compliance with testing standards including proper documentation format, Configure::read usage, and avoiding prohibited patterns
---

# PHP Test Validator

A specialized skill for validating PHP test files in CakePHP projects, particularly focused on strict testing principles that ensure tests guarantee production code behavior.

## Core Validation Rules

### 1. Test Documentation Format (保証対象/失敗時の損失)

Every test method MUST have proper PHPDoc with:
- **保証対象**: Numbered list format (1., 2., 3., ...)
- **失敗時の損失**: Business impact if test doesn't exist
- Assertion labels for each verification

**Valid Format:**
```php
/**
 * 機能説明タイトル
 *
 * 保証対象:
 * 1. 具体的な機能・動作の説明
 * 2. 別の保証対象
 * 失敗時の損失:
 * - このテストが存在しない場合の問題
 * - ビジネスへの影響
 */
public function testSomeFeature(): void
{
    // 保証対象1: 具体的な検証内容
    $result = $this->doSomething();
    $this->assertResponseOk();
}
```

### 2. Configure::read() Usage Validation

**Required Pattern:**
- Use `Configure::read()` for all configuration values
- Never hardcode status values or flags
- Include `use Cake\Core\Configure;` statement in fixtures

**Check for violations:**
```php
// ❌ WRONG: Hardcoded value
$status = 5;

// ✅ CORRECT: Using Configure::read
$status = Configure::read('Application.Status.applying');
```

### 3. Prohibited Patterns Detection

**Critical Violations:**
- `Configure::write()` in test methods
- Mocking production code (Components, Models, Helpers)
- Schema definition in model files (`_initializeSchema`)
- Creating test data outside fixtures (with limited exceptions)
- Fallback mechanisms without specification

### 4. Production Code Verification

**Check that test targets existing production code:**
- Controller file exists
- Action method exists
- Route is defined
- URL pattern matches

### 5. Docker Command Validation

**Approved commands only:**
```bash
# ✅ CORRECT
docker compose -f docker-compose.test.yml run --rm web

# ❌ WRONG
composer test
vendor/bin/phpunit
```

## Validation Process

When analyzing a test file:

1. **Parse PHPDoc blocks** - Check for 保証対象/失敗時の損失 format
2. **Scan for hardcoded values** - Identify potential Configure::read violations
3. **Detect prohibited patterns** - Search for Configure::write, mocking, etc.
4. **Verify production code** - Confirm controller/action/route existence
5. **Check fixture compliance** - Ensure proper fixture usage patterns

## Output Format

Return validation results as:
```
✅ PASS: [Description of what passed]
❌ FAIL: [Description of violation]
   Line X: [Code snippet or issue]
   Fix: [Suggested correction]
⚠️ WARN: [Non-critical issue]
```

## Examples

### Example 1: Validating test documentation
```php
// Input: Test method without proper documentation
public function testIndex(): void
{
    $this->get('/user/users');
    $this->assertResponseOk();
}

// Output:
❌ FAIL: Missing required PHPDoc documentation
   Line 1: testIndex() lacks 保証対象 and 失敗時の損失
   Fix: Add PHPDoc with numbered 保証対象 list and business impact
```

### Example 2: Detecting Configure::write violation
```php
// Input: Test with configuration override
public function testWithConfig(): void
{
    Configure::write('App.setting', 'test-value');
    // ...
}

// Output:
❌ FAIL: Prohibited pattern - Configure::write in test
   Line 3: Configure::write('App.setting', 'test-value')
   Fix: Use actual production configuration value with Configure::read()
```

## Integration with CakePHP Projects

This skill is specifically designed for:
- CakePHP 4.x projects
- Multi-tenant database architectures
- Projects following strict test principles
- PHP 8.x codebases

## Usage Notes

- Run validation before committing test files
- Integrate with pre-commit hooks
- Use in conjunction with `test-guardian` agent for comprehensive checks
- Particularly important during PHP/CakePHP version upgrades