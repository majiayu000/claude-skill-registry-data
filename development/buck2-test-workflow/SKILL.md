---
name: buck2-test-workflow
description: Comprehensive testing workflow that should be used proactively after ANY code changes. Covers immediate testing, recursive package validation with `...`, target determination for affected packages, and reverse dependency testing. Use this skill after modifying BUILD files, changing code, fixing tests, or before committing to ensure nothing breaks downstream. (project)
---

# Buck2 Test Workflow

## Overview

Ensure comprehensive test coverage and prevent downstream breakage by following a systematic testing workflow after any code changes. This skill provides step-by-step procedures for validating changes at multiple levels: immediate targets, entire packages recursively, affected targets via target determination, and reverse dependencies.

## Critical Testing Principle

**ALWAYS test comprehensively after making changes.** A passing single test is not sufficient. Changes can break:
- Other tests in the same package
- Dependent packages downstream
- Integration points not immediately obvious

Follow the complete workflow below to catch issues before they reach production or break other developers' work.

## When to Use This Skill

Use this skill proactively and automatically after:
- Creating or modifying BUILD files
- Creating or modifying PACKAGE files
- Changing source code (Rust, TypeScript, C++, etc.)
- Fixing failing tests
- Refactoring code
- Adding new dependencies
- Before creating commits
- Before creating pull requests

**Use pattern**: After completing any change → immediately invoke this testing workflow.

## Complete Testing Workflow

Follow these steps in order. Do NOT skip steps.

### Step 1: Test the Immediate Target

First, verify the specific target being modified works correctly.

```bash
buck2 test <target>
```

**Examples:**
```bash
# Test a specific binary
buck2 test //src/buildflow:buildflow

# Test a specific library
buck2 test //src/tools/brainiac:brainiac

# Test a specific test target
buck2 test //src/lib/mylib:test-parser
```

**Success criteria**: All tests pass with no failures.

**If tests fail**: Fix the issues before proceeding. Do not continue to the next step with failing tests.

### Step 2: Test Package Recursively

After the immediate target passes, test ALL targets in the package recursively using the `...` pattern. This catches:
- Related tests in subdirectories
- Integration tests
- Lint tests
- Other targets in the same package

```bash
buck2 test <package-path>/...
```

**Examples:**
```bash
# Test all targets in buildflow package
buck2 test //src/buildflow/...

# Test all targets in brainiac package
buck2 test //src/tools/brainiac/...

# Test entire depot (use cautiously - very slow)
buck2 test //...
```

**Why this matters**: Individual targets may pass, but package-level tests or sibling targets may fail. The `...` pattern ensures complete package validation.

**Success criteria**: All tests in the package pass.

**If tests fail**: Fix the issues. The recursive test found problems the immediate test missed.

### Step 3: Determine Affected Targets

Use target determination to find which other packages are affected by the changes. This identifies:
- Direct dependents (rdeps)
- Transitive dependents
- Packages that need rebuilding due to API changes

**Using the MCP tool (preferred)**:

```bash
# Use the target determination MCP tool
mcp__brainiac__target_determination(
  from: "trunk()",
  to: "@",
  universe: ["root//...", "third-party//..."]
)
```

**Using buck2-target-determination skill (alternative)**:

Invoke the `buck2-target-determination` skill to run target determination analysis. This will identify affected targets based on the current changes.

**Manual approach (if needed)**:

```bash
# Find reverse dependencies manually
buck2 uquery "rdeps(//..., <your-target>)"

# Example: find everything that depends on brainiac
buck2 uquery "rdeps(//..., //src/tools/brainiac:brainiac)"
```

**Output**: List of affected target patterns.

### Step 4: Build and Test Affected Targets

Build and test all targets identified by target determination to ensure changes don't break downstream consumers.

**Build affected targets first**:

```bash
buck2 build <affected-targets...>
```

**Example:**
```bash
# Build multiple affected targets
buck2 build //src/tools/omnifix:omnifix //src/lib/parser:parser //tests/integration:all
```

**Then test affected targets**:

```bash
buck2 test <affected-targets...>
```

**Example:**
```bash
# Test all affected targets
buck2 test //src/tools/omnifix:omnifix //src/lib/parser:parser //tests/integration:all
```

**Why this matters**: Changes to libraries, APIs, or shared code can break packages that depend on them. Testing only the changed package misses these downstream failures.

**Success criteria**: All affected targets build and test successfully.

**If tests fail**: The changes broke a downstream consumer. Either:
- Fix the downstream package to accommodate the changes
- Revise the changes to maintain backward compatibility
- Document breaking changes if intentional

### Step 5: Verify Reverse Dependencies (Advanced)

For critical changes to widely-used libraries, explicitly test reverse dependencies.

**Find direct reverse dependencies**:

```bash
buck2 uquery "rdeps(//..., <target>, 1)"
```

**Find transitive reverse dependencies**:

```bash
buck2 uquery "rdeps(//..., <target>)"
```

**Test reverse dependencies**:

```bash
# Extract targets from uquery output and test them
buck2 test <rdep-targets...>
```

**When to use**:
- Modifying core libraries used across the monorepo
- Changing public APIs
- Refactoring shared utilities
- Making breaking changes

**Skip when**:
- Changes are isolated to a single package
- Target determination already covered all affected targets
- Working on leaf nodes with no dependents

## Quick Reference

**Minimal workflow** (use after every change):
```bash
buck2 test <target>              # Step 1: immediate
buck2 test <package>/...         # Step 2: recursive
```

**Complete workflow** (use before commits/PRs):
```bash
buck2 test <target>              # Step 1: immediate
buck2 test <package>/...         # Step 2: recursive
# Run target determination        # Step 3: affected
buck2 build <affected>           # Step 4: build affected
buck2 test <affected>            # Step 4: test affected
```

**Advanced workflow** (use for library changes):
```bash
buck2 test <target>              # Step 1: immediate
buck2 test <package>/...         # Step 2: recursive
# Run target determination        # Step 3: affected
buck2 build <affected>           # Step 4: build affected
buck2 test <affected>            # Step 4: test affected
buck2 uquery "rdeps(//..., <target>)"  # Step 5: find rdeps
buck2 test <rdeps>               # Step 5: test rdeps
```

## Common Testing Patterns

### Pattern: New BUILD File

After creating a BUILD file:

1. Test the primary target: `buck2 test //path/to:target`
2. Test package recursively: `buck2 test //path/to/...`
3. Verify no syntax errors in BUILD file: `buck2 targets //path/to/...`

### Pattern: Modified Source Code

After changing source code:

1. Test immediate target: `buck2 test //path/to:target`
2. Test package: `buck2 test //path/to/...`
3. Run target determination to find affected targets
4. Build and test affected targets

### Pattern: Fixed Failing Tests

After fixing tests:

1. Verify fix: `buck2 test <fixed-target>`
2. Test package: `buck2 test <package>/...` (ensure fix didn't break other tests)
3. Run target determination (fixes might affect dependents)
4. Test affected targets

### Pattern: Dependency Changes

After adding/removing dependencies:

1. Test immediate target: `buck2 test <target>`
2. Test package: `buck2 test <package>/...`
3. Find rdeps: `buck2 uquery "rdeps(//..., <target>)"`
4. Test rdeps to ensure dependency changes don't break consumers

### Pattern: Refactoring

After refactoring:

1. Test affected package: `buck2 test <package>/...`
2. Run target determination
3. Build affected targets: `buck2 build <affected>`
4. Test affected targets: `buck2 test <affected>`
5. Explicitly test rdeps for API changes

## Troubleshooting

### Issue: Tests Pass Individually but Fail in Package

**Symptom**: `buck2 test <target>` passes, but `buck2 test <package>/...` fails.

**Cause**:
- Interference between tests
- Missing test isolation
- Shared state between test targets
- Integration tests catching issues unit tests miss

**Solution**: Investigate which specific test is failing in the package run and why it differs from individual execution.

### Issue: Target Determination Shows No Affected Targets

**Symptom**: Target determination returns empty or minimal results despite significant changes.

**Cause**:
- Changes not committed (target determination compares commits)
- Universe parameter too narrow
- Comparing wrong revisions

**Solution**:
- Ensure changes are committed: `jj commit`
- Expand universe: `["root//...", "third-party//..."]`
- Verify revision parameters: `from: "trunk()"`, `to: "@"`

### Issue: Affected Targets Fail

**Symptom**: Downstream packages fail after changes.

**Cause**: Breaking changes to APIs, behavior, or contracts.

**Solution**:
- **Option 1**: Fix downstream packages to accommodate changes
- **Option 2**: Revise changes to maintain compatibility
- **Option 3**: Accept breaking change and update all consumers together

### Issue: Tests Too Slow

**Symptom**: `buck2 test //...` takes too long.

**Cause**: Testing entire monorepo is expensive.

**Solution**:
- Use target determination to test only affected targets
- Test package recursively instead of entire depot
- Run full test suite in CI, not locally
- Use `buck2 build` first to fail fast on compilation errors

## Best Practices

### Always Use Recursive Testing

```bash
# ❌ Insufficient - only tests one target
buck2 test //src/buildflow:buildflow

# ✅ Comprehensive - tests entire package
buck2 test //src/buildflow/...
```

### Build Before Testing

Building first catches compilation errors faster than waiting for test execution:

```bash
# Fast failure on build errors
buck2 build <targets>
buck2 test <targets>
```

### Use Target Determination for Large Changes

Don't guess which packages might be affected:

```bash
# ❌ Guessing
buck2 test //src/tools/... //src/lib/...

# ✅ Systematic
# Run target determination
buck2 test <affected-targets>
```

### Test at Increasing Scope

Start narrow, expand scope:

1. Single target (fast, specific)
2. Package recursive (medium, thorough)
3. Affected targets (slow, complete)
4. Reverse dependencies (slowest, exhaustive)

### Commit Only When Green

Never commit with failing tests. The workflow is:

1. Make changes
2. Run testing workflow
3. Fix issues
4. Re-run testing workflow
5. Commit when all tests pass

## Integration with Other Workflows

### Before Committing

```bash
buck2 test <package>/...
# Run target determination
buck2 test <affected>
jj commit -m "..."
```

### Before Creating PRs

```bash
buck2 test <package>/...
# Run target determination
buck2 build <affected>
buck2 test <affected>
# Create PR
```

### After Merging

CI should run comprehensive tests:
- Full monorepo test: `buck2 test //...`
- Target determination against main branch
- Performance benchmarks
- Integration tests

## Related Skills

- `buck2-target-determination` - Determine affected targets from changes
- `buck2-build-troubleshoot` - Debug build failures
- `buck2-query-helper` - Query dependency graphs and targets

## Summary

**Golden rule**: After any change, always:
1. ✅ Test immediate target
2. ✅ Test package recursively with `...`
3. ✅ Determine affected targets
4. ✅ Build and test affected targets
5. ✅ (Optional) Test reverse dependencies for critical changes

This workflow prevents downstream breakage and ensures high code quality across the monorepo.
