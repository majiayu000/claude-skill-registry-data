---
name: doc-query
description: Query up-to-date tool documentation using Context7. Use when you need current documentation for Python 3.14+, Claude Code CLI, or other configured tools.
---

# Documentation Query Skill

Query real-time documentation for configured tools and technologies using Context7 API.

## When to Use This Skill

**ALWAYS invoke this skill in these scenarios:**

1. **Before using Python 3.14+ features**
   - Async features (async/await, TaskGroup, AsyncExitStack)
   - Type hints (new syntax, generics, Annotated)
   - New stdlib modules or functions
   - When uncertain about current API

2. **Before using Claude Code CLI features**
   - Skills, agents, hooks, slash commands
   - MCP integration, settings configuration
   - Plugin development

3. **When encountering errors with configured tools**
   - Parse error messages for tool names
   - Query tool-specific troubleshooting docs

4. **When user asks "How do I... <tool-name>..." questions**
   - Extract tool name from question
   - Query documentation before attempting answer

## Why This Matters

Training data may be outdated for:
- Python 3.14+ (released after training cutoff)
- Claude Code CLI (rapidly evolving)
- Other modern tools (ruff, uv, etc.)

Context7 provides **real-time access** to current documentation.

## Instructions

### Step 1: Check Available Sources

```bash
.claude/skills/doc-query/scripts/list-sources
```

This shows all configured documentation sources.

### Step 2: Query Documentation

```bash
.claude/skills/doc-query/scripts/query <source> "<topic>" [tokens]
```

**Parameters:**
- `source`: Source name from doc-sources.toml (e.g., "python", "claude-code")
- `topic`: Search query (e.g., "async context managers")
- `tokens`: Optional token limit (uses source default if omitted)

**Examples:**
```bash
.claude/skills/doc-query/scripts/query python "async context managers"
.claude/skills/doc-query/scripts/query claude-code "create skill" 2000
.claude/skills/doc-query/scripts/query py "type hints"  # Using alias
```

### Step 3: Process Results

The script outputs markdown documentation from Context7. Process this to:
1. Extract relevant code examples
2. Identify key patterns
3. Answer user's question with current information

## Alias Support

Sources can have aliases for convenience:
- `py` → `python`
- `claude` → `claude-code`

Check `.claude/doc-sources.toml` for configured aliases.

## Configuration

Documentation sources are configured in `.claude/doc-sources.toml`:

```toml
[sources.python]
context7_id = "websites/python_3_14"
description = "Python 3.14+ standard library"
default_tokens = 3000
aliases = ["py", "python3"]
```

To add new sources, use the **add-doc skill**.

## Error Handling

**If CONTEXT7_API_KEY not set:**
```
Error: CONTEXT7_API_KEY environment variable not set.
See CONTRIBUTING.md for setup instructions.
```

**If source not found:**
```
Error: Unknown documentation source: 'ruff'
Available sources: python, claude-code
Run '.claude/skills/doc-query/scripts/list-sources' to see all sources.
```

## Examples

### Example 1: Python async features

**User:** "How do I create an async context manager in Python 3.14?"

**Skill execution:**
```bash
.claude/skills/doc-query/scripts/query python "async context manager" 2000
```

**Process results** → Provide answer with current API.

### Example 2: Claude Code skill creation

**User:** "How do I create a custom skill?"

**Skill execution:**
```bash
.claude/skills/doc-query/scripts/query claude-code "create skill"
```

**Process results** → Show skill directory structure and SKILL.md format.

### Example 3: Using aliases

**User:** "What's new in Python type hints?"

**Skill execution:**
```bash
.claude/skills/doc-query/scripts/query py "type hints new features" 3000
```

## Integration with Other Skills

**When adopting new tools:**
1. Create/update ADR (adr skill)
2. Add documentation source (add-doc skill)
3. Query documentation (this skill)

See CLAUDE.md for workflow details.

## Token Efficiency

- Default token limits per source (2000-3000)
- Only query when needed (not preloaded)
- Local processing (no LLM overhead for queries)
- Cost: ~0 Sonnet tokens (direct API call)

## Technical Details

**Implementation:**
- Python 3.12+ stdlib only (urllib, tomllib)
- TOML-based configuration
- Generic Context7 client
- Modern type hints

**See:** [ADR-0003](../../../docs/adrs/adr-0003-use-context7-for-documentation-access.md)
