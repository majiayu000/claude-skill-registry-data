---
name: testing-wpf
description: Create and maintain WPF UI tests and ViewModel tests for the .NET 8 widget host app. Use when setting up UI automation, testing MVVM logic, or building a test harness for widgets and the shell.
---

# Testing Wpf

## Overview

Cover UI behavior and ViewModel logic without coupling tests to WPF internals.

## Core areas

- ViewModel unit tests
- UI automation tests
- Test harness for widget windows

## Definition of done (DoD)

- ViewModels tested via WidgetTestHarness with NoOp service implementations
- Commands tested for execute and can-execute behavior
- State changes tested through observable property assertions
- No tests depend on actual WPF runtime (prefer ViewModel tests)
- Test harness updated when new services are added

## Workflow

1. Write ViewModel tests for commands, state, and validation.
2. Use UI automation sparingly for critical flows.
3. Keep UI tests stable by controlling test data and timings.
4. Build a test harness that can host widgets and shell views.

## Guidance

- Prefer ViewModel tests over UI automation where possible.
- Avoid fragile selector strategies in UI tests.
- Keep test runs isolated from user desktop state.

## References

- `references/ui-testing.md` for UI automation strategy.
- `references/viewmodel-tests.md` for MVVM test patterns.
- `references/test-harness.md` for widget test host setup.
