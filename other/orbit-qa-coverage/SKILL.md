---
name: orbit-qa-coverage
description: Code coverage measurement for a WordPress plugin — line / branch / function coverage via PHPUnit + Xdebug or pcov, plus uncovered-file ranking. Catches files / functions never exercised by tests. Use when the user says "code coverage", "what's not tested", "coverage report", "PHPUnit coverage".
---

# 🪐 orbit-qa-coverage — Code coverage measurement

Coverage is necessary but not sufficient. 100% coverage with weak tests = false confidence (hence pair with `/orbit-qa-mutation`). 30% coverage = absolute gaps. This skill finds those gaps.

---

## Quick start

```bash
# With Xdebug
XDEBUG_MODE=coverage vendor/bin/phpunit --coverage-html reports/coverage --coverage-text

# With pcov (faster)
vendor/bin/phpunit -d pcov.enabled=1 --coverage-html reports/coverage --coverage-text
```

Open `reports/coverage/index.html` for line-by-line view.

---

## What it measures

### 1. Line coverage
"Did this line execute during the test suite?" Most basic.

### 2. Branch coverage
"Did each branch of every conditional execute?" 
```php
if ( $a ) {  // branch A
  ...
} else {     // branch B
  ...
}
```
Both A and B must hit. Line coverage might say 100% if only A ran.

### 3. Function coverage
"Was each function called?" Spots whole untested files.

### 4. Uncovered file ranking
Sort by largest uncovered files — fix big gaps first.

---

## Targets

| Layer | Min | Good | Excellent |
|---|---|---|---|
| Critical paths (security, billing) | 80% | 95% | 100% |
| Business logic | 60% | 80% | 90% |
| Glue / boilerplate | 30% | 50% | 70% |
| Vendor / third-party | exclude | exclude | exclude |

**Whitepaper intent:** 80% as a global target is lazy — different code matters differently. Critical paths need 95%+. Boilerplate (autoloaders, plugin headers) can be 0% covered without harm.

---

## Configure phpunit.xml.dist

```xml
<phpunit>
  <coverage>
    <include>
      <directory suffix=".php">src</directory>
      <directory suffix=".php">includes</directory>
    </include>
    <exclude>
      <directory>vendor</directory>
      <directory>tests</directory>
      <file>my-plugin.php</file>
    </exclude>
    <report>
      <html outputDirectory="reports/coverage"/>
      <text outputFile="php://stdout" showOnlySummary="true"/>
    </report>
  </coverage>
  <testsuites>
    <testsuite name="unit"><directory>tests/unit</directory></testsuite>
    <testsuite name="integration"><directory>tests/integration</directory></testsuite>
  </testsuites>
</phpunit>
```

---

## CI gate

```bash
COVERAGE=$(vendor/bin/phpunit --coverage-text | grep 'Lines:' | awk '{print $2}' | tr -d '%')
if (( $(echo "$COVERAGE < 70" | bc -l) )); then
  echo "Coverage $COVERAGE% < 70%"
  exit 1
fi
```

---

## Common low-coverage causes

### No tests for `register_activation_hook` / `uninstall.php`
These run once but break entire installs when wrong. Always test.

### Admin-only code
Run integration tests as admin user. Use `wp-cli` or factory user creation.

### Branches inside callbacks (filters / actions)
`add_filter` callbacks aren't called by your unit tests unless your test triggers the filter. Use `apply_filters` in tests.

### Error paths
The `try { } catch { }` catch block. Trigger it deliberately:
```php
public function test_rejects_invalid_input() {
  $this->expectException( InvalidArgumentException::class );
  $this->plugin->save( 'bad-input' );
}
```

---

## Output

```markdown
# Code Coverage — my-plugin

Lines: 73% (4,182 / 5,727)
Branches: 61%
Functions: 84%

## Largest uncovered files
- includes/class-uninstall.php — 0% (0/124 lines)
   → ⚠ uninstall.php is the highest-leverage file to test
- includes/class-rest-api.php — 22% (44/200)
   → Test each endpoint via WP_REST_Request
- includes/class-payment-gateway.php — 35% (68/195)
   → Mock Stripe SDK, cover error paths
- includes/admin/class-settings.php — 45% (157/348)

## Recommendation
Add 2 test files (uninstall + rest-api) to reach 80%+ overall.
```

---

## Pair with

- `/orbit-qa-mutation` — coverage tells you "hit"; mutation tells you "covered well"
- `/orbit-uninstall-test` — uninstall.php specifically
- `/orbit-rest-fuzzer` — REST endpoints

---

## Sources & Evergreen References

### Canonical docs
- [PHPUnit Coverage](https://docs.phpunit.de/en/12.0/code-coverage.html) — official
- [Xdebug Coverage](https://xdebug.org/docs/code_coverage) — driver
- [pcov](https://github.com/krakjoe/pcov) — faster alt to Xdebug for coverage

### Rule lineage
- pcov as preferred coverage driver — since 2019, faster than Xdebug
- Branch coverage stable — long-standing PHPUnit feature

### Last reviewed
- 2026-04-29
