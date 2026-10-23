---
name: new-analyzer
description: Scaffold a new AWS service analyzer - src/aws_analyzer/<service>.py with the five-section layout, the shared helpers imported from _kit and its Analyzer and View built on _kit's base classes, a first set of useful commands, moto tests, a README section, a docs guide page and a line on the home page. Use when starting a new service; bedrock_kb.py (Bedrock Knowledge Bases) is the latest one built this way.
argument-hint: "<module name, e.g. sagemaker> [what users should be able to see first]"
---

# New analyzer

Request: `$ARGUMENTS`. The first word is the module name (snake_case, and a valid Python identifier, because
users will `import` it). The rest, if given, says what users need from it.

A new analyzer is a new module of the package with the same shape as `src/aws_analyzer/s3.py` and
`src/aws_analyzer/dynamodb.py`.
Read CLAUDE.md's "Hard constraints" and "Architecture of an analyzer file" first. Everything below follows them.
`dynamodb.py` is the smallest analyzer, so model the new one on it; `bedrock_kb.py` and its tests show how to test a service moto doesn't cover (botocore `Stubber` on injected clients).

## 1. Research the service (before writing code)

- **Clients and read-only operations.** List the operations of each boto3 client the analyzer will use. For
  Knowledge Bases these are `bedrock-agent` (configuration) and `bedrock-agent-runtime` (retrieval):

  ```bash
  .venv/bin/python -c "import botocore.session as s; m = s.get_session().get_service_model('bedrock-agent'); print(sorted(m.operation_names))"
  ```

  Only Get / List / Describe / Head / Search / Retrieve style calls. Nothing that writes, starts a job or ingests
  data.
- **moto support.** Look for the client in
  `.venv/bin/python -c "from moto.backend_index import backend_url_patterns as b; print([n for n, _ in b])"`.
  Where moto doesn't cover a client or an operation, the tests use `botocore.stub.Stubber` or
  `monkeypatch` instead. Say which in the plan.
- **Costs.** Work out what the service bills that users would want estimated. That becomes a
  `<SERVICE>_PRICES` table of us-east-1 list prices, and callers can override it with `prices=`.
- **IAM.** List the permission each operation needs.

## 2. Agree on the first commands

Propose three to five View commands and confirm them with the user before building. The one-argument call of
the first command has to be useful. A typical set:

- an overview of everything in the region, with the warnings, like `tables()` / `overview()`
- a detail report for one resource, with findings and the call to copy for the next step, like `table_info()` /
  `bucket_info()`
- one or two commands that look at the data itself (for Knowledge Bases: data sources and sync status, and a
  test retrieval that shows the chunks returned with their scores and sources)

For each command, give its name, what the user decides from it, its cards, and its findings.

## 3. Create `src/aws_analyzer/<service>.py`

Pick the names first:

- the classes: `<Service>Analyzer` / `<Service>View` (for example `BedrockKBAnalyzer` / `BedrockKBView`)
- a short CSS root class, the file's `_ROOT` (taken: `s3a`, `ddb`, `kba`, `kbc`, `smk`, `osv`, `lmb`)
- the price table: `<SERVICE>_PRICES`

Then build the file:

1. **Module docstring.** Same shape as the others: what it is, "Part of aws-analyzer: ``pip install
   aws-analyzer``, then ``from aws_analyzer import <Service>View``", the requirements, the two layers, and a quick
   start that shows the commands.
2. **Imports.** `from __future__ import annotations`, then only the stdlib, `boto3`, `botocore` and the package's
   own `_kit` at the top (never another analyzer). Anything optional is imported inside functions through
   `_require`.
3. **The five banners**, exactly in this form: `# 1. Helpers: ...`, `# 2. Data models (what <Service>Analyzer
   returns)`, `# 3. Pure analysis (no AWS calls - ...)`, `# 4. <Service>Analyzer - pure logic layer ...`,
   `# 5. <Service>View - notebook UI layer ...`, each between `# ===...` lines.
4. **Shared helpers.** Import what's in `src/aws_analyzer/_kit/` (`human_size`, `_plural`, `_require`, `_esc`,
   `_why`, `_Hint`, the render blocks `_Title`, `_Cards`, `_Table`, ... and `_call`, `_signature`, `_render_text`,
   `_report_html`, `_base_css`, ...) the way `dynamodb.py` does, only the names the file uses: never copy them,
   `rules.py` fails on a copy. At the start of section 5, set the service's look the way `dynamodb.py` does:
   `_ROOT`, `_CSS = _base_css(_ROOT)` (or `_base_css(_ROOT, _EXTRA_CSS)` with the rules for its own blocks, each
   starting with `.<root>`), `_BADGE`, and `_render_html(blocks, max_rows)` calling `_report_html` with the three.
   A block type of its own registers how it's drawn with `@_draws(_Block, "html")` and `@_draws(_Block, "text")`
   (CLAUDE.md, "How the View layer works"). Nothing else is copied: the analyzer and the View get the rest from
   their base classes (steps 5 and 6).
5. **The analyzer.** Subclass `_BaseAnalyzer` (`from ._kit.analyzer import _BaseAnalyzer`) and set
   `_LIST_PRICES = <SERVICE>_PRICES`. The constructor matches the others:
   `(session=None, *, region=None, profile=None, client=None, prices=None)`, and starts with
   `super().__init__(session, region=region, profile=profile, prices=prices)`, which sets `self.session`, the
   clients' retry settings `self._config` and `self.prices`. Clients are made lazily, each with the service name
   spelled out (`self.session.client("<service>", config=self._config)`, so `rules.py` sees its calls), and a
   missing region turns into a readable `ValueError` (see `DynamoDBAnalyzer.client`). The base's `region`,
   `_paginate`, `_map` (set `self.max_workers`) and `_cached_client` (set `self._clients` and `self._lock`) are
   there to use. Record config sections the caller can't read in `errors`. Long reads take `limit=` and
   `progress=`.
6. **The View.** Subclass `_BaseView` (`from ._kit.view import _BaseView, _friendly_errors`):
   `__init__(core=None, *, mode="auto", max_rows=50, progress="auto")` calls
   `super().__init__(mode=mode, max_rows=max_rows, progress=progress)` and then sets
   `self.core: <Service>Analyzer = core or <Service>Analyzer()`. The class sets
   `_render_html = staticmethod(_render_html)`, `_GROUPS` (commands by task, for help()) and `_START` (the first
   two or three calls to try); `_show`, `_progress`, `help()` and `_price_basis` come from the base. Every command
   is decorated with `@_friendly_errors`, and its docstring's first paragraph is its help() text. Give the View an
   `_explain(code, message)` that says what the service's common AWS errors mean and what to do (a not-found names
   the command that lists what exists; see `LambdaView._explain`). Set the file's `_BADGE` (the chip before each
   report title) and CSS root class.

Build each command the way `/add-command` does: the data model, then the pure function and its findings, then
the analyzer method, then the View method.

A window to click through (an explorer, like `KBExplorer` or `LambdaExplorer`) comes later, if at all, and is built
on `src/aws_analyzer/_kit/window.py` (CLAUDE.md, "The windows' kit"): subclass `_Explorer` (call its `__init__`
first, set `_PREFIX`, `_THREADS` and `_reword`, build with `_tab_bar` and `_frame`, read AWS with `_later`), make its
fields `_Picker`s and its lines `_row_button`s, and guard its commands with `@_window_errors`. Take what it shares
with the other windows from there, never from another window's file.

## 4. Tests: `tests/test_<service>.py`

Use the same layout as `tests/test_dynamodb.py`: `# ---- helpers` (pure functions), `# ---- AWS (moto)` with
an `aws` fixture around `mock_aws()` plus seeded fixtures, and `# ---- UI` with `ui` in `mode="text"` and the
`run(capsys, fn, ...)` helper. Cover at least one failure path that shows a note instead of a traceback.

`tests/conftest.py` already puts `src/` on `sys.path` (tests import `from aws_analyzer import <service>`) and sets
fake credentials. If moto supports the
service, add its extra to the `moto[...]` line in `requirements-dev.txt` and `pip install -r
requirements-dev.txt`.

CI needs no changes: it lints, imports and tests every `src/aws_analyzer/*.py`. Check that the loop in
`.github/workflows/ci.yml` still globs.

The PyPI package ships every module in `src/aws_analyzer/`; wire the new one into `src/aws_analyzer/__init__.py`:
its name in `_MODULES` (`tests/test_package.py` fails without it), and the Analyzer and View classes in `__all__`,
`_EXPORTS` and the `TYPE_CHECKING` imports. If the service's API is newer than the `boto3>=` floor in `pyproject.toml`, raise the floor
to the first boto3 release that has every operation the file calls, and put any new optional package in an extra.

## 5. Docs

- `README.md`:
  - Add a row to the "Services" table (what it shows you, the file and its guide) and a link to the new section
    in the links under the title.
  - Add a `## <Service>` section with the same parts as the DynamoDB one: a one-line intro with the file and guide,
    a screenshot, quick start, the commands tables (one per `_GROUPS` group), and under "Reference" the folded
    "Getting the data", cost notes, and IAM permissions.
  - Update the Development paragraph if it names the guides.
- `docs/<service>.md`: a new guide. Copy `docs/dynamodb.md`'s structure (front matter, hero, headings with
  explicit ids, figures, callouts, troubleshooting entries, the `ref` command table), and cover set up in
  SageMaker, a five-minute tour, a section per area, using the data in Python, cost, permissions,
  troubleshooting and a command reference. Leave out screenshots you can't make yet (see `/demo --html`).
- `docs/images/aws/<service>.svg`: the service's 64 px icon from AWS's Architecture Icons package
  (https://aws.amazon.com/architecture/icons/), unchanged; the home page's line, the guide's eyebrow and README's Services table
  and section show it.
- `docs/index.md`: add a line for the new guide to the `.svc` list (its icon, name, module and two or three
  questions a data scientist would ask that it answers), and add the guide to `nav` in
  `mkdocs.yml`. Check it with `mkdocs build --strict` (`pip install -r requirements-docs.txt`).
- `CHANGELOG.md`: a bullet under `## [Unreleased]` → `### Added` naming the service, its file and View, and its
  first commands.
- `CLAUDE.md`: update the list of analyzers, the price tables, the moto extras (or the Stubber note, as for Bedrock)
  and anything service-specific a future session needs.

## 6. Demo data and verification

1. Add `seed_<service>()` and an entry in `SEEDERS` in `.claude/skills/demo/demo.py`, if moto supports the
   service.
2. Run `/check`. `rules.py` must report 0 errors, and every IAM warning is fixed in the README.
3. Run `/demo <service>` on each command and read the output against the product rules.

Report the files created, the commands with their help() lines, a demo excerpt, the IAM permissions, and what
is still missing (screenshots, commands left for later). Don't commit unless asked.
