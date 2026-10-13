---
name: python-pytest-patterns
description: >
  Use this when authoring or reviewing any test under tests/, designing a new
  fixture and choosing its scope, wiring async tests via pytest-asyncio,
  registering custom markers, or replacing a unittest.TestCase / for-loop with
  idiomatic pytest. Covers function/module/session fixture scope, yield-based
  cleanup, conftest.py placement, parametrize with pytest.param ids,
  asyncio_mode=auto, marker registration in pyproject.toml, monkeypatch for env
  isolation, caplog/capsys/capfd capture, indirect parametrization, skip/xfail,
  pytest.raises with match, fakes vs mocks, and the recommended pyproject
  template (strict-markers, filterwarnings=error).
  Triggers: pytest, fixture, parametrize, conftest, async def test_, @pytest.mark, monkeypatch, tmp_path, caplog, asyncio_mode, pytest.raises, xfail.
---

# python-pytest-patterns (v1.0.0)

## Rationale

`unittest.TestCase` is acceptable Python but the Python pack default is **pytest**. The default is not stylistic: pytest's fixture model (parameter injection, scoped finalization, indirect parametrization) makes it harder to leak setup state between tests, makes test discovery uniform, and integrates with `pytest-asyncio`, `pytest-benchmark`, `pytest-randomly`, `pytest-repeat`, and the testcontainers-python ecosystem the testing-phase agents depend on. Every Python pack agent that runs tests assumes pytest semantics — `sdk-integration-flake-hunter-python` runs `pytest --count=3`, `sdk-benchmark-devil-python` reads `pytest-benchmark` JSON, `sdk-asyncio-leak-hunter-python` ships custom fixtures.

This skill is cited by `code-reviewer-python` (test quality), `sdk-existing-api-analyzer-python` (snapshot baseline parsing), `sdk-integration-flake-hunter-python`, `sdk-benchmark-devil-python`, `sdk-complexity-devil-python`, `sdk-asyncio-leak-hunter-python`, `documentation-agent-python` (doctest mode), and `sdk-convention-devil-python` (C-14).

## Activation signals

- Designing or reviewing any test file under `tests/`.
- Writing a new pytest fixture; deciding scope (function / module / session).
- Setting up integration tests that use testcontainers.
- Adding async tests that need `asyncio_mode`.
- Code review surfaces `unittest.TestCase` usage.
- Code review surfaces a for-loop in a test instead of `@pytest.mark.parametrize`.

## Core rules

### Rule 1 — Pytest, not unittest

Tests live under `tests/`. Files named `test_<module>.py`. Functions named `test_<behavior>`. Classes named `Test<Subject>` (no `__init__`).

```python
# tests/test_client.py
def test_client_publish_succeeds(): ...
def test_client_publish_fails_on_invalid_topic(): ...

class TestClient:
    def test_construction(self): ...
    def test_close_is_idempotent(self): ...
```

Avoid `unittest.TestCase` subclasses. They prevent fixture injection, cannot use `@pytest.mark.parametrize`, and require `self.assertEqual` instead of plain `assert`. If you inherit a TestCase from a third-party (e.g., `TransactionTestCase` from Django), wrap it in pytest.

### Rule 2 — Parametrize over for-loops

```python
# WRONG — for-loop in a test
def test_validators():
    cases = [("foo", True), ("", False), ("a" * 256, False)]
    for input_, expected in cases:
        assert is_valid(input_) is expected
        # First failure stops the loop; you don't see the others.

# RIGHT — parametrize
@pytest.mark.parametrize(
    "input_,expected",
    [
        pytest.param("foo", True, id="happy-path"),
        pytest.param("", False, id="empty"),
        pytest.param("a" * 256, False, id="too-long"),
    ],
)
def test_is_valid(input_: str, expected: bool) -> None:
    assert is_valid(input_) is expected
```

`pytest.param(..., id="...")` produces deterministic test IDs (`test_is_valid[empty]`) which downstream tools (`sdk-integration-flake-hunter-python`, CI dashboards) cite. Never use `pytest.param(..., id=str(input_))` — special characters break test selection.

### Rule 3 — Fixture scope is the most-frequently-mis-set knob

```python
# Function scope (default) — recreated for every test. Use for:
@pytest.fixture
def fresh_config() -> Config:
    return Config(timeout=1.0)

# Module scope — created once per test module. Use for expensive but read-only setup.
@pytest.fixture(scope="module")
def shared_db_schema() -> Schema:
    return Schema.from_file("tests/data/schema.json")

# Session scope — created once per pytest invocation. Use for testcontainers.
@pytest.fixture(scope="session")
def postgres_container() -> Iterator[PostgresContainer]:
    container = PostgresContainer("postgres:16")
    container.start()
    yield container
    container.stop()
```

The risk in non-default scopes: state leaks across tests in the same module/session. ANY fixture with mutable state needs `scope="function"` unless you can guarantee no test mutates it. Common bug: a session-scoped `Client` whose internal cache silently contaminates the next test's behavior.

### Rule 4 — `yield` for fixtures with cleanup

```python
@pytest.fixture
def temp_log_dir(tmp_path: Path) -> Iterator[Path]:
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    yield log_dir
    # cleanup runs after the test, including on failure
    shutil.rmtree(log_dir, ignore_errors=True)
```

Do NOT use `request.addfinalizer(...)` for new fixtures — it predates `yield` and is now a legacy pattern. The `yield` form is cleaner and harder to forget.

`tmp_path` (per-test) and `tmp_path_factory` (broader scope) are pytest built-ins; never write to a hardcoded `/tmp/foo` path — concurrent test runners collide.

### Rule 5 — `conftest.py` placement

Per-directory shared fixtures live in `tests/<dir>/conftest.py`. Top-level fixtures shared across all tests live in `tests/conftest.py`. Avoid placing conftest.py at repo root unless you specifically need fixtures available to non-test code (rare).

```
tests/
  conftest.py              # cross-cutting fixtures (Config defaults, etc.)
  unit/
    conftest.py            # unit-only fixtures (in-memory fakes)
    test_client.py
  integration/
    conftest.py            # testcontainer fixtures (session-scoped)
    test_client_e2e.py
```

### Rule 6 — Async tests via pytest-asyncio in `auto` mode

Configure once in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

Then every `async def test_...` runs without per-test decoration:

```python
async def test_client_publish_async(client: Client) -> None:
    await client.publish("topic", b"hi")
    assert client.last_publish.acked
```

Avoid `asyncio_mode = "strict"` for SDK code unless mixing sync and async tests in the same project — strict requires `@pytest.mark.asyncio` on every async test, which is noise.

Async fixtures use `async def` + `yield`:

```python
@pytest.fixture
async def client(config: Config) -> AsyncIterator[Client]:
    async with Client(config) as c:
        yield c
```

### Rule 7 — Custom markers REGISTER in pyproject.toml

```toml
[tool.pytest.ini_options]
markers = [
    "integration: requires running infrastructure (testcontainers, docker)",
    "slow: takes > 5 seconds",
    "leak_hunt: targeted by sdk-asyncio-leak-hunter-python",
    "perf: targeted by sdk-benchmark-devil-python",
]
```

Without registration, `@pytest.mark.integration` works but emits a `PytestUnknownMarkWarning` that taints CI logs. Registered markers also make `pytest --markers` list them for documentation.

Run subsets:

```bash
pytest -m "not integration"   # unit tests only
pytest -m "integration"       # integration only
pytest -m "leak_hunt"         # only leak-hunter targets
```

### Rule 8 — `monkeypatch` for environment / attribute isolation

```python
def test_reads_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MOTADATA_API_KEY", "test-key")
    cfg = Config.from_env()
    assert cfg.api_key == "test-key"
    # auto-reverted after the test, even on assertion failure.
```

Use `monkeypatch.setattr` to replace a function/attribute for the duration of one test (e.g., stub a slow network call). Do NOT mutate `os.environ` directly — your test will leak state into the next test.

### Rule 9 — `caplog` for structured log assertions

```python
def test_publish_emits_warning(client: Client, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING, logger="motadatapysdk.client")
    client.publish_with_retry("topic", b"x")
    warning_records = [r for r in caplog.records if r.levelname == "WARNING"]
    assert len(warning_records) == 1
    assert "retry" in warning_records[0].message
```

`caplog.records` returns the `LogRecord` objects (typed access to `.levelname`, `.name`, `.message`, `.args`). `caplog.text` is the rendered output (string match only — fragile).

### Rule 10 — `capfd` / `capsys` for stdout/stderr

```python
def test_cli_help(capsys: pytest.CaptureFixture[str]) -> None:
    main(["--help"])
    out = capsys.readouterr().out
    assert "Usage: motadata" in out
```

`capfd` captures at the file-descriptor level (catches subprocess output); `capsys` captures Python's `sys.stdout`/`sys.stderr`. Pick `capfd` when testing CLIs that may shell out.

### Rule 11 — Fixture parametrization (indirect)

When the same test should run against multiple variants of a fixture:

```python
@pytest.fixture
def client_with_backend(request: pytest.FixtureRequest) -> Client:
    backend_url = request.param
    return Client(Config(backend_url=backend_url))


@pytest.mark.parametrize(
    "client_with_backend",
    ["http://localhost:8080", "http://localhost:8081"],
    indirect=True,
)
def test_publish(client_with_backend: Client) -> None:
    client_with_backend.publish("topic", b"x")
```

`indirect=True` means the parametrize value is fed INTO the fixture, not directly into the test. Use this for matrix testing without writing a test loop.

### Rule 12 — Skip / xfail / skipif

```python
@pytest.mark.skipif(sys.platform == "win32", reason="POSIX-only path")
def test_unix_socket(): ...

@pytest.mark.xfail(reason="upstream issue #123, fix in next release")
def test_known_broken(): ...

if not docker_available():
    pytest.skip("docker not available", allow_module_level=True)
```

`xfail` differs from `skip`: xfail RUNS the test and asserts it fails; if it unexpectedly passes, that's a `XPASS` warning (now you can remove the marker). `skip` does not run the test at all. Prefer `xfail(strict=True)` if you want XPASS to fail the build.

### Rule 13 — `pytest.raises` for expected exceptions

```python
def test_invalid_topic_raises(client: Client) -> None:
    with pytest.raises(ValidationError, match="topic must not be empty"):
        client.publish("", b"x")

# For exception chains:
def test_chained(client: Client) -> None:
    with pytest.raises(NetworkError) as exc_info:
        client.publish("topic", b"x")
    assert isinstance(exc_info.value.__cause__, ConnectionError)
```

`match` uses `re.search` against `str(exc)`. Always pin the match — a bare `pytest.raises(Exception)` masks unrelated breakage.

### Rule 14 — Test doubles: prefer narrow fakes

For SDK test doubles, prefer in-memory fakes over `unittest.mock.Mock` when possible. Mocks check call patterns; fakes check behavior. Behavior is what consumers care about.

```python
# Fake (preferred for non-trivial behavior)
class FakeBackend:
    def __init__(self) -> None:
        self.published: list[tuple[str, bytes]] = []
    async def post(self, url: str, data: bytes) -> None:
        self.published.append((url, data))

async def test_client_publish(monkeypatch) -> None:
    fake = FakeBackend()
    client = Client(Config(...), _backend=fake)
    await client.publish("topic", b"x")
    assert fake.published == [("https://...", b"x")]
```

Use `unittest.mock.AsyncMock` ONLY for narrow assertions on call patterns (was-it-called, was-it-called-with) — the kinds of assertions a behavioral fake cannot make.

### Rule 15 — `pytest.fixture` vs module-level constants

```python
# WRONG — module-level mutable state
TEST_CONFIG = Config(timeout=1.0)   # mutated by tests; leaks across tests

# RIGHT — fixture
@pytest.fixture
def test_config() -> Config:
    return Config(timeout=1.0)
```

Module-level constants are FINE for immutable values (e.g., `EXAMPLE_PAYLOAD = b"hello"`). Anything mutable, anything that holds resources, anything depending on environment — fixture.

## GOOD: integration test against testcontainers

```python
# tests/integration/conftest.py
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_url() -> Iterator[str]:
    with PostgresContainer("postgres:16") as pg:
        yield pg.get_connection_url()


# tests/integration/test_storage.py
import pytest
pytestmark = pytest.mark.integration

async def test_storage_roundtrip(postgres_url: str) -> None:
    storage = Storage(Config(db_url=postgres_url))
    async with storage:
        await storage.put("key", b"value")
        assert await storage.get("key") == b"value"
```

`pytestmark` at module level marks every test in the file with `@pytest.mark.integration`.

## BAD anti-patterns

```python
# 1. unittest.TestCase
class TestThing(unittest.TestCase):
    def test_x(self): self.assertEqual(...)
# Use pytest functions; plain `assert`.

# 2. for-loop in test
def test_validate():
    for input_ in [...]:
        assert is_valid(input_)
# Use @pytest.mark.parametrize.

# 3. Session-scoped mutable fixture
@pytest.fixture(scope="session")
def client() -> Client:
    return Client(...)            # cache leaks across tests

# 4. Direct os.environ mutation
def test_thing():
    os.environ["KEY"] = "x"        # leaks
    # use monkeypatch.setenv instead

# 5. Naked pytest.raises(Exception)
with pytest.raises(Exception):
    do_thing()                     # masks unrelated breakage

# 6. Unregistered marker
@pytest.mark.slow                  # warns; register in pyproject.toml

# 7. asyncio_mode=strict + missing decorator
async def test_async():            # silently doesn't run if mode=strict
    ...

# 8. Mocking what you should fake
mock = AsyncMock()
mock.publish.return_value = None
# Better: a small FakeBackend class with verifiable state.
```

## pyproject.toml — pytest configuration template

```toml
[tool.pytest.ini_options]
minversion = "8.0"
addopts = [
    "-ra",                         # short summary for non-passing tests
    "--strict-markers",            # warn on unregistered markers
    "--strict-config",             # warn on misspelled config keys
    "--tb=short",
]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
markers = [
    "integration: requires testcontainers / docker",
    "slow: > 5s",
    "leak_hunt: leak-hunter targets",
    "perf: pytest-benchmark targets",
]
filterwarnings = [
    "error",                       # warnings are errors
    "ignore::DeprecationWarning:third_party_library.*",
]
```

`filterwarnings = ["error"]` is aggressive but pays off — surfaces deprecated APIs early. Allowlist deprecations from third-party deps you can't control; never broaden to `"ignore::DeprecationWarning"`.

## Cross-references

- `python-asyncio-patterns` — patterns the async tests verify.
- `python-mock-strategy` (when authored) — when to fake vs mock.
- `python-doctest-patterns` — doctest examples in docstrings (run via `pytest --doctest-modules`).
- `tdd-patterns` (shared) — RED/GREEN/REFACTOR cycle the tests follow.
- `sdk-existing-api-analyzer-python` — how baseline test results are captured.
