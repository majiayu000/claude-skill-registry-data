---
name: deptrac-fixer
description: Diagnose and fix Deptrac architectural violations by refactoring code to respect hexagonal architecture boundaries. Use when Deptrac reports dependency violations ("must not depend on"), layers are incorrectly coupled, the Domain layer imports framework code, or Infrastructure calls Application handlers directly. Never modifies deptrac.yaml — always fixes the code to match the architecture.
---

# Deptrac Fixer Skill

## Profile keys consumed

- `make.deptrac`
- `make.tests`
- `make.ci`
- `quality.deptrac_violations`
- `architecture.source_root`
- `architecture.bounded_contexts`
- `architecture.shared_context`
- `persistence.mapper`
- `framework.name`
- `framework.api_platform`

## Context (Input)

- The target mapped by `make.deptrac` reports violations
- Error message contains "must not depend on"
- Domain layer has framework imports (`framework.name` components, Doctrine, API Platform)
- Infrastructure directly calls Application handlers
- Any architectural boundary violation detected

If `make.deptrac` is `null`, the capability is absent — record a degrade note and stop instead of inventing a target.

## Task (Function)

Diagnose and fix Deptrac violations by refactoring code to respect hexagonal architecture boundaries.

**Success criteria**: the target mapped by `make.deptrac` reports `quality.deptrac_violations` violations — a **fixed ceiling of `0`** that may never be raised (relaxing it would lower the bar; raise-only thresholds and fixed ceilings per ADR-7).

---

## Core Principle

**Fix the code, NEVER modify `deptrac.yaml`**

The architecture is correct. The code must conform to it, not vice versa.

---

## Quick Start: Fix a Violation

### Step 1: Run Deptrac

Run the target mapped by `make.deptrac`.

### Step 2: Parse Violation Message

```text
Domain must not depend on Symfony
  <architecture.source_root>/<Context>/Domain/Entity/Customer.php:8
    uses Symfony\Component\Validator\Constraints as Assert
```

`<Context>` is one of `architecture.bounded_contexts` (or `architecture.shared_context`).

**Extract:**

- **Violating layer**: Domain
- **Forbidden dependency**: the framework component
- **File & line**: path under `architecture.source_root`
- **Violation type**: `uses` (import statement)

### Step 3: Identify Fix Pattern

| Violation                    | Fix pattern                                            |
| ---------------------------- | ------------------------------------------------------ |
| Domain → framework validator | Move constraints to validator YAML config (Pattern 1)  |
| Domain → Doctrine (ORM/ODM)  | Move mapping to XML files (Pattern 2)                  |
| Domain → API Platform        | Move resource config to YAML (Pattern 3)               |
| Infrastructure → Handler     | Use Command Bus (Pattern 4)                            |

### Step 4: Apply Fix

Apply the matching pattern below, then re-run the target mapped by `make.deptrac`. Repeat until zero violations.

---

## Layer Dependency Rules

```text
Domain ─────────────────> (NO dependencies)
           │
Application ──────────> Domain + Infrastructure + framework + API Platform
           │
Infrastructure ───────> Domain + Application + framework + Doctrine
```

| Layer              | Can depend on                                           |
| ------------------ | ------------------------------------------------------- |
| **Domain**         | Nothing (pure PHP only)                                 |
| **Application**    | Domain, Infrastructure, `framework.name`, API Platform  |
| **Infrastructure** | Domain, Application, `framework.name`, Doctrine         |

Layers repeat per bounded context: `<architecture.source_root>/<context>/{Domain,Application,Infrastructure}` for each entry in `architecture.bounded_contexts`, plus the shared kernel under `architecture.shared_context` when set.

---

## Common Fix Patterns (Quick Reference)

### Pattern 1: Domain → Framework Validator

❌ **Problem**: validation attributes in a Domain entity

```php
use Symfony\Component\Validator\Constraints as Assert;

class Customer {
    #[Assert\NotBlank]
    private string $name;
}
```

✅ **Solution**: move validation to the framework's validator config (e.g. `config/validator/{Entity}.yaml`)

### Pattern 2: Domain → Doctrine Annotations

❌ **Problem**: Doctrine attributes in a Domain entity

```php
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity]
class Customer { }
```

✅ **Solution**: create XML mapping in `config/doctrine/` — file suffix follows `persistence.mapper` (`.orm.xml` for `doctrine-orm`, `.mongodb.xml` for `doctrine-odm`)

### Pattern 3: Domain → API Platform

Applies only when `framework.api_platform` is set (not `false`).

❌ **Problem**: API Platform attributes in a Domain entity

```php
use ApiPlatform\Metadata\ApiResource;

#[ApiResource]
class Customer { }
```

✅ **Solution**: create YAML config in `config/api_platform/resources/{entity}.yaml`

### Pattern 4: Infrastructure → Application Handler

❌ **Problem**: direct handler call from Infrastructure

```php
class Repository {
    public function __construct(
        private SomeHandler $handler  // ❌ Circular dependency
    ) {}
}
```

✅ **Solution**: use the Command Bus pattern

```php
class Repository {
    public function __construct(
        private CommandBusInterface $commandBus  // ✅ Interface
    ) {}

    public function someMethod() {
        $this->commandBus->dispatch(new SomeCommand());
    }
}
```

---

## Diagnostic Workflow

When facing multiple violations:

1. **Get all violations**: run the target mapped by `make.deptrac` and capture the output to a scratch file.
2. **Categorize by layer pair**: Domain → framework, Domain → Doctrine, Domain → API Platform, Infrastructure → Application, etc. Group per bounded context (`architecture.bounded_contexts`).
3. **Fix in priority order**:
   1. **Domain violations first** (most critical — purity of the core)
   2. **Infrastructure violations** (circular dependencies)
   3. **Application violations** (least common)
4. **Verify incrementally**: re-run the target mapped by `make.deptrac` after each fix. Track progress: 15 violations → 10 → 5 → 0.

---

## Constraints (Parameters)

### NEVER

- Modify `deptrac.yaml` to allow violations
- Disable Deptrac checks
- Add suppression comments or ignore directives (`@SuppressWarnings`, `@psalm-suppress`, `@phpstan-ignore*`, `@infection-ignore*`, `phpcs:ignore`)
- Create "wrapper" classes to hide dependencies
- Move an entire class to the wrong layer just to satisfy Deptrac
- Move classes into unrelated/random directories just to make Deptrac pass (for example, hiding `Generator` classes under `Factory`)
- Brute-force Deptrac by reorganizing code around tool output instead of business responsibility
- Create ad-hoc directory/class types; use only well-known software patterns (e.g., Strategy, Factory, Provider, Resolver, CQRS Command/Handler)
- Use reflection or dynamic loading to bypass checks

### ALWAYS

- Fix the code to match the architecture
- Keep the Domain layer pure (no framework imports)
- Use interfaces for cross-layer dependencies
- Move configuration to YAML/XML files
- Keep "Directory X contains ONLY class type X" semantics
- For new directories/classes, use explicit, well-known pattern names aligned with DDD/CQRS
- Verify fixes with the target mapped by `make.deptrac` after each change
- Check that tests still pass after refactoring (target mapped by `make.tests`)

---

## Format (Output)

Expected Deptrac output:

```text
Deptrac

Checking dependencies...

✅ No violations found
```

Expected CI output: the target mapped by `make.ci` passes.

---

## Verification Checklist

After fixing violations:

- [ ] Target mapped by `make.deptrac` shows `quality.deptrac_violations` (= 0) violations
- [ ] Domain entities have no framework imports
- [ ] Validation moved to the framework's validator config
- [ ] Doctrine mapping moved to XML (suffix per `persistence.mapper`)
- [ ] API Platform config moved to YAML (when `framework.api_platform` is set)
- [ ] Infrastructure uses Command Bus, not direct handler calls
- [ ] All tests still pass (target mapped by `make.tests`)
- [ ] Target mapped by `make.ci` passes completely

---

## Anti-Patterns to Avoid

### ❌ DON'T Modify deptrac.yaml

```yaml
# ❌ NEVER DO THIS
paths:
  - { collector: layer_domain, exclude: '.*Annotation.*' } # Hiding violations
```

### ❌ DON'T Create Wrapper Classes

```php
// ❌ BAD: Hiding framework dependency
class MyValidator {
    private SymfonyValidator $validator;  // Still violates!
}
```

### ❌ DON'T Move Classes to the Wrong Layer

```php
// ❌ BAD: Moving a Domain entity to Application to "fix" a violation
// <source_root>/<Context>/Application/Entity/Customer.php  // WRONG LAYER!
```

### ✅ DO Fix the Root Cause

- Extract validation to YAML
- Move mapping configuration to XML
- Use interfaces and dependency inversion
- Respect layer responsibilities

---

## Quick Commands

```bash
# Run Deptrac analysis: the target mapped by make.deptrac

# Check uncovered dependencies (generic tooling, works in any repo)
vendor/bin/deptrac analyze --report-uncovered

# Verify architecture after fixes: make.deptrac, then make.ci
```

```yaml # profile-example
# Upstream reference profile values this skill reads:
architecture:
  source_root: src
  bounded_contexts: [User, OAuth]
  shared_context: Shared
make:
  deptrac: deptrac   # invoked as `make deptrac`
  tests: tests
  ci: ci
quality:
  deptrac_violations: 0
persistence:
  mapper: doctrine-odm   # mappings live in config/doctrine/*.mongodb.xml
```

---

## Related Skills

- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) — understanding DDD patterns and layer responsibilities
- [api-platform-crud](../api-platform-crud/SKILL.md) — YAML-based API Platform configuration
- [database-migrations](../database-migrations/SKILL.md) — XML-based Doctrine mappings
- [complexity-management](../complexity-management/SKILL.md) — refactoring without breaking architecture
- [quality-standards](../quality-standards/SKILL.md) — overview of all protected thresholds

---

## Success Criteria Summary

- Zero Deptrac violations (`quality.deptrac_violations` ceiling)
- Domain layer pure (no framework imports)
- All configuration externalized (YAML/XML)
- Proper use of Command Bus for cross-layer communication
- All tests passing (target mapped by `make.tests`)
- CI pipeline green (target mapped by `make.ci`)
