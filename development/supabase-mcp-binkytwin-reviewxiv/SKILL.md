---
name: supabase-mcp
description: Configure and use Supabase MCP from Claude Code to inspect and manage a Supabase project. Use when the user asks to create tables, migrations, RLS policies, storage buckets, or to query Supabase from Claude Code. Includes safe setup steps (project-scoped, dev-only, optional read-only).
---

# Supabase MCP for Claude Code

## Safety first (non-negotiable)
- Do **NOT** connect MCP to production data. Use a dev project/branch and non-sensitive data.
- Prefer **project scoping** so Claude cannot access other Supabase projects.
- If connecting to real data is unavoidable, use a **read-only** mode when available.

(These are recommended mitigations due to LLM prompt-injection risk and data exposure concerns.)

## Current project setup
This project is connected to Supabase MCP:
- Project ref: `iyyqdoahxhmdumojnqip`
- Status: Connected (project-scoped)

## Setup (reference)

### Option A — CLI (recommended)
Use Supabase remote MCP URL with project_ref (project-scoped):

```bash
# Add server (project scope) - replace PROJECT_REF:
claude mcp add --scope project --transport http supabase "https://mcp.supabase.com/mcp?project_ref=PROJECT_REF"
```

Then authenticate:
1. Run `claude /mcp`
2. Select `supabase` → Authenticate
3. Complete browser login (Supabase uses dynamic client registration)

### Option B — .mcp.json
Create `.mcp.json` at repo root:
See: [templates/mcp.supabase.project.json](templates/mcp.supabase.project.json)

## CI / headless authentication (optional)
If browser OAuth is not possible (CI), configure an access token header:
- Use `Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}` and `project_ref` env vars.

## How to use (prompting patterns)

When operating with Supabase MCP tools:

1. **Ask for schema introspection first** (tables, columns, RLS status)
2. **Propose a migration plan** before executing write operations
3. **If asked to run SQL**:
   - Generate SQL
   - Explain it
   - Then run it (only after confirmation if the action is destructive)

## Available MCP tools
- `list_tables` - List all tables in the database
- `get_table_schema` - Get schema for a specific table
- `execute_sql` - Execute SQL queries
- `list_storage_buckets` - List storage buckets
- `create_migration` - Create a new migration

## Output expectations
- Always provide the SQL/migration diff in the answer.
- Always mention what MCP tools were used and what changed.

## DeepRead Database Schema (reference)

### papers table
```sql
CREATE TABLE papers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  filename TEXT NOT NULL,
  file_path TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### paper_pages table
```sql
CREATE TABLE paper_pages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  paper_id UUID REFERENCES papers(id) ON DELETE CASCADE,
  page_number INTEGER NOT NULL,
  text_content TEXT,
  text_items JSONB,
  width FLOAT,
  height FLOAT,
  has_text BOOLEAN DEFAULT true
);
```

### highlights table
```sql
CREATE TABLE highlights (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  paper_id UUID REFERENCES papers(id) ON DELETE CASCADE,
  page_number INTEGER NOT NULL,
  start_offset INTEGER NOT NULL,
  end_offset INTEGER NOT NULL,
  color TEXT DEFAULT 'yellow',
  note TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### chat_messages table
```sql
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  paper_id UUID REFERENCES papers(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  citations JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```
