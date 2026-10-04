---
name: integration-testing
description: Integration testing patterns for database state, API contracts, service boundaries, and component wiring. Use when testing how multiple parts of a system work together without mocks.
---

# Integration Testing

Verify the interaction between components, data stores, and external services to ensure contract correctness and state integrity.

## When to Activate

- Test database interactions and repository logic
- Verify API client behavior against wire services
- Ensure middleware and handlers work together
- Test multi-service flows in a single process
- Debug cross-component state synchronization
- Refactor internals while keeping public contracts stable
- Audit data persistence and retrieval behavior

## Testing Layers

| Level | Isolation | Speed | Confidence |
| --- | --- | --- | --- |
| Unit | Pure functions, mocked collaborators | Fastest | Low (Logic only) |
| Integration | Real database, real network clients | Medium | Medium (Contracts + State) |
| E2E | Real browser, full environment | Slowest | High (User journey) |

## Database Integration

| Strategy | When to use | Rule |
| --- | --- | --- |
| Per-test Transaction | Standard relational DB tests | Wrap in `begin`, then `rollback` on teardown |
| Unique Fixtures | Parallel tests or non-transactional DBs | Use UUIDs/Random prefixes forทุก record |
| Truncation | Between suites or for dirty state | Truncate only the tables used |

BAD

```python
def test_get_user_orders():
    # Relies on order ID 1 existing from previous test
    orders = get_user_orders(user_id=1)
    assert len(orders) == 1
```

GOOD

```python
def test_get_user_orders(db_session, user_factory, order_factory):
    user = user_factory.create()
    order_factory.create(user_id=user.id)

    orders = get_user_orders(user_id=user.id)
    assert len(orders) == 1
```

## API Boundaries

| Concern | Strategy |
| --- | --- |
| HTTP Clients | Use WireMock or Prism instead of mocking the client class |
| Message Brokers | Use a real containerized instance (Testcontainers) |
| File Storage | Use a local filesystem fake or MinIO |

## Checklist

- [ ] Database tests use a dedicated clean environment (e.g. Testcontainers)
- [ ] Tests create their own data rather than relying on shared state
- [ ] Teardown logic reliably cleans up files, records, and connections
- [ ] Network calls to external APIs are intercepted at the wire level
- [ ] Tests verify side effects like database writes or message emits
- [ ] Serialized output matches the expected JSON/Protobuf contract
- [ ] Error paths (404, 500, timeouts) are tested with realistic failure modes
- [ ] Connection pooling and timeouts are exercised in the setup
- [ ] Asynchronous background tasks are awaited before assertion
- [ ] Migrations are run on the test database before the suite starts
- [ ] Environment variables for integration are isolated from local dev

