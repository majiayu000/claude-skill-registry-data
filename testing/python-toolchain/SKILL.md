---
name: python-toolchain
description: Use when laying down or changing the configuration every Python distribution carries once in `pyproject.toml` — the src layout, the linter's rule selection and its written function-size and complexity thresholds, the few sanctioned lint suppressions, strict type checking, the line length, the test runner's configuration block, development dependencies grouped by role, and whether a dependency this project consumes may carry a version floor — and when writing any file that names a version by hand, a Dockerfile, a compose file, a CI workflow or a hook configuration, whose versions are read from their source, never recalled. Holds alike for a service of either architecture family, a CLI tool and a library. The interpreter floor and the type-ignore policy are `python-style`'s; which runtime libraries a service's roles bring and its migration bootstrap belong to the architecture family's setup skill; the version this distribution itself declares is `python-versioning`. - Also when asked to configure ruff or mypy, why a complexity or too-many-arguments rule fired, whether a `noqa` is allowed, which line length to use, how to start a new package, library or CLI tool, where dev dependencies go, whether to pin or floor a dependency, or which version of a container image, CI action or hook to write.
---

# Python Toolchain — layout, lint, type-check and dependency declarations

The configuration a Python distribution carries **once**, whatever it is and whatever its internal
layout: where the package sits, what the linter and the type checker enforce, and how dependencies are
declared — and, the one rule reaching past `pyproject.toml`, where any other version written by hand
comes from. None of it recurs per feature. **Which** libraries a program depends on is not here — a
service's roles decide that, under its architecture family's setup skill; a library or a CLI tool with
no family needs only this skill.

## When to use vs. neighbours

- The interpreter floor, its house value and the three settings that name it → `python-style`; this
  skill writes them where it says.
- A comment in `pyproject.toml`, a `Dockerfile`, a compose file, a CI workflow or a hook configuration
  → `python-style`'s **Comments**, which holds in every file the project writes by hand.
- An inline type-ignore, a `cast`, annotation coverage of tests → `python-style`, which owns the
  type-suppression policy; this skill owns only the per-package missing-stub override in the config.
- The wildcard re-export in `__init__.py` and what a package root exports → `python-packaging`.
- The version this distribution declares, and what a raised dependency floor costs a library's
  consumers → `python-versioning`.
- Which runtime and development libraries a service's roles bring, the floors its family's templates
  rely on, and the migration bootstrap → the family's setup skill (`flat-project-setup`, in the
  `pyhouse-flat` plugin, or `hex-project-setup`, in `pyhouse-hex`).
- What the test runner's configuration block must hold → `test-principles`; this skill writes the
  block, and the fixtures it loads are the family's integration-setup skill's.
- Several distributions in one repository → `python-workspace`, which writes these values once at the
  root; what they are is still this skill's.
- The image a runnable program ships in — its stages, its user, its build context →
  `python-container-image`; the tags it names are read under rule 12 here.
- How large a module may grow → the architecture's one-responsibility rule, held in review; the linter
  has no module-length rule.

## Template — ruff, mypy, pytest, hatchling (pyproject.toml)

`uv init --package --build-backend hatch myapp` lays the src layout — plain `uv init` lays a single
module that matches nothing here. Then `uv add <library>` for a runtime dependency and `uv add --dev <library>`
for a development one; `uv lock` writes the pins.

```toml
[project]
name = "myapp"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []

[dependency-groups]
dev = [
    "mypy",
    "pytest",
    # only where the suite has async tests
    "pytest-asyncio>=0.26",  # 0.26: asyncio_default_test_loop_scope
    "ruff",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 120
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "B006", "B904", "C901", "PLR0911", "PLR0912", "PLR0913", "PLR0915", "PLR0917"]

[tool.ruff.lint.mccabe]
max-complexity = 10

[tool.ruff.lint.pylint]
max-args = 7
max-positional-args = 5
max-branches = 12
max-returns = 6
max-statements = 50

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F403", "F405"]
"migrations/**/versions/*.py" = ["PLR0915"]  # only with migrations

[tool.mypy]
python_version = "3.13"
strict = true
files = ["src", "tests"]
explicit_package_bases = true
mypy_path = ["src", "."]
plugins = ["pydantic.mypy"]  # only with pydantic

[tool.pytest.ini_options]
addopts = "--import-mode=importlib"
pythonpath = ["."]
# only where the suite has async tests
asyncio_mode = "auto"
# only where a session-scoped async resource exists
asyncio_default_fixture_loop_scope = "session"
# only where a session-scoped async resource exists
asyncio_default_test_loop_scope = "session"
filterwarnings = ["error"]
```

`--import-mode=importlib` lets two test modules with one basename live in different directories — a
`test_foo.py` under both `tests/unit/` and `tests/integration/` — without an `__init__.py` in every
test directory. `pythonpath = ["."]` puts the distribution's root on the runner's path, so a test
imports shared test support by package (`tests.helpers`) — in a single distribution; in a workspace,
`python-workspace`. `filterwarnings` is `test-principles` reliability rule 8. The async lines are
`test-principles`' async mode and its one session loop (reliability rule 7, *Fixture scope rules*): the
loop scopes are required where a session-scoped async resource exists. The async lines and
`pytest-asyncio` go in together or not at all — pytest rejects a key no installed plugin declares, and
`filterwarnings = ["error"]` turns that into a failed start — and the plugin is a development
dependency (rule 10) floored at 0.26, where `asyncio_default_test_loop_scope` first ships (rule 9).

At a workspace root the tables are written once; what a root changes in them is `python-workspace`'s.
A library, and a service that runs a single process, remove the `main` stub and script `uv init`
generates; a CLI tool declares one console script naming its app (`python-cli`), and a service with
several processes one per process, in `[project.scripts]`.

`E` and `F` are the error and pyflakes families, `I` import sorting; `B904` is raise-without-from and
`B006` the mutable default argument; `F403` and `F405` are the two wildcard-import warnings. `C901` is
cyclomatic complexity; `PLR0911`, `PLR0912`, `PLR0913`, `PLR0915` and `PLR0917` are too many returns,
branches, arguments, statements and positional arguments.

Ruff runs with no paths, so it covers every Python file in the tree, `migrations/` included; mypy is
given `src` and `tests` and stops there. `tests/` is not a package, so a `conftest.py` at two levels
would be two modules with one name — `explicit_package_bases` with `src` and the tree root on
`mypy_path` makes mypy derive each module's name from its path instead.

The pydantic plugin is not optional where pydantic is used: without it strict mode reports every
no-argument settings construction — `QuxSettings()` — as a call missing its required fields. A third-party
package the project depends on that ships no stubs and no `py.typed` marker adds one block, dev dependencies
included when the suite imports them:

```toml
[[tool.mypy.overrides]]
module = ["<package>", "<package>.*"]
ignore_missing_imports = true
```

**The line length.** `120` is the width this catalogue's templates are written to; `88` is the
formatter's default, which every tool and shared config already agrees on. On an empty tree nothing
needs reformatting, and the wider limit spares signatures and single-line comments from being cut
instead of wrapped; on an established tree the reformat is real, which argues for the number already
there. Either is compliant once written; the setting drives the formatter as well as the lint rule.

## Other bindings

- **Another package manager or build backend.** poetry or pdm replace the commands and the lock file;
  `uv_build` or setuptools replace hatchling. The src layout, names-only dependencies with floors only
  at a named break, and a development group installed by default — PEP 735 `[dependency-groups]`, or the
  tool's own table where it reads no other, never a deprecated one — are unchanged.
- **Another linter or type checker.** flake8 with its plugins, or pyright in strict mode: the rule codes
  and keys change; the parity of `src` and `tests`, the narrow selection that still refuses an unchained
  `raise` in `except` and a mutable default, every size and complexity threshold written down, one
  written line length and the closed list of suppressions do not.

## Rules

1. **The src layout, from the first commit.** The package lives under `src/<package>/`, tests under
   `tests/` beside it, for a service, a CLI tool and a library alike. A single-module or flat tree has
   to be moved before the second module, and the import path it tests is not the one an installed
   distribution has.
2. **One configuration, in `pyproject.toml`, and lint and type-check hold `src` and `tests` at
   parity**, so a defect never hides in whichever surface the other skips. Lint also covers any tree
   outside both, migrations included; the type checker stops at `src` and `tests`. What keeps `tests`
   green under strict checking is `python-style`'s full annotation coverage.
3. **The correctness selection is narrow**: the error and pyflakes families, import sorting, and two
   bugbear rules — a `raise` inside `except` that neither chains the cause nor says `from None`, and a
   mutable default argument — not the whole bugbear family.
4. **Function size and complexity are bounded by the linter, with every threshold written down.**
   Cyclomatic complexity stops at 10, McCabe's own published ceiling; branches at 12, return statements
   at 6 and statements at 50, pylint's long-standing defaults. Arguments are capped twice: positional
   ones at 5, and all of them at 7, because a keyword-only argument names itself at every call site. The
   numbers are written even where they equal the tool's default, because an unwritten threshold moves
   when the tool's default does. No bound is dropped from the selection or raised, and a function that
   trips one is split, never suppressed.
5. **A lint suppression is sanctioned only where a skill names it.** One is sanctioned everywhere — the
   wildcard ignore on `__init__.py` (`python-packaging`). Where a family's migration bootstrap is laid,
   its setup skill sanctions at most two more — for generated revisions and for registration-only
   imports — and names them. No other `noqa`, inline or per file, in `src`, `tests` or anywhere else.
6. **Type checking is strict, with the validation library's plugin where the project uses one that
   ships it.** A third-party package with no type information gets one per-package override in the configuration;
   every other type suppression follows `python-style`'s policy.
7. **The line length is written down once, in one file, and the number is the project's.** Settled at setup; a later
   change reformats the tree and travels as its own commit, never inside a feature change.
8. **The interpreter floor is written in the three settings `python-style` names, all naming one
   interpreter**, and its value is `python-style`'s — for a deployable and for a distributed package
   alike.
9. **Dependencies are declared by name; a version floor marks a known break and says which.** The lock
   file is the only home for a pin. A floor sits at the release where an API the code relies on arrived
   or changed, with that API named beside it — never at a version remembered as recent, which is a
   guess dressed as a constraint — and a floor whose API the code no longer calls is removed with it.
   **A distributed package's floors are its consumers' contract**: they bound what every consumer's
   resolver may choose, so they sit at the oldest release that works and never pin exactly, and raising
   one is a change consumers see, released under `python-versioning`.
10. **Dependencies are grouped by role.** What the running code imports is a runtime dependency and
    arrives with the code that imports it; what only developing it needs — the test runner, the linter,
    the type checker — goes in the group the package manager installs by default, never a deprecated
    tool-specific table. A distributed package's optional integration is an extra its consumers opt
    into, not a runtime dependency all of them install. A package nothing imports is removed.
11. **The test runner's configuration is one block in the same file.** It lets two test modules share
    a basename in different directories, lets a test import shared test support by package rather than
    by path, resolving to its own distribution's tree (in a workspace, `python-workspace` rule 10), and holds what `test-principles` requires of
    the run — a warning failing it; where the suite has async tests, async-ness declared once; and where
    it holds a session-scoped async resource, one session loop.
12. **A version written by hand is read from its source when it is written, never recalled.** A
    remembered version is the one current when it was learned — often years old and out of support. A
    dependency's version is the package manager's to write, into the lock file. What a floor names is
    chosen by its own rule — the interpreter's by `python-style`, a dependency's by rule 9 — and this
    distribution's own version by `python-versioning`; this rule asks only that the release they name
    be confirmed in its changelog. Every other version — a container image tag, a CI action, a hook
    revision, the interpreter an image or a job installs — is chosen for its reason: the line the
    project already runs where it runs one, the floor where a job exists to test it, otherwise the
    newest supported release; its exact spelling is read from the registry or release page that
    publishes it, at the precision the project pins. Where a source cannot be read, the version is
    written and reported to whoever asked as unverified — never presented as current, and never marked
    in the file. A version in an example, this catalogue's included, says nothing about what is
    current.

## Hard stops

- Asked which runtime libraries a service needs → stop, that is its roles', under the family's setup
  skill (`flat-project-setup`, in `pyhouse-flat`, or `hex-project-setup`, in `pyhouse-hex`); this skill
  says only how they are declared.
- Asked for the interpreter floor's value, or whether an inline type-ignore or a `cast` is allowed →
  stop, use `python-style`.
- Asked what version this distribution declares → stop, use `python-versioning`.
- Laying the root of a repository holding several distributions → stop, use `python-workspace`; the
  values it writes there are still this skill's.
