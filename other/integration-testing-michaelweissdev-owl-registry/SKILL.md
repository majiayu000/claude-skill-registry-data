---
name: integration-testing
description: >
  Architect, implement, and run reliable integration tests verifying interactions
  across database, network, API, and process boundaries. Use when testing real
  database transactions with Testcontainers or ephemeral DBs, mocking external
  third-party HTTP services with WireMock/responses, managing test fixtures,
  or orchestrating end-to-end integration test suites.
compatibility: >
  Agent Skills-compatible coding agents implementing integration tests across
  application stacks.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "testing, integration-tests, databases, testcontainers, fixtures, api-testing"
  topics: "testing, software-development"
---

# Robust Integration Testing

While unit tests verify logic in isolation, integration tests verify that multiple real components (application code, databases, caches, message queues, external HTTP services) work together correctly. Reliable integration tests must be deterministic, isolated between test cases, and clean up all state automatically.

## Core Rules

1. **Test real boundaries with ephemeral infrastructure**: Prefer lightweight containerized services (via Testcontainers or local Docker Compose) over mocking internal database queries.
2. **Never run integration tests against shared staging databases**: Tests must run against private, isolated database instances to prevent data contamination and flaky concurrency collisions.
3. **Isolate test cases with transactions or clean migrations**: Either run each test inside an uncommitted database transaction that rolls back at test completion, or truncate tables between tests.
4. **Mock third-party external APIs, not internal databases**: Use HTTP stub servers (e.g. WireMock, `respx`, `responses`) to simulate external vendor endpoints reliably with controlled latency and error codes.
5. **Set explicit connection and query timeouts**: Prevent test suites from hanging indefinitely when background containers or network sockets stall.

---

## 1. Database Integration Testing (Transaction Rollback Pattern)

In pytest/SQLAlchemy, execute each integration test inside a rolled-back transaction so test data never persists to disk:

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from my_app.models import Base, User

# Engine created once per test session
@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("postgresql+psycopg://test:test@localhost:5432/test_db")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

# Each test runs in an isolated nested transaction
@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback() # Discards all test inserts/updates!
    connection.close()

def test_create_and_query_user(db_session):
    new_user = User(username="alice", email="alice@example.com")
    db_session.add(new_user)
    db_session.commit()

    retrieved = db_session.query(User).filter_by(username="alice").first()
    assert retrieved is not None
    assert retrieved.email == "alice@example.com"
    # When test finishes, transaction.rollback() leaves database completely clean!
```

---

## 2. Using Testcontainers for Ephemeral Services

Run integration tests against real database engines without needing locally installed PostgreSQL or Redis daemons:

```python
import pytest
from testcontainers.postgres import PostgresContainer
from my_app.db import init_pool

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres.get_connection_url()

def test_full_repository_lifecycle(postgres_container):
    pool = init_pool(postgres_container)
    assert pool.ping() is True
```

---

## 3. Mocking External Third-Party APIs

When integrating with external payment gateways, SMS providers, or SaaS APIs, mock only at the HTTP network boundary:

```python
import httpx
import respx
import pytest
from my_app.payment import PaymentClient, PaymentError

@respx.mock
def test_payment_charge_declined():
    # Mock external Stripe/payment HTTP response
    respx.post("https://api.gateway.com/v1/charges").mock(
        return_value=httpx.Response(
            status_code=402,
            json={"error": {"code": "card_declined", "message": "Insufficient funds"}}
        )
    )

    client = PaymentClient(base_url="https://api.gateway.com")
    with pytest.raises(PaymentError, match="Insufficient funds"):
        client.charge_card("tok_123", amount_cents=5000)
```

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Mocking database queries with `unittest.mock` | Misses real SQL syntax errors, constraint violations, and migration bugs | Run against real SQLite or Postgres container |
| Tests relying on previous tests' data | Tests fail if run in isolation or random order | Make every test self-contained with fresh fixtures |
| Calling real third-party production APIs | Flaky tests, rate limits, credit card charges | Stub HTTP endpoints with `respx` or WireMock |
| Uncleaned test files on local disk | Fills developer disks and pollutes git working trees | Use `tempfile.TemporaryDirectory` with context manager |

---

## 5. Verification Checklist

- [ ] Tests run against private, ephemeral database instances.
- [ ] Database state is clean before and after each test.
- [ ] No real calls to external internet APIs during test runs.
- [ ] Tests pass when run in parallel or random order (`pytest -n 4`).
- [ ] All containers and background processes terminate cleanly on test exit.
