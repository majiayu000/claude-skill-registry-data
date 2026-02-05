---
name: elixir-quality-gate
description: Run comprehensive Elixir quality checks (format, credo, dialyzer, tests) with proper error handling and reporting. Use when validating code quality, before commits, or preparing for deployment.
allowed-tools: Bash, Read, Grep
---

# Elixir Quality Gate

This skill runs comprehensive quality checks on Elixir/Phoenix projects following best practices.

## When to Use

- Before creating commits
- After implementing new features
- Before merging pull requests
- When preparing for deployment
- During code reviews

## Quality Checks Performed

### 1. Code Formatting
```bash
mix format --check-formatted
```
- Validates all files are properly formatted
- Fails fast if formatting issues found
- Shows which files need formatting

### 2. Compilation
```bash
mix compile --warnings-as-errors
```
- Ensures clean compilation
- Treats warnings as errors
- Catches unused variables, deprecated functions

### 3. Static Analysis (Credo)
```bash
mix credo --strict
```
- Runs strict code quality checks
- Checks for consistency, design issues, readability
- Reports refactoring opportunities

### 4. Type Checking (Dialyzer)
```bash
mix dialyzer
```
- Performs static type analysis
- Builds PLT (Persistent Lookup Table) if needed
- First run takes 1-2 minutes, subsequent runs are fast
- Catches type errors and inconsistencies

### 5. Test Suite
```bash
mix test
```
- Runs full test suite
- Reports coverage if configured
- Shows failures and pending tests

## Usage Pattern

### Full Quality Gate (Recommended)
Run all checks in sequence:
```bash
mix format --check-formatted && \
mix compile --warnings-as-errors && \
mix credo --strict && \
mix dialyzer && \
mix test
```

### Quick Check (Pre-commit)
If project has a precommit alias:
```bash
mix precommit
```

### Individual Checks
Run specific checks when iterating:
```bash
# Just format
mix format

# Just tests
mix test

# Specific test file
mix test test/my_app/accounts_test.exs

# Just credo
mix credo --strict
```

## Error Handling

**Format Failures:**
- Read the output to see which files need formatting
- Run `mix format` to fix automatically
- Re-run checks

**Compilation Warnings:**
- Read warnings carefully
- Common issues: unused variables (prefix with _), deprecated functions
- Fix warnings before proceeding

**Credo Issues:**
- Review suggested improvements
- Refactoring opportunities are optional but recommended
- Design and consistency issues should be addressed

**Dialyzer Errors:**
- First run builds PLT (takes time, this is normal)
- Type errors indicate potential runtime bugs
- Use @spec annotations to guide Dialyzer

**Test Failures:**
- Read failure messages carefully
- Run failing test in isolation: `mix test test/path/to/test.exs:LINE`
- Fix failures before proceeding

## Best Practices

1. **Run locally before pushing** - Catch issues early
2. **Fix formatting first** - It's the fastest fix
3. **Don't ignore warnings** - They often indicate real problems
4. **Keep PLT cached** - Add `priv/plts/` to .gitignore
5. **Run full suite before PR** - Don't rely only on CI

## Environment Variables

```bash
# Run in test environment
MIX_ENV=test mix dialyzer

# Skip dialyzer if building PLT takes too long locally
mix format && mix compile --warnings-as-errors && mix credo --strict && mix test
```

## Exit Codes

- 0: All checks passed
- Non-zero: At least one check failed (stops at first failure with &&)

## Integration with Git Hooks

If using BMAD git hooks, these checks run automatically on:
- pre-commit: Full quality gate
- pre-push: Quick validation

## Troubleshooting

**PLT build fails:**
```bash
# Clean and rebuild
rm -rf _build priv/plts
mix deps.get
mix dialyzer --plt
```

**Tests fail in CI but pass locally:**
- Check MIX_ENV (should be test)
- Verify database is created: `MIX_ENV=test mix ecto.create`
- Check for async test conflicts

**Credo reports too many issues:**
- Start with formatting and compilation
- Fix high-priority issues first
- Consider configuring .credo.exs to match team preferences
