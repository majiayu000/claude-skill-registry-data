---
name: MCP Architecture
description: This skill should be used when the user asks to "organize MCP tools", "structure multi-tool MCP", "design MCP architecture", "group MCP tools", "organize 10+ tools", or discusses how to architect complex MCP servers with many tools. Provides patterns for organizing, naming, and structuring multi-tool MCP servers.
version: 0.1.0
---

# MCP Architecture

## Purpose

Design the overall architecture and organization of Model Context Protocol servers with multiple tools (10+ tools). Provide patterns for grouping related tools, naming conventions for discoverability, and structural approaches that scale as MCP servers grow.

## When to Use

Apply these patterns when:
- Designing an MCP server with 10 or more tools
- Reorganizing an existing MCP for better discoverability
- Planning tool relationships and data flow
- Structuring tools for progressive discovery
- Creating consistent naming across related tools

## Core Principles

### 1. Logical Grouping

Group tools by domain, workflow, or data type rather than technical implementation.

**Example: Code Search MCP**

| Tool | Group | Purpose |
|------|-------|---------|
| search | query | Find code patterns |
| get_definition | lookup | Get symbol definition |
| find_references | lookup | Find symbol usages |
| get_context | enrichment | Get full context for symbol |
| info | discovery | Enumerate available tools |

**Sparse table format** - Human readable, shows relationships at a glance.

**JSON array format** for automation:
```json
{
  "tool_groups": [
    {
      "name": "query",
      "tools": ["search"],
      "purpose": "Initial discovery operations"
    },
    {
      "name": "lookup",
      "tools": ["get_definition", "find_references"],
      "purpose": "Detailed symbol information"
    }
  ]
}
```

### 2. Naming Conventions

Use consistent verb-noun patterns that indicate:
- **Action**: What the tool does (search, get, find, list, create)
- **Target**: What it operates on (file, symbol, process, session)

**Good naming patterns:**

```
Query tools:     search_*, find_*, list_*
Lookup tools:    get_*, fetch_*, retrieve_*
Creation tools:  create_*, start_*, init_*
Management:      update_*, delete_*, stop_*
Discovery:       info, help, describe_*
```

**Examples:**

| Tool Name | Pattern | Clear Purpose |
|-----------|---------|---------------|
| search_code | verb_noun | ✓ |
| get_definition | verb_noun | ✓ |
| code_search | noun_verb | ✗ Ambiguous order |
| find | verb_only | ✗ Too vague |
| get | verb_only | ✗ Get what? |

### 3. Tool Relationships

Define explicit relationships between tools using token/ID systems for cross-tool references.

**Example: Browser Integration MCP**

```
proxy_start
  ↓ (generates: proxy_id)
proxy_status
  ↑ (consumes: proxy_id)
proxy_log
  ↑ (consumes: proxy_id)
  ↓ (generates: request_id)
proxy_replay
  ↑ (consumes: request_id)
```

**Sparse table representation:**

| Tool | Generates | Consumes | Relationship |
|------|-----------|----------|--------------|
| proxy_start | proxy_id | - | Root |
| proxy_status | - | proxy_id | Status query |
| proxy_log | request_id | proxy_id | Log retrieval |
| proxy_replay | - | request_id | Request replay |

This shows data flow and tool dependencies at a glance.

### 4. Server Metadata

Structure server metadata for clarity and automation.

**Minimal metadata:**
```json
{
  "name": "code-search",
  "version": "1.0.0",
  "description": "Lightning-fast semantic code search and analysis"
}
```

**Comprehensive metadata:**
```json
{
  "name": "code-search",
  "version": "1.0.0",
  "description": "Lightning-fast semantic code search and analysis",
  "tool_count": 12,
  "tool_groups": ["query", "lookup", "enrichment", "discovery"],
  "progressive_discovery": true,
  "has_info_tool": true,
  "token_systems": ["result_id", "symbol_id"],
  "max_response_tokens": 2000,
  "capabilities": {
    "search": true,
    "definitions": true,
    "references": true,
    "call_hierarchy": true
  }
}
```

Automation flags like `progressive_discovery` and `has_info_tool` help AI agents understand how to use the server effectively.

## Organizational Patterns

### Pattern 1: Layered Discovery

Organize tools in progressive layers of detail:

**Layer 1: Discovery** - `info` tool
**Layer 2: Overview** - `search`, `list_*` tools
**Layer 3: Details** - `get_*`, `find_*` tools
**Layer 4: Deep Dive** - `analyze_*`, `trace_*` tools

**Example structure:**

| Layer | Tools | Token Cost | Use When |
|-------|-------|------------|----------|
| 1 | info | ~50 | Starting exploration |
| 2 | search_code | ~100 | Finding candidates |
| 3 | get_definition | ~200 | Understanding specific symbol |
| 4 | trace_callers | ~500 | Deep analysis |

### Pattern 2: Workflow Grouping

Organize tools around common workflows:

**Code Search Workflows:**

```
Workflow: Find Implementation
  1. search_code("function name")
     → Generates: result_id[]
  2. get_definition(result_id)
     → Returns: Full definition

Workflow: Understand Usage
  1. search_code("class name")
  2. find_references(result_id)
  3. get_context(reference_id)
```

Document workflows in server metadata or info tool output.

### Pattern 3: Domain Separation

For servers handling multiple domains, use prefixes:

```
Code domain:     code_search, code_definition, code_references
File domain:     file_search, file_read, file_stats
Project domain:  project_info, project_structure, project_deps
```

**Sparse table:**

| Prefix | Domain | Tool Count |
|--------|--------|------------|
| code_* | Code analysis | 5 |
| file_* | File operations | 3 |
| project_* | Project metadata | 4 |

## Scaling Strategies

### When to Split an MCP Server

Consider splitting when:
- Tool count exceeds 20
- Distinct domains with different deployment requirements
- Different authentication/authorization needs
- Tools have different performance characteristics

**Example: Split recommendation**

```
Before (25 tools):
  unified-dev-server
    - Code tools (8)
    - Browser tools (7)
    - Process tools (6)
    - Session tools (4)

After (3 servers):
  code-search-server (8 tools)
  browser-proxy-server (7 tools)
  process-manager-server (10 tools, combining process + session)
```

### When to Keep Tools Together

Keep tools in one server when:
- They share common data/state
- Cross-tool workflows are frequent
- Combined tool count < 15
- Deployment complexity isn't worth the split

## Naming Examples

### Good Tool Names (Following Patterns)

**Code Search Domain:**
```
search_code          - Search code by pattern
get_definition       - Get symbol definition by ID
find_references      - Find symbol references
list_symbols         - List all symbols in file
analyze_dependencies - Analyze code dependencies
```

**Process Management Domain:**
```
start_process   - Start a new process
get_status      - Get process status by ID
stop_process    - Stop running process
list_processes  - List all processes
tail_output     - Get recent process output
```

**Browser Integration Domain:**
```
start_proxy      - Start reverse proxy
get_errors       - Get JavaScript errors
capture_screenshot - Capture browser screenshot
inject_script    - Inject JavaScript code
measure_performance - Get performance metrics
```

### Poor Tool Names (Avoid These)

```
search          - Too vague (search what?)
get             - Too vague (get what?)
find            - Too vague (find what?)
process         - Noun, not verb-noun
code            - Not clear what it does
run             - Ambiguous (run what?)
```

## Architecture Documentation

Document architecture in server metadata, README, or info tool output.

**Example info tool output (sparse table):**

```
Tool Groups
===========

Query Tools (Fast, <100 tokens)
  search_code      - Search code patterns
  search_files     - Search file names

Lookup Tools (Medium, ~200 tokens)
  get_definition   - Get symbol definition
  find_references  - Find symbol usages

Analysis Tools (Slow, ~500 tokens)
  trace_callers    - Trace call hierarchy
  analyze_deps     - Analyze dependencies

Use get_help(tool_name) for detailed tool documentation.
```

**JSON format for automation:**

```json
{
  "tool_groups": [
    {
      "name": "Query Tools",
      "performance": "fast",
      "avg_tokens": 100,
      "tools": [
        {"name": "search_code", "description": "Search code patterns"},
        {"name": "search_files", "description": "Search file names"}
      ]
    }
  ],
  "discovery": {
    "info_tool": "info",
    "help_tool": "get_help"
  }
}
```

## Additional Resources

### Reference Files

For detailed patterns and advanced techniques, consult:
- **`references/patterns.md`** - Comprehensive organizational patterns
- **`references/naming.md`** - Extended naming conventions and examples
- **`references/scaling.md`** - Strategies for scaling MCP servers

### Examples

Working examples in `examples/`:
- **`code-search-architecture.json`** - Complete code search MCP structure
- **`browser-proxy-architecture.json`** - Browser integration MCP structure
- **`process-manager-architecture.json`** - Process management MCP structure

## Quick Reference

**When architecting an MCP server:**

1. **Group logically** - By domain, workflow, or data type
2. **Name consistently** - Use verb-noun patterns
3. **Define relationships** - Document token/ID systems
4. **Layer discovery** - From overview to deep dive
5. **Document structure** - In metadata or info tool
6. **Use sparse tables** - For human readability
7. **Provide JSON** - For automation

**Tool organization checklist:**

- [ ] Tools grouped by logical domain
- [ ] Consistent verb-noun naming
- [ ] Token/ID relationships documented
- [ ] Progressive discovery layers defined
- [ ] Server metadata includes automation flags
- [ ] Info tool provides architecture overview
- [ ] Workflows documented
- [ ] Scaling strategy considered

Focus on discoverability and progressive access to prevent overwhelming users with too many tools at once.
