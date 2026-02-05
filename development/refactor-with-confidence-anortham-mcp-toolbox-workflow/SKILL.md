---
name: refactor-with-confidence
description: Safe code refactoring combining Sherpa's refactor workflow, Julie's reference checking and safe renaming, and Goldfish's before/after checkpointing. Activates for code improvement with systematic testing, refactoring, and verification. Use when cleaning up or improving existing code.
allowed-tools: mcp__sherpa__guide, mcp__sherpa__approach, mcp__julie__fast_refs, mcp__julie__rename_symbol, mcp__julie__fuzzy_replace, mcp__julie__get_symbols, mcp__goldfish__checkpoint, Read, Edit, Write, Bash
---

# Refactor with Confidence Workflow

## Purpose
Perform **safe, systematic code refactoring** with test protection and full tracking. Combines Sherpa's refactor workflow guidance, Julie's safe refactoring tools, and Goldfish's before/after state preservation.

## When to Activate
- "refactor this code", "cleanup", "improve code quality"
- "reorganize", "simplify", "optimize"
- "extract", "rename", "restructure"

## Trinity for Safe Refactoring

**Sherpa:** Guides refactor phases (Tests → Refactor → Verify)
**Julie:** Safe renames, reference checking, impact analysis
**Goldfish:** Pre/post state checkpoints, decision tracking

## Orchestration

### Pre-Refactor: Baseline State
```
1. Goldfish: checkpoint({ description: "Pre-refactor baseline: [current state]" })
2. Sherpa: approach({ workflow: "refactor" })
3. Julie: get_symbols → Capture current structure
```

### Phase 1: Tests First (Sherpa)
```
guide() → "Ensure test coverage exists"

Check existing tests:
- Run test suite
- Verify coverage for code being refactored
- Add missing tests if needed

checkpoint({ description: "Verified test coverage for [component]" })
guide({ done: "test coverage verified" })
```

### Phase 2: Refactor Code (Julie + Sherpa)
```
guide() → "Refactor while staying green"

Julie safe refactoring:
- fast_refs → Check all references before rename
- rename_symbol → Workspace-wide safe rename
- fuzzy_replace → Targeted improvements
- Tests stay green throughout!

checkpoint({ description: "Refactored: [specific changes made]" })
guide({ done: "refactoring complete, tests still green" })
```

### Phase 3: Verify (Sherpa + Goldfish)
```
guide() → "Verify no regressions"

Verification:
- Run full test suite → All green
- get_symbols → Verify structure
- fast_refs → Check updated references

checkpoint({ description: "Refactor verified: all tests pass, [N] files updated" })
guide({ done: "verified refactor, all tests pass" })
```

## Example: Extract Helper Class

```markdown
User: "This UserService is too big, extract validation logic"

PRE-REFACTOR:
→ checkpoint({ description: "Pre-refactor: UserService 487 lines with inline validation" })
→ approach({ workflow: "refactor" })

PHASE 1: TESTS
→ guide()
→ Run tests → 23 tests pass ✅
→ checkpoint({ description: "Verified UserService has 23 passing tests" })

PHASE 2: REFACTOR
→ guide()
→ Julie: Create UserValidator class
→ Julie: fuzzy_replace to extract validation methods
→ Julie: rename_symbol to update references
→ Tests → 23 tests still pass ✅
→ checkpoint({ description: "Extracted UserValidator class, UserService now 312 lines" })

PHASE 3: VERIFY
→ guide()
→ fast_refs({ symbol: "UserService" }) → All references updated
→ get_symbols → Structure cleaner
→ Full test suite → 23 tests pass ✅
→ checkpoint({ description: "Refactor complete: UserService 312 lines, UserValidator 175 lines, all 23 tests pass" })

Result: Clean separation, all tests green, tracked in Goldfish!
```

## Key Behaviors

**✅ DO:**
- Checkpoint before and after
- Ensure tests exist first
- Use Julie's safe tools
- Keep tests green throughout
- Verify all references updated

**❌ DON'T:**
- Refactor without tests
- Skip reference checking
- Break tests during refactoring
- Forget final verification

---

**Safe refactoring: Test → Refactor → Verify. Sherpa guides, Julie protects, Goldfish preserves!**
