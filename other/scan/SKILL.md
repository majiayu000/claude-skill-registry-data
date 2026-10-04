---
name: scan
description: Scan project once per session. Run first — all other skills depend on this.
mcp: codebase-memory-mcp
---

# /supergraph:scan

Load verified, project-scoped graph context once. Follow the shared
`references/codebase-memory-contract.md`.

Announce: "📡 /supergraph:scan — loading project context..."

## 1. Detect project and branch

Use `git branch --show-current`, resolve the repository to an **absolute** path,
and run `bin/detect-project.sh` when present. Otherwise detect commands from:

| File | Type | Test | Lint | Format | Build |
|---|---|---|---|---|---|
| `package.json` | node | `npm test --` | `npx eslint .` | `npx prettier --write .` | `npm run build` |
| `Cargo.toml` | rust | `cargo test` | `cargo clippy` | `cargo fmt` | `cargo build` |
| `pyproject.toml` | python | `pytest` | `ruff check .` | `ruff format .` | `python -m build` |
| `go.mod` | go | `go test ./...` | `golangci-lint run` | `gofmt -w .` | `go build ./...` |
| `pubspec.yaml` | flutter | `flutter test` | `flutter analyze` | `dart format .` | `flutter build` |

Ask when none match; never guess commands. Derive one stable `CBM_PROJECT` from
the repository root name and retain it across branches. Default
`CBM_INDEX_MODE=moderate`.

## 2. Verify provider and freshness

1. Call `list_projects` and find `CBM_PROJECT`.
2. If found, call `index_status(project=CBM_PROJECT)`.
3. Treat missing project, changed branch, stale state, tool error, failed state,
   or `status: "degraded"` as requiring a new index.
4. **TTL reuse (10m):** If `index_status` returns `status: "ready"` and `BRANCH` matches `.supergraph-env:BRANCH` and `now - CBM_INDEXED_AT < 600s` and `head_sha` unchanged, reuse index — skip `index_repository`. Otherwise proceed to step 5. TTL check requires healthy `index_status`; never cache degraded/stale/error. On cache hit, still re-run `index_status` once to confirm liveness before `get_graph_schema`.
5. Call `index_repository(repo_path=<absolute repo path>, name=CBM_PROJECT,
   mode=CBM_INDEX_MODE)` when required (cache miss or stale/degraded). Require `status: "indexed"`.
6. Re-run `index_status`; never claim reuse without a healthy response.
7. Call `get_graph_schema(project=CBM_PROJECT)` and `get_architecture(project=CBM_PROJECT, aspects=["overview","layers","boundaries","clusters","hotspots"])` **in parallel** after verified `index_status`.
8. On cache hit, `get_graph_schema` and `get_architecture` may run in parallel immediately after TTL-passed `index_status`.

On any mandatory provider/index/schema error: STOP, show the exact error and the
recovery command (`codebase-memory-mcp cli index_repository --repo-path
<absolute> --name <project> --mode moderate`). Do not write freshness state.

## 3. Reverify Serena

Always call Serena initial instructions and activate project with the absolute repository path:
`mcp__serena__activate_project(project=<absolute repo path>)`.
Then load a top-level symbols overview (`mcp__serena__get_symbols_overview`).
Set `SERENA_ACTIVE=true` only after success; otherwise set it false and report Serena unavailable.

## 4. Write `.supergraph-env`

Only after healthy `index_status`, schema, and architecture responses:

```dotenv
PROJECT_TYPE=...
TEST_CMD=status=0; for test_file in plugins/supergraph/tests/test-*.sh; do bash "$test_file" || status=1; done; exit "$status"
LINT_CMD=bash -n install.sh plugins/supergraph/install.sh plugins/supergraph/tests/test-*.sh
FORMAT_CMD=...
BUILD_CMD=...
BRANCH=...
GRAPH_PROVIDER=codebase-memory-mcp
CBM_PROJECT=...
CBM_INDEX_MODE=moderate
CBM_INDEXED_AT=YYYY-MM-DDTHH:MM:SS
SERENA_ACTIVE=true|false
SCAN_TIMESTAMP=YYYY-MM-DDTHH:MM:SS
```

Branch-matched TTL reuse still requires `index_status` and Serena revalidation; TTL only skips `index_repository`, never skips `index_status` or schema checks. Serena revalidation is guarded by `SERENA_ACTIVE` — skip `initial_instructions` if `.supergraph-env:SERENA_ACTIVE=true` and scan ran <10m ago.

## 5. Report

Report project/type/commands, provider/project/index status, architecture counts
available from the response, Serena status, and whether scan was fresh or reused.

## Rules

- Never record false freshness after errors or degraded state.
- All graph calls include `project=CBM_PROJECT` where supported.
- Respect pagination and failure semantics in the shared contract.
- For trivial ≤2 files / <20 lines, graph discovery may stop after verified status (no hubs/bridges needed).
