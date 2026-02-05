---
name: doc-lookup
description: Locate and retrieve specific documentation sections from DiPeO's docs/ by heading anchors or keywords. Returns minimal, targeted excerpts instead of full files. Use when you need precise documentation context without loading entire guides.
allowed-tools: Read, Grep, Glob, Bash
---

# Doc Lookup Skill

Retrieve **precise documentation sections** from DiPeO's `docs/` directory using anchors or keyword search.

## When to Use This Skill

Use doc-lookup when you need:
- **Specific guidance** on a subtopic (e.g., "CLI flags", "MCP registration", "handler patterns")
- **Minimal context** instead of loading entire 600-1000 line documents
- **Anchor-based retrieval** for known documentation sections
- **Keyword search** when you know the topic but not the exact location

**Don't use for**:
- Reading entire documentation files (use Read tool directly)
- Code exploration (use Grep/Glob tools)
- General codebase questions (use codebase-qna agent)

## How It Works

The doc-lookup skill uses a helper script that:
1. **Parses markdown files** and extracts sections by headings (##, ###)
2. **Matches queries** against:
   - Explicit anchors: `{#anchor-id}` in headings (highest priority)
   - Implicit anchors: auto-generated from heading text (GitHub-style slugs)
   - Heading text: fuzzy matching
   - Content keywords: when heading doesn't match
3. **Scores and ranks** sections by relevance
4. **Returns top 1-3 sections** with file path, heading, and content

**Note**: Only Markdown-native anchor format `{#anchor-id}` in headings is supported. Standalone HTML anchor tags `<a id="">` are NOT supported and should not be used in documentation.

## Usage Patterns

### Pattern 1: Exact Anchor Lookup (Fastest)

When you know the anchor ID from router skills or previous lookups:

```bash
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query "cli-commands" \
  --paths docs/agents/backend-development.md \
  --top 1
```

**Use when**: Router skills reference specific anchors (e.g., `#cli-commands`, `#mcp-tools`)

### Pattern 2: Heading Search

When you know the heading text but not the anchor:

```bash
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query "MCP Tool Registration" \
  --paths docs/ \
  --top 2
```

**Use when**: Searching for a known topic across multiple docs

### Pattern 3: Keyword Search

When you need sections related to a concept:

```bash
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query "background execution async" \
  --paths docs/ \
  --top 3
```

**Use when**: Exploring documentation for a general topic

### Pattern 4: Headings-Only Preview

To see available sections without content:

```bash
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query "cli" \
  --paths docs/agents/ \
  --no-content \
  --top 5
```

**Use when**: Discovering what documentation exists on a topic

## Command Reference

```bash
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query <search-query> \
  --paths <file-or-dir> [<file-or-dir> ...] \
  --top <number> \
  --max-lines <number> \
  --no-content
```

**Arguments**:
- `--query`: Search term (anchor ID, heading text, or keywords) - **REQUIRED**
- `--paths`: Files or directories to search (default: `docs/`)
- `--top`: Number of results to return (default: 3)
- `--max-lines`: Max lines of content per section (default: 30)
- `--no-content`: Show only headings/anchors without content

## Output Format

Each result includes:
```
================================================================================
Score: 100.0 (match type: anchor)
File: docs/agents/backend-development.md:145
Heading: ## CLI Flags
Anchor: #cli-flags

--------------------------------------------------------------------------------
[Section content here, up to --max-lines]
================================================================================
```

**Match types** (from best to worst):
- `anchor`: Exact or partial anchor match (score: 90-100)
- `heading`: Exact or partial heading match (score: 60-80)
- `content`: Keyword match in content (score: 0-50)

## Integration with Router Skills

Router skills should reference anchors for common lookups:

```markdown
## Key Documentation Sections

### CLI Commands
- Full guide: `docs/agents/backend-development.md#cli-commands`
- Architecture: `docs/agents/backend-development.md#cli-architecture`

### MCP Server
- Tools: `docs/agents/backend-development.md#mcp-tools`
- Available tools: `docs/features/mcp-server-integration.md#available-tools`

## Lookup Procedure
1. Check if anchor is known → use exact anchor query
2. If not → use keyword search
3. Review top 1-2 results
4. If insufficient → escalate to full agent
```

## Examples

### Example 1: Find CLI Flag Documentation

**Task**: User asks about adding `--json` flag to `dipeo run`

**Workflow**:
```bash
# Look up CLI commands section
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query "cli-commands" \
  --paths docs/agents/backend-development.md \
  --top 1
```

**Result**: Returns ~50 lines about CLI commands and conventions, not 600-line full document

### Example 2: Understand MCP Tool Registration

**Task**: Debug MCP tool registration issue

**Workflow**:
```bash
# Search for MCP registration docs
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query "MCP registration" \
  --paths docs/features/ \
  --top 2
```

**Result**: Returns relevant sections from `mcp-server-integration.md`

### Example 3: Learn Handler Patterns

**Task**: Implement new node handler

**Workflow**:
```bash
# Find handler implementation guidance
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query "handler patterns" \
  --paths docs/agents/package-maintainer.md \
  --top 1 \
  --max-lines 50
```

**Result**: Returns handler implementation section with examples

## Tips for Effective Use

1. **Prefer anchor queries** when known (fastest, most accurate)
2. **Start narrow** (specific file) then expand (directory) if needed
3. **Use --top 1** for known topics, `--top 3` for exploration
4. **Increase --max-lines** if section is truncated and you need more context
5. **Use --no-content** first to discover available sections, then fetch full content

## Anchor Conventions in DiPeO Docs

DiPeO documentation uses **Markdown-native anchor format only**:

```markdown
## Heading Text {#anchor-id}
### Subheading {#sub-anchor}
```

**Common anchor patterns**:
- **Commands**: `#cli-commands`, `#cli-architecture`, `#background-execution`
- **Architecture**: `#service-architecture`, `#service-registry-pattern`, `#envelope-pattern-output`
- **Features**: `#mcp-tools`, `#available-tools`, `#database-schema`
- **Handlers**: `#node-handler-pattern`, `#when-adding-new-features`, `#your-responsibilities`
- **Codegen**: `#type-system-design-principles`, `#ir-builder-architecture`, `#generation-workflow`

**Do NOT use** HTML anchor tags like `<a id="anchor-id"></a>` - they are not supported by doc-lookup.

See router skills for complete anchor indexes.

## Troubleshooting

**No results found**:
- Check spelling of query
- Try broader keywords
- Use `--paths docs/` to search all docs
- Use `--no-content --top 10` to see what's available

**Too many results**:
- Use more specific query
- Narrow `--paths` to specific file/directory
- Reduce `--top` to 1-2

**Section truncated**:
- Increase `--max-lines` (default: 30)
- Or read the full section using the returned file path

**Wrong section returned**:
- Use explicit anchor if available
- Make query more specific (e.g., "CLI flags" instead of "CLI")
- Check anchor conventions in router skills

## Version History

- **v1.1.0** (2025-10-21): Removed all `<a id="">` HTML anchor tags from docs; now supports only Markdown-native `{#anchor-id}` format
- **v1.0.0** (2025-10-19): Initial implementation with anchor + keyword search
