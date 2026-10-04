---
name: debugging-dbt-runs
description: Diagnose and fix failing dbt runs — Jinja/compilation errors, ref/dependency and DAG issues, incremental models producing wrong or duplicate rows, full-refresh needs, and state/deferral problems. Use when dbt run or dbt build fails, a model compiles wrong, an incremental model is stale or duplicated, or a CI dbt job errors.
---

# Debugging dbt Runs

## When to use

- `dbt run`/`dbt build` fails or a model errors.
- Compilation/Jinja errors, or `ref()` cannot find a model.
- An incremental model is stale, missing rows, or has duplicates.
- CI dbt job behaves differently from local.
- Do NOT use for authoring new models/tests (use the building/testing skills).

## Workflow

```
- [ ] Read the actual error + the compiled SQL (target/compiled/...)
- [ ] Classify: compile/Jinja, dependency/DAG, incremental, or env/state
- [ ] Reproduce the smallest failing command
- [ ] Fix, then re-run just that node with --select
```

1. **Read the compiled SQL.** dbt writes it to `target/compiled/...`. Most
   "weird" errors are obvious once you see the rendered SQL, not the Jinja.
2. **Classify the failure** and apply the matching fix below.
3. **Isolate** with `dbt run --select <model>` (and `+model`/`model+` for
   upstream/downstream) rather than rebuilding everything.
4. **Re-run** the single node to confirm.

## Patterns

**Compilation / Jinja**

- `dbt compile --select <model>` and open `target/compiled/...` to see rendered SQL.
- Undefined variable/macro → check `{{ }}` names, `vars:`, and package installs
  (`dbt deps`).
- "Model depends on a node that was not found" → a `ref()` name typo or the model
  isn't in a selected path.

**Dependency / DAG**

- Circular dependency → two models `ref()` each other; break the cycle via an
  intermediate model.
- `dbt ls --select +<model>` shows the upstream graph to trace missing nodes.

**Incremental problems**

- Duplicates after re-run → missing/incorrect `unique_key`, or `append` strategy
  where `merge` was needed.
- Missing recent rows → the `is_incremental()` filter is too strict (no lookback)
  or compares the wrong column.
- Schema changed and run fails → set `on_schema_change` or run
  `dbt run --select <model> --full-refresh` once to rebuild.
- To rebuild from scratch: `dbt run --full-refresh --select <model>`.

**Environment / state**

- Works locally, fails in CI → different `--target`, missing `dbt deps`, or stale
  `manifest.json` for `state:modified` selection. Regenerate/pass `--state`.
- `dbt build --select state:modified+ --defer --state <prod-manifest>` runs only
  changed models against prod parents (Slim CI). A stale manifest selects the
  wrong nodes.

## Common pitfalls

- **Debugging Jinja instead of compiled SQL** — always read the rendered query.
- **`--full-refresh` in production by reflex** — it rebuilds huge tables; only do
  it when the incremental logic or schema genuinely changed.
- **Ignoring `dbt deps`** — missing packages cause macro-not-found errors in CI.
- **Assuming order** — dbt parallelizes; never rely on run order, only on `ref()`
  dependencies.
- **Silent incremental drift** — add a periodic full-refresh or reconciliation
  test to catch rows that the incremental filter missed.
