---
name: surrealdb
description: "Expert SurrealDB 3 architect and developer skill (tracks v3.1.4+). SurrealQL mastery, multi-model data modeling (document, graph, vector, time-series, geospatial), schema design, security, deployment, performance tuning, SDK integration (JS, Python, Go, Rust, Java, .NET, C, PHP, Swift, Kotlin, Ruby), Surrealism WASM extensions, SurrealML scope coverage (preview), built-in MCP (v3.1+) and standalone SurrealMCP, LangChain Python integration, editor tooling (LSP v0.1.6, tree-sitter, CodeMirror v1.0.6, VS Code/JetBrains/Neovim/Zed), and ecosystem integrations (Surrealist v3.9, Surreal-Sync, SurrealFS, SurrealKit v0.7, n8n, Agent Skills, setup-surreal). Universal skill for 30+ AI agents."
version: "1.7.1"
license: MIT
metadata:
  version: "1.7.1"
  author: "24601"
  snapshot_date: "2026-06-17"
  repository: "https://github.com/24601/surreal-skills"
  openclaw:
    requires:
      env:
        - SURREAL_ENDPOINT
        - SURREAL_USER
        - SURREAL_PASS
        - SURREAL_NS
        - SURREAL_DB
      bins:
        - surreal
        - python3
        - uv
    primaryEnv: SURREAL_PASS
    homepage: "https://github.com/24601/surreal-skills"
    always: false
    install:
      - kind: brew
        formula: surrealdb/tap/surreal
        bins: [surreal]
      - kind: brew
        formula: uv
        bins: [uv]
requires:
  binaries:
    - name: surreal
      install: "brew install surrealdb/tap/surreal"
      purpose: "SurrealDB CLI for server management, SQL REPL, import/export"
      optional: false
    - name: python3
      version: ">=3.10"
      purpose: "Required for skill scripts (doctor.py, schema.py, onboard.py)"
      optional: false
    - name: uv
      install: "brew install uv"
      purpose: "PEP 723 script runner -- installs script deps automatically"
      optional: false
    - name: docker
      purpose: "Containerized SurrealDB instances"
      optional: true
    - name: gh
      install: "brew install gh"
      purpose: "GitHub CLI -- used only by check_upstream.py for comparing upstream repo SHAs"
      optional: true
  env_vars:
    - name: SURREAL_ENDPOINT
      purpose: "SurrealDB server URL"
      default: "http://localhost:8000"
      sensitive: false
    - name: SURREAL_USER
      purpose: "Authentication username"
      default: "root"
      sensitive: true
    - name: SURREAL_PASS
      purpose: "Authentication password"
      default: "root"
      sensitive: true
    - name: SURREAL_NS
      purpose: "Default namespace"
      default: "test"
      sensitive: false
    - name: SURREAL_DB
      purpose: "Default database"
      default: "test"
      sensitive: false
security:
  no_network: false
  no_network_note: "doctor.py and schema.py connect to a user-specified SurrealDB endpoint (WebSocket) for health checks and schema introspection. check_upstream.py calls GitHub API via gh CLI to compare upstream repo SHAs. No other third-party network calls."
  no_credentials: false
  no_credentials_note: "Scripts accept SURREAL_USER/SURREAL_PASS for DB authentication. No credentials are stored in the skill itself."
  no_env_write: true
  no_file_write: false
  no_file_write_note: "schema.py can write exported schema files when --output-dir is set. onboard.py can write a local .env file during interactive setup if the user explicitly confirms."
  no_shell_exec: false
  no_shell_exec_note: "Scripts invoke surreal CLI and gh for health checks."
  scripts_auditable: true
  scripts_use_pep723: true
  no_obfuscated_code: true
  no_binary_blobs: true
  no_minified_scripts: true
  no_curl_pipe_sh: true
---

# SurrealDB 3 Skill

Expert-level SurrealDB 3 architecture, development, and operations. Covers SurrealQL, multi-model data modeling, graph traversal, vector search, security, deployment, performance tuning, SDK integration, and the wider SurrealDB ecosystem, including SurrealKit, SurrealMCP, n8n, CodeMirror, and agent-skill surfaces.

## For AI Agents

Get a full capabilities manifest, decision trees, and output contracts:

```bash
uv run {baseDir}/scripts/onboard.py --agent
```

See [AGENTS.md]({baseDir}/AGENTS.md) for the complete structured briefing.

| Command | What It Does |
|---------|-------------|
| `uv run {baseDir}/scripts/doctor.py` | Health check: verify surreal CLI, connectivity, versions |
| `uv run {baseDir}/scripts/doctor.py --check` | Quick pass/fail check (exit code only) |
| `uv run {baseDir}/scripts/schema.py introspect` | Dump full schema of a running SurrealDB instance |
| `uv run {baseDir}/scripts/schema.py tables` | List all tables with field counts and indexes |
| `uv run {baseDir}/scripts/onboard.py --agent` | JSON capabilities manifest for agent integration |

## Prerequisites

- **surreal CLI** -- `brew install surrealdb/tap/surreal` (macOS) or see [install docs](https://surrealdb.com/docs/surrealdb/installation)
- **Python 3.10+** -- Required for skill scripts
- **uv** -- `brew install uv` (macOS) or `pip install uv` or see [uv docs](https://docs.astral.sh/uv/getting-started/installation/)

Optional:

- **Docker** -- For containerized SurrealDB instances (`docker run surrealdb/surrealdb:v3`)
- **SDK of choice** -- JavaScript, Python, Go, Rust, Java, Kotlin, .NET, C, PHP, Swift, or Ruby

> **Security note**: This skill documents package-manager and container installs
> only. Prefer auditable installs through Homebrew, apt/dnf, Cargo, npm, or
> Docker rather than remote one-line shell installers.

## Quick Start

> **Credential warning**: Examples below use `root/root` for **local development
> only**. Never use default credentials against production or shared instances.
> Create scoped, least-privilege users for non-local environments.

```bash
# Start SurrealDB in-memory for LOCAL DEVELOPMENT ONLY
surreal start memory --user root --pass root --bind 127.0.0.1:8000

# Start with persistent RocksDB storage (local dev)
surreal start rocksdb://data/mydb.db --user root --pass root

# Start with SurrealKV (time-travel queries supported, local dev)
surreal start surrealkv://data/mydb --user root --pass root

# Connect via CLI REPL (local dev)
surreal sql --endpoint http://localhost:8000 --user root --pass root --ns test --db test

# Import a SurrealQL file
surreal import --endpoint http://localhost:8000 --user root --pass root --ns test --db test schema.surql

# Export the database
surreal export --endpoint http://localhost:8000 --user root --pass root --ns test --db test backup.surql

# Check version
surreal version

# Run the skill health check
uv run {baseDir}/scripts/doctor.py
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SURREAL_ENDPOINT` | SurrealDB server URL | `http://localhost:8000` |
| `SURREAL_USER` | Root or namespace username | `root` |
| `SURREAL_PASS` | Root or namespace password | `root` |
| `SURREAL_NS` | Default namespace | `test` |
| `SURREAL_DB` | Default database | `test` |

These map directly to the `surreal sql` CLI flags (`--endpoint`, `--user`, `--pass`, `--ns`, `--db`) and are recognized by official SurrealDB SDKs.

## Core Capabilities

### SurrealQL Mastery

Full coverage of the SurrealQL query language: `CREATE`, `SELECT`, `UPDATE`, `UPSERT`, `DELETE`, `RELATE`, `INSERT`, `LIVE SELECT`, `DEFINE`, `REMOVE`, `INFO`, subqueries, transactions, futures, and all built-in functions (array, crypto, duration, geo, math, meta, object, parse, rand, string, time, type, vector).

See: `rules/surrealql.md`

### Multi-Model Data Modeling

Design schemas that leverage SurrealDB's multi-model capabilities -- document collections, graph edges, relational references, vector embeddings, time-series data, and geospatial coordinates -- all in a single database with a single query language.

See: `rules/data-modeling.md`

### Graph Queries

First-class graph traversal without JOINs. `RELATE` creates typed edges between records. Traverse with `->` (outgoing), `<-` (incoming), and `<->` (bidirectional) operators. Filter, aggregate, and recurse at any depth.

See: `rules/graph-queries.md`

### Vector Search

Built-in vector similarity search using HNSW indexes (the v3 vector index type; brute-force is available as a fallback during index build/rebuild). Define vector fields, create indexes with configurable distance metrics (cosine, euclidean, manhattan, minkowski), and query with `vector::similarity::*` functions. Build RAG pipelines and semantic search directly in SurrealQL.

See: `rules/vector-search.md`

### Security and Permissions

Row-level security via `DEFINE TABLE ... PERMISSIONS`, namespace/database/record-level access control, `DEFINE ACCESS` for JWT/token-based auth, `DEFINE USER` for system users, and `$auth`/`$session` runtime variables for permission predicates.

See: `rules/security.md`

### Deployment and Operations

Single-binary deployment, Docker, Kubernetes (Helm charts), storage engine selection (memory, RocksDB, SurrealKV, TiKV for distributed), backup/restore, monitoring, and production hardening.

See: `rules/deployment.md`

### Performance Tuning

Index strategies (unique, search, vector HNSW), query optimization with `EXPLAIN`, connection pooling, storage engine trade-offs, batch operations, and resource limits.

See: `rules/performance.md`

### SDK Integration

Official SDKs for JavaScript/TypeScript (Node.js, Deno, Bun, browser), Python, Go, Rust, Java, Kotlin, .NET, C, PHP, Swift (iOS/macOS/visionOS), and Ruby. Includes the source-only C binding, Python v3 unreleased API boundary, .NET v0.10.2 beta surface, connection protocols, authentication flows, live query subscriptions, and typed record handling.

See: `rules/sdks.md`

### Surrealism WASM Extensions

New in SurrealDB 3: extend the database with custom functions, analyzers, and logic written in Rust and compiled to WASM. Define, deploy, and manage Surrealism modules.

See: `rules/surrealism.md`

### SurrealML In-Database Inference (preview / unstable)

`surrealml` has a GitHub `v0.1.2` release, but PyPI still exposes `surrealml` 0.0.4 as the latest package as of this snapshot. The `.surml` artifact format and `[sklearn]`, `[torch]`, `[tensorflow]` extras are the stable documented boundary. The v1.4.0 documentation for `DEFINE MODEL`, `INFO FOR MODEL`, `REMOVE MODEL`, `ml::name<version>(...)`, `surreal ml import`, `db.upload_ml(...)`, and the `SurMlFile.from_<framework>(...)` factory methods was retracted in v1.4.1. The current Python setup path downloads native libraries from GitHub Releases unless `LOCAL_BUILD=TRUE`, so pin and audit before production use.

See: `rules/surrealml.md`

### SurrealMCP -- Model Context Protocol Server

The official MCP server (`surrealdb/surrealmcp`) lets MCP-compatible AI hosts (Claude Desktop, Cursor, GitHub Copilot in VS Code, Zed, n8n) read and write SurrealDB through one configuration entry. Install from source (`cargo install --path .`) or Docker; not on crates.io or npm. Binary requires `start` subcommand. Tool wire-names are snake_case: `query`, `select`, `insert`, `create`, `upsert`, `update`, `delete`, `relate`, `connect_endpoint`, `use_namespace`, `use_database`, `list_namespaces`, `list_databases`, `disconnect_endpoint`, plus cloud tools.

See: `rules/surrealmcp.md`, `skills/surrealmcp/SKILL.md`

### Editor Tooling

`surrealql-language-server` v0.1.3 is the first-party LSP baseline; `surql-lsp` v0.1.1 remains a separate community crate. The rule tracks tree-sitter, first-party editor extensions, and `@surrealdb/codemirror` / `@surrealdb/lezer` v1.0.5 for custom web editors. Per-extension command palettes and settings still need each extension README as source of truth.

See: `rules/editor-tooling.md`

### LangChain Integration (Python only)

`langchain-surrealdb` 0.2.1 (Python; `langchain-core ~= 1.1.0`, `surrealdb ~= 1.0.8` v1 SDK) exposes SurrealDB as a vector store via constructor `SurrealDBVectorStore(embeddings, conn)`. JS package, async class, chat history, and hybrid retriever from v1.4.0 were retracted in v1.4.1.

See: `rules/langchain.md`

### Ecosystem Integrations

Official-docs and first-party-adjacent surfaces that are not full dedicated rules yet: `@surrealdb/n8n-nodes-surrealdb` v0.6.0 for self-hosted n8n, the official AI framework docs index, Spectron / Agent Memory Context as roadmap-only, CodeMirror packages, and the official `surrealdb/agent-skills` repo. Use this rule to avoid presenting roadmap or pointer pages as production APIs.

See: `rules/ecosystem-integrations.md`

### Ecosystem Tools

- **Surrealist** -- Official IDE and GUI for SurrealDB (schema designer, query editor, graph visualizer)
- **Surreal-Sync** -- Change Data Capture (CDC) for migrations from other databases
- **SurrealFS** -- AI agent filesystem built on SurrealDB
- **SurrealKit** -- Desired-state schema sync, rollout-based migrations, seeding, and declarative tests
- **SurrealML** -- Preview-stage `.surml` artifact tooling; server invocation surface still unstable
- **SurrealMCP** -- Model Context Protocol server for AI agents
- **n8n** -- Official scoped community package for self-hosted n8n workflows
- **CodeMirror** -- Official SurrealQL syntax packages for custom editors
- **setup-surreal** -- Official GitHub Action (`surrealdb/setup-surreal@v2`) for running SurrealDB in CI workflows. Not a CLI bootstrap (the v1.4.0 documentation that described it as one was retracted in v1.4.2)

See: `rules/surrealist.md`, `rules/surreal-sync.md`, `rules/surrealfs.md`, `rules/surrealkit.md`, `rules/surrealml.md`, `rules/surrealmcp.md`, `rules/ecosystem-integrations.md`, `rules/deployment.md` (setup-surreal section)

## Doctor / Health Check

```bash
# Full diagnostic (Rich output on stderr, JSON on stdout)
uv run {baseDir}/scripts/doctor.py

# Quick check (exit code 0 = healthy, 1 = issues found)
uv run {baseDir}/scripts/doctor.py --check

# Check a specific endpoint
uv run {baseDir}/scripts/doctor.py --endpoint http://my-server:8000
```

The doctor script verifies: surreal CLI installed and on PATH, server reachable, authentication succeeds, namespace and database exist, version compatibility, and storage engine status.

## Schema Introspection

```bash
# Full schema dump (all tables, fields, indexes, events, accesses)
uv run {baseDir}/scripts/schema.py introspect

# List tables with summary
uv run {baseDir}/scripts/schema.py tables

# Inspect a specific table
uv run {baseDir}/scripts/schema.py table <table_name>

# Export schema as SurrealQL (reproducible DEFINE statements)
uv run {baseDir}/scripts/schema.py export --format surql

# Export schema as JSON
uv run {baseDir}/scripts/schema.py export --format json
```

Introspection uses `INFO FOR DB`, `INFO FOR TABLE`, and `INFO FOR NS` to reconstruct the full schema.

## Rules Reference

| Rule File | Coverage |
|-----------|----------|
| `rules/surrealql.md` | SurrealQL syntax, statements, functions, operators, idioms |
| `rules/data-modeling.md` | Schema design, record IDs, field types, relations, normalization |
| `rules/graph-queries.md` | RELATE, graph traversal operators, path expressions, recursive queries |
| `rules/vector-search.md` | Vector fields, HNSW indexes (the v3 vector index type), similarity functions, RAG patterns |
| `rules/security.md` | Permissions, access control, authentication, JWT, row-level security |
| `rules/deployment.md` | Installation, storage engines, Docker, Kubernetes, production config; `surrealdb/setup-surreal@v2` GitHub Action (CI-only; not a CLI bootstrap) |
| `rules/performance.md` | Indexes, EXPLAIN, query optimization, batch ops, resource tuning |
| `rules/sdks.md` | JS/TS, Python, Go, Rust, Java, Kotlin, .NET, C, PHP, Swift, Ruby SDK usage, connection patterns, live queries |
| `rules/surrealism.md` | WASM extensions, custom functions, Surrealism module authoring |
| `rules/surrealml.md` | SurrealML preview scope, .surml artifacts, package/release boundaries, native dependency warning |
| `rules/surrealmcp.md` | Model Context Protocol server: tool catalog, host configuration, transports, deployment |
| `rules/editor-tooling.md` | LSP, tree-sitter grammar, CodeMirror, VS Code / JetBrains / Neovim / Helix / Sublime / Zed extensions |
| `rules/langchain.md` | LangChain Python integration: vector store, constructor API, custom_filter boundary |
| `rules/ecosystem-integrations.md` | n8n, AI framework docs index, Spectron roadmap boundary, CodeMirror, official Agent Skills repo |
| `rules/surrealist.md` | Surrealist IDE/GUI usage, schema designer, query editor |
| `rules/surreal-sync.md` | CDC migration tool, source/target connectors, migration workflows |
| `rules/surrealfs.md` | AI agent filesystem, file storage, metadata, retrieval patterns |
| `rules/surrealkit.md` | Desired-state schema sync, rollout-based migrations, seeding, and declarative DB testing |
| `rules/gotchas.md` | Cross-domain edge cases and footguns: upgrade, graph, vector, security, MCP, SDKs (v3.1.4+) |

## Workflow Examples

> **All workflow examples use `root/root` for local development only.**
> For production, use `DEFINE USER` with scoped, least-privilege credentials.

### New Project Setup

```bash
# 1. Verify environment
uv run {baseDir}/scripts/doctor.py

# 2. Start SurrealDB
surreal start rocksdb://data/myproject.db --user root --pass root

# 3. Design schema (use rules/data-modeling.md for guidance)
# 4. Import initial schema
surreal import --endpoint http://localhost:8000 --user root --pass root \
  --ns myapp --db production schema.surql

# 5. Introspect to verify
uv run {baseDir}/scripts/schema.py introspect
```

### Migration from SurrealDB v2

```bash
# 1. Export v2 data
surreal export --endpoint http://old-server:8000 --user root --pass root \
  --ns myapp --db production v2-backup.surql

# 2. Review breaking changes (see rules/surrealql.md v2->v3 migration section)
# Key changes: range syntax 1..4 is now exclusive of end, new WASM extension system

# 3. Import into v3
surreal import --endpoint http://localhost:8000 --user root --pass root \
  --ns myapp --db production v2-backup.surql

# 4. Verify schema
uv run {baseDir}/scripts/schema.py introspect
```

### Data Modeling for a New Domain

```bash
# 1. Read rules/data-modeling.md for schema design patterns
# 2. Read rules/graph-queries.md if your domain has relationships
# 3. Read rules/vector-search.md if you need semantic search
# 4. Draft schema.surql with DEFINE TABLE, DEFINE FIELD, DEFINE INDEX
# 5. Import and test
surreal import --endpoint http://localhost:8000 --user root --pass root \
  --ns dev --db test schema.surql
uv run {baseDir}/scripts/schema.py introspect
```

### Deploying to Production

```bash
# 1. Read rules/deployment.md for storage engine selection and hardening
# 2. Read rules/security.md for access control setup
# 3. Read rules/performance.md for index strategy
# 4. Run doctor against production endpoint
uv run {baseDir}/scripts/doctor.py --endpoint https://prod-surreal:8000
# 5. Verify schema matches expectations
uv run {baseDir}/scripts/schema.py introspect --endpoint https://prod-surreal:8000
```

## Upstream Source Check

```bash
# Check if upstream SurrealDB repos have changed since this skill was built
uv run {baseDir}/scripts/check_upstream.py

# JSON-only output for agents
uv run {baseDir}/scripts/check_upstream.py --json

# Only show repos that have new commits
uv run {baseDir}/scripts/check_upstream.py --stale
```

Compares current HEAD SHAs and release tags of all tracked repos against the
baselines in `SOURCES.json`. Use this to plan incremental skill updates.

## Source Provenance

This skill was refreshed on **2026-06-17** from these upstream sources:

| Repository | Release | Snapshot Date |
|------------|---------|---------------|
| [surrealdb/surrealdb](https://github.com/surrealdb/surrealdb) | v3.1.4 | 2026-06-10 |
| [surrealdb/surrealist](https://github.com/surrealdb/surrealist) | surrealist-v3.9.0 | 2026-06-16 |
| [surrealdb/surrealdb.js](https://github.com/surrealdb/surrealdb.js) | v2.0.3 | 2026-06-17 |
| [surrealdb/surrealdb.py](https://github.com/surrealdb/surrealdb.py) | v2.0.0 (PyPI); main 3.0.0 unreleased | 2026-06-17 |
| [surrealdb/surrealkit](https://github.com/surrealdb/surrealkit) | v0.7.0 | 2026-06-11 |
| [surrealdb/surrealmcp](https://github.com/surrealdb/surrealmcp) | v0.4.0 standalone; built-in MCP in 3.1+ | 2026-06-17 |

Documentation: [surrealdb.com/docs](https://surrealdb.com/docs) snapshot 2026-06-17.

Machine-readable provenance: `SOURCES.json`.

## Output Convention

All Python scripts in this skill follow a dual-output pattern:

- **stderr**: Rich-formatted human-readable output (tables, panels, status indicators)
- **stdout**: Machine-readable JSON for programmatic consumption by AI agents

This means `2>/dev/null` hides the human output, and piping stdout gives clean JSON for downstream processing.
