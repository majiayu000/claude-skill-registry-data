---
name: python-testcontainers-setup
description: >
  Use this when authoring integration tests against a real backend (PostgreSQL,
  Redis, Kafka, MinIO, NATS, MongoDB), debugging slow or flaky container-backed
  tests, gating tests on Docker availability, or capturing container logs on
  failure. Covers session-scoped fixtures, state reset between tests
  (TRUNCATE / transactional rollback / per-test schema), the
  @pytest.mark.integration marker plus pytest_collection_modifyitems Docker
  gate, healthcheck/wait policies, log dumping via request.addfinalizer, image
  version pinning, dynamic port discovery, TC_REUSE for dev iteration,
  DOCKER_HOST discovery, and per-service connection-URL recipes.
  Triggers: testcontainers, PostgresContainer, RedisContainer, KafkaContainer, MinioContainer, MongoDbContainer, NatsContainer, docker, integration, @pytest.mark.integration.
---

# python-testcontainers-setup (v1.0.0)

## Rationale

Mocks test what the SDK author thinks the dependency does. Containers test what the dependency actually does. For Python SDKs that talk to PostgreSQL / Redis / Kafka / MinIO / NATS / Mongo, the integration test layer runs against a real container booted from `testcontainers-python`. The discipline below covers fixture scope, marker registration, Docker availability gates, log capture, and common per-service quirks.

This skill is cited by `code-reviewer-python` (test-quality), `python-pytest-patterns` (Rule 7 marker registration, Rule 3 fixture scope), `sdk-integration-flake-hunter-python` (the agent that detects flake under `--count=3`), `sdk-existing-api-analyzer-python` (test baseline capture), and `sdk-convention-devil-python` (C-14).

## Activation signals

- Authoring integration tests for an SDK that talks to an external service.
- TPRD §3 declares an integration that needs a real backend.
- Tests are slow because every test starts a container.
- Tests are flaky on CI — race between test start and container readiness.
- `@pytest.mark.integration` marker is missing or unregistered.
- Docker not available on a developer's machine — what's the failure mode?

## Core rules

### Rule 1 — Mark every container test

Every test that needs a container is marked `@pytest.mark.integration` so it can be selected/excluded:

```python
# tests/integration/test_storage.py
import pytest

pytestmark = pytest.mark.integration                # whole file is integration


async def test_storage_e2e(postgres_url) -> None:
    ...
```

`pytestmark` at module level applies the marker to every test in the file. For per-test markers, use `@pytest.mark.integration` on the function.

Register the marker (per `python-pytest-patterns` Rule 7):

```toml
[tool.pytest.ini_options]
markers = [
    "integration: requires testcontainers / docker",
]
```

Run subsets:

```bash
pytest -m "not integration"           # unit only — fast, runs in CI's first pass
pytest -m "integration"               # integration only — slower, second pass
```

### Rule 2 — Session-scoped fixtures (default)

Containers are EXPENSIVE to start (5–30 seconds for Postgres; longer for Kafka). Create them ONCE per test session:

```python
# tests/integration/conftest.py
from collections.abc import Iterator

import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_container() -> Iterator[PostgresContainer]:
    container = PostgresContainer("postgres:16-alpine")
    container.start()
    yield container
    container.stop()


@pytest.fixture(scope="session")
def postgres_url(postgres_container: PostgresContainer) -> str:
    return postgres_container.get_connection_url()
```

Session scope means: ONE container for the whole test run. Tests share it. This is fast but requires Rule 3 (state isolation between tests).

Function scope (one container per test) is correct ONLY if state isolation can't be done another way — and is usually 100x slower. Avoid unless necessary.

### Rule 3 — Reset state between tests, not the container

Tests that share a container MUST reset state between runs. Three patterns, in order of preference:

**A. Truncate / FLUSHDB / drop-recreate at test entry**:

```python
@pytest.fixture
async def clean_pg(postgres_url) -> AsyncIterator[asyncpg.Pool]:
    pool = await asyncpg.create_pool(postgres_url)
    async with pool.acquire() as conn:
        await conn.execute("TRUNCATE TABLE users, sessions, events RESTART IDENTITY CASCADE;")
    yield pool
    await pool.close()
```

**B. Transactional rollback** (postgres-specific; cleanest):

```python
@pytest.fixture
async def pg_tx(postgres_url) -> AsyncIterator[asyncpg.Connection]:
    conn = await asyncpg.connect(postgres_url)
    tx = conn.transaction()
    await tx.start()
    yield conn
    await tx.rollback()                     # auto-undo all changes
    await conn.close()
```

**C. Per-test schema / namespace**:

```python
@pytest.fixture
async def pg_schema(postgres_url, request) -> AsyncIterator[str]:
    schema = f"test_{request.node.name}_{uuid.uuid4().hex[:8]}"
    conn = await asyncpg.connect(postgres_url)
    await conn.execute(f'CREATE SCHEMA "{schema}"')
    await conn.execute(f'SET search_path TO "{schema}"')
    yield schema
    await conn.execute(f'DROP SCHEMA "{schema}" CASCADE')
    await conn.close()
```

Use B for transactional dbs (Postgres, MySQL). Use A for non-transactional or simpler stores (Redis FLUSHDB, MinIO DELETE bucket). Use C when tests need full DDL (CREATE TABLE) — schemas isolate cheaply.

### Rule 4 — Docker availability gate

Container tests skip cleanly when Docker isn't available:

```python
# tests/integration/conftest.py
import pytest

def _docker_available() -> bool:
    try:
        import docker
        client = docker.from_env()
        client.ping()
        return True
    except Exception:
        return False


def pytest_collection_modifyitems(config, items):
    """Skip integration tests if docker is unavailable."""
    if _docker_available():
        return
    skip = pytest.mark.skip(reason="Docker not available")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip)
```

This is a `conftest.py` hook; runs once. Local development without Docker → unit tests still pass. CI with Docker → integration tests run.

Alternative: per-fixture skip:

```python
@pytest.fixture(scope="session")
def postgres_container() -> Iterator[PostgresContainer]:
    if not _docker_available():
        pytest.skip("Docker not available", allow_module_level=True)
    ...
```

### Rule 5 — Healthcheck wait policy

`testcontainers-python` waits for the container's port to be reachable before `start()` returns. For services with multi-stage startup (Kafka — needs ZooKeeper too; Postgres — accepting connections ≠ ready), add an explicit readiness wait:

```python
from testcontainers.postgres import PostgresContainer
import asyncpg
import asyncio

@pytest.fixture(scope="session")
def postgres_container() -> Iterator[PostgresContainer]:
    container = PostgresContainer("postgres:16-alpine")
    container.start()

    # Wait until we can actually open a connection
    async def _wait_ready() -> None:
        url = container.get_connection_url().replace("psycopg2", "asyncpg")
        for _ in range(30):
            try:
                conn = await asyncpg.connect(url)
                await conn.close()
                return
            except (asyncpg.CannotConnectNowError, ConnectionRefusedError):
                await asyncio.sleep(0.5)
        raise TimeoutError("postgres not ready")

    asyncio.run(_wait_ready())
    yield container
    container.stop()
```

`testcontainers` 4.x exposes `wait_for(predicate)` and `wait_for_logs(...)` helpers — use them when available:

```python
container.start()
container.wait_container_is_ready()
```

### Rule 6 — Log capture on failure

When an integration test fails, the container's logs are the most useful debugging signal. Capture them automatically:

```python
@pytest.fixture(scope="session")
def postgres_container(request) -> Iterator[PostgresContainer]:
    container = PostgresContainer("postgres:16-alpine")
    container.start()

    def _dump_logs_on_failure() -> None:
        if request.session.testsfailed:
            print("\n=== Postgres container logs ===")
            print(container.get_logs()[0].decode("utf-8", errors="replace"))
            print("===")

    request.addfinalizer(_dump_logs_on_failure)
    yield container
    container.stop()
```

The finalizer runs AFTER all tests in the session. If any test failed, logs print to stdout. CI captures stdout — engineers see why the container misbehaved without re-running.

### Rule 7 — Image version pinning

NEVER use `:latest`:

```python
# WRONG — image changes under your feet
PostgresContainer("postgres:latest")

# RIGHT — pin major version + use Alpine for size
PostgresContainer("postgres:16-alpine")
```

Pin to the same version your production deployment uses. SDK should test against the version users are on, not the bleeding edge.

For multi-version coverage, parametrize:

```python
@pytest.fixture(scope="session", params=["postgres:15-alpine", "postgres:16-alpine"])
def postgres_container(request) -> Iterator[PostgresContainer]:
    container = PostgresContainer(request.param)
    container.start()
    yield container
    container.stop()
```

The session runs the integration suite TWICE — once per version. CI cost doubles; only do this when both versions are supported targets.

### Rule 8 — Network and port allocation

Containers bind to dynamic host ports. Get the URL via the testcontainers helper, not hardcoded:

```python
url = container.get_connection_url()                # ✓ dynamic
url = "postgresql://localhost:5432/test"            # ✗ collides on parallel CI
```

For services without a `get_connection_url()` helper, build it from the dynamic port:

```python
from testcontainers.core.container import DockerContainer

container = DockerContainer("nats:2.10-alpine").with_exposed_ports(4222)
container.start()
host = container.get_container_host_ip()
port = container.get_exposed_port(4222)
nats_url = f"nats://{host}:{port}"
```

### Rule 9 — Reuse mode (development convenience, NOT for CI)

For tight inner-loop dev, container reuse skips startup on re-run:

```python
container = PostgresContainer("postgres:16-alpine").with_kwargs(reuse=True)
container.start()
```

Reuse keeps the container alive after the test session, reusing it on the next run. ONLY use for dev convenience — CI should always start fresh containers (reuse leaks state across pipeline runs).

Document the toggle:

```python
@pytest.fixture(scope="session")
def postgres_container() -> Iterator[PostgresContainer]:
    reuse = os.environ.get("TC_REUSE", "0") == "1"
    container = PostgresContainer("postgres:16-alpine")
    if reuse:
        container = container.with_kwargs(reuse=True)
    container.start()
    yield container
    if not reuse:
        container.stop()
```

`TC_REUSE=1 pytest` for dev iteration; CI doesn't set the env var; CI starts fresh.

### Rule 10 — Docker socket on remote engines

`testcontainers` reads `DOCKER_HOST` env var. On Linux with Docker Desktop / Colima / OrbStack:

```bash
# Colima
export DOCKER_HOST=unix:///Users/$USER/.colima/default/docker.sock

# OrbStack
export DOCKER_HOST=unix:///Users/$USER/.orbstack/run/docker.sock
```

Add a CI-friendly `DOCKER_HOST` discovery to conftest.py for cross-platform compatibility:

```python
def _discover_docker_host() -> str | None:
    if "DOCKER_HOST" in os.environ:
        return os.environ["DOCKER_HOST"]
    candidates = [
        f"/Users/{os.environ.get('USER')}/.colima/default/docker.sock",
        f"/Users/{os.environ.get('USER')}/.orbstack/run/docker.sock",
        "/var/run/docker.sock",
    ]
    for path in candidates:
        if os.path.exists(path):
            return f"unix://{path}"
    return None
```

## Service-specific recipes

### PostgreSQL

```python
from testcontainers.postgres import PostgresContainer
import asyncpg

@pytest.fixture(scope="session")
def postgres_container() -> Iterator[PostgresContainer]:
    with PostgresContainer("postgres:16-alpine") as container:
        yield container


@pytest.fixture
async def pg_pool(postgres_container) -> AsyncIterator[asyncpg.Pool]:
    url = postgres_container.get_connection_url().replace("psycopg2", "asyncpg")
    pool = await asyncpg.create_pool(url, min_size=1, max_size=4)
    yield pool
    await pool.close()
```

Note: `testcontainers.postgres` returns a `psycopg2`-flavored URL by default. Strip / replace for asyncpg.

### Redis

```python
from testcontainers.redis import RedisContainer
import redis.asyncio as redis

@pytest.fixture(scope="session")
def redis_container() -> Iterator[RedisContainer]:
    with RedisContainer("redis:7-alpine") as container:
        yield container


@pytest.fixture
async def redis_client(redis_container) -> AsyncIterator[redis.Redis]:
    host = redis_container.get_container_host_ip()
    port = redis_container.get_exposed_port(6379)
    client = redis.Redis(host=host, port=port, decode_responses=False)
    await client.flushdb()                         # clean slate per test
    yield client
    await client.flushdb()
    await client.aclose()
```

### Kafka

```python
from testcontainers.kafka import KafkaContainer

@pytest.fixture(scope="session")
def kafka_container() -> Iterator[KafkaContainer]:
    with KafkaContainer("confluentinc/cp-kafka:7.6.0") as container:
        yield container


@pytest.fixture
def kafka_bootstrap(kafka_container) -> str:
    return kafka_container.get_bootstrap_server()
```

Kafka is the slowest container (45s+ to ready). ALWAYS session-scoped. Per-test isolation via topic naming:

```python
topic_name = f"test-{uuid.uuid4().hex[:8]}"
```

### MinIO (S3-compatible)

```python
from testcontainers.minio import MinioContainer
import aioboto3

@pytest.fixture(scope="session")
def minio_container() -> Iterator[MinioContainer]:
    with MinioContainer("minio/minio:latest") as container:
        yield container


@pytest.fixture
async def s3_client(minio_container) -> AsyncIterator:
    config = minio_container.get_config()
    session = aioboto3.Session()
    async with session.client(
        "s3",
        endpoint_url=f"http://{config['endpoint']}",
        aws_access_key_id=config["access_key"],
        aws_secret_access_key=config["secret_key"],
        region_name="us-east-1",
    ) as client:
        yield client
```

### NATS

```python
from testcontainers.core.container import DockerContainer
import nats

@pytest.fixture(scope="session")
def nats_container() -> Iterator[DockerContainer]:
    container = DockerContainer("nats:2.10-alpine").with_exposed_ports(4222)
    container.start()
    container.wait_container_is_ready()
    yield container
    container.stop()


@pytest.fixture
async def nats_client(nats_container) -> AsyncIterator:
    host = nats_container.get_container_host_ip()
    port = nats_container.get_exposed_port(4222)
    nc = await nats.connect(f"nats://{host}:{port}")
    yield nc
    await nc.close()
```

### MongoDB

```python
from testcontainers.mongodb import MongoDbContainer
import motor.motor_asyncio

@pytest.fixture(scope="session")
def mongo_container() -> Iterator[MongoDbContainer]:
    with MongoDbContainer("mongo:7.0") as container:
        yield container


@pytest.fixture
async def mongo_client(mongo_container) -> AsyncIterator:
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_container.get_connection_url())
    yield client
    client.close()
```

## GOOD: full conftest example

```python
# tests/integration/conftest.py
"""Session-scoped testcontainer fixtures."""
import os
from collections.abc import Iterator

import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer


def _docker_available() -> bool:
    try:
        import docker
        docker.from_env().ping()
        return True
    except Exception:
        return False


def pytest_collection_modifyitems(config, items) -> None:
    if _docker_available():
        return
    skip = pytest.mark.skip(reason="Docker not available")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip)


@pytest.fixture(scope="session")
def postgres_container(request) -> Iterator[PostgresContainer]:
    container = PostgresContainer("postgres:16-alpine")
    container.start()

    def _dump_logs() -> None:
        if request.session.testsfailed:
            print("\n=== Postgres logs ===")
            print(container.get_logs()[0].decode("utf-8", errors="replace"))

    request.addfinalizer(_dump_logs)
    yield container
    container.stop()


@pytest.fixture(scope="session")
def redis_container(request) -> Iterator[RedisContainer]:
    container = RedisContainer("redis:7-alpine")
    container.start()

    def _dump_logs() -> None:
        if request.session.testsfailed:
            print("\n=== Redis logs ===")
            print(container.get_logs()[0].decode("utf-8", errors="replace"))

    request.addfinalizer(_dump_logs)
    yield container
    container.stop()


@pytest.fixture(scope="session")
def postgres_url(postgres_container: PostgresContainer) -> str:
    return postgres_container.get_connection_url().replace("psycopg2", "asyncpg")
```

The conftest demonstrates: Docker gate (Rule 4), session-scoped containers (Rule 2), log capture on failure (Rule 6), pinned versions (Rule 7), per-service helpers.

## BAD anti-patterns

```python
# 1. Function-scoped containers (slow)
@pytest.fixture                              # default scope=function
def postgres():
    with PostgresContainer(...) as c:
        yield c                              # 10s startup × every test

# 2. :latest tag
PostgresContainer("postgres:latest")        # version drift

# 3. Hardcoded port
url = "postgresql://localhost:5432/test"    # CI parallelism collides

# 4. No state reset between tests
async def test_a(pg_pool):
    await insert_user(pg_pool, "alice")
async def test_b(pg_pool):
    users = await list_users(pg_pool)
    assert users == []                       # FAILS — leftover from test_a

# 5. Container kept alive after session (no .stop())
container.start()
yield container                              # missing container.stop() / __exit__

# 6. Synchronous DB driver in async test
@pytest.fixture
def conn(postgres_url):
    return psycopg2.connect(postgres_url)    # blocks event loop in async tests

# 7. No Docker availability gate
# CI without Docker → cryptic "Cannot connect to Docker daemon" errors

# 8. No log capture on failure
# Test fails → engineer can't see WHY without reproducing locally

# 9. Reuse=True in CI
container = PostgresContainer(...).with_kwargs(reuse=True)
# CI runs leak state across pipelines

# 10. Marker not registered
@pytest.mark.integration                     # PytestUnknownMarkWarning
```

## Tooling configuration

```toml
[project.optional-dependencies]
test-integration = [
    "testcontainers[postgresql,redis,kafka,minio,mongodb] >= 4.0",
    "asyncpg >= 0.29",                     # if using Postgres
    "redis >= 5.0",                        # if using Redis
    "aiokafka >= 0.10",                    # if using Kafka
    "aioboto3 >= 12",                      # if using MinIO
    "motor >= 3.4",                        # if using Mongo
    "nats-py >= 2.6",                      # if using NATS
    "docker >= 7.0",                       # for the availability check
]

[tool.pytest.ini_options]
markers = [
    "integration: requires testcontainers / docker",
]
testpaths = ["tests"]
```

Split unit and integration test runs in CI:

```yaml
# .github/workflows/ci.yml
- name: Unit tests
  run: pytest -m "not integration"
- name: Integration tests
  run: pytest -m "integration"
```

## Cross-references

- `python-pytest-patterns` Rule 3 (fixture scope), Rule 7 (marker registration), Rule 4 (yield for cleanup).
- `python-asyncio-patterns` — async fixtures driving the containers.
- `python-mock-strategy` — for unit tests, prefer in-memory fakes; reserve testcontainers for integration tier.
- `python-asyncio-leak-prevention` — close container clients in `__aexit__` to keep leak fixtures green.
- `python-mypy-strict-typing` — type the fixture return types as `Iterator[...]` / `AsyncIterator[...]`.
- `sdk-integration-flake-hunter-python` — runs integration tests with `--count=3` to catch flake.
- `sdk-existing-api-analyzer-python` — captures integration-test baseline.
- `sdk-convention-devil-python` C-14 — design-rule enforcement.
