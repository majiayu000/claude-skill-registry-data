---
name: implementing-data-cicd
description: Set up CI/CD for data pipelines — SQL/dbt linting (SQLFluff), compilation and test gates, dbt Slim CI with state:modified and deferral, environment promotion (dev/staging/prod), and running only changed models on pull requests. Use when adding CI checks to a dbt or SQL project, automating pipeline tests on PRs, speeding up CI, or promoting changes across environments.
---

# Implementing Data CI/CD

## When to use

- Adding CI checks to a dbt/SQL/pipeline repo.
- Automating lint, compile, and tests on pull requests.
- Speeding up CI by building only changed models (Slim CI).
- Promoting changes across dev → staging → prod.
- Do NOT use for reviewing an individual PR's logic (use
  `reviewing-data-pipeline-code`).

## Workflow

```
- [ ] Lint SQL (SQLFluff) and check formatting on every PR
- [ ] Compile the project to catch ref/Jinja errors early
- [ ] Build + test only changed models against prod parents (Slim CI)
- [ ] Run in an isolated CI schema; tear it down after
- [ ] Promote across environments with the same code, different targets
```

1. **Lint first** — SQLFluff catches style and some correctness issues fast and
   cheap, before spinning up a warehouse.
2. **Compile** — `dbt compile` (or `parse`) fails on bad `ref()`/Jinja without
   running SQL.
3. **Slim CI** — build and test only `state:modified+` using a production
   `manifest.json` as state, and **defer** unchanged parents to prod so CI doesn't
   rebuild the whole project.
4. **Isolate** — run into a unique CI schema (e.g. per PR) and drop it afterward so
   runs don't collide.
5. **Promote** — the same code runs against dev/staging/prod via `--target`; never
   fork logic per environment.

## Patterns

**dbt Slim CI (GitHub Actions sketch):**

```yaml
- run: dbt deps
- run: dbt compile
- run: |
    dbt build --select state:modified+ \
      --defer --state ./prod-artifacts \
      --target ci
```

`--select state:modified+` builds changed models and their children; `--defer
--state` points unchanged parents at prod, so CI stays fast. A fresh/stale
`prod-artifacts/manifest.json` is required for correct selection.

**SQLFluff config** (`.sqlfluff`) — pin the dialect and templater so lint matches
your warehouse and dbt:

```ini
[sqlfluff]
dialect = snowflake
templater = dbt
```

**Environment promotion** — dev (developer schemas) → staging (full build on
merge) → prod (scheduled). Same repo, different `profiles.yml` targets and
credentials.

## Common pitfalls

- **Rebuilding the whole project on every PR** — slow and expensive; use Slim CI
  with `state:modified` + deferral.
- **Stale/missing state manifest** — `state:modified` selects the wrong nodes;
  refresh prod artifacts in CI.
- **Shared CI schema across PRs** — concurrent runs clobber each other; use a
  unique schema per PR and drop it.
- **Skipping `dbt deps` in CI** — macro/package-not-found failures.
- **Different logic per environment** — drift and "works in dev" bugs; vary only
  the target/config, not the code.
- **No teardown** — orphaned CI schemas accumulate cost.
