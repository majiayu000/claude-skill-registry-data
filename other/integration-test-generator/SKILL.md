---
name: integration-test-generator
description: Generate integration tests that verify component interactions across API boundaries, databases, message queues, and external services. Use when testing.
---

# Integration Test Generator

Generate integration tests that verify the correct interaction between multiple components, services, and infrastructure dependencies. Unlike unit tests that isolate a single function, integration tests exercise the boundaries where components connect: HTTP APIs, database queries, message queues, file systems, and third-party services.

## When to Use This Skill

Use this skill when you need to:

- Test REST or GraphQL API endpoints end-to-end (request through response)
- Verify database operations (queries, transactions, migrations) against a real or containerized database
- Test service-to-service communication patterns (synchronous calls, async messaging)
- Validate message queue producers and consumers (Kafka, RabbitMQ, SQS)
- Implement contract tests between API providers and consumers
- Set up testcontainers for reproducible integration test environments
- Verify authentication and authorization flows across service boundaries
- Test file upload/download and storage integration
- Validate caching behaviour with real cache stores (Redis, Memcached)

**Trigger phrases**: "integration test", "API test", "database test", "service test", "contract test", "testcontainers", "end-to-end API", "test the endpoint", "test database queries", "message queue test", "REST test", "GraphQL test"

## What This Skill Does

### Integration Testing Layers

Integration tests operate at several layers, each with different scope and infrastructure requirements:

| Layer | What It Tests | Infrastructure Needed |
|---|---|---|
| API Integration | HTTP request/response cycle | Running application server |
| Database Integration | SQL/NoSQL operations, migrations, transactions | Database instance (container or in-memory) |
| Service-to-Service | Inter-service HTTP/gRPC calls | Multiple running services or mocks |
| Message Queue | Producer/consumer message flow | Message broker (container or embedded) |
| Contract Testing | API schema compatibility between provider and consumer | Contract broker (e.g., Pact) |
| External Service | Third-party API integration | Mocks, stubs, or sandbox environments |

### Test Architecture Principles

1. **Use real infrastructure when feasible**: Prefer containerized databases and brokers over in-memory fakes to catch real-world issues (SQL dialect differences, connection pooling, transaction isolation)
2. **Isolate test data**: Each test should create its own data and clean up afterward; never depend on pre-existing database rows
3. **Control external boundaries**: Mock or stub external services you do not own; use contract tests to verify compatibility
4. **Keep tests fast**: Integration tests are slower than unit tests but should still complete in seconds, not minutes; use connection pooling, parallel containers, and test data factories
5. **Test failure modes**: Integration tests should cover not just happy paths but also network errors, timeouts, invalid responses, and partial failures

## Instructions

### Step 1: Set Up API Integration Tests

**Python (FastAPI + pytest + httpx):**
```python
import pytest
from httpx import AsyncClient, ASGITransport
from myapp.main import app
from myapp.database import get_db, Base, engine


@pytest.fixture(autouse=True)
async def setup_database():
    """Create tables before each test, drop after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    """Async HTTP client wired to the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestUserApi:
    """Integration tests for the /users API endpoints."""

    async def test_create_user_returns_201(self, client):
        response = await client.post("/users", json={
            "email": "alice@example.com",
            "name": "Alice",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "alice@example.com"
        assert "id" in data

    async def test_create_duplicate_email_returns_409(self, client):
        await client.post("/users", json={
            "email": "bob@example.com",
            "name": "Bob",
        })
        response = await client.post("/users", json={
            "email": "bob@example.com",
            "name": "Bob Again",
        })
        assert response.status_code == 409

    async def test_get_user_by_id(self, client):
        create_response = await client.post("/users", json={
            "email": "carol@example.com",
            "name": "Carol",
        })
        user_id = create_response.json()["id"]

        get_response = await client.get(f"/users/{user_id}")
        assert get_response.status_code == 200
        assert get_response.json()["name"] == "Carol"

    async def test_get_nonexistent_user_returns_404(self, client):
        response = await client.get("/users/99999")
        assert response.status_code == 404

    async def test_delete_user_returns_204(self, client):
        create_response = await client.post("/users", json={
            "email": "dave@example.com",
            "name": "Dave",
        })
        user_id = create_response.json()["id"]

        delete_response = await client.delete(f"/users/{user_id}")
        assert delete_response.status_code == 204

        get_response = await client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

    async def test_list_users_with_pagination(self, client):
        for i in range(15):
            await client.post("/users", json={
                "email": f"user{i}@example.com",
                "name": f"User {i}",
            })
        response = await client.get("/users?page=1&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10
        assert data["total"] == 15

    async def test_create_user_with_invalid_email_returns_422(self, client):
        response = await client.post("/users", json={
            "email": "not-an-email",
            "name": "Invalid",
        })
        assert response.status_code == 422
```

**JavaScript (Express + supertest + Jest):**
```javascript
const request = require("supertest");
const { createApp } = require("../src/app");
const { setupDatabase, teardownDatabase, getDb } = require("../src/database");

let app;
let db;

beforeAll(async () => {
  db = await setupDatabase({ inMemory: true });
  app = createApp({ db });
});

afterAll(async () => {
  await teardownDatabase(db);
});

afterEach(async () => {
  await db("users").truncate();
});

describe("POST /users", () => {
  test("creates a user and returns 201", async () => {
    const response = await request(app)
      .post("/users")
      .send({ email: "alice@example.com", name: "Alice" })
      .expect(201);

    expect(response.body).toMatchObject({
      email: "alice@example.com",
      name: "Alice",
    });
    expect(response.body.id).toBeDefined();
  });

  test("returns 409 for duplicate email", async () => {
    await request(app)
      .post("/users")
      .send({ email: "bob@example.com", name: "Bob" })
      .expect(201);

    await request(app)
      .post("/users")
      .send({ email: "bob@example.com", name: "Bob Again" })
      .expect(409);
  });

  test("returns 422 for invalid email", async () => {
    await request(app)
      .post("/users")
      .send({ email: "not-an-email", name: "Invalid" })
      .expect(422);
  });
});

describe("GET /users/:id", () => {
  test("returns the user by ID", async () => {
    const createResponse = await request(app)
      .post("/users")
      .send({ email: "carol@example.com", name: "Carol" })
      .expect(201);

    const response = await request(app)
      .get(`/users/${createResponse.body.id}`)
      .expect(200);

    expect(response.body.name).toBe("Carol");
  });

  test("returns 404 for nonexistent user", async () => {
    await request(app).get("/users/99999").expect(404);
  });
});

describe("DELETE /users/:id", () => {
  test("deletes the user and returns 204", async () => {
    const createResponse = await request(app)
      .post("/users")
      .send({ email: "dave@example.com", name: "Dave" })
      .expect(201);

    await request(app)
      .delete(`/users/${createResponse.body.id}`)
      .expect(204);

    await request(app)
      .get(`/users/${createResponse.body.id}`)
      .expect(404);
  });
});
```

**Java (Spring Boot + JUnit 5 + MockMvc):**
```java
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class UserApiIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserRepository userRepository;

    @AfterEach
    void tearDown() {
        userRepository.deleteAll();
    }

    @Test
    void createUserReturns201() throws Exception {
        mockMvc.perform(post("/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {"email": "alice@example.com", "name": "Alice"}
                    """))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.email").value("alice@example.com"))
                .andExpect(jsonPath("$.id").isNumber());
    }

    @Test
    void duplicateEmailReturns409() throws Exception {
        mockMvc.perform(post("/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {"email": "bob@example.com", "name": "Bob"}
                    """))
                .andExpect(status().isCreated());

        mockMvc.perform(post("/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {"email": "bob@example.com", "name": "Bob Again"}
                    """))
                .andExpect(status().isConflict());
    }

    @Test
    void getUserByIdReturns200() throws Exception {
        var result = mockMvc.perform(post("/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {"email": "carol@example.com", "name": "Carol"}
                    """))
                .andExpect(status().isCreated())
                .andReturn();

        String body = result.getResponse().getContentAsString();
        int userId = com.fasterxml.jackson.databind.ObjectMapper
                .readTree(body).get("id").asInt();

        mockMvc.perform(get("/users/" + userId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Carol"));
    }

    @Test
    void getNonexistentUserReturns404() throws Exception {
        mockMvc.perform(get("/users/99999"))
                .andExpect(status().isNotFound());
    }
}
```

### Step 2: Set Up Database Integration Tests with Testcontainers

**Python (pytest + testcontainers):**
```python
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="module")
def postgres():
    """Start a PostgreSQL container for the test module."""
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg


@pytest.fixture
def db_session(postgres):
    """Create a fresh database session with transaction rollback."""
    engine = create_engine(postgres.get_connection_url())
    # Run migrations
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                customer_email TEXT NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT NOW()
            )
        """))
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


class TestOrderRepository:
    """Database integration tests using a real PostgreSQL container."""

    def test_create_order(self, db_session):
        repo = OrderRepository(db_session)
        order = repo.create(
            customer_email="alice@example.com",
            total_amount=99.99,
        )
        assert order.id is not None
        assert order.status == "pending"

    def test_find_orders_by_customer(self, db_session):
        repo = OrderRepository(db_session)
        repo.create(customer_email="bob@example.com", total_amount=50.00)
        repo.create(customer_email="bob@example.com", total_amount=75.00)
        repo.create(customer_email="carol@example.com", total_amount=100.00)

        bob_orders = repo.find_by_customer("bob@example.com")
        assert len(bob_orders) == 2

    def test_update_order_status(self, db_session):
        repo = OrderRepository(db_session)
        order = repo.create(
            customer_email="dave@example.com",
            total_amount=200.00,
        )
        updated = repo.update_status(order.id, "shipped")
        assert updated.status == "shipped"

    def test_transaction_rollback_on_error(self, db_session):
        repo = OrderRepository(db_session)
        repo.create(customer_email="eve@example.com", total_amount=50.00)

        with pytest.raises(ValueError):
            repo.update_status(99999, "shipped")  # Non-existent order

        # Original order should still exist despite the error
        orders = repo.find_by_customer("eve@example.com")
        assert len(orders) == 1
```

**JavaScript (Jest + testcontainers):**
```javascript
const { GenericContainer } = require("testcontainers");
const { Client } = require("pg");

let container;
let client;

beforeAll(async () => {
  container = await new GenericContainer("postgres:16-alpine")
    .withEnvironment({
      POSTGRES_USER: "test",
      POSTGRES_PASSWORD: "test",
      POSTGRES_DB: "testdb",
    })
    .withExposedPorts(5432)
    .start();

  client = new Client({
    host: container.getHost(),
    port: container.getMappedPort(5432),
    user: "test",
    password: "test",
    database: "testdb",
  });
  await client.connect();

  await client.query(`
    CREATE TABLE orders (
      id SERIAL PRIMARY KEY,
      customer_email TEXT NOT NULL,
      total_amount DECIMAL(10, 2) NOT NULL,
      status TEXT NOT NULL DEFAULT 'pending',
      created_at TIMESTAMP DEFAULT NOW()
    )
  `);
}, 60000);

afterAll(async () => {
  await client.end();
  await container.stop();
});

afterEach(async () => {
  await client.query("DELETE FROM orders");
});

describe("OrderRepository with PostgreSQL", () => {
  test("creates an order", async () => {
    const result = await client.query(
      "INSERT INTO orders (customer_email, total_amount) VALUES ($1, $2) RETURNING *",
      ["alice@example.com", 99.99]
    );
    expect(result.rows[0].customer_email).toBe("alice@example.com");
    expect(result.rows[0].status).toBe("pending");
  });

  test("finds orders by customer email", async () => {
    await client.query(
      "INSERT INTO orders (customer_email, total_amount) VALUES ($1, $2), ($1, $3)",
      ["bob@example.com", 50.0, 75.0]
    );
    const result = await client.query(
      "SELECT * FROM orders WHERE customer_email = $1",
      ["bob@example.com"]
    );
    expect(result.rows).toHaveLength(2);
  });
});
```

**Java (JUnit 5 + Testcontainers):**
```java
import org.junit.jupiter.api.*;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import javax.sql.DataSource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import static org.junit.jupiter.api.Assertions.*;

@Testcontainers
class OrderRepositoryIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");

    private JdbcTemplate jdbc;
    private OrderRepository repo;

    @BeforeEach
    void setUp() {
        var ds = new DriverManagerDataSource();
        ds.setUrl(postgres.getJdbcUrl());
        ds.setUsername(postgres.getUsername());
        ds.setPassword(postgres.getPassword());
        jdbc = new JdbcTemplate(ds);

        jdbc.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                customer_email TEXT NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending'
            )
        """);
        repo = new OrderRepository(jdbc);
    }

    @AfterEach
    void tearDown() {
        jdbc.execute("DELETE FROM orders");
    }

    @Test
    void createOrderPersistsToDatabase() {
        var order = repo.create("alice@example.com", java.math.BigDecimal.valueOf(99.99));
        assertNotNull(order.getId());
        assertEquals("pending", order.getStatus());
    }

    @Test
    void findOrdersByCustomerReturnsMatchingRows() {
        repo.create("bob@example.com", java.math.BigDecimal.valueOf(50));
        repo.create("bob@example.com", java.math.BigDecimal.valueOf(75));
        repo.create("carol@example.com", java.math.BigDecimal.valueOf(100));

        var bobOrders = repo.findByCustomer("bob@example.com");
        assertEquals(2, bobOrders.size());
    }
}
```

### Step 3: Set Up Service-to-Service Integration Tests

**Python (using responses library for HTTP mocking):**
```python
import responses
import pytest
from myapp.services import OrderService, PaymentGateway


class TestOrderServiceIntegration:
    """Test OrderService integration with PaymentGateway."""

    @responses.activate
    def test_place_order_calls_payment_gateway(self):
        responses.add(
            responses.POST,
            "https://payments.example.com/charge",
            json={"transaction_id": "txn_123", "status": "success"},
            status=200,
        )

        service = OrderService(
            payment_gateway_url="https://payments.example.com"
        )
        result = service.place_order(
            customer_email="alice@example.com",
            amount=99.99,
        )

        assert result.status == "confirmed"
        assert result.transaction_id == "txn_123"
        assert len(responses.calls) == 1

    @responses.activate
    def test_place_order_handles_payment_failure(self):
        responses.add(
            responses.POST,
            "https://payments.example.com/charge",
            json={"error": "insufficient_funds"},
            status=402,
        )

        service = OrderService(
            payment_gateway_url="https://payments.example.com"
        )
        result = service.place_order(
            customer_email="bob@example.com",
            amount=999999.99,
        )

        assert result.status == "payment_failed"

    @responses.activate
    def test_place_order_handles_gateway_timeout(self):
        responses.add(
            responses.POST,
            "https://payments.example.com/charge",
            body=ConnectionError("Connection timed out"),
        )

        service = OrderService(
            payment_gateway_url="https://payments.example.com"
        )
        with pytest.raises(ServiceUnavailableError):
            service.place_order(
                customer_email="carol@example.com",
                amount=50.00,
            )
```

**JavaScript (nock for HTTP mocking):**
```javascript
const nock = require("nock");
const { OrderService } = require("../src/services/orderService");

describe("OrderService integration with PaymentGateway", () => {
  afterEach(() => {
    nock.cleanAll();
  });

  test("place order calls payment gateway and confirms", async () => {
    nock("https://payments.example.com")
      .post("/charge")
      .reply(200, { transaction_id: "txn_123", status: "success" });

    const service = new OrderService({
      paymentGatewayUrl: "https://payments.example.com",
    });
    const result = await service.placeOrder("alice@example.com", 99.99);

    expect(result.status).toBe("confirmed");
    expect(result.transactionId).toBe("txn_123");
  });

  test("place order handles payment failure gracefully", async () => {
    nock("https://payments.example.com")
      .post("/charge")
      .reply(402, { error: "insufficient_funds" });

    const service = new OrderService({
      paymentGatewayUrl: "https://payments.example.com",
    });
    const result = await service.placeOrder("bob@example.com", 999999.99);

    expect(result.status).toBe("payment_failed");
  });

  test("place order throws on gateway timeout", async () => {
    nock("https://payments.example.com")
      .post("/charge")
      .replyWithError("Connection timed out");

    const service = new OrderService({
      paymentGatewayUrl: "https://payments.example.com",
    });

    await expect(service.placeOrder("carol@example.com", 50.0)).rejects.toThrow(
      "Service unavailable"
    );
  });
});
```

**Java (WireMock):**
```java
import com.github.tomakehurst.wiremock.junit5.WireMockTest;
import com.github.tomakehurst.wiremock.client.WireMock;
import org.junit.jupiter.api.Test;
import static com.github.tomakehurst.wiremock.client.WireMock.*;
import static org.junit.jupiter.api.Assertions.*;

@WireMockTest(httpPort = 8089)
class OrderServiceIntegrationTest {

    @Test
    void placeOrderCallsPaymentGateway() {
        stubFor(post(urlEqualTo("/charge"))
                .willReturn(okJson("""
                    {"transaction_id": "txn_123", "status": "success"}
                    """)));

        var service = new OrderService("http://localhost:8089");
        var result = service.placeOrder("alice@example.com",
                java.math.BigDecimal.valueOf(99.99));

        assertEquals("confirmed", result.getStatus());
        assertEquals("txn_123", result.getTransactionId());
    }

    @Test
    void placeOrderHandlesPaymentFailure() {
        stubFor(post(urlEqualTo("/charge"))
                .willReturn(aResponse()
                        .withStatus(402)
                        .withBody("""
                            {"error": "insufficient_funds"}
                            """)));

        var service = new OrderService("http://localhost:8089");
        var result = service.placeOrder("bob@example.com",
                java.math.BigDecimal.valueOf(999999.99));

        assertEquals("payment_failed", result.getStatus());
    }

    @Test
    void placeOrderHandlesGatewayTimeout() {
        stubFor(post(urlEqualTo("/charge"))
                .willReturn(aResponse()
                        .withFixedDelay(30000)));

        var service = new OrderService("http://localhost:8089");
        service.setTimeoutMs(1000);

        assertThrows(ServiceUnavailableException.class,
                () -> service.placeOrder("carol@example.com",
                        java.math.BigDecimal.valueOf(50)));
    }
}
```

### Step 4: Set Up Contract Tests

**Python (Pact consumer test):**
```python
import atexit
from pact import Consumer, Provider

pact = Consumer("OrderService").has_pact_with(
    Provider("PaymentService"),
    pact_dir="./pacts",
)
pact.start_service()
atexit.register(pact.stop_service)


class TestPaymentServiceContract:
    """Consumer-side contract tests for PaymentService."""

    def test_successful_charge(self):
        expected = {"transaction_id": "txn_123", "status": "success"}

        (pact
         .given("a valid credit card")
         .upon_receiving("a charge request")
         .with_request("post", "/charge", body={
             "amount": 99.99,
             "currency": "USD",
             "customer_email": "alice@example.com",
         })
         .will_respond_with(200, body=expected))

        with pact:
            client = PaymentClient(base_url=pact.uri)
            result = client.charge(
                amount=99.99,
                currency="USD",
                customer_email="alice@example.com",
            )
            assert result["transaction_id"] == "txn_123"
```

### Step 5: Set Up Message Queue Integration Tests

**Python (Kafka with testcontainers):**
```python
import pytest
import json
from testcontainers.kafka import KafkaContainer
from kafka import KafkaProducer, KafkaConsumer


@pytest.fixture(scope="module")
def kafka():
    with KafkaContainer("confluentinc/cp-kafka:7.5.0") as kc:
        yield kc


class TestOrderEventMessaging:
    """Integration tests for Kafka message production and consumption."""

    def test_order_created_event_published(self, kafka):
        producer = KafkaProducer(
            bootstrap_servers=kafka.get_bootstrap_server(),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        consumer = KafkaConsumer(
            "order-events",
            bootstrap_servers=kafka.get_bootstrap_server(),
            auto_offset_reset="earliest",
            consumer_timeout_ms=10000,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )

        event = {
            "type": "order.created",
            "order_id": "ord_123",
            "customer_email": "alice@example.com",
            "total": 99.99,
        }
        producer.send("order-events", event)
        producer.flush()

        messages = list(consumer)
        assert len(messages) >= 1
        assert messages[0].value["type"] == "order.created"
        assert messages[0].value["order_id"] == "ord_123"

        producer.close()
        consumer.close()
```

## Best Practices

- **Use testcontainers over mocks for databases**: In-memory databases (H2, SQLite) have different SQL dialects and behaviour; testcontainers provide the real engine with minimal overhead
- **Isolate test data with transactions**: Wrap each test in a transaction and roll back after; this is faster than truncating tables
- **Test both success and failure paths**: An integration test that only covers the happy path provides false confidence; test timeouts, 4xx/5xx responses, and malformed data
- **Use contract tests between teams**: When two teams own different services, contract tests prevent breaking changes without requiring both services to be running simultaneously
- **Keep integration tests in a separate directory**: Integration tests have different infrastructure requirements and run slower; separate them from unit tests so developers can run unit tests quickly
- **Tag tests by infrastructure dependency**: Use markers/tags (e.g., `@Tag("database")`, `@pytest.mark.database`) so you can run subsets locally
- **Use factory functions for test data**: Create helper functions that generate valid test entities with sensible defaults; this reduces boilerplate and makes tests more readable
- **Set explicit timeouts on all network calls**: An integration test that hangs for 30 seconds waiting for a response wastes CI time; set timeouts and assert on timeout behaviour

## Common Pitfalls

- **Testing implementation details instead of contracts**: Integration tests should verify external behaviour (HTTP status codes, response bodies, database state), not internal method calls
- **Sharing test data across tests**: Tests that depend on data created by other tests are order-dependent and fragile; each test must create its own data
- **Not cleaning up resources**: Containers, connections, and file handles that are not closed leak resources and cause subsequent tests to fail
- **Using production credentials in tests**: Integration tests should never connect to production databases or APIs; use containers, mocks, or sandbox environments
- **Making tests too broad**: An integration test that exercises the entire request lifecycle through five services is an end-to-end test, not an integration test; keep the scope to 2-3 components
- **Ignoring test container startup time**: Container startup adds seconds to the test suite; use module-scoped containers that are shared across tests within the same module
- **Hardcoding URLs and ports**: Tests that bind to `localhost:5432` fail when that port is in use; use dynamic port allocation from testcontainers
- **Not testing idempotency**: Integration tests should verify that retrying an operation (e.g., creating the same order twice) produces the correct result, not a duplicate
- **Skipping error response body assertions**: Verifying that an API returns 400 is not enough; assert that the error response body contains a meaningful error code and message

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Unit tests are enough — integration tests duplicate coverage" | Unit tests verify individual functions with mocked dependencies; integration tests verify that the wiring between those functions works correctly; the Therac-25 radiation overdose incidents involved components that each worked correctly in isolation but failed catastrophically when integrated. |
| "Integration tests are too slow to run in CI" | Testcontainers starts a real database in 2-5 seconds and tears it down after the suite; the total overhead for a 50-test integration suite using containers is typically under 60 seconds, well within CI time budgets. |
| "We'll catch integration issues in the staging environment" | Staging environments are shared, have stale data, and are expensive to reproduce deterministically; an integration test suite that runs on every PR catches integration regressions at the point of introduction, not after merge. |
| "Sharing a database across integration tests is fine if tests are careful" | Test isolation via shared state fails when tests run in parallel or when a failing test leaves the database in an unexpected state; each test must own its data setup and teardown to be deterministic. |
| "Integration tests should cover the full end-to-end flow" | Tests that span the entire system are end-to-end tests, not integration tests; keeping integration tests scoped to 2-3 components produces tests that are fast, reliable, and unambiguous when they fail. |

## Verification

- [ ] Each integration test creates its own test data and does not depend on data from another test (verified by running tests in random order)
- [ ] All database and service containers are started and torn down per test module (not shared across the entire suite)
- [ ] Integration tests cover both success and error paths for each tested boundary
- [ ] Test suite completes in under 120 seconds on a standard CI runner
- [ ] All tests pass deterministically on three consecutive runs: `pytest tests/integration -q` exits with code 0 each time
