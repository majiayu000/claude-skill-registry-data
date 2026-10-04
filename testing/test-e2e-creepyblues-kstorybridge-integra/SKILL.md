---
name: test-e2e
description: Runs Playwright E2E tests with smart targeting by app and feature, supports multiple environments (local/staging/production), and can generate new E2E test files. This skill should be used when running E2E tests, generating test files for new features, or verifying application functionality end-to-end.
---

# Test E2E

This skill provides a smart E2E test runner with targeting by app/feature and the ability to generate new test files for uncovered areas (especially Creator app).

## When to Use This Skill

- Running E2E tests before deployment
- Testing specific features in isolation
- Generating new E2E tests for Creator app
- Verifying staging/production deployments
- Debugging test failures

## Current Test Coverage

### Dashboard App (3 test files)
- `auth.e2e.ts` - Authentication flows (signup, signin, protected routes, OAuth)
- `comps.e2e.ts` - Comps navigator functionality
- `trial.e2e.ts` - Trial mode features

### Creator App (0 test files)
**No E2E tests exist** - Use `--generate` to create tests

### Website App (0 test files)
Marketing pages, minimal testing needed

## Commands

### Running Tests

```
/test-e2e                                # Run all tests
/test-e2e dashboard                      # Run dashboard tests only
/test-e2e dashboard auth                 # Run dashboard auth tests
/test-e2e creator                        # Run creator tests (if any exist)
/test-e2e --staging                      # Run against staging environment
/test-e2e --production                   # Run against production (read-only tests)
/test-e2e --ui                           # Open Playwright UI mode
/test-e2e --debug                        # Run in headed debug mode
```

### Generating Tests

```
/test-e2e --generate creator auth        # Generate creator auth tests
/test-e2e --generate creator titles      # Generate creator title management tests
/test-e2e --generate creator profile     # Generate creator profile tests
/test-e2e --generate dashboard mandates  # Generate mandate search tests
```

## Test Running Workflow

### Step 1: Environment Setup

Configure test environment:

```bash
# Local (default)
export TEST_ENV=local
export BASE_URL=http://localhost:8081  # or 8083 for creator

# Staging
export TEST_ENV=staging
export BASE_URL=https://dashboard-staging.kstorybridge.com

# Production (read-only tests only!)
export TEST_ENV=production
export BASE_URL=https://dashboard.kstorybridge.com
```

### Step 2: Start Dev Server (for local)

If testing locally, ensure dev server is running:

```bash
# For dashboard tests
npm run dev:dashboard

# For creator tests
npm run dev:creator
```

Or use Playwright's webServer config (auto-starts).

### Step 3: Run Tests

```bash
# All tests
npm run test:e2e

# Specific test file
npx playwright test auth.e2e.ts

# Specific test by name
npx playwright test -g "should show validation errors"

# With UI
npm run test:e2e:ui

# With debugging
npm run test:e2e:debug
```

### Step 4: Analyze Results

```bash
# Show HTML report
npm run test:e2e:report

# View test artifacts
ls test-results/
ls playwright-report/
```

## Test Generation Workflow

### Step 1: Identify Test Scope

Determine what to test:

| App | Feature | Priority | Complexity |
|-----|---------|----------|------------|
| Creator | Auth (signup/signin) | HIGH | Medium |
| Creator | Title CRUD | HIGH | High |
| Creator | Profile editing | MEDIUM | Low |
| Creator | OAuth | MEDIUM | Medium |
| Dashboard | Mandate search | HIGH | Medium |
| Dashboard | AI chatbot | LOW | High (flaky) |

### Step 2: Generate Test File

Create test file from template:

```bash
# Create test directory if needed
mkdir -p apps/creator/e2e

# Generate file (using template)
# See templates/auth.template.ts for structure
```

### Step 3: Customize Tests

Adjust selectors and assertions for specific app:

```typescript
// Creator app uses different routes
await page.goto('/signin');  // Not /buyers/signin

// Creator app has different form fields
await page.getByLabel(/pen name/i).fill('Test Author');
```

### Step 4: Run and Verify

```bash
# Run new tests
npx playwright test apps/creator/e2e/auth.e2e.ts

# Debug if failures
npx playwright test --debug apps/creator/e2e/auth.e2e.ts
```

## Test Patterns

### Authentication Tests

```typescript
import { test, expect } from '@playwright/test';

test.describe('Creator Auth', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/signup');
  });

  test('should show signup form', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /create.*account/i })).toBeVisible();
    await expect(page.getByLabel(/email/i)).toBeVisible();
    await expect(page.getByLabel(/password/i)).toBeVisible();
  });

  test('should validate required fields', async ({ page }) => {
    await page.getByRole('button', { name: /create account/i }).click();
    await expect(page.getByText(/required/i)).toBeVisible();
  });

  test('should redirect to home after signup', async ({ page }) => {
    // Fill form
    await page.getByLabel(/email/i).fill('test@example.com');
    await page.getByLabel(/password/i).fill('Password123!');
    // ... fill other fields

    await page.getByRole('button', { name: /create account/i }).click();

    // Wait for redirect
    await expect(page).toHaveURL('/home');
  });
});
```

### Protected Route Tests

```typescript
test.describe('Protected Routes', () => {
  test('should redirect unauthenticated users to signin', async ({ page }) => {
    await page.goto('/home');
    await expect(page).toHaveURL('/signin');
  });

  test('should allow authenticated users to access protected routes', async ({ page }) => {
    // Login first
    await page.goto('/signin');
    await page.getByLabel(/email/i).fill('test@example.com');
    await page.getByLabel(/password/i).fill('Password123!');
    await page.getByRole('button', { name: /sign in/i }).click();

    // Access protected route
    await page.goto('/home');
    await expect(page).toHaveURL('/home');
  });
});
```

### CRUD Operation Tests

```typescript
test.describe('Title Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login as creator
    await loginAsCreator(page);
  });

  test('should create a new title', async ({ page }) => {
    await page.goto('/titles/new');

    await page.getByLabel(/title name/i).fill('Test Title');
    await page.getByLabel(/synopsis/i).fill('A test synopsis...');
    // ... fill other fields

    await page.getByRole('button', { name: /save/i }).click();

    await expect(page.getByText(/title created/i)).toBeVisible();
  });

  test('should edit an existing title', async ({ page }) => {
    await page.goto('/titles');
    await page.getByText('Test Title').click();
    await page.getByRole('button', { name: /edit/i }).click();

    await page.getByLabel(/title name/i).fill('Updated Title');
    await page.getByRole('button', { name: /save/i }).click();

    await expect(page.getByText(/updated/i)).toBeVisible();
  });

  test('should delete a title', async ({ page }) => {
    await page.goto('/titles');
    await page.getByText('Test Title').click();
    await page.getByRole('button', { name: /delete/i }).click();
    await page.getByRole('button', { name: /confirm/i }).click();

    await expect(page.getByText('Test Title')).not.toBeVisible();
  });
});
```

## Environment-Specific Testing

### Staging Tests

Run tests against staging environment:

```bash
TEST_ENV=staging npm run test:e2e
```

Considerations:
- Use test accounts (not production data)
- Tests may take longer (network latency)
- Some tests may need adjustment for staging data

### Production Tests

Run read-only tests against production:

```bash
TEST_ENV=production npm run test:e2e:production
```

**CRITICAL**: Production tests must be READ-ONLY:
- NO signup tests (creates real accounts)
- NO data modification tests
- Only test public pages and read operations

Safe production tests:
- Page load verification
- Public route accessibility
- Static content presence

## Test Reports

### Console Output

```
Running E2E tests...

Dashboard Tests
  auth.e2e.ts
    ✓ should show signup form (1.2s)
    ✓ should validate required fields (0.8s)
    ✓ should redirect to signin for protected routes (0.5s)
    ✗ should complete OAuth flow (timeout)

  comps.e2e.ts
    ✓ should show comps navigator (1.5s)
    ✓ should search for comps (2.3s)

Summary
  Tests: 5 passed, 1 failed
  Duration: 8.3s

Failed Tests:
  - auth.e2e.ts: should complete OAuth flow
    Error: Timeout waiting for OAuth callback
```

### HTML Report

After test run:
```bash
npm run test:e2e:report
# Opens browser with detailed report
```

### Slack Notification

```json
{
  "text": "E2E Test Results",
  "attachments": [
    {
      "color": "warning",
      "fields": [
        {"title": "Passed", "value": "5", "short": true},
        {"title": "Failed", "value": "1", "short": true},
        {"title": "Duration", "value": "8.3s", "short": true},
        {"title": "Environment", "value": "local", "short": true}
      ]
    }
  ]
}
```

## Debugging Tests

### Interactive Mode

```bash
# Open Playwright UI
npm run test:e2e:ui

# Run specific test in debug mode
npx playwright test -g "should show signup form" --debug
```

### Trace Viewer

```bash
# Enable trace for all tests
npx playwright test --trace on

# View trace
npx playwright show-trace test-results/auth-should-show-signup-form/trace.zip
```

### Screenshots and Videos

Test artifacts are saved automatically on failure:
- `test-results/[test-name]/screenshot.png`
- `test-results/[test-name]/video.webm`

## Tips

- **Flaky tests**: Add `test.retry(2)` for network-dependent tests
- **Slow tests**: Use `test.slow()` for long operations
- **Test isolation**: Each test should start with clean state
- **Selectors**: Prefer `getByRole`, `getByLabel`, `getByText` over CSS selectors
- **Timeouts**: Increase for slow operations with `{ timeout: 10000 }`
- **Skip**: Use `test.skip()` for temporarily broken tests

## Test Helpers

Create shared helpers in `tests/helpers/`:

```typescript
// tests/helpers/auth.ts
export async function loginAsCreator(page: Page) {
  await page.goto('/signin');
  await page.getByLabel(/email/i).fill(process.env.TEST_CREATOR_EMAIL!);
  await page.getByLabel(/password/i).fill(process.env.TEST_CREATOR_PASSWORD!);
  await page.getByRole('button', { name: /sign in/i }).click();
  await expect(page).toHaveURL('/home');
}

export async function loginAsBuyer(page: Page) {
  await page.goto('/buyers/signin');
  await page.getByLabel(/email/i).fill(process.env.TEST_BUYER_EMAIL!);
  await page.getByLabel(/password/i).fill(process.env.TEST_BUYER_PASSWORD!);
  await page.getByRole('button', { name: /sign in/i }).click();
  await expect(page).toHaveURL('/buyers/home');
}
```

## Related Skills

- `/deploy-staging` - Deploy to staging before running tests
- `/pr-production` - Create production PR after tests pass
- `/health-check` - Quick verification of app health
