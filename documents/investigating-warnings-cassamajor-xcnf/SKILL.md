---
name: investigating-warnings
description: Don't dismiss warnings without understanding them - investigate to determine if they indicate bugs, misconfigurations, or are cosmetic, then document findings either way
type: technique
tags: [debugging, warnings, verification, documentation]
---

# Investigating Warnings

## Overview

Warnings in output (compiler, runtime, CLI tools) shouldn't be automatically dismissed or ignored. Each warning deserves investigation to understand:

1. **Is it a bug?** - Indicates actual problem in code/config
2. **Is it a misconfiguration?** - Fixable issue
3. **Is it cosmetic?** - Expected behavior, just noisy

All three require documentation explaining the finding.

**Core Principle:** Every warning has a reason. Understand it, then decide.

## When to Use

Use this skill when:
- Any warning appears in output (build, test, runtime, CLI)
- Tool outputs cautionary messages
- Logs contain unexpected entries
- About to add "ignore this warning" to docs
- Considering suppressing warning output

## The Problem

### Bad Pattern
```bash
$ ping6 -I demop ff02::1
ping6: Warning: source address might be selected on device other than: demop
# "Probably fine, ignore it"
```

**Problems:**
- Don't know if it's hiding a bug
- Future maintainers will wonder about it
- Might indicate deeper issue
- No way to verify it's harmless

### What Actually Happened

**Session example:**

```bash
$ ping6 -I test_mainp ff02::1
ping6: Warning: source address might be selected on device other than: test_mainp
```

**User:** "Should we be concerned about the warning?"

**Investigation process:**
1. Check interface addresses: `ip addr show test_mainp`
2. Discovered TWO link-local addresses on interface:
   - Kernel auto-generated: `fe80::...` (from MAC)
   - Our assigned: `fe80::...` (random IID)
3. Researched ping6 behavior with multiple link-local addresses
4. Verified packets still flow correctly (eBPF captured them)

**Conclusion:**
- **Category:** Cosmetic - not a bug
- **Reason:** Multiple link-local addresses trigger warning
- **Fix:** Use `%` notation rather than `-I`: `ping6 ff02::1%test_mainp`
- **Action:** Document in README troubleshooting section

**Result:** User has confidence warning is harmless, future users won't be concerned.

## Categories of Warnings

### 1. Bugs (Must Fix)

**Example:**
```go
// Warning: variable 'err' is never checked
result, err := doSomething()
return result
```

**Investigation:**
- Check function signature
- Verify error handling

**Fix:**
```go
result, err := doSomething()
if err != nil {
    return nil, fmt.Errorf("doing something: %w", err)
}
return result
```

### 2. Misconfigurations (Should Fix)

**Example:**
```bash
WARNING: Running tests without -v flag may hide failure details
```

**Investigation:**
- Check test command flags
- Review CI configuration

**Fix:**
```bash
# Add -v flag to test commands
go test -v ./...
```

### 3. Cosmetic (Document)

**Example:**
```bash
ping6: Warning: source address might be selected on device other than: demop
```

**Investigation:**
- Check interface state
- Verify functionality still works
- Research tool behavior

**Documentation:**
```markdown
## Troubleshooting

**Warning: "source address might be selected on device other than"**
- Cosmetic warning from ping6
- Occurs when multiple link-local addresses exist on interface
- Packets flow correctly; eBPF programs capture traffic as expected
- No action needed
```

## Investigation Process

### Step 1: Reproduce and Capture

**Capture exact warning:**
```bash
# Save full output
command 2>&1 | tee output.log
```

**Note context:**
- When does it appear?
- Every time or intermittently?
- Before/after specific changes?

### Step 2: Inspect System State

**For network warnings:**
```bash
ip addr show <interface>
ip link show <interface>
ip route show
```

**For eBPF warnings:**
```bash
sudo bpftool prog list
sudo bpftool map list
dmesg | tail
```

**For build warnings:**
```bash
# Check actual definitions
go doc <package>.<Type>
# Verify imports
go list -m all
```

### Step 3: Research

**Check documentation:**
- Man pages: `man ping6`
- Package docs: `go doc`
- Project READMEs
- Kernel docs

**Search issues:**
```bash
gh issue list --repo <org>/<repo> --search "warning text"
```

**Web search:**
- Include exact warning text in quotes
- Add context (tool name, version)

### Step 4: Verify Impact

**Does it affect functionality?**
- Run tests
- Check output
- Verify expected behavior

**Session example:**
```bash
# Warning appeared but eBPF still captured packets
[peer] IPv6: fe80::... -> ff02::1 | next=58 len=64 ttl=255
# ✓ Functionality works despite warning
```

### Step 5: Document Findings

**In code (for build/lint warnings):**
```go
// Suppress "unused" warning: keepalive ticker prevents connection timeout
_ = keepaliveTicker
```

**In README (for runtime warnings):**
```markdown
### Known Warnings

**ping6 source address warning**
- Expected when interface has multiple link-local addresses
- Does not affect packet delivery
- See: https://man7.org/linux/man-pages/man8/ping.8.html
```

**In commit message:**
```
Add IPv6 link-local configuration

Note: ping6 may warn about source address selection when interface
has both kernel-generated and manually assigned link-local addresses.
This is cosmetic and doesn't affect functionality.
```

## Examples from Session

### ping6 Source Address Warning

**Warning:**
```bash
ping6: Warning: source address might be selected on device other than: test_mainp
```

**Investigation:**
```bash
$ ip addr show test_mainp
12: test_mainp@test_main: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    link/ether 96:8b:bf:87:91:04
    inet6 fe80::a4b3:12ff:fe34:5678/64 scope link    # Our assigned
    inet6 fe80::948b:bfff:fe87:9104/64 scope link    # Kernel generated
```

**Conclusion:** Two link-local addresses → ping6 unsure which to use → warning

**Documentation added to README:**
> **Warning: "source address might be selected on device other than"**
> - Cosmetic warning from ping6
> - Occurs when multiple link-local addresses exist
> - Packets still flow correctly through the interface

## Checklist

When encountering a warning:

- [ ] Capture exact warning text
- [ ] Note when it appears (build, runtime, specific command)
- [ ] Inspect relevant system state
- [ ] Research documentation and issues
- [ ] Verify whether functionality is affected
- [ ] Categorize: bug, misconfiguration, or cosmetic
- [ ] Fix if needed, document if cosmetic
- [ ] Update README/docs with finding

## Red Flags

Dismissing warnings without investigation:
- "Probably fine"
- "Just a warning, not an error"
- "Doesn't seem to break anything"
- "I'll look into it later"
- "Other people probably ignore this too"

## Common Rationalizations

- "It's just a warning, not an error" → Warnings can indicate bugs
- "Tests pass so it's fine" → Tests might not cover affected code path
- "It's too noisy to investigate" → Noise often hides real issues
- "I'll document it later" → You'll forget the context
- "It worked before the warning" → New warning = something changed

## Benefits

**For you:**
- Catch bugs early
- Understand tool behavior
- Build troubleshooting skills

**For others:**
- Clear documentation
- No mystery warnings
- Confidence in "expected" behavior

**For debugging:**
- Known cosmetic warnings documented
- Real warnings stand out
- Context for future issues

## Summary

**When you see a warning:**
1. **Capture it** → Full text and context
2. **Investigate it** → System state, docs, research
3. **Categorize it** → Bug, misconfiguration, or cosmetic
4. **Document it** → Code comments, README, commit message

**Every warning deserves understanding. Ignoring warnings = accepting unknown unknowns.**
