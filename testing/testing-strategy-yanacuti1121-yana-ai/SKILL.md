---
name: testing-strategy
description: Testing strategy — unit/integration/e2e pyramid, TDD workflow, mocking best practices, test isolation, coverage targets
triggers:
  - testing strategy
  - test pyramid
  - tdd workflow
  - unit test best practice
  - mock best practice
  - test isolation
  - integration test
  - test coverage target
  - pytest best practice
  - vitest jest best practice
do_not_use_for:
  - LLM evaluation — use ragas/deepeval
  - e2e browser testing — use playwright patterns
  - writing tests for specific code — use tdd-guide
see_also:
  - ai-code-maintainability
  - error-handling-patterns
  - type-safety-patterns
---

# Testing Strategy

## Test Pyramid

```
         [E2E]           ← few, slow, expensive, test real flows
       [Integration]     ← some, medium speed, real DB/API
     [Unit]              ← many, fast, isolated, mock externals
```

Target ratios: 70% unit, 20% integration, 10% e2e
Coverage targets: new code ≥ 80%, overall project ≥ 60%

## Python: pytest Best Practices

```python
# conftest.py — shared fixtures
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")   # test DB

@pytest.fixture
def db(engine) -> Session:
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
        session.rollback()   # clean up after each test

@pytest.fixture
def user(db: Session) -> User:
    u = User(name="Test User", email="test@example.com")
    db.add(u)
    db.flush()
    return u
```

```python
# test_user_service.py — unit test with mock
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from my_app.user_service import UserService, EmailSender

class TestUserService:
    def test_create_user_sends_welcome_email(self):
        # Arrange
        mock_sender = MagicMock(spec=EmailSender)
        mock_repo = MagicMock()
        mock_repo.save.return_value = User(id="u-1", name="Alice", email="a@b.com")
        service = UserService(repo=mock_repo, sender=mock_sender)

        # Act
        result = service.create_user("Alice", "a@b.com")

        # Assert
        assert result.name == "Alice"
        mock_sender.send.assert_called_once_with(
            to="a@b.com",
            subject="Welcome!",
        )

    @pytest.mark.asyncio
    async def test_async_method(self):
        mock_api = AsyncMock()
        mock_api.fetch.return_value = {"status": "ok"}
        service = MyService(api=mock_api)
        result = await service.do_thing()
        assert result == "ok"
```

## TypeScript: Vitest Best Practices

```typescript
// user.service.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { UserService } from "./user.service";

// Mock at module level
vi.mock("./email.service", () => ({
  EmailService: vi.fn().mockImplementation(() => ({
    send: vi.fn().mockResolvedValue(undefined),
  })),
}));

describe("UserService", () => {
  let service: UserService;
  let mockEmailService: { send: ReturnType<typeof vi.fn> };

  beforeEach(() => {
    mockEmailService = { send: vi.fn().mockResolvedValue(undefined) };
    service = new UserService({ emailService: mockEmailService });
  });

  it("sends welcome email on user creation", async () => {
    const user = await service.createUser({ name: "Alice", email: "a@b.com" });

    expect(user.name).toBe("Alice");
    expect(mockEmailService.send).toHaveBeenCalledOnce();
    expect(mockEmailService.send).toHaveBeenCalledWith(
      expect.objectContaining({ to: "a@b.com" })
    );
  });

  it("throws on duplicate email", async () => {
    await service.createUser({ name: "Alice", email: "dup@b.com" });
    await expect(
      service.createUser({ name: "Bob", email: "dup@b.com" })
    ).rejects.toThrow("email already exists");
  });
});
```

## Integration Test Pattern

```python
# test_order_api.py — integration: real DB, real HTTP
import pytest
import httpx
from fastapi.testclient import TestClient

@pytest.fixture(scope="module")
def client() -> TestClient:
    from my_app.main import app
    return TestClient(app)

def test_create_order_full_flow(client: TestClient, db: Session):
    # Create user
    user_resp = client.post("/users", json={"name": "Alice", "email": "a@b.com"})
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    # Create order
    order_resp = client.post("/orders", json={"user_id": user_id, "items": [{"sku": "A", "qty": 2}]})
    assert order_resp.status_code == 201
    order = order_resp.json()
    assert order["status"] == "pending"
    assert order["user_id"] == user_id
```

## TDD Workflow

```bash
# RED: write failing test first
pytest tests/test_feature.py::test_new_behavior -v
# → FAILED (expected)

# GREEN: minimal implementation to pass
# Write only enough code to make the test pass

pytest tests/test_feature.py::test_new_behavior -v
# → PASSED

# REFACTOR: clean up without breaking tests
pytest tests/test_feature.py -v
# → All PASSED
```

## What NOT to Mock

```python
# ✅ Mock external I/O (network, DB, file system, time)
# ✅ Mock slow operations (sleep, large computations)
# ✅ Mock non-deterministic values (random, uuid, datetime.now)

# ❌ Don't mock your own domain logic
# ❌ Don't mock data transformations — test them directly
# ❌ Don't mock to avoid test complexity — fix the design instead

# ❌ Over-mocking — this test proves nothing
def test_user_service_create():
    service = MagicMock(spec=UserService)
    service.create.return_value = User(id="1")
    result = service.create(...)
    assert result.id == "1"  # testing the mock
```

## Anti-Fake-Pass Checks

- Test that fails before implementation = TDD red phase — skip this = untested code
- `assert_called_once_with()` is strict — `assert_called_with()` only checks the last call
- `scope="session"` fixtures are shared across tests — don't mutate them in individual tests
- `asyncio` tests need `@pytest.mark.asyncio` or `asyncio_mode = "auto"` in `pytest.ini`
- Integration tests hitting real DB need cleanup — use `session.rollback()` or transaction per test
- Coverage ≥ 80% on new code — measure with `pytest --cov=src --cov-fail-under=80`
