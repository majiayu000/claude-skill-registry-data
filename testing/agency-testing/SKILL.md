---
name: agency-testing
description: Write and run pytest backend tests and Playwright E2E tests for the Social Media Agency. Use when creating tests, debugging test failures, adding test coverage, mocking external services, or configuring test infrastructure.
---

# Social Media Agency Testing

## Backend Testing (pytest)

### Quick Start

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/agency --cov-report=term-missing

# Run specific test file
pytest tests/test_clients.py -v

# Run single test
pytest tests/test_clients.py::test_create_client_success -v
```

### Project Structure

```
backend/tests/
├── conftest.py                # Shared fixtures (app, client, db, factories)
├── test_auth.py               # Login, signup, JWT validation
├── test_clients.py            # CRUD clients
├── test_campaigns.py          # CRUD campaigns
├── test_content.py            # Content creation, AI generation (mocked)
├── test_approvals.py          # Approval workflow lifecycle
├── test_calendar.py           # Scheduling, rescheduling
├── test_analytics.py          # Analytics endpoints
├── test_ai_engine.py          # LLM integration (mocked)
├── test_billing.py            # Stripe subscription flow (mocked)
├── test_assets.py             # Media upload/management
└── test_agentmail.py          # AgentMail email integration (mocked)
```

### conftest.py

```python
# backend/tests/conftest.py
import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from agency.main import create_app
from agency.config import get_settings

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest.fixture
def auth_headers():
    from jose import jwt
    settings = get_settings()
    token = jwt.encode(
        {
            "sub": str(uuid.uuid4()),
            "email": "admin@demoagency.com",
            "role": "admin",
            "org_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
        },
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def manager_headers():
    from jose import jwt
    settings = get_settings()
    token = jwt.encode(
        {
            "sub": str(uuid.uuid4()),
            "email": "manager@demoagency.com",
            "role": "manager",
            "org_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
        },
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def creator_headers():
    from jose import jwt
    settings = get_settings()
    token = jwt.encode(
        {
            "sub": str(uuid.uuid4()),
            "email": "creator@demoagency.com",
            "role": "content_creator",
            "org_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
        },
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    return {"Authorization": f"Bearer {token}"}
```

### Test Templates

#### API Endpoint Test

```python
# tests/test_clients.py
import pytest

@pytest.mark.asyncio
async def test_create_client(client, auth_headers):
    response = await client.post(
        "/api/v1/clients",
        json={
            "brand_name": "Sunrise Coffee",
            "industry": "Food & Beverage",
            "description": "Artisan coffee roaster with focus on organic beans and community.",
            "contact_email": "sarah@sunrisecoffee.com",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["brand_name"] == "Sunrise Coffee"
    assert data["industry"] == "Food & Beverage"

@pytest.mark.asyncio
async def test_create_client_unauthorized(client):
    response = await client.post("/api/v1/clients", json={})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_client_validation_error(client, auth_headers):
    response = await client.post(
        "/api/v1/clients",
        json={"brand_name": "A"},  # too short
        headers=auth_headers,
    )
    assert response.status_code == 422
```

#### Content & AI Test

```python
# tests/test_content.py
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_create_content(client, auth_headers):
    response = await client.post(
        "/api/v1/content",
        json={
            "client_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
            "platform": "instagram",
            "body": "Fresh roast dropping this Friday! Who's ready?",
            "hashtags": ["coffee", "freshroast", "artisancoffee"],
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["platform"] == "instagram"
    assert data["status"] == "draft"

@pytest.mark.asyncio
async def test_generate_content_with_ai(client, auth_headers, mock_openai):
    response = await client.post(
        "/api/v1/content/generate",
        json={
            "client_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
            "platform": "instagram",
            "topic": "new seasonal blend launch",
            "tone": "excited",
            "content_type": "post",
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "body" in data
    assert data["ai_generated"] is True
```

#### Approval Workflow Test

```python
# tests/test_approvals.py
import pytest

@pytest.mark.asyncio
async def test_approval_workflow(client, creator_headers, manager_headers):
    # Creator creates content
    content_resp = await client.post(
        "/api/v1/content",
        json={
            "client_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
            "platform": "instagram",
            "body": "Great post content here",
        },
        headers=creator_headers,
    )
    content_id = content_resp.json()["id"]

    # Creator submits for approval
    await client.post(
        f"/api/v1/approvals/{content_id}/submit",
        headers=creator_headers,
    )

    # Manager approves
    approval_resp = await client.post(
        f"/api/v1/approvals/{content_id}/approve",
        headers=manager_headers,
    )
    assert approval_resp.status_code == 200
    assert approval_resp.json()["status"] == "approved"
```

#### Service Unit Test

```python
# tests/test_ai_engine.py
import pytest
from unittest.mock import AsyncMock
from agency.services.ai_engine import AIEngine

@pytest.mark.asyncio
async def test_ai_engine_generates_content():
    engine = AIEngine()
    engine.primary = AsyncMock()
    engine.primary.chat.return_value = "Check out our amazing new seasonal blend!"

    messages = [{"role": "system", "content": "Generate a post."}, {"role": "user", "content": "Coffee launch"}]
    response = await engine.chat(messages)

    assert "seasonal" in response.lower()
    engine.primary.chat.assert_called_once()

@pytest.mark.asyncio
async def test_ai_engine_fallback_on_primary_failure():
    engine = AIEngine()
    engine.primary = AsyncMock()
    engine.primary.chat.side_effect = Exception("API down")
    engine.fallback = AsyncMock()
    engine.fallback.chat.return_value = "Fallback content"

    response = await engine.chat([{"role": "user", "content": "Hello"}])

    assert response == "Fallback content"
    engine.fallback.chat.assert_called_once()
```

### Mocking External Services

```python
# Mock OpenAI
@pytest.fixture
def mock_openai():
    with patch("agency.services.ai_engine.AsyncOpenAI") as mock:
        instance = mock.return_value
        instance.chat.completions.create = AsyncMock(return_value=MockCompletion("Generated content"))
        yield instance

# Mock Stripe
@pytest.fixture
def mock_stripe():
    with patch("agency.services.billing_service.stripe") as mock:
        mock.checkout.Session.create.return_value = {"url": "https://checkout.stripe.com/test"}
        mock.Customer.create.return_value = {"id": "cus_test123"}
        yield mock

# Mock AgentMail
@pytest.fixture
def mock_agentmail():
    with patch("agency.services.agentmail_client.AgentMail") as mock:
        instance = mock.return_value
        instance.inboxes.create.return_value = MockInbox("inbox@test.com")
        instance.inboxes.messages.send.return_value = MockMessage("msg_123")
        yield instance
```

### pyproject.toml Test Config

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = ["--cov=src/agency", "--cov-report=term-missing", "--verbose"]
```

---

## Frontend E2E Testing (Playwright)

### Quick Start

```bash
cd frontend

npx playwright install chromium
npx playwright test
npx playwright test --headed
npx playwright test --ui
npx playwright show-report
```

### Project Structure

```
frontend/tests/
├── e2e/
│   ├── auth.spec.ts            # Login, signup, logout
│   ├── dashboard.spec.ts       # Dashboard pages, KPIs, navigation
│   ├── clients.spec.ts         # Create, edit, manage clients
│   ├── content.spec.ts         # Create content, AI generation, scheduling
│   ├── calendar.spec.ts        # Calendar view, drag-and-drop
│   ├── approvals.spec.ts       # Approval workflow
│   ├── analytics.spec.ts       # Analytics charts, filters
│   ├── billing.spec.ts         # Pricing page, upgrade flow
│   ├── responsive.spec.ts      # Mobile + tablet viewports
│   └── navigation.spec.ts      # Sidebar, topbar, cross-page links
├── fixtures/
│   └── test-fixtures.ts
└── helpers/
    └── selectors.ts
playwright.config.ts
```

### Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: "html",
  use: {
    baseURL: process.env.E2E_BASE_URL || "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  webServer: {
    command: "npm run dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
  },
  projects: [
    { name: "chromium", use: { browserName: "chromium" } },
  ],
});
```

### E2E Test Templates

```typescript
// tests/e2e/clients.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Clients", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/login");
    await page.getByPlaceholder("Email").fill("admin@demoagency.com");
    await page.getByPlaceholder("Password").fill("password123");
    await page.getByRole("button", { name: "Sign In" }).click();
    await expect(page).toHaveURL(/\/dashboard/);
  });

  test("should create a new client", async ({ page }) => {
    await page.getByRole("link", { name: "Clients" }).click();
    await page.getByRole("button", { name: "Add Client" }).click();

    await page.getByLabel("Brand Name").fill("Sunrise Coffee");
    await page.getByLabel("Industry").fill("Food & Beverage");

    const [response] = await Promise.all([
      page.waitForResponse((r) => r.url().includes("/api/v1/clients") && r.status() === 201),
      page.getByRole("button", { name: "Create" }).click(),
    ]);

    await expect(page.getByText("Client created")).toBeVisible();
  });
});

// tests/e2e/content.spec.ts
test.describe("Content Creation", () => {
  test("should create and schedule content", async ({ page }) => {
    await page.getByRole("link", { name: "Content" }).click();
    await page.getByRole("button", { name: "Create Content" }).click();

    await page.getByLabel("Platform").selectOption("instagram");
    await page.getByLabel("Content").fill("Fresh roast dropping this Friday!");

    await page.getByRole("button", { name: "Create" }).click();
    await expect(page.getByText("Content created")).toBeVisible();
  });

  test("should generate content with AI", async ({ page }) => {
    await page.route("/api/v1/content/generate", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          body: "AI generated post content",
          hashtags: ["coffee", "artisan"],
          ai_generated: true,
        }),
      })
    );

    await page.getByRole("button", { name: "AI Generate" }).click();
    await expect(page.getByLabel("Content")).toHaveValue(/AI generated/);
  });
});
```

### Responsive Test

```typescript
test("should show mobile nav on small screens", async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto("/dashboard");

  await expect(page.locator("[data-testid='sidebar']")).not.toBeVisible();
  await page.getByRole("button", { name: "Menu" }).click();
  await expect(page.locator("[data-testid='mobile-nav']")).toBeVisible();
});
```

### CI Integration

```yaml
  e2e:
    runs-on: ubuntu-latest
    needs: [backend, frontend]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: npm ci
        working-directory: frontend
      - run: npx playwright install --with-deps chromium
        working-directory: frontend
      - run: npx playwright test
        working-directory: frontend
        env:
          E2E_BASE_URL: http://localhost:3000
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: frontend/playwright-report/
```

## Key Rules

1. **Always mock external services** in tests (OpenAI, Stripe, AgentMail)
2. **CI tests against real Postgres + Redis** — not SQLite or in-memory
3. **Every new endpoint gets tests** — happy path, auth guard, validation errors
4. **E2E tests are independent** — no reliance on test ordering
5. **Use factories for test data** — not raw SQL in each test
6. **Prefer `getByRole()` and `getByLabel()`** over CSS selectors in Playwright
7. **Add `data-testid`** to complex components for reliable E2E targeting
8. **Coverage target: 80%+** for backend services
