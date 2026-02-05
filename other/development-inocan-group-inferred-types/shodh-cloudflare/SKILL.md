---
name: shodh-cloudflare
description: Persistent memory system for AI agents running on Cloudflare's edge network. Use this skill to remember context across conversations, recall relevant information, and build long-term knowledge. Activate when you need to store decisions, learnings, errors, or context that should persist beyond the current session.
version: 1.0.0
author: Shodh AI (Cloudflare Edition)
tags:
  - memory
  - persistence
  - context
  - recall
  - knowledge-management
  - cloudflare
  - edge
---

# Shodh Cloudflare - Persistent Context for AI Agents

Shodh Cloudflare gives you persistent memory across conversations, powered by Cloudflare's globally distributed edge network. Unlike your context window which resets each session, memories stored here persist indefinitely and can be recalled semantically from anywhere in the world.

## When to Use Memory

**ALWAYS call `proactive_context` at the start of every conversation** with the user's first message. This surfaces relevant memories automatically.

### Store memories (`remember`) when:
- User makes a **decision** ("Let's use PostgreSQL for this project")
- You **learn** something new ("The codebase uses a monorepo structure")
- An **error** occurs and you find the fix
- You discover a **pattern** in the user's preferences
- Important **context** that will be useful later

### Recall memories (`recall`) when:
- User asks about past decisions or context
- You need to remember project-specific information
- Looking for patterns in how problems were solved before

## Memory Types

Choose the right type for better retrieval:

| Type | When to Use | Example |
|------|-------------|---------|
| `Decision` | User choices, architectural decisions | "User chose React over Vue for the frontend" |
| `Learning` | New knowledge gained | "This API requires OAuth2 with PKCE flow" |
| `Error` | Bugs found and fixes | "TypeError in auth.js fixed by null check" |
| `Discovery` | Insights, aha moments | "The performance issue was caused by N+1 queries" |
| `Pattern` | Recurring behaviors | "User prefers functional components over classes" |
| `Context` | Background information | "Working on e-commerce platform for client X" |
| `Task` | Work in progress | "Currently refactoring the payment module" |
| `Observation` | General notes | "User typically works in the morning" |
| `Conversation` | Auto-ingested conversations | Automatically stored conversation context |

## Best Practices

### 1. Call `proactive_context` First

```
Every user message → call proactive_context with the message
```

This automatically:
- Retrieves relevant memories based on semantic similarity
- Surfaces context from previous sessions
- Helps maintain continuity across conversations

### 2. Write Rich, Searchable Memories

**Good:**
```
"Decision: Use PostgreSQL with pgvector extension for the RAG application.
Reasoning: Need vector similarity search, user already has Postgres expertise,
avoids adding new infrastructure. Alternative considered: Pinecone (rejected
due to cost)."
```

**Bad:**
```
"Use postgres"
```

### 3. Use Tags for Organization

Tags enable fast filtering without semantic search:

```json
{
  "content": "API rate limit is 100 requests/minute",
  "tags": ["api", "rate-limit", "backend", "project-x"]
}
```

Later recall with: `recall` using tag filters or `forget_by_tags` for cleanup

### 4. Memory Types Affect Importance

The system automatically weights memory types:
- `Decision` and `Error` → Higher importance, slower decay
- `Context` and `Observation` → Lower importance, faster decay

Choose types accurately for better long-term retention.

## Common Patterns

### Starting a Session
```
1. User sends first message
2. Call proactive_context(context: user_message)
3. Review surfaced memories
4. Respond with relevant context
```

### After Making Progress
```
1. Complete a significant task
2. Call remember() with:
   - What was done
   - Why it was done
   - Key decisions made
   - Any gotchas discovered
```

### When User Asks "Do you remember..."
```
1. Call recall(query: "what user is asking about")
2. Also try list_memories to browse recent entries
3. Synthesize memories into response
```

### Debugging a Recurring Issue
```
1. recall(query: "error in [component]")
2. Check if similar errors were solved before
3. Apply previous fix or note new solution
4. remember() the resolution
```

## API Quick Reference

### Core Tools

| Tool | Purpose |
|------|---------|
| `proactive_context` | **Call every message.** Surfaces relevant memories automatically |
| `remember` | Store a new memory with type and tags |
| `recall` | Semantic search across all memories |
| `list_memories` | Browse all stored memories |
| `forget` | Delete a specific memory by ID |
| `forget_by_tags` | Delete memories matching specific tags |

### Diagnostic Tools

| Tool | Purpose |
|------|---------|
| `memory_stats` | Get counts, storage usage, and health status |
| `context_summary` | Quick overview of recent learnings and decisions |

## Example Workflow

```
User: "Let's start building the user authentication system"

You:
1. proactive_context("Let's start building the user authentication system")
   → Surfaces: Previous auth decisions, security preferences, tech stack

2. Response incorporates remembered context:
   "Based on our earlier decision to use PostgreSQL and your preference
   for JWT tokens, I'll set up auth with..."

3. After implementation:
   remember(
     content: "Implemented JWT authentication with refresh token rotation.
               Used bcrypt for password hashing (cost factor 12).
               Tokens expire in 15 minutes, refresh tokens in 7 days.",
     type: "Learning",
     tags: ["auth", "jwt", "security", "user-system"]
   )
```

## Tips for Effective Memory

1. **Be specific** - "React 18 with TypeScript" not "frontend framework"
2. **Include reasoning** - Why decisions were made, not just what
3. **Tag consistently** - Use a tagging convention across the project
4. **Review periodically** - Use `memory_stats` to see what's accumulated
5. **Trust the system** - Semantic search finds relevant memories automatically

## Cloudflare Edge Benefits

This implementation runs on Cloudflare's edge network, providing:

- **Global low-latency access** - Memories accessible from anywhere with minimal delay
- **High availability** - Cloudflare's distributed infrastructure ensures uptime
- **Automatic scaling** - Handles varying workloads seamlessly
- **D1 + Vectorize** - SQLite for metadata, vector database for semantic search
- **Workers AI** - BGE-small-en-v1.5 embeddings (384 dimensions) for semantic matching

---

*Shodh Cloudflare: Because context shouldn't reset with every conversation - and it should be fast, globally.*
