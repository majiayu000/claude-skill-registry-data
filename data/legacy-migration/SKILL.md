---
name: legacy-migration
description: This skill should be used when migrating features from src.legacy/ to the new kernel implementation or removing legacy code after reaching feature parity. Use for systematic legacy code removal, updating FEATURE_COMPARISON.md, verifying feature equivalence, and ensuring safe code retirement.
---

# Legacy Code Migration for Breenix

Systematically migrate features from legacy kernel and remove old code when parity is reached.

## Purpose

Breenix is transitioning from a legacy kernel (src.legacy/) to a modern implementation (kernel/). This skill provides patterns for safely migrating features, verifying parity, and removing legacy code.

## When to Use

- **Feature migration**: Porting legacy features to new kernel
- **Parity verification**: Confirming new implementation matches legacy behavior
- **Legacy removal**: Safely removing old code after feature completion
- **Documentation updates**: Keeping FEATURE_COMPARISON.md current
- **Risk assessment**: Evaluating what can be safely removed

## Legacy Migration Principle (from CLAUDE.md)

```
When new implementation reaches parity:
1. Remove code from src.legacy/
2. Update FEATURE_COMPARISON.md
3. Include removal in same commit as feature completion
```

**Key Point**: Don't accumulate dead code. Remove legacy as soon as parity is reached.

## Migration Workflow

### Phase 1: Identify Feature for Migration

**Review FEATURE_COMPARISON.md:**

```bash
# See what's in legacy but not new
cat docs/planning/legacy-migration/FEATURE_COMPARISON.md | grep "❌"

# See what's partially implemented
cat docs/planning/legacy-migration/FEATURE_COMPARISON.md | grep "🚧"
```

**Common patterns:**
- ✅ Fully implemented (safe to remove if in both)
- 🚧 Partially implemented (needs work)
- ❌ Not implemented (needs migration or decision)
- 🔄 Different approach (verify equivalence)

### Phase 2: Analyze Legacy Implementation

**Locate the legacy code:**

```bash
# Find legacy implementation
find src.legacy -name "*feature_name*"

# Search for specific functionality
grep -r "feature_function" src.legacy/
```

**Understand the implementation:**
1. What does it do? (API, behavior, edge cases)
2. Why does it exist? (requirements it satisfies)
3. How does it work? (algorithm, data structures)
4. What depends on it? (other modules, tests)

**Extract key characteristics:**
- Public API surface
- Critical behavior
- Edge case handling
- Error conditions
- Test coverage

### Phase 3: Implement in New Kernel

**Follow Breenix standards:**

```rust
// 1. Add to appropriate module in kernel/src/
// 2. Use modern Rust patterns
// 3. Add #[cfg(feature = "testing")] for test code
// 4. Write comprehensive tests
// 5. Document with clear comments
```

**Quality checklist:**
- [ ] Matches legacy API (if public)
- [ ] Handles all edge cases
- [ ] Error handling implemented
- [ ] Tests written and passing
- [ ] Documentation complete
- [ ] No compiler warnings
- [ ] Clippy clean

### Phase 4: Verify Parity

**Functional equivalence:**

```bash
# Run tests for the feature
cargo test feature_name

# Check behavior matches legacy
# (Compare outputs, test edge cases)

# Run full test suite
cargo test
```

**API compatibility:**
- If API is public: Must match exactly
- If internal: Can improve design
- Document any intentional differences

**Behavioral parity checklist:**
- [ ] Same inputs produce same outputs
- [ ] Edge cases handled identically
- [ ] Error conditions match
- [ ] Performance acceptable
- [ ] Integration with other subsystems works

### Phase 5: Update Documentation

**Update FEATURE_COMPARISON.md:**

```markdown
### Feature Category
| Feature | Legacy | New | Notes |
|---------|--------|-----|-------|
| Feature X | ~~✅ Full~~ (removed) | ✅ | Migrated in PR #123, legacy removed |
```

**Patterns:**
- Change legacy column to `~~✅ Full~~ (removed)`
- Update new column to ✅
- Add note about migration PR
- Include date if significant

**Document any differences:**

```markdown
## Implementation Differences

### Feature X
- **Legacy**: Used approach A
- **New**: Uses approach B (reason)
- **Rationale**: Cleaner design, better performance, etc.
```

### Phase 6: Remove Legacy Code

**In the SAME commit as feature completion:**

```bash
# Remove the legacy files
git rm src.legacy/path/to/feature.rs

# Or if removing entire module
git rm -r src.legacy/module/

# Stage FEATURE_COMPARISON.md changes
git add docs/planning/legacy-migration/FEATURE_COMPARISON.md

# Commit together
git commit -m "Complete Feature X implementation and remove legacy

- Implement Feature X in kernel/src/module/feature.rs
- Full parity with legacy implementation
- Remove legacy code from src.legacy/
- Update FEATURE_COMPARISON.md

Tested with: cargo test feature_x
"
```

**Critical**: Legacy removal MUST be in the same commit to maintain atomicity.

## Legacy Code Categories

### 1. Direct Migration

**What**: Feature can be ported directly with minimal changes

**Example**: VGA text mode removed after framebuffer complete

**Process**:
1. Understand legacy implementation
2. Port to new codebase
3. Test thoroughly
4. Remove legacy
5. Update docs

### 2. Reimplementation

**What**: New approach taken, but achieves same goals

**Example**: Timer system (different RTC implementation)

**Process**:
1. Identify requirements from legacy
2. Design new approach
3. Implement with modern patterns
4. Verify equivalent behavior
5. Remove legacy
6. Document differences

### 3. Obsolete Features

**What**: Feature no longer needed or superseded

**Example**: VGA text after framebuffer works

**Process**:
1. Verify feature truly obsolete
2. Check no dependencies
3. Remove from legacy
4. Update FEATURE_COMPARISON.md with rationale

### 4. Deferred Features

**What**: Features not yet needed in new kernel

**Example**: Network stack (not current priority)

**Process**:
1. Document decision to defer
2. Mark as ❌ in FEATURE_COMPARISON.md
3. Leave in legacy as reference
4. Add to future roadmap

## Common Migration Patterns

### Pattern: Device Driver

```rust
// Legacy: src.legacy/drivers/device_x.rs
// New: kernel/src/drivers/device_x.rs

// 1. Port driver structure
pub struct DeviceX {
    // ... fields
}

// 2. Port initialization
impl DeviceX {
    pub fn new() -> Self { ... }
}

// 3. Port public API
impl DeviceX {
    pub fn operation(&mut self) { ... }
}

// 4. Add tests
#[cfg(test)]
mod tests {
    #[test]
    fn test_device_x() { ... }
}
```

### Pattern: System Call

```rust
// Legacy: src.legacy/syscall/handler.rs (mostly commented out)
// New: kernel/src/syscall/handler.rs (full implementation)

// 1. Define syscall number
pub const SYS_FEATURE: u64 = N;

// 2. Add to dispatcher
pub fn syscall_handler(num: u64, args: ...) {
    match num {
        SYS_FEATURE => sys_feature(args),
        // ...
    }
}

// 3. Implement handler
fn sys_feature(args: ...) -> u64 {
    // Implementation
}

// 4. Test from userspace
// userspace/tests/feature_test.rs
```

### Pattern: Infrastructure

```rust
// Legacy: Multiple files implementing async
// New: Consolidated in kernel/src/task/

// 1. Analyze legacy architecture
// 2. Design improved structure
// 3. Implement with better patterns
// 4. Migrate tests
// 5. Document improvements
```

## Risk Assessment

Before removing legacy code, assess:

### High Risk (Don't Remove Yet)
- Features not yet implemented in new kernel
- Complex subsystems (network, filesystem)
- Code with unique algorithms or logic
- Reference implementations for future work

### Medium Risk (Remove with Caution)
- Features with partial new implementation
- Code with subtle edge cases
- Infrastructure with many dependencies

### Low Risk (Safe to Remove)
- Features fully implemented and tested
- Obsolete approaches (VGA text mode)
- Dead code (never called)
- Superseded implementations

## Integration with Development

### During Feature Development

```bash
# 1. Check if legacy has this feature
grep -r "feature_name" src.legacy/

# 2. If found, analyze it
less src.legacy/path/to/feature.rs

# 3. Implement in new kernel
# ... development work ...

# 4. Test thoroughly
cargo test feature_name

# 5. Remove legacy in same commit
git rm src.legacy/path/to/feature.rs

# 6. Update FEATURE_COMPARISON.md
# ... edit ...

# 7. Commit together
git commit -m "Implement feature_name and remove legacy"
```

### PR Review Checklist

When reviewing PRs that claim feature parity:

- [ ] New implementation tested
- [ ] Legacy code removed
- [ ] FEATURE_COMPARISON.md updated
- [ ] All changes in one atomic commit
- [ ] No regression in related features
- [ ] Documentation complete

## Current Migration Status

Based on FEATURE_COMPARISON.md (as of latest):

**Completed Migrations:**
- Memory management (frame allocator, paging, heap) ✅
- Async executor and task management ✅
- Timer system (PIT + RTC) ✅
- Keyboard driver ✅
- Serial output ✅
- Test infrastructure ✅
- Syscall infrastructure ✅
- Fork/exec system calls ✅

**Not Yet Migrated:**
- Network drivers (Intel E1000, RTL8139) ❌
- PCI bus support ❌
- Interrupt statistics tracking ❌
- Event system ❌

**Different Approach:**
- Print macros (log system vs direct print) 🔄
- Display (framebuffer vs VGA text) 🔄

## Special Cases

### When Legacy Has Better Implementation

**Scenario**: Legacy code is actually better designed

**Action**:
1. Port legacy approach to new kernel
2. Improve if possible
3. Remove legacy
4. Document that you used legacy as reference

### When API Must Change

**Scenario**: Legacy API is poor, new needs different design

**Action**:
1. Design better API
2. Document differences in FEATURE_COMPARISON.md
3. Explain rationale in commit message
4. Remove legacy

### When Uncertain

**Scenario**: Not sure if new implementation is equivalent

**Action**:
1. Write comprehensive tests
2. Compare outputs on same inputs
3. Ask for review
4. Document any known differences
5. Only remove legacy when confident

## Best Practices

1. **Remove in same commit**: Legacy removal with feature completion
2. **Update docs immediately**: Don't accumulate documentation debt
3. **Test thoroughly**: Verify parity before removing legacy
4. **Document differences**: Explain any intentional changes
5. **Keep reference**: For complex features, document algorithm before removing
6. **Atomic operations**: Feature + removal + docs in one commit
7. **Review carefully**: PRs that remove legacy need extra scrutiny

## Example Migration Session

```bash
# Identify target feature
cat docs/planning/legacy-migration/FEATURE_COMPARISON.md | grep "❌"

# Found: Event system not yet implemented

# Analyze legacy
less src.legacy/events/mod.rs
grep -r "Event" src.legacy/

# Implement in new kernel
# ... create kernel/src/events/mod.rs ...
# ... write tests ...

# Verify
cargo test events

# Remove legacy and update docs
git rm -r src.legacy/events/
# Edit FEATURE_COMPARISON.md

# Commit atomically
git add kernel/src/events/ tests/test_events.rs
git add docs/planning/legacy-migration/FEATURE_COMPARISON.md
git commit -m "Implement event system and remove legacy

- Add event system in kernel/src/events/
- Full parity with legacy implementation
- Enhanced with better error handling
- Remove src.legacy/events/
- Update FEATURE_COMPARISON.md

Tested with: cargo test events
All tests passing, no regressions.
"
```

## Summary

Legacy code migration requires:
- Systematic analysis of legacy implementation
- Full parity verification with tests
- Atomic commits (feature + removal + docs)
- FEATURE_COMPARISON.md updates
- Risk assessment before removal
- Documentation of differences

The goal: Clean codebase with no dead code accumulation.
