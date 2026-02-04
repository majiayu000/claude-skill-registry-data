---
name: cidx
description: Code search and intelligence using CIDX. Use when searching codebases, finding implementations, tracing call graphs, analyzing dependencies, or searching git history. Preferred over grep/find for all code exploration.
---

# CIDX - Semantic Code Search and Intelligence

Comprehensive CIDX (Code Indexer) documentation for AI coding assistants.

## INDEX MANAGEMENT - CRITICAL FIRST STEP

**Before querying, verify indexes exist**. Queries fail or return empty results without proper indexes.

### Check Index Status

```bash
cidx status                  # Semantic/FTS index status (shows indexed files, last update)
cidx scip status             # SCIP indexes per project (shows SUCCESS/FAILED/PENDING)
cidx scip status -v          # Detailed status with error messages
```

**Status interpretation**:
- **Semantic/FTS**: Shows file count, languages, last indexed time
- **SCIP SUCCESS**: Project indexed successfully, queries will work
- **SCIP FAILED**: Generation failed (check -v for errors, fix issues, rebuild)
- **SCIP PENDING**: Not yet generated (run `cidx scip generate`)
- **SCIP LIMBO**: Partial success (some projects succeeded, some failed)

### Create Indexes

```bash
# Semantic + FTS indexes (required for cidx query)
cidx init                    # Initialize .code-indexer/ in project
cidx index                   # Index current codebase
cidx index --index-commits   # Also index git history (enables temporal search)

# SCIP indexes (required for cidx scip commands)
cidx scip generate           # Generate SCIP indexes for all discovered projects
cidx scip generate --project backend/  # Generate only for specific project
```

### Re-index / Update Indexes

```bash
# Semantic/FTS re-indexing
cidx index                   # Re-indexes changed files (incremental)
cidx index --force           # Full re-index (ignores cache)

# SCIP re-indexing
cidx scip rebuild PROJECT    # Rebuild specific project
cidx scip rebuild --failed   # Rebuild all failed projects
cidx scip rebuild --force PROJECT  # Force rebuild even if succeeded
```

### Supported Languages

**Semantic/FTS**: All text-based source files (auto-detected)

**SCIP** (requires language-specific tooling):
| Language | Project Marker | Requirement |
|----------|----------------|-------------|
| Java | pom.xml | Maven |
| TypeScript | package.json | npm/yarn |
| Python | pyproject.toml | Poetry |
| Kotlin | build.gradle.kts | Gradle |
| C# | *.sln, *.csproj | .NET SDK 8.0+ |
| Go | go.mod | Go SDK 1.18+ |

---

## SEMANTIC SEARCH - MANDATORY FIRST ACTION

**CIDX FIRST**: Always use `cidx query` before grep/find/rg for semantic searches.

**Decision Rule**:
- "What code does", "Where is X implemented" → CIDX semantic (default)
- Exact text (identifiers, function names) → `--fts`
- Pattern matching (regex) → `--fts --regex` (10-50x faster than grep)
- CIDX unavailable → grep/find (fallback only)

**Key Flags**: `--limit N` (default 10, start with 5-10 to conserve context) | `--language python` | `--path-filter */tests/*` | `--exclude-path PATTERN` | `--exclude-language LANG` | `--min-score 0.8` | `--accuracy high` | `--quiet`

**Context Conservation**: Start with low `--limit` values (5-10) on initial queries. High limits consume context window rapidly when results contain large code files.

**Example**: `cidx query "authentication" --language python --exclude-path "*/tests/*" --limit 5 --quiet`

---

## FULL-TEXT SEARCH (FTS)

**Use For**: Exact names, identifiers, TODO comments, typo debugging.

**Flags**: `--fts` | `--case-sensitive` | `--fuzzy` | `--edit-distance N` | `--snippet-lines N`

**Example**: `cidx query "authenticate_user" --fts --case-sensitive --quiet`

**Hybrid**: `--fts --semantic` runs both in parallel.

---

## REGEX MODE (Grep Replacement)

**Flags**: `--fts --regex` | Incompatible with `--semantic` and `--fuzzy`

**Token-Based**: Matches individual tokens only.
- Works: `def`, `login.*`, `test_.*`
- Doesn't work: `def\s+\w+` (whitespace removed)

**Example**: `cidx query "def.*auth" --fts --regex --language python --quiet`

**Fallback**: Use grep only when CIDX unavailable.

---

## TEMPORAL SEARCH (Git History)

**Use For**: Code archaeology, commit message search, bug history, feature evolution.

**Prerequisite**: `cidx index --index-commits` (indexes git history)

**Flags**: `--time-range-all` | `--time-range YYYY-MM-DD..YYYY-MM-DD` | `--chunk-type commit_message` | `--chunk-type commit_diff` | `--author EMAIL`

**Examples**:
- When added: `cidx query "JWT auth" --time-range-all --quiet`
- Bug history: `cidx query "database bug" --time-range-all --chunk-type commit_message --quiet`
- Author work: `cidx query "refactor" --time-range-all --author "dev@company.com" --quiet`

**Indexing Options**: `--all-branches` | `--max-commits N` | `--since-date YYYY-MM-DD`

---

## SCIP CALL GRAPH AND DEPENDENCY ANALYSIS

CIDX provides precise code intelligence via SCIP (Source Code Intelligence Protocol) indexes.

**Prerequisite**: `cidx scip generate` (generates SCIP indexes)

**For complete SCIP documentation**: See reference/scip-intelligence.md

**Quick reference - SCIP commands**:
- `cidx scip definition SYMBOL` - Find where a symbol is defined
- `cidx scip references SYMBOL` - Find all references to a symbol
- `cidx scip dependencies SYMBOL` - Get symbols this symbol depends on
- `cidx scip dependents SYMBOL` - Get symbols that depend on this symbol
- `cidx scip callchain FROM TO` - Trace call chains between symbols
- `cidx scip context SYMBOL` - Get smart context (curated file list)
- `cidx scip impact SYMBOL` - Analyze change impact

**Common options**: `--limit N` | `--exact` | `--project PATH` | `--depth N`

---

## REFERENCE DOCUMENTATION

Detailed documentation available in reference/ directory:
- reference/semantic-search.md - Semantic search flags and patterns
- reference/fts-search.md - Full-text search, regex, fuzzy modes
- reference/temporal-search.md - Git history search guide
- reference/scip-intelligence.md - Complete SCIP call graph and dependency analysis guide
