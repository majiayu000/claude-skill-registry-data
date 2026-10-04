---
name: memory-kg
description: Persistent cross-session memory using the Knowledge Graph MCP server already configured in .mcp.json. Use to save decisions, conventions, bugs, architecture context, and recall them across sessions for OpenCode.
---

# Memory KG — Knowledge Graph Memory

This skill uses the `memory` MCP server already configured in `.mcp.json`. It persists information across sessions in a knowledge graph stored at `.context/memory.jsonl`.

## When to use

- Start of a new session that builds on previous work.
- Before making architectural decisions.
- After discovering a bug or a non-obvious convention.
- When the user asks about past decisions, project history, or "what did we do last time".

## Core tools

| Tool | Purpose |
|------|---------|
| `create_entities` | Add new entities (e.g. `pariscore-architecture`, `jwt-auth-decision`) |
| `create_relations` | Link entities (e.g. `pariscore-architecture` → `uses` → `prisma`) |
| `add_observations` | Append facts to an existing entity |
| `search_nodes(query)` | Find entities by keyword |
| `open_nodes(names)` | Read full entities and observations |
| `read_graph` | Dump the whole graph |

## Entity naming convention

Use kebab-case, domain-prefixed names:

- `pariscore-architecture`
- `pariscore-conventions`
- `pariscore-bugs`
- `pariscore-decisions`
- `api-football-schema`
- `odds-api-schema`
- `user-preferences`

## Session start ritual

At the start of a session, recall context:

```markdown
1. search_nodes("pariscore")
2. search_nodes("architecture")
3. search_nodes("conventions")
4. search_nodes("bugs")
5. search_nodes("user preferences")
6. open_nodes(["pariscore-architecture", "pariscore-conventions"])
```

Synthesize findings in one paragraph.

## Session end ritual

Before ending the session, save:

```markdown
1. Session log → entity `pariscore-session-log`
2. New user preferences → entity `user-preferences`
3. New conventions → entity `pariscore-conventions`
4. Bugs / lessons → entity `pariscore-bugs`
5. Architecture decisions → entity `pariscore-architecture`
```

## Examples

### Save an architecture decision

```json
{
  "entities": [
    {
      "name": "pariscore-architecture",
      "entityType": "decision",
      "observations": ["Chose Zod over Yup for better TypeScript inference."]
    }
  ]
}
```

### Save a bug

```json
{
  "entities": [
    {
      "name": "pariscore-bugs",
      "entityType": "lesson",
      "observations": ["JWT expiry must be validated before decoding payload."]
    }
  ]
}
```

### Recall

```json
{ "query": "pariscore conventions" }
```

## Rules

1. Trust the codebase over memory. If memory conflicts with code, save a correction.
2. Search before creating to avoid duplicates.
3. Keep observations concise and factual.
4. Use relations to link related entities.
