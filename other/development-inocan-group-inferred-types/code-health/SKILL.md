---
name: code-health
description: Analyze codebase health - large files, test coverage gaps, duplicate code, dead/legacy code, and documentation issues. Use when asked to scan, audit, or assess code quality, find refactoring targets, or identify technical debt.
---

# Code Health Analysis

Run `scripts/health.py` to analyze codebase health. The script auto-detects project type (Go, Python, JS/TS) and runs appropriate checks.

## Usage

**Primary (LLM/programmatic use):**

```bash
# Full scan with JSON output (recommended for LLM consumption)
python /path/to/skill/scripts/health.py --json [directory]

# Specific checks with JSON output
python /path/to/skill/scripts/health.py --check size --json [directory]
python /path/to/skill/scripts/health.py --check tests --json [directory]
python /path/to/skill/scripts/health.py --check dupes --json [directory]
python /path/to/skill/scripts/health.py --check dead --json [directory]
python /path/to/skill/scripts/health.py --check docs --json [directory]
```

**Secondary (human debugging):**

```bash
# Human-readable output with emojis (for manual inspection)
python /path/to/skill/scripts/health.py [directory]
python /path/to/skill/scripts/health.py --check size [directory]
```

## Checks

| Check | Description |
|-------|-------------|
| `size` | Large files, function counts, git churn |
| `tests` | Coverage gaps, missing test files, test quality |
| `dupes` | Duplicate function names, similar patterns |
| `dead` | Legacy markers, unused exports, stale code |
| `docs` | Undocumented exports, missing READMEs |

## Output

**JSON format (recommended):** Structured output for LLM/programmatic parsing with severity levels:

- `"critical"`: Immediate attention needed
- `"warning"`: Should address soon
- `"info"`: Nice to fix

Each finding includes file path, line number (when applicable), message, and suggested action.

**Human-readable format (debugging only):** Pretty-printed output with emoji severity indicators (🔴 critical, 🟡 warning, 🟢 info) for manual inspection.

## AST-Based Function Analysis

For more accurate function analysis, use the included AST parsers:

### gofuncs - Go Function Analyzer

```bash
go run scripts/gofuncs.go -dir /path/to/project
```

**Output format:** `file:line:type:exported:name:receiver:signature`

- `type`: `f`=function, `m`=method
- `exported`: `y`=public, `n`=private

**Example:**

```plain
api.go:15:f:n:fetchItems:()[]Item
config.go:144:m:y:GetCategory:*Mapper:(string)string
```

### pyfuncs - Python Function Analyzer

```bash
python scripts/pyfuncs.py --dir /path/to/project
```

**Output format:** `file:line:type:exported:name:class:signature:decorators`

- `type`: `f`=function, `m`=method, `s`=staticmethod, `c`=classmethod, `p`=property
- `exported`: `y`=public, `n`=private (underscore prefix)

**Example:**

```plain
main.py:15:f:y:process_data::(data:List[str])->Dict[str,int]:
api.py:45:m:y:fetch:APIClient:async (url:str)->Response:cache,retry
```

### jsfuncs - JavaScript/TypeScript Function Analyzer

```bash
node scripts/jsfuncs.js --dir /path/to/project
```

**Output format:** `file:line:type:exported:name:class:signature:decorators`

- `type`: `f`=function, `m`=method, `a`=arrow, `c`=constructor, `g`=getter, `s`=setter
- `exported`: `y`=public, `n`=private

**Example:**

```plain
main.js:15:f:y:processData::(data:string[])=>Promise<Object>:
api.ts:45:m:y:fetch:APIClient:async (url:string)=>Response:
```

## Use Cases for AST Tools

These tools provide accurate function-level analysis for:

- **Complexity analysis**: Count functions per file, analyze parameter complexity
- **Test coverage**: Identify which specific functions lack tests
- **Duplicate detection**: Find similar function signatures across the codebase
- **API surface analysis**: List all public vs private functions
- **Documentation gaps**: Cross-reference with doc comments

Combine with `health.py` for comprehensive codebase health analysis.

## Requirements

Required: `python3`
Optional (for better results): `rg` (ripgrep), `fd`, `git`, `go` (for Go projects), `staticcheck`, `node` (for JS/TS projects)

Missing tools are reported but don't block execution.
