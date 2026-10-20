---
name: iru-python-docstrings
description: >-
  Audit given Python file(s)/package scope (FastAPI service, Django project, or plain library) for complete, well-formed PEP 257 docstrings on every public module, package, class, function, method and property — summary line, then `Args:`/`Returns:`/`Yields:`/`Raises:`/`Attributes:` sections in the project's convention (Google unless its Ruff `[tool.ruff.lint.pydocstyle] convention`, a `ruff.toml`, or a `[pydocstyle]` config says `numpy` or `pep257`) — generate any missing or incomplete docstrings grounded in the actual code and current changes, without restating what type hints already say, then verify the result: Ruff's pydocstyle `D` rules run scoped with `--select D` even when the project doesn't enable them (plus the preview pydoclint `DOC` rules as an advisory check for undocumented returns/raises), `interrogate` when the project configures it, and a build of the project's API docs with warnings as errors — Sphinx (autodoc + napoleon, `docs/api/conf.py` per this catalog's scaffold contract, or `docs/conf.py`/`docs/source/conf.py`), MkDocs + mkdocstrings (`mkdocs build --strict`), or pdoc — into a throwaway directory to prove every docstring renders. Framework-aware: Django migrations are never touched; FastAPI route-function docstrings become OpenAPI operation descriptions and Pydantic model docstrings become schema descriptions, so their developer-only sections go after a `\f` (the skill handles the resulting Ruff `D301`); DRF/Ninja view docstrings feed their schema the same way. Detects the runner (`uv run`, `poetry run`, `pdm run`, `pipenv run`, `.venv/bin/`) at runtime. Invoke as `/iru-python-docstrings <path-or-glob>` (comma-separated paths/globs or dotted module names accepted), or `/iru-python-docstrings` with no argument to scope to Python files touched by uncommitted changes plus commits on the current branch not yet on the base branch. Use whenever the user wants docstring completeness checked and filled in for specific Python code, instead of relying on a docs build to surface gaps (Sphinx autodoc silently renders an undocumented member as a bare signature, or skips it).
model: sonnet
allowed-tools: Read Edit Write Glob Grep Bash(git *) Bash(uv run *) Bash(uvx *) Bash(uv tree *) Bash(poetry run *) Bash(pdm run *) Bash(pipenv run *) Bash(.venv/bin/*) Bash(python -m *) Bash(python3 -m *) Bash(python3 -c *) Bash(command -v *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(head *) Bash(test *) Bash(mkdir -p build*) Bash(rm -rf build/iru-python-docstrings-*)
---

# Python Docstrings

Make sure a set of Python modules carry complete, well-formed docstrings, filling in whatever is missing, then prove
the result is valid through Ruff's docstring rules and the project's own API-docs build. This skill only adds/completes
docstrings (and, when the project lists modules explicitly, the API-docs entry that makes a new public module render)
— it does not change behavior, signatures, type hints, decorators, imports, or any non-docstring code. Test code
(`tests/`, `test_*.py`, `*_test.py`, `conftest.py`) is out of scope — it doesn't need docstrings added, even if named
explicitly — but any docstring a test already has must be left as-is. It makes no assumptions about this being any
particular repository — discover the project's flavor, conventions, and tooling fresh each run.

## Step 0 — Detect the project's flavor and runner

Flavor, first match wins (the same markers `iru-explore` uses): a root `manage.py` or `django` in the project's
dependencies → **django**; `fastapi` in the dependencies → **fastapi**; anything else with a `pyproject.toml`/
`setup.cfg`/`setup.py` → **library**. The flavor decides what's excluded (Step 1) and the API-facing caveats (Step 2).

Runner — detect, never install globally, never `pip install` into the system Python:

| Marker | Prefix |
|---|---|
| `uv.lock` | `uv run` (add `--group <g>` for a dependency group that isn't synced by default, e.g. `docs`) |
| `poetry.lock` | `poetry run` |
| `pdm.lock` | `pdm run` |
| `Pipfile.lock` | `pipenv run` |
| `.venv/` | `.venv/bin/<tool>` |
| none | `python3 -m <tool>` — warn that no project environment was found |

Ruff not in the project's environment (`<runner> ruff --version` fails) → use `uvx ruff` when `uv` exists and say so;
otherwise report that the Ruff check couldn't run. Editing docstrings needs no environment; only Step 5 does.

## Step 1 — Determine scope

- **Argument provided** (comma-separated paths, globs, or dotted module names): resolve each to its `.py` file(s) via
  `find`/`ls` (a dotted name → `src/<a>/<b>.py`, `<a>/<b>.py`, or `<a>/<b>/__init__.py`). Drop any resolved test file
  per the definition above — say so in the Step 6 report rather than silently ignoring it.
- **No argument**: default to every non-test `.py` file touched by uncommitted changes plus commits on the current
  branch not yet on the base branch, same approach as `iru-update-docs`:
  ```bash
  git status
  git diff <base-branch>...HEAD --name-only
  git diff --name-only
  ```
  (determine the base branch via `git symbolic-ref refs/remotes/origin/HEAD` or `git branch -a` if unclear; ask the
  user only if genuinely ambiguous).
- Always filter out virtualenvs (`.venv/`, `venv/`), `build/`, `dist/`, `node_modules/`, generated code (a
  setuptools-scm/hatch-vcs `_version.py`, `*_pb2.py`, anything git-ignored), **Django `migrations/`** (generated by
  `makemigrations`; never edited by hand, documentation included), `manage.py`, and Alembic `versions/` revisions.
- If the resulting scope is empty, tell the user there is nothing to document and stop.
- **What gets documented** (the audit set for Step 3), following PEP 257 and Ruff's own notion of "public": every
  public module (no leading underscore in the module path) and package `__init__.py`; every public class, function,
  method (including `@property`, `@classmethod`, `@staticmethod`, `@overload`-free implementations) and nested public
  class; module-level public constants and class attributes, documented through the owning module/class docstring
  (`Attributes:`) or an attribute docstring when the project uses those. A module's `__all__`, when present, is the
  authoritative public surface — a name outside it is not a gap. `_private` names, `__dunder__` magic methods and
  `__init__` are out of scope unless the project's Ruff config enables `D105`/`D107` (with the Google convention the
  constructor's arguments go in the **class** docstring's `Args:`, which is what napoleon renders by default).

## Step 2 — Discover this project's actual docstring bar before auditing

Don't assume a fixed convention — discover it from the project itself:

- **Convention**: `[tool.ruff.lint.pydocstyle] convention` (or `[lint.pydocstyle]` in `ruff.toml`/`.ruff.toml`),
  else `[tool.pydocstyle]`/`setup.cfg [pydocstyle] convention`, else `[tool.numpydoc_validation]` (numpy), else
  Sphinx `conf.py` napoleon flags (`napoleon_numpy_docstring = True` with `napoleon_google_docstring = False` →
  numpy) or mkdocstrings `docstring_style:`, else observed practice, else **Google** — this catalog's default and the
  scaffold contract's (`iru-setup-python-*` writes `convention = "google"`). A reST/Sphinx-field project
  (`:param x:`/`:returns:`) stays reST; never convert an existing style.
- **Ruff selection**: whether `D` is already in `select`/`extend-select`, what's ignored (`D105`, `D107`, `D203`…),
  and `per-file-ignores` (tests and migrations usually ignore `D`). The project's ignores are part of the bar.
- **interrogate**: `[tool.interrogate]` in `pyproject.toml` (or `.interrogate`, `setup.cfg [tool:interrogate]`) —
  `fail-under`, `ignore-init-method`, `ignore-init-module`, `ignore-magic`, `ignore-private` (double-underscore
  names only), `ignore-semiprivate` (single underscore), `ignore-property-decorators`, `ignore-nested-functions`.
- **API docs tool** (Step 5 builds whichever exists): Sphinx — `docs/api/conf.py` (this catalog's scaffold contract,
  next to Antora's `docs/antora.yml`), `docs/conf.py`, `docs/source/conf.py`, `docs/sphinx/conf.py`; MkDocs —
  `mkdocs.yml` with a `mkdocstrings` plugin; pdoc — a `pdoc` dependency or a script/CI step calling it. Note whether
  modules are listed explicitly (`.. automodule::`, `::: pkg.mod`) or discovered (`autosummary :recursive:`,
  `sphinx-apidoc`, `sphinx-autoapi`, a gen-files script).
- **Contributor guides** (`CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING`, `README`) and 2-3 well-documented modules near
  the scope: voice (imperative "Return …" vs third person "Returns …" — Google convention doesn't enforce `D401`),
  whether `Raises:` and `Examples:` (doctest `>>>`) are habitual, line length (72 chars for docstrings per PEP 8 is a
  recommendation; Ruff's `E501`/`W505` decide), and attribute style. Follow the **stricter** of stated vs observed.

**The convention, Google flavor** (adapt the section syntax for numpy — underlined `Parameters`/`Returns`/`Raises`,
`name : type` — or reST fields):

- Summary: one line, ending in a period, on the first line of the docstring (`D212` under Google), saying what the
  object does or represents; a blank line, then an optional description. Module docstrings say what the module holds;
  package `__init__.py` docstrings describe the package.
- `Args:` — one entry per parameter (`name: Description.`), `*args`/`**kwargs` included; **no types** when the
  signature has type hints (`sphinx-autodoc-typehints`, mkdocstrings and pdoc render them from the annotations —
  repeating them drifts). Say what a `None` default means, units, accepted values.
- `Returns:` / `Yields:` — what is returned, not its type again; omitted for `-> None`. `Raises:` — one
  `ExceptionType: When …` entry per exception the body raises or deliberately lets propagate (griffe/mkdocstrings
  rejects an entry that isn't `Exception: description` — verified).
- Classes: summary, then `Attributes:` for public instance/class attributes (dataclass/Pydantic/attrs fields
  included) and `Args:` for constructor parameters that aren't attributes. Properties: document the getter only,
  as an attribute ("The shelf's capacity.").
- `Examples:` with `>>>` lines only where the project already runs doctests or the API is non-obvious.
- `@deprecated`/`warnings.warn(DeprecationWarning)` → a `.. deprecated:: X.Y` note (Sphinx) carried over verbatim,
  never added on a guess.

**Framework caveats** — docstrings here are also API documentation, so write them for the API's consumers:

- **FastAPI**: a path-operation function's docstring becomes the OpenAPI operation `description` (Markdown, shown in
  Swagger UI/ReDoc) unless the decorator passes `description=`; FastAPI truncates it at the first form feed. Put the
  consumer-facing text first, then `\f`, then the developer-only `Args:`/`Returns:`/`Raises:` sections (verified:
  only the text before `\f` reaches `app.openapi()`). A non-raw docstring containing `\f` trips Ruff `D301` — add
  `# noqa: D301` after the docstring's closing quotes (verified; making the string raw would turn `\f` into two
  literal characters and break the truncation). Pydantic model docstrings become the JSON-schema `description` of
  the component (verified, `Attributes:` section included) — keep them consumer-facing too; with
  `model_config = ConfigDict(use_attribute_docstrings=True)` an attribute docstring under a field becomes that
  field's `description` (verified), otherwise use `Field(description=…)`, which is code and out of scope here. A
  `Depends` dependency function's docstring is not published.
- **Django**: models, managers, querysets, services, forms and template tags are documented like any library code;
  `Meta`/`Media` inner classes are not. DRF views/viewsets — drf-spectacular takes the view docstring as the
  operation description unless `@extend_schema(description=…)` overrides it; Django Ninja does the same with the
  operation function's docstring — so keep developer-only sections out of those or move them to a comment. Admin
  classes, `apps.py` `AppConfig`s and settings modules need only a module/class summary.

## Step 3 — Audit each in-scope file

Start with Ruff for the mechanical part, scoped to the files, with the docstring rules forced on:

```bash
<runner> ruff check --select D [--config 'lint.pydocstyle.convention = "google"'] --output-format json <files> > build/iru-python-docstrings-ruff.json
```

Pass `--config …convention…` only when the project sets no convention (then use the one Step 2 resolved) — with no
convention Ruff enables mutually incompatible rules (`D203`/`D211`, `D212`/`D213`). `--select D` replaces the
project's selection for this run but keeps its `per-file-ignores`/`ignore`. Read the JSON with `python3 -c` and keep
`code`, `filename`, `location.row`, `message` per finding — never paste the raw file. `D100`–`D107` are missing
docstrings (module, class, method, function, package, magic, nested class, `__init__`), `D417` a parameter missing
from `Args:`, the rest formatting. Write the report under `build/` (create it if needed; remove `build/` at the end
only if this run created it) and delete it afterwards.

Then read each full file — Ruff doesn't know whether a docstring is any good — and, for every symbol in Step 1's audit
set, check that the docstring exists, actually describes the symbol rather than restating its name, and is current:

- **Modules/packages**: a docstring saying what the module provides.
- **Functions/methods**: summary; `Args:` entry for every parameter, in signature order, none for removed/renamed
  parameters; `Returns:`/`Yields:` when a value is returned/yielded; `Raises:` for each exception that can propagate.
- **Classes**: summary; `Attributes:` for public fields; constructor `Args:` per the project's habit.
- **FastAPI routes / DRF views / Ninja operations / Pydantic models**: consumer-facing first part, per Step 2.

For each gap record: the symbol, its kind, what's missing (whole docstring vs a missing/stale section or entry), and
the file.

## Step 4 — Generate the missing docstrings

Before editing, if Step 5's tools are wired, run the API-docs build (and interrogate) once and keep its warnings per
file as this run's baseline — Step 5 needs it to tell pre-existing warnings from ones the new docstrings caused.

For every gap from Step 3, write the docstring grounded in:

- The actual implementation — read the body: what is returned and when (`None`, empty list), which exceptions are
  raised or re-raised, which fields a model exposes, what a route returns per status code, which side effects happen
  (commits, emails, `transaction.on_commit` hooks). Never claim a guarantee the code doesn't give.
- Current uncommitted/branch changes (`git diff` / `git log -p` for that file) — describe current behavior, not what
  the name suggests.
- The convention from Step 2 — section names, voice, indentation, wrapping — so new docstrings are indistinguishable
  from hand-written ones.

Apply the edits with the Edit tool, as the first statement of the module/class/function (a module docstring goes
above the imports, after a license header comment or shebang/encoding line). Do not modify code, signatures, type
hints, decorators, or formatting outside the added/completed docstrings, and don't reorder members.

**API-docs reachability**: when the project lists modules explicitly (Step 2) and an in-scope public module is new and
listed nowhere, add the entry that makes it render — an `.. automodule:: <pkg.mod>` with `:members:` in
`docs/api/index.rst` (or the project's per-module `.rst` layout), or a `::: <pkg.mod>` line on the matching MkDocs
page. Discovered layouts (autosummary `:recursive:`, autoapi, apidoc in CI) need nothing. Say in the report which
entries were added.

## Step 5 — Verify

Run what the project has, scoped where the tool allows it, through Step 0's runner. Write every output under `build/`
with an `iru-python-docstrings-` prefix and delete it afterwards.

1. **Ruff `D`** — re-run Step 3's command. Every finding in an in-scope file must be gone (a `D` finding in a symbol
   this run didn't touch but that sits in an in-scope file is still a gap — fix it). Then the advisory pydoclint
   rules, which catch what `D` can't:
   ```bash
   <runner> ruff check --preview --select DOC [--config '…convention…'] --output-format json <files>
   ```
   `DOC201` (return not documented), `DOC402` (yield not documented), `DOC501` (raised exception missing from
   `Raises:`), `DOC502` (documented exception never raised). These are preview rules (Ruff 0.17) — fix the ones in
   docstrings you wrote, report the rest as advisory, and note that `--output-format concise` prints rule *names*
   instead of codes for preview rules, which is why JSON is used. They only check functions whose docstring has
   sections; a one-line summary docstring isn't flagged.
2. **interrogate** (only when configured — Step 2): `<runner> interrogate -c pyproject.toml -vv <paths>` (or `uvx
   interrogate …` when it isn't a project dependency). Exit 1 means coverage is under the project's `fail-under`; the
   `-vv` table marks each symbol `COVERED`/`MISSED` — every `MISSED` in an in-scope file must be fixed or explained
   (e.g. a single-underscore method interrogate counts because the project didn't set `ignore-semiprivate`).
3. **API docs build, warnings as errors**, into a throwaway target so the project's real output is untouched:
   - **Sphinx** (`<sphinx-dir>` = the directory holding `conf.py` from Step 2; `docs/api` per the scaffold contract):
     ```bash
     uv run --group docs sphinx-build -W --keep-going -b html <sphinx-dir> build/iru-python-docstrings-site
     ```
     (other runners: `<runner> sphinx-build …`; use the dependency group/extra the project declares Sphinx in — the
     contract's is `docs`). Exit 1 = at least one warning. Warnings name their source as
     `<path>.py:docstring of <dotted.name>:<line>: WARNING: …` — the line is relative to the docstring. Typical
     docstring-caused ones: `Unexpected indentation`, `Block quote ends without a blank line`, `Bullet list ends
     without a blank line`, `Inline emphasis start-string without end-string` (an unescaped `*args` — write
     `` ``*args`` `` or `\*args` in reST, though napoleon handles `*args` inside `Args:`), `undefined label`/`py:class
     reference target not found` with `-n`, and `duplicate object description of <x>` — a dataclass/Pydantic field
     documented both in the class's `Attributes:` section and by autodoc's own member listing (verified; fixed by the
     project setting `napoleon_use_ivar = True`, or by `:no-index:`/excluding members — a `conf.py` change: report it,
     don't make it). A warning about a module that fails to import (`autodoc: failed to import`) is an environment/
     config problem — for Django the `conf.py` must set `DJANGO_SETTINGS_MODULE` and call `django.setup()` before
     autodoc imports models; report it as pre-existing rather than editing `conf.py`.
   - **MkDocs + mkdocstrings**: `<runner> mkdocs build --strict -d build/iru-python-docstrings-site` (from the
     directory holding `mkdocs.yml`; `-f <path>` otherwise). griffe's docstring parser warnings
     (`griffe: <file>:<line>: Failed to get 'exception: description' pair …`, `No type or annotation for parameter
     …`, `Parameter … does not appear in the function signature`) abort a strict build — fix those in in-scope files.
   - **pdoc**: `<runner> pdoc -d <google|numpy|restructuredtext> -o build/iru-python-docstrings-site <in-scope
     modules>` naming the in-scope modules explicitly — pdoc exits non-zero with a traceback when a named module fails
     to import, but when walking a package it skips broken submodules silently, and it never validates docstring
     syntax (it renders whatever it gets), so Ruff is the real check on a pdoc project.
   - None of the three configured → say so: no API-docs build exists, so only Ruff (and interrogate) verified the
     docstrings. Don't add a docs toolchain — that is `iru-setup-python-*`'s job.
   Compare against the Step 4 baseline: any **new** warning naming an in-scope file was caused by this run — fix and
   re-run until none remain. Pre-existing warnings are not this skill's to fix.
4. **FastAPI** (only when a route/model docstring was touched and the project has the export script from the scaffold
   contract): `uv run python scripts/export_openapi.py build/iru-python-docstrings-openapi.json`, then confirm the
   touched operations' `description`s contain no `Args:`/`Returns:` text.

A failure naming a symbol or file **outside** the current scope is pre-existing — mention it in the report as a
follow-up, don't fix it unless the user asks.

## Step 6 — Report

Per file in scope: how many symbols were already fully documented, how many gaps were found and filled (name each,
with its kind and what was added — e.g. "`Shelf` class: summary + `Attributes:` (2)", "`add()`: `Raises: ValueError`",
"`list_books` route: consumer description + `\f` + `Args:`"), and any API-docs entry added (Step 4). Then the
verification result per tool that ran — Ruff `D`: clean or the remaining codes; Ruff `DOC` (advisory): remaining
codes; interrogate: coverage % vs `fail-under`; Sphinx/MkDocs/pdoc: pass, or the warnings still open — and which
tools weren't available or configured. Name the convention used and where it came from, any argument dropped as a
test file or migration, and out-of-scope pre-existing failures as follow-ups. Never paste raw tool output or JSON.

Do not fix lint or type issues unrelated to docstrings, change code to make a docstring "true", edit `conf.py`/
`mkdocs.yml`/Ruff config, edit license headers, or add/modify tests — those belong to `iru-python-code-quality`, the
coding skills, and the user.

## Verification notes

Verified in `$TMPDIR/iru-verify/python/docs-bump/demo/` (a `uv init --lib` project, uv 0.12.8, CPython 3.13, Ruff
0.17.0, Sphinx 9.1.0 with `sphinx.ext.autodoc` + `sphinx.ext.napoleon` + `sphinx_autodoc_typehints` in a `docs` dependency
group, `docs/api/conf.py` + `index.rst` per the scaffold contract):

- `ruff check --select D --config 'lint.pydocstyle.convention = "google"' --output-format json src` on undocumented
  code reported `D100`/`D101`/`D102`/`D105` with `code`/`filename`/`location.row`/`message`; a partial `Args:` gave
  `D417`; with `[tool.ruff.lint.per-file-ignores] "tests/**" = ["S101", "D"]` the tests stayed clean under
  `--select D`; switching the override to `numpy` flagged Google sections (`D406`/`D407`).
- `--preview --select DOC` reported `DOC501` (missing `Raises: ValueError`) and `DOC201`; without `--preview` Ruff
  warns the selection has no effect. A summary-only docstring wasn't flagged by `DOC201`.
- `uv run --group docs sphinx-build -W --keep-going -b html docs/api build/iru-python-docstrings-site`: exit 1 with
  `…/shelf.py:docstring of demo_lib.shelf.titles_by:17: WARNING: Bullet list ends without a blank line; unexpected
  unindent. [docutils]`; exit 1 with `duplicate object description of demo_lib.shelf.Shelf.capacity` for a dataclass
  with an `Attributes:` section (cleared by `napoleon_use_ivar = True`); exit 0 once fixed. A mis-indented
  continuation line inside `Args:` produced no Sphinx warning (napoleon is lenient) — Ruff/griffe are the stricter
  checks.
- FastAPI 0.143.1: a route docstring with `\f` → `app.openapi()` description held only the text before it; Ruff
  reported `D301`, silenced by `"""  # noqa: D301` on the closing line; Sphinx rendered the `Args:` after `\f`
  cleanly. Pydantic 2.14.1: model docstring (with `Attributes:`) became the schema `description`;
  `use_attribute_docstrings=True` turned a field's attribute docstring into its `description` (needs the class in a
  real source file).
- `uvx interrogate -c pyproject.toml -vv src` (interrogate 1.7.0): exit 1 below `fail-under = 100`, listing
  `Shelf._internal … MISSED` because `ignore-private` only covers double-underscore names.
- `mkdocs build --strict` with `mkdocstrings[python]` (`docstring_style: google`): aborted on `griffe: …/shelf.py:50:
  Failed to get 'exception: description' pair …` for a free-text `Raises:` entry that Sphinx and Ruff accepted; exit 0
  after the fix.
- pdoc 16.0.0 (`-d google -o …`): exit 0 rendering the package; naming a module that fails to import → exit 1 with a
  traceback; the same module reached only by walking the package was skipped silently.

Not verified: Sphinx autodoc on a real Django project (`django.setup()` in `conf.py`), drf-spectacular/Ninja
description extraction, `sphinx-autoapi`/autosummary-recursive layouts, numpy/reST conventions end-to-end through
Sphinx, and `poetry run`/`pdm run`/`pipenv run` runners.

## Sources

- irurueta docs: programming-languages/python/docstrings.adoc (PEP 257 layout; Google/NumPy/reST styles; Sphinx
  autodoc + napoleon, pdoc, MkDocs + mkdocstrings)
- irurueta docs: programming-languages/python/lexical-structure-and-style.adoc (PEP 8, 72-char docstring lines)
- irurueta docs: programming-languages/python/debugging-and-tooling.adoc (Ruff as the default linter)
- irurueta docs: backend/fastapi/openapi-and-interactive-docs.adoc (docstring → operation description, `\f` truncation)
- irurueta docs: web/django/django-rest-framework.adoc, web/django/django-ninja.adoc (schema generation from views)
- PEP 257; Ruff rules `D` (pydocstyle) and `DOC` (pydoclint); Sphinx napoleon; mkdocstrings-python/griffe; pdoc
