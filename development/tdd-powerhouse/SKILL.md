---
name: tdd-powerhouse
description: Complete Test-Driven Development workflow combining Sherpa guidance, Julie code intelligence, and Goldfish progress tracking. Automatically activates for feature implementation with systematic phases, semantic code search, and persistent checkpointing. Use when implementing new features with test-first discipline.
allowed-tools: mcp__sherpa__guide, mcp__sherpa__approach, mcp__julie__fast_search, mcp__julie__get_symbols, mcp__julie__fast_refs, mcp__julie__rename_symbol, mcp__goldfish__recall, mcp__goldfish__checkpoint, mcp__goldfish__plan, Read, Edit, Write, Bash
---

# TDD Powerhouse Workflow

## Purpose
Orchestrate **complete Test-Driven Development** using all three MCP tools in harmony. This is the ultimate systematic development workflow combining behavioral guidance, code intelligence, and persistent memory.

## When to Activate
Use when the user:
- **Implements new features**: "build payment processing", "add user authentication"
- **Wants TDD discipline**: "use TDD", "test-first development"
- **Builds from scratch**: "create a new service", "implement new API"
- **Emphasizes quality**: "build this right", "with proper tests"

## The Powerhouse Trinity

### 🧭 Sherpa - Workflow Guidance
- Guides through TDD phases
- Celebrates progress
- Tracks milestones
- Builds systematic habits

### 🔍 Julie - Code Intelligence
- Semantic search for patterns
- Symbol navigation
- Safe refactoring
- Token-efficient exploration

### 💾 Goldfish - Persistent Memory
- Checkpoints after each phase
- Survives context resets
- Tracks long-term work
- Documents decisions

## TDD Powerhouse Orchestration

### Session Start: Context Restoration
```
1. Goldfish recall() → Restore previous session
2. Check for active TDD plan
3. If plan exists → Resume where left off
4. If new work → Create plan and start fresh
```

### Phase 1: 📋 Define Contract

**Sherpa Activation:**
```
approach({ workflow: "tdd" })
guide() → "Phase 1: Define Contract - Design interfaces first"
```

**Julie Intelligence:**
```
fast_search({ query: "similar [feature] patterns", mode: "semantic" })
→ Find existing code with similar functionality
get_symbols on relevant files → See structure without reading all
→ Learn from existing patterns
```

**Design Work:**
- Define interfaces and types based on patterns
- Specify method signatures
- Document expected behavior

**Goldfish Checkpoint:**
```
checkpoint({
  description: "Designed [Feature]Interface with [N] methods based on [Pattern]",
  tags: ["tdd", "design", "phase-1"]
})
```

**Sherpa Progress:**
```
guide({ done: "designed complete interface for [feature]" })
→ Celebrates design, moves to Phase 2
```

### Phase 2: ✅ Write Tests

**Sherpa Guidance:**
```
guide() → "Phase 2: Write Tests - Comprehensive suite BEFORE implementation"
```

**Julie Intelligence:**
```
fast_search({ query: "[feature] test examples", mode: "semantic" })
→ Find similar test patterns
get_symbols on test files → See test structure
→ Learn testing patterns
```

**Test Writing:**
- Write comprehensive test cases
- Cover happy paths, edge cases, errors
- Ensure tests fail for right reasons

**Goldfish Checkpoint:**
```
checkpoint({
  description: "Wrote [N] comprehensive tests for [feature]: [list key scenarios]",
  tags: ["tdd", "tests", "phase-2"]
})
```

**Sherpa Progress:**
```
guide({ done: "wrote [N] test cases covering all [feature] scenarios" })
→ Celebrates test discipline: "🎉 Outstanding test coverage!"
→ Moves to Phase 3
```

### Phase 3: 🚀 Implement

**Sherpa Guidance:**
```
guide() → "Phase 3: Implementation - Make those tests green!"
```

**Julie Intelligence:**
```
get_symbols on related files → Understand structure
fast_refs({ symbol: "dependencies" }) → See how to use dependencies
→ Implement with confidence
```

**Implementation:**
- Write minimal code to pass tests
- Run tests frequently
- See tests turn green one by one

**Goldfish Checkpoint:**
```
checkpoint({
  description: "Implemented [feature], all [N] tests passing",
  tags: ["tdd", "implementation", "phase-3", "tests-green"]
})
```

**Sherpa Progress:**
```
guide({ done: "implemented [feature], all tests passing" })
→ Celebrates success: "🏆 All green! Beautiful work!"
→ Moves to Phase 4
```

### Phase 4: ✨ Refactor

**Sherpa Guidance:**
```
guide() → "Phase 4: Refactor - Improve code while tests stay green"
```

**Julie Safe Refactoring:**
```
fast_refs({ symbol: "oldName" }) → Check impact before rename
rename_symbol({ old_name: "oldName", new_name: "betterName" })
→ Workspace-wide safe rename

fuzzy_replace for targeted improvements
→ Keep tests green throughout
```

**Refactoring:**
- Improve code quality
- Remove duplication
- Enhance readability
- Tests protect you!

**Goldfish Checkpoint:**
```
checkpoint({
  description: "Refactored [feature]: extracted [Helper], improved naming, tests still green",
  tags: ["tdd", "refactor", "phase-4", "complete"]
})
```

**Sherpa Completion:**
```
guide({ done: "refactoring complete, all tests green, code clean" })
→ Celebrates completion: "🌟 TDD Workflow Complete! Clean code, solid tests!"
→ Potential milestone: "🏆 Milestone: TDD Mastery!"
```

**Goldfish Plan Update:**
```
plan({
  action: "update",
  id: "[feature-plan]",
  content: "TDD phase complete for [feature]. All tests green, code refactored."
})
```

## Complete Example: Payment Processing

```markdown
User: "Implement Stripe payment processing"

=== SESSION START ===

→ Goldfish: recall()
  No previous work on payments. Starting fresh.

→ Goldfish: plan({
    action: "save",
    title: "Payment Processing Implementation",
    content: "Implement Stripe payment processing with TDD..."
  })

→ Sherpa: approach({ workflow: "tdd" })
  🎯 TDD Workflow activated!

=== PHASE 1: DEFINE CONTRACT ===

→ Sherpa: guide()
  "Phase 1: Define Contract"

→ Julie: fast_search({ query: "payment service interface patterns", mode: "semantic" })
  Found: similar payment interfaces in other services

→ Julie: get_symbols({ file: "src/services/order-service.ts", mode: "structure" })
  See similar service pattern

→ Design PaymentService interface based on patterns:
  - charge(amount, token)
  - refund(paymentId)
  - getStatus(paymentId)

→ Goldfish: checkpoint({
    description: "Designed PaymentService interface with charge, refund, getStatus methods",
    tags: ["tdd", "design", "phase-1", "payment"]
  })

→ Sherpa: guide({ done: "designed complete PaymentService interface" })
  ✨ "Excellent contract design! Moving to Phase 2: Write Tests"

=== PHASE 2: WRITE TESTS ===

→ Sherpa: guide()
  "Write comprehensive tests BEFORE implementation"

→ Julie: fast_search({ query: "service test examples", mode: "semantic" })
  Found: test patterns in existing services

→ Write 12 test cases:
  - Successful charge
  - Failed charge (invalid card)
  - Refund operations
  - Status checking
  - Error handling
  - Edge cases (negative amounts, etc.)

→ Run tests → All fail (expected!)

→ Goldfish: checkpoint({
    description: "Wrote 12 comprehensive payment tests: charge success/failure, refunds, validation",
    tags: ["tdd", "tests", "phase-2", "payment"]
  })

→ Sherpa: guide({ done: "wrote 12 test cases covering all payment scenarios" })
  🎉 "Outstanding test coverage! 12 comprehensive tests!"
  "Phase 3: Implementation"

=== PHASE 3: IMPLEMENT ===

→ Sherpa: guide()
  "Now make those tests green!"

→ Julie: get_symbols({ file: "src/services/user-service.ts" })
  Understand service structure pattern

→ Implement PaymentService:
  - Integrate Stripe SDK
  - Implement charge method
  - Implement refund method
  - Handle errors gracefully

→ Run tests → All green! ✅

→ Goldfish: checkpoint({
    description: "Implemented PaymentService with Stripe integration, all 12 tests passing",
    tags: ["tdd", "implementation", "phase-3", "payment", "tests-green"]
  })

→ Sherpa: guide({ done: "implemented payment service, all 12 tests passing" })
  🏆 "All green! Beautiful work!"
  "Phase 4: Refactor"

=== PHASE 4: REFACTOR ===

→ Sherpa: guide()
  "Polish your code while tests stay green"

→ Julie: fast_refs({ symbol: "stripeClient" })
  Used in multiple places - extract to shared utility

→ Julie: fuzzy_replace to extract StripeClient helper
  Tests still green ✅

→ Julie: rename_symbol({ old_name: "processCharge", new_name: "executeCharge" })
  Better naming, workspace-wide update

→ Improve error messages
→ Add JSDoc comments
→ Tests still green ✅

→ Goldfish: checkpoint({
    description: "Refactored PaymentService: extracted StripeClient helper, improved naming and error handling, all tests green",
    tags: ["tdd", "refactor", "phase-4", "payment", "complete"]
  })

→ Sherpa: guide({ done: "refactoring complete, all tests green, code clean and documented" })
  🌟 "TDD Workflow Complete! Clean code, solid tests!"
  🏆 "Milestone: First TDD Workflow Complete!"

→ Goldfish: plan({
    action: "update",
    id: "payment-processing",
    content: "✅ TDD complete for PaymentService. 12 tests passing, code refactored and documented."
  })

=== RESULT ===

PaymentService implemented with TDD discipline:
- ✅ Clean interface design
- ✅ 12 comprehensive tests
- ✅ Solid implementation
- ✅ Refactored and documented
- ✅ All tests green
- ✅ Progress tracked and checkpointed
```

## Integration Patterns

### Continuous Checkpointing
```
After EVERY phase → Goldfish checkpoint
- Captures progress
- Survives context resets
- Documents decision trail
```

### Guided Search
```
Before design/implementation → Julie semantic search
- Find similar patterns
- Learn from existing code
- Don't reinvent the wheel
```

### Systematic Guidance
```
Throughout workflow → Sherpa guide
- Clear next steps
- Progress celebration
- Milestone tracking
```

## Key Behaviors

### ✅ DO
- Recall at session start (mandatory)
- Activate TDD workflow explicitly
- Search for patterns before designing
- Checkpoint after EACH phase
- Use Julie for token-efficient exploration
- Let Sherpa guide and celebrate
- Update plan at completion

### ❌ DON'T
- Skip phases (Sherpa will guide you back)
- Write implementation before tests
- Forget to checkpoint progress
- Ignore existing code patterns
- Read entire files (use get_symbols!)
- Skip celebration (Sherpa builds habits!)

## Success Criteria

TDD Powerhouse succeeds when:
- All four phases completed systematically
- Tests written before implementation
- All tests green before refactoring
- Progress checkpointed throughout
- Code follows existing patterns
- User builds TDD muscle memory
- Work survives context resets

## Performance

Total workflow:
- Pattern search: ~100-200ms (Julie semantic)
- Phase guidance: ~50ms (Sherpa)
- Checkpoints: ~10ms each (Goldfish)
- Safe refactoring: ~200-500ms (Julie)

**Result:** Seamless orchestration, feels natural and fast!

---

**Remember:** TDD Powerhouse combines the best of all three tools. Sherpa guides, Julie finds patterns, Goldfish preserves. Together, they build test-first mastery!
