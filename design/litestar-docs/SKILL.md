---
name: litestar-docs
description: "Use when working with zensical.toml, docs/conf.py, sphinx, shibuya, litestar-sphinx-theme, mkdocstrings, Griffe, objects.inv, or API reference docs. Not for OpenAPI route schemas."
---

# litestar-docs

Dual-engine documentation architecture for `litestar-org` and ecosystem repositories, supporting both **Sphinx** (`docs/conf.py` + `shibuya` / `litestar-sphinx-theme` + `autodoc` / `napoleon`) and **Zensical** (`zensical.toml` + `mkdocstrings-python` / Griffe static AST). Match the repository's chosen documentation engine and apply shared quality invariants across both.

## Documentation Engine Matrix

| Aspect | Sphinx (`docs/conf.py`) | Zensical (`zensical.toml`) |
| --- | --- | --- |
| **Primary Config** | `docs/conf.py` | `zensical.toml` |
| **Markup Formats** | `.rst` (reStructuredText) + `.md` (`myst-parser`) | `.md` (Python Markdown + `pymdown-extensions`) |
| **Theme & Styling** | `shibuya` or `litestar-sphinx-theme` (`docs/_static/custom.css`) | `variant = "modern"` (`docs/stylesheets/extra.css`) |
| **Python API Extraction** | `sphinx.ext.autodoc` + `sphinx.ext.napoleon` | `mkdocstrings-python` (Griffe static AST) |
| **Cross-Repo Linking** | `sphinx.ext.intersphinx` (`objects.inv`) | `mkdocstrings` (`enable_inventory = true`, `objects.inv`) |
| **UI Components & Tabs** | `sphinx-design` (`.. grid::`, `.. tab-set::`), `auto-pytabs` | `pymdownx.tabbed` (`content.tabs.link`), `pymdownx.details` |
| **Code Inclusion** | `.. literalinclude::` | `pymdownx.snippets` (`--8<--`, `check_paths = true`) |
| **CLI Reference** | `sphinx-click` (`.. click::`) | `tools/docs/generate_cli_docs.py` |
| **Diagrams** | `sphinxcontrib-mermaid` (`.. mermaid::`) | `pymdownx.superfences` (```` ```mermaid ````) |

## Core Rules

- **Match the repository's existing documentation engine.** Reason: Both Sphinx and Zensical are first-class engines in the Litestar ecosystem; inspect `docs/conf.py` vs `zensical.toml` before making edits.
- **Enforce a `68–75ch` (`46rem`) reading column with persistent left and right sidebars.** Reason: Uncapped prose columns and hidden right-hand `"On this page"` outlines degrade scannability on technical pages.
- **Cap guide pages at `<= 12` viewports (`~80–200` lines) and Reference pages at `<= 120 KB` HTML (`<= 14` TOC items).** Reason: Monolithic module dumps with 15+ classes and 200+ inherited methods bury primary constructors.
- **Disable inherited members on leaf classes and show base classes (`show_bases = true` / `:show-inheritance:`).** Reason: Base driver or repository methods belong once on the base class Reference page.
- **Document every public `TypedDict` and `msgspec.Struct` field with a PEP 257 inline docstring immediately below the field.** Reason: Sphinx `autoclass` renders zero fields without inline attribute docstrings, and Griffe requires them to build structured parameter tables.
- **Never write docstrings on `@overload` stubs or leak internal compiler notes (`mypyc`, `PyCapsule`) into public docstrings.** Reason: Both engines render overload docstrings ahead of the implementation docstring.
- **Execute standalone `docs/examples/**/*.py` modules in `pytest`.** Reason: Standalone modules checked by `ruff`, `pyright`, and `pytest` stay runnable and prevent snippet rot.
- **Use `[data-md-color-scheme]` CSS classes (not `<picture><source media="(prefers-color-scheme: dark)">`) for light/dark hero banners on Zensical pages, hide single-page left sidebars on `Home`, and omit redundant `<h1>` titles above hero logos.** Reason: `<picture>` media queries only respond to OS-level dark mode and fail when toggling Zensical's theme button (`[data-md-color-scheme="slate"]`).
- **Keep headings unnumbered and free of inline `` `code` `` pills, reserve bordered code pills strictly for clickable links (`a > code`), keep tab labels short (`white-space: nowrap`), and never write `\|` inside backticked code in Markdown tables.** Reason: Python-Markdown splits table cells on `|` before backticks are parsed (leaving literal `\|` in `<code>`), and bordered pills on every non-link code span create visual noise.

## Quick Reference

| Topic | Reference File | Key Contents |
| --- | --- | --- |
| Sphinx Architecture | [`references/sphinx-architecture.md`](references/sphinx-architecture.md) | `docs/conf.py`, `shibuya` / `litestar-sphinx-theme`, `autodoc` + `napoleon`, `sphinx-design`, `custom.css` |
| Zensical Architecture | [`references/zensical-architecture.md`](references/zensical-architecture.md) | `zensical.toml`, built-in plugins, `mkdocstrings-python`, `pymdownx`, `postbuild.py`, `verify_docs_artifacts.py` |
| Information Architecture | [`references/information-architecture.md`](references/information-architecture.md) | Domain tabs (`Learn`, `Databases`, `Integrations`, `Reference`), page budgets, WCAG AAA palette, tutorial structure |
| Python Docstrings | [`references/python-docstrings.md`](references/python-docstrings.md) | Google style, inline `TypedDict` / `msgspec.Struct` docstrings, type alias leak prevention, AST scanner |
| Database Adapter Docs | [`references/database-adapters.md`](references/database-adapters.md) | Central Capability Matrix, 1-page per-driver guide, own-symbols-only Reference templates (Sphinx & Zensical) |
| Polyglot & CLI Docs | [`references/polyglot-cli.md`](references/polyglot-cli.md) | TypeScript (`TypeDoc` / `mkdocstrings-typescript`), Rust (`.pyi` stubs + `/rustdoc/`), Click CLI generation |
| Interop & Redirects | [`references/migration-interop.md`](references/migration-interop.md) | Directive translation matrix, cross-engine `objects.inv` linking, URL redirect stubs |

<workflow>

## Workflow

### Step 1: Detect Engine and Configure Dependencies

Inspect the repository root for `docs/conf.py` (Sphinx) or `zensical.toml` (Zensical):

- **Sphinx Track**: Configure `[dependency-groups] doc` with `sphinx`, `shibuya` (or `litestar-sphinx-theme`), `sphinx-design`, `sphinx-copybutton`, `sphinx-click`, `sphinxcontrib-mermaid`, `auto-pytabs`, and `myst-parser`. Configure `docs/conf.py` with `sphinx.ext.autodoc`, `sphinx.ext.napoleon`, and `sphinx.ext.intersphinx`. See [`references/sphinx-architecture.md`](references/sphinx-architecture.md).
- **Zensical Track**: Configure `[dependency-groups] doc` with `zensical>=0.0.71`, `mkdocstrings-python>=2.0.1`, `pymdown-extensions>=10.16`, and `ruff>=0.15.0`. Configure `zensical.toml` with `use_directory_urls = true`, `navigation.tabs`, `toc.follow`, `pymdownx.snippets` (`check_paths = true`), and `enable_inventory = true`. See [`references/zensical-architecture.md`](references/zensical-architecture.md).

### Step 2: Enforce Docstring and `TypedDict` Hygiene

Run `tools/docs/scan_public_docstrings.py --check-leaks --check-overloads --check-typeddicts <pkg>` before building docs. Ensure every public `TypedDict` and `msgspec.Struct` field has an inline PEP 257 docstring and zero duplicate class-level `Attributes:` blocks. See [`references/python-docstrings.md`](references/python-docstrings.md).

### Step 3: Structure Domain Tabs and Runnable Examples

Organize top-level navigation into task-oriented sections (`Learn`, `Databases` when multi-driver, `Integrations`, `Reference`, `Playground` when applicable, `Project`). Author runnable scripts under `docs/examples/<area>/<topic>.py` with `main()` entry points, include them via `.. literalinclude::` (Sphinx) or `--8<--` (Zensical), and execute them in `tests/unit/docs/test_examples.py`. See [`references/information-architecture.md`](references/information-architecture.md).

### Step 4: Author Curated Reference Pages (`<= 120 KB` HTML, `<= 14` TOC items)

Group API directives (`.. autoclass::` in Sphinx or `:::` in Zensical) under `2–5` H2 category headings per Reference page with explicit member allowlists. Keep `inherited_members: false` / `:no-inherited-members:` on leaf classes so inherited base methods are documented once on the base class page. For Click CLIs, use `.. click::` (`sphinx-click`) in Sphinx or `tools/docs/generate_cli_docs.py` in Zensical.

### Step 5: Run Build and Quality Gates

- **Sphinx**: Run `uv run sphinx-build -b html -W --keep-going docs site` and verify output artifacts.
- **Zensical**: Run `zensical build --clean`, `tools/docs/postbuild.py`, and `tools/docs/verify_docs_artifacts.py`.

</workflow>

<guardrails>

## Guardrails

- **Never hide `.sy-rside` (Sphinx) or `.md-sidebar--secondary` (Zensical) in custom CSS.** Reason: Hiding the right-hand `"On this page"` outline traps readers on multi-section guides and API pages.
- **Never load `numpydoc` or `sphinx_autodoc_typehints` alongside `sphinx.ext.napoleon` in Sphinx.** Reason: Combining them double-parses docstrings and duplicates union types across signatures and parameter lists.
- **Never place `:no-index:` on primary `.. automodule::` directives in Sphinx.** Reason: `:no-index:` strips HTML `id=""` anchors from public classes and breaks `:class:` cross-references across the site.
- **Never enable inherited members on leaf adapter or plugin classes.** Reason: Repeating 40+ base methods across adapter pages inflates HTML past `400 KB` and duplicates search results.
- **Never use `mkdocs-click` on Click `>= 8.3` in Zensical.** Reason: `mkdocs-click` renders literal `Sentinel.UNSET` defaults and drops positional argument tables; use `tools/docs/generate_cli_docs.py`.
- **Never map `"path/foo.md" = "path/foo/index.md"` in Zensical `redirect_maps` when `use_directory_urls = true`.** Reason: Both resolve to `site/path/foo/index.html` and create a self-redirect loop; emit flat `site/path/foo.html` stubs in `postbuild.py`.
- **Never use `<picture><source media="(prefers-color-scheme: dark)">` for hero banners inside Zensical Markdown pages.** Reason: Zensical switches themes via `[data-md-color-scheme="default"|"slate"]` without altering the browser's OS media query, causing the light-mode dark-ink banner to render invisibly on the dark slate canvas.
- **Never style non-link inline `` `code` `` spans with heavy border pills or place inline `` `code` `` / numbering in `##`/`###` headings.** Reason: Bordered pills on every identifier clutter prose and tables, and code spans in headings wrap awkwardly in both the main column and the right-hand TOC.

</guardrails>

<validation>

## Validation Checkpoint

- [ ] `uv run python -m tools.docs.scan_public_docstrings --check-leaks --check-overloads --check-typeddicts <pkg>` exits `0`
- [ ] Documentation build (`sphinx-build -b html -W --keep-going docs site` or `zensical build --clean`) exits `0` with zero warnings
- [ ] `objects.inv` exists in the built output directory and is non-empty
- [ ] Every built Reference HTML file is `<= 120,000` bytes with `<= 14` `"On this page"` TOC items
- [ ] `uv run pytest tests/unit/docs/ -q` passes with zero inline comments in `docs/examples/`

</validation>

<example>

## Example — Curated Adapter Reference Page (Zensical & Sphinx)

### Zensical (`docs/reference/adapters/asyncpg.md`)

````markdown
# AsyncPG API Reference

```python
from sqlspec.adapters.asyncpg import AsyncpgConfig, AsyncpgDriver
```

API reference for `sqlspec.adapters.asyncpg`. Inherited execution methods are documented on [`AsyncDriverAdapterBase`](../driver/async.md).

## Configuration & Parameter Types

::: sqlspec.adapters.asyncpg.AsyncpgConfig
    options:
      members:
        - provide_connection
        - provide_session
        - provide_pool
        - create_pool
        - close_pool

::: sqlspec.adapters.asyncpg.config.AsyncpgPoolConfig

## Driver & Exception Handling

::: sqlspec.adapters.asyncpg.AsyncpgDriver
    options:
      inherited_members: false
      show_bases: true
      members:
        - dialect
        - data_dictionary
````

### Sphinx (`docs/reference/adapters/asyncpg.rst`)

```rst
AsyncPG API Reference
=====================

.. code-block:: python

    from sqlspec.adapters.asyncpg import AsyncpgConfig, AsyncpgDriver

API reference for ``sqlspec.adapters.asyncpg``. Inherited execution methods are documented on :class:`~sqlspec.driver.AsyncDriverAdapterBase`.

Configuration & Parameter Types
-------------------------------

.. autoclass:: sqlspec.adapters.asyncpg.AsyncpgConfig
    :members: provide_connection, provide_session, provide_pool, create_pool, close_pool
    :no-inherited-members:
    :show-inheritance:

.. autoclass:: sqlspec.adapters.asyncpg.config.AsyncpgPoolConfig
    :members:
    :no-inherited-members:

Driver & Exception Handling
---------------------------

.. autoclass:: sqlspec.adapters.asyncpg.AsyncpgDriver
    :members: dialect, data_dictionary
    :no-inherited-members:
    :show-inheritance:
```

</example>

## References Index

- [Sphinx Documentation Architecture](references/sphinx-architecture.md)
- [Zensical Documentation Architecture](references/zensical-architecture.md)
- [Information Architecture & Page Budgets](references/information-architecture.md)
- [Python Docstrings & API Hygiene](references/python-docstrings.md)
- [Database Adapter Documentation](references/database-adapters.md)
- [Polyglot TypeScript, Rust, and Click CLI Docs](references/polyglot-cli.md)
- [Engine Interoperability, Syntax Translation & Redirects](references/migration-interop.md)

## Official References

- <https://www.sphinx-doc.org/en/master/> — Sphinx documentation
- <https://shibuya.lepture.com/> — Shibuya Sphinx theme
- <https://zensical.org/docs/> — Zensical documentation
- <https://mkdocstrings.github.io/python/> — mkdocstrings-python & Griffe options

## Shared Styleguide Baseline

- [General Principles](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [CI/CD](../litestar-styleguide/references/ci-cd.md)
