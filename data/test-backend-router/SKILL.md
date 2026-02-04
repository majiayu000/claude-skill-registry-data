---
name: test-backend-router
description: Test implementation of thin router skill for DiPeO backend. Provides decision criteria and documentation anchors for FastAPI server, CLI (dipeo run/results/metrics/compile/export), SQLite schema, and MCP integration in apps/server/. Use when task mentions CLI commands, server endpoints, database queries, or MCP tools.
allowed-tools: Read, Grep, Glob, Bash
---

# Test Backend Router Skill

**Purpose**: Demonstrate thin router pattern for on-demand documentation retrieval.

This is a **proof-of-concept** router skill showing how to replace automatic documentation injection with progressive disclosure via doc-lookup.

## When to Use This Skill (NOT the Agent)

Use this skill for **simple, focused tasks**:
- ✅ Reading CLI help text
- ✅ Understanding server configuration
- ✅ Reviewing database schema structure
- ✅ Learning MCP tool signatures
- ✅ Small config changes (<20 lines, 1 file)
- ✅ Debugging with logs (read-only investigation)

**Typical token usage**: ~1,500 tokens (router + specific section)

## When to Escalate to dipeo-backend Agent

Escalate for **complex, multi-step work**:
- ❌ Adding new CLI commands (multi-file changes)
- ❌ Database schema migrations
- ❌ New MCP tool implementation
- ❌ FastAPI route changes (>1 file)
- ❌ Background execution modifications
- ❌ Any task affecting >2 files

**Agent token usage**: Higher, but justified for complex work

## Decision Workflow

```
1. Task received
     ↓
2. Is it simple? (1 file, <20 lines, read-only)
     ↓ YES                    ↓ NO
3. Use this skill          5. Escalate to agent
     ↓
4. Need detailed docs?
     ↓ YES
   Load doc-lookup with specific anchor
```

## Key Documentation Sections

Use `Skill(doc-lookup)` with these anchors for targeted retrieval:

### CLI Commands & Architecture
- **Full guide**: `docs/agents/backend-development.md#cli-system`
- **Command examples**: `docs/agents/backend-development.md#cli-commands`
- **Architecture**: `docs/agents/backend-development.md#cli-architecture`
- **Background execution**: `docs/agents/backend-development.md#background-execution`

**Example lookup**:
```bash
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query "cli-commands" \
  --paths docs/agents/backend-development.md \
  --top 1
```

### FastAPI Server
- **Overview**: `docs/agents/backend-development.md#fastapi-server`
- **Core responsibilities**: `docs/agents/backend-development.md#core-responsibilities`

### Database & Persistence
- **Database schema**: `docs/agents/backend-development.md#database-schema`
- **Message store**: `docs/agents/backend-development.md#message-store`
- **Full DB section**: `docs/agents/backend-development.md#database-persistence`

**Example lookup**:
```bash
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query "database-schema" \
  --paths docs/agents/backend-development.md \
  --top 1 \
  --max-lines 40
```

### MCP Server Integration
- **MCP overview**: `docs/agents/backend-development.md#mcp-server`
- **MCP tools**: `docs/agents/backend-development.md#mcp-tools`
- **MCP resources**: `docs/agents/backend-development.md#mcp-resources`
- **MCP architecture**: `docs/agents/backend-development.md#mcp-architecture`

**Example lookup**:
```bash
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query "mcp-tools" \
  --paths docs/agents/backend-development.md \
  --top 1
```

### General Reference
- **Common patterns**: `docs/agents/backend-development.md#common-patterns`
- **Troubleshooting**: `docs/agents/backend-development.md#troubleshooting`
- **Escalation**: `docs/agents/backend-development.md#escalation`

## Usage Examples

### Example 1: Understanding CLI Flags

**User request**: "How do I add a `--json` flag to `dipeo run`?"

**Router workflow**:
1. Assess: Simple task, need CLI context
2. Load doc-lookup for CLI commands section:
   ```bash
   python .claude/skills/doc-lookup/scripts/section_search.py \
     --query "cli-commands" \
     --paths docs/agents/backend-development.md \
     --top 1
   ```
3. Review returned section (~50 lines)
4. Answer question or make simple change
5. **Token cost**: ~1,000 tokens (vs. 15,000 with auto-injection)

### Example 2: Debugging MCP Tool Registration

**User request**: "The `dipeo_run` MCP tool isn't showing up"

**Router workflow**:
1. Assess: Debugging task, need MCP tool context
2. Load doc-lookup for MCP tools:
   ```bash
   python .claude/skills/doc-lookup/scripts/section_search.py \
     --query "mcp-tools" \
     --paths docs/agents/backend-development.md \
     --top 1 \
     --max-lines 50
   ```
3. Review MCP tool implementation section
4. Investigate registration logic
5. If fix is simple → handle directly
6. If complex (multi-file) → escalate to agent

### Example 3: Database Schema Review

**User request**: "What columns are in the executions table?"

**Router workflow**:
1. Assess: Read-only, need database schema
2. Load doc-lookup for database schema:
   ```bash
   python .claude/skills/doc-lookup/scripts/section_search.py \
     --query "database-schema" \
     --paths docs/agents/backend-development.md \
     --top 1
   ```
3. Return schema information from section
4. **Token cost**: ~800 tokens (just the schema section)

### Example 4: Complex Task → Escalate

**User request**: "Add support for background execution with progress callbacks"

**Router workflow**:
1. Assess: Complex (affects CLI, database, possibly execution engine)
2. Decision: This requires multi-file changes and architecture decisions
3. **Escalate**: `Task(dipeo-backend, "Add background execution with progress callbacks")`
4. Agent can then load specific sections as needed during implementation

## Escalation Paths

### To dipeo-package-maintainer
When task involves:
- Execution handler logic
- Service architecture (EventBus, ServiceRegistry)
- Domain models
- LLM infrastructure

### To dipeo-codegen-pipeline
When task involves:
- GraphQL schema changes
- Generated type issues
- TypeScript model specs

## Quick Reference: Files You Can Work With

**Directly editable** (if task is simple):
- `apps/server/src/dipeo_server/cli/parser.py` - CLI argument parsing
- `apps/server/src/dipeo_server/api/router.py` - API routes
- `apps/server/main.py` - Server initialization
- `apps/server/src/dipeo_server/infra/db_schema.py` - Database schema

**Requires agent** (if complex):
- Multiple files across CLI, API, and database
- New feature implementation
- Architecture changes

## Testing the Router + Doc-Lookup Pattern

This test skill demonstrates:
1. ✅ **Thin router**: ~100 lines vs. 600+ lines of full docs
2. ✅ **Anchor references**: Stable links to specific sections
3. ✅ **Decision criteria**: Clear guidelines for skill vs. agent
4. ✅ **Progressive disclosure**: Load only needed sections via doc-lookup
5. ✅ **Token efficiency**: ~1,500 tokens vs. 15,000 with auto-injection

## Token Savings Analysis

**Before (auto-injection via PreToolUse hook)**:
- Backend agent invocation: 15,000 tokens automatic
- Total: 15,000 tokens (all-or-nothing)

**After (router + doc-lookup)**:
- Router skill load: ~500 tokens
- Doc-lookup single section: ~500-1,000 tokens
- Total: ~1,000-1,500 tokens (on-demand)
- **Savings**: ~90% reduction for focused tasks

## Version History

- **v1.0.0** (2025-10-19): Initial test implementation demonstrating thin router pattern
