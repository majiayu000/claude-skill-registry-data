---
name: coding-python
description: >-
  Enforces Python + expression style, type discipline, error handling,
  concurrency, and module organization standards.
  Use when writing, editing, reviewing, refactoring, or debugging
  .py/.pyi modules, implementing domain models, ROP pipelines,
  Protocol-driven services, or configuring pyproject.toml, Ruff, or ty.
---

# [H1][CODING-PYTHON]
>**Dictum:** *Python expression style, type discipline, and module organization govern all Python work.*

All code follows six governing principles:
- **Polymorphic** — one entrypoint per concern, generic over specific, extend over duplicate
- **Functional + ROP** — pure pipelines, typed error rails, monadic composition
- **Strongly typed** — inference-first, one canonical model per concept, zero `Any`/`cast` leakage
- **Programmatic** — variable-driven dispatch, `Literal` vocabularies, zero stringly-typed routing
- **Algorithmic** — reduce branching through transforms, folds, and discriminant-driven projection
- **AOP-driven** — cross-cutting concerns via `ParamSpec`-preserving decorator stacks, not in-method duplication


## Paradigm

- **Immutability**: `frozen=True` models, `model_copy(update=...)` transitions, `expression.Block`/`Map` collections
- **Typed error channels**: `@tagged_union` error variants for file-internal errors (never exported), shared domain error types at package level (few per system, boundary-crossing); `Result[T, E]` sync, `@effect.async_result` async
- **Exhaustive dispatch**: `match/case` on `@tagged_union` / `Annotated[Union, Discriminator]` closed domains, `singledispatch` for open extension
- **Type anchoring**: `NewType` for opaque scalars, `Annotated` + constraints for validated scalars, `BaseModel(frozen=True)` for rich objects — derive projections, never parallel models
- **Expression control flow**: `pipe` + curried projections (`result.bind`, `result.map`, `seq.filter`), `@effect.result` / `@effect.async_result` generators, zero statement branching
- **Programmatic logic**: `Literal` types for bounded vocabularies, `singledispatch` for open extension, zero stringly-typed routing
- **Surface ownership**: one polymorphic entrypoint per concern, `ParamSpec`-preserving decorators, no helpers
- **Private integration**: module logic is the export's implementation, not its neighbor — `_`-prefixed internals are closures, nested functions, or inline compositions inside the public function/class, not standalone module-level declarations consumed by a single caller
- **Cross-cutting composition**: decorator stacks (`trace > authorize > validate > cache > retry`), `Protocol`-first DI via `@effect.result` dependency threading


## Conventions

| Concern              | Library               | Scope                                          |
| -------------------- | --------------------- | ---------------------------------------------- |
| Domain + pipelines   | expression            | Result, Option, tagged unions, pipe, @effect   |
| Dependency injection | Protocol + expression | Structural contracts, @effect.result threading |
| Concurrency          | anyio                 | TaskGroup, CancelScope, structured spawning    |
| Boundary validation  | Pydantic              | Frozen models, TypeAdapter, ingress/egress     |


## Contracts

**Type discipline**
- `NewType` for opaque scalars, `Annotated` + constraints for validated scalars.
- `BaseModel(frozen=True)` for domain objects with smart constructors returning `Result[T, E]`.
- `@tagged_union` / `Annotated[Union, Discriminator]` for closed variant spaces.
- One canonical model per concept; derive projections, never parallel models.
- Zero `Any`/`cast()` without explicit boundary justification.
- Zero bare primitives in public signatures when typed atoms exist.
- Zero mutable collections in model fields — `tuple[T, ...]` or `expression.Block[T]`.
- Zero `class(ABC)`/`abstractmethod` — use `Protocol`.

**Control flow**
- Zero `if`/`else`/`elif` for variant dispatch — `match/case` only.
- Zero `try`/`except` in domain transforms.
- `pipe` + curried projections (`result.bind`, `result.map`) for linear pipelines.
- `@effect.result` / `@effect.async_result` generators for branching compositions.
- `.or_else_with(fn)` for error recovery at composition boundaries — never inside `@effect.result` generators.
- Boundary adapters may use required statement forms with marker: `# BOUNDARY ADAPTER — reason`.

**Error handling**
- `@tagged_union` error variants for file-internal errors — never exported, never cross module boundaries.
- Shared domain error types at package level — few per system, boundary-crossing, co-located in owning package (no dedicated error files).
- Domain error types carry polymorphic/agnostic logic reusable across all call sites.
- `Result[T, E]` sync fallible, `@effect.async_result` async fallible, `Option[T]` for absence.
- Zero `Optional[T]` for fallible returns — `Result[T, E]` or `Option[T]`.

**Decorators**
- `ParamSpec` + `Concatenate` + `@wraps` for all decorators.
- Canonical execution order (outer → inner): `trace > authorize > validate > cache > retry > operation`.
- Idempotency + double-decoration guards (`__wrapped__`/marker attr).
- Zero god decorators, zero mutable closure state, preserve `contextvars` propagation.
- Deterministic stacks — every decorator states its effect surface in code.

**Surface**
- One polymorphic entrypoint per concern.
- Private-by-default: every non-exported symbol carries `_` prefix. Module exports 1–2 symbols maximum via `__all__`.
- Internal logic integrates INTO exports — closures/nested functions inside the public function or class, inline compositions inside pipe chains. Not defined alongside as standalone module-level declarations consumed by a single caller.
- No helper files (`helpers.py`, `*_utils.py`) — colocate in domain module.
- No single-caller extracted functions, no one-use module-level declarations.
- `~350 LOC` scrutiny threshold — investigate for compression via polymorphism, not file splitting.

**Resources**
- `anyio.create_task_group()` for structured concurrency.
- Explicit deadlines via `CancelScope`, cooperative checkpoints.
- `except*` at TaskGroup boundaries for `ExceptionGroup` handling.
- Zero unbounded concurrency, zero global mutable singletons.


## Load sequence

**Foundation** (always):

| Reference                                 | Focus                                                                                |
| ----------------------------------------- | ------------------------------------------------------------------------------------ |
| [decorators.md](references/decorators.md) | ParamSpec algebra, ordering, composition, descriptor protocol                        |
| [transforms.md](references/transforms.md) | Compositional logic: dispatch, folds, polymorphism, monadic composition, AOP algebra |

**Task-routed references**:

| Reference                                 | Focus                                                                            |
| ----------------------------------------- | -------------------------------------------------------------------------------- |
| [types.md](references/types.md)           | Python typing, NewType, Annotated, generics, type-level discipline               |
| [effects.md](references/effects.md)       | Result/Option pipelines, @effect.result/@effect.async_result builders, ROP       |
| [errors.md](references/errors.md)         | Error construction, @tagged_union hierarchies, domain error policy               |
| [protocols.md](references/protocols.md)   | Protocol ports, adapter boundaries, structural DI                                |
| [numeric.md](references/numeric.md)       | Protocol-driven numerics, Polars lazy frames, Decimal, reductions                |
| [validation.md](references/validation.md) | Compliance checklist, detection heuristics, completion gate for all `.py` audits |

**Specialized** (load when task matches):

| Reference                                       | Load when                                                                                                              |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| [concurrency.md](references/concurrency.md)     | TaskGroup, CancelScope, ExceptionGroup, sub-interpreters                                                               |
| [observability.md](references/observability.md) | structlog, OpenTelemetry, RED metrics, context propagation                                                             |
| [serialization.md](references/serialization.md) | Pydantic ingress, msgspec egress/msgpack, suitkaise cucumber/sk/circuits/timing, codec pipelines, transport boundaries |
| [performance.md](references/performance.md)     | Memory layout, CPython internals, profiling, JIT                                                                       |


## Validation gate

- Required during iteration: `pnpm python`.
- Required for final completion: `pnpm quality`, `pnpm dotnet`, `pnpm python`.
- Reject completion when load order, contracts, or checks are not satisfied.
- Python tool posture is Ruff + ty first; mention alternate checkers only when the target project already configures them.
- Examples inside this skill are executable doctrine: no unjustified `type: ignore`, no unmarked `cast`, no `.or_else_with` recovery inside `@effect.result` generators, and `case _ as unreachable: assert_never(unreachable)` for closed domains.

## Skill eval prompts

- Explicit invocation: "Using coding-python, refactor this .py module into expression Result rails with Protocol DI."
- Implicit invocation: "Review this Python service for ty/Ruff issues, monadic error handling, and helper drift."
- Noisy context: "Ignore the product notes and only audit the Python serialization boundary."
- Negative control: "Write only SQL DDL." Expected: do not invoke Python references unless Python code appears.
- Compliance checks: output should load only relevant references, avoid command thrash, avoid new helper files, preserve Result/Option doctrine, and run `pnpm python` or narrower Ruff/ty gates when code is touched.


## First-class libraries

These packages are standard libraries — use over stdlib equivalents.

| Package       | Provides                                                                                |
| ------------- | --------------------------------------------------------------------------------------- |
| expression    | Tagged unions, Result/Option, pipe/compose, @effect builders, Block/Map/Seq, curry      |
| anyio         | Structured async concurrency                                                            |
| Pydantic      | Frozen models, validation, serialization                                                |
| structlog     | Structured logging                                                                      |
| OpenTelemetry | Distributed tracing, metrics                                                            |
| msgspec       | High-performance serialization                                                          |
| httpx         | Async HTTP client                                                                       |
| polars        | DataFrame operations                                                                    |
| suitkaise     | Cross-process transport of unpicklable objects (cucumber modules: sk, circuits, timing) |
| beartype      | Runtime type checking                                                                   |
| pytest        | Test framework                                                                          |
| hypothesis    | Property-based testing                                                                  |
