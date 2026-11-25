---
name: codegraph-adhoc
description: Ad hoc context lookup across every repo under ~/git.work using the codegraph CLI from bash, from any working directory (including ~ or non-indexed dirs). Locate a symbol, file, flag, table, or flow fast, then pull just the source you need. Use when asked "where is X defined", "which repo has X", "find context for X", "look up X across repos", "what calls X", when the cwd is not an indexed repo, or when the codegraph_* tools are unavailable or timing out.
---

# codegraph-adhoc

Quick, cheap context lookups against the shared `~/git.work` graph. For deep work
inside one repo, use the `codegraph` skill and its `codegraph_explore` tool instead.

## Facts from past sessions

- Only three indexes exist: `~/git.work/.codegraph` (root, ~21.9k files, all repos),
  `353.e2e-bdd-playwright`, and `380.sdd_scheduler_workspace.`. Every other repo
  path walks up to the **root** graph. A path like `~/git.work/322.PlatformSync-Logic-Service`
  still searches all repos, so results from other repos leak in.
- Root explore costs ~30 s and has a budget of 4 calls. `query`, `node`, and
  `callers` take under 1.5 s each.
- These failed in past sessions:
  - `structure_only` / `context --no-code` on the root: command failed.
  - Huge multi-repo "trace everything" queries: `aborted` / `timed out`.
  - Non-code files (`.yml`, `jest.config.js`, `.idea/*`, some `.md`): `No relevant code found`.
  - Any command during an index or sync: `database is locked`.
- `~/svn` is not indexed.

## Ladder: cheapest first

Always pass `-p ~/git.work` so the command works from any cwd. Prefix paths with the
repo folder, e.g. `322.PlatformSync-Logic-Service/src/...`.

1. **Locate** the symbol, file, or string name. Returns repo/file:line.
   ```bash
   codegraph query EntityOrderingLock -p ~/git.work -l 10
   codegraph query isPatientFormV2Enabled -p ~/git.work -k function -j
   ```
2. **Read one symbol or file**. Returns source plus callers, callees, and dependents.
   ```bash
   codegraph node EntityOrderingLock -p ~/git.work -f 322.PlatformSync-Logic-Service/src/functions/inbound/services/entityOrderingLock.ts
   codegraph node -p ~/git.work -f <repo>/<file> --symbols-only        # symbol map only
   codegraph node -p ~/git.work -f <repo>/<file> --offset 120 --limit 80
   ```
3. **Who uses it / what breaks**:
   ```bash
   codegraph callers <symbol> -p ~/git.work -l 20
   codegraph callees <symbol> -p ~/git.work
   codegraph impact  <symbol> -p ~/git.work -d 2
   ```
   The root graph matches by bare name across all repos. Generic names (`debug`,
   `handler`, `acquire`) can resolve to the wrong repo, so check the repo prefix
   on every hit.
4. **List a repo's files**:
   ```bash
   codegraph files -p ~/git.work --filter 322.PlatformSync-Logic-Service/src/functions --format flat --no-metadata
   ```
5. **Explore a flow**. Use this only after steps 1–3 have named the symbols.
   ```bash
   codegraph explore -p ~/git.work --max-files 4 \
     "Only 322.PlatformSync-Logic-Service: handler -> EntityOrderingLock.acquire -> release"
   ```
   Run it with `timeout 120`. Use the `codegraph_explore` tool for the same job if it is loaded.

## Query habits that worked

- Name concrete symbols plus repo-prefixed paths:
  `"317.rt-scheduler-iq-dev/src/modules/scheduler/rules_engine/rule_checker.py RuleChecker._run_slot_evaluation run_rules_once"`.
- Scope root queries: start with `Only <repo>:` and end with `Exclude other repos.`
- For a flow, name both ends: `"how does createAppointment reach sqsPublish"`.
- For one or two repos, name them in the query instead of asking "across all
  repositories". Split cross-repo questions into one query per repo.
- Feature flags, table names, and config keys are often constants. Run `query` on
  the exact string first.

## Fall back to plain tools when

- The target is config, YAML, a workflow, an IDE file, or docs: use `read`, or `rg` in that repo.
- `query` returns nothing for an exact string literal (strings in bodies are not
  symbols): use `rg -n '<string>' ~/git.work/<repo>`.
- You get `database is locked`: an index or sync is running. Wait, or use `rg`. Never run `unlock` unless the user asks.
- The target is in `~/svn`: not indexed, use `rg`.

## Freshness

The index does not watch files. If results look stale after pulls, run
`codegraph sync ~/git.work` (incremental, in the background with `nohup`, tail the log
with a timeout). Never run `init`, `index`, `uninit`, or `daemon`.

## Report

Answer with `repo/path:line` citations from the output. Say which part of the
question was not covered. Do not paste whole explore dumps.

## In Claude Code

The `codegraph_explore` tool is named `mcp__codegraph__codegraph_explore` here. The CLI steps above work unchanged through Bash.
