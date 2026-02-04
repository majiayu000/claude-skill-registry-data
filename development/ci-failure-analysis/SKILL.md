---
name: ci-failure-analysis
description: This skill should be used when analyzing failed GitHub Actions CI/CD runs for Breenix kernel development. Use for diagnosing test failures, parsing QEMU logs, identifying kernel panics or faults, understanding timeout issues, and determining root causes of CI failures.
---

# CI Failure Analysis for Breenix

Systematically analyze and diagnose CI/CD test failures in Breenix kernel development.

## Purpose

This skill provides tools and workflows for analyzing failed CI runs, understanding kernel crashes, identifying environment issues, and determining root causes. It focuses on the unique challenges of kernel development CI: QEMU logs, kernel panics, double faults, page faults, and timeout analysis.

## When to Use This Skill

Use this skill when:

- **CI run fails**: GitHub Actions workflow fails and you need to understand why
- **Test timeout**: Test exceeds time limit and you need to determine if it's a hang or just slow
- **Kernel panic/fault**: Double fault, page fault, or other kernel crash in CI
- **Missing output**: Expected kernel log signals don't appear
- **Environment issues**: Build or dependency problems in CI that don't occur locally
- **Regression analysis**: New PR breaks previously passing tests

## Quick Start

When a CI run fails:

1. **Download artifacts**: Go to failed GitHub Actions run, download log artifacts
2. **Run analyzer**: `ci-failure-analysis/scripts/analyze_ci_failure.py target/xtask_*_output.txt`
3. **Review findings**: Analyzer reports known patterns with diagnosis and fixes
4. **Check context**: Use `--context` flag to see surrounding log lines
5. **Apply fix**: Follow suggested remediation steps

## Failure Analysis Script

The skill provides `analyze_ci_failure.py` to automatically detect common failures:

### Basic Usage

```bash
# Analyze a CI log file
ci-failure-analysis/scripts/analyze_ci_failure.py target/xtask_ring3_smoke_output.txt

# Show context around failures
ci-failure-analysis/scripts/analyze_ci_failure.py --context target/xtask_ring3_smoke_output.txt

# Analyze multiple logs
ci-failure-analysis/scripts/analyze_ci_failure.py target/*.txt logs/breenix_*.log
```

### What It Detects

The analyzer recognizes these failure patterns:

1. **Double Fault** - Stack corruption, unmapped exception handlers
2. **Page Fault** - Accessing unmapped or incorrectly mapped memory
3. **Test Timeout** - Exceeding time limits
4. **QEMU Not Found** - Missing system dependencies
5. **Rust Target Missing** - Wrong toolchain configuration
6. **rust-src Missing** - Missing required Rust component
7. **Userspace Binary Missing** - Forgetting to build userspace tests
8. **Compilation Error** - Build failures
9. **Signal Not Found** - Expected output missing (test didn't complete)
10. **Kernel Panic** - Unrecoverable errors

### Output Format

```
======================================================================
CI Failure Analysis: target/xtask_ring3_smoke_output.txt
======================================================================
Log size: 1523 lines
Patterns detected: 2

──────────────────────────────────────────────────────────────────────

[1] Page Fault
    Line 1234: PAGE FAULT at 0x10001082 Error Code: 0x0

    📊 Diagnosis:
       Page fault accessing unmapped or incorrectly mapped memory

    🔧 Fix:
       Identify the faulting address and check:
       1) Is it mapped in the active page table?
       2) Are the flags correct (USER_ACCESSIBLE, WRITABLE)?
       3) Was it recently unmapped?

    📄 Context:
         1230: [ INFO] Process created: PID 2
         1231: [DEBUG] Switching to process page table
         1232: [DEBUG] About to access userspace memory
         1233: [DEBUG] Buffer pointer: 0x10001082
    >>>  1234: PAGE FAULT at 0x10001082 Error Code: 0x0
         1235: Stack trace:
         1236:   0: copy_from_user
         1237:   1: sys_write
         1238:   2: syscall_handler
```

## Common Failure Patterns

### Double Fault

**Symptoms**:
```
DOUBLE FAULT - Error Code: 0x0
Instruction Pointer: 0x...
Code Segment: ... Ring3
```

**Common Causes**:
1. Kernel stack not mapped in process page table (Ring 3 → Ring 0 transition fails)
2. IST stack misconfigured or unmapped
3. Exception handler itself causes exception
4. Stack overflow

**Diagnosis**:
- Check if fault occurs during syscall (int 0x80)
- Look for recent page table changes
- Verify TSS RSP0 points to valid kernel stack
- Check IST configuration

**Fix Examples**:
- Add kernel stack mapping to process page tables
- Verify IST stacks are mapped
- Increase stack size if overflow
- Review exception handler code

### Page Fault

**Symptoms**:
```
PAGE FAULT at 0x... Error Code: 0x...
```

**Error Code Decoding**:
- Bit 0 (P): 0 = not present, 1 = protection violation
- Bit 1 (W/R): 0 = read, 1 = write
- Bit 2 (U/S): 0 = kernel, 1 = user
- Bit 3 (RSVD): 1 = reserved bit violation
- Bit 4 (I/D): 1 = instruction fetch

**Common Causes**:
1. Accessing unmapped memory
2. Writing to read-only page
3. User code accessing kernel page
4. Page table entry missing

**Diagnosis**:
- Identify faulting address and operation
- Check if address should be mapped
- Verify page table flags (PRESENT, WRITABLE, USER_ACCESSIBLE)
- Look for recent memory operations

### Test Timeout

**Symptoms**:
```
Timeout reached (60s)
... OR ...
Error: test exceeded time limit
```

**Distinguishing Hang vs Slow**:

1. **Kernel hang**: No new output for extended period
   - Timer interrupt not firing
   - Infinite loop
   - Deadlock

2. **Legitimately slow**: Continuous output, just takes longer
   - CI environment slower than local
   - Verbose logging enabled
   - Many tests in sequence

**Diagnosis**:
- Check last log message - what was kernel doing?
- Is timer interrupt still firing? (look for timer ticks)
- Are there any locks being acquired?
- Does it complete locally?

**Fixes**:
- Infinite loop: Add timeout or fix logic
- Deadlock: Review lock acquisition order
- Slow test: Increase timeout or optimize
- Hang: Add debug checkpoints to narrow down location

### Missing Success Signal

**Symptoms**:
```
❌ Ring-3 smoke test failed: no evidence of userspace execution
```

**Common Causes**:
1. Test didn't run (compilation failed silently)
2. Kernel panicked before reaching test
3. Test ran but failed assertions
4. Signal string changed but test wasn't updated

**Diagnosis**:
- Search log for ANY output from the test
- Check if kernel reached test execution point
- Look for earlier errors or panics
- Verify signal string matches test code

### Compilation Error

**Symptoms**:
```
error[E0...]: ...
  --> kernel/src/...
```

**Common Causes**:
1. Wrong Rust nightly version
2. Missing features
3. Syntax error
4. Dependency version mismatch

**Diagnosis**:
- Check Rust version in CI vs. expected
- Verify all required crates are available
- Look for changed dependencies
- Check for feature flag mismatches

### Environment Issues

**Symptoms**:
```
qemu-system-x86_64: command not found
... OR ...
error: target 'x86_64-unknown-none' may not be installed
```

**Common Causes**:
1. System dependencies not installed
2. Rust components missing
3. Wrong Rust installation method
4. PATH not set correctly

**Diagnosis**:
- Check workflow YAML for dependency installation
- Verify Rust toolchain setup
- Check for typos in package names
- Confirm correct ubuntu version

## Analysis Workflow

### Step 1: Identify Failure Type

1. **Download artifacts** from failed GitHub Actions run
2. **Check Actions summary** for which step failed
3. **Determine failure category**:
   - Build failure (compilation)
   - Environment setup failure (missing deps)
   - Test execution failure (kernel crash, timeout, wrong output)

### Step 2: Automated Analysis

```bash
# Run the analyzer on downloaded logs
ci-failure-analysis/scripts/analyze_ci_failure.py \
  --context \
  target/xtask_*_output.txt
```

Review the output for:
- Detected patterns
- Suggested diagnosis
- Recommended fixes

### Step 3: Manual Analysis

If automated analysis doesn't find clear patterns:

```bash
# Search for specific error keywords
grep -i "error\|panic\|fault\|timeout" target/xtask_*_output.txt

# Find last successful operation
grep "SUCCESS\|✓\|✅" target/xtask_*_output.txt | tail -20

# Look for specific subsystem activity
grep "memory\|page table\|process\|syscall" target/xtask_*_output.txt
```

### Step 4: Reproduce Locally

```bash
# Run exact same command as CI
cargo run -p xtask -- ring3-smoke

# Or use quick debug for faster iteration
kernel-debug-loop/scripts/quick_debug.py --signal "EXPECTED_SIGNAL" --timeout 30
```

### Step 5: Compare Environments

| Aspect | Local | CI |
|--------|-------|-----|
| Rust version | Check with `rustc --version` | Check workflow YAML |
| QEMU version | `qemu-system-x86_64 --version` | ubuntu-latest package |
| Timeout | Usually 30s | Usually 60s |
| Build cache | Warm | Cold or partial |
| System load | Low | Variable |

### Step 6: Root Cause Analysis

Document findings using the systematic debugging pattern:

1. **Problem**: What failed?
2. **Root Cause**: Why did it fail?
3. **Solution**: What fixes it?
4. **Evidence**: How do you know it's fixed?

## Integration with Other Skills

### Use with kernel-debug-loop

After identifying a failure, use `kernel-debug-loop` for rapid iteration:

```bash
# Test fix with quick feedback
kernel-debug-loop/scripts/quick_debug.py \
  --signal "🎯 KERNEL_POST_TESTS_COMPLETE 🎯" \
  --timeout 15
```

### Use with github-workflow-authoring

Fix workflow issues:

```bash
# If environment issue detected:
# 1. Identify missing dependency from analyzer output
# 2. Update workflow using github-workflow-authoring skill
# 3. Test change in PR
```

### Use with systematic-debugging

Document the failure:

```markdown
# Problem
CI run #123 failed with page fault at 0x10001082

# Root Cause
[Fill in after analysis]

# Solution
[Fill in after fix]

# Evidence
[Fill in after verification]
```

## Advanced Techniques

### Diff Analysis

Compare working vs broken runs:

```bash
# Download logs from last successful run and failed run
diff -u successful_run.txt failed_run.txt | less
```

Look for:
- First point where outputs diverge
- Missing initialization steps
- Different memory addresses (ASLR not implemented, so addresses should match)

### Timeline Reconstruction

Find the last known-good state:

```bash
grep -n "SUCCESS\|COMPLETE\|initialized" target/xtask_*_output.txt | tail -20
```

This shows what completed before the failure.

### Iterative Binary Search

If failure point unclear:

1. Add checkpoint log in middle of suspect region
2. Rebuild and retest
3. Narrow down based on whether checkpoint reached
4. Repeat until failure location isolated

### Statistical Analysis

For intermittent failures:

```bash
# Run test 10 times, count failures
for i in {1..10}; do
  cargo run -p xtask -- ring3-smoke && echo "PASS" || echo "FAIL"
done | sort | uniq -c
```

## Best Practices

1. **Always download logs**: Don't rely on Actions UI truncation
2. **Check multiple logs**: Compile errors vs runtime errors vs test output
3. **Compare with local**: Reproduce failures locally when possible
4. **Search for first error**: Often followed by cascading failures
5. **Check recent changes**: What changed between last working and first broken run?
6. **Verify environment**: Toolchain versions, dependencies, configurations
7. **Document patterns**: Add new patterns to analyzer when discovered
8. **Test fixes**: Verify fix locally before pushing to CI

## Example Analysis Session

```bash
# 1. Download artifact from failed CI run
#    Save to: target/xtask_ring3_smoke_output.txt

# 2. Run automated analysis
ci-failure-analysis/scripts/analyze_ci_failure.py \
  --context target/xtask_ring3_smoke_output.txt

# Output shows: Page Fault at 0x10001082

# 3. Search for context
grep -B10 -A10 "0x10001082" target/xtask_ring3_smoke_output.txt

# 4. Identify: copy_from_user failing

# 5. Check if this address is mapped
grep "process page table\|mapping" target/xtask_ring3_smoke_output.txt

# 6. Hypothesis: User buffer not mapped in process page table

# 7. Review recent changes to process memory code

# 8. Identify fix needed

# 9. Test locally with quick iteration
kernel-debug-loop/scripts/quick_debug.py \
  --signal "USERSPACE OUTPUT" \
  --timeout 10

# 10. Verify fix works

# 11. Push to PR, monitor CI
```

## Summary

CI failure analysis for Breenix requires:
- Automated pattern detection for common failures
- Manual log analysis for novel issues
- Environment comparison (local vs CI)
- Systematic root cause investigation
- Integration with debugging and testing workflows
- Documentation of findings

The `analyze_ci_failure.py` script automates common pattern detection, but kernel debugging ultimately requires understanding the code, memory management, interrupt handling, and the specific feature being tested.
