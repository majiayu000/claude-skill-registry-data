---
name: testing
description: Write, review, and audit tests for Flutter projects using Clean Architecture + Riverpod. Use when writing unit tests, widget tests, golden tests, reviewing test quality, checking test coverage, creating mocks/spies, or testing Riverpod providers.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Testing - Write & Review Tests

Write high-quality, maintainable tests following Clean Architecture patterns. Every test should clearly express intent and catch regressions without being brittle.

## When to Use This Skill

- Writing new tests (unit, widget, golden, integration)
- Reviewing test code quality
- Setting up test infrastructure (helpers, mocks, spies)
- Testing Riverpod providers and notifiers
- Auditing test coverage

## Quick Reference

### Test Types

| Type | Purpose | When to Use |
|------|---------|-------------|
| **Unit** | Isolated logic | Repositories, services, utils, providers |
| **Widget** | UI interactions | Screens, navigation |
| **Golden** | Visual regression | Layout, themes |
| **Integration** | Real implementations | Storage, cache, API flows |

### Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| File | `{component}_test.dart` | `auth_repository_impl_test.dart` |
| Test | `test_{subject}_{scenario}_{expected}` | `test_signIn_withValidCredentials_returnsAuthResult` |
| Factory | `any{Type}()` | `anyEmail()`, `anyUserProfile()` |
| SUT | `makeSUT()` | Creates System Under Test |

### Commands

```bash
# Run all tests
flutter test

# Run with coverage
flutter test --coverage

# Run specific type
flutter test test/unit/
flutter test test/widget/

# Audit test coverage
dart run .claude/skills/testing/scripts/check.dart

# Generate missing test files
dart run .claude/skills/testing/scripts/check.dart --generate

# Update golden files
flutter test --update-goldens test/golden/
```

## Workflow

### 1. Create Test File

Mirror source path: `test/unit/features/{feature}/data/repositories/{name}_test.dart`

### 2. Write Tests Using Patterns

See [patterns-guide.md](patterns-guide.md) for:
- **makeSUT()** - Factory for System Under Test
- **Spy Pattern** - Track method calls
- **Arrange-Act-Assert** - Clear structure
- **Disposal Testing** - Verify cleanup
- **Inbox Checklist** - Infrastructure testing

### 3. Verify Coverage

```bash
dart run .claude/skills/testing/scripts/check.dart
```

## Checklist

**Structure:**
- [ ] Uses `makeSUT()` for consistent setup
- [ ] Uses `any*()` factories for test data
- [ ] Clear Arrange-Act-Assert structure

**Coverage:**
- [ ] Tests success and error paths
- [ ] Verifies side effects (storage, API calls)

**Quality:**
- [ ] No hardcoded delays
- [ ] No flaky assertions
- [ ] Disposal tested

## Coverage Expectations

| Component | Minimum |
|-----------|---------|
| Repositories | 90%+ |
| Providers | 85%+ |
| Utils | 80%+ |
| Widgets | 60%+ |

## Guides

| Guide | Use For |
|-------|---------|
| [patterns-guide.md](patterns-guide.md) | Test patterns, helpers, spies |
| [examples.md](examples.md) | Before/after examples |

## Related Skills

- `/a11y` - Accessibility tests (`textContrastGuideline`, etc.)
