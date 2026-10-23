---
name: modularize
description: Turn one service module (lambda_functions.py, s3.py, ...) into a package of small modules - core (models, analysis, analyzer) that every front-end shares, and front-ends (report blocks, View, explorer window) on top - without changing anything a user sees. Holds the plan, the target layout per service, the rules the split must keep, the step-by-step recipe and the progress table. Use for "/modularize lambda_functions", for the tooling step ("/modularize tooling"), or before touching code in a service that is half-way through the split.
argument-hint: "<service | tooling | status>"
---

# Modularize: one service, one package

Request: `$ARGUMENTS`. A service name (`lambda_functions`, `s3`, `_bedrock`, ...) means: do that service's step,
following the recipe below. `tooling` means Phase 0. `status` means: read the progress table, check it against the
tree (`ls src/aws_analyzer/`), and say what's next.

Read CLAUDE.md first. Everything there still holds, and this plan doesn't relax any of it, except where it says so
explicitly (the per-file lists in "Config files that are keyed by file").

## Why

Each service is one file with five `# ====` sections, and four of them are 8,500 to 12,000 lines. They grow with
every command, window tab and agent tool. Nobody (human or agent) can hold such a file in their head, and the parts
used by different consumers are mixed together.

The library has one core and several front-ends:

```
                 ┌──────────── core (per service) ─────────────┐
                 │ helpers · models · analysis · analyzer       │
                 │ (parses, decides, talks to AWS, returns data)│
                 └──────▲───────────────▲───────────────▲───────┘
                        │               │               │
           View (reports)    explorer / window (widgets)    agent toolkit (AI, in agent/)
                 └──── _kit's UI runtime ────┘                └── agent/'s runtime
```

The goal: **the core is written once and every front-end uses it its own way.** A front-end only reads the core.
The core never knows a front-end exists. That only holds if the code is laid out so it's visible and checked.

## The decisions (already made, don't reopen them in a step's PR)

1. **Each service becomes a package with the same layer names.** Every package uses the same names, so an agent who
   knows one service knows where things are in all of them. Small services stay flat; big ones get sub-packages
   where they grow.
2. **The public import path doesn't change.** `from aws_analyzer.lambda_functions import parse_function, LambdaView`
   keeps working: the package's `__init__.py` re-exports every public name. Submodule paths
   (`aws_analyzer.lambda_functions.analysis.logs`) are internal and may move again.
3. **Moves only. No behaviour change.** A split step changes no output, no public name, no method or attribute of a
   public class. It doesn't fix bugs, rename things or clean up style on the way: moved code is pasted as it was,
   so `git diff --color-moved` shows it as moved and review is fast. Anything else goes in its own PR.
4. **A module stays under `MAX_MODULE_LINES` (1,500).** `tests/test_style.py` enforces it. The files that were
   already longer are listed in `LONG_FILES` until they're split.
5. **A class that's too big for one module is split into mixins by concern, in the same commit.** For example,
   `LambdaExplorer(_LogsTab, _CodeTab, ..., _Explorer)` or `S3View(_ListingCommands, _FileCommands, ..., _BaseView)`.
   Methods and attributes keep their names, so tests and users see the same class. Turning mixins into proper
   components later is a separate design change, not part of this plan.
6. **Agent toolkits stay in `agent/toolkits/`.** We considered moving each toolkit into its service's package and
   rejected it. A toolkit subclasses `agent.toolkits.base.Toolkit`, which needs the agent's `Budget`, and a tool
   can join two services (`s3_triggers` reads S3 and, through `peer("lambda")`, Lambda). Either would make a service
   import the agent or another service, which breaks "importing one analyzer loads no other". The agent is a
   cross-service front-end, and it keeps being the companion of the services it reads.
7. **The agent reads only the core's public API.** Today it reaches into private names
   (`LambdaAnalyzer._window`, `._numbers`, `S3Analyzer._cloudwatch_in`, `s3._rule_scope`, `s3._rule_actions`,
   `s3._exposure`, `s3._encryption_label`, `s3._block_label`). Each service's step makes the ones it owns public
   (a plain rename, all callers updated) as its first commit, because `__init__` only re-exports public names.
8. **`_kit` files don't move.** `rules.py` classifies them instead.
   - **Core-safe:** `fmt`, `text`, `errors`, `deps`, `analyzer`.
   - **UI:** `blocks`, `render`, `view`, `window`, `progress`, `highlight`, `jsontree`.
   - The one exception is `render._call` (and `_signature`). The core uses them to write calls into findings. They
     stay allowed until Phase 2 removes the need.

## Target layout of a service package

```
src/aws_analyzer/<service>/
  __init__.py      # module docstring (the old file's), public re-exports, __all__. Nothing else.
  helpers.py       # section 1: parsing and formatting
  models.py        # section 2: dataclasses
  analysis.py      # section 3: pure functions and *_findings  -> analysis/ package once over the limit
  analyzer.py      # section 4: <Service>Analyzer, the only module that makes AWS clients
  style.py         # _ROOT, _EXTRA_CSS, _CSS, _BADGE, _render_html: the service's look
  blocks.py        # the service's own render blocks and their @_draws drawers  -> blocks/ when big
  view.py          # <Service>View, its cell/row helpers  -> view/ with _<Topic>Commands mixins when big
  explorer/        # only if the service has a widget window: the window class, tabs as mixins, its CSS
```

Service-specific core modules go next to these, at the layer they belong to. Examples: `readers/` (S3's file parsers),
`http.py` (OpenSearch's signed REST client), `machine.py` / `envs.py` (SageMaker).

**Layers, lowest first.** A module imports only from its own layer or lower ones:

| Layer | Modules | May also import |
|---|---|---|
| core | helpers → models → analysis → analyzer (and the service-specific core modules) | stdlib, boto3/botocore, core-safe `_kit` (+ `render._call`), `_bedrock` for the Bedrock pair |
| UI | style → blocks → view → explorer | anything in core, every `_kit` module |

- `analysis` never imports `analyzer`. Pure functions make no AWS calls.
- `view` imports `explorer` only lazily, inside `explore()`, to avoid an import cycle.
- Optional packages still load lazily (`_require`), in every module.
- Every module starts with a docstring and `from __future__ import annotations`. The `# ====` section banners go
  away, since the module is the section now.
- Mixin naming, so `rules.py` can find them:
  - View command mixins: `_<Topic>Commands`.
  - Explorer tab mixins: `_<Topic>Tab`, and `_<Topic>Pane` for a window without tabs (S3's list and report panes).
  - Analyzer mixins: `_<Topic>Reads`.
  - The composed class lives in the module named for its layer (`view.py` or `view/__init__.py`, ...).

## Phase 0: tooling (done)

The guardrails used to assume one file per analyzer. Now they check packages, and every later step relies on them.
This is what they do, so you know what a failing check means. All of it was tried on a throwaway copy of the repo
where `dynamodb`, `s3` and `_bedrock` were packages, with a deliberate violation for each rule.

`.claude/skills/check/rules.py`:
- **The read-only check covers the whole package.** It finds the services an analyzer makes clients for across
  every module of its package (`owner_services`), plus its COMPANIONS parents', each a file or a package. So a
  module that calls `client.put_item` on a client another module made is still caught.
- **Parents and SHARED may be packages** (`module_files`, `top_modules`): `s3/` as the agent's parent, `_bedrock/`
  as the Bedrock pair's shared package.
- **Commands in mixins are checked.** In a package, every class named `*View`, `*Explorer`, `_*Commands` or `_*Tab`
  (`_ui_classes`) gets the command checks (`check_commands`): a guard (`@_friendly_errors` on a View or
  `_*Commands`, `@_window_errors` on an explorer or `_*Tab`), a docstring, `-> None`, and no
  `print` / `display` / `HTML`.
- **The layer rule** (`check_layers`). A core module that imports its package's `style` / `blocks` / `view` /
  `explorer` / `window`, or a UI module of `_kit` (except `render._call` / `_signature`), is an error, and so is
  `analysis*` importing `analyzer*`. The package's `__init__.py` is exempt, since it re-exports both layers.
- **No copies inside a package** (`check_package`). A function or class defined in two modules of one package is an
  error. Constants may share a name.
- **No reaching into private names** (`check_reach`). A companion package (`agent/`) touching a private name of
  an analyzer or of its module (`core._window`, `lf._x`, `s3._exposure`) is a warning. It found exactly the nine
  in decision 7. It becomes an error in "the leftovers".

`tests/test_style.py`:
- `MAX_MODULE_LINES = 1500` applies to every module under `src/aws_analyzer/` except those in `LONG_FILES`.
- `LONG_FILES` is the set of files that were longer than that before this plan. A file in it may still grow, since
  features keep landing in services that haven't been split yet.
- The second test fails once a listed file is gone or fits the limit, so its entry gets removed.

`.claude/skills/check/snapshot.py`:
- **What `names.json` records for a package:** `defined` is the names in its `__all__`, which is its promise to
  users. `inside` is every name its modules define.
- **How `compare` judges a missing name:**
  - a private name that left the top level but is in `inside` counts as `moved`, not `LOST`;
  - a public name missing from the top level is always `LOST`.

  No flag is needed.

`tests/test_package.py`: a `SHARED` module may be a package.

Found on the way and fixed:
- `agent/toolkits/s3_tools.py` had its own copy of `_lambda_module`. It now imports the one in `lambda_tools.py`.

## The recipe for one service

One PR per service, branch `modularize/<service>`, one commit per bullet so each can be checked on its own.
`.venv/bin/python` if it exists, else `python`; `$S` below is the service.

1. **Baseline**, from main, before changing anything. Save both outputs in the scratchpad, not the repo:

   ```bash
   python .claude/skills/check/snapshot.py run "$SCRATCH/base" --service $S
   python .claude/skills/check/rules.py --apis > "$SCRATCH/base-apis.txt"
   ```

2. **Make the private names the agent uses public** (decision 7), if this service owns any. Rename the name and
   update every caller: the module, `agent/`, tests, `demo.py` and `snapshot.py`'s cases. Nothing else changes.

3. **File becomes a package:** `git mv src/aws_analyzer/$S.py src/aws_analyzer/$S/__init__.py` (git keeps the
   history). Then:
   - Fix relative imports: `from ._kit` → `from .._kit`, and `from ._bedrock` → `from .._bedrock`.
   - Re-key the per-file config: `ruff.toml` per-file-ignores and `COMMENTS_LEFT`. Swap the path in `LONG_FILES`
     for `src/aws_analyzer/$S/__init__.py`, since it's still the long file until step 4 empties it.

   The full check must pass. This commit changes no line of code beyond those imports.

4. **Split it with `split.py`, in one commit.** Never retype code: retyping thousands of lines lets in mistakes that
   tests can miss.
   1. **Write the plan** in the scratchpad, `$SCRATCH/$S_plan.py`, the way `plans/opensearch.py` does:
      - `MODULES`: every top-level statement by name, in layer order;
      - `DOCS`: each module's docstring;
      - `REEXPORT_KIT`: the public `_kit` names the old module imported, which `__init__` keeps exporting.

      To list the statements, run `split.py` with an empty plan: it names the ones not placed. A name assigned twice
      at the top level is named with its line, `_SECRET_NAME_RE@1669`. In one file the last assignment wins for every
      function, so check what giving each half its own module changes before you place them. A bare expression
      statement (a drawer registered with `_draws(...)(...)`) is named by its line, `expr@4291`.
   2. **A class over the limit becomes mixins first** (decision 5), with `mixins.py`. Add `MIXINS` to the same plan:
      the class, then each mixin's name, docstring and members, in the order they go in its bases. Keep `__init__`
      and anything that calls `super()` on the class. An alias in the class body (`_preview_tsv = _preview_csv`) is
      a member named by its first name: put it in the mixin of the method it names, or the class can't be built. Then split its output instead of the file:

      ```bash
      python .claude/skills/modularize/mixins.py "$SCRATCH/$S.py" "$SCRATCH/$S_plan.py" "$SCRATCH/$S-mixed.py"
      ```

      The mixins are top-level classes now, so the plan places them like any other statement. Compare the sorted
      non-blank lines of the two files: only the mixins' headers and docstrings, and the class's new bases, should be
      new.
   3. **A lower layer that has to reach a higher one at run time** imports it inside the function, and that's the
      one line a split may add. It happens when the View opens the window (`from .explorer.window import
      LambdaExplorer` in `LambdaView.explore()`). Make the edit in the scratch copy before splitting, and say so in
      the commit. `split.py` doesn't ask for a top-level import of a name a function imports itself.
   4. **Split** the file as it was before step 3 (`git show HEAD~1:src/aws_analyzer/$S.py`), so its imports have
      their original depth, with the edits from 2 and 3 applied:

      ```bash
      python .claude/skills/modularize/split.py "$SCRATCH/$S.py" "$SCRATCH/$S_plan.py" "$SCRATCH/$S-out"
      ```

      It moves each statement verbatim with the comments above it, drops the `# ====` banners, writes each module's
      imports from the names it reads (relative ones for its own package), and stops if a module would read a name
      from a later one at run time. Fix that by reordering the plan, or by moving the statement next to what it
      reads: a dataclass whose property calls an analysis function belongs in that analysis module, not in
      `models.py`. Otherwise `models` and `analysis` would import each other. To see every such dependency at once,
      not one per run, loop over the plan with `split.py`'s `read_source`, `defined_names` and `used_names`.
   5. **Put the output in place** of `src/aws_analyzer/$S/`. Then remove the imports it wrote generously:
      `ruff check src/aws_analyzer/$S --select F401 --fix`.
   6. **Print the config entries** each module needs, and replace the one entry in `ruff.toml` and in
      `COMMENTS_LEFT` with them:

      ```bash
      python .claude/skills/modularize/split.py --report src/aws_analyzer/$S C901,PLR0912,PLR0913,PLR0915
      ```

      Use the old entry's rules. Then take `$S` off `LONG_FILES`.
   7. **Check:** `ruff check .`, `python .claude/skills/check/rules.py` and
      `python -m pytest tests/test_$S.py tests/test_package.py tests/test_style.py -k "not docstrings" -q`.

5. **Fix the tests and scripts that reached into the old file:**
   - `monkeypatch.setattr(lfmod, "_RUN_LINES", 6)` must now patch the module that *reads* the name
     (`from aws_analyzer.lambda_functions.explorer import logs as logs_tab`). Patching the package's re-export changes
     nothing, and the test then passes or fails for the wrong reason.
   - Private names a test imports come from their new module. Import the submodules under names that can't clash
     with a test's local variables (`stylemod`, `wiring_block`, `logs_tab`): ruff's F823 catches a local that
     shadows one.
   - A test that swaps a name by assignment (`lfmod.map_package = held_back`) swaps it on the module that looks it
     up, the same as a monkeypatch.
   - Do the same in `.claude/skills/demo/*.py` and in `snapshot.py`'s `DEMO_CASES`.

   Test files keep their names (`tests/test_$S.py`). Splitting them is a separate change.

6. **Prove nothing changed:**

   ```bash
   python .claude/skills/check/snapshot.py run "$SCRATCH/new" --service $S
   python .claude/skills/check/snapshot.py compare "$SCRATCH/base" "$SCRATCH/new"
   python .claude/skills/check/rules.py --apis | diff "$SCRATCH/base-apis.txt" -   # only paths may differ
   ```

   Every output must be identical, and no name `LOST`. Private names that moved into a module are reported as
   `moved`, which is fine. The snapshot's `apis.txt` differs only by the file it names
   (`<pkg>/$S.py` → `<pkg>/$S/analyzer.py`): check that by diffing it with the path swapped back. Any other
   difference is a bug in the move: find it, don't accept it.

7. **Docs for agents:**
   - Update CLAUDE.md where it names this service's file (`lambda_functions.py`'s `_EXPLORER_CSS`, ...) so a path
     search lands in the right module.
   - Update the progress table below.
   - No CHANGELOG entry: users see no change.

8. Run `/check` in full, then open the PR. The PR description says it's a move-only refactor, links this plan, and
   tells the reviewer to use `git diff main --color-moved=dimmed-zebra -M`.

### Config files that are keyed by file

These lists normally only shrink, and a new file is never added. A split is the one sanctioned exception, because the
same code just changes file:
- **`ruff.toml` per-file-ignores:** replace the service's one entry with one entry per new module, listing only the
  rules that module actually breaks. Run `ruff check <module> --select <the old entry's rules>` without the ignore
  to see which. Never a rule the old entry didn't have.
- **`COMMENTS_LEFT`:** one entry per new module, with its real count. The new counts must add up to no more than the
  old number. The `# ====` / `# 1. ...` banners aren't counted, so dropping them changes nothing.
- **`LONG_FILES`:** the old file's entry goes once the split is done, and no new module may be added to it.

## Per-service plans

Line counts are from 0.20.0. A class over 1,500 lines needs mixins. The exact grouping is the agent's call, made by
reading the code, but follow the topics below and the View's `_GROUPS`.

### `opensearch` (4,198 lines) — the pilot, done

It's small and has most of the layers, so it proves Phase 0's tooling and the recipe cheaply, and its PR stays easy
to review. It doesn't exercise mixins, an explorer window, the service's own blocks or the agent's private names.
`lambda_functions` comes next and proves those, so treat it as the second pilot. After each of the two, write what
went differently from this plan under "Lessons" at the end and fix the recipe, before the next service starts.

```
opensearch/
  __init__.py
  helpers.py         # section 1 (~400 lines): parse_location, endpoint_service, parse_engine_version,
                     #   version_at_least, vector_norm, vector_summary, values_at, _int, _bytes, ...
  models.py          # section 2 (~390): Domain, Collection, Endpoint, VectorField, IndexInfo, ClusterHealth,
                     #   KnnStats, StoreReport, VectorCheck, Sample, Embedding, Hit, SearchResult, Overview
  analysis/          # section 3 (~1,280): under the limit, but split by topic to prove the analysis/ pattern
    parsing.py       #   the names tables, similarity_name, score_meaning, parse_domain, parse_collection,
                     #   network_access, parse_mapping, unindexed_fields, read_settings, guess_text_field,
                     #   source_field, source_of, index_from_cat, parse_knn_stats
    vectors.py       #   vector_memory, vector_count, index_vector_memory, knn_memory_limit, domain_knn_memory,
                     #   score_to_similarity, check_vectors
    cost.py          #   domain_monthly_cost, serverless_minimum, ocu_monthly_cost
    queries.py       #   the filter operators, build_filter, describe_filter, knn_query, query_python,
                     #   describe_vector_field
    findings.py      #   domain_findings ... search_findings (~450)
  http.py            # _READ_POSTS, OpenSearchError, _error_details, _path, _store_url
  embeddings.py      # _as_vector, _base_model, _embedding_style, _embedding_request, _embedding_from
  analyzer.py        # OpenSearchAnalyzer (~850)
  style.py           # _ROOT, _CSS, _BADGE, _render_html
  view.py            # the cell and label helpers (_state_tone ... _filter_rows) and OpenSearchView (~1,050)
```

- **`request()` and the signing stay methods of `OpenSearchAnalyzer`.** Taking them out of the class would change
  code, not move it. `http.py` holds only the module-level REST helpers, and `analyzer.py` imports `_READ_POSTS`
  from it. CLAUDE.md's description of `request()` stays true.
- `_exists` and `_drop` (in section 4, before the class) go to whichever module their callers are in.
- A constant that both the view and the analysis read (the names tables, `_FILTER_OPS`, ...) goes in the lower
  layer, and the view imports it from there.
- No first commit for decision 7: the agent has no OpenSearch tools.
- Tests: `osmod._bytes` and `osmod._int` come from `aws_analyzer.opensearch.helpers`, and `osmod._render_html` from
  `aws_analyzer.opensearch.style`. There are no monkeypatches to re-target. `tests/fake_opensearch.py` and demo.py's
  `seed_opensearch()` use public names only, but grep them anyway.

### `lambda_functions` (11,890 lines) — second, the full pilot, done

The layout below was the plan. What it became is `plans/lambda_functions.py` (34 modules, the largest `view.py` at
1,450 lines). It differs in these ways:
- `prices.py` holds the price table.
- `analysis/text.py` holds the findings' wording helpers (`_window`, `_cli`).
- `analysis/overview.py` holds `Overview`.
- `LogRun` / `LogPage` live in `analysis/logs.py`, the code map's dataclasses in `analysis/codemap/model.py`, and the
  graph's in `analysis/codemap/graph.py`: each next to the functions its properties call.
- `analysis/codemap/` has `terms.py` (what the reader knows) and `syntax.py`.
- The explorer is `frame.py`, `widgets.py`, a module per tab and `window.py`.

It has every kind of front-end (View, explorer, agent tools), so it proves what OpenSearch couldn't: mixins, an
explorer, blocks, and decision 7.

```
lambda_functions/
  helpers.py              # section 1 (lines ~100-320)
  models.py               # section 2: Function, Invocation, Overview, LogEvent, CodeMap, CodeStep, CodeGraph, ...
  analysis/
    functions.py          # masked_config, parse_function, runtime_status, parse_policy, parse_event_source_mapping
    cost.py               # provisioned_monthly_cost, log_storage_monthly_cost, function_monthly_cost
    findings.py           # function_findings, account_findings, _runtime_findings, _usage_findings, _errors_level
    errors.py             # request_id_of, classify_error, group_errors, error_findings
    logs.py               # parse_report, split_runs, line_level
    performance.py        # percentile, suggest_memory, performance_findings
    package.py            # handler_file, package_file_name, read_package, package_findings
    codemap/              # ~2,300 lines on its own
      aws_model.py        # _service_name, _botocore_loader, _aws_model, _iam_action, events, secrets
      reader.py           # _Sym, _Frame, _Module, _Collect, _CodeReader (~1,060 lines)
      mapping.py          # map_code, map_package
      findings.py         # code_map_findings, _code_summary
      graph.py            # code_graph, the mermaid helpers
  analyzer.py             # LambdaAnalyzer (~1,130 lines)
  style.py
  blocks/
    wiring.py             # _Wiring, _Columns and their drawers
    outline.py            # _Outline, _flow_html, _outline_html/_lines
    graph.py              # _Graph, _GCard, the _g_* SVG layout and drawing (~700 lines)
  view.py                 # LambdaView (~1,180 lines) and its cell helpers (_label, _runtime_meaning, ...)
  explorer/
    __init__.py           # LambdaExplorer composed from its tabs, explore()
    window.py             # _explorer_rules, _EXPLORER_CSS, _window_text, _FunctionField, _Row, _RunRow
    functions.py logs.py code.py ...   # LambdaExplorer (~2,150 lines) as _<Topic>Tab mixins
```

- First commit (decision 7): `LambdaAnalyzer._window` → `window` and `._numbers` → `numbers`. Pick clearer names if
  they collide with an attribute; every caller changes.
- Tests to re-target: `_RUN_LINES`, `_TOGGLE_GRACE`, `map_package` (patched where the explorer looks it up),
  `urllib.request.urlopen` (on the module that calls it).

### `s3` (11,679) and `s3_explorer` (2,932), done

The layout below was the plan. What it became is `plans/s3.py` (51 modules, the largest `view/folders.py` at 860
lines) and `plans/s3_explorer.py` (`s3/explorer/`, 8 modules). It differs in these ways:
- `readers/` comes after `models` (the parsers return `Document`, `Picture`, `PdfPage`) and holds formats, avro,
  office (Word, PowerPoint, Excel), pdf, media and data; `prices.py` holds the price tables and `ARCHIVE_CLASSES`.
- `analysis/` is cost, summary, bucket (bucket_findings and the settings in words the agent reads), duplicates,
  downloads, lifecycle, policy, notifications, documents (`pdf_flow`) and details (`file_details()`'s readers).
- `S3Analyzer` keeps its plumbing (`__init__`, regions, clients, `account_id`) in `analyzer/s3_analyzer.py`, over
  `_BucketReads`, `_ListingReads`, `_VersionReads`, `_FileReads`, `_PreviewReads` and `_DownloadReads`, a module
  each; `threads.py` and `streams.py` hold the module-level helpers.
- `S3View` (`view/s3_view.py`) is a `_<Topic>Commands` mixin per `_GROUPS` entry, in `view/buckets.py` ...
  `view/downloads.py`, each with the cell helpers only it uses; `view/cells.py` has the two that several share.
- `S3Explorer` (`explorer/window.py`) is `_ListPane`, `_ReportPane`, `_SelectionPane` and `_SettingsPane`, with
  `navigator.py` (the pure helpers and `S3Navigator`) and `frame.py` (stylesheet, rows).

- `helpers.py` plus `readers/`: the stdlib-only Avro, DOCX and PPTX parsers and format sniffing (section 1 is
  1,440 lines, mostly these).
- `analysis/`: summary, lifecycle (simulate_lifecycle), policy (explain_policy), cost, findings.
- `S3Analyzer` (~3,590 lines) → `analyzer/` with `_<Topic>Reads` mixins: listing, configuration, files and preview,
  downloads (`clean_downloads` and the downloads-folder guards stay together in one module, because they are the
  one place that deletes files), CloudWatch.
- `S3View` (~2,460 lines) → `view/` with `_<Topic>Commands` mixins by `_GROUPS`.
- **Fold `s3_explorer.py` in as `s3/explorer/`** (S3Navigator and the pure helpers in `explorer/navigator.py`).
  `aws_analyzer/s3_explorer.py` stays as a module that re-exports `S3Explorer` and `S3Navigator`, so old imports
  work. Along with it:
  - Remove `s3_explorer` from `COMPANIONS`.
  - Point `_EXPORTS` for `S3Explorer` and `S3Navigator` at `s3`.
  - Update `test_explorer_builds_on_the_s3_installed_with_it` and the bare-name list in `tests/conftest.py`.
  - `_s3_module()` becomes a plain import of the parent package. Its `import s3` / `__main__` fallbacks date from
    the standalone files and go.

  This is the one step in the plan that changes a test's expectation (where `S3Explorer` is defined). Say so in the
  PR.
- First commit (decision 7): `S3Analyzer._cloudwatch_in`, and `s3._rule_scope`, `_rule_actions`, `_exposure`,
  `_encryption_label`, `_block_label`.

### `_bedrock.py` (2,078) → `_bedrock/`, done

The layout below was the plan. What it became is `plans/_bedrock.py` (11 modules, the largest `markdown.py` at 730
lines). It differs in these ways:
- The dataclasses (`KBDocument`, `Passage`, `Citation`, `ModelInfo`) are in `models.py`, and `parse_models` with its
  helpers in `foundation_models.py`, so `prices.py` holds only the tables, `model_price`, `short_model` and the
  rerank models.
- `helpers.py` (IDs, source names, Bedrock's metadata keys, name matching) and `words.py` (the question's words,
  snippets and `_highlight`) are new.
- `markdown.py` is pure (it imports only `_kit.text`), and `blocks.py` is the one UI module: `_Answer`, `_Json`,
  `_Download`, their drawers and `_file_list_blocks`.

`prices.py` (price tables, `DEFAULT_MODEL`, `model_price`, `short_model`, `parse_models`, `ModelInfo`), `parsing.py`
(`Passage`, `Citation`, `KBDocument`, `parse_retrieve`, `parse_document`), `filters.py`, `estimates.py`
(cost and tokens), `markdown.py` (`_Markdown`, `_Answer`, `_Json` and their drawers: UI layer), `files.py`
(`presigned_url`, the file lists, `_Download`). `SHARED` and `rules.py`'s shared-name check follow the package.

### `bedrock_kb` (8,566), done

The layout below was the plan. What it became is `plans/bedrock_kb.py` (34 modules, the largest `explorer/window.py`
at 1,060 lines). It differs in these ways:
- `BedrockKBAnalyzer` was 1,370 lines, under the limit, but took mixins by its own sub-banners: `_KnowledgeBaseReads`
  (knowledge bases and data sources), `_SearchReads` (retrieval and generation), `_DecidingReads` and `_FileReads`,
  in `analyzer/`, with `kb_analyzer.py` keeping `__init__` and `client`.
- `BedrockKBView` is `_KnowledgeBaseCommands`, `_IndexCommands` ("What's indexed", 840 lines), `_SearchCommands` and
  `_MeasureCommands` by `_GROUPS`, in `view/`; `kb_view.py` keeps the plumbing and `explore()`, and `view/cells.py`
  the labels and tones the View and the window share.
- `analysis/` is common, prompting, parsing, settings, filters, deciding, cost, findings, files, metadata and chunks.
- The blocks fit in one `blocks.py` (290 lines), and the explorer is `frame.py`, `widgets.py` and `window.py`.

`analysis/`: inventory and file states (`inventory_files`, `file_state`, `FILE_STATES`), chunks (`place_chunks`,
`order_chunks`, `chunk_overlap`), retrieval and answers, findings. `BedrockKBAnalyzer` (~1,950) → `_<Topic>Reads`
mixins (configuration, files, search). `BedrockKBView` (~2,585) → `_<Topic>Commands`. Blocks (`_Steps`,
`_Pipeline`, `_Chunks`, `_Shares`, `_Passage`) into `blocks/`. `KBExplorer` (~1,000) → `explorer/`.

### `bedrock_chat` (9,079), done

The layout below was the plan. What it became is `plans/bedrock_chat.py` (34 modules, the largest `analyzer.py` at
920 lines). It differs in these ways:
- `BedrockChatAnalyzer` (880 lines) stayed one module, with no mixins.
- `analysis/` is parsing, schema, filters, choices (what the pickers list), request, findings, batches, sweeps,
  ranking, records and code. `Field` lives in `analysis/schema.py`, `Batch` / `BatchItem` in `analysis/batches.py` and
  `Sweep` in `analysis/ranking.py`, each next to what its properties call; `_diff` went to `helpers.py`.
- `BedrockChatView` is `_ChatCommands`, `_TestCommands`, `_RunsCommands`, `_SettingsCommands` and
  `_KnowledgeBaseCommands` by `_GROUPS`, in `view/`; `chat_view.py` keeps the plumbing and `chat()`.
- `_ChatApp` is `_PickersPane`, `_ConversationPane`, `_SettingsTab`, `_RequestTab` (Request, Response and Code),
  `_TestTab` and `_RunsTab`, in `window/`; `app.py` keeps `__init__`, the layout, the plumbing and the public
  methods the View calls (`sync`, `added`, `cleared`, `ran`, `swept`, `loaded`, `runs_changed`).
- `blocks.py` also holds what the View and the window both draw with (`_wrap`, `_kind_text`, `_setting_marks`,
  `_QUICK`), since the View can't import the window.

`analysis/`: the request schema (`request_schema`, `Field`, `Schema`, `_KNOWN`, `build_request`,
`settings_from_request`, `validate_request`), runs and sweeps (`parse_questions`, `sweep_setups`, `rank_runs`,
`run_score`, `ranking_findings`), the code it writes (`python_script`, `config_json`, `cli_command`), and saved runs
(`run_record`, `read_runs`). `_ChatApp` (~2,020) → `window/` with a `_<Topic>Tab` mixin per side tab (settings,
test, runs, code, request/response) and one for the pickers and composer. `BedrockChatView` (~2,230) →
`_<Topic>Commands`.

### `sagemaker_env` (5,044), done

The layout below was the plan. What it became is `plans/sagemaker_env.py` (14 modules, the largest `view.py` at
1,140 lines). It differs in these ways:
- `prices.py` holds `INSTANCE_TYPES` and `SAGEMAKER_PRICES`.
- `machine.py` and `envs.py` are `SageMakerAnalyzer`'s mixins (`_MachineReads`, `_EnvReads`), with the constants only
  they read (`METADATA_FILE`, `_HOMES`, `_PACKAGES`). `create_env` and `_run` are `envs.py`'s `_EnvMaking`, a mixin
  of their own. `analyzer.py` keeps `__init__`, the clients, the notebooks and `running()`.
- The pure side of each is in `analysis/`: `machine` (the `/proc`, nvidia-smi and metadata parsers, which return
  section-2 dataclasses, so they left section 1), `common` (what several reports' findings share), `notebooks`,
  `disk`, `running` and `envs`.
- `shell_path` and `_tilde` moved from section 3 to `helpers.py`, since the disk, environment and View code all
  write paths with them.

The core has three parts, not one:
- `machine.py`: `/proc`, disks, GPU, the metadata file, `_shown` / `_real`.
- `envs.py`: environments, kernels, tools, `env_plan`.
- `analyzer.py`: AWS.

`create_env` and `_run` are the module's only writes, so keep them together in one module with nothing else that
writes. The View (~1,055) stays one module.

### `dynamodb` (3,499), done

The layout below was the plan. What it became is `plans/dynamodb.py` (7 modules, the largest `view.py` at 1,300
lines). It differs in one way: `prices.py` holds `DYNAMODB_PRICES`, as in every other package.

A flat package, like the template, with no mixins expected. DynamoDB JSON ↔ Python conversion stays in
`helpers.py`.

### Last: the leftovers

- Update the `new-analyzer` skill to scaffold a package from the template, with dynamodb as its model.
- Update CLAUDE.md: remove "Architecture of an analyzer file" and the five-sections rule in `rules.py`.
- Update README / docs wherever they say "each service is one module", and the module name each guide's eyebrow
  and `docs/index.md` show (`<code>opensearch.py</code>`). These were left alone so the split wouldn't collide
  with the docs rewrite on `docs-skimmable`.
- Make the private-names warning from Phase 0 an error.

## Phase 2 (needs its own plan and the user's go-ahead): findings that carry actions

Today a finding is `("warn", "... (see errors('etl'))")`. The View call is written into the sentence, and each
window rewrites it with regexes (`_window_text`, `_WINDOW_WORDS`) into "the Errors tab". The core is speaking one
front-end's language. The direction is a core-side `Finding(level, message, action)` with
`Action(command, args, kwargs)`, rendered by each front-end: the View through `_call`, a window as its tab, the
agent as a `_next`.

It isn't part of the moves because:
- It changes what `*_findings` return, which is public API.
- CLAUDE.md says the pairs stay as they are.

Write that plan only after the moves are done, and ask the user before starting it.

## Progress

Update this table in each step's PR.

| Step | Status | PR | Notes |
|---|---|---|---|
| Phase 0: tooling | done | #97 | branch `modularize/tooling` |
| opensearch | done | #98 | plan in `plans/opensearch.py` |
| lambda_functions | done | #99 | plan in `plans/lambda_functions.py` (mixins and modules) |
| s3 + s3_explorer | done | #101 | plans in `plans/s3.py` and `plans/s3_explorer.py`; branch `modularize/s3` |
| _bedrock | done | #107 | plan in `plans/_bedrock.py`; branch `modularize/_bedrock` |
| bedrock_kb | done | #108 | plan in `plans/bedrock_kb.py` (mixins and modules); branch `modularize/bedrock_kb` |
| bedrock_chat | in review | #114 | plan in `plans/bedrock_chat.py` (mixins and modules); every module now fits the limit, so `LONG_FILES` is empty |
| sagemaker_env | done | #105 | plan in `plans/sagemaker_env.py` (mixins and modules); branch `modularize/sagemaker_env` |
| dynamodb | in review | #109 | plan in `plans/dynamodb.py`; branch `modularize/dynamodb` |
| leftovers | not started | | new-analyzer skill, CLAUDE.md, README, private-names error |
| Phase 2: findings with actions | needs a plan | | ask the user first |

## Mistakes to avoid

- **Mixing a fix into a move.** If you spot a bug while moving code, note it for a follow-up PR. A move commit that
  also changes code is hard to review, and the snapshot can't tell the two apart.
- **Patching the re-export.** `monkeypatch.setattr(package, name, ...)` doesn't reach a submodule that imported the
  name. Patch the module that looks it up.
- **Import cycles.** If `view.py` and `explorer/` import each other at the top, the package fails to import.
  Lower layers never import higher ones, and `explore()` imports the explorer inside the function.
- **Leaving `__init__.py` heavy.** It holds the docstring, the imports for re-export and `__all__`. No logic, no
  constants, no helper "for now".
- **Losing an AWS operation from `rules.py --apis`.** That means the read-only check no longer sees a call. Fix the
  services lookup; don't accept the diff.
- **Raising a number** in `COMMENTS_LEFT`, `LONG_FILES` or a per-file-ignores entry to make a check pass.

## Lessons

What a finished step found that this plan got wrong or didn't say, newest first, with the service it came from. Fix
the recipe above as well. This section is for what the next agent must know and can't see in the code.

- **bedrock_chat:**
  - **A window's public methods that the View calls aren't commands.** `_ChatApp.sync()`, `ran()`, ... have no
    `@_window_errors`, and `rules.py` checks every public method of a `_*Tab` / `_*Pane` as a command. They stayed in
    the composed class (`_ChatApp` isn't named `*Explorer`, so it isn't checked), and the mixins hold only private
    methods. Adding the guard would change behaviour, so it's not part of a move.
  - **A top-level bare expression** (`_draws(_Code, "text")(_text_lines)`, a drawer registered without a `def`) had no
    name a plan could use. `split.py` now names one `expr@<line>`.
  - **A test patched a name two modules look up** (`_cell_number`: `app()` records it, `_ipython_display_` compares
    with it). Patching one would make the test pass for the wrong reason; `in_cell()` patches both.
  - **mixins.py writes the new class line as one line**, which went past 120 characters for `BedrockChatView`. Wrap it
    in the scratch copy before splitting, as with the lazy import.
  - **Nothing for decision 7**: the agent doesn't read bedrock_chat.

- **dynamodb:**
  - **`rules.py --apis` lists `dynamodb:Scan` / `Query` under `models.py` and `view.py`.** Strings that name an
    operation (`operation: str = "scan"`, `_GROUPS`'s `"query"`, `_call("scan", ...)`) count as one unless they're a
    keyword value or compared. In one file they merged with the analyzer's real calls; split apart they show. The union
    per service is the baseline's, which is what to compare.
  - **Nothing for decision 7**: the agent has no DynamoDB tools.

- **bedrock_kb:**
  - **`REEXPORT_KIT` takes any public name the old module imported**, not only `_kit`'s: `split.py` finds where each
    came from in the old imports. bedrock_kb's `_bedrock` names (`MODEL_PRICES`, `Passage`, the `X as X` ones) are
    listed there, so `bedrock_kb.MODEL_PRICES` still works.
  - **`split.py` rewrites the imports, so a comment above them is dropped.** bedrock_kb's two lines above its
    `_bedrock` imports went, and `COMMENTS_LEFT`'s total went down by two.
  - **Module-level helpers in section 4 that several mixins call** (`_question_text`, `_eval_pairs`, `_with_errors`)
    were pure, so they went to `analysis/`, not into one mixin's module.
  - **A test patched a stdlib module through the service** (`monkeypatch.setattr(kbmod.time, "monotonic", ...)`):
    it's the same module object, so the test imports `time` itself.
  - **`apis.txt` lists the operations per module now**: compare the union per service with the baseline's (a short
    script over both files), as s3's lesson says.

- **_bedrock:**
  - **Its users imported its private names** (`from ._bedrock import _highlight, _Answer, ...`), and a package's
    `__init__` re-exports only public names. bedrock_kb, bedrock_chat and the agent now import each name from the
    module that defines it (`from ._bedrock.words import _highlight`), their `X as X` re-exports kept; that was the
    one change outside the package. When bedrock_kb or bedrock_chat is split, `split.py` carries those imports over
    with the right depth (`from .._bedrock.words import ...`).
  - **No snapshot covers it on its own**, and `names.json` skips modules whose name starts with `_`. Run the snapshot
    for bedrock_kb and bedrock_chat (whose names include what they import from it), the agent's tests, and compare
    `dir(aws_analyzer._bedrock)` before and after against the names its submodules define.
  - **`rules.py` read the package's `__all__` as a shared name** and flagged every other `__all__` as a copy of it.
    `shared_names()` now leaves dunders out and says which module has each name.

- **sagemaker_env:**
  - **An analyzer under the limit can still take mixins**, when the plan splits it by where it reads from. They
    followed the class's own `# ----` sub-banners (this machine, disk, Python environments), which moved with the
    first member under each, so the comment count didn't change.
  - **A test that patched a module through the service** (`smmod.platform`) patches the same module object through
    the submodule that calls it (`envs_reads.platform`); `_kit` names a test read off the service (`smmod._Hint`,
    `smmod._Title`) come from `_kit`.
  - **Patching the class still works for mixins.** demo.py sets `SageMakerAnalyzer._disk_usage` and friends on the
    composed class, which shadows the mixin's method, so it needed no change.

- **s3:**
  - **The explorer couldn't stay a companion through the split.** It reached into s3 through `self.s3._Note`,
    `self.s3._render_html`, `self.s3._zip_layout`, ..., and a package re-exports public names only. Its own commit
    (before the split) made it part of the package: those names are imported from `_kit` and the parent package
    instead, `_s3_module()` is the parent package, and `x.s3` stays. Do the same for any window that reads its
    service through a module object.
  - **An alias module** (`s3_explorer.py`) keeps the old import path. `rules.py` checks it holds nothing but
    re-exports (`ALIASES`), and `test_package` lets it load its target. The snapshot's compare lists the old file's
    private names as LOST, since a file module has no "inside"; check each one is in the new package's `inside` in
    names.json (they all were) instead of `--allow-lost`-ing them.
  - **Parsers in section 1 returned section-2 dataclasses**, and pure analysis read section-4 names (`_READ_ERRORS`,
    `_ReadLimit`, `_columnar_info`, `_npy_header`). `readers/` went between `models` and `analysis`, and those names
    moved down into it. `split.py` stops on each such case; the deps listing (`read_source`, `defined_names`,
    `used_names` over every statement and every member of the big classes) showed them all at once.
  - **Class-body aliases** (`_preview_tsv = _preview_psv = _preview_csv`) stayed behind in the class and broke it.
    `mixins.py` now treats one as a member named by its first name.
  - **A rename for decision 7 can collide with a local**: the View has `exposure = _exposure(...)`, so `_exposure`
    became `public_exposure`. The View helpers the agent reads moved to the core (`analysis/bucket.py`), since the
    agent reads only the core.
  - **The tools assumed one file**: `snapshot.py`'s `_layout` looked for `s3.py`, and `shots.py` found the View by
    `__module__ ==` (so it couldn't find a package's). Both fixed. `rules.py --apis` now lists S3's operations per
    module; compare the union per service against the baseline, not the lines.
  - **CI's wheel smoke test (`ci.yml`, and the same in `release.yml`) named `s3_explorer._s3_module`**, which local
    `/check` didn't catch, since `run.py` has its own copy of the check. Grep `.github/workflows/` for the names
    a step moves, too.
  - **`--allow-lost` takes several names after one flag** (`--allow-lost a b c`); repeating the flag keeps the last.

- **lambda_functions:**
  - **Some dataclasses call analysis functions** in their properties (`Overview` reads `function_monthly_cost`,
    `LogPage` reads `split_runs`). In one file that works because names are looked up when they're called. Split
    apart, `models` and `analysis` would import each other. They moved next to the functions they call, which keeps
    the layers acyclic without changing a line. Expect the same in every big service.
  - **A name was assigned twice at the top level.** `_SECRET_NAME_RE` was the environment-variable pattern for
    `secret_like()` and, 1,200 lines later, the code reader's. The second won everywhere. The two patterns match the
    same names, so giving each its own module changed nothing, but check this every time. Follow-up: one pattern,
    one name.
  - **Mixins by tab worked.** `LambdaExplorer`'s methods were already grouped by tab, so each mixin is a run of
    them, and a constant only one tab reads moved into that tab's module. A test then patches it there
    (`logs_tab._RUN_LINES`). Rules now check the explorer's public commands, and they already had `@_window_errors`.
  - **Reaching up a layer took one lazy import**, in `LambdaView.explore()`. It's the only line in the split that
    isn't a move.
  - **The OpenSearch PR left a dead link** in README's services table (`opensearch.py`). Grep README for the old file
    name, not only the line the recipe names.
  - **`rules.py --apis` showed a false `lambda:ListFunctions` in `view.py`.** The view calls
    `self.core.list_functions()`, the analyzer's own method, and the check skipped method names only when the same
    file defined them. It now reads every function the package defines (`owner_functions`). If a split's API list
    gains a line in a UI module, look for the same thing before anything else.
  - **`view.py` is 1,450 lines**, close to the limit. The next command that grows it should split it into
    `_<Topic>Commands` mixins by `_GROUPS`.
- **opensearch:**
  - **One commit for the whole split, not one per module.** Code moved by `split.py` changes in no other way, and
    the snapshot checks every module at once. The recipe (step 4) now says so.
  - **The old module's docstring stays as written** in `__init__.py`, even where it says "this file". It's what
    `help(aws_analyzer.opensearch)` shows, and rewording it is a change of its own.
  - **`__init__` re-exports the public `_kit` names the old module imported** (`human_size`, `HOURS_PER_MONTH`,
    ...), since `aws_analyzer.opensearch.human_size` worked before. Stdlib and botocore names it imported
    (`datetime`, `ClientError`) aren't re-exported. Nothing used them, and they were never its API.
  - **Two modules were added to the layout:**
    - `prices.py` (core), for the price tables. They were 240 lines of section 1, and a price check touches only
      them.
    - `embeddings.py` (core), for building Bedrock embedding requests.

    The analyzer-only helpers `_exists` / `_drop` stayed in `analyzer.py`.
  - **A view importing a core module's private helper** (`_key_label`, `_is_serverless`, `_base_model`) is fine:
    they're in the same package.
- **Phase 0:** `test_docstrings_have_their_quotes_on_their_own_lines` takes about 100 s, almost all of it on the
  long files (`ast.get_source_segment` slows down on very long files). Expect it to speed up as services are
  split. Until then, run `pytest tests/test_<service>.py` while you work, and the full suite at the end.
