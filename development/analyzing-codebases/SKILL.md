---
name: analyzing-codebases
description: Generates LLM-optimized code context with function call graphs, side effect detection, and incremental updates. Processes JavaScript/TypeScript codebases to create compact semantic representations including multi-level summaries, entry point identification, and hash-based change tracking. Provides 74-97% token reduction compared to reading raw source files. Useful for understanding code architecture, debugging complex systems, reviewing pull requests, and onboarding to unfamiliar projects.
---

# LLM Context Tools

Generate compact, semantically-rich code context for LLM consumption with 99%+ faster incremental updates.

## What This Skill Does

Transforms raw source code into LLM-optimized context:
- **Function call graphs** with side effect detection
- **Multi-level summaries** (System → Domain → Module)
- **Incremental updates** (only re-analyze changed files)
- **Hash-based change tracking**
- **Query interface** for instant lookups

**Token Efficiency**: 74-97% reduction vs reading raw files

## When To Use

✅ User asks to "analyze this codebase"
✅ User wants to understand code architecture
✅ User needs help debugging or refactoring
✅ You need efficient context about a large codebase
✅ User wants LLM-friendly code documentation

## Quick Start

```bash
# Check if tool is available
llm-context version

# If not available, user needs to install
# See setup.md for installation

# Run analysis
llm-context analyze

# Query results
llm-context stats
```

## How It Works

### Progressive Disclosure Strategy

Read in this order for maximum token efficiency:

1. **L0** (200 tokens) → `.llm-context/summaries/L0-system.md`
   - Architecture overview, entry points, statistics

2. **L1** (50-100 tokens/domain) → `.llm-context/summaries/L1-domains.json`
   - Domain boundaries, module lists

3. **L2** (20-50 tokens/module) → `.llm-context/summaries/L2-modules.json`
   - File-level exports, entry points

4. **Graph** (variable) → `.llm-context/graph.jsonl`
   - Function details, call relationships, side effects

5. **Source** (as needed) → Read targeted files only

**Never read raw source files first!** Use summaries and graph for context.

## Common Commands

```bash
# Analysis
llm-context analyze              # Auto-detect full/incremental
llm-context check-changes        # Preview what changed

# Queries
llm-context stats                # Show statistics
llm-context entry-points         # Find entry points
llm-context side-effects         # Functions with side effects
llm-context query calls-to func  # Who calls this?
llm-context query trace func     # Call tree
```

## Usage Patterns

### Pattern 1: First-Time Codebase Understanding

```bash
# 1. Run analysis
llm-context analyze

# 2. Read L0 for overview
cat .llm-context/summaries/L0-system.md

# 3. Get statistics
llm-context stats

# 4. Find entry points
llm-context entry-points
```

**Response template**:
```
I've analyzed the codebase:

[L0 content - architecture, components, entry points]

Statistics: X functions, Y files, Z calls

Would you like me to:
1. Explain a specific domain?
2. Trace a function's call path?
3. Review the architecture?
```

### Pattern 2: After Code Changes

```bash
# Incremental analysis (only changed files)
llm-context analyze

# See what changed
cat .llm-context/manifest.json
```

**Response**: Highlight new/modified functions and their impact

### Pattern 3: Debugging

```bash
# Find function
llm-context query find-function buggyFunc

# Trace calls
llm-context query trace buggyFunc

# Check side effects
llm-context side-effects | grep buggy
```

**Response**: Explain call path and identify potential issues based on side effects

## Detailed Guides

**Setup & Installation**: See [setup.md](setup.md)
**Usage Examples**: See [examples.md](examples.md)
**Command Reference**: See [reference.md](reference.md)
**Common Workflows**: See [workflows.md](workflows.md)

## Side Effect Types

When analyzing functions, these effects are detected:

- `file_io` - Reads/writes files
- `network` - HTTP, fetch, API calls
- `database` - DB queries, ORM
- `logging` - Console, logger
- `dom` - Browser DOM manipulation

## Graph Format

Each function in `graph.jsonl`:

```json
{
  "id": "functionName",
  "file": "path/file.js",
  "line": 42,
  "calls": ["foo", "bar"],
  "effects": ["database", "network"]
}
```

## Best Practices

### ✅ DO

- Read L0 → L1 → L2 → Graph → Source (in order)
- Use queries before reading files
- Run incremental analysis after edits
- Mention detected side effects when debugging
- Check manifest age before using cached data

### ❌ DON'T

- Read raw source files first
- Grep through files manually
- Re-read entire codebase on changes
- Skip summaries and go straight to source

## Token Efficiency

**Traditional approach**:
- Read 10 files = 10,000 tokens
- Missing: call graphs, side effects

**LLM-context approach**:
- L0 + L1 + Graph = 500-2,000 tokens
- Includes: complete context + relationships

**Savings**: 80-95%

## Performance

### Initial Analysis
- 100 files: 2-5s
- 1,000 files: 30s-2min
- 10,000 files: 5-15min

### Incremental Updates
- 1 file: 30-50ms
- 10 files: 200-500ms
- 50 files: 1-2s

**Key**: Incremental is 99%+ faster at scale

## Troubleshooting

**"No manifest found"**
→ Run `llm-context analyze` first

**"Cannot find module"**
→ User needs to install: See [setup.md](setup.md)

**"Graph is empty"**
→ No JavaScript files found. Check directory.

## Success Criteria

This skill is working when:

1. ✅ Analysis completes without errors
2. ✅ `.llm-context/` exists with all files
3. ✅ `llm-context stats` shows functions
4. ✅ You use summaries before reading source
5. ✅ Token usage is 50-95% less than raw reading

## Summary

Transform from:
- ❌ Reading thousands of lines token-by-token
- ❌ Missing global context
- ❌ Slow re-analysis

To:
- ✅ Compact semantic representations
- ✅ Call graphs + side effects
- ✅ 99%+ faster incremental updates
- ✅ 50-95% token savings
