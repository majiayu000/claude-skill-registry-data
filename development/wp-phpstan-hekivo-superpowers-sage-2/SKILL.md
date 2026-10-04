---
name: superpowers-sage:wp-phpstan
description: >
  PHPStan static analysis in Sage/Acorn projects — lando composer phpstan,
  phpstan.neon configuration, PHPStan level 0-9, WordPress PHP stubs,
  szepeviktor/phpstan-wordpress, baseline generation, CI phpstan,
  suppress errors, type errors, return type mismatch, nullable types,
  WordPress function stubs, WP_Post WP_Query WP_User types
user-invocable: false
---

# Static Analysis for Sage/Acorn with PHPStan

## When to use

- Setting up static analysis on a Sage theme for the first time
- Adding PHPStan to an existing project and managing the baseline
- Fixing type errors reported by PHPStan in Sage/Acorn code
- Configuring CI pipelines to enforce static analysis
- Incrementally raising the PHPStan analysis level

## Inputs required

- Current PHPStan level (if already configured), or confirmation this is a fresh setup
- Whether Larastan and WordPress stubs are already installed
- Target analysis level (or follow the recommended progression)
- CI platform in use (GitHub Actions, GitLab CI, etc.) if configuring CI integration

## Procedure

### 1. Install dependencies

```bash
lando theme-composer require --dev phpstan/phpstan larastan/larastan szepeviktor/phpstan-wordpress
```

This installs:

- **phpstan/phpstan** — the core static analysis engine
- **larastan/larastan** — Laravel-specific extensions (facades, models, service container, Eloquent)
- **szepeviktor/phpstan-wordpress** — WordPress function stubs and type definitions

### 2. Configure `phpstan.neon`

Create or update `phpstan.neon` in the theme root:

```neon
includes:
    - vendor/larastan/larastan/extension.neon
    - vendor/szepeviktor/phpstan-wordpress/extension.neon

parameters:
    paths:
        - app/

    level: 0

    # WordPress dynamic functions that PHPStan cannot resolve
    ignoreErrors:
        - '#Function apply_filters invoked with#'
        - '#Function do_action invoked with#'
        - '#Function add_filter expects#'
        - '#Function add_action expects#'

    # Scan files for WordPress global function definitions
    scanDirectories:
        - vendor/szepeviktor/phpstan-wordpress/bootstrap.php

    # Treat Acorn facades correctly via Larastan
    checkGenericClassInNonGenericObjectType: false
```

### 3. Run the initial analysis

```bash
lando theme-composer exec phpstan -- analyse
```

At level 0, this should produce few or no errors. If errors exist, fix them or generate a baseline.

### 4. Generate a baseline

A baseline captures all existing errors so they can be addressed incrementally without blocking development.

```bash
lando theme-composer exec phpstan -- analyse --generate-baseline
```

This creates `phpstan-baseline.neon`. Include it in the main config:

```neon
includes:
    - vendor/larastan/larastan/extension.neon
    - vendor/szepeviktor/phpstan-wordpress/extension.neon
    - phpstan-baseline.neon
```

New code must pass analysis; baseline errors are addressed over time.

### 5. Common fixes for Sage/Acorn/WordPress patterns

#### WordPress hook callbacks

```php
// PHPStan complains about callable types
// Fix: use explicit Closure or typed callable
add_filter('the_content', function (string $content): string {
    return $content . '<p>Appended</p>';
});
```

#### ACF field return types

```php
// get_field() returns mixed — PHPStan cannot infer the type
// Fix: assert or cast the return value
/** @var string|null $subtitle */
$subtitle = get_field('subtitle');

// Or use a wrapper with PHPDoc
/**
 * @return array<string, mixed>
 */
function get_hero_fields(): array
{
    return (array) get_field('hero_section') ?: [];
}
```

#### Mixed return from `get_field`

```php
// Bad — PHPStan reports "Cannot access property on mixed"
$image = get_field('image');
echo $image['url']; // Error

// Good — type-narrow first
$image = get_field('image');
if (is_array($image) && isset($image['url'])) {
    echo $image['url'];
}
```

#### Eloquent model properties

Larastan handles most Eloquent patterns automatically. For custom model attributes, add PHPDoc:

```php
/**
 * @property int $id
 * @property string $title
 * @property \Carbon\Carbon $created_at
 */
class Event extends Model
{
    // ...
}
```

### 6. Level progression strategy

| Level | Catches | Effort | Recommendation |
|---|---|---|---|
| **0** | Basic errors, unknown classes | Minimal | Start here |
| **1** | Possibly undefined variables | Low | Move to quickly |
| **2** | Unknown methods on mixed | Low | Move to quickly |
| **3** | Return types checked | Moderate | First real milestone |
| **4** | Basic dead code detection | Moderate | Good target for most projects |
| **5** | Argument types checked | High | Requires disciplined typing |
| **6+** | Strict union/intersection types | Very high | For projects committed to strict typing |

**Recommended progression:**

- **0 to 3**: Move quickly. These levels catch real bugs with minimal effort. Fix issues as you go.
- **3 to 5**: Requires adding return types and parameter types. Use the baseline to manage existing code while enforcing types on new code.
- **5+**: Only pursue if the team commits to strict typing throughout the codebase.

After raising the level, regenerate the baseline:

```bash
lando theme-composer exec phpstan -- analyse --generate-baseline
```

### 7. CI integration

Run PHPStan in CI without progress output:

```bash
lando theme-composer exec phpstan -- analyse --no-progress --error-format=github
```

#### GitHub Actions example

```yaml
- name: Run PHPStan
  run: |
    cd web/app/themes/<theme-name>
    composer exec phpstan -- analyse --no-progress --error-format=github
```

The `--error-format=github` flag produces annotations that appear inline on pull requests.

#### Preventing baseline growth

In CI, verify the baseline has not grown:

```bash
# Regenerate baseline and check for changes
lando theme-composer exec phpstan -- analyse --generate-baseline
git diff --exit-code phpstan-baseline.neon
```

If the diff is non-empty, the PR introduces new errors that must be fixed.

### 8. Integration with Acorn

Larastan provides analysis support for Laravel patterns used in Acorn:

- **Facades**: Larastan resolves facade accessors to their underlying classes
- **Service container**: `app()->make()` and dependency injection are type-aware
- **Eloquent models**: relationships, scopes, and attributes are analyzed
- **Collections**: return types through collection chains are tracked
- **Config/View**: `config()` and `view()` calls are understood

No additional configuration is needed beyond including `larastan/extension.neon`.

## Verification

- [ ] `lando theme-composer exec phpstan -- analyse` runs without errors (or only baseline errors)
- [ ] `phpstan.neon` includes both Larastan and WordPress stubs extensions
- [ ] Baseline file exists and is included in the config
- [ ] Analysis level matches the project's target level
- [ ] CI pipeline runs PHPStan and fails on new errors
- [ ] No new errors added to the baseline without justification

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| "Class not found" for WordPress functions | WordPress stubs not installed or not included | Verify `szepeviktor/phpstan-wordpress` is installed and included in `phpstan.neon` |
| "Class not found" for Acorn facades | Larastan not included | Verify `larastan/larastan` is installed and `extension.neon` is included |
| Hundreds of errors on first run | Level set too high for current codebase | Start at level 0, generate baseline, increment gradually |
| Baseline keeps growing | New code introducing type errors | Enforce CI check that baseline does not grow |
| Memory exhaustion during analysis | Large codebase or too many paths scanned | Limit `paths` to `app/`, increase PHP memory limit in `phpstan.neon`: `parameters.memoryLimit: 512M` |
| False positives on WordPress hooks | Dynamic invocation patterns | Add specific patterns to `ignoreErrors` in `phpstan.neon` |
| Larastan conflicts with PHPStan version | Version mismatch | Check Larastan compatibility matrix, pin compatible versions in `composer.json` |

## Escalation

- If PHPStan reports errors that appear to be false positives in WordPress or Acorn code, check the GitHub issues for `szepeviktor/phpstan-wordpress` and `larastan/larastan` before suppressing
- For complex type issues involving WordPress hooks or ACF, consider writing custom PHPStan extensions or type stubs
- If the baseline grows uncontrollably, schedule a dedicated refactoring session to reduce it rather than ignoring it
- For questions about level progression strategy, discuss with the team lead to set a realistic target level
