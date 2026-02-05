---
name: btr-capture
description: |
  Save to LOCAL BTR context tree (NOT ByteRover/brv).

  Capture code snippets, patterns, and context from the current conversation and store them in the BTR context tree.

  PROACTIVE TRIGGER: Automatically suggest saving when the user confirms something works ("That works!", "Perfect!", "It's working now", "Thanks, that fixed it!"), after fixing a bug, making an architecture decision, establishing a pattern, or solving a complex problem.

  Also use when the user explicitly says "save this", "remember this pattern", "capture this context", "save to BTR", "save this to BTR", or "add to BTR".
allowed-tools: Read, Write, Bash
---

# BTR Capture

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

Capture and store valuable context for future retrieval.

## PROACTIVE BEHAVIOR (CRITICAL)

**DO NOT wait for the user to say "save this"** - you should proactively suggest saving valuable context.

### Trigger Conditions

After ANY of these events, ASK the user if they want to save the context:

1. **User confirms code works** - "That works!", "Perfect!", "It's working now"
2. **Bug was fixed** - Successfully resolved an issue after debugging
3. **Architecture decision made** - Discussed and decided on a design approach
4. **New pattern established** - Created a reusable pattern, utility, or component
5. **Complex problem solved** - Figured out a non-obvious solution
6. **Configuration established** - Set up tooling, environment, or integration

### Example Flow

```
User: "That fixed the authentication issue, thanks!"

Claude: "Great! The JWT refresh token rotation pattern we implemented
could be valuable for future auth work. Save to BTR?

I'd capture:
- Domain: auth
- Topic: jwt-refresh-rotation
- Key details: The rotation logic, error handling, and token invalidation"
```

### Proactive Check-In

Every 10-15 messages during active development, consider:
- Have we established patterns worth preserving?
- Did we make decisions that should be documented?
- Is there context that would help future sessions?

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

1. Identify the content to capture (code, explanation, pattern)
2. Determine appropriate domain (e.g., auth, api, database, frontend, testing)
3. Generate a descriptive topic name (kebab-case, e.g., jwt-validation, error-handling)
4. Extract or ask for relevant tags
5. Run the CLI command to save the context
6. Confirm successful capture to user

## Domain Suggestions

- `auth` - Authentication, authorization, sessions
- `api` - REST endpoints, GraphQL, rate limiting
- `database` - Queries, migrations, connection pooling
- `frontend` - Components, state management, styling
- `testing` - Test patterns, mocking, fixtures
- `devops` - Deployment, CI/CD, monitoring
- `architecture` - Design decisions, patterns

## Examples

### Save a code pattern
User: "Save this JWT validation pattern"
```bash
btr curate auth jwt-validation --content "..." --tags security,tokens,middleware
```

### Save a design decision
User: "Remember why we chose Redis for caching"
```bash
btr curate architecture caching-decision --content "..." --tags redis,decisions,performance
```

For more examples, see [examples.md](examples.md).
