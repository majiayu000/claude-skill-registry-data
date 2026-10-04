---
name: codebase-index
description: 3-layer codebase indexing system for token-efficient code navigation. Builds compact index + symbol map so agents read targeted lines instead of entire files. Achieves ~5-10x token savings.
---

# Codebase Index - 3-Layer Memory Optimizer

Build and maintain a progressive disclosure index that prevents agents from reading entire files when they only need a function signature or a specific line range.

## When to Activate

- During `/crew init` (full build)
- During `/crew reindex` (full rebuild)
- When an agent needs to find code but the index exists (consult mode)
- After file edits (incremental update mode via index-updater skill)

## Three-Layer Architecture

### Layer 1 - Compact Index (`.claude/crew-index.json`, ~2-5KB)

The cheapest layer. Costs ~50 tokens to read. Contains just enough to route queries to the right file:

**Per-file entry:**
- `hash`: SHA-256 of file content (for change detection)
- `size`: file size in bytes
- `type`: language (javascript, python, typescript, etc.)
- `exports`: exported functions/classes/constants
- `imports`: external dependencies
- `functions`: all function/method names
- `classes`: all class names
- `lines`: total line count
- `category`: core | test | config | docs | util
- `summary`: 1-line description of what this file does

**Global metadata:**
- `version`: schema version
- `generated`: ISO timestamp
- `contentHash`: hash of all file hashes combined
- `dependencies`: package dependencies with versions
- `architecture.entryPoint`: main entry file
- `architecture.pipeline`: data flow description
- `architecture.patterns`: detected patterns (MVC, pipeline, event-driven, etc.)
- `stats`: totalFiles, totalLines, languages, lastIndexed

### Layer 2 - Symbol Map (`.claude/crew-symbols.json`, ~5-15KB)

Mid-detail layer. Costs ~100-200 tokens for relevant section. Contains function signatures and relationships:

**Per-symbol entry** (keyed as `filepath::symbolName`):
- `type`: function | class | method | constant | type
- `signature`: full signature string
- `params`: parameter list with types if available
- `returns`: return type if available
- `calls`: what this symbol calls
- `calledBy`: what calls this symbol
- `lineRange`: [startLine, endLine]
- `description`: 1-line description

**Relationship maps:**
- `callGraph`: which functions call which
- `fileRelationships`: import/export connections between files

### Layer 3 - Full Details (on-demand file reads)

Agents read actual file contents ONLY after consulting Layer 1+2 to know exactly which file and line range they need. Use the Read tool with `offset` and `limit` parameters to read specific line ranges.

## Building the Index (Full Build)

When triggered for full build:

### Step 1: Discover source files
```
Use Glob to find all source files:
- **/*.{js,ts,jsx,tsx,py,go,rs,java,kt,rb,php,c,cpp,h,cs}
- Exclude: node_modules, .git, dist, build, __pycache__, .next, vendor
- Also find: package.json, requirements.txt, go.mod, Cargo.toml, pyproject.toml
```

### Step 2: Read each file and extract metadata
For each source file:
1. Read the file content
2. Compute SHA-256 hash (use `shasum -a 256` via Bash)
3. Extract exports (look for `module.exports`, `export`, `def`, `func`, `fn`, `public`)
4. Extract imports (look for `require`, `import`, `from`, `use`)
5. Extract function names and signatures with line ranges
6. Extract class names
7. Count lines
8. Categorize: core (src/), test (test/), config (root configs), docs, util (lib/, utils/)
9. Generate 1-line summary

### Step 3: Build call graph
From the imports/exports and function calls data:
1. Map which files import from which
2. Map which functions call which (by scanning function bodies for calls to known symbols)
3. Identify entry points (files not imported by anything)

### Step 4: Write index files
1. Write `.claude/crew-index.json` (Layer 1)
2. Write `.claude/crew-symbols.json` (Layer 2)
3. Report stats: files indexed, total lines, languages detected

## Incremental Update

When a single file changes:
1. Recompute its hash
2. Compare with stored hash in crew-index.json
3. If different: re-read the file, update its Layer 1 + Layer 2 entries
4. Update the global contentHash
5. Do NOT rebuild entries for unchanged files

## How Agents Should Use the Index

```
INDEX-FIRST PROTOCOL (mandatory):

Before reading ANY source file:
1. Read .claude/crew-index.json → find which file(s) are relevant
   - Match by: function names, exports, summary keywords, category
2. Read .claude/crew-symbols.json → find exact symbol and line range
   - Match by: symbol name, signature, calledBy/calls relationships
3. Read ONLY the specific line range you need from the actual file
   - Use: Read tool with offset=startLine and limit=(endLine-startLine+1)

NEVER:
- Read an entire file when you only need one function
- Grep the whole codebase when the index has the answer
- Skip the index because "it's faster to just read the file"

ALWAYS:
- Consult Layer 1 first (cheapest)
- Consult Layer 2 only if Layer 1 isn't specific enough
- Read Layer 3 (actual file) only for the exact lines you need
- After making changes, note which files were modified for index update
```

## Token Savings

| Approach | Tokens Used | When |
|----------|-------------|------|
| Read all files | ~2000-10000+ | Without index |
| Layer 1 only | ~50-100 | Finding which file has a feature |
| Layer 1 + Layer 2 | ~150-300 | Finding a specific function |
| Layer 1 + 2 + targeted read | ~300-500 | Reading + editing a function |
| **Savings** | **5-10x** | Per agent interaction |

## Edge Cases

- **New file not in index**: If an agent creates a new file, add it to the index immediately
- **Deleted file still in index**: On reindex, remove entries for files that no longer exist
- **Binary/large files**: Skip files > 100KB or binary files (images, compiled assets)
- **Generated files**: Skip dist/, build/, .next/ directories
- **Config files**: Index but categorize as "config" — lower priority for code searches
