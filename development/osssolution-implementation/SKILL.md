---
name: oss:solution-implementation
description: Phase 3 of OSS contribution - Design and implement the solution following project standards and best practices. Writes code following conventions, adds/updates tests, handles edge cases. Use when issue analysis is complete and ready to write code.
---

# Phase 3: Solution Implementation

Design and implement the solution following project standards and best practices.

## Purpose

Transform the implementation plan into working code that:
- Solves the issue completely
- Follows project conventions
- Passes all tests
- Handles edge cases
- Is maintainable and reviewable

## When to Use

**Triggers:**
- "솔루션 구현"
- "이슈 해결 시작"
- "코드 작성"
- "테스트 작성"

**Use when:**
- Issue analysis (Phase 2) is complete
- Code locations identified
- Ready to write code
- Need implementation guidance
- Want to follow best practices

## Implementation Framework

### Step 0: CONTRIBUTING.md Compliance Check

**MANDATORY: Final verification before implementation**
- Review all CONTRIBUTING.md requirements from Phase 1
- Ensure implementation will follow:
  - Code style and formatting standards
  - Commit message format
  - Branch naming conventions
  - Testing requirements
  - Documentation standards
- **All code written MUST strictly follow these guidelines**

### Step 1: Implementation Planning

Plan your approach before writing code.

**Design decisions:**

```markdown
### Implementation Plan

**Approach:**
[High-level description of solution approach]

**Why this approach:**
1. [Reason 1: e.g., matches existing patterns]
2. [Reason 2: e.g., minimal invasive change]
3. [Reason 3: e.g., easily testable]

**Alternative approaches considered:**
- **[Approach A]:** [why not chosen]
- **[Approach B]:** [why not chosen]

**Implementation order:**
1. [Task 1] - [rationale for doing first]
2. [Task 2] - [builds on previous]
3. [Task 3] - [completes the feature]

**Checkpoints:**
- After step 1: [what to verify]
- After step 2: [what to verify]
- After step 3: [final verification]
```

### Step 2: Test-Driven Development (TDD)

Start with tests when possible.

**TDD workflow:**

1. **Write failing test:**
   - Captures the requirement
   - Specific and focused
   - Fails for right reason

2. **Implement minimal solution:**
   - Make test pass
   - No premature optimization
   - Follow existing patterns

3. **Refactor:**
   - Clean up code
   - Extract duplications
   - Improve readability
   - Tests still pass

**When TDD makes sense:**
- Bug fixes (test reproduces bug)
- New utility functions
- Clear acceptance criteria
- Well-understood requirements

**When to code first:**
- Exploratory work
- UI/UX iteration
- Complex interactions
- Unclear requirements

**Test-first template:**

```markdown
### TDD Cycle

**Red (Failing Test):**
```javascript
// test/feature.test.js
describe('NewFeature', () => {
  it('should do X when Y', () => {
    const result = newFeature(input)
    expect(result).toBe(expected) // ❌ FAILS
  })
})
```

**Green (Minimal Implementation):**
```javascript
// src/feature.js
function newFeature(input) {
  // Simplest thing that makes test pass
  return expected
}
```

**Refactor (Clean Up):**
```javascript
// src/feature.js
function newFeature(input) {
  // Proper implementation
  // Handles edge cases
  // Clean and readable
  return properResult
}
```

**Verify:** All tests pass ✅
```

### Step 3: Code Implementation

Write production code following project conventions.

**Quality checklist:**

```markdown
### Code Quality

**Correctness:**
- [ ] Solves the stated problem
- [ ] Handles all requirements
- [ ] Covers edge cases
- [ ] No logical errors

**Convention adherence:**
- [ ] Naming matches project style
- [ ] Formatting follows guidelines
- [ ] Imports organized correctly
- [ ] Comments where helpful

**Code quality:**
- [ ] DRY (Don't Repeat Yourself)
- [ ] Single Responsibility Principle
- [ ] Appropriate abstractions
- [ ] Clear variable/function names

**Error handling:**
- [ ] Validates inputs
- [ ] Handles errors gracefully
- [ ] Provides clear error messages
- [ ] Fails safely

**Performance:**
- [ ] No obvious inefficiencies
- [ ] Appropriate data structures
- [ ] Avoids unnecessary work
- [ ] Acceptable time/space complexity

**Security:**
- [ ] Input validation
- [ ] No injection vulnerabilities
- [ ] Proper authorization checks
- [ ] Sensitive data protection
```

**Implementation patterns:**

**For Bug Fixes:**
```markdown
### Bug Fix Implementation

**1. Add test that reproduces bug:**
```javascript
it('should handle edge case correctly', () => {
  // This test currently fails
  const result = buggyFunction(edgeCase)
  expect(result).toBe(correctValue)
})
```

**2. Locate root cause:**
- Function: `[name]` @ [file:line]
- Problem: [what's wrong]
- Why it happens: [explanation]

**3. Implement fix:**
```javascript
// Before:
function buggyFunction(input) {
  return input.value // Fails when input.value is undefined
}

// After:
function buggyFunction(input) {
  return input?.value ?? defaultValue // Handles undefined
}
```

**4. Verify:**
- [ ] New test passes
- [ ] Existing tests pass
- [ ] Manual testing confirms fix
```

**For Features:**
```markdown
### Feature Implementation

**1. Define interface:**
```typescript
// Define types/interfaces first
interface NewFeature {
  doSomething(param: Type): ReturnType
}
```

**2. Implement core logic:**
```javascript
function coreFunction() {
  // Happy path first
  // Clear, readable code
  // One level of abstraction
}
```

**3. Handle edge cases:**
```javascript
function coreFunction(input) {
  // Validate inputs
  if (!isValid(input)) {
    throw new Error('Invalid input: ...')
  }

  // Handle empty/null
  if (isEmpty(input)) {
    return defaultValue
  }

  // Core logic
  const result = process(input)

  // Post-conditions
  validateResult(result)

  return result
}
```

**4. Add tests for each path:**
- [ ] Happy path
- [ ] Edge cases
- [ ] Error cases
```

**For Refactoring:**
```markdown
### Refactoring Implementation

**1. Ensure test coverage:**
- [ ] Tests exist for current behavior
- [ ] Tests are comprehensive
- [ ] Tests pass before refactoring

**2. Refactor incrementally:**

**Step 1:** Extract function
```javascript
// Before:
function complexFunction() {
  // Long complex code
  // Mixing concerns
  // Hard to understand
}

// After Step 1:
function complexFunction() {
  const data = fetchData()
  const processed = processData(data)
  return formatOutput(processed)
}

function fetchData() { /* extracted */ }
function processData(data) { /* extracted */ }
function formatOutput(processed) { /* extracted */ }
```

**Step 2:** Improve naming
**Step 3:** Remove duplication
**Step 4:** Simplify logic

**After each step:**
- [ ] Tests still pass
- [ ] Code is more readable
- [ ] Behavior unchanged
```

### Step 4: Test Implementation

Write comprehensive tests.

**Test coverage goals:**

```markdown
### Test Strategy

**Unit tests:** (test individual functions)
- Location: [where tests go]
- Coverage target: [percentage or specific cases]

**Test cases:**

**Happy path:**
```javascript
it('should work with valid input', () => {
  expect(feature(validInput)).toBe(expected)
})
```

**Edge cases:**
```javascript
it('should handle empty input', () => {
  expect(feature([])).toBe(defaultValue)
})

it('should handle null input', () => {
  expect(feature(null)).toThrow('Invalid input')
})

it('should handle large input', () => {
  const largeInput = generateLargeData()
  expect(feature(largeInput)).toBeDefined()
})
```

**Error cases:**
```javascript
it('should throw on invalid input', () => {
  expect(() => feature(invalid)).toThrow()
})

it('should provide clear error message', () => {
  expect(() => feature(invalid))
    .toThrow('Expected X but got Y')
})
```

**Integration tests:** (if needed)
```javascript
it('should integrate with existing feature', () => {
  // Test feature working with other parts
})
```

**Snapshot tests:** (for UI, if applicable)
```javascript
it('should render correctly', () => {
  const tree = renderer.create(<Component />).toJSON()
  expect(tree).toMatchSnapshot()
})
```
```

**Test best practices:**

```markdown
### Test Quality

**Clear and focused:**
- [ ] One assertion per test (generally)
- [ ] Clear test names describe behavior
- [ ] Tests are independent
- [ ] No test interdependencies

**Readable:**
- [ ] Arrange-Act-Assert structure
- [ ] Descriptive variable names
- [ ] Comments for complex setups
- [ ] DRY (use helpers/fixtures)

**Maintainable:**
- [ ] Tests don't test implementation details
- [ ] Tests are resilient to refactoring
- [ ] Test data is realistic
- [ ] Mocks/stubs are minimal

**Fast:**
- [ ] Unit tests run quickly
- [ ] Minimal external dependencies
- [ ] No unnecessary setup/teardown
```

### Step 5: Local Verification

Test thoroughly before committing.

**Verification checklist:**

```markdown
### Local Testing

**Build:**
```bash
# Clean build
[build command]

# Check for warnings
[any warnings to address?]
```

**Tests:**
```bash
# Run all tests
[test command]
# ✅ All pass

# Run with coverage
[coverage command]
# ✅ Coverage meets threshold

# Run specific affected tests
[command for affected tests]
# ✅ Pass
```

**Linting:**
```bash
# Check code style
[lint command]
# ✅ No errors

# Auto-fix if available
[format command]
```

**Type checking (if applicable):**
```bash
[type check command]
# ✅ No type errors
```

**Manual testing:**
- [ ] Feature works as expected
- [ ] Edge cases handled
- [ ] Error messages clear
- [ ] UI looks correct (if applicable)
- [ ] Performance acceptable

**Regression check:**
- [ ] Existing features still work
- [ ] No unintended side effects
- [ ] Related functionality intact
```

### Step 6: Code Review Self-Check

Review your own code before submitting.

**Self-review checklist:**

```markdown
### Self Code Review

**Completeness:**
- [ ] All requirements implemented
- [ ] All edge cases handled
- [ ] All acceptance criteria met
- [ ] No TODO/FIXME left unaddressed

**Code quality:**
- [ ] Code is self-explanatory
- [ ] Complex parts have comments
- [ ] No dead code or commented-out code
- [ ] No debugging code (console.log, etc)

**Changes are minimal:**
- [ ] Only changed what's necessary
- [ ] No unrelated refactoring
- [ ] No formatting-only changes mixed in
- [ ] Git diff is clean and focused

**Testing:**
- [ ] Tests are comprehensive
- [ ] Tests are meaningful (not just for coverage)
- [ ] Tests pass consistently
- [ ] Edge cases have tests

**Documentation:**
- [ ] Public APIs documented
- [ ] Complex logic explained
- [ ] README updated if needed
- [ ] Migration guide if breaking

**Security:**
- [ ] No secrets/credentials committed
- [ ] User input validated
- [ ] No obvious vulnerabilities
- [ ] Dependencies are safe

**Performance:**
- [ ] No performance regressions
- [ ] Algorithms are efficient
- [ ] Resource usage reasonable
- [ ] No memory leaks

**Commits:**
- [ ] Commits are logical
- [ ] Commit messages are clear
- [ ] No merge commits from main (rebase if needed)
- [ ] History is clean
```

### Step 7: Documentation

Document your changes appropriately.

**Documentation types:**

```markdown
### Documentation Updates

**Code comments:**
```javascript
/**
 * Converts user data to CSV format
 *
 * @param {User[]} users - Array of user objects
 * @param {ExportOptions} options - Export configuration
 * @returns {string} CSV formatted string
 * @throws {ValidationError} If users array is invalid
 *
 * @example
 * const csv = exportToCSV(users, { includeHeaders: true })
 */
function exportToCSV(users, options) {
  // Implementation
}
```

**README updates:**
- [ ] New features documented
- [ ] Usage examples added
- [ ] Installation steps updated
- [ ] API changes reflected

**CHANGELOG:**
- [ ] Entry added with:
  - Version (if applicable)
  - Date
  - Type: [Added/Changed/Fixed/Removed]
  - Description

```markdown
## [Unreleased]
### Added
- Export to CSV functionality (#123)
  - New `exportToCSV` function
  - Customizable column selection
  - Header row optional
```

**API documentation:**
- [ ] New endpoints documented
- [ ] Parameters described
- [ ] Response format specified
- [ ] Error codes listed
- [ ] Examples provided

**Migration guide (if breaking):**
```markdown
## Migrating to v2.0

### Breaking Changes

**Function signature changed:**
```javascript
// Old:
doSomething(param)

// New:
doSomething(param, options)
```

**Migration steps:**
1. Find all calls to `doSomething`
2. Add empty options object: `doSomething(param, {})`
3. Configure options as needed
```
```

## Implementation Best Practices

**Start small:**
- Implement core functionality first
- Add features incrementally
- Test each increment
- Commit working states

**Follow patterns:**
- Match existing code style
- Use same abstractions
- Don't introduce new paradigms
- Be consistent

**Communicate:**
- Ask questions early
- Share progress on complex issues
- Discuss tradeoffs
- Welcome feedback

**Iterate:**
- Don't aim for perfection first try
- Reviewers will have feedback
- Be open to changes
- Learn from reviews

## Common Pitfalls

**Avoid:**

❌ **Scope creep** - Stick to issue requirements
❌ **Over-engineering** - Keep it simple
❌ **Ignoring conventions** - Match project style
❌ **Skipping tests** - Tests are requirements
❌ **Poor commit messages** - Future you will be confused
❌ **Not testing edge cases** - Where bugs hide
❌ **Mixing concerns** - One logical change per commit
❌ **Committing secrets** - Check before pushing

## Output Format

Provide implementation summary:

```markdown
# ✅ Implementation Complete: [Issue Title]

**Issue:** #[number]
**Branch:** [branch-name]

---

## Changes Made

### Core Implementation

**1. [Primary change]**
- File: `[path]`
- Changes: [description]
- Lines modified: ~[count]

**2. [Secondary change]**
- File: `[path]`
- Changes: [description]

### Tests Added

**Unit tests:**
- `[test-file]` - [N] test cases
  - Happy path
  - Edge cases: [list]
  - Error cases: [list]

**Coverage:** [percentage] (previous: [X]%, delta: +[Y]%)

### Documentation

- [ ] Code comments added
- [ ] README updated
- [ ] CHANGELOG entry added
- [ ] API docs updated

---

## Verification

**Local testing:**
- ✅ All tests pass
- ✅ Linting passes
- ✅ Build succeeds
- ✅ Manual testing complete

**Checklist:**
- ✅ Requirements met
- ✅ Edge cases handled
- ✅ Follows conventions
- ✅ Self-review complete

---

## Commits

```bash
# Commit history
git log --oneline origin/main..HEAD
```

**Summary:**
- [N] commits
- All commits are focused and logical
- Commit messages are clear

---

## Next Steps

✅ Implementation complete - Ready for **Phase 4: Documentation & PR**

**Before PR:**
- [ ] Final review
- [ ] Rebase on main (if needed)
- [ ] Squash commits (if needed)
- [ ] Push to remote
```

## Integration with Main Framework

When invoked from main framework:

1. **Receive context:** Issue analysis from Phase 2, requirements, code locations
2. **Guide implementation:** Step-by-step with quality checks
3. **Verify completion:** All requirements met, tests pass
4. **Return summary:** What was implemented and how
5. **Update tracker:** Mark Phase 3 complete
6. **Transition:** Ready for documentation and PR creation

Implementation phase may iterate with Phase 2 if code structure different than expected.

## Incremental Development

**For large implementations:**

1. **Milestone 1:** Core functionality
   - Implement minimal working version
   - Add basic tests
   - Commit: "feat: add core X functionality"

2. **Milestone 2:** Edge cases
   - Handle edge cases
   - Add edge case tests
   - Commit: "feat: handle X edge cases"

3. **Milestone 3:** Polish
   - Error messages
   - Documentation
   - Commit: "docs: add X documentation"

**Benefits:**
- Can get early feedback
- Easier to review
- Simpler to debug
- Clear progress tracking
