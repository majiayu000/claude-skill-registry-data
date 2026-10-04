---
name: "Role: Testing Obsessive"
description: "Pragmatic testing with Vitest: risk-based strategy, Svelte component testing, test-after development."
when_to_use: "When writing or reviewing tests, or deciding what's worth testing at all; fires on test coverage, Vitest setup and 'should I test this'."
user-invocable: false
metadata:
  family: clod-role
# No paths gate: the "should I test this at all?" moment happens while writing
# source, when no test file exists yet to match a glob
allowed-tools:
  - Read
  - Glob
  - Grep
  - "Bash(npm:*)"
  - "Bash(bun:*)"
  - "Bash(pnpm:*)"
  - "Bash(deno:*)"
  - "Bash(vitest:*)"
---

# Testing Foundations

Comprehensive testing guidance for JavaScript/TypeScript applications, with emphasis on Vitest, Svelte component testing and pragmatic test-after development. Addresses testing as a professional skill for code quality.

## When This Skill Applies

Use this skill when:
- Writing new tests for features or components
- Setting up testing infrastructure
- Debugging failing tests
- Discussing testing strategies or coverage goals
- Refactoring tests for better maintainability
- Questions about testing best practices
- Deciding what to test and when

## Testing Philosophy

### Why Test?

**Not for 100% coverage** - Test for:
1. **Confidence** - Deploy without fear
2. **Documentation** - Tests show how code should be used
3. **Refactoring safety** - Change implementation without breaking behaviour
4. **Regression prevention** - Bugs stay fixed
5. **Design feedback** - Hard-to-test code often signals design issues

### The Testing Pyramid
```
       /\
      /  \     E2E Tests
     /    \    (Few, slow, expensive)
    /------\
   /        \  Integration Tests
  /          \ (Some, medium speed)
 /------------\
/              \ Unit Tests
----------------  (Many, fast, cheap)
```

**Shape, not a quota**: unit tests stay cheapest and most numerous for genuinely isolated logic, but CLAUDE.md's own preference for integration tests on critical paths over exhaustive unit coverage governs the actual split. Don't count towards a percentage; let the risk assessment below decide what gets covered and at which layer.

### Pragmatic Approach

**Test-after development workflow**:
1. Implement working feature
2. Manual verification
3. Assess risk (see Risk-Based Testing)
4. Write automated tests for high/medium risk code
5. Refactor with test safety net

This approach:
- Lets you prototype quickly
- Tests based on real implementation
- Focuses effort where it matters
- Builds confidence incrementally

## Risk-Based Testing

**Prioritise testing based on risk assessment**

### Risk Dimensions

**Impact** - What breaks if this fails?
- Critical: Data loss, security breach, payment failures
- High: Core features broken, bad UX
- Medium: Minor features affected
- Low: Cosmetic issues

**Complexity** - How likely to have bugs?
- High: Complex algorithms, async logic, edge cases
- Medium: Standard business logic
- Low: Simple CRUD, straightforward functions

**Change Frequency** - How often modified?
- High: Rapidly evolving features
- Medium: Occasional updates
- Low: Set-and-forget code

### Testing Priority Matrix
```
HIGH PRIORITY (Must test):
✓ Payment/financial logic
✓ Authentication/authorization
✓ Data validation and persistence
✓ Critical user journeys
✓ Complex algorithms
✓ API integrations
✓ Security-sensitive code
✓ Accessibility requirements (keyboard nav, screen reader, contrast)

MEDIUM PRIORITY (Should test):
✓ Business logic with multiple branches
✓ Utility functions used across codebase
✓ Form validation
✓ Data transformations
✓ Error handling paths
✓ Frequently changed features

LOW PRIORITY (Optional):
- Simple getters/setters
- UI styling/layout
- Configuration files
- Straightforward CRUD operations
- One-time scripts
```

### Risk Assessment Example
```typescript
// HIGH RISK - Must test
// Impact: Critical (payments)
// Complexity: High (currency conversion, rounding)
// Change frequency: Medium
function calculateOrderTotal(items, discounts, taxRate) {
  // Complex calculation logic
  // Write comprehensive tests
}

// MEDIUM RISK - Should test
// Impact: Medium (UX issue if broken)
// Complexity: Medium (validation rules)
// Change frequency: Low
function validateEmail(email) {
  // Standard validation
  // Write basic tests
}

// LOW RISK - Optional
// Impact: Low (cosmetic)
// Complexity: Low (simple assignment)
// Change frequency: Low
function getUserDisplayName(user) {
  return user.name || user.email;
  // Can skip testing, or add simple test
}
```

## Test-After Development Workflow

### Step 1: Implement Feature

Focus on making it work:
- Write working code
- Manual testing in browser/console
- Get feedback from users/stakeholders
- Iterate on implementation

**Don't worry about tests yet** - understand the problem first.

### Step 2: Manual Verification

Test the feature manually:
- Happy path works
- Edge cases handled
- Error states graceful
- Performance acceptable

**Document interesting cases** - these become test scenarios.

### Step 3: Risk Assessment

Ask yourself:
- What's the impact if this breaks?
- How complex is this code?
- Will this change frequently?
- Are there edge cases I'm worried about?

**Use the priority matrix** to decide testing level.

### Step 4: Write Automated Tests

Based on risk assessment:

**High priority** - Comprehensive tests:
```typescript
describe('calculateOrderTotal', () => {
  it('should calculate total with single item');
  it('should apply percentage discount');
  it('should apply fixed discount');
  it('should calculate tax correctly');
  it('should handle multiple currencies');
  it('should round to 2 decimal places');
  it('should throw on negative prices');
  it('should handle empty cart');
});
```

**Medium priority** - Essential tests:
```typescript
describe('validateEmail', () => {
  it('should accept valid email');
  it('should reject invalid format');
  it('should reject missing domain');
});
```

**Low priority** - Skip or minimal:
```typescript
// Maybe one smoke test if you're feeling thorough
it('should return user name when available', () => {
  expect(getUserDisplayName({ name: 'Alice' })).toBe('Alice');
});
```

### Step 5: Refactor with Confidence

Now that tests exist:
- Optimise performance
- Improve code structure
- Rename variables
- Extract functions

**Tests catch regressions** while you improve code.

## Test-Driven Bug Fixing

When bugs are found, use this workflow:

### 1. Reproduce Bug

Write failing test that reproduces the issue:
```typescript
it('should handle empty cart without crashing', () => {
  // This currently fails
  const result = calculateOrderTotal([], [], 0.2);
  expect(result).toBe(0);
});
```

### 2. Fix Bug

Implement the fix:
```typescript
function calculateOrderTotal(items, discounts, taxRate) {
  if (items.length === 0) return 0; // Fix
  
  // Rest of logic...
}
```

### 3. Verify Test Passes

Run test suite, confirm:
- New test passes
- No regressions

### 4. Keep Test for Regression

This test now prevents the bug from returning.

**Benefits**:
- Documents bug fixes
- Builds test suite organically
- Prevents regression
- Forces you to understand the bug

## Additional resources

Mechanical how-to and reference material, loaded only when needed:

- [vitest-patterns.md](vitest-patterns.md): Vitest setup, unit/component/mocking/async test patterns, test organisation, coverage config, matcher and query quick reference
- [pitfalls-and-accessibility.md](pitfalls-and-accessibility.md): common testing mistakes (over-mocking, brittle selectors, implementation-detail testing) and accessibility test patterns
## Success Criteria

Tests are effective when they:
- Pass reliably (no flakiness)
- Run quickly (<1s for unit tests)
- Test behaviour, not implementation
- Catch real bugs before production
- Give confidence to refactor
- Focus on high-risk code
- Serve as documentation
- Reflect professional judgment about priorities
- Include accessibility checks for user-facing components
