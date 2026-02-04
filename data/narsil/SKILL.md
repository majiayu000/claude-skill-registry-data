---
name: narsil
description: Use narsil-mcp code intelligence tools effectively. Use when searching code, finding symbols, analyzing call graphs, scanning for security vulnerabilities, exploring dependencies, or performing static analysis on indexed repositories.
allowed-tools: mcp__narsil-mcp__*
---

# Narsil Code Intelligence

Narsil is an MCP server providing 76 code intelligence tools. This skill helps you use them effectively.

## Critical: Parameter Naming

Use **short parameter names**. These are the most common mistakes:

| Wrong | Correct |
|-------|---------|
| `repo_path` | `repo` |
| `symbol_name` | `symbol` |
| `file_path` | `path` |
| `function_name` | `function` |

The `repo` parameter expects the **repository name** from `list_repos`, not the full filesystem path.

## Getting Started

**Always start with:**
```
list_repos  → See indexed repositories
get_index_status  → See which features are enabled
```

## Feature Requirements

Some tools require specific CLI flags when starting narsil-mcp:

| Feature | Required Flag | Tools |
|---------|--------------|-------|
| Git integration | `--git` | get_blame, get_file_history, get_recent_changes, get_hotspots, get_contributors, get_commit_diff, get_symbol_history, get_branch_info, get_modified_files |
| Call graph | `--call-graph` | get_call_graph, get_callers, get_callees, find_call_path, get_complexity, get_function_hotspots |
| LSP | `--lsp` | Enhanced: get_hover_info, get_type_info, go_to_definition |
| Neural search | `--neural` | neural_search, get_neural_stats |
| Remote repos | `--remote` | add_remote_repo, list_remote_files, get_remote_file |

If a tool returns empty results or errors, check `get_index_status` to verify the feature is enabled.

## Tool Selection Guide

### Finding Code

| Task | Best Tool | When to Use |
|------|-----------|-------------|
| Find files by name | `find_symbols` with `file_pattern` | Know filename pattern |
| Find function/class definitions | `find_symbols` | Know symbol type |
| Search by content | `search_code` | Keyword search |
| BM25-ranked search | `semantic_search` | Better ranking than search_code |
| Semantic code search | `hybrid_search` | Natural language queries (combines BM25 + TF-IDF) |
| Find similar code | `find_similar_code` | Have a code snippet |
| Find code like a symbol | `find_similar_to_symbol` | Find patterns similar to existing function |
| Find code clones | `find_semantic_clones` | Detect duplicate/similar code (Type-3/4 clones) |
| Search AST chunks | `search_chunks` | Want function/class boundaries |
| Fuzzy symbol search | `workspace_symbol_search` | Unsure of exact name |
| AI codebase overview | `explain_codebase` | Quick understanding of unfamiliar repo |
| Find feature location | `find_implementation` | Know feature name, not code location |

### Understanding Code

| Task | Best Tool |
|------|-----------|
| Read a file | `get_file` |
| Read specific lines | `get_excerpt` |
| Get AST chunks for file | `get_chunks` |
| Get function source | `get_symbol_definition` |
| Find all references | `find_references` |
| Find all usages (cross-file) | `find_symbol_usages` |
| See what exports a module has | `get_export_map` |
| Analyze imports/dependencies | `get_dependencies` |
| See what calls a function | `get_callers` |
| See what a function calls | `get_callees` |
| Full call graph | `get_call_graph` |
| Find path between functions | `find_call_path` |
| Function complexity | `get_complexity` |
| Find high-connection functions | `get_function_hotspots` |
| Get type info at position | `get_hover_info` |
| Get precise type info | `get_type_info` |
| Go to definition | `go_to_definition` |

### Security Analysis

| Task | Best Tool |
|------|-----------|
| Full security scan | `scan_security` |
| Security overview | `get_security_summary` |
| OWASP Top 10 check | `check_owasp_top10` |
| CWE Top 25 check | `check_cwe_top25` |
| Find injection flaws | `find_injection_vulnerabilities` |
| Find taint sources | `get_taint_sources` |
| Trace tainted data | `trace_taint` |
| Explain a vulnerability | `explain_vulnerability` |
| Get fix suggestion | `suggest_fix` |
| Check dependencies for CVEs | `check_dependencies` |
| Find upgrade paths | `find_upgrade_path` |
| License compliance | `check_licenses` |
| Generate SBOM | `generate_sbom` |

### Static Analysis

| Task | Best Tool |
|------|-----------|
| Control flow graph | `get_control_flow` |
| Data flow analysis | `get_data_flow` |
| Reaching definitions | `get_reaching_definitions` |
| Find dead code | `find_dead_code` |
| Find dead stores | `find_dead_stores` |
| Find uninitialized vars | `find_uninitialized` |
| Infer types (Python/JS/TS) | `infer_types` |
| Check type errors | `check_type_errors` |
| Taint flow with types | `get_typed_taint_flow` |
| Import dependency graph | `get_import_graph` |
| Find circular imports | `find_circular_imports` |

### Git History (requires --git)

| Task | Best Tool |
|------|-----------|
| Git blame for file | `get_blame` |
| File commit history | `get_file_history` |
| Recent repo changes | `get_recent_changes` |
| High-churn files | `get_hotspots` |
| Contributors to file/repo | `get_contributors` |
| Diff for a commit | `get_commit_diff` |
| Symbol change history | `get_symbol_history` |
| Current branch info | `get_branch_info` |
| Uncommitted changes | `get_modified_files` |

### Utility & Diagnostics

| Task | Best Tool |
|------|-----------|
| List indexed repos | `list_repos` |
| Get project structure | `get_project_structure` |
| Check enabled features | `get_index_status` |
| Force re-index | `reindex` |
| Discover repos in directory | `discover_repos` |
| Validate repo path | `validate_repo` |
| Incremental index status | `get_incremental_status` |
| Performance metrics | `get_metrics` |
| Embedding stats | `get_embedding_stats` |
| Chunk stats | `get_chunk_stats` |

## Common Patterns

### Explore a new codebase
```
1. list_repos → get repo name
2. get_project_structure(repo) → see directory tree
3. find_symbols(repo, symbol_type="function") → see main functions
4. get_import_graph(repo) → understand module structure
```

### Find where something is implemented
```
1. workspace_symbol_search(query="feature name") → find candidates
2. find_symbol_usages(repo, symbol) → see all usages
3. get_symbol_definition(repo, symbol) → read the code
```

### Security audit
```
1. scan_security(repo) → get all findings
2. check_owasp_top10(repo) → check critical vulnerabilities
3. check_dependencies(repo) → find vulnerable dependencies
4. find_injection_vulnerabilities(repo) → focus on injection flaws
5. For each finding: suggest_fix(repo, path, line) → get remediation
```

### Understand a function
```
1. get_symbol_definition(repo, symbol) → read source
2. get_callers(repo, function, transitive=true) → who calls it
3. get_callees(repo, function) → what it calls
4. get_complexity(repo, function) → cyclomatic complexity
5. get_data_flow(repo, path, function) → variable flow
```

## Handling Large Results

For large codebases, use pagination and filtering:

- `max_results` parameter limits output size
- `file_pattern` filters by glob (e.g., `"*.py"`, `"src/**/*.ts"`)
- `severity_threshold` filters security findings (critical, high, medium, low)

## Troubleshooting

**"No repository found"** → Run `list_repos` and use exact repo name

**Empty results from git tools** → Check `get_index_status` shows git enabled

**Empty results from call graph** → Check `get_index_status` shows call-graph enabled

**Slow searches** → Use `file_pattern` to narrow scope

For detailed workflow examples, see [WORKFLOWS.md](WORKFLOWS.md).
