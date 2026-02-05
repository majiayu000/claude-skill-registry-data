---
name: complexity-management
description: Maintain and improve code quality using PHPInsights without decreasing quality thresholds. Use when PHPInsights fails, cyclomatic complexity is too high, code quality drops, or when refactoring for better maintainability. Always maintains 93% complexity for src/ and 95% for tests/, plus 100% quality/architecture/style scores.
---

# Code Complexity Management

Maintain exceptional code quality standards using PHPInsights in this Symfony-based microservice. This skill ensures complexity stays manageable while preserving hexagonal architecture, DDD patterns, and CQRS design.

## When to Use This Skill

Use this skill when:

- PHPInsights checks fail (`make phpinsights` returns errors)
- Cyclomatic complexity exceeds thresholds
- Code quality score drops below 100%
- Architecture score falls below 100%
- Style score drops below 100%
- Complexity score falls below thresholds (93% for src/, 95% for tests/)
- Adding new features that increase complexity
- Refactoring existing code for better maintainability
- Before committing code changes (proactive quality check)

## ⚡ Quick Start

**New to complexity refactoring?** Start with the [Quick Start Guide](reference/quick-start.md) for a fast-track workflow with immediate action steps.

## Protected Quality Thresholds

**CRITICAL**: These thresholds are defined in `phpinsights.php` (for src/) and `phpinsights-tests.php` (for tests/) and must NEVER be lowered:

```php
// phpinsights.php (source code in src/)
'requirements' => [
    'min-quality' => 100,      // Code quality
    'min-complexity' => 93,    // Cyclomatic complexity for src/
    'min-architecture' => 100, // Architecture compliance
    'min-style' => 100,        // Coding style
],

// phpinsights-tests.php (test code in tests/)
'requirements' => [
    'min-quality' => 95,       // Code quality for tests
    'min-complexity' => 95,    // Cyclomatic complexity for tests/
    'min-architecture' => 90,  // Architecture compliance for tests
    'min-style' => 95,         // Coding style for tests
],
```

**Policy**: If PHPInsights fails, fix the code - NEVER lower these thresholds.

---

## ⚠️ CRITICAL POLICY: NEVER CHANGE CONFIG

```
╔═══════════════════════════════════════════════════════════════╗
║  When PHPInsights fails, you MUST FIX THE CODE.               ║
║  NEVER lower thresholds in phpinsights.php.                   ║
║                                                               ║
║  ❌ FORBIDDEN: Changing config to pass checks                 ║
║  ✅ REQUIRED:  Refactoring code to meet standards             ║
╚═══════════════════════════════════════════════════════════════╝
```

**Protected thresholds are non-negotiable**:

For source code (src/):

- min-quality: 100% (never lower)
- min-complexity: 93% (never lower)
- min-architecture: 100% (never lower)
- min-style: 100% (never lower)

For tests (tests/):

- min-quality: 95% (never lower)
- min-complexity: 95% (never lower)
- min-architecture: 90% (never lower)
- min-style: 95% (never lower)

If you're tempted to lower a threshold, it means the code needs refactoring, not the config.

---

## Core Workflow

### 1. Identify Complex Classes

**First, find which classes need refactoring**:

```bash
# Find top 20 most complex classes (default)
make analyze-complexity

# Find top 10 classes
make analyze-complexity N=10

# Export as JSON for tracking
make analyze-complexity-json N=20 > complexity-report.json

# Export as CSV for spreadsheets
make analyze-complexity-csv N=15 > complexity.csv
```

**Output shows** for each class:

- **CCN (Cyclomatic Complexity)**: > 15 is critical
- **WMC (Weighted Method Count)**: Sum of all method complexities
- **Avg Complexity**: CCN ÷ Methods (target: < 5)
- **Max Complexity**: Highest complexity of any single method
- **Maintainability Index**: 0-100 (target: > 65)

**See**: [analysis-tools.md](reference/analysis-tools.md) for complete tools documentation

### 2. Run PHPInsights Analysis

```bash
# Using project make command (recommended)
make phpinsights

# Direct execution with verbosity
vendor/bin/phpinsights -v

# Analyze specific directory
vendor/bin/phpinsights analyse src/Customer

# Generate JSON report for parsing
vendor/bin/phpinsights --format=json > insights-report.json
```

### 3. Interpret Results

PHPInsights provides four scores:

```
[CODE] 100.0 pts       ✅ Target: 100%
[COMPLEXITY] 93.5 pts  ✅ Target: 93%+ (src), 95%+ (tests)
[ARCHITECTURE] 100 pts ✅ Target: 100%
[STYLE] 100.0 pts      ✅ Target: 100%
```

**If any score is below threshold**, identify issues:

```bash
# Look for issues by severity
✗ [Complexity] Method `CustomerCommandHandler::handle` has cyclomatic complexity of 12
✗ [Architecture] Class `CustomerRepository` violates layer dependency rules
✗ [Style] Line exceeds 100 characters in CustomerTransformer.php:45
```

### 4. Prioritize Fixes

**Priority Order:**

1. **CRITICAL (Complexity > 15)**: Immediate refactoring required
2. **HIGH (Architecture violations)**: Breaks hexagonal/DDD boundaries
3. **MEDIUM (Complexity 10-15)**: Plan refactoring
4. **LOW (Style issues)**: Quick fixes, often auto-fixable

### 5. Apply Fixes

Based on issue type:

**For Complexity Issues** → See [refactoring-strategies.md](refactoring-strategies.md)
**For Metric Details** → See [reference/complexity-metrics.md](reference/complexity-metrics.md)
**For Common Errors** → See [reference/troubleshooting.md](reference/troubleshooting.md)

### 6. Verify Improvements

```bash
# Re-run PHPInsights
make phpinsights

# Verify all thresholds pass
✅ Code quality: 100%
✅ Complexity: 93%+ (src), 95%+ (tests)
✅ Architecture: 100%
✅ Style: 100%
```

## Quick Fixes by Issue Type

### Cyclomatic Complexity Too High

**Problem**: Method has too many decision points (if/else/switch/loops)

**First, identify which classes need refactoring**:

```bash
# Find top 10 most complex classes
make analyze-complexity N=10
```

**Solutions**:

1. **Extract methods**: Break complex method into smaller private methods
2. **Strategy pattern**: Replace conditionals with polymorphism
3. **Early returns**: Reduce nesting with guard clauses
4. **Command pattern**: Separate command handling logic

See [refactoring-strategies.md](refactoring-strategies.md) for DDD/CQRS-specific patterns.

### Architecture Violations

**Problem**: Layer dependencies violated (e.g., Domain depending on Infrastructure)

**Solutions**:

1. **Review layer boundaries**: Domain → Application → Infrastructure
2. **Use interfaces**: Define contracts in Domain, implement in Infrastructure
3. **Dependency injection**: Inject dependencies through constructors
4. **Repository pattern**: Keep data access in Infrastructure layer

**Project Architecture**:

```
src/{BoundedContext}/
├── Domain/           # No external dependencies
│   ├── Entity/
│   ├── ValueObject/
│   └── Repository/  # Interfaces only
├── Application/      # Depends on Domain
│   ├── Command/
│   ├── CommandHandler/
│   └── Event/
└── Infrastructure/   # Depends on Domain + Application
    └── Repository/   # Implementations
```

### Style Issues

**Problem**: Code doesn't meet PSR-12 or Symfony coding standards

**Solutions**:

```bash
# Auto-fix most style issues
make phpcsfixer

# Re-run PHPInsights to verify
make phpinsights
```

### Line Length > 100 Characters

**Problem**: Lines exceed configured limit (100 chars)

**Config**:

```php
LineLengthSniff::class => [
    'lineLimit' => 100,
    'ignoreComments' => true,
],
```

**Solutions**:

1. Break long method calls into multiple lines
2. Extract complex expressions into variables
3. Use named parameters (PHP 8+)
4. Refactor long argument lists into DTOs

## Project-Specific Configuration

### Excluded Sniffs

These sniffs are intentionally disabled in `phpinsights.php`:

```php
'remove' => [
    UnusedParameterSniff::class,              // Allow unused params in interfaces
    SuperfluousInterfaceNamingSniff::class,   // Allow "Interface" suffix
    SuperfluousExceptionNamingSniff::class,   // Allow "Exception" suffix
    SpaceAfterNotSniff::class,                // Symfony style preference
    ForbiddenSetterSniff::class,              // Allow setters where needed
    UseSpacingSniff::class,                   // Symfony style preference
],
```

**Do NOT** create issues for these patterns - they're explicitly allowed.

### Excluded Files

Some files are excluded from specific checks:

```php
ForbiddenNormalClasses::class => [
    'exclude' => [
        'src/Shared/Infrastructure/Bus/Command/InMemorySymfonyCommandBus',
        'src/Shared/Infrastructure/Bus/Event/InMemorySymfonyEventBus',
        'src/Core/Customer/Domain/Entity/Customer',
    ],
],
```

These are intentionally not marked `final` - architectural decision.

## Integration with Other Skills

- **quality-standards** skill: Broader quality enforcement including Psalm, Deptrac
- **ci-workflow** skill: PHPInsights runs as part of CI checks
- **testing-workflow** skill: Maintain test coverage while refactoring
- **database-migrations** skill: Ensure entity changes maintain architecture compliance

## Common Patterns in This Codebase

### Command Handler Complexity

Command handlers should have low complexity:

```php
// ✅ GOOD: Low complexity (2-3)
final readonly class CreateCustomerCommandHandler implements CommandHandlerInterface
{
    public function __construct(
        private CustomerRepository $repository,
        private DomainEventPublisher $publisher
    ) {}

    public function __invoke(CreateCustomerCommand $command): void
    {
        $customer = Customer::create(
            $command->id,
            $command->name,
            $command->email
        );

        $this->repository->save($customer);
        $this->publisher->publish(...$customer->pullDomainEvents());
    }
}
```

**If complexity is high**: Business logic likely in wrong layer - move to Domain.

### Domain Entity Complexity

Domain entities can have higher complexity for business rules:

```php
// ✅ Acceptable: Complexity in domain logic
class Customer extends AggregateRoot
{
    public function updateSubscription(SubscriptionPlan $plan): void
    {
        // Complex validation logic is appropriate here
        $this->validateSubscriptionChange($plan);
        $this->applyDiscount($plan);
        $this->record(new SubscriptionChanged($this->id, $plan));
    }
}
```

**If too complex**: Extract to Domain Service or Value Object.

## Success Criteria

After running this skill, verify:

✅ `make phpinsights` passes without errors
✅ Code quality: 100%
✅ Complexity: ≥ 93% (src), ≥ 95% (tests)
✅ Architecture: 100%
✅ Style: 100%
✅ No layer boundary violations (checked by Deptrac)
✅ All tests still pass (`make unit-tests`, `make integration-tests`)
✅ Code remains aligned with hexagonal architecture

## Additional Resources

### Quick References

- **⚡ Quick Start**: [quick-start.md](reference/quick-start.md) - Fast-track workflow for immediate action
- **🔧 Analysis Tools**: [analysis-tools.md](reference/analysis-tools.md) - Complete guide to complexity analysis commands

### Detailed Guides

- **Refactoring Patterns**: [refactoring-strategies.md](refactoring-strategies.md) - Modern PHP patterns with real-world examples
- **Understanding Metrics**: [reference/complexity-metrics.md](reference/complexity-metrics.md) - What each metric means
- **Troubleshooting**: [reference/troubleshooting.md](reference/troubleshooting.md) - Common issues and solutions
- **Monitoring**: [reference/monitoring.md](reference/monitoring.md) - Track improvements over time

### External Resources

- **PHPInsights Documentation**: https://phpinsights.com/
- **Project Architecture**: See CLAUDE.md for hexagonal/DDD/CQRS patterns
