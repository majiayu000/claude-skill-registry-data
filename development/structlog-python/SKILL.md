---
name: structlog-python
description: Use for writing, configuring, integrating, reviewing, debugging, or testing Python structured logging with structlog. Trigger for bound loggers, event dictionaries, processor chains, JSON or console rendering, standard-library logging integration, contextvars, request correlation, exception rendering, and structlog test capture. Do not use for stdlib-logging-only, Loguru-only, metrics-only, tracing-only, or collector configuration tasks that do not use structlog.
argument-hint: "[structlog task, code, event contract, or logging failure]"
---

# structlog Python

Produce one version-grounded event pipeline whose context lifetime, processor
order, output ownership, event schema, and tests are explicit.

## Boundary

Use this skill when the project uses structlog or the user explicitly requests
it. Do not introduce structlog into a standard-library-only or Loguru-only task.
Metrics, traces, OpenTelemetry collector pipelines, and logging-platform queries
are outside scope unless the requested change is the Python structlog boundary.
Preserve the application's established logging owner and event schema unless the
task explicitly changes them.

## Know the runtime model

| Object | Runtime meaning | Decision consequence |
|---|---|---|
| `BoundLogger` | A proxy holding immutable-style bound context, a wrapped output logger, and a processor chain. | `.bind()` returns a logger with added context; retain that return value. |
| Event dictionary | A fresh mapping made from bound context, call fields, and the `event` value for one log call. | Processors transform this contract; renderers consume it. |
| Processor | A callable `(wrapped_logger, method_name, event_dict)` that returns an event dictionary until the terminal step, or raises `DropEvent`. | Order is behavior. Enrich and redact before rendering. |
| Terminal processor | The one final renderer or adapter that returns what the wrapped logger accepts. | Never append processors after it or combine incompatible terminals. |
| Wrapped logger / factory | The output implementation and the callable that creates it: print/write/bytes or stdlib logging. | Choose from output ownership and interoperability, not familiarity. |
| Context variables | Execution-context-local fields merged by `merge_contextvars`. | Clear at each request/job start, then bind; test real sync/async boundaries. |
| Global configuration | Defaults used when lazy logger proxies are first assembled. | Configure once before first use; caching can freeze earlier choices. |

A call follows this path:

```text
bound context + call fields + event
                -> fresh event_dict
                -> processor 1 -> ... -> processor N
                -> exactly one terminal renderer/adapter
                -> wrapped logger / handler / stream
```

Read [the object and event model](references/object-model.md) whenever `.bind()`,
processor return values, configuration caching, or output ownership is unclear.

## Ordered workflow

1. Recover the event contract: stable event names, required keys, levels,
   timestamps, correlation fields, exceptions, redaction, and output consumer.
2. Inventory existing `logging` handlers/formatters, framework initialization,
   and foreign stdlib emitters. Choose one integration architecture.
3. Build shared processors in semantic order. Put one renderer or handoff last.
4. Configure at the composition root before application work or cached loggers.
5. Bind long-lived component data on returned loggers; clear and bind
   request/job context at its boundary.
6. Emit named events with structured keyword fields. Do not duplicate values in
   interpolated prose.
7. Test event dictionaries separately from final transport/rendering.

## Choose by intent

| Intent | Use |
|---|---|
| Obtain a lazy logger proxy | `structlog.get_logger(...)` |
| Add component/object fields | `log = log.bind(...)` |
| Remove known bound keys | `.unbind(...)`; use `.try_unbind(...)` only when absence is allowed |
| Replace a bound logger's local context | `.new(...)`; do not confuse this with contextvars cleanup |
| Add request/task context | `clear_contextvars()` then `bind_contextvars(...)`, with `merge_contextvars` first in the chain |
| Bind context for one nested scope | `with bound_contextvars(...):` |
| Filter a non-stdlib pipeline cheaply | `make_filtering_bound_logger(level)` |
| Filter through stdlib logger levels | `structlog.stdlib.filter_by_level` with a stdlib logger factory |
| Add standard fields | built-in processors such as `add_log_level`, `add_logger_name`, and `TimeStamper` |
| Render exception text | `format_exc_info` before the renderer |
| Emit structured traceback data | `ExceptionRenderer(ExceptionDictTransformer(show_locals=False))` after installed-version inspection; enable locals only by an explicit safe contract |
| Production structured output | `JSONRenderer` or an established terminal adapter |
| Human development output | `ConsoleRenderer`, selected by configuration, not event call sites |
| Drop an event in a processor | raise `structlog.DropEvent` deliberately |
| Assert event semantics | `LogCapture` or carefully scoped `capture_logs()` |
| Assert wrapped call/rendering | `CapturingLoggerFactory`, a real handler, or parsed output |

Read [the intent-to-API map](references/api-map.md) before reaching for an
unfamiliar helper or relying on an exact signature.

## Canonical standalone pipeline

```python
import logging

import structlog


def configure_logging(*, development: bool = False) -> None:
    renderer = (
        structlog.dev.ConsoleRenderer() if development else structlog.processors.JSONRenderer()
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )


log = structlog.get_logger("payments").bind(component="authorizer")
log.info("payment_authorized", payment_id="pay_123", amount_cents=2500)
```

`get_logger()` returns a proxy; the event dictionary is assembled and processed
when a log method runs. `WriteLoggerFactory` writes a whole line atomically.
Choose the factory that matches the application stream and renderer return type.

## Choose exactly one integration architecture

| Condition | Architecture |
|---|---|
| Application events use structlog; foreign stdlib output need not share its schema | Render in structlog and let the selected wrapped logger transport the result. |
| structlog and foreign stdlib records must share one final renderer | Use `ProcessorFormatter`: structlog ends with `wrap_for_formatter`; formatter-side processors remove metadata then render. |
| Existing stdlib handlers and formatters must receive event fields | Use the installed supported render-to-logging adapter and test `LogRecord` extras. |
| Conventional stdlib-backed defaults are sufficient | Inspect `structlog.stdlib.recreate_defaults()` before custom configuration. |

Do not put `JSONRenderer` before `ProcessorFormatter.wrap_for_formatter`. Do not
render once in structlog and again in a formatter. Read [stdlib integration](references/integration.md).

## Processor and context rules

- Order filters before expensive enrichment when the selected logger makes that
  valid. Merge context before processors that consume those fields.
- A normal custom processor must return the event dictionary on every retained
  path. It may mutate it because structlog copied the call context first.
- Redact or omit secrets before any renderer or stdlib handoff. Never bind raw
  tokens, credentials, authorization headers, full request bodies, or unbounded
  objects.
- Keep one stable machine event name such as `inventory_reservation_failed`;
  put changing values in fields. Treat field names as an external contract.
- Use logger `.bind()` for data scoped to a returned logger. Use contextvars for
  data that follows the current execution context. These are different stores.
- In hybrid sync/async frameworks, test propagation across the actual boundary;
  contextvars can be isolated between execution mechanisms.

Read [processor contracts](references/processors.md) and [context lifecycle](references/context.md).

## Failure routing

- Duplicate lines: inspect propagation, root/child handlers, repeated startup,
  and whether two layers render the same record.
- Missing foreign fields: verify the chosen formatter/adapter path and its
  `foreign_pre_chain`; do not assume all `LogRecord` extras survive.
- Missing exception detail: pass `exc_info` via `.exception(...)` or the intended
  signal and run an exception processor before rendering.
- Leaked request IDs: clear at unit-of-work start and test two sequential units.
- Changed configuration has no effect: inspect cached loggers and initialization
  order; do not repeatedly reset production global state as a workaround.
- Slow async code: measure the actual processor and I/O cost, then inspect the
  installed async methods and executor behavior before redesigning.

## Version grounding and completion

Inspect project locks and run `python scripts/inspect_structlog.py` from the
installed skill directory when names, signatures, async methods, renderer byte
contracts, or integration helpers can drift. Read [API grounding](references/api-grounding.md).

Do not declare completion until one output owner is evident; processor ordering
and the terminal step are coherent; event keys, level filtering, exception
shape, context cleanup, and secret exclusion are tested; foreign records and
duplicate initialization are tested when applicable; and project checks pass or
skipped evidence and consequences are reported.

## References

- [Event pipeline recipes](references/recipes-events.md)
- [Integration and test recipes](references/recipes-integration.md)
- [Object and event model](references/object-model.md)
- [Intent-to-API map](references/api-map.md)
- [Processor contracts](references/processors.md)
- [Standard-library integration](references/integration.md)
- [Context lifecycle](references/context.md)
- [Testing structlog behavior](references/testing.md)
- [API grounding](references/api-grounding.md)
