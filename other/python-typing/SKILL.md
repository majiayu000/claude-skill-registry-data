---
name: python-typing
description: Python static typing and type annotations, checked with a static type checker — ty (Astral) or pyright (Microsoft/Pylance). Use when adding, writing, or reviewing type hints or annotations on Python functions, methods, parameters, or return values; adding return type annotations across a module; fixing or resolving Python type errors; making a function or class generic with a type parameter; modernizing hints to X | None instead of Optional, A | B instead of Union, and built-in list[]/dict[] generics; choosing between Protocol and ABC for an interface or using typing.Self and PEP 695 syntax; or setting up, configuring, or running ty or pyright under [tool.ty] or [tool.pyright] in pyproject.toml, migrating from mypy, and wiring a type-check step into the dev gate or CI. For Python code only — not TypeScript, Go, or other languages, not runtime isinstance checks, formatting, or test-writing.
license: MIT
---

# Python typing conventions

A static type checker is the type gate for the project: either `ty` (Astral's fast checker and
language server) or `pyright` (Microsoft's checker, the engine behind Pylance) — pick whichever the
project already uses. Type the public surface, keep the type check clean, and write modern
annotation syntax. `ty` is pre-1.0, so expect its diagnostics and config to move. For deeper edge
cases see [reference.md](reference.md).

## 1. Annotate the public surface

Every public function, method, and module-level constant gets parameter and return annotations —
that is the contract the checker enforces and editors surface. Annotate internal locals only where the
type is not obvious from the right-hand side. Avoid `Any` (it disables checking — prefer `object`,
a `Protocol`, or a type variable) and use `# type: ignore[rule-code]` with a specific code,
sparingly, never a bare blanket ignore.

## 2. Configure and run a type checker

Both checkers configure in `pyproject.toml` and run through `uv`. Use one — wire its check into
`make typecheck` and CI.

**ty** reads `[tool.ty]`. The minimal config sets the version floor and the src root; tune
individual diagnostics under `[tool.ty.rules]`:

```toml
[tool.ty.environment]
python-version = "3.13"
root = ["./src"]

[tool.ty.rules]
possibly-unresolved-reference = "warn"   # severities: "ignore" | "warn" | "error"
```

```sh
uv run ty check            # type-check the project (wire into `make typecheck` + CI)
uv run ty server           # the LSP language server, for editor integration
```

**pyright** reads `[tool.pyright]` (or a standalone `pyrightconfig.json`, which takes precedence if
present). Set the checked paths and the interpreter version; `typeCheckingMode` selects strictness
(`"basic" | "standard" | "strict"`, default `"standard"`):

```toml
[tool.pyright]
include = ["src"]
pythonVersion = "3.13"
typeCheckingMode = "standard"
```

```sh
uv add --dev pyright       # pin it in the dev dependency group
uv run pyright             # type-check the project (or `uvx pyright` for a one-off run)
```

## 3. Write modern annotation syntax

- **`X | None`, not `Optional[X]`; `A | B`, not `Union`.** Built-in generics (`list[int]`,
  `dict[str, int]`) — never the deprecated `typing.List`/`Dict`. The ruff `UP` rules (see
  `python-style`) rewrite the old forms.
- **PEP 695 type parameters and aliases** (3.12+) instead of `TypeVar`/`TypeAlias`:

  ```python
  def first[T](items: list[T]) -> T: ...

  class Box[T]:
      def __init__(self, value: T) -> None:
          self.value = value

  type Vector = list[float]
  ```

- **`typing.Self`** for fluent/factory methods that return their own type; **`@override`** (3.12+)
  on methods that override a base, so the checker catches signature drift.

## 4. Prefer Protocol over ABC for interfaces

Structural typing keeps the interface at the consumer (the analogue of Go's consumer-defined
interfaces) — no base class to inherit, and any object with the right shape satisfies it:

```python
from typing import Protocol

class Reader(Protocol):
    def read(self, size: int) -> bytes: ...
```

Reserve `abc.ABC` for when you need shared implementation or runtime `isinstance` enforcement.

## 5. Deferred annotations

Default to `from __future__ import annotations` at the top of each module: annotations become
strings, so forward references need no quotes, import cycles used only for typing disappear, and
there is no runtime cost. Guard typing-only imports behind `if TYPE_CHECKING:`. The exception is
code that introspects annotations at runtime (some serializers/validators) — see
[reference.md](reference.md).

For runtime data validation reach for a model library; plain annotations are not checked at
runtime. For style and the ruff `UP` rules see the `python-style` skill; for typing test doubles
see `python-testing`; for the `make typecheck` target and CI wiring see `python-project` and
`python-release`.
