---
name: go-client-mock-strategy
description: >
  Use this when picking test doubles for a new SDK client — choosing between
  in-memory wire-protocol fakes (miniredis, embedded NATS), gomock against a
  caller-owned narrow interface, or testcontainers for integration. Covers
  compile-time interface assertions and the interface-size ceiling rule.
  Triggers: miniredis, interface assertion, var _ Interface, newTestCache, fake vs mock, gomock.Controller, testcontainers.
---

# go-client-mock-strategy (v1.0.0)

## Rationale

SDK client tests face three test-double choices: (1) an in-process **fake** that
speaks the same wire protocol as the real server (e.g. `miniredis` for Redis,
`nats-server/v2/server` embedded for NATS), (2) a **generated mock** of a
caller-owned interface (gomock), or (3) a real server in a **testcontainer**.
Picking wrong makes tests either fragile (over-mocked) or slow/flaky
(container-per-test). The target SDK picks in this order: **in-memory fake →
testcontainer for integration → gomock only for caller-visible ports that the
SDK itself depends on**. The `dragonfly` package is the reference: unit and
bench tests use `miniredis.RunT(t)`, integration tests use a real Dragonfly
container, and no gomock is used anywhere because the package exposes a
concrete `*Cache`, not an interface the SDK re-consumes.

Interface-first design means: the SDK defines the **smallest** interface the
*caller* needs (`io.Closer`, a one-method `Publisher`, etc.) and asserts
conformance with `var _ Interface = (*Impl)(nil)`. Callers mock the interface
they own, not one the SDK forces on them.

## Activation signals

- A TPRD §Skills-Manifest lists `go-client-mock-strategy`
- Designing a new SDK client and choosing between miniredis-style fake and generated mocks
- `sdk-testing-lead` is about to write the first `newTest<Name>` helper
- A reviewer flags "over-mocked" or "mock leaking into integration test"

## GOOD examples

### 1. In-memory fake via `miniredis.RunT(t)` (target SDK pattern)

From `core/l2cache/dragonfly/cache_test.go` — no mocks, real wire protocol:

```go
// newTestCache boots miniredis + dials a Cache at its addr.
func newTestCache(t *testing.T, opts ...Option) (*Cache, *miniredis.Miniredis) {
    t.Helper()
    mr := miniredis.RunT(t) // auto-cleanup via t.Cleanup
    base := []Option{
        WithAddr(mr.Addr()),
        WithPoolStatsInterval(1 * time.Second),
        WithProtocol(2), // miniredis speaks RESP2
    }
    c, err := New(append(base, opts...)...)
    require.NoError(t, err)
    t.Cleanup(func() { _ = c.Close() })
    return c, mr
}
```

### 2. Compile-time interface assertion on the concrete type

From `core/l2cache/dragonfly/cache.go`:

```go
// Compile-time assertions: *Cache implements io.Closer; internal
// scraper implements the stopper shape.
var (
    _ io.Closer = (*Cache)(nil)
    _ stopper   = (*poolStatsScraper)(nil)
)
```

If the caller needs to mock `*Cache`, *they* declare a one-method interface
covering the calls they make, and gomock-generate from their interface — not
ours.

### 3. Testcontainer for integration, gated by build tag

```go
//go:build integration

func setupRealDragonfly(t *testing.T) *Cache {
    t.Helper()
    ctx := context.Background()
    container, err := testcontainers.GenericContainer(ctx, /* dragonfly image */)
    require.NoError(t, err)
    t.Cleanup(func() { _ = container.Terminate(ctx) })
    c, err := New(WithAddr(addrFromContainer(container)))
    require.NoError(t, err)
    t.Cleanup(func() { _ = c.Close() })
    return c
}
```

## BAD examples

### 1. Mocking the SDK's own concrete struct

```go
// BAD: forces the caller to depend on a generated mock of *Cache.
// *Cache has 40+ methods — mockgen output is unusable; tests are tied
// to every private method signature.
mockCache := mocks.NewMockCache(ctrl) // AVOID
```

Instead, the caller defines the 2-method interface they actually use.

### 2. Hand-rolled fake that diverges from wire semantics

```go
// BAD: fake returns a Go map; real Redis returns redis.Nil for misses.
// Tests pass; prod panics on type assertion.
type fakeCache struct{ m map[string][]byte }
func (f *fakeCache) Get(_ context.Context, k string) ([]byte, error) {
    return f.m[k], nil // never returns ErrNil
}
```

Use `miniredis` — it returns the real sentinel shape.

### 3. gomock in an integration test

```go
// BAD: integration tests must use real infra. Mocks here hide wire bugs.
func TestIntegration_Set(t *testing.T) {
    mockRDB := mocks.NewMockRedisClient(ctrl) // WRONG — use testcontainer
    mockRDB.EXPECT().Set(...).Return(nil)
}
```

## Decision criteria

| Scenario | Choice |
|---|---|
| Unit test, in-process, no external deps | **in-memory fake** (`miniredis`, embedded NATS) |
| Unit test, caller-owned port (e.g. `CredentialProvider`) | **gomock** of the interface the SDK exposes |
| Integration test, `//go:build integration` | **testcontainer** of the real server |
| Bench, hot path, latency matters | **in-memory fake** (avoid container variance) |
| E2E against staging | **no doubles** — real cluster |

Interface size rule: if the SDK publishes an interface, it SHOULD have ≤5
methods. Large concrete types (`*Cache`) are not interface-wrapped by the SDK;
callers who need a seam define their own narrow interface.

## Cross-references

- `go-mock-patterns` — gomock mechanics (controller lifecycle, EXPECT chains, matchers)
- `go-testcontainers-setup` — when and how to use real containers for integration
- `go-struct-interface-design` — interface sizing and placement rules
- `tdd-patterns` — test-first workflow that drives interface discovery
- `go-client-shutdown-lifecycle` — `t.Cleanup` ordering for fakes

## Guardrail hooks

- **G43.sh** — gofmt compliance on generated mock files
- **G61.sh** — coverage ≥90%; over-reliance on mocks drops branch coverage
- **G63.sh** — `go test -count=3 -race`; flaky mocks fail here
- Informal: the 5-method interface ceiling is enforced by `sdk-api-ergonomics-devil-go`
