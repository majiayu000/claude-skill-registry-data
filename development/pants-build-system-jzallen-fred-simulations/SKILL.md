---
name: "Pants Build System"
description: "Expert guidance on using Pants build system for Python projects, focusing on optimal caching, test execution, and target-based workflows."
version: "2.0.0"
---

# Pants Build System

You are a Pants build system expert helping developers maximize build performance and leverage Pants' advanced caching capabilities through proper target-based workflows.

## What is Pants?

Pants is a modern build system providing:
- **Fine-grained caching** - File-level dependency tracking for maximum cache hits
- **Parallel execution** - Concurrent builds and tests across all CPU cores
- **Dependency inference** - Automatic dependency detection without manual BUILD maintenance
- **Hermetic builds** - Reproducible results across machines

## The #1 Critical Rule

### ALWAYS Use Target Addresses, NEVER File Paths

This is the most important concept in Pants. Understanding this prevents 80% of common mistakes.

**Target addresses and file paths create SEPARATE caches**:

```bash
# ✅ CORRECT: Uses target cache, maximizes cache hits
pants test epistemix_platform:src-tests

# ❌ WRONG: Creates separate cache, loses memoization benefits
pants test epistemix_platform/tests/test_something.py
```

**Why This Matters:**

When you run `pants test epistemix_platform:src-tests`:
1. First run executes all tests and caches results per file
2. Subsequent runs only re-run tests affected by changed files
3. Unchanged tests return cached results instantly

**File-path invocations break this** because they create different cache keys, losing all accumulated cache benefits.

**When file paths are acceptable:** Only for one-off debugging sessions. Always return to target-based execution for normal development.

> **Deep dive**: [caching-deep-dive.md](reference/caching-deep-dive.md)

## Essential Commands

### Running Tests
```bash
pants test ::                           # All tests (top-level cache)
pants test epistemix_platform::         # Component tests
pants test epistemix_platform:src-tests # Specific target (PREFERRED)

# Pass arguments to pytest with --
pants test epistemix_platform:src-tests -- -vv  # Verbose
pants test epistemix_platform:src-tests -- -k test_user  # Pattern
pants test epistemix_platform:src-tests -- -x  # Stop on first failure
```

### Code Quality
```bash
pants fmt ::              # Format all code
pants lint ::             # Lint all code
pants fmt lint ::         # Both together
pants fmt --changed-since=HEAD  # Only changed files
```

### Building
```bash
pants package epistemix_platform:epistemix-cli  # Build PEX binary
```

### Dependency Management
```bash
pants generate-lockfiles  # Update all lockfiles
pants export --resolve=epistemix_platform_env  # Export to virtualenv
```

> **Complete command reference**: [command-reference.md](reference/command-reference.md)

## Target Specifications

### The :: Wildcard
```bash
pants test ::               # All targets in repository
pants test epistemix_platform::  # All targets in directory + subdirs
```

### Specific Targets
```bash
pants test epistemix_platform:src-tests  # Named target in BUILD file
```

### Listing Targets
```bash
pants list epistemix_platform::  # List all targets
pants list epistemix_platform/tests/test_models.py  # Find owners
```

> **Complete target guide**: [target-specifications.md](reference/target-specifications.md)

## Project-Specific Targets

Key test targets in this repository:
```bash
pants test epistemix_platform:src-tests        # Platform tests
pants test epistemix_platform:infrastructure-tests  # Infrastructure tests
pants test simulation_runner:src-tests         # Simulation runner tests
pants test ::                                  # All tests (recommended)
```

## Available Resources

### Core Documentation

- **[caching-deep-dive.md](reference/caching-deep-dive.md)** - How Pants caching works
  - Target vs file-path cache keys explained
  - Cache invalidation and optimization
  - Local vs remote caching
  - Performance tuning
  - Read when: Optimizing build performance or troubleshooting cache

- **[command-reference.md](reference/command-reference.md)** - Complete command catalog
  - All goals with options (test, fmt, lint, package, etc.)
  - Passing arguments to underlying tools
  - Inspection commands (list, peek, dependencies)
  - Read when: Need full syntax for a specific command

- **[target-specifications.md](reference/target-specifications.md)** - BUILD files and targets
  - Target address format
  - BUILD file structure
  - python_tests target anatomy
  - Multiple test target organization
  - Read when: Setting up BUILD files or organizing targets

### Advanced Topics

- **[advanced-topics.md](reference/advanced-topics.md)** - Configuration and optimization
  - Test batching for expensive fixtures
  - Multiple resolves (epistemix_platform_env, infrastructure_env)
  - CI/CD patterns with --changed-since
  - Performance tuning
  - Read when: Configuring batching, using multiple resolves, or CI setup

- **[tdd-integration.md](reference/tdd-integration.md)** - TDD workflow with Pants
  - Red-Green-Refactor cycle optimization
  - Effective pytest arguments
  - Watch mode alternatives
  - Fast feedback strategies
  - Read when: Practicing TDD or setting up rapid iteration

## Golden Rules

1. **ALWAYS use target addresses** (`epistemix_platform:src-tests`), NEVER file paths
2. **Run from top-down** (`pants test ::` or `pants test component::`)
3. **Trust Pants' caching** - it only re-runs what's affected
4. **Use :: wildcard** for directory-based execution
5. **Separate Pants args from pytest args** with `--`
6. **Leverage --changed-since** in CI pipelines
7. **Keep cache warm** - don't clean unnecessarily
8. **Use consistent targets** throughout TDD cycles

## Quick Workflow Examples

### TDD Cycle
```bash
# Red: Write failing test, run to see it fail
pants test epistemix_platform:src-tests -- -k test_new_feature

# Green: Implement, run same command
pants test epistemix_platform:src-tests -- -k test_new_feature

# Refactor: Run full target to ensure nothing breaks
pants test epistemix_platform:src-tests
```

### Pre-Push Verification
```bash
# Format, lint, and test everything
pants fmt lint test ::
```

### Rapid Iteration
```bash
# Edit code, run tests - only affected tests re-run
vim epistemix_platform/src/epistemix_platform/models/user.py
pants test epistemix_platform:src-tests  # Fast!
```

## Common Mistakes to Avoid

❌ **Using file paths habitually**
```bash
pants test epistemix_platform/tests/test_models.py  # DON'T
```

❌ **Running individual files during TDD**
```bash
pants test file1.py  # Creates fragmented cache
pants test file2.py  # Separate cache key
```

❌ **Not leveraging :: syntax**
```bash
pants test epistemix_platform/tests pants test simulation_runner/tests  # DON'T
pants test ::  # DO - Let Pants handle it
```

❌ **Fighting Pants' parallelization**
```bash
pants test component1:: & pants test component2:: &  # DON'T
pants test ::  # DO - Pants parallelizes automatically
```

## Key Concepts

- **Targets** - Addressable units of metadata in BUILD files (e.g., `python_tests`)
- **BUILD files** - Define targets with dependencies and configuration
- **Goal** - A Pants command like `test`, `fmt`, `lint`
- **Resolve** - Set of Python dependencies (epistemix_platform_env, infrastructure_env, etc.)
- **Dependency inference** - Pants automatically detects imports and creates dependencies

## Performance Tips

1. **Cache warmth** - After major changes, run `pants test ::` once to warm cache
2. **Top-down execution** - Start with `::`, let Pants optimize
3. **Use --changed-since** - In CI, only test affected code
4. **Trust the cache** - Don't use `pants clean-all` unless troubleshooting

## Remember

Pants' power comes from file-level dependency tracking and intelligent caching. The key to unlocking this power is **consistently using target addresses instead of file paths**. This single practice transforms Pants from a build tool into a performance multiplier.

Every time you're tempted to run `pants test path/to/file.py`, remember: you're creating a new cache key and losing all the optimization benefits Pants provides.

---

**For comprehensive guidance, explore the reference/ directory based on your current need.**
