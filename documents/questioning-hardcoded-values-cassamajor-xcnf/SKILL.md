---
name: questioning-hardcoded-values
description: Hardcoded strings and numbers need justification - they're either conventions that need documentation, magic numbers that should be constants, or assumptions that need verification
type: technique
tags: [code-review, documentation, assumptions, conventions]
---

# Questioning Hardcoded Values

## Overview

When you see hardcoded strings, numbers, or other literal values in code during review or implementation, **question them**. They fall into three categories:

1. **Conventions** - Need documentation
2. **Magic numbers** - Should be named constants
3. **Assumptions** - Need verification

All three require justification and documentation.

**Core Principle:** Hardcoded values should answer "why this specific value?"

## When to Use

Use this skill when:
- Reviewing code (your own or others')
- Seeing unexplained literals in implementation
- Implementing protocols, naming schemes, or standards
- Encountering values that "just work" without explanation

## The Problem

### Bad Pattern

```go
func CreatePair(name string) (*Pair, error) {
    // ... create primary ...

    // Get peer
    peerName := name + "p"  // Why "p"?
    peer, err := netlink.LinkByName(peerName)
    // ...
}
```

**Questions this should raise:**
- Why "p"?
- Is this a standard convention?
- What if peer has different naming?
- Did we test this assumption?

### What Actually Happened

**Session example:**

```go
// My code:
peerName := name + "p"
```

**User:** "Why are we hardcoding the p?"

**Investigation revealed:**
- It's NOT a kernel convention (kernel uses other patterns)
- We SET this via `SetPeerAttrs()` ourselves
- Needs explicit documentation as OUR convention
- Should be verified against actual behavior

**Result:** Added comment explaining it's our choice, verified it works, documented in README.

## Categories of Hardcoded Values

### 1. Conventions That Need Documentation

**Example:**
```go
// Bad - no explanation
peerName := name + "p"

// Good - documented convention
// Peer naming convention: primary name + "p" suffix
// (e.g., "nk0" primary -> "nk0p" peer, similar to veth naming)
peerName := name + "p"
```

**Actions:**
- Comment explaining the convention
- Document in README
- Reference standards if applicable

**Example from session:**
```go
// Set up peer attributes with "p" suffix convention
// (e.g., "nk0" primary -> "nk0p" peer, similar to veth naming)
peerName := name + "p"
```

README:
```markdown
### Naming Convention

Netkit devices follow a "primary + p" naming convention (similar to veth):
- Primary: `nk0`
- Peer: `nk0p`

This is explicitly configured using `SetPeerAttrs()` before device creation.
```

### 2. Magic Numbers That Should Be Constants

**Example:**
```go
// Bad - what is 37?
if len(data) < 37 {
    return
}

// Good - named constant
const ipv6EventSize = 37  // 16 src + 16 dst + 1 next + 2 len + 1 hop + 1 dir

if len(data) < ipv6EventSize {
    return
}
```

**Actions:**
- Extract to named constant
- Add comment explaining calculation
- Use sizeof if applicable

### 3. Assumptions That Need Verification

**Example:**
```go
// Assumption: interface will be "up" immediately
assert.Equal(t, "up", iface.OperState.String())
```

**User catches:** "Is this always true?"

**Investigation:**
```bash
# Test shows: netkit shows "unknown" or "down" initially
assert.Equal(t, "up", pair.Primary.Attrs().OperState.String())
# FAILS
```

**Fix:** Test what actually matters
```go
// Verify interface exists and has correct name
assert.Equal(t, devName, pair.Primary.Attrs().Name)
assert.Greater(t, pair.PrimaryIdx, 0)
```

**Actions:**
- Test the assumption
- Document actual behavior
- Update code/tests based on reality

## Process for Questioning

### Step 1: Identify the Value

**Strings:**
- Suffixes/prefixes: `"p"`, `"_peer"`, `"test_"`
- Paths: `"/sys/kernel/btf/vmlinux"`
- Formats: `"fe80::/64"`

**Numbers:**
- Buffer sizes: `256 * 1024`
- Offsets: `37`
- Counts: `3` (retries), `5` (timeout)

**Patterns:**
- Calculations: `name + "p"`
- Checks: `if x == "up"`

### Step 2: Ask Questions

**For strings:**
- Is this a standard? (RFC, kernel convention)
- Is this our convention?
- Could this change?

**For numbers:**
- What does this represent?
- Why this specific value?
- Is there a calculation?

**For assumptions:**
- Is this always true?
- Have we tested this?
- What if it's not true?

### Step 3: Take Action

| Category | Action |
|----------|--------|
| **Standard/Convention** | Document with reference |
| **Our Choice** | Comment + README explanation |
| **Magic Number** | Extract to constant |
| **Assumption** | Verify with test |
| **Configuration** | Make it configurable |

## Examples from Session

### Example 1: Peer Naming

**Original:**
```go
peerName := name + "p"
peer, err := netlink.LinkByName(peerName)
```

**Question:** "Why are we hardcoding the p?"

**Investigation:**
```bash
$ sudo ip link add test type netkit mode l3
$ ip link show | grep test
22: nk0@test: ...  # Kernel generated name!
23: test@nk0: ...
```

Kernel doesn't use "p" suffix automatically.

**Resolution:**
```go
// Set up peer attributes with "p" suffix convention
// (e.g., "nk0" primary -> "nk0p" peer, similar to veth naming)
peerName := name + "p"
peerAttrs := netlink.NewLinkAttrs()
peerAttrs.Name = peerName
primary.SetPeerAttrs(&peerAttrs)
```

+ README documentation + comment explaining our choice

### Example 2: OperState Assumption

**Original test:**
```go
// Verify both interfaces are up
assert.Equal(t, "up", pair.Primary.Attrs().OperState.String())
assert.Equal(t, "up", pair.Peer.Attrs().OperState.String())
```

**Actual result:**
```
expected: "up"
actual: "unknown"
```

**Question:** Is OperState immediately "up"?

**Answer:** No - netkit interfaces may show "unknown" or "down" initially.

**Fix:**
```go
// Verify interface names follow convention
assert.Equal(t, devName, pair.Primary.Attrs().Name)
assert.Equal(t, devName+"p", pair.Peer.Attrs().Name)
// Index > 0 proves interface exists
assert.Greater(t, pair.PrimaryIdx, 0)
```

### Example 3: Event Size

**Original:**
```go
if len(data) < 37 {
    return
}
```

**Question:** What is 37?

**Should be:**
```go
const (
    ipv6SrcAddrBytes = 16
    ipv6DstAddrBytes = 16
    ipv6NextHeader   = 1
    ipv6PayloadLen   = 2
    ipv6HopLimit     = 1
    ipv6Direction    = 1
    ipv6EventSize    = 37  // Total: 16+16+1+2+1+1
)

if len(data) < ipv6EventSize {
    return
}
```

## Code Review Checklist

When reviewing code, check for:

- [ ] Hardcoded strings explained with comments
- [ ] Magic numbers extracted to constants
- [ ] Assumptions verified with tests
- [ ] Conventions documented in README
- [ ] Standards referenced (RFC, kernel docs, etc.)
- [ ] "Why this value?" has an answer

## Red Flags

Hardcoded values that raise concerns:
- Unexplained suffixes/prefixes
- Numbers without context
- Paths without documentation
- Equality checks on dynamic values
- "It just works" without explanation

## Common Patterns

### File Paths

```go
// Bad
path := "/sys/kernel/btf/vmlinux"

// Good
const kernelBTFPath = "/sys/kernel/btf/vmlinux"  // Standard kernel BTF location

// Or configurable
var btfPath = flag.String("btf", "/sys/kernel/btf/vmlinux", "Path to kernel BTF")
```

### Protocol Constants

```go
// Bad
if eth.h_proto != 0x86DD {

// Good
const ETH_P_IPV6 = 0x86DD  // IPv6 ethertype per IEEE 802
if eth.h_proto != bpf_htons(ETH_P_IPV6) {
```

### Naming Conventions

```go
// Bad
testName := "test_" + name

// Good
// Test isolation: prefix with "test_" to identify temporary resources
testName := "test_" + name
```

## Benefits

**For you:**
- Understand code's assumptions
- Catch bugs early
- Easier to change later

**For others:**
- Clear why values were chosen
- Documented conventions
- Can modify with confidence

**For debugging:**
- Know what's configurable
- Understand failures better
- Verify assumptions quickly

## Summary

**When you see hardcoded values, ask:**
1. **Is this a convention?** → Document it
2. **Is this a magic number?** → Name it
3. **Is this an assumption?** → Verify it

**Every hardcoded value should answer: "Why this specific value?"**

Not asking = hidden assumptions = future bugs.
