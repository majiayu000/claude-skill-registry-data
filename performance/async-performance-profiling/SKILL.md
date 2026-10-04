---
name: async-performance-profiling
description: Async performance profiling and latency optimization patterns for VoxAgent. Use when profiling async code, optimizing pipeline latency, measuring provider performance, or identifying bottlenecks. Triggers on tasks involving performance, latency, profiling, benchmarking, or slow pipeline execution.
---

# Async Performance Profiling for VoxAgent

Guidelines for profiling, measuring, and optimizing async Python performance across VoxAgent's voice pipeline. Covers event loop health, pipeline instrumentation, provider latency, and benchmarking.

## When to Apply

Reference these guidelines when:
- The voice pipeline feels slow (total latency > 5 seconds)
- Adding instrumentation or metrics to any module
- Profiling a provider for latency or throughput
- Investigating event loop blocking or stalls
- Writing performance benchmarks or regression tests
- Optimizing resource usage (memory, connections, file handles)

## VoxAgent Latency Budget

Total target: **< 5 seconds** end-to-end (wake word to TTS playback)

| Stage | Budget | Module | Notes |
|-------|--------|--------|-------|
| Wake Word Detection | ~0ms | system/ | Always-on, near-zero latency |
| Speech-to-Text | 500ms | providers/stt | Depends on audio length |
| Intent Classification | 50ms | core/intent | Local model or regex |
| LLM Response | 3000ms | providers/llm | Largest budget, streaming helps |
| Skill Execution | 2000ms | skills/ | Varies widely by skill |
| Text-to-Speech | 800ms | providers/tts | Can start before full response |

## Rule Categories by Priority

| Priority | Category | Impact | Applies to |
|----------|----------|--------|------------|
| 1 | Event Loop Health | CRITICAL | All async code |
| 2 | Pipeline Instrumentation | HIGH | core/ |
| 3 | Provider Latency | HIGH | providers/ |
| 4 | Memory & Resources | MEDIUM | All modules |
| 5 | Benchmarking | MEDIUM | tests/ |

## Quick Reference

### 1. Event Loop Health (CRITICAL)

- `perf-no-sync-in-async` — NEVER run synchronous/blocking code in async functions. Common violations:
  ```python
  # Bad: blocks event loop
  data = open("file.txt").read()           # use aiofiles
  result = requests.get(url)               # use httpx
  time.sleep(1)                            # use asyncio.sleep
  json.loads(huge_string)                  # wrap in asyncio.to_thread()
  subprocess.run(["cmd"])                  # use asyncio.create_subprocess_exec()

  # Good: non-blocking
  async with aiofiles.open("file.txt") as f:
      data = await f.read()
  ```

- `perf-loop-monitor` — Detect event loop blocking with a monitor in development:
  ```python
  import asyncio

  LOOP_BLOCK_THRESHOLD_MS = 100

  def enable_loop_monitor() -> None:
      loop = asyncio.get_event_loop()
      loop.slow_callback_duration = LOOP_BLOCK_THRESHOLD_MS / 1000
      loop.set_debug(True)
  ```

- `perf-gather-bounded` — Use `asyncio.gather()` for parallel I/O, but limit concurrency to avoid overwhelming external services:
  ```python
  MAX_CONCURRENT_REQUESTS = 5

  async def check_all_providers(providers: list[Provider]) -> list[bool]:
      semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

      async def check_with_limit(p: Provider) -> bool:
          async with semaphore:
              return await p.health_check()

      return await asyncio.gather(*[check_with_limit(p) for p in providers])
  ```

- `perf-task-cancellation` — Always handle `asyncio.CancelledError`. Clean up resources on cancellation:
  ```python
  async def long_running_task() -> None:
      try:
          while True:
              await process_next()
      except asyncio.CancelledError:
          await cleanup()
          raise  # re-raise to propagate cancellation
  ```

### 2. Pipeline Instrumentation (HIGH)

- `perf-timing-decorator` — Use a reusable timing decorator for all pipeline stages:
  ```python
  import time
  import functools
  import logging

  logger = logging.getLogger(__name__)

  def timed(stage: str):
      def decorator(fn):
          @functools.wraps(fn)
          async def wrapper(*args, **kwargs):
              start = time.perf_counter()
              try:
                  return await fn(*args, **kwargs)
              finally:
                  elapsed_ms = (time.perf_counter() - start) * 1000
                  logger.info("%s completed in %.1fms", stage, elapsed_ms)
          return wrapper
      return decorator

  # Usage
  @timed("stt")
  async def transcribe(audio: bytes) -> str:
      ...
  ```

- `perf-pipeline-trace` — Collect timing for all pipeline stages into a single trace object:
  ```python
  @dataclass
  class PipelineTrace:
      request_id: str
      stages: dict[str, float] = field(default_factory=dict)

      def record(self, stage: str, elapsed_ms: float) -> None:
          self.stages[stage] = elapsed_ms

      @property
      def total_ms(self) -> float:
          return sum(self.stages.values())

      def over_budget(self, budgets: dict[str, float]) -> list[str]:
          return [s for s, ms in self.stages.items() if ms > budgets.get(s, float("inf"))]
  ```

- `perf-structured-metrics` — Log metrics in structured format for analysis:
  ```python
  logger.info(
      "pipeline_complete",
      extra={
          "request_id": trace.request_id,
          "total_ms": trace.total_ms,
          "stages": trace.stages,
          "over_budget": trace.over_budget(LATENCY_BUDGETS),
      },
  )
  ```

- `perf-budget` — Define and enforce latency budgets. Warn when a stage exceeds its budget:
  ```python
  LATENCY_BUDGETS: dict[str, float] = {
      "stt": 500.0,
      "intent": 50.0,
      "llm": 3000.0,
      "skill": 2000.0,
      "tts": 800.0,
  }

  async def check_budget(trace: PipelineTrace) -> None:
      violations = trace.over_budget(LATENCY_BUDGETS)
      if violations:
          logger.warning("Latency budget exceeded: %s", violations)
  ```

### 3. Provider Latency (HIGH)

- `perf-provider-timing` — Track per-provider latency with rolling averages:
  ```python
  from collections import deque

  ROLLING_WINDOW = 100

  class ProviderMetrics:
      def __init__(self) -> None:
          self._latencies: deque[float] = deque(maxlen=ROLLING_WINDOW)

      def record(self, latency_ms: float) -> None:
          self._latencies.append(latency_ms)

      @property
      def avg_ms(self) -> float:
          return sum(self._latencies) / len(self._latencies) if self._latencies else 0.0

      @property
      def p95_ms(self) -> float:
          if not self._latencies:
              return 0.0
          sorted_vals = sorted(self._latencies)
          idx = int(len(sorted_vals) * 0.95)
          return sorted_vals[idx]
  ```

- `perf-connection-pool` — Reuse HTTP connections. Never create a new `httpx.AsyncClient` per request:
  ```python
  # Good: shared client
  class Provider:
      def __init__(self):
          self._client = httpx.AsyncClient(limits=httpx.Limits(max_connections=10))

  # Bad: client per request
  async def call_api(self):
      async with httpx.AsyncClient() as client:  # new TCP connection each time
          ...
  ```

- `perf-streaming-prefer` — Use streaming responses when available. Start processing before the full response arrives:
  ```python
  async def stream_llm(messages: list[Message]) -> AsyncGenerator[str, None]:
      async with client.stream("POST", url, json=payload) as response:
          async for chunk in response.aiter_text():
              yield chunk
  ```

- `perf-cache-responses` — Cache deterministic responses (embeddings, classifications) with TTL:
  ```python
  from functools import lru_cache
  from asyncio import Lock

  _cache: dict[str, tuple[float, Any]] = {}
  _cache_lock = Lock()
  CACHE_TTL_SECONDS = 300

  async def cached_classify(text: str) -> str:
      async with _cache_lock:
          if text in _cache:
              ts, result = _cache[text]
              if time.time() - ts < CACHE_TTL_SECONDS:
                  return result
      result = await classify(text)
      async with _cache_lock:
          _cache[text] = (time.time(), result)
      return result
  ```

### 4. Memory & Resources (MEDIUM)

- `perf-memory-lifecycle` — Track resource lifecycle. Every resource opened must be closed:
  ```python
  # Good: automatic cleanup
  async with aiosqlite.connect(db_path) as db:
      ...

  # Good: explicit cleanup in shutdown
  async def shutdown(self) -> None:
      await self._client.aclose()
      await self._db.close()
  ```

- `perf-gc-pressure` — Avoid creating excessive temporary objects in hot paths. Reuse buffers:
  ```python
  # Good: reuse buffer
  buffer = bytearray(CHUNK_SIZE)
  async for chunk in audio_stream:
      buffer[:len(chunk)] = chunk
      process(buffer[:len(chunk)])

  # Bad: new bytes object per chunk
  async for chunk in audio_stream:
      process(bytes(chunk))  # allocation per chunk
  ```

- `perf-weak-refs` — Use `weakref` for caches that shouldn't prevent garbage collection of large objects.

### 5. Benchmarking (MEDIUM)

- `perf-benchmark-isolated` — Benchmark one thing at a time. Isolate network, disk, and CPU benchmarks:
  ```python
  @pytest.mark.benchmark
  async def test_intent_classification_speed():
      classifier = IntentClassifier()
      inputs = [make_test_input() for _ in range(100)]

      start = time.perf_counter()
      for inp in inputs:
          await classifier.classify(inp)
      elapsed = time.perf_counter() - start

      avg_ms = (elapsed / len(inputs)) * 1000
      assert avg_ms < 50, f"Intent classification too slow: {avg_ms:.1f}ms (budget: 50ms)"
  ```

- `perf-regression-baseline` — Store baseline measurements. Fail CI if regression exceeds 20%:
  ```python
  BASELINE_MS = {
      "stt_transcribe": 450.0,
      "intent_classify": 35.0,
      "llm_chat": 2500.0,
  }
  REGRESSION_THRESHOLD = 1.2  # 20% regression allowed
  ```

- `perf-profile-async` — Use `pyinstrument` for async profiling (not cProfile, which misses await time):
  ```python
  from pyinstrument import Profiler

  async def profile_pipeline():
      profiler = Profiler(async_mode="enabled")
      profiler.start()
      await run_pipeline(test_input)
      profiler.stop()
      print(profiler.output_text(unicode=True))
  ```

## Operational Procedure

### Before profiling
1. Establish baseline measurements for each pipeline stage
2. Identify the specific stage or operation to optimize
3. Check if the bottleneck is I/O-bound or CPU-bound

### During optimization
1. Apply the `@timed()` decorator to suspect functions
2. Use `PipelineTrace` to collect full pipeline timing
3. Check event loop blocking with debug mode
4. Profile with `pyinstrument` for async code

### After optimization
1. Compare new measurements against the latency budget
2. Add benchmark tests for critical paths
3. Log structured metrics for ongoing monitoring
4. Update baseline measurements if performance improved
