---
name: gh-search-code
description: Use when searching code across GitHub repositories - provides syntax for file extensions, filenames, languages, sizes, exclusions, and using -w flag for regex search via web interface
---

# GitHub CLI: Search Code

## Overview

Search for code **across GitHub repositories** using `gh search code`. **Important**: CLI API uses legacy search engine. For regex and advanced features, use `-w` flag to open in web browser.

## When to Use This Skill

Use this skill when searching code across GitHub:
- Searching for code patterns across multiple repositories
- Finding specific file types or filenames in repos/orgs
- Locating code by language or file size across GitHub
- Searching in specific repositories or organizations
- Need to exclude certain results (requires `--` flag)
- **Need regex search** (use `-w` to open in browser)

## Syntax

```bash
gh search code <query> [flags]
```

## Key Flags Reference

| Flag | Purpose | Example |
|------|---------|---------|
| `--extension <string>` | Filter by file extension | `--extension js` |
| `--filename <string>` | Target specific filenames | `--filename package.json` |
| `--language <string>` | Filter by programming language | `--language python` |
| `--owner <strings>` | Limit to specific owners | `--owner microsoft` |
| `-R, --repo <strings>` | Search within repository | `--repo cli/cli` |
| `--size <string>` | Filter by file size (KB) | `--size ">100"` |
| `--match <strings>` | Search in file or path | `--match file` or `--match path` |
| `-L, --limit <int>` | Max results (default: 30) | `--limit 100` |
| `-w, --web` | Open in browser | `-w` |
| `--json <fields>` | JSON output | `--json path,repository` |

## JSON Output Fields

Available fields: `path`, `repository`, `sha`, `textMatches`, `url`

## Exclusion Syntax (Critical!)

When using inline query exclusions (negations with `-`), you MUST use the `--` separator:

✅ Correct: `gh search code -- "search-terms -qualifier:value"`
❌ Wrong: `gh search code "search-terms" --flag=-value`
❌ Wrong: `gh search code "search-terms" --flag=!value`
❌ Wrong: `gh search code "search-terms" --filename="!test"`

**Examples:**
- `gh search code -- "function -filename:test"` (exclude files named "test")
- `gh search code -- "import -language:javascript"` (exclude language)
- `gh search code -- "config -path:vendor"` (exclude vendor directories)
- `gh search code -- "TODO -extension:md"` (exclude extension)

**Why the `--` separator is required:**
The `--` tells the shell to stop parsing flags and treat everything after it as arguments. Without it, `-qualifier:value` inside quotes may be misinterpreted.

## Understanding `-filename:` vs `-path:` Qualifiers

**Critical Distinction:** These qualifiers have different matching behaviors:

| Qualifier | Matches | Use When |
|-----------|---------|----------|
| `-filename:` | **Filename only** (e.g., `test.js`, `utils_test.py`) | Excluding files by their name pattern |
| `-path:` | **Full file path** (e.g., `src/test/file.js`, `lib/testing/util.js`) | Excluding directory paths or path segments |

### When to Use Each

**Use `-filename:` when:**
- User says "exclude test files" → means files named with "test"
- Targeting files by their name pattern
- Examples: `test.js`, `config_test.py`, `utils.test.ts`

**Use `-path:` when:**
- User says "exclude test directories" → means directories containing "test"
- Targeting files in specific directory paths
- Examples: `tests/`, `__test__/`, `src/test/`, `lib/testing/`

### Matching Examples

**`-filename:test` matches:**
- `test.js` ✅
- `utils_test.py` ✅
- `test_helper.rb` ✅
- `src/file.js` ❌ (doesn't contain "test" in filename)
- `tests/utils.js` ❌ (filename is "utils.js", not "test")

**`-path:test` matches:**
- `tests/utils.js` ✅ (path contains "test")
- `src/test/file.js` ✅ (path contains "test")
- `lib/testing/helper.py` ✅ (path contains "test")
- `test.js` ✅ (path includes filename)
- `src/utils.js` ❌ (path doesn't contain "test")

### Practical Examples

**Exclude files by name:**
```bash
# User: "Find functions but NOT in test files"
gh search code -- "function -filename:test"
# Excludes: test.js, utils_test.py, config.test.ts
# Includes: tests/utils.js (filename is "utils.js", not "test")
```

**Exclude directories:**
```bash
# User: "Find config but NOT in test directories"
gh search code -- "config -path:test"
# Excludes: tests/config.js, src/test/config.py, __test__/setup.js
# Includes: config_test.js (not in test directory)
```

**Combine both qualifiers:**
```bash
# User: "Exclude both test files AND test directories"
gh search code -- "function -filename:test -path:test"
# Excludes: test.js, tests/utils.js, src/test/file.js, utils_test.py
```

## Critical Syntax Rules

### When to Use Flag Syntax vs Query Syntax

**Decision Tree:**
```
Does your search include:
  - Any exclusions (NOT, minus, without, except)?  → Use Query Syntax with `--`
  - Complex boolean logic (OR, AND)?              → Use Query Syntax with `--`

Otherwise:
  - Simple positive filters only?                  → Use Flag Syntax
```

**Flag Syntax** (for positive filters):
```bash
gh search code "import" --language python --extension py
```

**Query Syntax with `--`** (required for exclusions):
```bash
gh search code -- "function -filename:test.js -language:javascript"
```

**⚠️ NEVER mix both syntaxes in a single command!**

### 1. Exclusions and Negations

**CRITICAL:** When excluding results, you MUST use query syntax with the `--` separator.

#### Exclusion Syntax Rules:
1. Use the `--` separator before your query
2. Use `-qualifier:value` format (dash prefix for negation)
3. Quote the entire query string

#### Examples:

**Single exclusion:**
```bash
# Exclude files named "test.js"
gh search code -- "function -filename:test.js"

# Exclude specific language
gh search code -- "import -language:javascript"

# Exclude vendor directories
gh search code -- "config -path:vendor"
```

**Multiple exclusions:**
```bash
# Exclude multiple filenames
gh search code -- "function -filename:test.js -filename:spec.js"

# Exclude language and test directories
gh search code -- "TODO -language:go -path:test"

# Exclude multiple languages
gh search code -- "class -language:java -language:kotlin"
```

**Combine with positive filters using flags:**
```bash
# Wrong - mixing syntaxes:
gh search code "function" --language python -filename:test  # ❌

# Correct - use query syntax for everything when excluding:
gh search code -- "function language:python -filename:test"  # ✅
```

**PowerShell exclusions:**
```powershell
# Use --% to prevent PowerShell parsing
gh --% search code -- "function -filename:test.js"
```

#### Common Exclusion Patterns:

| User Request | Command | Qualifier Used |
|--------------|---------|----------------|
| "Find code but not in test files" | `gh search code -- "function -filename:test"` | `-filename:` (matches file names) |
| "Code excluding test directories" | `gh search code -- "function -path:test"` | `-path:` (matches directory paths) |
| "Code excluding specific language" | `gh search code -- "import -language:javascript"` | `-language:` |
| "Code not in vendor/node_modules dirs" | `gh search code -- "config -path:vendor -path:node_modules"` | `-path:` (matches directories) |
| "Functions excluding test and spec files" | `gh search code -- "function -filename:test -filename:spec"` | `-filename:` (matches file names) |
| "Code excluding large files" | `gh search code -- "class -size:>500"` | `-size:` |
| "Code not in specific extension" | `gh search code -- "TODO -extension:md -extension:txt"` | `-extension:` |
| "Code excluding example/doc directories" | `gh search code -- "api -path:examples -path:docs"` | `-path:` (matches directories) |

### 2. Quoting Rules

**Multi-word search:**
```bash
gh search code "error handling"
```

**Complex queries with qualifiers:**
```bash
gh search code "TODO in:file" --language javascript
```

### 3. Size Comparisons

Use quotes for comparison operators:
```bash
gh search code "import" --size ">50" --language python
```

## Common Use Cases

**Search for function patterns:**
```bash
gh search code "async function" --language typescript
```

**Find configuration files:**
```bash
gh search code "database" --filename config.json --owner myorg
```

**Search in specific repo:**
```bash
gh search code "TODO" --repo owner/repo --language go
```

**Exclude files named with "test":**
```bash
gh search code -- "function -filename:test"
```

**Exclude test directories:**
```bash
gh search code -- "function -path:test"
```

**Search by file size:**
```bash
gh search code "import" --size "100..500" --language python
```

**Use regex (via web):**
```bash
# Open in browser for regex support
gh search code "function.*test" --language javascript -w
# Web UI allows: /function.*test/ or /class\s+\w+/
```

**Build complex query, refine in web:**
```bash
# Start with CLI filters, finish with regex in browser
gh search code --owner microsoft --language typescript -w
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `--extension="NOT js"` or `--language=-python` | Flag syntax doesn't support negation | Use query: `-- "-extension:js"` or `-- "-language:python"` |
| `gh search code import -language:js` | `-language` interpreted as flag | Use `--`: `gh search code -- "import -language:js"` |
| `"function NOT language:js"` | `NOT` keyword doesn't work | Use `-`: `-- "function -language:js"` |
| Mixing syntaxes: `--language python "code -filename:test"` | Can't mix flags with query qualifiers | Use query for all: `-- "code language:python -filename:test"` |
| Not quoting multi-word queries | Searches separately | Quote: `"error handling"` |
| Forgetting quotes on comparisons | Shell interprets `>` | Quote: `--size ">100"` |
| Using `-filename` inline without `--` | Parsed as flag | Use `--`: `-- "code -filename:test"` |
| Trying regex via CLI | CLI API doesn't support regex | Use `-w` flag: `gh search code "pattern" -w` |
| PowerShell without `--%` | Breaks with exclusions | Add: `gh --%` |

## Installation Check

If `gh` command not found:
```bash
# Check if gh is installed
which gh

# If not installed, see: https://cli.github.com/manual/installation
```

If not authenticated:
```bash
# Authenticate with GitHub
gh auth login
```

## Web Browser Flag (`-w/--web`)

**Important workaround for advanced features:**

The `-w/--web` flag opens your search in GitHub's web interface, which supports features not available via CLI API:

### Regex Search (Web Only)

```bash
# This opens in browser where you can use regex
gh search code "function.*test" --language javascript -w

# In the web UI, you can then modify to use regex syntax:
# /function.*test/ language:javascript
```

### When to Use `-w`

Use the web flag when you need:
- **Regex patterns** - `/pattern/` syntax for complex matching
- **Advanced filters** - Newer GitHub search features
- **Visual browsing** - Easier to explore results visually
- **Better results** - Web uses newer search engine

### Combining CLI + Web

```bash
# Build query with CLI, open in web for regex
gh search code --language python --repo myorg/myrepo -w
# Then add regex pattern in web UI
```

## Limitations (CLI API)

- Powered by legacy GitHub search engine
- Results may differ from github.com
- **Regex search not available via CLI** (use `-w` flag instead)
- Some advanced features may not work
- **Workaround:** Use `-w/--web` to access full GitHub search features

## Related

- GitHub search syntax: https://docs.github.com/search-github/searching-on-github/searching-code
- For searching other resources: `gh-search-issues`, `gh-search-prs`, `gh-search-repos`, `gh-search-commits`
