---
name: cqs
description: "Unified cqs CLI dispatcher — semantic code search, call graph navigation, impact analysis, quality tools, notes, and infrastructure. Use `/cqs <command> [args]` for any cqs operation."
disable-model-invocation: false
argument-hint: "<command> [args...]"
---

# cqs — Unified CLI Dispatcher

Parse the first argument as the command name, pass remaining arguments as flags.

Run via Bash: `cqs <command> <args> --json 2>/dev/null`

`-q/--quiet` exists ONLY on top-level search (`cqs "query" -q`) — subcommands reject it. Use `2>/dev/null` to suppress tracing noise instead.

Present results to the user.

---

## Search & Discovery

### search `<query>` — Semantic code search
Finds functions by concept, not text. Use instead of grep/glob. Default path is dense cosine + SPLADE sparse fusion with per-category routing (RRF keyword fusion is opt-in via `--rrf`).

```
cqs "<query>" [flags] --json -q
```

| Flag | Description |
|------|-------------|
| `-l/--lang <L>` | Filter by language (rust, python, typescript, javascript, go, c, java, sql, markdown) |
| `-n/--limit <N>` | Max results (default 5; `--limit 0` rejected) |
| `-t/--threshold <N>` | Similarity threshold (default 0.3) |
| `--name-only` | Definition lookup, skips embedding |
| `--rrf` | Enable RRF hybrid search (keyword + semantic fusion); off by default |
| `--splade` / `--splade-alpha <F>` | Force SPLADE on for unknown-category queries / pin fusion weight (1.0 = pure cosine) |
| `--reranker <none\|onnx>` | Cross-encoder re-ranking (default none; opt-in, measured net-negative on the standing eval) |
| `--include-docs` | Include markdown/config chunks (default: code only) |
| `--no-demote` | Disable demotion of test functions and underscore-prefixed names |
| `-p/--path <glob>` | Path pattern filter (e.g., `src/cli/**`) |
| `--include-type <T>` | Include only: function, method, class, struct, test, endpoint, etc. |
| `--exclude-type <T>` | Exclude: test, variable, configkey, etc. |
| `--pattern <P>` | Pattern: builder, error_swallow, async, mutex, unsafe, recursion |
| `--name-boost <F>` | Weight for name matching in hybrid search 0.0-1.0 (default 0.2) |
| `--ref <name>` | Search only this reference index (`--include-refs` to merge refs in) |
| `--tokens <N>` | Token budget (greedy knapsack by score) |
| `--expand-parent` | Parent type/module context (small-to-big retrieval) |
| `-C/--context <N>` | Lines of context around chunk |
| `--no-content` | File:line only, no code |
| `--no-stale-check` | Skip per-file staleness checks |
| `--model <M>` | Query embedder override (embeddinggemma-300m default) |

### similar `<function>` — Find similar code
Find code similar to a given function. Refactoring discovery, duplicates.

```
cqs similar "<name>" --json
```

### gather `<query>` — Smart context assembly
Seed search + BFS call graph expansion. "Show me everything related to X."

```
cqs gather "<query>" [flags] --json 2>/dev/null
```

| Flag | Description |
|------|-------------|
| `-d/--depth <N>` (alias `--expand`) | BFS depth (default 1, max 5) |
| `--direction <D>` | both, callers, callees (default both) |
| `-n/--limit <N>` | Max seed results (default 5) |
| `--tokens <N>` | Token budget |
| `--ref <name>` | Cross-index: seed from reference, bridge into project |

### where `<description>` — Placement suggestion
Where to add new code based on semantic similarity and local patterns.

```
cqs where "<description>" --json
```

### scout `<task>` — Pre-investigation dashboard
Search + callers/tests + staleness + notes in one call. First step for new tasks.

```
cqs scout "<task>" [-n N] [--tokens N] --json 2>/dev/null
```

### task `<description>` — Implementation brief
Scout + gather + impact + placement + notes. Waterfall token budgeting (scout 15%, code 50%, impact 15%, placement 10%, notes 10%).

```
cqs task "<description>" [-n N] [--tokens N] --json 2>/dev/null
```

### onboard `<concept>` — Guided codebase tour
Entry point + call chain + callers + types + tests. Ordered reading list.

```
cqs onboard "<concept>" [-d/--depth N] [--tokens N] --json 2>/dev/null
```

### read `<path>` — File with contextual notes
File contents with notes injected as comments. Richer than raw Read.

```
cqs read <path> [--focus <function>] --json
```

`--focus <function>` returns only the target function + type dependencies.

### context `<file>` — Module overview
Chunks, callers, callees, notes for a file.

```
cqs context <file> --json
```

### explain `<function>` — Function card
Signature, docs, callers, callees, similar in one call.

```
cqs explain "<name>" --json
```

---

## Call Graph

### callers `<function>` — Who calls this?
```
cqs callers "<name>" --json
```

### callees `<function>` — What does this call?
```
cqs callees "<name>" --json
```

### trace `<source>` `<target>` — Shortest call path
BFS shortest path between two functions.

```
cqs trace "<source>" "<target>" --json
```

### deps `<name>` — Type dependencies
Forward: who uses this type? Reverse (`--reverse`): what types does this function use?

```
cqs deps "<name>" [--reverse] --json
```

### related `<function>` — Co-occurrence
Functions sharing callers, callees, or types.

```
cqs related "<name>" --json
```

### impact `<function>` — What breaks if you change X?
Callers with snippets + affected tests via reverse BFS.

```
cqs impact "<name>" [--depth N] [--suggest-tests] --json
```

### impact-diff — Diff-aware impact analysis
Changed functions, affected callers, tests to re-run.

```
cqs impact-diff [--base <ref>] [--stdin] [--json] [--tokens N]
```

### test-map `<function>` — Map function to tests
Tests that exercise a function via reverse call graph.

```
cqs test-map "<name>" --json
```

---

## Quality & Review

### dead — Find dead code
Functions/methods with no callers.

```
cqs dead [--include-pub] [--min-confidence low|medium|high] --json
```

### stale — Index freshness
Files modified since last index.

```
cqs stale --json
```

### health — Codebase quality snapshot
Stats + dead code + staleness + hotspots + untested hotspots + notes.

```
cqs health [--json]
```

### ci — CI pipeline analysis
Review + dead code + gate logic. Exit 3 on gate fail.

```
cqs ci [--base <ref>] [--stdin] [--gate high|medium|off] [--json] [--tokens N]
```

### review — Comprehensive diff review
Impact + notes + risk scoring + staleness. More detailed than `ci` (no gate).

```
cqs review [--base <ref>] [--stdin] [--json] [--tokens N]
```

### suggest — Auto-suggest notes
Scan for dead code clusters, untested hotspots, high-risk functions.

```
cqs suggest [--apply] [--json]
```

### gc — Garbage-collect the index
Removes stale chunks and rebuilds the vector index. MUTATING — not a report-only command.

```
cqs gc --json
```

### stats — Index statistics
Chunk counts, languages, last update.

```
cqs stats --json
```

---

## Notes

### notes add `<text>` — Add a note
```
cqs notes add "<text>" [--sentiment N] [--mentions a,b,c]
```

Sentiment: -1 (serious pain), -0.5 (notable pain), 0 (neutral), 0.5 (notable gain), 1 (major win).

### notes update `<exact text>` — Update a note
```
cqs notes update "<exact text>" [--new-text "..."] [--new-sentiment N]
```

### notes remove `<exact text>` — Remove a note
```
cqs notes remove "<exact text>"
```

### audit-mode — Toggle audit mode
Excludes notes from search/read for unbiased review.

```
cqs audit-mode [on|off] [--expires 30m] --json
```

---

## Infrastructure

### ref — Reference index management
Manage external codebases for multi-index search.

| Subcommand | Usage |
|------------|-------|
| `ref add <name> <path> [--weight 0.8]` | Index external codebase (weight 0.0-1.0) |
| `ref list` | Show all references |
| `ref update <name>` | Re-index reference |
| `ref remove <name>` | Delete reference |

### watch — File watcher / daemon
Keep index fresh automatically. `--serve` also answers daemon queries over the socket (3-19ms vs ~2s CLI startup); the systemd service runs `cqs watch --serve`.

```
cqs watch [--debounce <ms>] [--no-ignore] [--poll] [--serve]
```

### Daemon & index plumbing

| Command | Usage |
|---------|-------|
| `ping` | Daemon healthcheck — model, uptime, counters (`cqs ping --json`) |
| `status` | Watch-mode freshness — is the index caught up (`cqs status --json`) |
| `refresh` | Invalidate daemon caches, re-open the Store |
| `slot list/create/promote/remove/active` | Named side-by-side indexes under `.cqs/slots/<name>/`; `--slot <name>` on most commands |
| `cache stats/prune/compact` | Embeddings cache at `.cqs/embeddings_cache.db` |
| `model show/list/swap` | Embedding model recorded in the index |
| `eval <query_file>` | R@K eval harness (`cqs eval evals/queries/v3_test.v2.json --json`) |
| `telemetry` | Usage dashboard — command frequency, categories, sessions |
| `doctor [--fix]` | Check model, index, hardware |

### convert `<path>` — Document conversion
PDF/HTML/CHM/MD to cleaned Markdown.

```
cqs convert <path> [--output <dir>] [--overwrite] [--dry-run] [--clean-tags <tags>]
```

Tags: `aveva`, `pdf`, `generic`.

### diff `<source>` — Semantic diff
Compare indexed snapshots. Requires references via `ref add`.

```
cqs diff "<source>" [target] [--threshold F] [--lang L] --json
```

### drift `<reference>` — Semantic drift detection
Embedding distance between same-named functions across snapshots.

```
cqs drift "<ref>" [--min-drift 0.1] [--lang L] [--limit N] --json
```
