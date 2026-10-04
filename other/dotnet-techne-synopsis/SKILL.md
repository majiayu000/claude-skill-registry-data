---
name: dotnet-techne-synopsis
description: "Use when you need blast-radius analysis, dependency graphs, cross-repo impact, breaking-change diff, or architectural overview of .NET workspaces. Keywords: blast radius, dependency graph, impact analysis, cross-repo, call graph, endpoint map, EF Core lineage, breaking change, daemon, reindex."
disable-model-invocation: false
user-invocable: true
license: MIT
compatibility: Pre-built binaries for osx-arm64, osx-x64, win-x64, win-arm64, linux-x64, linux-arm64. No SDK required.
metadata:
  author: Metalnib
  version: "1.6.0"
  trigger_keywords:
    - blast radius
    - dependency graph
    - impact analysis
    - cross-repo dependencies
    - call graph
    - endpoint map
    - ef core lineage
    - what does this change affect
    - architectural overview
    - breaking change diff
    - reindex repository
    - daemon mode
---

# Synopsis - .NET Workspace Dependency & Blast-Radius Explorer

Static analysis tool that scans .NET workspaces via Roslyn, builds a dependency graph, and answers blast-radius and breaking-change queries. Supports both one-shot CLI use and long-running daemon mode for multi-repo workspaces.

## Requirements

No SDK or manual installation needed. The detect script auto-downloads the correct binary on first use.

| Platform | Binary | Downloaded from |
|---|---|---|
| macOS Apple Silicon | `bin/osx-arm64/synopsis` | GitHub Release `synopsis-osx-arm64.tar.gz` |
| macOS Intel | `bin/osx-x64/synopsis` | GitHub Release `synopsis-osx-x64.tar.gz` |
| Windows x64 | `bin/win-x64/synopsis.exe` | GitHub Release `synopsis-win-x64.zip` |
| Windows arm64 | `bin/win-arm64/synopsis.exe` | GitHub Release `synopsis-win-arm64.zip` |
| Linux x64 | `bin/linux-x64/synopsis` | GitHub Release `synopsis-linux-x64.tar.gz` |
| Linux arm64 | `bin/linux-arm64/synopsis` | GitHub Release `synopsis-linux-arm64.tar.gz` |

External dependencies for auto-download:
- **macOS/Linux:** `curl` (pre-installed) or `wget`
- **Windows:** PowerShell 5+ (built-in `System.Net.Http`)

When a .NET 10 SDK is installed, the detect script downloads the slim framework-dependent build (`synopsis-<RID>-slim`, ~7x smaller) instead of the self-contained one. No SDK - self-contained build, no difference in behaviour.

## Install (optional - build from source)

Only needed if you want to rebuild or no GitHub Release is available. Requires .NET 10+ SDK.

**Bash (Linux/macOS):**
```bash
./skills/dotnet-techne-synopsis/scripts/install.sh
```

**PowerShell (Windows):**
```powershell
.\skills\dotnet-techne-synopsis\scripts\install.ps1
```

## When to use this skill

Use when the user asks to:
- Analyze blast radius of a code change
- Map dependencies across .NET repos
- Find what endpoints/services are affected by a change
- Trace call chains from controller to database
- Review cross-repo boundaries
- Audit ambiguous/unresolved dependencies
- Compare architecture between two snapshots (diff)
- Classify breaking changes between two snapshots
- Scope a PR's impact via git diff
- Run a persistent daemon serving multiple repos under one graph
- Find all callers of an HTTP endpoint across repos (`endpoint_callers`)
- Find which services depend on a NuGet package and at what version (`package_dependents`)
- Find HTTP endpoints that write to a specific database table (`table_entry_points`)
- Get a service-to-service HTTP call dependency map (`repo_dependency_matrix`)

## Workflow

### Step 0: Detect tool

**Claude Code (plugin install):** if `mcp__plugin_dotnet-episteme-skills_synopsis__*` tools are visible, use them directly - the plugin already runs the MCP server with persistent state, so skip detection and the CLI steps below entirely. The CLI path remains for every other tool and for one-shot commands (`scan`, `diff`, `breaking-diff`).

**Bash:**
```bash
./skills/dotnet-techne-synopsis/scripts/detect-tool.sh
```

**PowerShell:**
```powershell
.\skills\dotnet-techne-synopsis\scripts\detect-tool.ps1
```

### Step 1: Scan a workspace

```bash
synopsis scan /path/to/workspace -o graph.json
```

This produces `graph.json` containing all nodes (repos, projects, controllers, methods, endpoints, HTTP clients, DB contexts, entities, tables, NuGet packages) and edges (calls, injects, implements, cross-repo, depends-on-package, etc.).

### Step 2: Query the graph

**Blast radius of a symbol:**
```bash
synopsis query symbol --fqn "OrdersController" --blast-radius --graph graph.json
synopsis query symbol --fqn "IOrderRepository" --blast-radius --direction upstream --graph graph.json
```

**Impact analysis:**
```bash
synopsis query impact --node "OrdersController" --direction downstream --graph graph.json --json
synopsis query impact --node "Orders" --direction upstream --graph graph.json --json
```

**Find paths between nodes:**
```bash
synopsis query paths --from "OrdersController" --to "Orders" --graph graph.json --json
```

**Audit ambiguous edges:**
```bash
synopsis query ambiguous --graph graph.json --json
```

### Step 3: Git-aware analysis

Scope analysis to files changed in a PR:
```bash
synopsis git-scan /path/to/workspace --base main --json
```

### Step 4: Diff two scans

Compare architecture before/after a change:
```bash
synopsis diff before.json after.json --json
```

### Step 5: Breaking-change classification

Classify typed breaking changes between two snapshots:
```bash
synopsis breaking-diff before.json after.json --json
synopsis breaking-diff before.json after.json -o report.json
```

Produces typed `BreakingChangeKind` values:
- **Paired changes:** `NugetVersionBump`, `EndpointRouteChange`, `EndpointVerbChange`, `ApiSignatureChange`, `TableRename`
- **Removals:** `PackageRemoved`, `EndpointRemoved`, `ApiRemoved`, `TableRemoved`

Heuristic pairings carry `Ambiguous` certainty; unmatched nodes flow into removal kinds.

### Step 6: MCP daemon mode (multi-repo)

For persistent AI agent integration over multiple repositories. The daemon holds a `CombinedGraph` that merges per-repo scans in memory and persists state to disk.

**stdio (one-shot, single repo):**
```bash
synopsis mcp --root /path/to/workspace
synopsis mcp --graph graph.json
```

**Unix socket daemon (multi-repo, persistent):**
```bash
synopsis mcp --root /path/to/workspace --socket /tmp/synopsis.sock --state-dir ~/.synopsis/workspace
```

**TCP daemon:**
```bash
synopsis mcp --root /path/to/workspace --tcp localhost:5100
```

State is persisted to `--state-dir` and restored on restart. On restart, repos are loaded from disk without re-scanning; use `reindex_all` to force a fresh scan of all known repos.

**Log file (v1.6.0+):** `--log-file <path>` (or env `SYNOPSIS_LOG_FILE`) appends UTC-timestamped diagnostics to a file in addition to stderr, so external monitors can tail daemon activity. Older binaries ignore the flag.

**Async startup scan (v1.6.0+):** with `--root`, the server answers `initialize` immediately and scans in the background - graph tools return an "indexing in progress" message until the first scan lands (state-dir-hydrated repos serve queries right away); `scan_stats` reports `indexing.inProgress`/`startedAtUtc`/`error`.

## Quick Reference

```bash
# === One-shot scan and query ===
synopsis scan /workspace -o graph.json                              # Scan
synopsis query symbol --fqn "OrdersController" --blast-radius       # Blast radius
synopsis query impact --node "Orders" --direction upstream --json   # Upstream impact
synopsis git-scan /workspace --base main --json                     # PR impact
synopsis breaking-diff before.json after.json --json                # Breaking changes

# === Export formats ===
synopsis export json /workspace -o graph.json
synopsis export csv /workspace -o output/
synopsis export jsonl /workspace -o graph.jsonl

# === Daemon (multi-repo) ===
synopsis mcp --root /workspace --socket /tmp/synopsis.sock --state-dir ~/.synopsis/ws

# === All commands support --json for machine-readable output ===
synopsis scan /workspace --json
synopsis query impact --node X --json
```

## Output Contract

When `--json` is used, stdout contains a single JSON envelope:
```json
{"command":"query impact","ok":true,"result":{...},"ms":142,"schemaVersion":1}
```

`schemaVersion` identifies the envelope contract (bumps only on a breaking shape change). All diagnostics and progress go to stderr. stdout is always machine-readable when `--json` is specified.

## MCP Tools Available

When running in MCP mode (`synopsis mcp`), the following tools are exposed:

| Tool | Description |
|---|---|
| `blast_radius` | Upstream/downstream impact subgraph for a symbol |
| `find_paths` | All paths between two nodes |
| `list_endpoints` | HTTP endpoints filtered by project/verb |
| `list_nodes` | Nodes filtered by type/project/query |
| `node_detail` | Single node with all incoming/outgoing edges |
| `db_lineage` | EF Core entity-to-table lineage chain |
| `cross_repo_edges` | All cross-repository boundary edges |
| `ambiguous_review` | Unresolved and ambiguous edge audit |
| `scan_stats` | Scan statistics and metadata |
| `breaking_diff` | Classify breaking changes between two graph snapshots |
| `endpoint_callers` | All callers of an HTTP endpoint across repos, with certainty |
| `package_dependents` | All repos/projects that depend on a NuGet package, with versions |
| `table_entry_points` | HTTP endpoints that eventually read or write a database table |
| `repo_dependency_matrix` | Per-repo outbound call counts and resolved cross-repo dependency pairs |
| `list_repositories` | List all repos in the CombinedGraph with scan metadata |
| `reindex_repository` | Re-scan a single repository and update the graph |
| `reindex_all` | Re-scan all known repositories |

## HTTP Cross-Service Resolution

Synopsis traces HTTP calls across microservice boundaries. For best resolution accuracy:

- **Use `IHttpClientFactory` with named clients** — the client name is the strongest signal for matching
- **Put base URLs in appsettings with descriptive keys** — `Services:CatalogApi:BaseUrl` not generic `ApiUrl`
- **Name repos and projects consistently** — `CatalogClient` auto-matches repo `catalog-api` and project `Catalog.Api`

See [http-resolution.md](http-resolution.md) for the full guide on supported patterns, appsettings configuration, service-affinity matching, certainty levels, and recommendations.

## Notes

- Synopsis uses Roslyn MSBuildWorkspace for semantic analysis — it understands DI registration, interface dispatch, call graphs, and EF Core mappings
- The tool targets .NET Core/.NET 5+ projects only (no .NET Framework 4.x support)
- First scan of a large workspace takes 15–60s; subsequent queries on a loaded `graph.json` are instant
- MCP daemon mode scans once at startup (or on `reindex_*` calls), then serves queries with no re-scan overhead
- NuGet packages are first-class graph nodes (`Package` type, `DependsOnPackage` edges) from v1.4.0
- Graph node IDs are SHA256-based and stable across scans of the same codebase
