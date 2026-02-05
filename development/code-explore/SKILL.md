---
name: code-explore
description: "Systematic codebase exploration using tree-sitter AST analysis and repomix semantic search. Use when: (1) User asks to explore/analyze/find/search codebase, (2) Looking for functions/classes/symbols/patterns, (3) Understanding project structure, (4) Tracing dependencies/usage, (5) ANY code analysis task. CRITICAL: NEVER use basic filesystem tools (find, grep, Glob, Read multiple files) when tree-sitter MCP or repomix tools are available."
version: 1.1.0
metadata:
  priority: high
  replaces: ["manual grep", "find commands", "iterative file reading"]
  changelog: "v1.1.0: Added security validation, token awareness, and configuration best practices from ClaudeKit analysis"
---

# Code Exploration with Tree-Sitter & Repomix

## Overview

**Problem:** Using filesystem tools (find, grep, Read) for code exploration is inefficient:
- Wastes context tokens reading full files
- Requires multiple iterations to find patterns
- No semantic understanding of code structure
- Slow and error-prone

**Solution:** Purpose-built code analysis tools:
1. **Tree-Sitter MCP**: AST-based analysis for precise code understanding
2. **Repomix**: Semantic codebase packaging for AI consumption
3. **Strategic routing**: Right tool for each exploration type

**Core Principle:** ALWAYS use specialized tools over filesystem commands for code analysis.

---

## When to Use This Skill

### Trigger Phrases

Activate this skill when user says:
- "Find all [functions/classes/imports]"
- "Where is [symbol] used?"
- "Show me the structure of [project/file]"
- "What does [file] import?"
- "Search for [pattern/idiom]"
- "Explore the codebase"
- "Analyze [component]"
- "Trace [dependency]"

### Red Flags - STOP and Use This Skill

If you catch yourself thinking:
- "Let me search for files with glob..."
- "I'll read each [language] file to find..."
- "Let me grep for this pattern..."
- "I'll use find to locate..."
- "I need to read multiple files to understand..."

**ALL of these mean: STOP. Use code-explore skill instead.**

### Anti-Patterns This Skill Prevents

❌ **NEVER do this:**
```
1. Glob("**/*.py")
2. For each file: Read(file)
3. Search manually for pattern
```

✅ **ALWAYS do this instead:**
```
repomix grep "pattern" --context 2
```

❌ **NEVER do this:**
```
1. Read("module.py")
2. Manually parse imports from content
```

✅ **ALWAYS do this instead:**
```
tree-sitter get_dependencies(project, "module.py")
```

---

## Core Workflow

### Phase 1: One-Time Setup

**Check if project is registered:**

```
tree-sitter list_projects_tool()
→ Project exists? Skip to Phase 2
→ Not registered? Continue below
```

**Register project with tree-sitter:**

```
tree-sitter register_project_tool(
  path="/absolute/path/to/project",
  name="project-name",
  description="Brief description"
)
```

**Pack codebase with repomix:**

```
repomix pack_codebase(
  directory="/absolute/path/to/project",
  style="xml",
  topFilesLength=15
)
```

**Store the outputId** returned by repomix for future searches.

---

### Phase 2: Route to Optimal Tool

Use this decision tree to select the right tool:

```
What type of exploration?
│
├─ Find ALL symbols (functions/classes)?
│  └─ repomix grep "^class |^def |^function "
│     Why: Fast, language-agnostic pattern matching
│
├─ Understand project structure?
│  ├─ tree-sitter analyze_project(project, scan_depth=3)
│  │  Why: Language counts, directory structure, entry points
│  └─ repomix pack (for semantic overview)
│     Why: See file tree + metrics
│
├─ Find symbols IN SPECIFIC FILE?
│  └─ tree-sitter get_symbols(project, file_path, ["functions", "classes", "imports"])
│     Why: Precise AST extraction
│
├─ Trace dependencies/imports?
│  └─ tree-sitter get_dependencies(project, file_path)
│     Why: Direct import analysis
│
├─ Find where symbol is used?
│  └─ tree-sitter find_usage(project, symbol, [file_path], [language])
│     Why: Tracks references across codebase
│
├─ Search for code patterns/idioms?
│  └─ repomix grep_repomix_output(outputId, pattern, contextLines=2)
│     Why: Regex search with context
│
├─ Analyze code complexity?
│  └─ tree-sitter analyze_complexity(project, file_path)
│     Why: Metrics (cyclomatic complexity, nesting depth)
│
└─ Find similar code?
   └─ tree-sitter find_similar_code(project, snippet, threshold=0.8)
      Why: Structural similarity detection
```

---

### Phase 3: Validate, Synthesize & Return Results

#### Step 3.1: Security Validation (for packed outputs)

**BEFORE delivering repomix packed output, check for sensitive data:**

Repomix has built-in security scanning that detects:
- API keys, tokens, auth credentials
- Connection strings with passwords
- Private keys, certificates
- Environment variable secrets

**If sensitive data detected:**
1. **Warn user immediately**: "⚠️ Packed output contains potential secrets"
2. **Suggest .repomixignore patterns**: Exclude config files, .env, credentials
3. **Recommend alternatives**: Use includePatterns to focus on source code only
4. **Never share sensitive output directly**

**Example warning:**
```
⚠️ Security Check: Found potential secrets in packed output:
- DATABASE_URL with password in config/database.yml
- API_KEY in .env.production

Recommendation: Add to .repomixignore:
  config/database.yml
  .env*
  **/*credentials*

Or use: includePatterns="src/**/*.py,tests/**/*.py"
```

#### Step 3.2: Token Awareness

**Check packed output size:**
- Repomix returns token count in metrics
- If > 100K tokens, suggest optimization:
  - `compress: true` - Tree-sitter compression (70% reduction)
  - `includePatterns` - Focus on relevant files
  - Split analysis across multiple sessions

**Example token warning:**
```
📊 Token Count: 156,842 tokens (exceeds typical context window)

Recommendations:
1. Enable compression: compress=true (reduces to ~47K tokens)
2. Focus packing: includePatterns="src/**/*.ts,tests/**/*.test.ts"
3. Or analyze in phases: pack src/ first, then tests/ separately
```

#### Step 3.3: Synthesize & Format

**DON'T:**
- Dump raw tool output to user
- Return unformatted grep results
- Show 500-line JSON responses

**DO:**
- Synthesize findings into clear summary
- Extract relevant code snippets with file:line references
- Provide actionable insights
- Format results as tables/lists for readability

**Example Good Output:**

```
Found 8 logging functions across the codebase:

1. log_info() - lib/bash-logger.sh:2952
2. log_warn() - lib/bash-logger.sh:2953
3. log_error() - lib/bash-logger.sh:2954
...

Usage pattern: 207 calls across 6 scripts:
- ntt-backup-chll.sh: 34 calls
- ntt-backup-usb.sh: 28 calls
- floppy-orchestrator: 45 calls
...
```

---

## Tool Reference

### Tree-Sitter MCP Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `register_project_tool` | One-time project setup | First time analyzing codebase |
| `list_projects_tool` | List registered projects | Check if project exists |
| `analyze_project` | Project-wide structure | Understand overall architecture |
| `get_symbols` | Extract functions/classes/imports | Find symbols in specific file |
| `find_usage` | Trace symbol references | "Where is X used?" |
| `get_dependencies` | Parse imports/dependencies | "What does X import?" |
| `find_similar_code` | Find structural patterns | Detect code duplication |
| `analyze_complexity` | Code metrics | Complexity analysis |
| `run_query` | Custom tree-sitter queries | Advanced AST analysis |

### Repomix Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `pack_codebase` | Package into AI-optimized format | Initial codebase overview |
| `grep_repomix_output` | Regex search packed output | Find patterns/idioms |
| `read_repomix_output` | Read specific line ranges | View specific sections |
| `attach_packed_output` | Load existing pack | Resume from previous pack |

**See [references/tool-comparison.md](./references/tool-comparison.md) for detailed capabilities.**

---

## Repomix Configuration Best Practices

### When to Use .repomixignore

Create `.repomixignore` in project root to systematically exclude:

```
# Dependencies
node_modules/
venv/
.venv/
vendor/

# Build artifacts
dist/
build/
*.pyc
__pycache__/

# Configuration with secrets
.env*
config/credentials*
**/*secret*
**/*password*

# Large binary files
*.zip
*.tar.gz
*.pdf
*.png
*.jpg

# IDE files
.vscode/
.idea/
```

### includePatterns vs excludePatterns

**Use includePatterns when:** You want to focus on specific source files
```bash
includePatterns="src/**/*.ts,tests/**/*.test.ts"
# Only packs TypeScript source and tests
```

**Use ignorePatterns when:** You want everything except specific files
```bash
ignorePatterns="test/**,*.spec.js"
# Packs everything except tests
```

### Comment Removal Strategy

**Remove comments (`--remove-comments`) when:**
- Token budget is tight
- Comments add noise (auto-generated docs, linter rules)
- You need pure code structure

**Keep comments when:**
- Comments explain complex logic
- Documentation is needed for understanding
- First-time codebase exploration

### Output Format Selection

| Format | Best For | Token Efficiency |
|--------|----------|------------------|
| **XML** | AI parsing, structured analysis | Medium |
| **Markdown** | Human review, documentation | Low (most readable) |
| **JSON** | Programmatic processing, grep | High (compact) |
| **Plain** | Simple text search | Highest (minimal formatting) |

**Recommendation:** Use XML (default) for AI analysis, unless token budget requires JSON/Plain.

### Compression Flag Usage

**Use `compress: true` when:**
- Codebase > 50K lines
- Token count > 100K
- Need overview without implementation details

**Compression extracts:**
- Function signatures (not bodies)
- Class definitions (not methods)
- Type definitions
- Import statements
- ~70% token reduction

**Skip compression when:**
- Need full implementation details
- Debugging specific logic
- Small codebase (< 10K lines)

---

## Concrete Examples

### Example 1: Find All Logging Functions

**User asks:** "Find all the logging functions in ntt"

**Wrong approach:**
```
Glob("**/*.sh")
→ Read each file
→ Search for "log" manually
```

**Correct approach:**
```
repomix grep_repomix_output(
  outputId="...",
  pattern="log_info|log_warn|log_error",
  contextLines=0
)
```

**Result:** 207 matches in <1 second

---

### Example 2: Understand Project Structure

**User asks:** "What's the structure of this project?"

**Wrong approach:**
```
Bash("find . -type f")
→ Parse output manually
```

**Correct approach:**
```
tree-sitter analyze_project("ntt", scan_depth=3)
```

**Result:** Language counts, directory structure, file types

---

### Example 3: Find Where CopyWorker is Used

**User asks:** "Where is CopyWorker class used?"

**Wrong approach:**
```
Grep("CopyWorker", "**/*.py")
→ Read each match manually
```

**Correct approach:**
```
tree-sitter find_usage(
  project="ntt",
  symbol="CopyWorker",
  language="python"
)
```

**Result:** All usage locations with file:line references

---

### Example 4: Trace Import Dependencies

**User asks:** "What does ntt-copier.py import?"

**Wrong approach:**
```
Read("bin/ntt-copier.py")
→ Parse import statements manually
```

**Correct approach:**
```
tree-sitter get_dependencies("ntt", "bin/ntt-copier.py")
```

**Result:** Complete dependency tree

---

## Advanced Patterns

### Combining Tools for Complex Analysis

**Pattern 1: Find + Analyze**
```
1. repomix grep "^class " → Find all classes
2. tree-sitter get_symbols → Extract methods for each
3. Synthesize into class hierarchy
```

**Pattern 2: Structure + Dependencies**
```
1. tree-sitter analyze_project → Get file list
2. For key files: get_dependencies → Build dependency graph
3. Visualize as mermaid diagram
```

**Pattern 3: Pattern + Usage**
```
1. repomix grep "pattern" → Find pattern usage
2. tree-sitter find_usage → Trace each occurrence
3. Summarize usage context
```

---

## Performance Characteristics

### Tree-Sitter

**Strengths:**
- Precise AST-based analysis
- Language-aware parsing
- Fast symbol extraction
- Handles syntax errors gracefully

**Limitations:**
- Requires language parser support
- One file at a time for some operations
- Setup required (registration)

### Repomix

**Strengths:**
- Entire codebase in single output
- Fast regex search
- No language limitations
- Includes metrics + file tree

**Limitations:**
- Large codebases = large output (use compress flag)
- Regex only (no AST understanding)
- Need to pack first (one-time cost)

**See [references/tool-comparison.md](./references/tool-comparison.md) for detailed benchmarks.**

---

## Integration with Other Skills

### Works With

- **skills/repomix** - Detailed repomix usage patterns
- **skills/docs-seeker** - Finding external documentation
- **skills/systematic-debugging** - Root cause analysis
- **skills/memory-augmented-dev** - Store exploration findings

### Common Workflow

```
1. code-explore → Understand codebase structure
2. memory-augmented-dev → Store key insights
3. systematic-debugging → Apply findings to debug
4. docs-seeker → Find relevant documentation
```

---

## The Iron Law

```
NEVER USE FILESYSTEM TOOLS WHEN CODE ANALYSIS TOOLS ARE AVAILABLE
```

If tree-sitter MCP tools are present, you MUST use them instead of:
- `find` / `Glob` / `ls` for finding code
- `grep` / `Grep` for searching patterns
- `cat` / `Read` for parsing symbols
- Manual file iteration

**Violating this rule wastes tokens and time.**

---

## Checklist: Before Using Filesystem Tools

Before using `Glob`, `Grep`, or `Read` for code analysis, ask:

- [ ] Is this a code exploration task?
- [ ] Are tree-sitter MCP tools available?
- [ ] Is repomix packed for this project?
- [ ] Would tree-sitter or repomix be more efficient?

**If any answer is YES, use this skill instead.**

---

## Quick Reference Card

```
TASK                          TOOL                              COMMAND
────────────────────────────────────────────────────────────────────────
Find all functions            repomix grep                      "^def |^function "
Find classes                  repomix grep                      "^class "
Project structure             tree-sitter analyze_project       scan_depth=3
Symbols in file               tree-sitter get_symbols           ["functions", "classes"]
Where is X used?              tree-sitter find_usage            symbol="X"
What does X import?           tree-sitter get_dependencies      file_path="X"
Find pattern                  repomix grep_repomix_output       pattern="..."
Code complexity               tree-sitter analyze_complexity    file_path="X"
Similar code                  tree-sitter find_similar_code     snippet="..."
```

---

## Further Reading

- [Tool Comparison Matrix](./references/tool-comparison.md) - Detailed capability analysis
- [Query Pattern Library](./references/query-patterns.md) - Common search patterns
- [claudekit-skills/repomix](https://github.com/mrgoonie/claudekit-skills/tree/main/.claude/skills/repomix) - Official repomix skill
