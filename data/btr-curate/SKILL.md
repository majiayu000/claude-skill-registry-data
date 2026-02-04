---
name: btr-curate
description: Add context to LOCAL BTR tree (NOT ByteRover/brv). Use `btr` CLI or `mcp__btr__*` MCP tools. Add or update context in the BTR tree with AI-powered metadata extraction. Use when the user wants to "add to context tree", "store this in BTR", "curate to BTR", or needs to organize knowledge with intelligent tagging.
allowed-tools: Read, Write, Bash
---

# BTR Curate

## ⚠️ CRITICAL: BTR ≠ ByteRover

**This skill uses `btr` (local context tree), NOT `brv` (ByteRover CLI).**

| Command | Tool | Syntax |
|---------|------|--------|
| ✓ CORRECT | `btr` | `btr curate <domain> <topic> --content "..."` |
| ✗ WRONG | `brv` | Different tool, different syntax, requires auth |

**PREFER MCP tools when available:**
- `mcp__btr__curate_context` - Structured, type-safe
- `mcp__btr__query_context` - Validated search

Only use Bash `btr` commands if MCP tools are unavailable.

Add or update context with intelligent metadata extraction.

## Preferred Method

1. **FIRST**: Use MCP tools if available
   ```
   mcp__btr__curate_context(domain="auth", topic="jwt-flow", content="...", tags=["security"])
   ```

2. **FALLBACK**: Use `btr` CLI via Bash
   ```bash
   btr curate auth jwt-flow --content "..." --tags security
   ```

3. **NEVER**: Use `brv` (different product entirely)

## Quick Start

```bash
btr curate <domain> <topic> --content "<content>" [--tags tag1,tag2]
```

## Instructions

1. Analyze the content to curate
2. Suggest appropriate domain and topic
3. Auto-extract relevant tags from content
4. Generate a brief summary
5. Run the CLI command
6. Confirm successful curation

## Auto-Tagging Guidelines

Extract tags based on:
- Technology names (react, typescript, postgresql)
- Patterns (singleton, middleware, decorator)
- Concepts (authentication, caching, validation)
- Categories (security, performance, best-practice)

## Interactive Mode

For complex content, use interactive mode:
```bash
btr curate --interactive
```

This walks through domain selection, topic naming, and tag extraction step by step.

## Domain Selection Guide

| Content Type | Suggested Domain |
|--------------|-----------------|
| Login, tokens, sessions | `auth` |
| REST endpoints, GraphQL | `api` |
| SQL, ORM, migrations | `database` |
| Components, hooks, CSS | `frontend` |
| Unit tests, integration tests | `testing` |
| CI/CD, containers, monitoring | `devops` |
| Design decisions, patterns | `architecture` |
| Security rules, validation | `security` |
| Performance tuning | `performance` |

## Topic Naming Conventions

Use kebab-case with descriptive names:

**Good:**
- `jwt-refresh-token-flow`
- `postgres-connection-pool-config`
- `react-form-validation-hook`

**Avoid:**
- `jwt` (too generic)
- `myStuff` (not descriptive)
- `temp_notes` (not permanent-sounding)

## Updating Existing Context

To update an existing topic:

```bash
btr curate auth jwt-validation --content "..." --update
```

The `--update` flag merges new content with existing content.

## Content Guidelines

When curating content, include:

1. **The What**: Actual code or configuration
2. **The Why**: Reason for this approach
3. **The When**: When to use this pattern
4. **Usage Examples**: How to apply it
5. **Caveats**: Any gotchas or limitations

## Example Curation Flow

User provides a code snippet for database connection pooling.

1. **Analyze content**: PostgreSQL connection pool configuration
2. **Suggest domain**: `database`
3. **Suggest topic**: `postgres-connection-pooling`
4. **Extract tags**: `postgresql`, `connection-pool`, `performance`, `configuration`
5. **Execute**:
   ```bash
   btr curate database postgres-connection-pooling \
     --content "..." \
     --tags postgresql,connection-pool,performance,configuration
   ```
6. **Confirm**: "Curated to database/postgres-connection-pooling with 4 tags"

For metadata extraction scripts, see [scripts/extract-metadata.py](scripts/extract-metadata.py).
