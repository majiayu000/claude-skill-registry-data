---
name: orbit-qa-mutation
description: Mutation testing for PHP via Infection — measures TEST quality (not code quality). Mutates each line of code (e.g. `<` → `<=`, `&&` → `||`) and runs the test suite. If tests still pass, the mutation "survived" = the test missed the bug. Higher kill rate = better tests. Use when the user says "mutation testing", "Infection PHP", "test quality", "are my tests good".
---

# 🪐 orbit-qa-mutation — Infection PHP mutation testing

Tests can pass while having gaping holes. Mutation testing is the test-quality test: deliberately break code, see if tests notice.

---

## Quick start

```bash
# Install once
composer require --dev infection/infection

# Run
vendor/bin/infection --threads=4
```

Output: `infection.log` + `reports/mutation-<timestamp>.md`.

---

## What "mutation" means

Infection rewrites each line of your PHP — small, deterministic changes:

```php
// Original
if ($price > 100) { return true; }

// Mutation 1: `>` → `<`
if ($price < 100) { return true; }

// Mutation 2: `>` → `>=`
if ($price >= 100) { return true; }

// Mutation 3: `true` → `false`
if ($price > 100) { return false; }

// Mutation 4: `100` → `0`
if ($price > 0) { return true; }
```

For each mutation, Infection runs your test suite. If any test fails → mutation "killed." If all pass → mutation "survived." Survived mutations = a real bug your tests would miss.

---

## Mutation Score Indicator (MSI)

```
MSI (Mutation Score Indicator) = killed / total mutations
```

| MSI | Verdict |
|---|---|
| 90%+ | Excellent — tests truly cover behaviour |
| 70-89% | Good |
| 50-69% | Mediocre — tests check existence, not behaviour |
| < 50% | Tests probably just check "doesn't crash" |

---

## Configure for a WP plugin

`infection.json5`:
```json5
{
  "$schema": "https://raw.githubusercontent.com/infection/infection/0.27.0/resources/schema.json",
  "source": { "directories": ["src", "includes"] },
  "phpUnit": { "configDir": "tests" },
  "logs": {
    "text": "infection.log",
    "html": "reports/mutation.html"
  },
  "mutators": {
    "@default": true,
    "@cast": false,    // skip type-casting mutations (noisy in WP)
    "@regex": false    // skip regex mutations (noisy)
  },
  "minMsi": 70,
  "minCoveredMsi": 80
}
```

`minMsi` and `minCoveredMsi` are CI gates — fail the build if score drops.

---

## Common survived mutations

### Off-by-one
```php
// Original — `<=` (inclusive)
for ($i = 0; $i <= count($items); $i++)

// Mutation: `<=` → `<` (exclusive — drops last item)
for ($i = 0; $i < count($items); $i++)
```

If tests don't cover the boundary case (last item), mutation survives.

### Boolean inversion
```php
if ( ! current_user_can( 'manage_options' ) ) wp_die();
// Mutation: drop the !
if ( current_user_can( 'manage_options' ) ) wp_die();
```

If tests don't try a permitted user expecting success AND a denied user expecting fail, mutation survives.

### Default value
```php
$value = get_option( 'my_setting', 'default' );
// Mutation: 'default' → ''
$value = get_option( 'my_setting', '' );
```

If tests don't run with the option missing, mutation survives.

---

## Output

```markdown
# Mutation Testing — my-plugin

Mutations: 1,247
Killed: 1,082 (87%)
Survived: 165 (13%)
Timed out: 0
Skipped: 0

MSI: 87% — Good (target: 90%)

## Top survived mutations (suggested test additions)
- src/class-cart.php:47 — boolean inversion
   → Add test: anonymous user CAN'T add to cart
- src/class-checkout.php:103 — off-by-one in loop
   → Add test: 0-item cart, 1-item cart, max-items cart
- src/class-pricing.php:88 — default fallback
   → Add test: option deleted, expect $0.00 not 'free'
```

---

## Pair with

- `/orbit-qa-coverage` — line coverage (mutation testing IS quality of coverage)
- `/orbit-wp-standards` — clean code easier to mutate-test

---

## Sources & Evergreen References

### Canonical docs
- [Infection PHP](https://infection.github.io/) — root
- [Infection Configuration](https://infection.github.io/guide/usage.html) — config reference
- [Mutation Testing — Wikipedia](https://en.wikipedia.org/wiki/Mutation_testing) — theory
- [Stryker Mutator](https://stryker-mutator.io/) — JS / TS mutation testing

### Rule lineage
- Mutation testing — academic since 1971, practical PHP since Infection 0.x (~2017)
- Infection 1.0 — 2024

### Last reviewed
- 2026-04-29
