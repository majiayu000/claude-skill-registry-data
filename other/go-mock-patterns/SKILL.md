---
name: go-mock-patterns
description: >
  Use this when generating mocks for port interfaces, deciding between mock vs
  fake vs stub for a test, writing custom matchers for complex assertions, or
  ordering expectations across multiple dependencies. Covers mockgen commands,
  controller lifecycle, EXPECT chaining, custom matchers, and ordered
  expectations.
  Triggers: gomock, mockgen, EXPECT, controller, matcher, mock vs fake vs stub.
---



# Mock Patterns

Standardizes test double usage across all microservices. Defines when to
use mocks (verify interactions), fakes (in-memory implementations), and
stubs (fixed returns). All generated mocks use gomock.

## When to Activate
- When generating mocks for port interfaces
- When deciding between mock, fake, and stub for a test
- When writing custom matchers for complex assertions
- When ordering expectations across multiple dependencies
- Used by: test-generator, code-generator, simulated-qa-engineer

## mockgen Commands

Generate mocks from interface source files.

```bash
# From source file (preferred for internal interfaces)
mockgen -source=internal/ports/outbound/user_repo.go \
  -destination=internal/ports/outbound/mocks/mock_user_repo.go \
  -package=mocks

# From interface name (for external/third-party interfaces)
mockgen -destination=internal/mocks/mock_publisher.go \
  -package=mocks \
  github.com/yourorg/shared/pkg/messaging Publisher

# Generate all mocks via go generate
//go:generate mockgen -source=repository.go -destination=mocks/mock_repository.go -package=mocks
```

## Controller Lifecycle

```go
func TestSomeFunction(t *testing.T) {
    ctrl := gomock.NewController(t)
    // No need for defer ctrl.Finish() in Go 1.14+
    // Controller auto-cleans up via t.Cleanup

    mockRepo := mocks.NewMockUserRepository(ctrl)
    mockPub := mocks.NewMockEventPublisher(ctrl)

    // set expectations, run code, assert results
}
```

## EXPECT Chaining

```go
// Basic: method, args, return, call count
mockRepo.EXPECT().FindByID(gomock.Any(), tenantID, userID).Return(expectedUser, nil).Times(1)

// Any number of calls
mockRepo.EXPECT().FindByEmail(gomock.Any(), gomock.Any(), gomock.Any()).
    Return(nil, apperrors.NotFound("user", "unknown")).AnyTimes()

// Exact argument matching
mockPub.EXPECT().Publish(gomock.Any(), "tenant."+tenantID.String()+".user.created", gomock.Any()).
    Return(nil).Times(1)

// DoAndReturn: capture arguments for assertions
var captured model.UserCreatedEvent
mockPub.EXPECT().Publish(gomock.Any(), gomock.Any(), gomock.Any()).
    DoAndReturn(func(ctx context.Context, subject string, data []byte) error {
        return msgpack.Unmarshal(data, &captured)
    }).Times(1)
```

## Custom Matchers

```go
type matchByField struct { field string; value interface{} }

func MatchByField(field string, value interface{}) gomock.Matcher {
    return &matchByField{field: field, value: value}
}

func (m *matchByField) Matches(x interface{}) bool {
    v := reflect.ValueOf(x)
    if v.Kind() == reflect.Ptr { v = v.Elem() }
    f := v.FieldByName(m.field)
    return f.IsValid() && reflect.DeepEqual(f.Interface(), m.value)
}

func (m *matchByField) String() string { return fmt.Sprintf("has %s=%v", m.field, m.value) }

// Usage:
mockRepo.EXPECT().Create(gomock.Any(), MatchByField("Email", "alice@example.com")).Return(nil)
```

## Ordered Expectations

```go
func TestCreateUserFlow(t *testing.T) {
    ctrl := gomock.NewController(t)
    mockRepo := mocks.NewMockUserRepository(ctrl)
    mockPub := mocks.NewMockEventPublisher(ctrl)

    // Enforce call order: check duplicate first, then create, then publish
    gomock.InOrder(
        mockRepo.EXPECT().
            FindByEmail(gomock.Any(), gomock.Any(), "new@example.com").
            Return(nil, apperrors.NotFound("user", "new@example.com")),
        mockRepo.EXPECT().
            Create(gomock.Any(), gomock.Any()).
            Return(nil),
        mockPub.EXPECT().
            Publish(gomock.Any(), gomock.Any(), gomock.Any()).
            Return(nil),
    )

    svc := service.NewUserService(mockRepo, mockPub)
    _, err := svc.CreateUser(ctx, input)
    require.NoError(t, err)
}
```

## Mock vs Fake vs Stub

### Mock (gomock) -- Verify Interactions
Use when you need to assert that specific methods were called with
specific arguments in a specific order.

```go
mockRepo.EXPECT().Create(gomock.Any(), gomock.Any()).Times(1)
// Test fails if Create is not called exactly once
```

**Best for**: testing side effects, event publishing, external API calls.

### Fake -- In-Memory Implementation
Use when you need a working implementation without external dependencies.

```go
type FakeUserRepository struct {
    users map[uuid.UUID]*model.User
    mu    sync.RWMutex
}

func (f *FakeUserRepository) Create(ctx context.Context, user *model.User) error {
    f.mu.Lock()
    defer f.mu.Unlock()
    if _, exists := f.users[user.ID]; exists { return apperrors.Conflict("user already exists") }
    f.users[user.ID] = user
    return nil
}

func (f *FakeUserRepository) FindByID(ctx context.Context, tenantID, id uuid.UUID) (*model.User, error) {
    f.mu.RLock()
    defer f.mu.RUnlock()
    u, ok := f.users[id]
    if !ok || u.TenantID != tenantID { return nil, apperrors.NotFound("user", id.String()) }
    return u, nil
}
```

**Best for**: repository tests, complex multi-step workflows, stateful logic.

### Stub -- Fixed Return Values
Use when you only need a dependency to return specific values and do not
care about how or how many times it was called.

```go
type StubClock struct {
    now time.Time
}

func (s *StubClock) Now() time.Time { return s.now }

// Usage
clock := &StubClock{now: time.Date(2026, 1, 15, 10, 0, 0, 0, time.UTC)}
svc := service.NewOrderService(repo, clock)
```

**Best for**: time, config, feature flags, simple value providers.

## NATS Mock Patterns

Mock NATS connections for unit tests. Use the embedded NATS server for
integration tests. Never mock NATS in E2E tests.

### Unit Tests: Mock NATS Publisher

```go
// Mock the Publisher interface from pkg/nats
mockPub := mocks.NewMockPublisher(ctrl)
mockPub.EXPECT().
    Publish(gomock.Any(), "tenant.abc123.order.created", gomock.Any()).
    Return(nil).Times(1)
```

### Unit Tests: Mock NATS Request-Reply Client

```go
// Mock the ServiceQuerier interface for inter-service queries
mockQuerier := mocks.NewMockServiceQuerier(ctrl)
mockQuerier.EXPECT().
    Query(gomock.Any(), "tenant.abc123.user.query.get_by_id", gomock.Any()).
    Return([]byte(`{"id":"user-1","name":"Alice"}`), nil).Times(1)
```

### Integration Tests: Embedded NATS (real server, no mocks)

```go
// Integration tests use the embedded NATS server -- never mock NATS
nc, js := setupNATS(t)
// ... test with real pub/sub and request-reply
```

### E2E Tests: Real NATS cluster (no mocks, no embedded server)

E2E tests connect to the deployed NATS cluster and verify real message
flow between services. Never mock NATS in E2E tests.

## Anti-Patterns

1. **Over-mocking** -- Only mock port interfaces (repositories, publishers, service queriers). Never mock domain logic, DTOs, or pure functions.
2. **Testing implementation details** -- Asserting exact call counts for internal methods makes tests break on safe refactors.
3. **Fragile mock setup** -- Use `gomock.Any()` unless the exact argument defines the test scenario.
4. **Shared mocks across subtests** -- Create a new `gomock.Controller` per subtest to avoid data races.
5. **Mock leakage into integration tests** -- Integration tests use real containers and embedded NATS, not mocks.
6. **Mocking NATS in E2E tests** -- E2E tests must use the real NATS cluster to verify actual inter-service message flow.
