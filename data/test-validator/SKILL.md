---
name: test-validator
description: Validates PHP test files for CakePHP projects, ensuring compliance with testing standards including proper documentation format, Configure::read usage, and avoiding prohibited patterns
hooks:
  SessionStart:
    - type: command
      command: |
        if command -v yq &> /dev/null && [ -f ".claude/config.yaml" ]; then
          echo "=== Testing Constraints ==="
          yq -o=json '.constraints.testing' .claude/config.yaml 2>/dev/null || true
          yq -o=json '.constraints.schema' .claude/config.yaml 2>/dev/null || true
          yq -o=json '.constraints.business_rules' .claude/config.yaml 2>/dev/null || true
        fi
---

# PHP Test Validator

A specialized skill for validating PHP test files in CakePHP projects, particularly focused on strict testing principles that ensure tests guarantee production code behavior.

## Configuration

This skill reads project-specific test rules from:
1. `.claude/config.yaml` - `testing.rules.documentation` path
2. `tests/README.md` - Project test documentation (default)

```yaml
# .claude/config.yaml
testing:
  rules:
    documentation: "tests/README.md"
```

## Core Principle

> **Test code exists to guarantee the functionality of production code. Code that contradicts this purpose is prohibited.**

All validation rules derive from this principle. Tests must:
- Execute production code paths
- Use production configuration
- Verify actual behavior, not code structure

## Core Validation Rules

### 1. Test Documentation Format

Test documentation format is defined in project configuration:

```yaml
# .claude/config.yaml
testing:
  documentation_format: "tests/README.md"  # Path to project-specific format rules
```

**Default requirements** (when no project-specific format defined):
- `@covers` annotation specifying the target class/method
- `@group` annotation for test categorization
- Clear test method naming (`test<Action><ExpectedBehavior>`)

**Example:**
```php
/**
 * @covers \App\Controller\UsersController::index
 * @group integration
 */
public function testIndexReturnsUserList(): void
{
    $this->get('/users');
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

All patterns violate the core principle. See `tests/README.md` for project-specific examples.

**Critical Violations:**

| # | Category | Pattern | Why Prohibited |
|---|----------|---------|----------------|
| 1 | Conditional | `if`, `??`, `try-catch` with assertions | Result depends on execution path |
| 2 | Config Override | `Configure::write()` | Test uses different config than production |
| 3 | Missing @covers | Test without `@covers` annotation | Coverage target unknown |
| 4 | Existence Check | `method_exists()`, `class_exists()` | Tests code structure, not behavior |
| 5 | Placeholder | `markTestSkipped()`, `assertTrue(true)` | No actual verification |
| 6 | PHPDoc Content | `NOTE:`, dates, impl notes in PHPDoc | Spec only, no implementation details |
| 7 | Defensive Definition | `if (!defined()) { define(); }` | Masks production errors where constant is undefined |
| 8 | Shallow Assertion | Only `assertResponseOk()` without business logic verification | Tests HTTP status, not actual functionality |
| - | Mock Production | Mock Components, Models, Helpers | Business logic not tested |
| - | Schema Override | `_initializeSchema` in Model | DB schema diverges from migration |
| - | Direct Data | `newEntity()` without Fixture | Test data diverges from production |

**Rule 7 - Defensive Definition Details:**

Test code should NOT protect against undefined constants, classes, or functions. If production code requires them, the test should fail when they're missing.

```php
// ❌ WRONG: Defensive definition masks production errors
if (!defined('APP_VERSION')) {
    define('APP_VERSION', '1.0.0');
}

// ❌ WRONG: Defensive class existence check
if (!class_exists('SomeService')) {
    class SomeService { /* mock */ }
}

// ✅ CORRECT: Let the test fail if constant is undefined
// Production code should define APP_VERSION; test should verify it exists
$this->assertNotEmpty(APP_VERSION);
```

**Rule 8 - Shallow Assertion Details:**

`assertResponseOk()` only verifies HTTP 2xx status. It does NOT verify:
- Response body content matches expected data
- Database state changed correctly
- Business rules were applied

```php
// ❌ WRONG: Only checks HTTP status
public function testCreateUser(): void
{
    $this->post('/users', ['name' => 'John']);
    $this->assertResponseOk();  // Passes even if user wasn't created!
}

// ✅ CORRECT: Verify actual business outcome
public function testCreateUser(): void
{
    $this->post('/users', ['name' => 'John']);
    $this->assertResponseOk();

    // Verify database state
    $user = $this->Users->find()->where(['name' => 'John'])->first();
    $this->assertNotNull($user);
    $this->assertEquals('John', $user->name);

    // Or verify response content
    $this->assertResponseContains('User created successfully');
}
```

### 4. Production Code Verification

**Check that test targets existing production code:**
- Controller file exists
- Action method exists
- Route is defined
- URL pattern matches

### 5. Test Command Validation

Use the test command defined in project configuration:

```yaml
# .claude/config.yaml
testing:
  command: "docker compose run --rm web vendor/bin/phpunit"  # Example
```

**Validation rules:**
- Only use the command specified in `testing.command`
- Do NOT run test commands directly (e.g., `composer test`, `vendor/bin/phpunit`) unless configured
- Check project configuration before executing tests

### 6. Specification Alignment Validation

Validates alignment between test documentation (README.md) and actual test code.

**Alignment Checks:**
- Test function names match documentation
- Implementation status markers are accurate
- Test counts per category are correct
- Consolidation notes are documented

**Integrity Score:**
```
Score = (Matching Functions / Total Functions in README) × 100

100:    Perfect alignment
90-99:  Minor discrepancies
70-89:  Moderate misalignment - fix before PR
0-69:   Critical misalignment - fix immediately
```

**When to Run:**
- After test code is written or modified
- Before creating PR or committing test changes
- During quality review

## Validation Process

When analyzing a test file:

1. **Load project rules** - Read tests/README.md for project-specific prohibitions
2. **Parse PHPDoc blocks** - Check for required annotations (@covers, @group, etc.)
3. **Scan for hardcoded values** - Identify potential Configure::read violations
4. **Detect prohibited patterns** - Check against core + project-specific patterns
5. **Verify production code** - Confirm controller/action/route existence
6. **Check fixture compliance** - Ensure proper fixture usage patterns
7. **Validate specification alignment** - Compare README.md with actual test code

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
   Line 1: testIndex() lacks @covers annotation
   Fix: Add PHPDoc with @covers specifying the target class/method
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

### Example 3: Conditional assertion violation
```php
// Input: Test with conditional logic
public function testWithCondition(): void
{
    $result = $this->service->process();
    if ($result !== null) {
        $this->assertEquals($expected, $result);
    } else {
        $this->markTestSkipped('No data');
    }
}

// Output:
❌ FAIL: Prohibited pattern - Conditional assertion
   Line 4-8: if/else block with assertions
   Fix: Remove conditional; test should have deterministic expected outcome
```

### Example 4: Existence check violation
```php
// Input: Test checking code structure instead of behavior
public function testMethodExists(): void
{
    $this->assertTrue(method_exists($this->controller, 'index'));
}

// Output:
❌ FAIL: Prohibited pattern - Existence check
   Line 3: method_exists() tests code structure, not behavior
   Fix: Call the method and verify its actual output/behavior
```

## Integration with CakePHP Projects

This skill is specifically designed for:
- CakePHP 4.x/5.x projects
- Multi-tenant database architectures
- Projects following strict test principles
- PHP 8.x codebases

**Configuration File:** `.claude/config.yaml`
**Project Rules:** `tests/README.md`

## Usage Notes

- Read `tests/README.md` first to load project-specific rules
- Run validation before committing test files
- Integrity score must be >= 90 for PR approval
- All ERROR severity issues must be resolved before merge
- Particularly important during PHP/CakePHP version upgrades

## Used By Agents

- **quality-reviewer**: Validates test code during code review
- **deliverable-evaluator**: Gate-check before commit/PR
- **code-developer**: Validates tests during implementation

## Related Skills

This skill supersedes `test-spec-validator` (now integrated):
- Test code quality validation (PHPDoc, assertions, patterns)
- README.md ↔ test code alignment validation