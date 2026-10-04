---
name: codebase-recon
description: Efficient codebase understanding using targeted scripts instead of brute-force file reading. Use when exploring unfamiliar code, planning features, debugging, or needing to understand how components connect. Triggers on "understand this codebase", "how does X work", "where is Y used", "what calls Z", or any task requiring codebase context.
---

# Codebase Recon

Build context fast using scripts. Read files only after scripts tell you WHERE to look.

## Core Principle

Scripts extract structure. LLMs interpret meaning.

**Wrong approach:** Read files → Hope to find what you need → Miss things → Waste tokens
**Right approach:** Run targeted scripts → Get structured data → Read only relevant files → Complete picture

## When to Use This Skill

Trigger recon when:
- Starting work on an unfamiliar codebase
- Planning a feature that touches multiple areas
- Debugging and need to trace data flow
- Asked "how does X work" or "where is Y used"
- Need to understand dependencies or impact of changes

## The Toolbelt

Scripts organized by what you're trying to learn. Run the script, interpret the output, THEN decide what files to read.

---

### 1. PROJECT DISCOVERY — What kind of project is this?

**Detect project type and structure:**
```bash
# Show project root structure (2 levels, ignore noise)
find . -maxdepth 2 -type f -name "*.json" -o -name "*.toml" -o -name "*.yaml" -o -name "*.yml" -o -name "Makefile" -o -name "Dockerfile" -o -name "*.mod" -o -name "*.lock" 2>/dev/null | head -30

# Quick file type census
find . -type f -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.java" 2>/dev/null | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Size of codebase (line count by extension)
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.py" -o -name "*.go" \) -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | xargs wc -l 2>/dev/null | tail -1
```

**Interpret:** This tells you the tech stack, project structure, and scale before reading any code.

---

### 2. ENTRY POINTS — Where does execution start?

**Find main entry points:**
```bash
# Package.json scripts (JS/TS)
cat package.json 2>/dev/null | grep -A 20 '"scripts"'

# Main files
find . -maxdepth 3 -type f \( -name "main.*" -o -name "index.*" -o -name "app.*" -o -name "server.*" \) -not -path "*/node_modules/*" 2>/dev/null

# Python entry points
find . -maxdepth 3 -type f -name "__main__.py" -o -name "main.py" -o -name "app.py" -o -name "wsgi.py" 2>/dev/null

# Go entry points
grep -rl "func main()" --include="*.go" . 2>/dev/null | head -10
```

**Interpret:** These are the files to read FIRST — they show the application's skeleton.

---

### 3. DEPENDENCY MAP — What depends on what?

**External dependencies:**
```bash
# JS/TS - direct dependencies
cat package.json 2>/dev/null | grep -A 100 '"dependencies"' | grep -B 100 '"devDependencies"' | head -50

# Python - requirements
cat requirements.txt 2>/dev/null || cat pyproject.toml 2>/dev/null | grep -A 50 '\[project.dependencies\]'

# Go modules
cat go.mod 2>/dev/null | grep -v "^//"
```

**Internal import graph (who imports whom):**
```bash
# JS/TS - find all imports of a specific module
grep -rn "from ['\"].*modulename" --include="*.ts" --include="*.tsx" . 2>/dev/null

# Find the most-imported internal modules (hot files)
grep -roh "from ['\"]\..*['\"]" --include="*.ts" --include="*.tsx" . 2>/dev/null | sort | uniq -c | sort -rn | head -20

# Python imports
grep -rn "^from \|^import " --include="*.py" . 2>/dev/null | grep -v "__pycache__" | head -30
```

**Interpret:** Most-imported files are the core abstractions. Read those before anything else.

---

### 4. SYMBOL SEARCH — Where is X defined? Where is X used?

**Find definition of a function/class/type:**
```bash
# Find function definitions (JS/TS)
grep -rn "function FUNCNAME\|const FUNCNAME\|export.*FUNCNAME\|class FUNCNAME" --include="*.ts" --include="*.tsx" . 2>/dev/null

# Find function definitions (Python)
grep -rn "def FUNCNAME\|class FUNCNAME" --include="*.py" . 2>/dev/null

# Find all usages of a symbol
grep -rn "SYMBOLNAME" --include="*.ts" --include="*.tsx" --include="*.py" . 2>/dev/null | grep -v "node_modules"
```

**Find type/interface definitions (TypeScript):**
```bash
grep -rn "^export type\|^export interface\|^type \|^interface " --include="*.ts" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -30
```

**Interpret:** Now you know exactly which file(s) to read for a specific symbol.

---

### 5. API SURFACE — What endpoints/routes exist?

**REST endpoints:**
```bash
# Express.js routes
grep -rn "app\.\(get\|post\|put\|delete\|patch\)\|router\.\(get\|post\|put\|delete\|patch\)" --include="*.ts" --include="*.js" . 2>/dev/null | grep -v node_modules

# FastAPI/Flask routes (Python)
grep -rn "@app\.\(get\|post\|put\|delete\|route\)\|@router\." --include="*.py" . 2>/dev/null

# Next.js API routes (file-based)
find . -path "*/api/*" -name "*.ts" -o -path "*/api/*" -name "*.js" 2>/dev/null | grep -v node_modules
```

**GraphQL:**
```bash
# Find schema definitions
find . -name "*.graphql" -o -name "*.gql" 2>/dev/null | head -10

# Find resolvers
grep -rn "Query:\|Mutation:\|Resolver" --include="*.ts" --include="*.js" . 2>/dev/null | grep -v node_modules | head -20
```

**Interpret:** This maps the external interface before you read implementation details.

---

### 6. DATA LAYER — How is data stored/accessed?

**Database schemas:**
```bash
# Find migration files
find . -type d -name "migrations" -o -name "migrate" 2>/dev/null
find . -name "*.sql" -not -path "*/node_modules/*" 2>/dev/null | head -10

# Prisma schema
find . -name "schema.prisma" 2>/dev/null

# SQLAlchemy models
grep -rln "class.*Base\|Column(\|relationship(" --include="*.py" . 2>/dev/null | head -10

# TypeORM/Sequelize models
grep -rln "@Entity\|@Column\|Model.init" --include="*.ts" . 2>/dev/null | head -10
```

**Interpret:** Schema files define the data model — critical context for any data-touching feature.

---

### 7. CHANGE HISTORY — What's been touched recently?

**Hot files (most frequently changed):**
```bash
git log --pretty=format: --name-only --since="3 months ago" 2>/dev/null | sort | uniq -c | sort -rn | head -20
```

**Recent changes to a specific area:**
```bash
git log --oneline --since="1 month ago" -- "path/to/directory" 2>/dev/null | head -20
```

**Who knows this code best:**
```bash
git shortlog -sn -- "path/to/file" 2>/dev/null | head -5
```

**Interpret:** Hot files often contain bugs or are under active development. Recent changes show current focus areas.

---

### 8. ERROR PATTERNS — Where are errors handled?

**Find error handling:**
```bash
# Try/catch blocks
grep -rn "try {" --include="*.ts" --include="*.tsx" . 2>/dev/null | grep -v node_modules | wc -l

# Custom error classes
grep -rn "extends Error\|class.*Error" --include="*.ts" --include="*.py" . 2>/dev/null | grep -v node_modules

# Error boundaries (React)
grep -rln "componentDidCatch\|ErrorBoundary" --include="*.tsx" --include="*.jsx" . 2>/dev/null
```

**Find logging:**
```bash
grep -rn "console\.\(log\|error\|warn\)\|logger\.\|logging\." --include="*.ts" --include="*.py" . 2>/dev/null | grep -v node_modules | head -20
```

**Interpret:** Error handling patterns show how the codebase expects to fail — useful for debugging.

---

### 9. TEST COVERAGE — What's tested?

**Find test files:**
```bash
find . -name "*.test.ts" -o -name "*.spec.ts" -o -name "test_*.py" -o -name "*_test.py" -o -name "*_test.go" 2>/dev/null | grep -v node_modules | head -20
```

**Test to source ratio:**
```bash
# Count test files vs source files
echo "Test files:" && find . -name "*.test.*" -o -name "*.spec.*" -o -name "test_*" 2>/dev/null | grep -v node_modules | wc -l
echo "Source files:" && find . -name "*.ts" -o -name "*.py" 2>/dev/null | grep -v node_modules | grep -v test | grep -v spec | wc -l
```

**Interpret:** Test files show expected behavior and edge cases — often clearer than reading implementation.

---

### 10. CONFIG & ENVIRONMENT — How is it configured?

**Find all config files:**
```bash
find . -maxdepth 2 -name "*.config.*" -o -name ".env*" -o -name "*.toml" -o -name "*.yaml" -o -name "*.yml" 2>/dev/null | grep -v node_modules | head -20
```

**Environment variables used:**
```bash
grep -roh "process\.env\.[A-Z_]*\|os\.environ\[.*\]\|os\.getenv" --include="*.ts" --include="*.js" --include="*.py" . 2>/dev/null | sort | uniq
```

**Interpret:** Config files reveal deployment modes, feature flags, and integration points.

---

## Recon Workflow

When you need codebase context, follow this sequence:

1. **Project Discovery** (30 seconds)
   - Run project type detection
   - Get file census
   - Understand scale

2. **Map the skeleton** (1-2 minutes)
   - Find entry points
   - Map dependencies (most-imported files)
   - Identify API surface

3. **Targeted deep-dive** (as needed)
   - Symbol search for specific functions
   - Read only the files scripts pointed you to
   - Use git history to understand evolution

4. **Build mental model**
   - Entry point → Core abstractions → Data layer → External interfaces
   - Now you understand the codebase without reading every file

---

## Script Selection Guide

| I need to understand... | Run these scripts |
|------------------------|-------------------|
| What kind of project this is | Project Discovery |
| Where execution starts | Entry Points |
| The core abstractions | Dependency Map (most-imported) |
| Where a function is defined | Symbol Search (definition) |
| What uses a function | Symbol Search (usages) |
| The API surface | API Surface scripts |
| The data model | Data Layer scripts |
| What's actively being worked on | Change History (hot files) |
| How errors are handled | Error Patterns |
| Expected behavior | Test Coverage (read tests) |

---

## Anti-Patterns

| Don't do this | Do this instead |
|---------------|-----------------|
| Read files hoping to find what you need | Run symbol search, then read specific files |
| Start with implementation details | Start with entry points and work outward |
| Read all files in a directory | Find most-imported files, read those first |
| Guess at project structure | Run project discovery first |
| Ignore test files | Tests document expected behavior clearly |
| Read code without history | Check git log for context on why |

---

## Adapting Scripts

The scripts above are templates. Adapt them:

- Replace file extensions for your stack
- Adjust `grep` patterns for your framework
- Add project-specific patterns (your error classes, your route patterns)
- Combine with `ripgrep` (`rg`) if available — much faster

<constraint>
Never read files blindly — run recon scripts first.
Never start with implementation details — map the skeleton first.
Never assume project structure — detect it.
Always prefer targeted symbol search over full-file reading.
Use git history to understand WHY code exists, not just WHAT it does.
</constraint>
