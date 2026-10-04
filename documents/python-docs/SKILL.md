---
name: python-docs
description: Python documentation conventions — a Google-style docstring on every public module, class, and function, enforced by ruff's pydocstyle (D) rules with the google convention, and LLM-ready markdown CLI reference generation for Click or Typer tools via a reproducible docgen helper. Use when writing or reviewing docstrings, choosing or enforcing a docstring style, configuring ruff's D rules, deciding where module or package docstrings belong, or generating markdown CLI documentation for a Click/Typer-based Python tool.
license: MIT
---

# Python documentation conventions

Docstrings are the API's reference manual: editors, `help()`, and doc generators render them, and
LLM coding agents read them to learn an API. These rules say where they go, what style they take,
and how the linter enforces them. For the code itself see the `python-style` skill.

## 1. A docstring on every public API, Google style

Every public module, class, function, and method carries a docstring; private (`_`-prefixed) and
trivial dunder methods do not need one. Use **Google style** — a one-line imperative summary, then
`Args:`, `Returns:`, `Raises:` as needed:

```python
def parse(line: str) -> tuple[str, str]:
    """Split a KEY=VALUE line into its key and value.

    Args:
        line: A single ``key=value`` pair; whitespace around each side is trimmed.

    Returns:
        The ``(key, value)`` pair.

    Raises:
        ValueError: If the separator is missing or the key is empty.
    """
```

Document behavior and invariants the caller can rely on, not the implementation. Types live in the
annotations (see `python-typing`), so do not repeat them in the docstring prose.

## 2. Module and package docstrings

Every module starts with a docstring on line 1 (after `from __future__ import annotations` if
present) describing what it provides. A package's docstring lives in its `__init__.py`.

## 3. Enforce with ruff's D rules

Make docstring presence and format a lint error, not a review nit — add the `D` family and pin the
convention so ruff checks Google style specifically:

```toml
[tool.ruff.lint]
extend-select = ["D"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["D"]   # tests document themselves through their names
```

`uv run ruff check` now flags missing and malformed docstrings.

## 4. Generate an LLM-ready CLI reference

A Click command tree (Typer compiles to Click) already knows every command, flag, and help string —
publish it as one markdown page per command that humans, search engines, and LLMs can read:

- Give every command and option a clear help string; expose the root command from your CLI module.
- Copy [templates/docgen.py](templates/docgen.py) to `src/myapp/tools/docgen.py` and point its
  import at your command (for Typer, convert with `typer.main.get_command(app)`). It walks the tree
  writing timestamp-free markdown, so the output is reproducible.
- It imports your application packages, so it runs in-project with `uv run` — it is not a separate
  tool. Add a Makefile target:

  ```make
  docs: ## Regenerate the CLI reference (docs/cli) from the command tree
  	uv run python -m myapp.tools.docgen --out docs/cli
  ```

- Commit the generated `docs/cli` and refresh it whenever commands or flags change, so the
  reference never drifts from the tool.

For style see the `python-style` skill; for the Makefile and layout see `python-project`.
