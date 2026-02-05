---
name: codebase-index
description: Quickly index and understand a codebase's architecture. Use at session start to get up to speed fast. Finds entry points, API routes, classes, models, configs, and patterns.
allowed-tools: Bash, Read, Grep, Glob
---

# Codebase Index - Fast Architecture Discovery

Get up to speed on any codebase in seconds, not minutes.

## When to Use

- **Session startup** - First thing after entering a new repo
- **Context recovery** - After compaction, understand what you're working with
- **New project** - Quickly map an unfamiliar codebase
- **Architecture review** - Find patterns and structure

## Quick Start Commands

Run these in sequence to build a mental map:

### 1. Entry Points (Where does it start?)

```bash
# Python entry points
rg "if __name__.*main" --type py -l

# Node/TypeScript entry points
rg "^(export default|module\.exports)" --type ts --type js -l | head -20

# Main files
ls -la **/main.* **/index.* **/app.* 2>/dev/null | head -20
```

### 2. API Endpoints (What does it expose?)

```bash
# FastAPI routes
rg "@(app|router)\.(get|post|put|delete|patch)" --type py -n | head -30

# Flask routes
rg "@.*\.route\(" --type py -n | head -30

# Express routes
rg "(app|router)\.(get|post|put|delete)\(" --type js --type ts -n | head -30

# Cloud Functions
rg "functions_framework|@functions\." --type py -n
```

### 3. Classes & Core Definitions

```bash
# Python classes
rg "^class \w+" --type py -n | head -40

# TypeScript/JS classes and interfaces
rg "^(export )?(class|interface|type) \w+" --type ts -n | head -40

# Python functions (top-level only)
rg "^def \w+" --type py -n | head -40
```

### 4. Database Models

```bash
# SQLAlchemy models
rg "class.*\(.*Base\)|class.*Model\):" --type py -n

# Prisma models
rg "^model \w+" --glob "*.prisma"

# Django models
rg "class.*models\.Model" --type py -n

# Pydantic models
rg "class.*\(.*BaseModel\)" --type py -n
```

### 5. Configuration & Environment

```bash
# Find config files
fd -e yaml -e yml -e toml -e ini -e json -e env 2>/dev/null | grep -i config | head -20

# Environment variable usage
rg "os\.environ|os\.getenv|process\.env" -n | head -30

# Settings/config classes
rg "class.*(Config|Settings)" --type py -n
```

### 6. Tests Structure

```bash
# Find test files
fd -e py -e ts -e js | grep -i test | head -20

# Test classes and functions
rg "^(class Test|def test_|describe\(|it\()" --type py --type ts --type js -n | head -30
```

### 7. Key Imports (Dependencies)

```bash
# Most imported packages (Python)
rg "^(from|import) " --type py | cut -d' ' -f2 | cut -d'.' -f1 | sort | uniq -c | sort -rn | head -20

# Package.json dependencies
cat package.json 2>/dev/null | grep -A 50 '"dependencies"' | head -30
```

### 8. Architecture Patterns

```bash
# Decorators (Python)
rg "^@\w+" --type py | cut -d':' -f2 | sort | uniq -c | sort -rn | head -15

# Dependency injection
rg "Depends\(|@inject|@Inject" --type py --type ts -n

# Error handling patterns
rg "class.*Exception|class.*Error\(" --type py -n

# Logging setup
rg "logging\.(getLogger|basicConfig)|logger = " --type py -n | head -15
```

## Language-Specific Quick Indexes

### Python Project

```bash
# One-liner: core structure
rg "^(class |def |@app\.|@router\.)" --type py -n | head -50
```

### TypeScript/Node Project

```bash
# One-liner: core structure
rg "^(export |class |interface |function |\s*(get|post)\()" --type ts -n | head -50
```

### Go Project

```bash
# One-liner: core structure
rg "^(func |type .* struct)" --type go -n | head -50
```

## Full Codebase Snapshot

Run this to get a complete picture:

```bash
echo "=== ENTRY POINTS ===" && rg "if __name__|^func main" --type py --type go -l 2>/dev/null
echo "=== API ROUTES ===" && rg "@(app|router)\.(get|post|put|delete)" --type py -c 2>/dev/null
echo "=== CLASSES ===" && rg "^class " --type py -c 2>/dev/null | head -10
echo "=== CONFIG FILES ===" && fd -e yaml -e toml -e env 2>/dev/null | head -10
echo "=== TEST FILES ===" && fd test --type f 2>/dev/null | wc -l
```

## Pro Tips

| Tip | Why |
|-----|-----|
| Use `-c` (count) first | See scope before diving in |
| Use `-l` (files only) | Find relevant files, then read them |
| Pipe to `head` | Don't overwhelm context with output |
| Chain with `grep -i topic` | Filter results to what you care about |
| Use `--type` flags | Focus on relevant file types |

## Token Efficiency

All commands return summaries, not full files. A complete codebase index typically uses <500 tokens while giving you the mental map to know exactly what to read next.

## Related Skills

- **index-docs**: Markdown heading extraction
- **search-history**: Find past discussions about this codebase
- **post-compact**: Full context recovery workflow
