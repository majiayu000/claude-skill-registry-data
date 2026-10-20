---
name: iru-python-coverage
description: >-
  Run a Python project's container-free pytest suite (FastAPI, Django with pytest-django, or a plain library) with coverage.py via pytest-cov — falling back to `coverage run -m pytest` + `coverage xml` when pytest-cov isn't installed — through whichever environment runner the project uses (`uv run --frozen`, `poetry run`, `pdm run`, `pipenv run`, `.venv/bin/python -m`, plain `python -m`), write a Cobertura report to `build/coverage/coverage.xml`, and read it with a small stdlib Python parser to report the exact line % and branch % (plus coverage.py's combined figure, the one `fail_under` compares) for the total and per file, with uncovered line ranges and partial branches for files under the bar. Only container-free tests count toward the gate — the `integration` marker (or `tests/integration/` directory) is always deselected, so the number is reproducible without Docker; integration coverage is measured only on explicit request and labeled as not the gate value. Honors the project's `[tool.coverage.run] source`/`omit`/`branch`, adds `--cov-branch`, neutralizes `fail_under` during the run (`--cov-fail-under=0`) so the skill compares against the requested bar itself, and reports "coverage not wired" instead of a false 0%. Invoke as `/iru-python-coverage [selector] [targets]` — `[selector]` uses `iru-python-test`'s syntax (paths, node ids, `-k "<expr>"`), `[targets]` is a comma-separated list of source files, directories, or dotted modules to report on (e.g. `app/services/books.py,apps.catalog`) — or `/iru-python-coverage` with no argument for whole-project coverage; a `bar: <N>` line sets the threshold (default 80). Use whenever the user (or a `iru-fastapi-*`/`iru-django-*` group skill via `iru-gate-runner`) wants to check, or verify a bar for, a Python file, package, or the whole project, instead of eyeballing `--cov-report=term-missing` output.
model: haiku
allowed-tools: Read Bash(uv *) Bash(poetry *) Bash(pdm *) Bash(pipenv *) Bash(.venv/bin/*) Bash(python *) Bash(python3 *) Bash(DJANGO_SETTINGS_MODULE=* *) Bash(command -v *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(test *) Bash(mkdir -p build*) Bash(rm -f build/coverage/*) Bash(rm -f .coverage*)
---

# Python Coverage

Run the project's fast (container-free) pytest suite with coverage.py enabled and report the exact, measured line and
branch coverage for the files the user cares about, read from a Cobertura XML report. This skill only measures and
reports coverage — it does not add tests, modify source/test code, or change coverage configuration unless asked to
as a follow-up.

## Step 1 — Determine scope, runner, and test selection

- **Selector** (optional): paths, node ids, and `-k "<expr>"` with exactly `iru-python-test`'s Step 0 syntax. No
  selector → the whole fast suite.
- **Targets** (optional): a comma-separated list of source files (`app/services/books.py`), directories/packages
  (`apps/catalog/`), or dotted modules (`apps.catalog.services` → `apps/catalog/services.py` or
  `apps/catalog/services/`). Without targets, infer them from the selector by convention — `tests/test_books.py` /
  `tests/services/test_books.py` → the source file named `books.py` under the measured source;
  `apps/catalog/tests/test_views.py` → `apps/catalog/views.py`; a directory or `-k` selector can't be inferred, so
  report every file the report lists (or ask which ones matter if there are many unrelated ones).
- **`bar: <N>`** (optional line) — the threshold to judge against; default **80** (this catalog's group gate). The
  project's own `[tool.coverage.report] fail_under` (the author's docs use 90) is reported alongside, not used as the
  gate.

Detect the **environment runner** and the pytest wiring (pytest-django settings, async plugins, xdist) exactly as
`iru-python-test` Steps 1–2 do, and the **integration split** exactly as its Step 3 does. The gate run always
deselects the integration selection (`-m "not integration"`, or `--ignore=<tests/integration dir>`, plus any other
heavyweight marker the project excludes from its everyday run such as Django's `browser`): container-backed tests
need Docker, and a gate number that depends on them can't be reproduced without it. If the project has no split and
the suite is container-backed (testcontainers imported by unmarked tests), say the gate number depends on Docker.

Same caveat as `iru-java-coverage`: coverage is only recorded for code the selected tests execute. A narrow selector
undercounts a module that other test files also exercise — when in doubt, prefer a broader selector (the containing
directory, the whole fast suite) and say which tests ran.

## Step 2 — Check that coverage is wired (never trust a 0% without this)

```bash
<prefix> python -c "import importlib.util as u; print({n: bool(u.find_spec(n)) for n in ('pytest_cov', 'coverage')})"
```

- **pytest-cov installed** → Step 3's primary command.
- **only `coverage` installed** → Step 3's fallback (`coverage run -m pytest`).
- **neither** → **stop and report "coverage not wired — add `pytest-cov` to the dev dependency group"**. Never
  pass `--cov` blindly: without pytest-cov pytest exits `4` with `unrecognized arguments: --cov`, which is a wiring
  problem, not 0%.

Read the coverage configuration (`[tool.coverage.*]` in `pyproject.toml`, else `.coveragerc`, `setup.cfg`
`[coverage:*]`, `tox.ini` `[coverage:*]`):

- **`[tool.coverage.run] source`/`source_pkgs`** decides what is measured. With it, files no test imported still
  appear at 0% (verified). Without it, bare `--cov` measures every imported file **including the tests themselves**
  (verified: `tests/test_calc.py` showed up in the report) and silently omits never-imported modules — so pass
  `--cov=<pkg>` per top-level source package instead: `src/<pkg>` (src layout), `app` (FastAPI layout), `apps` +
  `config` (Django layout), or the packages listed in `[tool.setuptools.packages]`/`[tool.hatch.build]`. Say which.
- **`omit`** — the scaffold contract omits migrations, `asgi.py`, `wsgi.py`, `manage.py`, settings, and tests; keep
  the project's list, never extend it to make a number pass. If it doesn't omit Django `*/migrations/*`, say the
  number includes them.
- **`branch`** — pass `--cov-branch` regardless; it only adds branch data (verified: without it and with
  `branch = false` the report's branch figures are `0/0`).
- **`fail_under`** — pytest-cov applies it to the run's exit code (verified: `FAIL Required test coverage of 80.0% not
  reached`, exit `1` even when every test passed). Pass `--cov-fail-under=0` so the exit code reflects only the tests;
  this skill judges the bar itself from the XML.
- **`concurrency`** — when the project uses async SQLAlchemy/SQLModel (`AsyncSession`, `create_async_engine`, the
  `sqlalchemy[asyncio]` extra), code run inside greenlets is invisible to the default tracer unless
  `[tool.coverage.run] concurrency = ["greenlet", "thread"]` is set (verified while writing
  `iru-fastapi-code-one-task-group`: 69% reported for code that was 100% exercised). If it's missing, don't edit the
  config yourself — report the number as **under-reported** and recommend adding that line.

## Step 3 — Run the coverage build

Delete stale data first, then write the report to the canonical path (the one `sonar.python.coverage.reportPaths`
and CI use):

```bash
rm -f build/coverage/coverage.xml .coverage && mkdir -p build/coverage build/test-results

# pytest-cov (primary)
<pytest> -m "not integration" [selector] --cov [--cov=<pkg> ...] --cov-branch \
  --cov-report=xml:build/coverage/coverage.xml --cov-fail-under=0 \
  -p no:cacheprovider --junitxml=build/test-results/pytest.xml

# coverage.py only (fallback)
<prefix> coverage run --branch [--source=<pkg>,...] -m pytest -m "not integration" [selector] -p no:cacheprovider \
  --junitxml=build/test-results/pytest.xml
<prefix> coverage xml -o build/coverage/coverage.xml --fail-under=0
```

(`<pytest>` / `<prefix>` as resolved in `iru-python-test` Step 1; with the `.venv/bin/python -m` prefix the fallback
is `.venv/bin/python -m coverage run …`.) Notes:

- If the project's `addopts` already contains `--cov=…`/`--cov-report=…`, the explicit flags add to them — the XML
  path above is still written. `--cov-report=term-missing` is optional for a human reading the console; this skill
  reads only the XML.
- pytest-cov combines pytest-xdist workers itself; leave the project's `-n` setting alone.
- **Test failures**: the XML is still written after failing tests — report the coverage but say it comes from a
  failing run (and list the failures via the JUnit log, parsed as in `iru-python-test` Step 5). A collection error
  (exit `2`) or usage error (exit `4`) writes **no** report (verified) — report that cause, and never read a stale file.
- **Integration coverage** only when the user explicitly asks (`integration`/`all` keyword): run it through
  `iru-python-test`'s Step 4 (Docker check + `.integration-test.lock`, `lock: held` honored) with
  `--cov-report=xml:build/coverage/coverage-integration.xml`, and report it separately, labeled "includes
  container-backed tests — not the gate value".

## Step 4 — Read the exact coverage from the Cobertura XML

Shape written by coverage.py 7.x (verified):

```xml
<coverage lines-valid="12" lines-covered="7" line-rate="0.5833" branches-valid="6" branches-covered="2" branch-rate="0.3333" ...>
  <sources><source>/abs/project/app</source></sources>          <!-- one <source> per measured root (Django: apps, config) -->
  <packages><package name="." ...><classes>
    <class name="calc.py" filename="calc.py" line-rate="0.5833" branch-rate="0.3333">  <!-- filename is relative to a <source> -->
      <lines>
        <line number="13" hits="1" branch="true" condition-coverage="50% (1/2)" missing-branches="14"/>
        <line number="14" hits="0"/>
```

Line % = `lines-covered / lines-valid`; branch % = `branches-covered / branches-valid`; coverage.py's own total (its
`TOTAL` row and what `fail_under` compares) is the **combined** `(lines-covered + branches-covered) / (lines-valid +
branches-valid)` — they differ whenever branches are measured (verified: 58.33% lines, 33.33% branches, 50.00%
combined). Parse with the project's interpreter, passing targets as the optional second argument:

```bash
<prefix> python - build/coverage/coverage.xml 'app/services/books.py,apps/catalog/' <<'PY'
import os
import sys
import xml.etree.ElementTree as ET

root = ET.parse(sys.argv[1]).getroot()
want = [w for w in (sys.argv[2] if len(sys.argv) > 2 else "").split(",") if w]
sources = [s.text or "" for s in root.iter("source")]
cwd = os.path.realpath(os.getcwd())


def pct(covered, valid):
    return f"{100 * covered / valid:.2f}%" if valid else "n/a"


def rel(filename):
    for src in sources:  # filenames are relative to one of the <source> roots
        path = os.path.realpath(os.path.join(src, filename))
        if os.path.exists(path):
            return os.path.relpath(path, cwd)
    return filename


def ranges(nums):
    out = []
    for n in sorted(nums):
        if out and n == out[-1][1] + 1:
            out[-1][1] = n
        else:
            out.append([n, n])
    return ", ".join(str(a) if a == b else f"{a}-{b}" for a, b in out)


lv, lc = int(root.get("lines-valid", 0)), int(root.get("lines-covered", 0))
bv, bc = int(root.get("branches-valid", 0)), int(root.get("branches-covered", 0))
print(f"TOTAL lines {lc}/{lv} ({pct(lc, lv)}) branches {bc}/{bv} ({pct(bc, bv)})"
      f" combined {pct(lc + bc, lv + bv)}")  # combined = coverage.py's own "TOTAL"/fail_under figure
for cls in root.iter("class"):
    path = rel(cls.get("filename"))
    if want and not any(path == w or path.endswith("/" + w) or path.startswith(w.rstrip("/") + "/") for w in want):
        continue
    lines = cls.find("lines")
    lines = [] if lines is None else lines.findall("line")
    fl = len(lines)
    fc = sum(1 for ln in lines if int(ln.get("hits", 0)) > 0)
    fbv = fbc = 0
    for ln in lines:
        cc = ln.get("condition-coverage")  # e.g. "50% (1/2)"
        if ln.get("branch") == "true" and cc:
            c, v = cc.split("(")[1].rstrip(")").split("/")
            fbc, fbv = fbc + int(c), fbv + int(v)
    miss = [int(ln.get("number")) for ln in lines if int(ln.get("hits", 0)) == 0]
    part = [f"{ln.get('number')}->{ln.get('missing-branches')}" for ln in lines if ln.get("missing-branches")]
    print(f"{path} lines {fc}/{fl} ({pct(fc, fl)}) branches {fbc}/{fbv} ({pct(fbc, fbv)})"
          + (f" uncovered: {ranges(miss)}" if miss else "")
          + (f" partial: {', '.join(part)}" if part else ""))
PY
```

Convert dotted-module targets to paths before passing them: `apps.catalog.services` → `apps/catalog/services.py`
when that file exists, else the package directory `apps/catalog/services/` (prefix rule; with a src layout prepend
`src/`). Matching is by project-relative path suffix/prefix, never substring, so `book.py`
doesn't match `notebook.py`.

**Ambiguous filenames with several `<source>` roots**: Cobertura stores each filename relative to its root, so two
files with the same relative name under different roots (e.g. `apps/__init__.py` and `config/__init__.py`) collapse
into one `<class>` entry (verified; harmless for empty `__init__.py` files — the XML totals still count every file).
When a target resolves under more than one root, read that file's exact figures from the `.coverage` data file
instead: `<prefix> coverage report --include='<path>' --show-missing --fail-under=0` (verified; its `Cover` column is
the combined figure).

A target that doesn't appear in the report at all is outside `source`, matched by `omit`, or (with no `source`
configured) never imported by any selected test — report that explicitly rather than a false 0%. A target that
appears with `lines 0/N` genuinely is 0%. A file with `0/0` lines (empty `__init__.py`, a pure re-export) is `n/a`,
not 0%.

Leave `build/coverage/coverage.xml` in place when `build/` is gitignored (CI and Sonar read it); otherwise delete
it and `.coverage` after parsing.

## Step 5 — Report results

State the runner, how coverage was collected (pytest-cov or `coverage run`), the measured roots (`source` or the
`--cov=` packages chosen), the test selection (and what was deselected — integration, `browser`), and whether the
tests passed. Then, computed from the actual XML numbers — never estimated:

- **Total**: line %, branch %, and coverage.py's combined %, and whether the **line %** meets the bar (the gate
  figure, the same metric the other stacks' gates use); mention the combined figure against the project's own
  `fail_under` when it differs.
- **Per target** (or per file, for an unscoped run with few files): line % and branch %, and for every target under
  the bar the uncovered line ranges and partial branches (`app/services/books.py: lines 75.00%, branches 50.00% —
  uncovered: 41-43, 57; partial: 39->41`) so the user, or a follow-up coding step, knows where to add tests.

Never paste the XML or the console table. If coverage wasn't wired, the run died before writing a report, or a
target fell outside the measured source, report that instead of a percentage, with the exact command and the fix.
Do not add tests, modify source/test code, edit coverage configuration, or re-run to raise the number — that's a
follow-up the user (or a coding skill) drives explicitly.

## Verification notes

Verified with uv 0.12.8, CPython 3.13, pytest 9.1.1, pytest-cov 7.1.0, coverage.py 7.16.2, Django 6.1.2 +
pytest-django 4.14.0, in `$TMPDIR/iru-verify/python/gates/{lib,dj}` (outside this repository):

- The pytest-cov command above wrote `build/coverage/coverage.xml`; the parser reported `TOTAL lines 7/12 (58.33%)
  branches 2/6 (33.33%) combined 50.00%` — the combined figure matched coverage.py's own `TOTAL 50%` row — and
  `app/calc.py … uncovered: 14, 16, 41-43 partial: 13->14, 15->16, 41->42,43`; target filtering by file and by
  directory worked. A never-imported module appeared at `0/2` with `source` configured.
- Without `--cov-fail-under=0`, `fail_under = 80` made the run exit `1` with `FAIL Required test coverage of 80.0% not
  reached`; with it, a green run exited `0`. Without `source`, bare `--cov` measured `tests/` too; `--cov=app`
  restored the right scope. `branch = false` without `--cov-branch` gave `branches 0/0 (n/a)`.
- The `coverage run --branch -m pytest …` + `coverage xml -o … --fail-under=0` fallback produced an identical report.
- Django layout (`source = ["apps", "config"]`, two `<source>` roots, `relative_files` on or off): files mapped back
  to `apps/books/models.py` / `config/urls.py` correctly; the two empty `__init__.py` files collapsed into one entry,
  and `coverage report --include=apps/books/models.py --show-missing --fail-under=0` gave the exact per-file figure.
  A collection error (exit `2`) wrote no XML at all.
- Still unverified: the Poetry, PDM and Pipenv prefixes, pytest-xdist workers with `--cov`, `source_pkgs`, and
  `.coveragerc`/`setup.cfg`-only configurations.

## Sources

- irurueta docs: backend/fastapi/testing.adoc (pytest-cov, `[tool.coverage.run] source/branch`,
  `[tool.coverage.report] show_missing/fail_under`, `exclude_also`, threshold as a ratcheting floor)
- irurueta docs: web/django/pytest-factories-and-browser-tests.adoc (`source = [<apps>, "config"]`, `omit` for
  migrations/tests/asgi/wsgi, `--cov-report=xml` for Sonar/Codecov, xdist handled by pytest-cov)
- irurueta docs: programming-languages/python/testing.adoc (pytest selection syntax shared with `iru-python-test`)
