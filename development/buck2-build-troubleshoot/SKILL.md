---
name: buck2-build-troubleshoot
description: Debugs Buck2 build failures systematically by analyzing error logs, checking common issues (cache, visibility, cycles), and suggesting fixes. Use when builds fail, tests won't run, or Buck2 reports errors.
---

# Buck2 Build Troubleshoot

## Overview

This skill provides systematic debugging for Buck2 build failures. It analyzes error logs, identifies common issues, and suggests concrete fixes. Instead of manually parsing verbose build output, use the build doctor script to diagnose problems quickly.

**Use this skill when:**
- Buck2 build fails with cryptic errors
- Targets won't compile or link
- Tests fail to run
- Visibility errors prevent building
- Dependency cycles are suspected
- Cache issues cause inconsistent builds
- Remote execution fails

**This skill provides:**
- `scripts/build_doctor.py` - Automated build diagnostics
- `references/common_errors.md` - Error patterns and solutions
- Systematic debugging workflow
- Quick fixes for common issues

## Quick Start

When a build fails:

```bash
# Run the build doctor
python3 scripts/build_doctor.py

# Or analyze specific target
python3 scripts/build_doctor.py //src/tools:mytool

# Verbose analysis
python3 scripts/build_doctor.py --verbose //src/tools:mytool
```

The script will:
1. Check what failed recently
2. Analyze error messages
3. Check common issues (cache, visibility, cycles)
4. Suggest specific fixes

## Common Build Failures

### Compilation Errors

**Rust compilation failure:**
```
Error: rustc failed with exit code 1
```

**Diagnosis:**
```bash
# See full error
python3 scripts/build_doctor.py --show-logs //target

# Check source files
buck2 query "//target" --output-attribute srcs

# Verify dependencies
buck2 query "deps('//target', 1)"
```

**Common fixes:**
- Fix syntax errors in source code
- Add missing dependencies to BUILD file
- Check Rust edition compatibility
- Verify feature flags

### Dependency Errors

**Missing dependency:**
```
Error: unresolved import `foo::bar`
```

**Fix:**
```python
# Add to BUILD file deps:
deps = [
    "//path/to:foo",
    "third-party//crate:crate",
]
```

**Circular dependency:**
```
Error: cycle detected in dependency graph
```

**Diagnosis:**
```bash
# Find the cycle
python3 scripts/build_doctor.py --check-cycles //src/...

# Investigate specific path
buck2 query "allpaths('//target/a', '//target/b')"
buck2 query "allpaths('//target/b', '//target/a')"
```

**Fix:** Break the cycle by:
- Extracting shared code to new library
- Removing unnecessary dependency
- Using dependency injection instead of direct import

### Visibility Errors

**Cannot access target:**
```
Error: //src/app:app cannot depend on //src/lib:internal (not visible)
```

**Diagnosis:**
```bash
# Check visibility settings
buck2 query "//src/lib:internal" --output-attribute visibility

# See who can access it
python3 scripts/build_doctor.py --check-visibility //src/lib:internal
```

**Fix:**
```python
# In BUILD file, update visibility:
depot.rust_library(
    name = "internal",
    visibility = [
        "//src/app/...",  # Allow src/app access
        # or
        "PUBLIC",  # Allow everyone
    ],
)
```

### Linking Errors

**Undefined reference:**
```
Error: undefined reference to `symbol`
```

**Common causes:**
- Missing library dependency
- Wrong link order
- ABI mismatch between libraries

**Fix:**
```bash
# Check all dependencies are present
buck2 query "deps('//target', 1)" --output-attribute deps

# For C++, check link order in BUILD
```

### Test Failures

**Tests won't run:**
```
Error: No tests found
```

**Diagnosis:**
```bash
# Verify test target exists
buck2 targets //path:test

# Check test is properly defined
buck2 query "//path:test" --output-attribute buck.type
```

**Fix:**
```python
# Ensure BUILD has test target:
depot.rust_test(
    name = "test",
    srcs = glob(["src/**/*.rs"]),
)
```

## Systematic Debugging Workflow

### Step 1: Identify What Failed

```bash
# Recent failures
buck2 log what-failed

# Or use build doctor
python3 scripts/build_doctor.py
```

### Step 2: Read the Error

```bash
# Full error output
buck2 log last

# Specific target
buck2 build //target -v 2  # Verbose mode
```

### Step 3: Check Common Issues

```bash
# Run automated checks
python3 scripts/build_doctor.py --all-checks //target
```

This checks:
- Cache corruption
- Visibility issues
- Circular dependencies
- Missing dependencies
- Common configuration errors

### Step 4: Verify Target Configuration

```bash
# Inspect BUILD file
buck2 query "//target" --json | jq

# Check dependencies
buck2 query "deps('//target', 1)"

# Verify source files exist
buck2 query "//target" --output-attribute srcs
```

### Step 5: Test in Isolation

```bash
# Build single target
buck2 build //target

# Build with fresh cache
buck2 clean && buck2 build //target

# Skip cache
buck2 build //target --no-remote-cache
```

## Build Doctor Script Usage

### Basic Diagnostics

```bash
# Analyze last failure
python3 scripts/build_doctor.py

# Specific target
python3 scripts/build_doctor.py //src/tools:mytool

# Multiple targets
python3 scripts/build_doctor.py //src/tools:tool1 //src/lib:lib2
```

### Check Options

```bash
# Check cache issues
python3 scripts/build_doctor.py --check-cache

# Check visibility
python3 scripts/build_doctor.py --check-visibility //target

# Check for cycles
python3 scripts/build_doctor.py --check-cycles //src/...

# Run all checks
python3 scripts/build_doctor.py --all-checks //target
```

### Output Options

```bash
# Verbose output
python3 scripts/build_doctor.py --verbose //target

# Show build logs
python3 scripts/build_doctor.py --show-logs //target

# JSON output for scripting
python3 scripts/build_doctor.py --json //target
```

## Common Error Patterns

### Pattern: "No such target"

**Error:**
```
Error: No targets found matching //src/tools:missing
```

**Causes:**
- Typo in target name
- Target not defined in BUILD
- Wrong package path

**Fix:**
```bash
# List available targets
buck2 targets //src/tools:

# Check BUILD file exists
ls -la src/tools/BUILD

# Search for target
buck2 targets //... | grep missing
```

### Pattern: "Glob matched no files"

**Error:**
```
Warning: glob(["src/**/*.rs"]) matched no files
```

**Causes:**
- Wrong glob pattern
- Files in wrong location
- Missing source directory

**Fix:**
```bash
# Check directory structure
ls -la src/

# Verify glob pattern
# For Rust binary: src/main.rs
# For Rust library: src/lib.rs
```

### Pattern: "Cannot find module"

**Error (Rust):**
```
Error: cannot find module `foo` in crate root
```

**Fix:**
1. Add module declaration: `mod foo;` in lib.rs/main.rs
2. Or add file to same directory
3. Or add as dependency in BUILD

### Pattern: "Feature not enabled"

**Error:**
```
Error: feature `foo` is required
```

**Fix:**
```python
# Add to BUILD file:
deps = [
    "third-party//crate:crate[foo]",  # Enable feature
]
```

### Pattern: "Output already used"

**Error:**
```
Error: output directory already in use
```

**Causes:**
- Multiple builds running
- Stale lock files
- Buck daemon issues

**Fix:**
```bash
# Kill buck daemon
buck2 kill

# Clean and rebuild
buck2 clean
buck2 build //target
```

## Advanced Troubleshooting

### Cache Issues

**Symptoms:**
- Inconsistent builds
- Changes not reflected
- Stale outputs

**Diagnosis:**
```bash
# Disable cache and test
buck2 build --no-remote-cache //target

# Check cache configuration
buck2 audit config cache
```

**Fix:**
```bash
# Clear local cache
buck2 clean

# For persistent issues, check .buckconfig
cat .buckconfig | grep -A5 cache
```

### Remote Execution Issues

**Symptoms:**
- Builds fail in CI but work locally
- Platform-specific errors
- Missing dependencies in remote environment

**Diagnosis:**
```bash
# Build locally only
buck2 build --no-remote-execution //target

# Check platform configuration
buck2 audit config re
```

**Fix:**
- Verify all dependencies are in BUILD
- Check platform compatibility
- Ensure no local-only paths

### Incremental Build Issues

**Symptoms:**
- Buck rebuilds everything
- No caching benefits
- Slow builds

**Diagnosis:**
```bash
# Check what changed
buck2 explain //target

# Verify target determinism
buck2 build //target
buck2 build //target  # Should be cached
```

**Fix:**
- Ensure reproducible builds
- Avoid generated source in working copy
- Check for timestamp dependencies

## Integration with Other Tools

### With jj Version Control

```bash
# Find what changed
jj diff --stat | cut -f2 | while read file; do
  buck2 query "owner('$file')"
done | while read target; do
  python3 scripts/build_doctor.py $target
done
```

### With CI/CD

```bash
# In CI pipeline
if ! buck2 build @targets; then
  python3 scripts/build_doctor.py --json > diagnosis.json
  cat diagnosis.json
  exit 1
fi
```

### With Target Determination

```bash
# Diagnose failures in changed targets
TARGETS=$(buck2 run root//buck/tools/quicktd -- '@-' '@' //src/...)
buck2 build @$TARGETS || {
  python3 scripts/build_doctor.py --show-logs
}
```

## Quick Reference

### Must-Know Commands

```bash
# What failed recently
buck2 log what-failed

# Show last build log
buck2 log last

# Build with verbose output
buck2 build //target -v 2

# Clean everything
buck2 clean

# Kill buck daemon
buck2 kill

# Explain why rebuilding
buck2 explain //target
```

### Common Quick Fixes

```bash
# 1. Clean build
buck2 clean && buck2 build //target

# 2. Kill daemon and retry
buck2 kill && buck2 build //target

# 3. Skip cache
buck2 build --no-remote-cache //target

# 4. Verbose output
buck2 build //target -v 2 2>&1 | tee build.log

# 5. Ignore broken targets during testing
buck2 test //... --keep-going
```

## Troubleshooting Checklist

When builds fail, check:

- [ ] Error message clearly read
- [ ] Target exists (`buck2 targets //path:`)
- [ ] BUILD file syntax valid
- [ ] Source files exist and in right location
- [ ] Dependencies declared in BUILD
- [ ] Visibility allows access
- [ ] No circular dependencies
- [ ] Cache not corrupted (try `buck2 clean`)
- [ ] Buck daemon healthy (try `buck2 kill`)
- [ ] Recent changes didn't break build

## Tips and Best Practices

1. **Read the full error** - Often the actual error is near the top, not bottom
2. **Build with -v 2** - Verbose mode shows what's actually running
3. **Test incrementally** - Fix one error at a time
4. **Use clean builds** - When in doubt, `buck2 clean`
5. **Check recent changes** - Use `jj log` to see what changed
6. **Isolate the problem** - Build specific targets, not everything
7. **Use build doctor** - Automated checks save time
8. **Keep BUILD files simple** - Complex BUILD files are hard to debug

## Getting Help

If stuck after trying these steps:

1. Run build doctor with verbose output
2. Collect full error logs: `buck2 build //target -v 2 2>&1 > error.log`
3. Check target configuration: `buck2 query //target --json`
4. Search for similar errors in documentation
5. Ask for help with specific error message and context
