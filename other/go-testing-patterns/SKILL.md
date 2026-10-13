---
name: go-testing-patterns
description: >
  Use this when writing unit, integration, or benchmark tests, setting up test
  infrastructure (PostgreSQL, NATS, Redis via testcontainers), or generating
  and using mocks for port interfaces. Covers table-driven units, testcontainers
  reuse, gomock for port isolation, httptest, fixtures, benchmark structure,
  and coverage enforcement.
  Triggers: testing, table-driven, testcontainers, gomock, httptest, benchmark, coverage.
---



# Testing Patterns

Standardizes testing across all microservices: table-driven tests for
units, testcontainers for database integration, embedded NATS for
messaging tests, and gomock for port isolation.

## When to Activate
- When writing unit, integration, or benchmark tests
- When setting up test infrastructure (PostgreSQL, NATS)
- When generating and using mocks for port interfaces
- Used by: component-designer, simulated-senior-developer, simulated-tech-lead

## Table-Driven Tests

```go
func TestCalculateDiscount(t *testing.T) {
    t.Parallel()
    tests := []struct {
        name     string
        quantity int
        price    float64
        want     float64
        wantErr  bool
    }{
        {"no discount under 10", 5, 100.0, 500.0, false},
        {"10% discount at 10+", 10, 100.0, 900.0, false},
        {"negative quantity errors", -1, 100.0, 0, true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            got, err := service.CalculateDiscount(tt.quantity, tt.price)
            if tt.wantErr { if err == nil { t.Fatal("expected error") }; return }
            if err != nil { t.Fatalf("unexpected error: %v", err) }
            if got != tt.want { t.Errorf("got %v, want %v", got, tt.want) }
        })
    }
}
```

## testcontainers-go PostgreSQL

```go
func setupPostgres(t *testing.T) *pgxpool.Pool {
    t.Helper()
    ctx := context.Background()
    container, err := postgres.Run(ctx, "duckdb/duckdb:latest",
        postgres.WithDatabase("testdb"),
        postgres.WithUsername("test"), postgres.WithPassword("test"),
        testcontainers.WithWaitStrategy(
            wait.ForLog("database system is ready to accept connections").WithOccurrence(2),
        ),
    )
    if err != nil { t.Fatalf("starting postgres: %v", err) }
    t.Cleanup(func() { _ = container.Terminate(ctx) })

    connStr, _ := container.ConnectionString(ctx, "sslmode=disable")
    pool, err := pgxpool.New(ctx, connStr)
    if err != nil { t.Fatalf("connecting: %v", err) }
    t.Cleanup(pool.Close)
    applyMigrations(t, pool)
    return pool
}
```

## Embedded NATS Server

```go
func setupNATS(t *testing.T) (*nats.Conn, nats.JetStreamContext) {
    t.Helper()
    srv, err := natsserver.NewServer(&natsserver.Options{
        Port: -1, JetStream: true, StoreDir: t.TempDir(),
    })
    if err != nil { t.Fatalf("creating nats server: %v", err) }
    srv.Start()
    t.Cleanup(srv.Shutdown)
    if !srv.ReadyForConnections(5 * time.Second) { t.Fatal("nats not ready") }

    nc, err := nats.Connect(srv.ClientURL())
    if err != nil { t.Fatalf("connecting: %v", err) }
    t.Cleanup(nc.Close)
    js, _ := nc.JetStream()
    return nc, js
}
```

## gomock Usage

Generate: `mockgen -source=internal/ports/outbound/order_repo.go -destination=internal/ports/outbound/mocks/order_repo_mock.go -package=mocks`

```go
func TestCreateOrderHandler(t *testing.T) {
    ctrl := gomock.NewController(t)
    mockRepo := mocks.NewMockOrderRepository(ctrl)
    mockPub := mocks.NewMockEventPublisher(ctrl)

    mockRepo.EXPECT().Create(gomock.Any(), gomock.Any()).Return(nil)
    mockPub.EXPECT().Publish(gomock.Any(), gomock.Any(), gomock.Any()).Return(nil)

    handler := command.NewCreateOrderHandler(mockRepo, mockPub)
    _, err := handler.Handle(context.Background(), model.CreateOrderCommand{})
    if err != nil { t.Fatalf("unexpected error: %v", err) }
}
```

## httptest Handler Testing (API Gateway Only)

httptest is used only for testing API Gateway HTTP handlers. Domain services
do not have HTTP business endpoints -- they use NATS inbound adapters.

```go
func TestCreateHandler(t *testing.T) {
    handler := NewCreateHandler( /* inject mocked deps */ )
    body := `{"name":"test-item","quantity":5}`
    req := httptest.NewRequest(http.MethodPost, "/items", strings.NewReader(body))
    req.Header.Set("Content-Type", "application/x-msgpack")
    rec := httptest.NewRecorder()
    handler.ServeHTTP(rec, req)
    if rec.Code != http.StatusCreated {
        t.Errorf("status = %d, want %d", rec.Code, http.StatusCreated)
    }
}
```

## NATS Message Handler Testing

Domain services receive messages via NATS. Use the embedded NATS server to
test NATS subscription handlers and request-reply responders.

```go
func TestOrderCreatedHandler(t *testing.T) {
    nc, js := setupNATS(t)

    // Create per-service stream (mirrors production auto-stream creation)
    _, err := js.AddStream(&nats.StreamConfig{
        Name:     "ORDER-SERVICE",
        Subjects: []string{"tenant.*.order-service.>", "order-service._reply.>"},
        Storage:  nats.MemoryStorage,
    })
    require.NoError(t, err)

    // Register handler under test via JetStream QueueSubscribe (mandatory queue group)
    var received atomic.Bool
    sub, err := js.QueueSubscribe("tenant.*.order-service.order.created", "order-service",
        func(msg *nats.Msg) {
            received.Store(true)
            msg.Ack()
        },
        nats.Durable("test-consumer"), nats.ManualAck(),
    )
    require.NoError(t, err)
    t.Cleanup(func() { _ = sub.Drain() })

    // Publish test message via JetStream (NOT core NATS nc.Publish)
    pubMsg := &nats.Msg{
        Subject: "tenant.test-tenant.order-service.order.created",
        Data:    []byte(`{"id":"order-1","tenant_id":"test-tenant"}`),
        Header:  nats.Header{},
    }
    pubMsg.Header.Set("Tenant-ID", "test-tenant")
    _, err = js.PublishMsg(pubMsg)
    require.NoError(t, err)

    // Wait for handler to process
    require.Eventually(t, func() bool { return received.Load() }, 5*time.Second, 50*time.Millisecond)
}
```

### NATS JetStream Request-Reply Handler Testing

Request-reply uses the JetStream reply topic pattern, not core NATS
`nc.Request`/`msg.Respond`. The requester publishes with a `Reply-Subject`
header, and the responder publishes the response to that subject.

```go
func TestGetOrderQueryHandler(t *testing.T) {
    nc, js := setupNATS(t)

    // Create per-service streams for the test
    _, err := js.AddStream(&nats.StreamConfig{
        Name:     "ORDER-SERVICE",
        Subjects: []string{"tenant.*.order-service.>", "order-service._reply.>"},
        Storage:  nats.MemoryStorage,
    })
    require.NoError(t, err)

    // Register request-reply handler via JetStream QueueSubscribe
    sub, err := js.QueueSubscribe("tenant.*.order-service.query.get_by_id", "order-service",
        func(msg *nats.Msg) {
            replySubject := msg.Header.Get("Reply-Subject")
            resp := &nats.Msg{
                Subject: replySubject,
                Data:    []byte(`{"id":"order-1","status":"active"}`),
                Header:  nats.Header{},
            }
            _, _ = js.PublishMsg(resp) // Reply via JetStream, NOT msg.Respond
            msg.Ack()
        },
        nats.Durable("test-query-handler"), nats.ManualAck(),
    )
    require.NoError(t, err)
    t.Cleanup(func() { _ = sub.Drain() })

    // Subscribe to reply subject to capture response
    var reply atomic.Value
    replySub, err := js.QueueSubscribe("order-service._reply.>", "test-reply",
        func(msg *nats.Msg) {
            reply.Store(msg)
            msg.Ack()
        },
        nats.Durable("test-reply-consumer"), nats.ManualAck(),
    )
    require.NoError(t, err)
    t.Cleanup(func() { _ = replySub.Drain() })

    // Publish request with Reply-Subject header
    reqMsg := &nats.Msg{
        Subject: "tenant.test-tenant.order-service.query.get_by_id",
        Data:    []byte(`{"order_id":"order-1"}`),
        Header:  nats.Header{},
    }
    reqMsg.Header.Set("Reply-Subject", "order-service._reply.test-correlation-id")
    _, err = js.PublishMsg(reqMsg)
    require.NoError(t, err)

    // Wait for reply
    require.Eventually(t, func() bool { return reply.Load() != nil }, 5*time.Second, 50*time.Millisecond)
    replyMsg := reply.Load().(*nats.Msg)
    assert.Contains(t, string(replyMsg.Data), "order-1")
}
```

## Test Fixture Loading

```go
func LoadFixture(t *testing.T, name string) []byte {
    t.Helper()
    _, file, _, _ := runtime.Caller(0)
    path := filepath.Join(filepath.Dir(file), "..", "testdata", name)
    data, err := os.ReadFile(path)
    if err != nil { t.Fatalf("loading fixture %s: %v", name, err) }
    return data
}
```

## Benchmark Template

```go
func BenchmarkSerializeOrder(b *testing.B) {
    order := model.Order{ID: uuid.New(), Status: "active"}
    b.ResetTimer()
    b.ReportAllocs()
    for range b.N {
        if _, err := msgpack.Marshal(order); err != nil { b.Fatal(err) }
    }
}
```

## Coverage Enforcement

```bash
go test -race -count=1 -coverprofile=coverage.out ./...
go tool cover -func=coverage.out | grep total | awk '{print $3}' | \
  awk -F'%' '{if ($1 < 80) { print "FAIL: coverage " $1 "% < 80%"; exit 1 }}'
```

## Common Mistakes

1. **Not using `t.Parallel()`** -- Sequential tests waste CI time. Add `t.Parallel()` as the first line of every top-level `Test*` function that uses only mock dependencies (no shared mutable state).
2. **Sharing test containers** -- Each test should get its own via `t.Cleanup`.
3. **Testing internals** -- Test behavior (inputs/outputs), not internal state.
4. **Missing `-race` flag** -- Always run with `-race` in CI.
5. **Fixtures with absolute paths** -- Use `runtime.Caller` for portability.
6. **Using time.Sleep() for async assertions** -- NEVER use `time.Sleep()` to wait for async operations (e.g., NATS message delivery) before asserting. Use `assert.Eventually` or `require.Eventually` with a polling interval instead. Example: `require.Eventually(t, func() bool { return counter.Load() == expected }, 2*time.Second, 50*time.Millisecond)`. `time.Sleep` causes flaky tests and wastes CI time (TS-002 HIGH finding in testing phase).
7. **Creating local embedded NATS server setup functions** -- Canonical test infrastructure lives in `src/tests/containers/`. NEVER create local `setupEmbeddedNATS` or `setupNATSServer` helper functions in individual test packages. Always import and use `src/tests/containers/nats.go:SetupEmbeddedNATS`. Duplicating NATS setup leads to 4+ near-identical implementations across test packages (TS-003 HIGH finding in testing phase).
