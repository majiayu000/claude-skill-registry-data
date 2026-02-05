---
name: Mandatory Testing & Linting Guard
description: Enforce mandatory npm test and npm run lint execution after every code change with no exceptions for code quality and test coverage compliance
---

# Mandatory Testing & Linting Guard

This skill enforces the **CRITICAL** requirement: After EVERY code change, you MUST run `npm test` and `npm run lint`. No exceptions for "small changes" or "trivial updates".

## When to Use This Skill

**ALWAYS.** This skill should be invoked automatically after:
- Any code modification (TypeScript, JavaScript, CSS)
- Any component creation or update
- Any service or utility change
- Any configuration file modification
- Before creating a git commit
- Before creating a pull request

**Trigger phrases:**
- "I've made changes to..."
- "I updated the code..."
- "I created a new component..."
- "I fixed the bug..."
- "I added a feature..."

## Critical Requirement

From `CLAUDE.md`:

> **CRITICAL**: After EVERY code change, you MUST run:
> 1. `npm test` - Ensure all tests pass
> 2. `npm run lint` - Verify code quality
>
> Never proceed without both passing. No exceptions for "small changes".

## Standard Workflow

### Workflow Overview

```
Code Change → npm test → npm run lint → Commit/PR
     ↓           ↓            ↓              ↓
   Edit      875 tests    ESLint       Git commit
              MUST pass   MUST pass    (only if both pass)
```

### Step-by-Step Process

#### 1. After Making Code Changes

**Action:** Run the test suite:

```bash
npm test
```

**Expected output:**
```
✓ 875 tests passed
  Test Files  46 passed (46)
  Tests  875 passed (875)
  Duration  12.5s
```

**What to check:**
- All 875+ tests pass (or current total)
- No test failures or errors
- No warnings about missing coverage
- Coverage threshold (50%) is met

**If tests fail:**
- DO NOT proceed to linting
- Fix the failing tests first
- Re-run `npm test` until all pass

#### 2. After Tests Pass

**Action:** Run ESLint:

```bash
npm run lint
```

**Expected output:**
```
✔ No ESLint warnings or errors found
```

**What to check:**
- Zero errors
- Zero warnings
- All files comply with style guide

**If linting fails:**
- Try auto-fix first: `npm run lint:fix`
- Manually fix remaining issues
- Re-run `npm run lint` until clean

#### 3. Both Pass - Ready to Commit

**Action:** Only NOW can you proceed with:
- Creating a git commit
- Pushing to remote
- Creating a pull request
- Marking task as complete

## Test Suite Overview

### Current Statistics

- **Total Tests:** 875+
- **Test Files:** 46
- **Coverage Threshold:** 50% (statements)
- **Test Framework:** Vitest + React Testing Library
- **Environment:** happy-dom

### Test Categories

**Components (60% coverage):**
- 40+ React component tests
- Rendering, interactions, state changes
- Accessibility checks
- Dark mode compatibility

**Services (80% coverage):**
- StorageManager singleton tests
- PromptManager business logic
- Validation and error handling
- Levenshtein distance algorithms

**Hooks (70% coverage):**
- Custom React hooks
- usePrompts, useCategories, useSettings
- Async state management

**Content Scripts (40% coverage):**
- Platform strategy tests
- Injection and insertion logic
- DOM manipulation

**Utilities (90% coverage):**
- Helper functions
- Formatters and validators
- Logger utilities

### Key Test Files

**Critical test locations:**
```
src/
├── components/__tests__/         # Component tests
│   ├── PromptCard.test.tsx
│   ├── AddPromptForm.test.tsx
│   └── ... (40+ files)
├── services/__tests__/           # Service tests
│   ├── storage.test.ts
│   └── promptManager.test.ts
├── hooks/__tests__/              # Hook tests
│   └── usePrompts.test.ts
└── content/platforms/__tests__/  # Platform tests
    ├── claude-strategy.test.ts
    └── ... (platform strategies)
```

## Common Test Errors

### Error 1: Test Timeout

**Symptom:**
```
Error: Test timed out after 5000ms
```

**Solutions:**
1. Add timeout to slow async tests:
   ```typescript
   it('loads large dataset', async () => {
     // ...
   }, 10000); // 10 second timeout
   ```

2. Use `waitFor` for async state updates:
   ```typescript
   await waitFor(() => {
     expect(screen.getByText('Loaded')).toBeInTheDocument();
   });
   ```

### Error 2: Mock Not Called

**Symptom:**
```
AssertionError: expected mock to have been called
```

**Solutions:**
1. Verify mock is setup correctly:
   ```typescript
   expect(mockFn).toHaveBeenCalled();
   ```

2. Check you're calling the right mock:
   ```typescript
   expect(StorageManager.getInstance().getPrompts).toHaveBeenCalled();
   ```

3. Clear mocks between tests:
   ```typescript
   beforeEach(() => {
     vi.clearAllMocks();
   });
   ```

### Error 3: DOM Element Not Found

**Symptom:**
```
Unable to find element with text: "Submit"
```

**Solutions:**
1. Use correct query method:
   ```typescript
   // Wait for async rendering
   await screen.findByText('Submit');

   // Query by role
   screen.getByRole('button', { name: /submit/i });
   ```

2. Debug the rendered output:
   ```typescript
   const { debug } = render(<Component />);
   debug(); // Prints current DOM
   ```

### Error 4: Coverage Below Threshold

**Symptom:**
```
ERROR: Coverage for statements (48%) is below threshold (50%)
```

**Solutions:**
1. Generate coverage report to see gaps:
   ```bash
   npm run test:coverage
   open coverage/index.html
   ```

2. Add tests for uncovered code paths:
   - Error handling branches
   - Edge cases
   - Conditional logic

3. Check if new files need tests:
   ```bash
   # See which files have low coverage
   npm run test:coverage | grep -E "^[^│]*│[^│]*│[^│]*[0-9]+\.[0-9]+%"
   ```

### Error 5: React 19 Hook Errors

**Symptom:**
```
Error: useActionState is not defined
```

**Note:** React 19 hooks (`useActionState`, `useOptimistic`) are not yet supported in Node.js test environments.

**Solutions:**
1. Test these hooks manually in browser
2. Skip automated tests for React 19-specific hooks
3. Use integration tests instead of unit tests
4. Document manual testing in PR description

## ESLint Common Issues

### Issue 1: Unused Variables

**Symptom:**
```
'variable' is defined but never used
```

**Solutions:**
1. Remove unused variables
2. Prefix with underscore if intentionally unused:
   ```typescript
   const _unusedParam = value; // Intentionally unused
   ```
3. Use in function signature but not body:
   ```typescript
   function canHandle(_element: HTMLElement): boolean {
     // _element is part of interface but not needed
   }
   ```

### Issue 2: Missing Return Type

**Symptom:**
```
Missing return type on function
```

**Solutions:**
1. Add explicit return type:
   ```typescript
   // Before
   async function getData() {
     return fetch('/api');
   }

   // After
   async function getData(): Promise<Response> {
     return fetch('/api');
   }
   ```

### Issue 3: Any Type Usage

**Symptom:**
```
Unexpected any. Specify a different type
```

**Solutions:**
1. Use specific type instead:
   ```typescript
   // Before
   const data: any = JSON.parse(str);

   // After
   const data: Prompt = JSON.parse(str);
   ```

2. Use `unknown` for truly unknown types:
   ```typescript
   try {
     // ...
   } catch (error) {
     const err = error as Error; // Cast from unknown
   }
   ```

### Issue 4: Missing Dependencies in useEffect

**Symptom:**
```
React Hook useEffect has missing dependencies
```

**Solutions:**
1. Add missing dependencies:
   ```typescript
   useEffect(() => {
     loadData(id);
   }, [id]); // Add id to dependency array
   ```

2. If intentionally omitted, add comment:
   ```typescript
   useEffect(() => {
     loadOnce();
   }, []); // eslint-disable-line react-hooks/exhaustive-deps
   ```

### Issue 5: Console Statements

**Symptom:**
```
Unexpected console statement
```

**Solution:**
Use the centralized Logger instead of `console.*`:

```typescript
// ❌ DON'T
console.log('Debug message');
console.error('Error occurred');

// ✅ DO
import { Logger } from '../utils';

Logger.debug('Debug message', { component: 'MyComponent' });
Logger.error('Error occurred', toError(err), { component: 'MyComponent' });
```

## Auto-Fix Strategies

### Strategy 1: Auto-Fix Linting Issues

**Action:**
```bash
npm run lint:fix
```

This automatically fixes:
- Formatting issues
- Missing semicolons
- Import order
- Unused imports
- Simple style violations

**Remaining issues must be fixed manually.**

### Strategy 2: Test-Driven Fixes

When tests fail, use this workflow:

1. **Identify the failing test:**
   ```bash
   npm test -- --reporter=verbose
   ```

2. **Run only that test file:**
   ```bash
   npm test -- PromptCard.test.tsx
   ```

3. **Enable watch mode for rapid iteration:**
   ```bash
   npm test -- PromptCard.test.tsx --watch
   ```

4. **Fix the code until test passes**

5. **Run full suite again:**
   ```bash
   npm test
   ```

### Strategy 3: Coverage-Driven Testing

When coverage is low:

1. **Generate coverage report:**
   ```bash
   npm run test:coverage
   ```

2. **Open HTML report:**
   ```bash
   open coverage/index.html
   ```

3. **Find red/yellow highlighted lines** (uncovered code)

4. **Add tests for those code paths**

5. **Re-run coverage check**

## Emergency Override Scenarios

### Scenario 1: Pre-commit Hook Failure

**When:** Git commit fails due to test/lint errors

**NEVER override with:**
```bash
git commit --no-verify  # ❌ NEVER DO THIS
```

**Instead:**
1. Fix the errors properly
2. Run tests and linting again
3. Then commit normally

### Scenario 2: CI/CD Pipeline Failure

**When:** GitHub Actions fails on PR

**NEVER merge with:**
- Disabling required checks
- Admin override
- Force push

**Instead:**
1. Pull latest changes: `git pull origin main`
2. Fix the errors locally
3. Run tests and linting
4. Push the fixes
5. Wait for CI to pass

### Scenario 3: Urgent Hotfix Needed

**When:** Production bug needs immediate fix

**Even for hotfixes:**
1. Create the fix
2. Run `npm test`
3. Run `npm run lint`
4. Both MUST pass
5. Then deploy

**Rationale:** Broken tests = broken code. Never skip.

## Integration with Development Workflow

### Git Commit Workflow

```bash
# 1. Make your changes
vim src/components/MyComponent.tsx

# 2. MANDATORY: Run tests
npm test

# 3. MANDATORY: Run linting
npm run lint

# 4. If both pass, stage changes
git add src/components/MyComponent.tsx

# 5. Commit
git commit -m "feat: add MyComponent

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# 6. Push
git push origin feature-branch
```

### Pull Request Workflow

**Before creating PR:**
```bash
# 1. Ensure on latest main
git checkout main
git pull origin main

# 2. Rebase feature branch
git checkout feature-branch
git rebase main

# 3. Run full test suite
npm test

# 4. Run linting
npm run lint

# 5. Run build to ensure no build errors
npm run build

# 6. All three must pass before creating PR
```

**In PR description, include:**
```markdown
## Testing Checklist

- [x] All 875+ tests pass locally
- [x] ESLint shows no errors or warnings
- [x] Coverage threshold maintained (50%+)
- [x] Manual testing completed on:
  - [ ] Chrome browser
  - [ ] AI platforms: Claude, ChatGPT, Perplexity
  - [ ] Light and dark mode
```

## Continuous Integration

### GitHub Actions Checks

The project has automated CI checks that run on every PR:

**PR Checks** (`.github/workflows/pr-checks.yml`):
```yaml
- name: Run Tests
  run: npm test

- name: Run Linting
  run: npm run lint

- name: Check Coverage
  run: npm run test:coverage
```

**All checks must pass before PR can be merged.**

### Pre-commit Hooks

The project uses Husky for pre-commit hooks:

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "vitest related --run"
    ]
  }
}
```

**This automatically runs:**
1. ESLint on changed files
2. Related tests for changed code

## Quick Reference

### Essential Commands

| Command | Purpose | When to Run |
|---------|---------|-------------|
| `npm test` | Run all 875+ tests | After EVERY change |
| `npm run lint` | Run ESLint checks | After EVERY change |
| `npm run lint:fix` | Auto-fix linting issues | When lint errors occur |
| `npm run test:coverage` | Generate coverage report | Weekly or when adding features |
| `npm run test:ui` | Interactive test UI | Debugging test failures |
| `npm test -- --watch` | Watch mode for tests | During active development |

### Success Indicators

**Tests Pass:**
```
✓ 875 tests passed
✓ Test Files  46 passed (46)
✓ Coverage: 55% (exceeds 50% threshold)
```

**Linting Pass:**
```
✔ No ESLint warnings or errors found
```

### Failure Indicators

**Tests Fail:**
```
✖ 3 tests failed
✖ Expected: true, Received: false
```
**Action:** Fix tests before proceeding

**Linting Fail:**
```
✖ 5 problems (3 errors, 2 warnings)
```
**Action:** Run `npm run lint:fix`, then fix remaining issues

## Enforcement Checklist

Before marking ANY task complete, verify:

- [ ] All code changes are complete
- [ ] `npm test` has been run
- [ ] All 875+ tests pass (or current total)
- [ ] `npm run lint` has been run
- [ ] Zero ESLint errors
- [ ] Zero ESLint warnings
- [ ] Coverage threshold (50%) maintained
- [ ] No console errors in test output
- [ ] Build succeeds (`npm run build`)

**Only after ALL checkboxes are checked can you:**
- Create a git commit
- Push to remote repository
- Create a pull request
- Mark the task as complete

## Related Documentation

- **Testing Guide:** `docs/TESTING.md` - Comprehensive testing strategies
- **Development Workflow:** `CLAUDE.md` - Essential commands and guidelines
- **Architecture:** `docs/ARCHITECTURE.md` - System design patterns

## Philosophy

**Why This Matters:**

1. **Test Coverage:** 875+ tests ensure nothing breaks
2. **Code Quality:** ESLint catches bugs before they ship
3. **Consistency:** Every developer follows the same standards
4. **Confidence:** Changes don't introduce regressions
5. **Documentation:** Tests serve as living documentation

**The Rule:**
> "If it's too small to test, it's too small to break."

Even "trivial" changes can cause cascading failures. Always test. Always lint. No exceptions.

---

**Last Updated:** 2025-10-18
**Skill Version:** 1.0.0
