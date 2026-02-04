---
name: registry-database
description: Manage the Registry platform - unified Convex database for tasks, articles, courses, emails, and all personal/professional data with MCP server integration
---

# registry-database Skill

Teaches how to work with the Registry platform - a Convex-backed database that serves as single source of truth for all data (tasks, articles, courses, emails, coding projects, etc.).

## When to Use This Skill

Use this skill when the user mentions:
- registry, convex, database, schema
- tasks, todos, task tracking, high-level tasks
- articles, article status, article metadata
- courses, quizzes, students, teaching data
- emails, outlook sync, email management
- MCP server tools, registry tools
- coding projects, session tracking
- morning review, unified dashboard

## Core Concepts

### Registry Platform Architecture

**Purpose:** Single source of truth for all personal and professional data.

**Tech Stack:**
- **Convex:** Real-time database with TypeScript schema
- **Bun:** Runtime for MCP server
- **React:** Web dashboard (planned)
- **MCP:** Model Context Protocol server for OpenCode integration

**Location:** `~/Code/github.com/theslyprofessor/registry/`

### Database Schema (10 Tables)

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **users** | Access control | username, email, displayName |
| **registries** | Item collections | name, type, username, visibility |
| **tasks** | High-level todos | content, status, priority, articleId, projectContext |
| **articles** | Vault content metadata | slug (ID), article_status, visibility |
| **opencode_sessions** | Session history | sessionId, projectContext, stats |
| **courses** | Teaching courses | canvasId, students, quizzes |
| **quizzes** | Course assessments | canvasQuizId, questions, deployed |
| **recording_sessions** | Lab/recording work | type, equipment, techniques |
| **emails** | Correspondence | outlookId, status, courseId, articleId |
| **people** | Contacts/students | name, email, relationship |
| **coding_projects** | Dev projects | repoUrl, tech_stack, tasks |

### Article Slug as ID

**Critical concept:** Article slugs ARE the articleId in registry.

```typescript
// Vault file: midimaze/Music Theory/Intervals.md
// Frontmatter: slug: intervals
// Registry: articleId = "intervals"
```

**Why:** 
- Slugs are unique, human-readable identifiers
- Used in web URLs for midimaze 2.0
- Natural link between vault and database

### Article Status (6 States)

```
draft → in_progress → needs_review → complete → published → archived
```

**NOT the same as HIL:**
- `article_status`: Content workflow state
- `hil`: Human-in-loop decision tracking

### Task Status & Priority

**Status:** `pending`, `in_progress`, `completed`, `cancelled`

**Priority:** `low`, `medium`, `high`

**Purpose:** Registry tracks high-level tasks and ideas across all domains (teaching, coding, personal). For AI coding tasks that need multi-session work, use Beads (separate system) or OpenSpec change proposals.

## MCP Server Tools

**Location:** `registry/packages/mcp/src/index.ts`

### Core Tools (Available Now)

| Tool | Purpose | Usage |
|------|---------|-------|
| `create_registry` | Create new registry | Type: tasks, articles, courses, etc. |
| `list_registries` | List user's registries | Filter by type |
| `create_task` | Add new task | content, priority, projectContext |
| `update_task_status` | Change task state | taskId, new status |
| `get_tasks` | Query tasks | Filter by status, project |
| `sync_todos` | Sync OpenCode todos | Batch sync from todoWrite |

### Planned Tools

- Email sync/management (Outlook → Registry)
- Course/quiz creation and management
- Article sync from vault (frontmatter → registry)
- Morning review dashboard queries
- Recording session tracking
- Coding project management

## Common Workflows

### 1. Create a Registry

```typescript
// User: "Create a new task registry for the NNT compiler project"

registry_create_registry({
  name: "nnt-compiler-tasks",
  type: "tasks",
  username: "ntiruviluamala",
  visibility: "private"
})
```

### 2. Add Tasks

```typescript
// User: "Add a task to implement the lexer"

registry_create_task({
  content: "Implement lexer for NNT notation",
  registryId: "<registry-id>",
  priority: "high",
  projectContext: "nnt-compiler",
  tags: ["parser", "core"]
})
```

### 3. Sync OpenCode Todos

```typescript
// User: "Sync my current todos to registry"

registry_sync_todos({
  todos: [...], // From todoRead
  registryId: "<registry-id>",
  projectContext: "current-project"
})
```

### 4. Query Tasks

```typescript
// User: "Show me all in-progress tasks for the registry project"

registry_get_tasks({
  registryId: "<registry-id>",
  status: "in_progress",
  projectContext: "registry"
})
```

## Development Workflows

### Start Convex Dev Server

```bash
cd ~/Code/github.com/theslyprofessor/registry
bun convex dev
```

**What happens:**
- Connects to Convex cloud project
- Watches `convex/schema.ts` for changes
- Auto-deploys on save
- Provides dashboard URL

### Modify Schema

**File:** `convex/schema.ts`

```typescript
// Add new field to tasks table
tasks: defineTable({
  // ... existing fields
  estimatedHours: v.optional(v.number()),
})
```

**Deploy:** Just save - auto-deploys in dev mode

**No migrations needed:** Optional fields are graceful

### Test MCP Server Locally

```bash
cd ~/Code/github.com/theslyprofessor/registry/packages/mcp
bun run src/index.ts
# Runs in stdio mode (for MCP protocol)
```

### Add New MCP Tool

1. **Define tool in schema:**
   ```typescript
   // packages/mcp/src/index.ts
   server.tool({
     name: "create_article",
     description: "Create article metadata in registry",
     input: z.object({
       slug: z.string(),
       title: z.string(),
       // ...
     }),
     execute: async (params) => {
       // Implementation
     }
   })
   ```

2. **Create Convex mutation:**
   ```typescript
   // convex/articles.ts
   export const create = mutation({
     args: { /* ... */ },
     handler: async (ctx, args) => {
       // Database logic
     }
   })
   ```

3. **Test in OpenCode:** Tools auto-discover on restart

## Data Flow Architecture

```
Vault (Obsidian markdown)
    ↓ frontmatter sync (planned)
Registry (Convex database)
    ↓ MCP tools
OpenCode (AI coding assistant)
    ↓ queries
Morning Review Dashboard (planned)
```

**External Integrations:**
- **Outlook:** Email sync via outlook-sqlite-mcp (planned)
- **Canvas LMS:** Course/quiz data (planned)
- **GitHub:** Coding project metadata (planned)
- **Vault:** Article frontmatter sync (planned)

## Schema Evolution Guidelines

### Adding Optional Fields

✅ **Safe:** Just add to schema, deploy
```typescript
tasks: defineTable({
  // ... existing
  newField: v.optional(v.string()),
})
```

### Adding Required Fields

⚠️ **Requires migration:**
```typescript
// 1. Add as optional first
newField: v.optional(v.string()),

// 2. Write migration mutation
export const backfillNewField = mutation({
  handler: async (ctx) => {
    // Populate existing records
  }
})

// 3. Make required after backfill
newField: v.string(),
```

### Adding Tables

✅ **Safe:** Add to schema, start using
```typescript
gear_inventory: defineTable({
  model: v.string(),
  category: v.string(),
  // ...
})
```

## Common Issues

### Convex Connection Errors

**Problem:** "Failed to connect to Convex"

**Solutions:**
- Check `CONVEX_URL` in `.env.local`
- Verify `bun convex dev` is running
- Check internet connection
- Re-authenticate: `bunx convex login`

### MCP Server Not Discoverable

**Problem:** Tools don't appear in OpenCode

**Solutions:**
- Check `~/.config/opencode/opencode.json` has registry config
- Restart OpenCode to reload MCP servers
- Test server directly: `bun run packages/mcp/src/index.ts`
- Check server logs for errors

### Schema Validation Errors

**Problem:** "Document doesn't match schema"

**Solutions:**
- Check all required fields are provided
- Verify field types match schema (string vs number)
- Use `v.optional()` for nullable fields
- Check array types: `v.array(v.string())`

### Task Creation Failures

**Problem:** "Failed to create task"

**Solutions:**
- Verify registryId exists (use `list_registries` first)
- Check required fields are provided (content, status, priority)
- Verify Convex connection is active
- Check projectContext is a valid string

## Integration with Other Systems

### OpenCode Sessions

**Purpose:** Track conversation history, link to tasks

**Flow:**
```
OpenCode starts → Create session record
Task created → Link to current sessionId
Session ends → Update stats (duration, tokens, files)
```

### Vault Articles

**Purpose:** Sync frontmatter metadata to registry

**Flow (Planned):**
```
Article saved → Extract frontmatter
Check slug exists → Update or create
Sync article_status → Track workflow
Link to tasks/courses → Bidirectional references
```

### Outlook Email

**Purpose:** Track correspondence, link to courses/articles

**Flow (Planned):**
```
Email received → Create registry record
Parse subject → Detect course/student
Link to courseId → Organize by context
Flag for follow-up → Task creation
```

## Configuration

**MCP Server Config:** `~/.config/opencode/opencode.json`

```json
{
  "mcp": {
    "registry": {
      "type": "local",
      "command": [
        "bun",
        "run",
        "/Users/ntiruviluamala/Code/github.com/theslyprofessor/registry/packages/mcp/src/index.ts"
      ],
      "enabled": true,
      "env": {
        "CONVEX_URL": "https://..."
      }
    }
  }
}
```

**Convex Config:** `registry/convex.json`

```json
{
  "project": "registry-project",
  "team": "theslyprofessor",
  "prodUrl": "https://..."
}
```

## Best Practices

### Task Management

1. **Use projectContext:** Group related tasks (e.g., "nnt-compiler", "registry", "swc-teaching")
2. **Set priority appropriately:** Reserve "high" for urgent work
3. **Link to articles:** Use articleId (slug) for documentation context
4. **Update status frequently:** Keep registry current with task progress
5. **High-level only:** Registry is for ideas and high-level tasks, not detailed AI coding tasks (use Beads/OpenSpec for those)

### Article Tracking

1. **Use slug as ID:** Never change slugs (breaks links)
2. **Track status progression:** draft → ... → published
3. **Set visibility correctly:** Private for `_` folders
4. **Link related content:** Tasks, courses, emails

### Schema Design

1. **Start with optional fields:** Easier to evolve
2. **Use references (IDs):** Link between tables
3. **Index query fields:** Add `.index()` for common filters
4. **Document relationships:** Comment foreign keys

### MCP Tool Design

1. **Clear descriptions:** Help OpenCode choose right tool
2. **Validate inputs:** Use Zod schemas strictly
3. **Return useful data:** Include IDs for follow-up actions
4. **Handle errors gracefully:** Return error messages, not exceptions

## Project Structure

```
registry/
├── convex/                    # Convex backend
│   ├── schema.ts             # Database schema (10 tables)
│   ├── tasks.ts              # Task mutations/queries
│   ├── articles.ts           # Article operations
│   └── ...                   # Other table logic
├── packages/
│   └── mcp/                  # MCP server
│       └── src/
│           └── index.ts      # Tool definitions
├── web/                      # React dashboard (planned)
├── convex.json               # Convex project config
└── package.json              # Dependencies
```

## See Also

- **Related Skills:**
  - `obsidian-workflows` - Vault management and article creation
  - `swc-teaching` - Course/quiz workflows
  - (Note: For AI coding tasks, see Beads or OpenSpec - separate systems)
  
- **Related AGENTS.md:**
  - `~/Code/github.com/theslyprofessor/registry/AGENTS.md` - Full project docs
  
- **External Resources:**
  - [Convex Documentation](https://docs.convex.dev)
  - [MCP Specification](https://spec.modelcontextprotocol.io)

## Quick Reference

### Essential Commands

```bash
# Start development
cd ~/Code/github.com/theslyprofessor/registry
bun convex dev

# Test MCP server
cd packages/mcp && bun run src/index.ts

# Deploy schema changes
# (Auto-deploys on save in dev mode)

# Re-authenticate
bunx convex login
```

### Key Concepts

- **Slug = Article ID** (always)
- **article_status ≠ HIL** (different workflows)
- **Tasks link to articles** (via articleId/slug)
- **High-level task tracking** (detailed AI tasks → Beads/OpenSpec)
- **Optional fields are safe** (no migrations needed)
- **MCP tools auto-discover** (restart OpenCode)
