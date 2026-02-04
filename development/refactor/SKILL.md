---
name: refactor
description: Use during REFACTOR phase of TDD or when code duplication is suspected. Defines search-first workflow and safe refactoring practices.
---

# Refactor Skill

This skill provides detailed guidance for the **REFACTOR** phase of the RED-GREEN-REFACTOR cycle in Test-Driven Development.

**When to use this skill:**
- After tests pass (GREEN phase complete)
- When code duplication is identified
- Before implementing new features that may duplicate existing patterns
- During code reviews to improve code quality

## Core Principle: Refactor-First Mindset

**Before writing new code, always ask:**
1. Does similar functionality already exist?
2. Can I refactor existing code to handle both cases?
3. What patterns or abstractions are already in use?
4. Would this be better as a modification to existing code?

## Refactoring Workflow

### Phase 1: Search for Existing Patterns

**CRITICAL: Always search before implementing new functionality**

Use code search tools to find:
- Similar function names or patterns
- Duplicate logic or algorithms
- Existing abstractions that could be extended
- Related utilities or helpers

**Search strategies:**
- Grep for similar function/method names
- Search for similar algorithm patterns
- Look for related types or interfaces
- Check for existing error handling patterns
- Search for similar data transformations

### Phase 2: Analyze Duplication

When similar code is found, evaluate:

**Questions to ask:**
- Is this duplication intentional or accidental?
- Do these implementations handle the same concept?
- Can they be unified without increasing complexity?
- Is there a common abstraction that emerges?

**Red flags for duplication:**
- Copy-pasted code with minor variations
- Similar logic in different locations
- Repeated error handling patterns
- Multiple implementations of same algorithm
- Similar data validation or transformation logic

### Phase 3: Choose Refactoring Strategy

Based on the duplication analysis, choose appropriate strategy:

**1. Extract Function/Method**
- When: Same code block appears multiple times
- Action: Extract to shared function
- Benefit: Single source of truth

**2. Parameterize Function**
- When: Similar functions with minor variations
- Action: Add parameters to handle variations
- Benefit: Reduces function count

**3. Extract Common Interface/Trait**
- When: Multiple types share similar behavior
- Action: Define shared interface
- Benefit: Polymorphic usage

**4. Introduce Abstraction Layer**
- When: Complex logic duplicated across features
- Action: Create abstraction that handles complexity
- Benefit: Simpler calling code

**5. Use Existing Abstraction**
- When: Functionality fits existing abstraction
- Action: Extend or modify existing abstraction
- Benefit: Consistency with codebase patterns

**6. Keep Duplication**
- When: Concepts are fundamentally different despite similar code
- When: Unification would increase coupling inappropriately
- When: Code will diverge in future
- Action: Document why duplication is intentional
- Benefit: Avoids premature abstraction

### Phase 4: Refactor Safely

**Safety rules for refactoring:**

1. **All tests must be GREEN before starting**
   - Never refactor with failing tests
   - Tests are your safety net

2. **Make small, incremental changes**
   - One refactoring at a time
   - Run tests after each change
   - Commit frequently

3. **Run ALL tests after each change**
   - Ensures no regression
   - Catches unintended side effects
   - Maintains confidence

4. **If tests fail, revert immediately**
   - Don't try to fix forward
   - Revert and try different approach
   - Smaller steps if needed

5. **Keep refactoring separate from feature work**
   - Don't mix refactoring and new features in same commit
   - Refactoring commits should not change behavior
   - Feature commits add new behavior

### Phase 5: Verify and Document

After refactoring:

**Verification checklist:**
- [ ] All tests still pass
- [ ] No new compiler warnings
- [ ] Code is more readable
- [ ] Duplication is reduced or eliminated
- [ ] Performance is not degraded
- [ ] Documentation is updated

**Documentation:**
- Update function/module documentation
- Add comments explaining complex refactorings
- Document design decisions (especially if keeping duplication)
- Update architecture diagrams if needed

## Refactoring Anti-Patterns

### ❌ Anti-Pattern 1: Premature Abstraction
**Problem:** Creating abstractions before understanding the pattern
**Solution:** Follow "rule of three" - wait until duplication appears 3 times

### ❌ Anti-Pattern 2: Over-Engineering
**Problem:** Creating overly complex abstractions for simple duplication
**Solution:** Keep refactoring simple and focused

### ❌ Anti-Pattern 3: Breaking Encapsulation
**Problem:** Exposing internals to reduce duplication
**Solution:** Sometimes duplication is better than bad coupling

### ❌ Anti-Pattern 4: Big Bang Refactoring
**Problem:** Changing too much at once
**Solution:** Small, incremental changes with test verification

### ❌ Anti-Pattern 5: Refactoring Without Tests
**Problem:** Changing code without safety net
**Solution:** Write tests first if they don't exist

## When NOT to Refactor

**Skip refactoring when:**
- Tests are not passing (fix tests first)
- Code will be deleted soon
- Time pressure is extreme (but add TODO)
- Concepts are fundamentally different despite similar code
- System is stable and working (if it ain't broke...)
- Refactoring would introduce inappropriate coupling

## Integration with TDD Workflow

Refactoring is **Step 4** in the RED-GREEN-REFACTOR cycle:

1. **RED**: Write test that fails
2. **GREEN**: Write minimal code to pass
3. **VERIFY**: Run all tests
4. **REFACTOR**: Improve code quality ← (this skill)
5. **VERIFY**: Run all tests again
6. **REPEAT**: Next test

**When implementing new features:**
1. Search for existing similar patterns (use this skill)
2. Decide: refactor existing vs. create new
3. If refactoring: do it before adding new feature
4. Then proceed with TDD cycle for new feature

## File Organization

**For guidance on splitting large files into modules:**
See [FILE-ORGANIZATION.md](FILE-ORGANIZATION.md) for guidelines on when and how to split files.

## Practical Checklist

Before writing new code:
- [ ] Search codebase for similar functionality
- [ ] Review existing abstractions in the area
- [ ] Check if existing code can be extended
- [ ] Consider refactoring existing code first
- [ ] Document decision (refactor vs. new code)

During refactoring:
- [ ] All tests passing before starting
- [ ] Make one small change at a time
- [ ] Run all tests after each change
- [ ] Commit working changes frequently
- [ ] Revert if tests fail

After refactoring:
- [ ] All tests still passing
- [ ] Code is more maintainable
- [ ] Duplication reduced or eliminated
- [ ] Documentation updated
- [ ] No performance regression
