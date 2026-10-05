---
name: python-architect
version: 1.4.1
description: Python 3.14 enterprise standards — modern typing (PEP 649), immutable dataclasses, Protocol-based DI, asyncio discipline, pytest 9, psycopg + .sql files via importlib.resources. Use when writing, reviewing, or scaffolding Python code.
---

# Python Architecture Standards

Targets **Python 3.14**. See [STACK.md](STACK.md) for pinned dependency versions.

## 1. Typing & Domain Safety

- **Modern syntax:** Built-in generics (`list[str]`, `dict[K, V]`, `X | None`). Never the legacy `typing.List` / `typing.Optional`.
- **Deferred annotations (PEP 649, 3.14):** Annotations are no longer eagerly evaluated — forward references no longer need quotes (`def f(arg: NotYetDefined)` works). Inspect via `annotationlib.get_annotations()`, not `__annotations__` directly.
- **Domain types:** `typing.NewType` to separate distinct concepts (`UserId` vs `OrderId`).
- **Enums:** Default to `Enum` (with `__str__` overridden) for closed sets of domain states — members are distinct identities, not interchangeable with raw primitives, which catches accidental comparisons against arbitrary strings/ints. Reach for `StrEnum` (3.11+) when members must interoperate directly with strings — JSON payloads, query params, f-strings — without a `.value` call at every site. Reach for `IntEnum` when members must support arithmetic or ordering against plain integers (HTTP status codes, priority levels, wire values from an external system). Both trade `Enum`'s identity-safety for primitive compatibility — reach for them only when that interop is a real requirement, not by default.
- **Constraints:** `Literal` for a narrow, function-local set of string flags that doesn't warrant a full `Enum`.
- **Structured payloads:** `TypedDict` over `dict[str, Any]` for known-shape mappings (see §3 for the broader dict/tuple-avoidance principle).
- **Subclassing safety:** `typing.override` decorator (3.12+) on every overriding method — mypy flags broken overrides.

## 2. Generators & Iterators

- **Return `Iterator[T]` / write a generator when:** the sequence is large or unbounded, the consumer might short-circuit (`break`, early `return`), or it's backed by a cursor (DB pagination, paginated HTTP APIs, file streaming). Laziness avoids materializing the whole sequence in memory.
- **Return `list[T]` when:** the result is small, bounded, and the caller almost always consumes the whole thing — don't wrap it in a generator just to look idiomatic.
- **Async generators:** `AsyncIterator[T]` / `async def ... yield` for streaming I/O (paginated API clients, chunked reads) — pairs with `async for`. See §5 for asyncio discipline.
- **`itertools`:** default toolkit for lazy composition (`chain`, `islice`, `groupby`, `pairwise`) over manual index bookkeeping.
- **Anti-pattern:** collecting a generator into a `list` immediately after producing it (`list(gen())`) just to satisfy a type checker — return the concrete type the caller actually needs instead of round-tripping through both.

## 3. Data Structures & Memory

- **Immutability:** Default to `@dataclass(slots=True, frozen=True)` for DTOs and value objects.
- **Mutable defaults:** Never use a mutable literal (`[]`, `{}`, `set()`) as a function parameter default or a bare dataclass field default — it's shared across every call/instance. Use `None` and assign inside the function body, or `field(default_factory=list)` on dataclasses. Enforced by ruff's `B006`/`B008` (bugbear, see §11).
- **Pydantic vs dataclass boundary:** Pydantic only at application boundaries (API request/response, DB row parsing, config). Standard dataclasses for core domain logic — keeps the domain free of validation-framework coupling.
- **Typed models over dicts/tuples:** Prefer a `dataclass` / `NamedTuple` / `TypedDict` (see §1) to `dict[str, Any]` or a raw `tuple` for anything with a stable shape — attribute access catches typos and missing fields that dict keys and tuple indices can't. Reserve bare dicts/tuples for genuinely dynamic or anonymous data (arbitrary JSON blobs, `zip()` output consumed immediately, coordinate pairs).
- **Ordering:** `@dataclass(order=True)` for value objects that need comparison operators — avoid hand-rolled `__lt__`/`__gt__`/`__le__`/`__ge__` chains. For one-off custom sort keys, pass a plain function to `sorted(key=...)` rather than implementing a full ordering protocol.
- **Memory:** `__slots__` (explicit or via `dataclass(slots=True)`) on high-volume instances.

## 4. Interfaces & DI

- **Protocols:** `typing.Protocol` (structural typing) over deep `abc.ABC` inheritance. Define protocols where consumed.
- **DI:** Pass dependencies into `__init__`. Never instantiate external clients inside a class.
- **State:** No globals. `contextvars` only when request-scoped state is unavoidable.

## 5. Concurrency & Resources

- **Asyncio discipline:** Never block the event loop. Offload sync I/O or CPU work via `asyncio.to_thread()`.
- **Task groups:** `asyncio.TaskGroup` for concurrent coroutines — handles cancellation and exception aggregation properly. Avoid bare `asyncio.gather`.
- **Multiple interpreters (PEP 734, 3.14):** Use `concurrent.interpreters` for CPU-bound parallelism — true multi-core without `multiprocessing`'s overhead, no GIL contention.
- **Introspection:** Debug live async apps with `python -m asyncio ps <PID>` / `pstree <PID>` (3.14).
- **Free-threaded builds (PEP 703):** Be aware of the no-GIL variant. Design hot paths to avoid shared mutable state regardless of GIL presence.
- **Resources:** Wrap I/O in `with` / `async with`. Use `contextlib` for compositions.

## 6. Packages & Imports

- **Imports:** Three groups separated by blank lines — stdlib, third-party, local. Prefer absolute imports.
- **`__init__.py`:** Minimal. Use `__all__ = [...]` to declare the public API explicitly.
- **Bundled resources:** Use `importlib.resources.files(__package__).joinpath("...").read_text()` for embedded files (SQL, templates). Survives wheel and zipapp packaging — never use `__file__`-relative paths for shipped assets.

## 7. Errors & Testing

- **Exceptions:** A base custom exception per module. Always chain (`raise NewError(...) from err`). Never bare `except:`.
- **Exception groups (PEP 654, 3.11+):** `asyncio.TaskGroup` (§5) raises `ExceptionGroup` when child tasks fail — catch with `except*` (e.g. `except* TimeoutError:`), never a bare `except Exception`, or concurrent failures from separate tasks collapse into one swallowed exception.
- **Bracketless except (PEP 758, 3.14):** `except TimeoutError, ConnectionRefusedError:` is now valid without parens when no `as` clause.
- **Finally hazards (PEP 765, 3.14):** `return` / `break` / `continue` inside `finally` now emits SyntaxWarning — refactor it out.
- **Iterables:** `map(strict=True)` (3.14) when consuming parallel iterables, matching `zip(strict=True)`.
- **Testing:** `pytest 9` with `conftest.py` fixtures. Never the legacy `unittest` module. `pytest-asyncio` for async tests.
- **Integration tests against Docker dependencies:** `testcontainers-python` — spins up real Postgres/Redis/Kafka/etc. containers per test run instead of mocking the driver or relying on a shared dev instance. Mark these with a dedicated `pytest` marker (e.g. `@pytest.mark.integration`) and exclude by default so `pytest` stays fast.

## 8. Documentation

- **Docstrings:** Google style (Args, Returns, Raises).
- **DRY:** Don't repeat type info already in hints.
- **Focus:** Explain *why* (domain rules, edge cases), not *what*.

## 9. Stdlib defaults

Prefer stdlib when it covers the use case.

- `pathlib.Path` for all paths — never `os.path` strings. New in 3.14: `Path.copy()`, `Path.move()`, `Path.copy_into()`, `Path.move_into()` for recursive operations.
- `compression.zstd` (3.14) over `gzip` / `bz2` for new payloads — `gzip` / `bz2` / `lzma` / `zlib` are now re-exported under `compression.*`.
- `importlib.resources` for shipped files (see §6).
- `contextlib` for resource lifecycle composition.
- `dataclasses` for data containers (see §3).

## 10. Database access — SQL files + `importlib.resources`

**Recommended pattern, not mandatory.** Mirrors the Go `sqlx + //go:embed` philosophy: raw SQL in `.sql` files, loaded once at module import, executed via `psycopg 3`. No ORM by default — keeps queries auditable in git and gives editors full SQL syntax highlighting and linting.

```python
from importlib.resources import files
import psycopg
from psycopg.rows import class_row

GET_USER_BY_ID = files(__package__).joinpath("queries/get_user_by_id.sql").read_text()

class UserRepo:
    def __init__(self, conn: psycopg.AsyncConnection) -> None:
        self._conn = conn

    async def get_by_id(self, user_id: int) -> User | None:
        async with self._conn.cursor(row_factory=class_row(User)) as cur:
            await cur.execute(GET_USER_BY_ID, (user_id,))
            return await cur.fetchone()
```

Layout:

```
src/myapp/userrepo/
├── __init__.py
├── repo.py
└── queries/
    ├── get_user_by_id.sql
    ├── insert_user.sql
    └── list_users.sql
```

- **Driver:** `psycopg 3` — sync + async, server-side cursors, COPY, prepared statements.
- **Migrations:** `alembic` — versioned, works with raw SQL (no SQLAlchemy ORM required).
- **Dynamic queries:** Compose `.sql` fragments in Python; never concatenate user input — bind parameters.
- **When an ORM is genuinely needed:** SQLAlchemy 2.x (Core or ORM). Record the decision in an ADR.

## 11. Tooling

- **Environment + packaging:** `uv` — replaces `pip`, `pip-tools`, `virtualenv`, `pyenv`. Single binary, fast. Commit `uv.lock`; run `uv sync --frozen` in CI.
- **Lint + format:** `ruff` — replaces `black`, `isort`, `flake8`, `pyupgrade`. One config, one tool. Drop-in template: [`assets/ruff.toml`](assets/ruff.toml) — copy to your project root as `ruff.toml` (or fold into `pyproject.toml` under `[tool.ruff]`) and set `known-first-party` to your package name. Run `ruff check` and `ruff format --check` on every commit and in CI; treat warnings as errors.
  - **Correctness & bugs:** `F` (pyflakes), `B` (bugbear, incl. `B006`/`B008` mutable defaults — see §3, and `B904` exception chaining — see §7), `ASYNC` (asyncio anti-patterns — see §5), `RUF` (ruff-specific, e.g. `RUF012` mutable class defaults).
  - **Security:** `S` (flake8-bandit) — SQL/command injection, hardcoded secrets, weak crypto. Test files relax `S101`/`S105`-`S107` via `per-file-ignores` since asserts and fixture creds are expected there.
  - **Typing discipline:** `ANN` (typed signatures — the mypy `--strict` baseline), `TC` (`TYPE_CHECKING` guards, with `runtime-evaluated-base-classes` carved out for Pydantic/Settings — see §3), `PYI` (stub-file quality).
  - **Modernization:** `UP` (pyupgrade — see §1), `FA` (future annotations), `FURB` (refurb), `PERF` (perflint).
  - **Style & structure:** `I` (isort), `N` (pep8-naming), `C4` (comprehensions), `SIM` (simplify), `RET`/`RSE` (control-flow and raise style), `PIE`, `PTH` (pathlib over `os.path` — see §9), `ISC`, `TID`, `A` (no builtin shadowing).
  - **Complexity & size:** `PL` (pylint subset), thresholds tuned in `[lint.pylint]` (`max-args = 7`, `max-branches = 12`, `max-returns = 6`, `max-statements = 50`) — split functions instead of suppressing.
  - **Test style:** `PT` (flake8-pytest-style) — fixture/mark parenthesis conventions tuned in `[lint.flake8-pytest-style]` (see §7).
  - **Docs & dead code:** `D` (pydocstyle, Google convention — see §8), `ERA` (eradicate — no commented-out code).
  - **Test-file relaxations:** `per-file-ignores` drops `ANN`, `D`, `S101`, `PLR2004`, `SLF001`, `INP001` under `tests/**` — type hints and docstrings on test functions add noise without value; asserts, magic numbers, and private-member access are the point of a test.
  - **Auto-fix guardrails:** `fixable = ["ALL"]`, but `unfixable` excludes `ERA`, `F401`, `F841` — never let `--fix` silently delete commented-out code or unused imports/locals; those need a human decision.
- **Type checking:** `mypy --strict` as the baseline — no `Any`-by-default escape hatches. Drop-in template: [`assets/mypy.ini`](assets/mypy.ini) — copy to your project root (or fold `[mypy]` into `pyproject.toml`'s `[tool.mypy]`) and set `packages` to your package name.
  - **Beyond `--strict`:** `warn_unreachable`, `warn_redundant_casts`, `warn_unused_ignores`, `strict_equality`, `extra_checks` — catch dead branches, stale `# type: ignore` comments, and cross-type equality bugs that `--strict` alone misses.
  - **Per-module overrides:** relax `disallow_untyped_defs` under `tests.*` (fixtures and `@pytest.mark.parametrize` routinely defeat full inference); `ignore_errors` under `migrations.*` (Alembic-generated, not hand-typed); scope `ignore_missing_imports` to named untyped dependencies instead of a blanket override, which would silently swallow first-party import typos too.
  - **CI parity:** run `ruff check`, `ruff format --check`, and `mypy` as three separate, mandatory CI gates — a formatting fix should never ride along with a type fix in the same commit.
- **Test:** `pytest 9` + `pytest-asyncio` for async paths. `pytest-cov` for coverage gating in CI.

## Canonical libraries

See [STACK.md](STACK.md) for the full pinned list — pydantic, pydantic-settings, fastapi, uvicorn, httpx, pytest, pytest-asyncio, mypy, ruff, uv, typer, psycopg, alembic.
