---
name: python-otel-instrumentation
description: >
  Use this when adding OpenTelemetry instrumentation to a Python SDK client,
  reviewing a tracer = trace.get_tracer() call inside a function body, finding
  custom or dynamic span attribute keys, or auditing exception handling inside
  an instrumented span. Covers module-scope tracer / meter / counter /
  histogram instruments, start_as_current_span context-manager spans, static
  low-cardinality span names, OTel semantic-convention attribute keys
  (messaging.*, http.*, db.*, rpc.*, net.*), paired record_exception +
  set_status on errors with CancelledError treated as UNSET, contextvars-based
  async propagation across await and create_task, LoggingHandler logs bridge,
  consumer-owned TracerProvider / MeterProvider setup and shutdown.
  Triggers: opentelemetry, otel, tracer, meter, TracerProvider, MeterProvider, start_as_current_span, record_exception, set_status, OTLP, BatchSpanProcessor, semconv.
---

# python-otel-instrumentation (v1.0.0)

## Rationale

Python OpenTelemetry has the same trap as Go's: per-request `get_tracer(...)` allocates, semantic conventions are easy to mis-name, span lifecycle is easy to mis-close, and exporter shutdown is easy to forget (resulting in dropped trailing spans). The Python pack standardizes on the patterns below so every client wires consistently.

This skill is cited by `code-reviewer-python` (review-criteria observability), `sdk-api-ergonomics-devil-python` (E-10 logging surface), `sdk-convention-devil-python` (C-7 OTel wiring), `sdk-perf-architect-python` (instrumentation overhead in perf-budget), and `python-asyncio-patterns` (async tracing across `await` points).

## Activation signals

- Adding instrumentation to a new SDK client.
- Code review surfaces `tracer = trace.get_tracer(__name__)` inside a function body.
- Code review surfaces span attribute keys not in OTel semantic conventions.
- Code review surfaces `try/except: pass` swallowing exceptions inside an instrumented span.
- TPRD §6 declares OTel-required.
- Quick start references `motadatapysdk.observability` or equivalent.

## Core wiring

### Rule 1 — `tracer` and `meter` are MODULE-SCOPED

```python
# motadatapysdk/client.py
from __future__ import annotations

from opentelemetry import metrics, trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Counters / histograms created ONCE at module scope, NOT per-request
publish_counter = meter.create_counter(
    name="motadata.publish.requests",
    unit="1",
    description="Count of publish requests",
)
publish_latency = meter.create_histogram(
    name="motadata.publish.latency",
    unit="s",
    description="Publish request latency",
)
```

`get_tracer(__name__)` is cheap-ish but NOT free (registry lookup + lock). At module scope it runs once at import; in a hot path it amortizes to ~zero. Move it inside a function and you pay the cost per call. The OTel API contract permits caching the tracer at module scope — use it.

`__name__` as the instrumentation library name is the convention; consumers see spans grouped by `motadatapysdk.client`, `motadatapysdk.events`, etc.

### Rule 2 — `start_as_current_span` context manager, not manual start/end

```python
async def publish(self, topic: str, payload: bytes) -> None:
    with tracer.start_as_current_span("motadata.client.publish") as span:
        span.set_attribute("messaging.system", "motadata")
        span.set_attribute("messaging.destination.name", topic)
        span.set_attribute("messaging.message.body.size", len(payload))
        try:
            await self._do_publish(topic, payload)
            publish_counter.add(1, {"topic": topic, "outcome": "success"})
        except NetworkError as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            publish_counter.add(1, {"topic": topic, "outcome": "error"})
            raise
```

The context-manager form auto-ends the span, attaches it to the active context (so child spans link automatically), and propagates context across `await` points.

`tracer.start_span(...)` (without `as_current`) is a lower-level form for cases where you DELIBERATELY don't want context attachment (e.g., a span representing a backgrounded task started inside the parent's request). Default is `start_as_current_span`.

Do NOT use `tracer.start_span(...)` + manual `.end()` — every error path becomes a leak.

### Rule 3 — Span names are static, low-cardinality

```python
# WRONG — high cardinality, garbage span names
with tracer.start_as_current_span(f"publish {topic}") as span: ...

# RIGHT — static name; topic goes in an attribute
with tracer.start_as_current_span("motadata.client.publish") as span:
    span.set_attribute("messaging.destination.name", topic)
```

Span names group calls in the backend (Tempo, Honeycomb, etc.). User-supplied dynamic data MUST be attributes, not span names. The Python OTel SDK does not enforce this; downstream cost (cardinality explosion in span-name index) is real.

Convention: `<module>.<class>.<method>` — `motadata.client.publish`, `motadata.cache.get`, `motadata.storage.put`. Lowercase, dot-separated.

### Rule 4 — Attribute keys follow semantic conventions

```python
# WRONG — custom keys
span.set_attribute("topic", topic)
span.set_attribute("payload_size_bytes", len(payload))

# RIGHT — semconv keys
span.set_attribute("messaging.system", "motadata")
span.set_attribute("messaging.destination.name", topic)
span.set_attribute("messaging.message.body.size", len(payload))
```

OpenTelemetry semantic conventions: <https://opentelemetry.io/docs/specs/semconv/>. The relevant namespaces for SDK clients:

| Domain | Namespace |
|--------|-----------|
| HTTP | `http.*` (`http.method`, `http.status_code`, `http.url`, `http.scheme`) |
| Messaging | `messaging.*` (`messaging.system`, `messaging.destination.name`, `messaging.operation.name`) |
| Database | `db.*` (`db.system`, `db.operation`, `db.name`) |
| RPC | `rpc.*` (`rpc.system`, `rpc.method`, `rpc.service`) |
| Network | `net.*` (`net.peer.name`, `net.peer.port`, `net.transport`) |
| Server / errors | `error.type`, `server.address`, `server.port` |

When semconv has a key that matches your domain, USE IT. Custom keys go under a vendor namespace (`motadata.<thing>`); never use unprefixed custom keys.

### Rule 5 — Errors are recorded AND set_status

```python
try:
    result = await self._call()
except SomeError as e:
    span.record_exception(e)                  # adds an event with the exception details
    span.set_status(Status(StatusCode.ERROR, str(e)))  # marks the span as failed
    raise
```

Both are needed:
- `record_exception` adds an event with stack trace + exception type. Backends display the trace.
- `set_status(ERROR)` flips the span's status flag, making it discoverable in error-rate queries.

If you only `record_exception`, span shows up in success queries. If you only `set_status`, span has no exception detail.

`asyncio.CancelledError` is special: cancellation is a normal control flow signal, NOT an error. Don't mark cancelled spans as ERROR:

```python
try:
    await self._call()
except asyncio.CancelledError:
    span.set_status(Status(StatusCode.UNSET))    # or do nothing; default is UNSET
    raise                                         # always re-raise
```

### Rule 6 — Counters / histograms reuse module-scope instruments

```python
# WRONG — instrument created per call
async def publish(self, topic: str, payload: bytes) -> None:
    counter = meter.create_counter("motadata.publish.requests")  # leaks
    counter.add(1)

# RIGHT — module scope (see Rule 1)
publish_counter = meter.create_counter("motadata.publish.requests", ...)

async def publish(self, topic: str, payload: bytes) -> None:
    publish_counter.add(1, {"topic": topic, "outcome": "success"})
```

OTel instruments are designed for reuse. Create-per-call duplicates registry entries and (in some exporters) breaks aggregation.

Histogram observation goes inside the span:

```python
import time

async def publish(self, topic: str, payload: bytes) -> None:
    start = time.perf_counter()
    try:
        with tracer.start_as_current_span("motadata.client.publish") as span:
            ...
    finally:
        elapsed_s = time.perf_counter() - start
        publish_latency.record(elapsed_s, {"topic": topic})
```

### Rule 7 — Async context propagation works automatically

Python OTel's context propagation hooks `contextvars`, which `asyncio` honors. A span started in one async function is visible (as the active span) inside any function it `await`s.

```python
async def outer() -> None:
    with tracer.start_as_current_span("outer"):
        await inner()

async def inner() -> None:
    # The active span is "outer"; this child becomes its child.
    with tracer.start_as_current_span("inner"):
        ...
```

EXCEPT: when you `asyncio.create_task(...)`, the new task captures the CURRENT context AT TASK-CREATION TIME. If you create a task inside a span and then exit the span before the task runs, the task still sees the span as its parent. This is usually correct.

If you DELIBERATELY want the task NOT to inherit the parent context (e.g., a long-running background task that should not extend the parent's span), pass an empty context:

```python
import contextvars
ctx = contextvars.copy_context()                 # snapshot
# work...
asyncio.create_task(background(), context=contextvars.Context())  # fresh context
```

Rare; don't reach for this without a reason.

### Rule 8 — Logging integration via LoggingHandler

Bridge stdlib `logging` records into OTel logs:

```python
# Setup (at SDK consumer's app startup, NOT in library code)
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider
import logging

logger_provider = LoggerProvider()
set_logger_provider(logger_provider)
logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(OTLPLogExporter())
)

handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logging.getLogger().addHandler(handler)
```

The LIBRARY ONLY calls `logging.getLogger(__name__)` and emits records. The CONSUMER decides whether to hook OTel. `python.json:toolchain` does not include LoggingHandler setup — that's the consumer's choice.

When the SDK emits a log record inside a span, OTel's LoggingHandler auto-attaches `trace_id` and `span_id` to the record. Consumers see correlated logs and traces in their backend without extra wiring.

### Rule 9 — Provider setup is the CONSUMER's job

```python
# WRONG — library calls these
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
trace.set_tracer_provider(TracerProvider())                  # NEVER do this in library
trace.get_tracer_provider().add_span_processor(...)          # NEVER

# RIGHT — library only consumes the API
tracer = trace.get_tracer(__name__)                          # API call; no SDK
with tracer.start_as_current_span("op"):
    ...
```

Library code uses the OTel API (`opentelemetry`). The OTel SDK (`opentelemetry-sdk`) is the CONSUMER's runtime dependency — they configure exporters, samplers, resource attributes. If the consumer never calls `set_tracer_provider`, the OTel API uses a no-op provider; spans go nowhere; the SDK's instrumentation is harmless.

### Rule 10 — Graceful shutdown

The CONSUMER's app shutdown must call:

```python
trace.get_tracer_provider().shutdown()         # flush spans
metrics.get_meter_provider().shutdown()        # flush metrics
logger_provider.shutdown()                      # flush logs
```

The SDK can OFFER a helper that consumers call:

```python
# motadatapysdk/observability.py — OPTIONAL convenience module
def setup_default_otel_consumer(*, otlp_endpoint: str) -> None:
    """Wire OTLP exporters with sane defaults. Call ONCE at app startup."""
    ...

def shutdown_default_otel_consumer() -> None:
    """Flush + shutdown OTel providers. Call at app shutdown."""
    trace.get_tracer_provider().shutdown()
    ...
```

Mark these clearly as OPTIONAL. The SDK does not require its OWN setup function — consumers may bring their own OTel wiring and the SDK works.

## GOOD: full instrumented method

```python
# motadatapysdk/client.py
from __future__ import annotations

import logging
import time

from opentelemetry import metrics, trace
from opentelemetry.trace import Status, StatusCode

from motadatapysdk.errors import NetworkError, TimeoutError as SDKTimeoutError

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

publish_counter = meter.create_counter(
    name="motadata.publish.requests",
    unit="1",
    description="Count of publish operations",
)
publish_latency = meter.create_histogram(
    name="motadata.publish.latency",
    unit="s",
    description="Publish request latency",
)


class Client:
    async def publish(self, topic: str, payload: bytes) -> None:
        """Publish ``payload`` to ``topic``."""
        start = time.perf_counter()
        outcome = "success"

        with tracer.start_as_current_span("motadata.client.publish") as span:
            span.set_attribute("messaging.system", "motadata")
            span.set_attribute("messaging.operation.name", "publish")
            span.set_attribute("messaging.destination.name", topic)
            span.set_attribute("messaging.message.body.size", len(payload))
            span.set_attribute("server.address", self._config.base_url)

            try:
                await self._do_publish(topic, payload)
            except SDKTimeoutError as e:
                outcome = "timeout"
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, "publish timeout"))
                raise
            except NetworkError as e:
                outcome = "network_error"
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise

        elapsed_s = time.perf_counter() - start
        publish_counter.add(1, {"topic": topic, "outcome": outcome})
        publish_latency.record(elapsed_s, {"topic": topic, "outcome": outcome})
```

Note: counter/histogram observation OUTSIDE the `with` block so `outcome` reflects the actual result. `start` captured BEFORE the span so latency includes span-overhead time too (which is honest — the consumer pays it).

## BAD anti-patterns

```python
# 1. Tracer per call
def f():
    tracer = trace.get_tracer(__name__)        # registry lookup per call
    with tracer.start_as_current_span(...): ...

# 2. Manual start/end (leaks on error)
span = tracer.start_span("op")
try:
    ...
except Exception:
    raise                                       # span never ended
span.end()

# 3. Dynamic span name
with tracer.start_as_current_span(f"publish {topic}"): ...   # cardinality blowup

# 4. Custom attribute keys
span.set_attribute("topic", t)                 # use messaging.destination.name

# 5. Swallow exception in span
with tracer.start_as_current_span("op"):
    try:
        do_thing()
    except Exception:
        pass                                    # span shows OK; bug invisible

# 6. Provider setup in library
trace.set_tracer_provider(TracerProvider())    # consumer's job

# 7. Counter recreated per call
async def publish(self, topic):
    counter = meter.create_counter("...")      # leaks
    counter.add(1)

# 8. Cancellation marked as ERROR
except asyncio.CancelledError:
    span.set_status(Status(StatusCode.ERROR))  # cancellation is normal

# 9. Print-style logging
print(f"published to {topic}")                 # use logger.info(...)

# 10. logging.basicConfig in library
logging.basicConfig(level=logging.INFO)        # caller's prerogative
```

## Cross-references

- `python-asyncio-patterns` — context propagation across `await` points.
- `python-exception-patterns` — record_exception + set_status pairing.
- `python-mypy-strict-typing` — typed Counter/Histogram return types.
- `python-doctest-patterns` — instrumented methods include `# doctest: +SKIP` on otel calls.
- `sdk-convention-devil-python` C-7 — design-rule enforcement at D3.
