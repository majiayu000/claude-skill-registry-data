---
name: avoiding-testing-anti-patterns
description: Use when writing or changing tests, adding mocks, or tempted to add test-only methods to production code - prevents testing mock behavior, production pollution with test-only methods, and mocking without understanding dependencies
---

# Testing Anti-Patterns

## Overview

Tests must verify real behavior, not mock behavior. Mocks are a means to isolate, not the thing being tested.

**Core principle:** Test what the code does, not what the mocks do.

**Following strict TDD prevents these anti-patterns.**

## The Iron Laws

```
1. NEVER test mock behavior
2. NEVER add test-only methods to production classes
3. NEVER mock without understanding dependencies
4. NEVER test implementation details - test user-visible behavior
5. NEVER ship UI without accessibility testing
6. NEVER test only happy path - test all UI states
```

## Anti-Pattern 1: Testing Mock Behavior

**The violation:**
```typescript
// ❌ BAD: Testing that the mock exists
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

**Why this is wrong:**
- You're verifying the mock works, not that the component works
- Test passes when mock is present, fails when it's not
- Tells you nothing about real behavior

**your human partner's correction:** "Are we testing the behavior of a mock?"

**The fix:**
```typescript
// ✅ GOOD: Test real component or don't mock it
test('renders sidebar', () => {
  render(<Page />);  // Don't mock sidebar
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});

// OR if sidebar must be mocked for isolation:
// Don't assert on the mock - test Page's behavior with sidebar present
```

### Gate Function

```
BEFORE asserting on any mock element:
  Ask: "Am I testing real component behavior or just mock existence?"

  IF testing mock existence:
    STOP - Delete the assertion or unmock the component

  Test real behavior instead
```

## Anti-Pattern 2: Test-Only Methods in Production

**The violation:**
```typescript
// ❌ BAD: destroy() only used in tests
class Session {
  async destroy() {  // Looks like production API!
    await this._workspaceManager?.destroyWorkspace(this.id);
    // ... cleanup
  }
}

// In tests
afterEach(() => session.destroy());
```

**Why this is wrong:**
- Production class polluted with test-only code
- Dangerous if accidentally called in production
- Violates YAGNI and separation of concerns
- Confuses object lifecycle with entity lifecycle

**The fix:**
```typescript
// ✅ GOOD: Test utilities handle test cleanup
// Session has no destroy() - it's stateless in production

// In test-utils/
export async function cleanupSession(session: Session) {
  const workspace = session.getWorkspaceInfo();
  if (workspace) {
    await workspaceManager.destroyWorkspace(workspace.id);
  }
}

// In tests
afterEach(() => cleanupSession(session));
```

### Gate Function

```
BEFORE adding any method to production class:
  Ask: "Is this only used by tests?"

  IF yes:
    STOP - Don't add it
    Put it in test utilities instead

  Ask: "Does this class own this resource's lifecycle?"

  IF no:
    STOP - Wrong class for this method
```

## Anti-Pattern 3: Mocking Without Understanding

**The violation:**
```typescript
// ❌ BAD: Mock breaks test logic
test('detects duplicate server', () => {
  // Mock prevents config write that test depends on!
  vi.mock('ToolCatalog', () => ({
    discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
  }));

  await addServer(config);
  await addServer(config);  // Should throw - but won't!
});
```

**Why this is wrong:**
- Mocked method had side effect test depended on (writing config)
- Over-mocking to "be safe" breaks actual behavior
- Test passes for wrong reason or fails mysteriously

**The fix:**
```typescript
// ✅ GOOD: Mock at correct level
test('detects duplicate server', () => {
  // Mock the slow part, preserve behavior test needs
  vi.mock('MCPServerManager'); // Just mock slow server startup

  await addServer(config);  // Config written
  await addServer(config);  // Duplicate detected ✓
});
```

### Gate Function

```
BEFORE mocking any method:
  STOP - Don't mock yet

  1. Ask: "What side effects does the real method have?"
  2. Ask: "Does this test depend on any of those side effects?"
  3. Ask: "Do I fully understand what this test needs?"

  IF depends on side effects:
    Mock at lower level (the actual slow/external operation)
    OR use test doubles that preserve necessary behavior
    NOT the high-level method the test depends on

  IF unsure what test depends on:
    Run test with real implementation FIRST
    Observe what actually needs to happen
    THEN add minimal mocking at the right level

  Red flags:
    - "I'll mock this to be safe"
    - "This might be slow, better mock it"
    - Mocking without understanding the dependency chain
```

## Anti-Pattern 4: Incomplete Mocks

**The violation:**
```typescript
// ❌ BAD: Partial mock - only fields you think you need
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' }
  // Missing: metadata that downstream code uses
};

// Later: breaks when code accesses response.metadata.requestId
```

**Why this is wrong:**
- **Partial mocks hide structural assumptions** - You only mocked fields you know about
- **Downstream code may depend on fields you didn't include** - Silent failures
- **Tests pass but integration fails** - Mock incomplete, real API complete
- **False confidence** - Test proves nothing about real behavior

**The Iron Rule:** Mock the COMPLETE data structure as it exists in reality, not just fields your immediate test uses.

**The fix:**
```typescript
// ✅ GOOD: Mirror real API completeness
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' },
  metadata: { requestId: 'req-789', timestamp: 1234567890 }
  // All fields real API returns
};
```

### Gate Function

```
BEFORE creating mock responses:
  Check: "What fields does the real API response contain?"

  Actions:
    1. Examine actual API response from docs/examples
    2. Include ALL fields system might consume downstream
    3. Verify mock matches real response schema completely

  Critical:
    If you're creating a mock, you must understand the ENTIRE structure
    Partial mocks fail silently when code depends on omitted fields

  If uncertain: Include all documented fields
```

## Anti-Pattern 5: Integration Tests as Afterthought

**The violation:**
```
✅ Implementation complete
❌ No tests written
"Ready for testing"
```

**Why this is wrong:**
- Testing is part of implementation, not optional follow-up
- TDD would have caught this
- Can't claim complete without tests

**The fix:**
```
TDD cycle:
1. Write failing test
2. Implement to pass
3. Refactor
4. THEN claim complete
```

---

## Anti-Pattern 6: Testing Implementation Details (Frontend)

**The violation:**
Testing internal component state, props, or hooks instead of user-visible behavior.

### Why This Is Wrong

**Users don't see internal state:**
- React state, Vue data, Angular component properties
- Tests break when refactoring (state → context → store)
- Doesn't verify UI actually updates

**Tests become brittle:**
- Change from state to props → test breaks
- Extract to hook → test breaks
- Move to external store → test breaks

**Misses real bugs:**
- State updates but UI doesn't render
- UI renders but wrong value displayed
- Accessibility broken (no ARIA labels)

### Examples

#### BAD: Testing Internal State

```typescript
// ❌ BAD: Testing React state directly
test('counter increments', () => {
  const { result } = renderHook(() => useCounter());
  result.current.increment();
  expect(result.current.count).toBe(1);
});
```

**Why wrong:**
- Users don't see `result.current.count`
- Tests implementation (state), not behavior (UI)
- Breaks when refactoring to props or context

#### GOOD: Testing User-Visible Behavior

```typescript
// ✅ GOOD: Testing what user sees
test('counter increments when button clicked', async () => {
  render(<Counter />);

  // User sees initial count
  expect(screen.getByText('Count: 0')).toBeInTheDocument();

  // User clicks button
  await userEvent.click(screen.getByRole('button', { name: /increment/i }));

  // User sees updated count
  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});
```

**Why correct:**
- Tests what users experience
- Survives refactoring (state → props → context)
- Catches UI rendering bugs

### More Examples

#### BAD: Testing Props

```typescript
// ❌ BAD: Testing component props
test('button has onClick prop', () => {
  const onClick = jest.fn();
  const { container } = render(<Button onClick={onClick} />);
  expect(container.firstChild.props.onClick).toBe(onClick);
});
```

#### GOOD: Testing Behavior

```typescript
// ✅ GOOD: Testing click behavior
test('button calls onClick when clicked', async () => {
  const onClick = jest.fn();
  render(<Button onClick={onClick}>Submit</Button>);

  await userEvent.click(screen.getByRole('button', { name: /submit/i }));

  expect(onClick).toHaveBeenCalledTimes(1);
});
```

#### BAD: Testing CSS Classes

```typescript
// ❌ BAD: Testing CSS classes
test('button is red', () => {
  render(<Button variant="danger" />);
  expect(screen.getByRole('button')).toHaveClass('btn-danger');
});
```

#### GOOD: Testing Visual Appearance

```typescript
// ✅ GOOD: Visual regression test
test('button is red', async ({ page }) => {
  await mount('<custom-button variant="danger"></custom-button>');
  await expect(page.locator('button')).toHaveScreenshot();
});
```

### Gate Function

```
BEFORE querying component internals:

  Ask: "Can a user see this value on screen?"

  IF no (state, props, hooks, refs, CSS classes):
    STOP - Don't test it directly
    Test the visible outcome instead

  IF yes (rendered text, ARIA labels, enabled/disabled state):
    Test via user-facing queries:
      - getByRole (best - accessible)
      - getByLabelText (forms)
      - getByText (visible text)
      - NOT: getByTestId (last resort)
```

### Query Priority (Testing Library)

```typescript
// 1. BEST: Accessible queries (what screen readers see)
screen.getByRole('button', { name: /submit/i });
screen.getByRole('heading', { name: /welcome/i });
screen.getByLabelText('Email address');

// 2. GOOD: Semantic queries (visible text)
screen.getByText('Click here to continue');
screen.getByPlaceholderText('Enter your email');

// 3. ACCEPTABLE: Test IDs (when nothing else works)
screen.getByTestId('submit-button');

// 4. NEVER: Implementation details
component.state.isSubmitting;
component.props.onClick;
wrapper.find('.submit-button');
```

### Framework-Agnostic Pattern

**Works with React, Vue, Angular, Svelte, Web Components:**

```typescript
// Test user behavior, not framework internals
test('form submits with valid data', async () => {
  // Render component (framework-specific mount)
  render(<LoginForm />);

  // User interactions (framework-agnostic)
  await userEvent.type(screen.getByLabelText('Email'), 'test@example.com');
  await userEvent.type(screen.getByLabelText('Password'), 'password123');
  await userEvent.click(screen.getByRole('button', { name: /submit/i }));

  // Verify user-visible outcome (framework-agnostic)
  expect(await screen.findByText('Login successful')).toBeInTheDocument();
});
```

---

## Anti-Pattern 7: No Accessibility Testing

**The violation:**
Shipping UI without verifying it's accessible to users with disabilities.

### Why This Is Wrong

**Legal requirement:**
- WCAG 2.1 Level AA compliance mandatory in many industries
- ADA lawsuits for inaccessible websites
- Section 508 compliance for government contracts

**Excludes users:**
- ~2% of users rely on screen readers
- Many more use keyboard navigation
- Inaccessible UI is unusable for these users

**Accessibility issues ARE bugs:**
- Button with no accessible name → can't be used
- Form input with no label → can't be filled

## References

For detailed information, see:

- `references/detailed-guide.md` - Complete workflow details, examples, and troubleshooting
