---
name: xUnit Test Framework
description: Run and write xUnit tests for C#/.NET projects — FluentAssertions and Moq. The .NET test runner.
when_to_use: Reach for this when the project tests C#/.NET with xUnit (*.csproj referencing xunit, *Tests.cs). Per-language test runner — use jest for JS/TS, pytest for Python, rspec for Ruby, exunit for Elixir. For .NET app code under test use developing-with-dotnet. If unsure which runner the project uses, run test-detector first.
version: 1.0.0
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
paths:
  - "**/*.csproj"
  - "**/*Tests.cs"
  - "**/*Tests.fs"
---

# xUnit Test Framework

## Purpose

Provide xUnit test execution and generation for C#/.NET projects.

## Usage

```bash
dotnet run --project generate-test.csproj -- --source=Calculator.cs --output=CalculatorTests.cs --description="Division by zero"
dotnet test --filter=CalculatorTests
```

## Output Format

JSON with success, passed, failed, total, and failures array.
