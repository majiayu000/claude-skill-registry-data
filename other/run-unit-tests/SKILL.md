---
name: "run-unit-tests"
description: "Use when a developer wants to run unit tests for the eShop solution. Trigger phrases: run unit tests, run tests, test, dotnet test, unit tests, failing tests, test results."
argument-hint: "Optionally specify a project name or leave blank to run all unit tests."
user-invocable: true
---

## Instructions

Read the full unit test guide at `.github/agents/run-unit-tests.agent.md` and follow all instructions defined there.

The `.github/agents/run-unit-tests.agent.md` file is the single source of truth for running unit tests and is shared with GitHub Copilot. Do not duplicate its content here.

## Summary

Runs the four unit test projects that require no live infrastructure:

- `Basket.UnitTests`
- `Ordering.UnitTests`
- `PaymentProcessor.UnitTests`
- `Security.Tooling.UnitTests`

Excludes `ClientApp.UnitTests` (requires `maui-tizen` workload) and functional test projects (require running containers).

## User Input

```text
$ARGUMENTS
```

If a project name is provided, run only that project. If empty, run all four unit test projects.
