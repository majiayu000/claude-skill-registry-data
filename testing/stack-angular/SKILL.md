---
name: stack-angular
description: Angular frontend conventions, patterns, and test infrastructure. Use when working with Angular components, services, modules, RxJS, Angular CLI, ng commands, Jasmine tests, Component Harnesses, HttpTestingController, Angular routing, Angular forms, Angular pipes, or Angular dependency injection.
user-invocable: false
---

## Integration Tests
```typescript
// Use Component Harnesses + HttpTestingController
describe('OrderListComponent', () => {
  it('should display orders after loading', async () => {
    const harness = await TestbedHarnessEnvironment.harnessForFixture(
      fixture, OrderListComponentHarness
    );
    await harness.clickRefresh();
    const items = await harness.getOrderItems();
    expect(items.length).toBeGreaterThan(0);
  });
});
```

## Frameworks
- Jasmine for tests
- Component Harnesses for component testing
- HttpTestingController for service integration

## Build & Test Commands
```bash
ng build
ng test --watch=false
```

## Test Patterns by Component Classification

### Presentational Components
Skip standalone tests — covered by parent component integration tests.
Exception: if the component has 3+ conditional branches (e.g., `*ngIf` / `@if` chains), write a focused component test.

### Smart/Container Components
```typescript
// Component Harness + HttpTestingController for smart components
describe('DashboardComponent', () => {
  it('should load and display stats from service', async () => {
    const harness = await TestbedHarnessEnvironment.harnessForFixture(
      fixture, DashboardComponentHarness
    );
    const req = httpTestingController.expectOne('/api/stats');
    req.flush(mockStats);
    const cards = await harness.getStatCards();
    expect(cards.length).toBe(mockStats.length);
  });
});
```

### Form-heavy Components
```typescript
// Integration test for reactive form submission
describe('ProfileFormComponent', () => {
  it('should submit valid form data', async () => {
    const harness = await TestbedHarnessEnvironment.harnessForFixture(
      fixture, ProfileFormComponentHarness
    );
    await harness.fillName('Jane Doe');
    await harness.fillEmail('jane@example.com');
    await harness.clickSubmit();
    const req = httpTestingController.expectOne('/api/profile');
    expect(req.request.body.name).toBe('Jane Doe');
  });

  it('should show validation error for invalid email', async () => {
    const harness = await TestbedHarnessEnvironment.harnessForFixture(
      fixture, ProfileFormComponentHarness
    );
    await harness.fillEmail('not-an-email');
    await harness.clickSubmit();
    const error = await harness.getEmailError();
    expect(error).toBeTruthy();
  });
});
```

Unit test custom validators separately only when they have complex rules:
```typescript
describe('passwordStrengthValidator', () => {
  it('should reject passwords without special characters', () => {
    const control = new FormControl('weakpassword');
    const result = passwordStrengthValidator(control);
    expect(result?.['passwordStrength']).toBeTruthy();
  });
});
```

### Critical User Journey (E2E)
```typescript
// Playwright Test — E2E for auth flow (runs in CI)
import { test, expect } from '@playwright/test';

test('login flow', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[data-testid="email"]', 'user@example.com');
  await page.fill('[data-testid="password"]', 'securepassword');
  await page.click('[data-testid="login-button"]');
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('[data-testid="welcome-message"]')).toBeVisible();
});
```

### Visual/Layout Components
Write Playwright visual regression tests — these run in CI and catch regressions automatically:
```typescript
// Playwright visual regression test (runs in CI)
test('sidebar matches visual baseline', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page.locator('[data-testid="sidebar"]')).toHaveScreenshot('sidebar.png');
});
```
For interactive spot-checks during development, use Playwright CLI (`playwright-cli snapshot`, `playwright-cli screenshot`). Neither replaces Playwright Test — see the `testing` skill's "Browser Testing Tools" section.

### Data Display Components
```typescript
// Integration test for data table with transformation
describe('OrderTableComponent', () => {
  it('should display formatted order data', async () => {
    const harness = await TestbedHarnessEnvironment.harnessForFixture(
      fixture, OrderTableComponentHarness
    );
    const req = httpTestingController.expectOne('/api/orders');
    req.flush([{ amount: 1500, date: '2024-01-15' }]);
    const rows = await harness.getRows();
    expect(rows.length).toBe(1);
    const amount = await rows[0].getAmount();
    expect(amount).toContain('$15.00');
  });
});
```

## Security
- Trust Angular's built-in XSS protection — do not bypass with `bypassSecurityTrust*` unless absolutely necessary and reviewed
- Use `HttpClient` which includes XSRF protection by default
- Sanitize user input displayed via `[innerHTML]` using `DomSanitizer`

Read the project's applicable agent guidance (`AGENTS.md` for Codex, `CLAUDE.md` for
Claude Code) and relevant `docs/<topic>.md` files for project-specific Angular
conventions when they exist.
