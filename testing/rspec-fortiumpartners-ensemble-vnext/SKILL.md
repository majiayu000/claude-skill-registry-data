---
name: RSpec Test Framework
description: Run and write RSpec tests for Ruby projects — let bindings, before hooks, mocking. The Ruby test runner.
when_to_use: Reach for this when the project tests Ruby with RSpec (spec/, .rspec, spec_helper.rb). Per-language test runner — use jest for JS/TS, pytest for Python, exunit for Elixir, xunit for C#/.NET. For Rails app code under test use rails. If unsure which runner the project uses, run test-detector first.
version: 1.0.0
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
paths:
  - ".rspec"
  - "spec/spec_helper.rb"
  - "spec/**/*_spec.rb"
---

# RSpec Test Framework

## Purpose

Provide RSpec test execution and generation for Ruby projects.

## Usage

```bash
ruby generate-test.rb --source=lib/calculator.rb --output=spec/calculator_spec.rb --description="Division by zero"
ruby run-test.rb --file=spec/calculator_spec.rb
```

## Output Format

JSON with success, passed, failed, total, and failures array.
