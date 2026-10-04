---
name: integration-e2e-testing
description: Integration and end-to-end testing patterns for VoxAgent. Use when writing API integration tests, pipeline E2E tests, designing fixtures, or building test infrastructure beyond unit tests. Triggers on tasks involving tests/integration/, tests/e2e/, conftest.py, or any test spanning multiple modules.
---

# Integration & E2E Testing Patterns for VoxAgent

Guidelines for writing reliable integration and end-to-end tests that verify VoxAgent's modules work together correctly. Covers test architecture, API testing with httpx, pipeline E2E flows, fixture design, and test data management.

## When to Apply

Reference these guidelines when:
- Writing tests that span multiple modules (core + providers, api + skills)
- Testing FastAPI endpoints with `TestClient` or `httpx.AsyncClient`
- Verifying the full voice pipeline (STT -> Intent -> LLM -> Skill -> TTS)
- Designing shared test fixtures in `conftest.py`
- Setting up test markers and CI test stages
- Debugging flaky or slow integration tests

## Proposed Test Directory Structure

```
tests/
├── conftest.py              # Shared fixtures (top-level)
├── unit/                    # Fast, isolated unit tests
│   ├── conftest.py
│   ├── test_intent.py
│   └── test_safety.py
├── integration/             # Multi-module integration tests
│   ├── conftest.py          # Integration-specific fixtures
│   ├── test_pipeline.py     # Core pipeline integration
│   ├── test_providers.py    # Provider integration
│   └── test_memory.py       # Database integration
├── api/                     # API endpoint tests
│   ├── conftest.py          # TestClient fixtures
│   ├── test_chat.py
│   └── test_health.py
└── e2e/                     # Full end-to-end tests
    ├── conftest.py          # E2E fixtures (mock audio, etc.)
    └── test_voice_pipeline.py
```

## Rule Categories by Priority

| Priority | Category | Impact | Applies to |
|----------|----------|--------|------------|
| 1 | Test Architecture | CRITICAL | All test code |
| 2 | API Integration Tests | HIGH | tests/api/ |
| 3 | Pipeline E2E Tests | HIGH | tests/e2e/ |
| 4 | Fixture Design | MEDIUM | conftest.py |
| 5 | Test Data & Mocking | MEDIUM | All test code |

## Quick Reference

### 1. Test Architecture (CRITICAL)

- `itest-layer-separation` — Clearly separate test layers. Each layer has different scope and speed:
  ```
  Unit tests:        Single function/class, no I/O, < 10ms each
  Integration tests: Multiple modules, mocked external APIs, < 500ms each
  API tests:         HTTP endpoints via TestClient, mocked providers, < 1s each
  E2E tests:         Full pipeline, mocked audio/TTS, < 5s each
  ```

- `itest-naming` — Name test files and functions to reflect scope and intent:
  ```python
  # Unit: test_{module}.py
  def test_intent_classifier_returns_open_app():

  # Integration: test_{feature}_integration.py
  async def test_pipeline_routes_to_correct_skill():

  # API: test_{endpoint}.py
  async def test_chat_endpoint_returns_streaming_response():

  # E2E: test_{scenario}_e2e.py
  async def test_voice_command_opens_application():
  ```

- `itest-mock-at-boundary` — Mock at module boundaries, not inside implementations. Replace the provider, not the HTTP call:
  ```python
  # Good: mock the provider interface
  mock_llm = AsyncMock(spec=LLMProvider)
  mock_llm.chat.return_value = "Opening Spotify"
  pipeline = Pipeline(llm=mock_llm)

  # Bad: mock internal HTTP calls
  with patch("httpx.AsyncClient.post"):  # too coupled to implementation
      ...
  ```

- `itest-no-sleep` — Never use `time.sleep()` or `asyncio.sleep()` in tests. Use events, conditions, or `asyncio.wait_for()`:
  ```python
  # Good: event-driven
  result_ready = asyncio.Event()
  async def on_complete(result):
      result_ready.set()
  await asyncio.wait_for(result_ready.wait(), timeout=5.0)

  # Bad: arbitrary sleep
  await asyncio.sleep(2)  # flaky, slow
  assert result is not None
  ```

### 2. API Integration Tests (HIGH)

- `itest-testclient` — Use httpx `AsyncClient` with `ASGITransport` for async FastAPI testing:
  ```python
  from httpx import ASGITransport, AsyncClient
  from api.main import app

  @pytest.fixture
  async def client():
      transport = ASGITransport(app=app)
      async with AsyncClient(transport=transport, base_url="http://test") as client:
          yield client

  async def test_health_endpoint(client: AsyncClient):
      response = await client.get("/health")
      assert response.status_code == 200
      assert response.json()["status"] == "healthy"
  ```

- `itest-auth-fixtures` — Create reusable auth fixtures for authenticated endpoints:
  ```python
  @pytest.fixture
  def auth_headers() -> dict[str, str]:
      token = "test-token-for-ci"
      return {"Authorization": f"Bearer {token}"}

  async def test_execute_requires_auth(client: AsyncClient):
      response = await client.post("/execute", json={"skill": "test"})
      assert response.status_code == 401

  async def test_execute_with_auth(client: AsyncClient, auth_headers):
      response = await client.post(
          "/execute",
          json={"skill": "open_app", "params": {"name": "spotify"}},
          headers=auth_headers,
      )
      assert response.status_code == 200
  ```

- `itest-error-scenarios` — Test error paths explicitly. Every endpoint needs tests for: 400 (bad input), 401 (no auth), 404 (not found), 503 (provider down):
  ```python
  async def test_chat_with_invalid_model(client: AsyncClient, auth_headers):
      response = await client.post(
          "/chat",
          json={"messages": [{"role": "user", "content": "hi"}], "model": "nonexistent"},
          headers=auth_headers,
      )
      assert response.status_code == 404
      assert "model" in response.json()["detail"].lower()
  ```

- `itest-response-schema` — Validate response shape, not just status code. Use Pydantic for assertion:
  ```python
  from api.schemas import ChatResponse

  async def test_chat_response_schema(client: AsyncClient, auth_headers):
      response = await client.post("/chat", json=payload, headers=auth_headers)
      data = ChatResponse.model_validate(response.json())  # raises if invalid
      assert data.model_used in VALID_MODELS
      assert data.latency_ms > 0
  ```

### 3. Pipeline E2E Tests (HIGH)

- `itest-pipeline-flow` — Test the full pipeline from transcript to skill execution:
  ```python
  async def test_full_pipeline_open_app(mock_providers):
      pipeline = VoicePipeline(
          stt=mock_providers.stt,
          intent=mock_providers.intent,
          llm=mock_providers.llm,
          executor=mock_providers.executor,
          tts=mock_providers.tts,
      )
      mock_providers.stt.transcribe.return_value = "open spotify"
      mock_providers.intent.classify.return_value = Intent(action="open_app", params={"app": "spotify"})

      result = await pipeline.process(audio=MOCK_AUDIO)

      assert result.skill_executed == "open_app"
      mock_providers.tts.speak.assert_called_once()
  ```

- `itest-provider-fallback-e2e` — Test that provider fallback chains work end-to-end:
  ```python
  async def test_llm_fallback_on_primary_failure():
      primary = AsyncMock(spec=LLMProvider)
      primary.chat.side_effect = ProviderUnavailableError("rate limited")
      fallback = AsyncMock(spec=LLMProvider)
      fallback.chat.return_value = "I opened Spotify"

      chain = ProviderChain([primary, fallback])
      result = await chain.chat(messages)

      assert result == "I opened Spotify"
      primary.chat.assert_called_once()
      fallback.chat.assert_called_once()
  ```

- `itest-concurrent-sessions` — Verify multiple voice sessions don't interfere:
  ```python
  async def test_concurrent_sessions_isolated():
      session_a = await create_session("user_a")
      session_b = await create_session("user_b")

      await session_a.process("open spotify")
      await session_b.process("what's the weather")

      assert session_a.last_skill != session_b.last_skill
      assert session_a.context.history != session_b.context.history
  ```

### 4. Fixture Design (MEDIUM)

- `itest-conftest-layered` — Layer conftest.py files. Each test directory has its own with appropriate scope:
  ```python
  # tests/conftest.py — shared across all test types
  @pytest.fixture(scope="session")
  def event_loop():
      loop = asyncio.new_event_loop()
      yield loop
      loop.close()

  @pytest.fixture
  def mock_keyring(monkeypatch):
      monkeypatch.setattr("keyring.get_password", lambda *a: "test-key")

  # tests/api/conftest.py — API-specific
  @pytest.fixture
  async def client(mock_keyring):
      transport = ASGITransport(app=app)
      async with AsyncClient(transport=transport, base_url="http://test") as c:
          yield c

  # tests/e2e/conftest.py — E2E-specific
  @pytest.fixture
  def mock_audio() -> bytes:
      return b"\x00" * 16000 * 2  # 1 second of silence at 16kHz mono
  ```

- `itest-fixture-scope` — Use the narrowest fixture scope that makes sense:
  ```
  function (default): New instance per test — most isolated
  class:             Shared within a test class
  module:            Shared within a file — for expensive setup
  session:           Shared across all tests — for event loop, DB schema
  ```

- `itest-fixture-composition` — Compose fixtures from smaller, focused fixtures:
  ```python
  @pytest.fixture
  def mock_stt():
      stt = AsyncMock(spec=STTProvider)
      stt.transcribe.return_value = "hello world"
      return stt

  @pytest.fixture
  def mock_llm():
      llm = AsyncMock(spec=LLMProvider)
      llm.chat.return_value = "Hi there!"
      return llm

  @pytest.fixture
  def mock_providers(mock_stt, mock_llm):
      return MockProviders(stt=mock_stt, llm=mock_llm)
  ```

- `itest-fixture-cleanup` — Always clean up resources in fixtures. Use `yield`, not `return`, when cleanup is needed:
  ```python
  @pytest.fixture
  async def db():
      conn = await aiosqlite.connect(":memory:")
      await init_schema(conn)
      yield conn
      await conn.close()
  ```

### 5. Test Data & Mocking (MEDIUM)

- `itest-factory-functions` — Use factory functions for test data. Never duplicate test object creation:
  ```python
  def make_message(role: str = "user", content: str = "test") -> Message:
      return Message(role=role, content=content)

  def make_intent(action: str = "open_app", **params) -> Intent:
      return Intent(action=action, parameters=params, confidence=0.95)

  # Usage in tests
  messages = [make_message("user", "open spotify"), make_message("assistant", "ok")]
  ```

- `itest-mock-specificity` — Mock at the right level of specificity. Too broad hides bugs, too narrow is brittle:
  ```python
  # Good: mock the provider (right level)
  mock_llm = AsyncMock(spec=LLMProvider)

  # Too broad: mock the entire registry
  mock_registry = AsyncMock(spec=ProviderRegistry)  # hides routing bugs

  # Too narrow: mock HTTP internals
  with patch("httpx.AsyncClient.post"):  # breaks if implementation changes
  ```

- `itest-deterministic` — Make tests deterministic. Seed random values, freeze time, control async ordering:
  ```python
  from unittest.mock import patch
  import time

  @pytest.fixture
  def frozen_time():
      with patch("time.time", return_value=1700000000.0):
          yield

  async def test_session_expiry(frozen_time):
      session = Session(created_at=time.time())
      assert not session.is_expired  # deterministic
  ```

- `itest-markers` — Use pytest markers to categorize tests. Run fast tests in CI, slow tests in nightly:
  ```python
  # pyproject.toml
  [tool.pytest.ini_options]
  markers = [
      "unit: Fast isolated tests (< 10ms)",
      "integration: Multi-module tests (< 500ms)",
      "api: HTTP endpoint tests (< 1s)",
      "e2e: Full pipeline tests (< 5s)",
      "benchmark: Performance benchmarks",
  ]

  # Usage
  @pytest.mark.integration
  async def test_pipeline_routes_correctly():
      ...

  # CLI
  # Fast CI:   pytest -m "unit or integration"
  # Full CI:   pytest -m "not benchmark"
  # Nightly:   pytest
  ```

## Operational Procedure

### Before writing tests
1. Determine the test layer: unit, integration, API, or E2E
2. Check existing fixtures in `conftest.py` — reuse before creating new ones
3. Identify what to mock: mock at boundaries, not internals

### During testing
1. Write the test name to describe the scenario, not the implementation
2. Follow Arrange-Act-Assert (AAA) structure
3. Test both happy path AND error paths
4. Use markers to categorize the test

### After writing tests
1. Run the full test suite: `pytest -x --tb=short`
2. Check coverage: `pytest --cov=voxagent --cov-report=term-missing`
3. Verify no flaky tests: run 3 times
4. Ensure no real network calls (mock all external APIs)
