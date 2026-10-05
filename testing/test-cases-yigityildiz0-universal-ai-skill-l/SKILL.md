---
name: test-cases
description: Create integration and end-to-end test scenarios covering workflows, API interactions, database operations, and system boundaries. Use when testing.
---

# Test Cases - Integration & E2E Tests

Generate comprehensive integration and end-to-end (E2E) test cases that validate component interactions, API behavior, and complete user workflows. This skill implements **Phase 3** of the 8-phase testing methodology.

## When to Use This Skill

Use this skill when you need to:

- Test interactions between multiple components
- Validate API endpoints and responses
- Test database operations and transactions
- Verify external service integrations
- Create user journey tests
- Test system workflows end-to-end
- Validate authentication and authorization flows

**Trigger phrases**: "integration tests", "e2e tests", "API tests", "test workflow", "test API endpoint", "system tests", "acceptance tests", "test user journey"

## What This Skill Does

### Integration Testing

1. **Component Integration**
   - Service-to-service communication
   - Database integration
   - Cache layer testing
   - Message queue interactions

2. **API Testing**
   - HTTP endpoint validation
   - Request/response verification
   - Status code checking
   - Header and body validation

3. **Database Testing**
   - CRUD operations
   - Transaction handling
   - Data integrity
   - Migration testing

### E2E Testing

1. **User Journeys**
   - Complete workflows
   - Multi-step processes
   - Cross-feature interactions

2. **System Validation**
   - Full stack testing
   - Production-like scenarios
   - Performance under load

### Language-Specific Examples

#### Python (pytest + requests/httpx)

```python
import pytest
import httpx
from sqlalchemy import create_engine
from myapp import create_app, db

@pytest.fixture(scope="module")
def app():
    """Create application for testing."""
    app = create_app(config="testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """Get authenticated headers."""
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    token = response.json["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestUserAPI:
    """Integration tests for User API."""

    def test_create_user_returns_201(self, client):
        """POST /api/users creates user and returns 201."""
        # Arrange
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "secure123"
        }

        # Act
        response = client.post("/api/users", json=user_data)

        # Assert
        assert response.status_code == 201
        assert response.json["email"] == "john@example.com"
        assert "id" in response.json
        assert "password" not in response.json

    def test_get_user_returns_user_data(self, client, auth_headers):
        """GET /api/users/{id} returns user details."""
        # Create user first
        create_response = client.post("/api/users", json={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password": "secure123"
        })
        user_id = create_response.json["id"]

        # Get user
        response = client.get(f"/api/users/{user_id}", headers=auth_headers)

        assert response.status_code == 200
        assert response.json["name"] == "Jane Doe"

    def test_update_user_modifies_data(self, client, auth_headers):
        """PUT /api/users/{id} updates user data."""
        # Create user
        create_response = client.post("/api/users", json={
            "name": "Original Name",
            "email": "original@example.com",
            "password": "secure123"
        })
        user_id = create_response.json["id"]

        # Update user
        response = client.put(
            f"/api/users/{user_id}",
            json={"name": "Updated Name"},
            headers=auth_headers
        )

        assert response.status_code == 200
        assert response.json["name"] == "Updated Name"

    def test_delete_user_removes_from_database(self, client, auth_headers):
        """DELETE /api/users/{id} removes user."""
        # Create user
        create_response = client.post("/api/users", json={
            "name": "To Delete",
            "email": "delete@example.com",
            "password": "secure123"
        })
        user_id = create_response.json["id"]

        # Delete user
        delete_response = client.delete(
            f"/api/users/{user_id}",
            headers=auth_headers
        )
        assert delete_response.status_code == 204

        # Verify deleted
        get_response = client.get(
            f"/api/users/{user_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404


class TestOrderWorkflow:
    """E2E tests for order workflow."""

    def test_complete_order_workflow(self, client, auth_headers):
        """Test complete order process from cart to confirmation."""
        # 1. Add items to cart
        client.post("/api/cart/items", json={
            "product_id": 1,
            "quantity": 2
        }, headers=auth_headers)

        # 2. Get cart
        cart = client.get("/api/cart", headers=auth_headers).json
        assert len(cart["items"]) == 1

        # 3. Create order from cart
        order = client.post("/api/orders", json={
            "shipping_address": "123 Test St",
            "payment_method": "credit_card"
        }, headers=auth_headers).json

        assert order["status"] == "pending"
        assert order["total"] > 0

        # 4. Process payment
        payment = client.post(f"/api/orders/{order['id']}/pay", json={
            "card_token": "tok_test_123"
        }, headers=auth_headers).json

        assert payment["status"] == "paid"

        # 5. Verify order confirmation
        final_order = client.get(
            f"/api/orders/{order['id']}",
            headers=auth_headers
        ).json

        assert final_order["status"] == "confirmed"
```

#### JavaScript/TypeScript (Jest + Supertest)

```typescript
import request from 'supertest';
import { app } from '../src/app';
import { db } from '../src/database';
import { createTestUser, getAuthToken } from './helpers';

describe('User API Integration', () => {
  let authToken: string;

  beforeAll(async () => {
    await db.migrate.latest();
    const user = await createTestUser();
    authToken = await getAuthToken(user);
  });

  afterAll(async () => {
    await db.migrate.rollback();
    await db.destroy();
  });

  describe('POST /api/users', () => {
    it('creates user and returns 201', async () => {
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'secure123'
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(201);

      expect(response.body.email).toBe('john@example.com');
      expect(response.body).toHaveProperty('id');
      expect(response.body).not.toHaveProperty('password');
    });

    it('returns 400 for invalid email', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ name: 'Test', email: 'invalid', password: 'test123' })
        .expect(400);

      expect(response.body.error).toContain('email');
    });
  });

  describe('GET /api/users/:id', () => {
    it('returns user data for authenticated request', async () => {
      const createResponse = await request(app)
        .post('/api/users')
        .send({ name: 'Jane', email: 'jane@example.com', password: 'test123' });

      const response = await request(app)
        .get(`/api/users/${createResponse.body.id}`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.name).toBe('Jane');
    });

    it('returns 401 without auth token', async () => {
      await request(app)
        .get('/api/users/1')
        .expect(401);
    });
  });
});

describe('Order Workflow E2E', () => {
  let authToken: string;
  let userId: number;

  beforeAll(async () => {
    const user = await createTestUser();
    userId = user.id;
    authToken = await getAuthToken(user);
  });

  it('completes full order workflow', async () => {
    // 1. Add to cart
    await request(app)
      .post('/api/cart/items')
      .set('Authorization', `Bearer ${authToken}`)
      .send({ productId: 1, quantity: 2 })
      .expect(200);

    // 2. Create order
    const orderResponse = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${authToken}`)
      .send({
        shippingAddress: '123 Test St',
        paymentMethod: 'credit_card'
      })
      .expect(201);

    const orderId = orderResponse.body.id;
    expect(orderResponse.body.status).toBe('pending');

    // 3. Process payment
    const paymentResponse = await request(app)
      .post(`/api/orders/${orderId}/pay`)
      .set('Authorization', `Bearer ${authToken}`)
      .send({ cardToken: 'tok_test_123' })
      .expect(200);

    expect(paymentResponse.body.status).toBe('paid');

    // 4. Verify final state
    const finalResponse = await request(app)
      .get(`/api/orders/${orderId}`)
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200);

    expect(finalResponse.body.status).toBe('confirmed');
  });
});
```

#### Java (Spring Boot Test)

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureTestDatabase
class UserApiIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Autowired
    private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        userRepository.deleteAll();
    }

    @Test
    void createUser_WithValidData_Returns201() {
        // Arrange
        UserCreateRequest request = new UserCreateRequest(
            "John Doe", "john@example.com", "secure123"
        );

        // Act
        ResponseEntity<UserResponse> response = restTemplate.postForEntity(
            "/api/users", request, UserResponse.class
        );

        // Assert
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody().getEmail()).isEqualTo("john@example.com");
        assertThat(response.getBody().getId()).isNotNull();
    }

    @Test
    void getUser_WithValidId_ReturnsUserData() {
        // Create user first
        User user = userRepository.save(new User("Jane", "jane@example.com"));

        // Get user
        ResponseEntity<UserResponse> response = restTemplate.getForEntity(
            "/api/users/" + user.getId(), UserResponse.class
        );

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody().getName()).isEqualTo("Jane");
    }

    @Test
    void deleteUser_RemovesFromDatabase() {
        User user = userRepository.save(new User("ToDelete", "delete@example.com"));

        restTemplate.delete("/api/users/" + user.getId());

        assertThat(userRepository.findById(user.getId())).isEmpty();
    }
}
```

## Prerequisites

- Unit tests completed (Phase 2)
- Test database or containers available
- API documentation or specifications
- Understanding of system boundaries

## Instructions

### Step 1: Identify Integration Points

1. **Map Component Boundaries**
   - List all service interactions
   - Identify database operations
   - Note external API calls
   - Document message flows

2. **Define Test Scenarios**
   - Happy path workflows
   - Error handling paths
   - Edge cases at boundaries

### Step 2: Set Up Test Infrastructure

1. **Test Database**
   - Use in-memory or containerized database
   - Create migration scripts
   - Seed test data

2. **Mock External Services**
   - WireMock for HTTP services
   - LocalStack for AWS
   - Testcontainers for Docker

### Step 3: Write Integration Tests

1. **API Tests**
   - Test each endpoint
   - Verify response codes
   - Validate response body
   - Check headers

2. **Database Tests**
   - Test CRUD operations
   - Verify transactions
   - Test constraints

### Step 4: Write E2E Tests

1. **User Journeys**
   - Map complete workflows
   - Test multi-step processes
   - Verify final states

## Quality Checklist

- [ ] All API endpoints tested
- [ ] Database operations verified
- [ ] Error responses validated
- [ ] Authentication flows tested
- [ ] Complete workflows covered
- [ ] Test data properly cleaned up
- [ ] Tests isolated from each other

## Related Skills

- `unit-tests` - Unit testing (Phase 2)
- `mocks-fixtures` - Test doubles (Phase 4)
- `performance-testing` - Load testing (Phase 5)

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates tests_generation/test_cases/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
