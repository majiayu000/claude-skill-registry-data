---
name: thalarch-python
description: >
  Project-version-aware Python engineering for services, libraries, automation, data tooling,
  and applications. Use for Python source, async code, typing, packaging, APIs, testing,
  profiling, data pipelines, or Python-specific refactoring.
---

# Thalarch Python

Use the runtime, package manager, frameworks, typing policy, and quality tools already declared
by the repository. Do not force `uv`, Poetry, Ruff, Pyright, FastAPI, Pydantic, or any other
modern tool merely because it is popular.

## Preflight

Identify:

- supported Python versions;
- `pyproject.toml`, setup/config files, lockfiles and environment manager;
- runtime/framework dependencies;
- formatter/linter/type checker configuration;
- test runner/plugins;
- packaging/distribution contract.

Use the repository's existing environment and commands when available.

## Idiomatic Python

Prefer clear Python-native constructs:

- comprehensions/generator expressions for simple transformations;
- `enumerate`, `zip`, `collections`, `itertools`, `pathlib`, context managers, and other
  standard-library primitives where they clarify intent;
- dataclasses/value types when the repository and problem benefit from them;
- precise function/type contracts rather than type noise on obvious locals;
- EAFP only where the exception is the real boundary signal and failure cost is acceptable.

Do not compress complex business logic into clever expressions. A readable loop is better than
a dense comprehension with hidden state or difficult branching.

Never use mutable default arguments unintentionally.

## Typing

Follow the project's configured type checker and Python floor.

- Preserve generics and protocols where they encode useful contracts.
- Prefer `unknown`-equivalent narrowing via actual Python type guards/contracts rather than
  casual `Any` propagation.
- Do not add annotations unsupported by the repository's minimum runtime without the required
  compatibility mechanism.
- Treat runtime validation and static typing as separate concerns.

## Async and concurrency

Identify whether the code uses `asyncio`, Trio/AnyIO, framework-managed async, threads,
processes, or synchronous execution.

Review:

- blocking I/O inside the event loop;
- task ownership and cancellation;
- orphan/background task lifetime;
- timeout behavior;
- semaphore/queue backpressure;
- shared mutable state;
- CPU-bound work incorrectly placed in async tasks;
- resource cleanup during cancellation.

Do not introduce async merely to make code look modern. For CPU-bound work, profile and choose
threads/processes/native/vectorized work based on the actual workload and GIL/runtime behavior.

## Exceptions and resources

- Never use a bare `except` unless implementing a true process-level boundary where all failures
  must be captured and re-raised/reported deliberately.
- Catch specific exceptions you can handle or translate.
- Preserve traceback/cause when re-raising.
- Use context managers for owned files, locks, connections, transactions, and temporary resources.
- Do not convert failures to `None`, empty collections, or success responses unless that is the
  documented contract.

## Web/API frameworks

Only use framework-specific patterns if the framework is present. Verify the installed version
before writing decorators, dependency hooks, Pydantic model APIs, ORM calls, or lifecycle code.

For FastAPI/Django/Flask/other services, combine with `thalarch-api`, `thalarch-security`, and
`thalarch-data-sql` when relevant.

## Testing

Use the configured test stack. Strong evidence may include:

- focused pytest/unittest cases;
- parametrized boundary matrices;
- property-based tests when invariants matter and Hypothesis is available/justified;
- integration tests for DB/network/process boundaries;
- async tests using the repository's configured async plugin;
- regression tests that fail for the original bug.

Do not chase a coverage percentage independently of behavior risk.

## Performance

Profile before tuning. Use available evidence such as cProfile, py-spy, scalene,
`tracemalloc`, benchmark tooling, DB/query traces, or application metrics.

Look for algorithmic waste, repeated serialization/parsing, accidental materialization,
N+1 I/O, event-loop blocking, excessive object churn, and unnecessary copies before reaching
for native extensions or concurrency.

## Verification

Run project-native format/lint/type/test/build/package commands as configured. State the actual
Python version/environment used for version-sensitive claims.
