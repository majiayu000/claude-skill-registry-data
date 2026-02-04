---
name: grey-haven-tool-design
description: "Design effective MCP tools and Claude Code integrations using the consolidation principle. Fewer, better-designed tools dramatically improve agent success rates. Use when creating MCP servers, designing tool interfaces, optimizing tool sets, or when user mentions 'tool design', 'MCP', 'fewer tools', 'tool consolidation', 'tool architecture', or 'tool optimization'."
# v2.0.43: Skills to auto-load for tool design work
skills:
  - grey-haven-code-style
  - grey-haven-api-design-standards
# v2.0.74: Tools for tool design work
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Tool Design Skill

Design effective MCP tools and Claude Code integrations using the consolidation principle.

## Core Insight

**Fewer tools = Higher success rates**

Vercel d0 achieved 80% → 100% success by reducing from 17 to 2 tools. This isn't coincidence—it's architecture.

## The Consolidation Principle

### Why Fewer Tools Work Better

1. **Reduced decision space** - Model selects correct tool more often
2. **Simpler context** - Less instruction text per tool
3. **Better parameter handling** - Focused parameters vs kitchen-sink
4. **Clearer intent** - Tool purpose is unambiguous

### Tool Count Impact

| Tool Count | Expected Success | Example |
|------------|------------------|---------|
| 1-3 | 95-100% | Vercel d0 (2 tools) |
| 4-7 | 85-95% | Focused agent |
| 8-15 | 70-85% | General assistant |
| 15+ | <70% | Kitchen sink |

## What's Included

### Examples (`examples/`)
- **MCP consolidation** - Real before/after tool reduction
- **Grey Haven patterns** - How Grey Haven MCP servers follow consolidation
- **Anti-patterns** - Common tool design mistakes

### Reference Guides (`reference/`)
- **Consolidation guide** - Complete tool reduction methodology
- **MCP best practices** - Naming, parameters, descriptions
- **Decision framework** - When to use tools vs agents vs skills

### Checklists (`checklists/`)
- **Tool audit checklist** - Evaluate existing tool sets
- **New tool checklist** - Before adding a new tool

## Key Patterns

### 1. Architectural Reduction

Before (17 tools):
```
create_file, read_file, update_file, delete_file,
list_directory, search_files, get_file_info,
create_folder, rename_file, move_file, copy_file,
get_permissions, set_permissions, watch_file,
compress_file, decompress_file, calculate_hash
```

After (2 tools):
```
file_operation(action, path, content?, options?)
directory_operation(action, path, options?)
```

**Result**: 80% → 100% success rate

### 2. Parameter Consolidation

Instead of many tools with few parameters, use few tools with structured parameters.

**Before** (5 tools):
```typescript
search_code(query: string)
search_files(pattern: string)
search_in_file(file: string, query: string)
search_directory(dir: string, query: string)
search_with_regex(regex: string)
```

**After** (1 tool):
```typescript
search(options: {
  query: string
  type: 'code' | 'files' | 'content'
  path?: string
  regex?: boolean
})
```

### 3. MCP Fully-Qualified Naming

Use prefixes to prevent collisions and clarify scope:

```
mcp__firecrawl__search          // External MCP
mcp__linear__create_issue       // External MCP
search                          // Claude Code native
```

### 4. Tool vs Agent Decision

| Use Tool When | Use Agent When |
|---------------|----------------|
| Single operation | Multi-step workflow |
| Deterministic result | Judgment required |
| Fast execution (<1s) | Complex reasoning |
| Simple I/O | Context accumulation |

## Grey Haven MCP Integration

Grey Haven uses these MCP servers effectively:

| Server | Tools | Purpose |
|--------|-------|---------|
| firecrawl | 5 | Web scraping, search |
| linear | 12 | Issue/project management |
| playwright | 15 | Browser automation |
| context7 | 2 | Documentation lookup |
| filesystem | 10 | File operations |

### Consolidation Opportunities

Even well-designed MCPs can be wrapped for consolidation:

```typescript
// Instead of exposing all 15 playwright tools
// Create 3 workflow-level tools:

browser_navigate(url, options?)       // Navigate + wait
browser_interact(selector, action)    // Click/type/select
browser_extract(selector, format)     // Screenshot/text/html
```

## Anti-Patterns

### 1. Feature Creep
Adding tools "just in case" someone needs them.

**Fix**: Only add tools with proven usage patterns.

### 2. Granular Operations
Separate tools for each atomic operation.

**Fix**: Combine related operations with action parameters.

### 3. Inconsistent Naming
`getUser`, `fetch_project`, `listTeams`, `SEARCH_ISSUES`

**Fix**: Consistent `verb_noun` pattern: `get_user`, `list_projects`

### 4. Missing Descriptions
Tools with cryptic names and no description.

**Fix**: Every tool needs clear description + examples.

## Use This Skill When

- Designing new MCP servers
- Auditing existing tool sets
- Improving agent success rates
- Reducing cognitive load on models
- Optimizing Claude Code integrations

## Related Skills

- `api-design-standards` - REST/GraphQL patterns apply to tools
- `llm-project-development` - Pipeline architecture
- `context-management` - Managing context with tools

## Quick Start

```bash
# Audit your tool set
cat checklists/tool-audit-checklist.md

# Learn consolidation patterns
cat reference/consolidation-guide.md

# See real examples
cat examples/mcp-consolidation-examples.md
```

---

**Skill Version**: 1.0
**Key Metric**: 17→2 tools = 80%→100% success
**Last Updated**: 2025-01-15
