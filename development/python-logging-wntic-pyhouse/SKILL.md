---
name: python-logging
description: Use when writing code that reports what it did or what went wrong — a log call, a `print` for progress or errors, an `except` that records a failure, or logging setup in an entry point, a CLI or a library. Owns one structured event per occurrence with a stable `<subject>_<past_tense_verb>` name and identifiers as fields, the rule that an error is logged once by the scope that stops it and never by a scope that re-raises, the warning a failed undo under compensation earns, logging configured once at the entry point and never inside a distributed package, what never reaches a log line, and a program's result on stdout as output rather than a log event, and a program whose stdout is its result logging to stderr. Annotation forms and comments are `python-style`; the error classes and their `context` are `exception-catalog`.
---

# Python Logging

A log line exists to be **queried** — filtered, grouped, counted, alerted on. Prose cannot be queried, so
every occurrence worth recording produces **exactly one structured event**: a name plus fields, never a
sentence with values spliced into it. These rules hold whatever the architecture is.

Only one thing here varies from project to project, and it varies as a *consequence*, not as a separate
rule: an error is logged once, by the scope that can add context and will not re-raise it — and where a
project's errors propagate to decides which scope that is. Everything else is unconditional.

## When to use vs. neighbours

- Writing or changing any log call, naming an event, configuring logging → this skill.
- Annotation forms, record types, comments → `python-style`.
- The exception classes, what goes into their `context`, translation with `from exc`, best-effort
  compensation itself → `exception-catalog`.
- Which layer of a hexagonal service may log at all → `hex-architecture`, in the `pyhouse-hex` plugin;
  in a flat service, where the scope that stops a run's failure sits → `flat-layered` and
  `flat-entrypoint`, in `pyhouse-flat`.
- Whether a test may assert on what was logged → `test-principles`.
- An event name as a frozen external contract among the others → `naming`.

## The event

Four obligations, whichever library provides them:

- **One logger, obtained at module level.** Not per call, not per instance, and not a second logging
  mechanism running alongside the first — two mechanisms split one event stream in half and neither half
  is complete. `print()` is not one of them, outside an entry-point debug path behind a flag. **What a
  program writes to stdout as its result is not a log event** — a CLI's report, a table, the JSON a
  caller pipes onward is the product, and `print()` or `sys.stdout` is the right way to emit it; this
  rule is about diagnostics, which never share that stream: **a program whose stdout is its product
  writes every log event to stderr**, so a caller reading the result never parses a diagnostic as data.
- **One event per occurrence.** The same occurrence logged twice is two incidents on the dashboard.
- **The event name is a stable contract** — snake_case, `<subject>_<past_tense_verb>`.
- **Identifiers and counts ride as fields**, never interpolated into the message.

The event name is what a query matches on: `foo_created`, `bar_archived`, `foos_imported`,
`run_failed`. These are stable strings — **do not rename once shipped**, because dashboards and
alerts key on them. `naming` lists them among the frozen external contracts for that reason.

Identifiers and counts are fields: the primary id as `<subject>_id`, the actor as `caller_id` where one
exists, counts (`imported`, `skipped`, `errors`) for a bulk operation. A distributed package uses
`logging.getLogger(__name__)` instead and configures nothing (rule 4). Under `structlog`, in an
application — unconfigured, it renders for a terminal on stdout, so the entry point sets both the
rendering and the stream (rules 1 and 3):

```python
import structlog

log = structlog.get_logger()

log.info("foo_created", foo_id=str(foo.id))
```

```python
# no — nothing in this line can be filtered by foo, grouped, or counted
log.info(f"created foo {foo.id}")
```

## Configuring the logger

**The logger is configured once, by the process's entry point, before its first event** — the sink, the
format, the level, and the routing that brings records from libraries into the same stream. Nothing
below the entry point configures logging, and a process whose entry point configures nothing emits
whatever defaults the library happens to have. **A distributed package configures nothing at all**: it
logs through the stdlib's `logging.getLogger(__name__)`, the one interface every importer already routes,
adds no handler and sets no level, and leaves every one of those choices to the application that imports
it.

**The rendering follows the sink**: machine-readable wherever a collector reads it; on an interactive
terminal it may be human-readable.

The stdlib `logging` module is the binding for a distributed package (rule 4) and an alternative for an
application: the event name is the record's message, the fields reach the record through `extra=` or a
`LoggerAdapter` (or the module sits behind a thin structured wrapper), and an application that chooses it
configures a JSON formatter once at its entry point. That buys one stream with no bridge, since
third-party libraries already log through `logging`; it costs enforcement, since nothing in the module
holds the field discipline, so the author holds it where a keyword-field interface would have made it
the path of least resistance. How the logger is obtained, configured and
fed its fields changes with the binding; nothing in `## Rules` does.

## Who logs an error

**An error is logged once, by the scope that can add context and will not re-raise it.** That is the
whole rule, and it binds with no layers at all: a scope that re-raises stays silent — what it was about
to log rides in the exception instead, the fields in `context` and the cause through `from exc`
(`exception-catalog`) — and the scope that stops the exception is the only one that logs.

To apply it, trace the exception outward to the first scope that handles it rather than re-raising.
A project that funnels every failure into one handler makes that handler the scope; a process that
contains each run's failure and carries on makes the code around each run the scope; where the exception
leaves the codebase entirely — a distributed package handing it to its caller — no scope inside
qualifies and nothing inside logs. Each architecture family fixes where that scope is, in its own
architecture skill — e.g. `hex-architecture`, in the `pyhouse-hex` plugin, or `flat-layered`, in
`pyhouse-flat`.

A branch unreachable through the normal write path — a constraint standing as defence in depth behind a
rule that already refuses — is **not** excused from logging: if it fired, the rule was bypassed, and that
is the most interesting line in the log. It is logged by whoever stops it, under the same allocation as
any other failure.

Level guide, for the scope that does log: `warning` for an expected rule violation surfacing at a
boundary — uniqueness, a foreign key; `error` for an unexpected failure — a network timeout, a
third-party 5xx, malformed data.

## Logging a re-raised error

`log.x(...)` immediately followed by `raise` in the same scope is two entries for one event, and there is
**no sanctioned exception** — a failed undo stopped under compensation, below, logs a different event
from the one it re-raises. With SQLAlchemy, for one:

```python
# yes — translate, carry the detail forward, stay silent
try:
    await self._session.execute(statement)
except IntegrityError as exc:
    raise ConflictError("foo name already exists", {"foo_name": foo.name}) from exc

# no — the layer that stops this will log it again, off the translated exception
except IntegrityError as exc:
    log.warning("foo_name_conflict", foo_name=foo.name)
    raise ConflictError("foo name already exists", {"foo_name": foo.name}) from exc
```

## A failed undo under compensation

Best-effort compensation (`exception-catalog`) is the one place a scope that re-raises also stops a
failure, and so the one place a scope that re-raises logs. The two are different events, which is why it
does not break the rule above: the **undo's** failure stops in this scope and is logged here, once; the
**original** failure is re-raised unlogged and is logged by whoever stops it.

- **Logged by the scope that stops the undo's failure** (`exception-catalog`, condition 1), in the
  `except` around the undo call, and nowhere else. The undo it called stays silent, like any scope that
  raises.
- **At `warning`, exactly one event**, named for the undo that failed (`foo_blob_undo_failed`), with the
  undo's identifying inputs as fields and the undo's error attached (`exc_info=` under `structlog`).
  Not `error`: the operation's failure is the error, and it is logged where it stops.
- It carries what a person needs to clean up by hand — the key, the id, the reservation — because the
  event is the only record that an effect outlived the operation that made it.

## What never reaches a log line

- A full request or response body → log identifiers and counts only; bodies may carry personal data.
- A password, bearer token, API key or connection string → log a length or a hash, never the value.
- A `UUID` object rather than `str(uuid_value)` → some sinks render it poorly.

The first two reach an exception's `context` as well, because the scope that logs renders `context`
verbatim into the log line. `exception-catalog` owns that statement of the rule.

## Rules

1. **One logger, obtained at module level, and one structured event per occurrence.** No `print()` for
   diagnostics outside an entry-point debug path behind a flag, and no second logging mechanism beside
   the configured one — two mechanisms split the event stream and neither half is complete. Output a
   program writes to stdout as its result is not a log event, and this rule does not reach it. A
   program whose stdout is its product writes every log event to stderr.
2. **Give every event a stable snake_case `<subject>_<past_tense_verb>` name, and carry its identifiers
   and counts as fields rather than interpolating them into the message.** A value inside a sentence
   cannot be filtered, grouped or counted — on every binding, the stdlib one included — and a renamed
   event silently breaks every dashboard keyed on the old string.
3. **Configure the logger once, in the process's entry point, before its first event.** Nothing below
   the entry point configures logging, and that one configuration picks the rendering for the sink —
   machine-readable wherever a collector reads it; on an interactive terminal it may be human-readable —
   and routes the standard library's loggers (a framework's, a driver's) through it, so no library's
   records bypass it with a handler or format of their own. Running the setup again leaves the same
   configuration — one handler of its own, not a second, and none it did not install removed — because a
   test that builds the app, or a second entrypoint in the same process, calls it again.
4. **A distributed package logs through the stdlib `logging.getLogger(__name__)` and configures
   nothing** — no handler, no level, no format; the application importing it owns all three.
5. **Log an error once, in the scope that can add context and will not re-raise it** — traced outward
   from the raise to the first scope that handles the exception rather than re-raising it; a project
   that funnels failures into one handler makes that handler the scope. A scope that re-raises does
   not log — a log call followed by `raise` is two entries for one event; the detail it would have
   logged goes into the exception's `context`. The one failure a re-raising scope stops — an undo's,
   under `exception-catalog`'s best-effort compensation — ends there, so that scope logs it: one
   `warning` event naming the failed undo, before re-raising the original. Never unlogged, never at
   `error`, never by the undo itself — it is the only record that an effect was left behind.
6. Check logged fields against **What never reaches a log line** before emitting them; the same bans
   on an exception's `context` are `exception-catalog`'s.

## Hard stops

- Choosing an annotation form, a record type or a comment → stop, use `python-style`.
- Defining an error class, deciding what its `context` carries, or writing the translation or the
  compensation itself → stop, use `exception-catalog`.
- Asked which layer of a service may log at all, or where a flat run's guard sits → stop, use
  `hex-architecture` (in `pyhouse-hex`) or `flat-layered` and `flat-entrypoint` (in `pyhouse-flat`), or
  the project's own layout where neither applies.
- Asked whether a test may assert on what was logged → stop, use `test-principles`.
