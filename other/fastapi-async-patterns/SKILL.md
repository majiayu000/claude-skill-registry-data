---
name: fastapi-async-patterns
description: FastAPI and async Python patterns for VoxAgent's backend. Use when writing API endpoints, implementing providers, building async pipelines, or testing async code. Triggers on tasks involving api/, providers/, core/ modules, or any async Python code.
---

# FastAPI & Async Python Patterns for VoxAgent

Guidelines for writing correct, performant async Python code across VoxAgent's FastAPI API layer, provider implementations, and core pipeline modules.

## When to Apply

Reference these guidelines when:
- Writing or modifying FastAPI endpoints in `api/routers/`
- Implementing new providers (LLM, STT, TTS, Vision)
- Building async pipelines in `core/` modules
- Writing async tests with pytest-asyncio
- Debugging async/await issues or race conditions

## Rule Categories by Priority

| Priority | Category | Impact | Applies to |
|----------|----------|--------|------------|
| 1 | Async Fundamentals | CRITICAL | All Python |
| 2 | FastAPI Patterns | HIGH | api/ |
| 3 | Provider Implementation | HIGH | providers/ |
| 4 | Error Handling | MEDIUM | All Python |
| 5 | Testing Async | MEDIUM | tests/ |

## Quick Reference

### 1. Async Fundamentals (CRITICAL)

- `async-no-blocking` — NEVER call blocking I/O in async functions. Use `aiohttp`/`httpx` instead of `requests`, `aiofiles` instead of `open()`, `asyncio.sleep()` instead of `time.sleep()`. If you must use blocking code, wrap with `asyncio.to_thread()`.

- `async-gather-parallel` — Run independent async operations concurrently with `asyncio.gather()`:
  ```python
  # Bad: sequential
  result_a = await fetch_a()
  result_b = await fetch_b()

  # Good: parallel
  result_a, result_b = await asyncio.gather(fetch_a(), fetch_b())
  ```

- `async-timeout` — Always set timeouts on external calls. Use `asyncio.wait_for()` or `httpx` timeout parameter:
  ```python
  async with httpx.AsyncClient(timeout=10.0) as client:
      response = await client.get(url)
  ```

- `async-context-manager` — Use `async with` for resources that need cleanup (HTTP clients, DB connections, file handles):
  ```python
  async with aiohttp.ClientSession() as session:
      async with session.get(url) as response:
          data = await response.json()
  ```

- `async-generator` — Use `async for` with async generators for streaming responses:
  ```python
  async def stream_response(provider: LLMProvider) -> AsyncGenerator[str, None]:
      async for chunk in provider.chat_stream(messages):
          yield chunk
  ```

### 2. FastAPI Patterns (HIGH)

- `fastapi-dependency-injection` — Use `Depends()` for shared resources. Never instantiate providers or DB connections inside endpoint functions:
  ```python
  async def get_provider(name: str = Query(...)) -> LLMProvider:
      return registry.get_llm(name)

  @router.post("/chat")
  async def chat(provider: LLMProvider = Depends(get_provider)):
      ...
  ```

- `fastapi-pydantic-models` — All request/response bodies MUST use Pydantic BaseModel. Never accept raw dicts:
  ```python
  class ChatRequest(BaseModel):
      messages: list[Message]
      model: str = "default"

  class ChatResponse(BaseModel):
      response: str
      model_used: str
      latency_ms: float
  ```

- `fastapi-lifespan` — Use lifespan context manager for startup/shutdown, not `@app.on_event`:
  ```python
  @asynccontextmanager
  async def lifespan(app: FastAPI):
      await registry.initialize()
      yield
      await registry.shutdown()

  app = FastAPI(lifespan=lifespan)
  ```

- `fastapi-background-tasks` — Use `BackgroundTasks` for non-critical post-response work (logging, analytics). Never use for critical operations:
  ```python
  @router.post("/execute")
  async def execute(background_tasks: BackgroundTasks):
      result = await skill.execute(intent)
      background_tasks.add_task(log_execution, result)
      return result
  ```

- `fastapi-streaming` — Use `StreamingResponse` with async generators for real-time output:
  ```python
  @router.post("/chat/stream")
  async def chat_stream(request: ChatRequest):
      return StreamingResponse(
          provider.chat_stream(request.messages),
          media_type="text/event-stream",
      )
  ```

- `fastapi-exception-handlers` — Register custom exception handlers. Map domain exceptions to HTTP status codes:
  ```python
  @app.exception_handler(ProviderUnavailableError)
  async def provider_error_handler(request, exc):
      return JSONResponse(status_code=503, content={"detail": str(exc)})
  ```

### 3. Provider Implementation (HIGH)

- `provider-abstract-base` — Every provider MUST implement all abstract methods from its base class in `providers/base.py`. No partial implementations.

- `provider-health-check` — Every provider MUST implement a health check method that verifies connectivity without side effects:
  ```python
  async def health_check(self) -> bool:
      try:
          await self._client.get("/models", timeout=5.0)
          return True
      except Exception:
          return False
  ```

- `provider-retry` — Use exponential backoff for transient failures. Max 3 retries, starting at 1s:
  ```python
  async def _request_with_retry(self, fn, max_retries: int = 3) -> Any:
      for attempt in range(max_retries):
          try:
              return await fn()
          except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
              if attempt == max_retries - 1:
                  raise
              await asyncio.sleep(2 ** attempt)
  ```

- `provider-fallback-chain` — When primary provider fails, fall back through the chain defined in config. Never silently switch providers — log the fallback:
  ```python
  logger.warning("Provider %s failed, falling back to %s", primary.name, fallback.name)
  ```

- `provider-session-reuse` — Create `httpx.AsyncClient` once in `__init__` or lifespan, reuse across requests. Never create a new client per request:
  ```python
  class OpenAIProvider(LLMProvider):
      def __init__(self, config: ProviderConfig):
          self._client = httpx.AsyncClient(
              base_url="https://api.openai.com/v1",
              headers={"Authorization": f"Bearer {config.api_key}"},
              timeout=30.0,
          )
  ```

### 4. Error Handling (MEDIUM)

- `error-async-context` — Always include async context in error logs (which provider, which operation, which request):
  ```python
  logger.error("Chat failed: provider=%s model=%s error=%s", self.name, model, str(e))
  ```

- `error-structured-logging` — Use structured logging with `logging` module. Include request_id, provider, operation:
  ```python
  logger.info("Request completed", extra={"request_id": req_id, "latency_ms": latency})
  ```

- `error-graceful-degradation` — API endpoints should return partial results when possible, not fail entirely:
  ```python
  providers = await asyncio.gather(*health_checks, return_exceptions=True)
  healthy = [p for p in providers if not isinstance(p, Exception)]
  ```

- `error-timeout-separate` — Distinguish timeout errors from other errors. Timeouts often need different recovery:
  ```python
  except asyncio.TimeoutError:
      logger.warning("Provider %s timed out after %ds", name, timeout)
      # Try next provider in chain
  except httpx.HTTPStatusError as e:
      logger.error("Provider %s returned %d", name, e.response.status_code)
      # May need auth refresh
  ```

### 5. Testing Async (MEDIUM)

- `test-pytest-asyncio` — All async tests use `@pytest.mark.asyncio` (or `asyncio_mode = "auto"` in config). Never use `asyncio.run()` in tests:
  ```python
  async def test_provider_chat():
      provider = MockLLMProvider()
      result = await provider.chat(messages)
      assert result == expected
  ```

- `test-mock-async` — Use `AsyncMock` for mocking async methods:
  ```python
  from unittest.mock import AsyncMock

  provider = AsyncMock(spec=LLMProvider)
  provider.chat.return_value = "mocked response"
  ```

- `test-httpx-mock` — Use `respx` or `pytest-httpx` for mocking HTTP calls. Never make real network calls:
  ```python
  @pytest.fixture
  def mock_api(respx_mock):
      respx_mock.post("https://api.openai.com/v1/chat/completions").respond(
          json={"choices": [{"message": {"content": "test"}}]}
      )
  ```

- `test-event-loop` — Never create your own event loop in tests. Let pytest-asyncio manage it. If testing callbacks, use `asyncio.Event`:
  ```python
  async def test_callback():
      received = asyncio.Event()
      async def on_result(data):
          received.set()
      await process(callback=on_result)
      await asyncio.wait_for(received.wait(), timeout=5.0)
  ```

## Operational Procedure

### Before coding
1. Identify if the function needs to be async (does it do I/O?)
2. Check if similar async patterns exist in the codebase
3. Determine error handling strategy (retry? fallback? degrade?)

### During coding
1. Use `async def` for any function that awaits
2. Use `asyncio.gather()` for independent operations
3. Always set timeouts on external calls
4. Use `Depends()` for shared resources in FastAPI

### After coding
1. Verify no blocking calls exist in async functions
2. Check that all `httpx.AsyncClient` instances are properly closed
3. Run async-specific tests: `python -m pytest tests/ -v -k "async or provider or api"`
