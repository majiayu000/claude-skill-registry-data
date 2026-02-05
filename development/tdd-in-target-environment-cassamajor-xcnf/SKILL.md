---
name: tdd-in-target-environment
description: Run tests in the actual execution environment, not just where they compile - TDD's "watch it fail" step is meaningless if tests skip or can't run where code will execute
type: technique
tags: [tdd, testing, cross-platform, verification]
---

# TDD in Target Environment

## Overview

Tests that skip or can't run in the actual execution environment don't verify anything meaningful. TDD's "watch it fail" and "watch it pass" steps require running tests **where the code will actually execute**, not just where it compiles.

**Core Principle:** Compilation ≠ Verification

## When to Use

Use this skill when:
- Writing platform-specific code (Linux kernel features, system calls, hardware)
- Developing cross-platform (macOS dev → Linux prod)
- Code requires special capabilities (root, BPF, network namespaces)
- Tests use `t.Skip()`, `os.Geteuid()`, or conditional execution
- CI passes but manual testing fails

## The Problem

### Bad Pattern
```go
func TestNetworkFeature(t *testing.T) {
    if runtime.GOOS != "linux" {
        t.Skip("Requires Linux")
    }

    // Test netlink, eBPF, etc.
}
```

**On macOS development machine:**
- ✅ Test compiles
- ✅ Test runs
- ⚠️ Test skips
- ❌ **No verification happened**

You think: "Tests pass locally, ship it!"

Reality: Code has bugs that only appear on Linux.

### What Actually Happened

**Session example:**
1. Wrote tests for netkit device creation
2. Tests compiled and "passed" on macOS (via skip)
3. User caught this: "Why are we skipping tests?"
4. Ran in OrbStack VM → tests actually failed
5. Found real bugs: peer naming wrong, OperState assumptions incorrect

**TDD cycle was broken:**
- ❌ Never watched test fail (skipped instead)
- ❌ Never verified implementation works (skipped instead)
- ❌ False confidence from "passing" tests

## The Solution

### Run Tests Where Code Executes

**For Linux-specific code developed on macOS:**

```bash
# DON'T: Run tests locally and skip
go test ./...  # Everything "passes" (skips)

# DO: Run tests in target environment
orb run bash -c "sudo -E go test ./... -v"
```

**TDD Cycle with Target Environment:**

1. **RED Phase:**
   ```bash
   # Write test on macOS
   # Run in VM to watch it fail
   orb run bash -c "sudo -E go test -v -run TestFeature"
   ```

   Expected: Actual failure (undefined function, etc.)

   Not: Skip or "pass"

2. **GREEN Phase:**
   ```bash
   # Implement on macOS
   # Run in VM to watch it pass
   orb run bash -c "sudo -E go test -v -run TestFeature"
   ```

   Expected: Actual pass

   Verify: All assertions pass, no skips

3. **REFACTOR Phase:**
   ```bash
   # Refactor code
   # Run in VM to keep tests green
   orb run bash -c "sudo -E go test -v ./..."
   ```

### Don't Skip Tests During Development

**Bad:**
```go
func TestCreateNetkit(t *testing.T) {
    if os.Geteuid() != 0 {
        t.Skip("Requires root")
    }
    // Test implementation
}
```

**Why it's bad:**
- Encourages running tests that skip
- Developer never sees tests actually run
- CI might not run them either

**Better:**
```go
func TestCreateNetkit(t *testing.T) {
    if os.Geteuid() != 0 {
        t.Skip("Requires root - run in VM: orb run bash -c 'sudo -E go test'")
    }
    // Test implementation
}
```

**Best:**
- Run tests in target environment during development
- Skip is fallback for CI/other devs, not your workflow
- Use `make test-vm` or similar to automate

## Patterns for Different Platforms

### Linux Features on macOS Dev Machine

**Tools:**
- OrbStack: `orb run bash -c "command"`
- Docker: `docker run --rm -v $(pwd):/workspace golang:latest bash -c "cd /workspace && go test"`
- Lima: `limactl shell default command`

**Workflow:**
```bash
# Edit code locally (macOS)
# Test in target environment (Linux VM)
orb run bash -c "cd /path/to/project && sudo -E go test -v ./..."
```

### Privileged Operations

**Don't:**
```go
if os.Geteuid() != 0 {
    t.Skip("Need root")
}
```

**Do:**
```bash
# Run tests with required privileges
sudo -E go test -v ./...
```

**Document:**
```markdown
## Testing

Requires root privileges:
```bash
sudo -E go test -v ./...
```

Or in VM:
```bash
orb run bash -c "sudo -E go test -v ./..."
```
```

### Hardware-Specific Features

**Example: eBPF, netlink, network namespaces**

```go
// NO Skip in the test itself
// Run in correct environment instead

func TestAttachXDP(t *testing.T) {
    // Actual test, no skip
    prog := loadXDPProgram(t)
    err := attachXDP(prog, "eth0")
    require.NoError(t, err)
}
```

**README:**
```markdown
## Testing

Tests require:
- Linux kernel 5.15+
- CAP_BPF, CAP_NET_ADMIN
- Network interfaces

Run in OrbStack VM:
```bash
orb run bash -c "sudo -E go test -v ./..."
```
```

## Meaningless Verification

### Avoid "Does It Compile?" Checks

**Bad:**
```bash
# "Verify" eBPF package compiles
go build ./bytecode
```

**Why it's bad:**
- Package has no `main()`, build produces nothing useful
- Only tests syntax, not functionality
- False confidence

**What to do instead:**
- Skip library-only packages
- Test at integration points
- Verify actual usage

**Good:**
```bash
# Integration test actually uses the package
go test -v ./...  # Tests import and use bytecode package
```

## Examples from Session

### Netkit Device Creation

**Before (macOS):**
```bash
$ go test ./netkit -v
=== RUN   TestCreatePair
    netkit_test.go:13: Requires root privileges
--- SKIP: TestCreatePair (0.00s)
```

"Tests pass!" (Wrong - they skipped)

**After (OrbStack VM):**
```bash
$ orb run bash -c "sudo -E go test ./netkit -v"
=== RUN   TestCreatePair/create_L3_pair
    netkit_test.go:51: failed to find peer "test0p"
--- FAIL: TestCreatePair/create_L3_pair (0.02s)
```

Found real bug! Fixed peer naming.

**Final (VM, fixed):**
```bash
$ orb run bash -c "sudo -E go test ./netkit -v"
=== RUN   TestCreatePair/create_L3_pair
--- PASS: TestCreatePair/create_L3_pair (0.02s)
```

Actual verification.

## Checklist

Before marking TDD work complete:

- [ ] All tests run in target environment
- [ ] Watched tests actually fail (not skip)
- [ ] Watched tests actually pass (not skip)
- [ ] Verified failure messages are correct
- [ ] Documented how to run tests in target environment
- [ ] No "does it compile?" checks for libraries
- [ ] Integration tests verify actual usage

## Red Flags

- Tests with `t.Skip()` that you never see run
- "All tests pass" but none actually executed
- Build checks for library packages
- Different behavior in CI vs local
- Platform-specific code without target environment testing
- Relying on compilation as verification

## Common Rationalizations

- "I'll test it in CI" → You won't catch issues during development
- "Skip is fine for cross-platform" → Only if you also test in target
- "It compiles, so it works" → Compilation proves syntax, not behavior
- "I manually tested it" → Not reproducible, not automated
- "CI will catch it" → Slow feedback loop, harder to debug

## Summary

**Bad Workflow:**
1. Write test on macOS
2. Test skips
3. Write implementation
4. Test still skips
5. Ship → breaks in production

**Good Workflow:**
1. Write test on macOS
2. Run in VM → watch it fail
3. Write implementation
4. Run in VM → watch it pass
5. Ship → confidence it works

**TDD requires running tests where code executes. Skipping tests breaks the cycle.**
