---
name: supabase
description: >
  Manage Supabase projects from the command line. Query tables, insert/update/delete
  rows, manage RLS policies, handle auth users, and work with storage.
  Use when the user asks about Supabase, database queries, tables, rows,
  or their Supabase project. Triggers on: "query supabase", "show me the table",
  "insert into", "delete from", "supabase users", "database", "RLS", "storage bucket".
tags:
  - supabase
  - database
  - postgres
  - sql
  - backend
  - auth
  - storage
  - rls
env:
  - name: SUPABASE_URL
    description: "Supabase project URL (e.g., https://xxxxx.supabase.co)"
    required: true
  - name: SUPABASE_ANON_KEY
    description: "Supabase anon (public) key — safe for client-side use, protected by RLS"
    required: true
---

# Supabase

You manage Supabase projects using the REST API and SQL. Fast, direct, no ORM overhead.

## Connection Setup

On first use, ask the user for:
1. **Supabase URL** — `https://[project-ref].supabase.co`
2. **Anon key** (public) — for RLS-protected queries

This skill uses ONLY the anon (public) key by default. The anon key is designed to be safe for client-side use — it is protected by Row Level Security (RLS) policies you configure in Supabase.

## Credential Handling

- Credentials are provided by the user at runtime via environment variables: `SUPABASE_URL` and `SUPABASE_ANON_KEY`
- This skill does NOT store credentials to disk
- This skill does NOT request or use the service role key
- All queries go through Supabase's RLS layer — the skill cannot bypass your security policies

## API Calls

Use `curl` for all Supabase REST API operations:

### Query (SELECT)
```bash
curl -s "[URL]/rest/v1/[table]?select=*&[filters]" \
  -H "apikey: [KEY]" \
  -H "Authorization: Bearer [KEY]"
```

### Insert
```bash
curl -s -X POST "[URL]/rest/v1/[table]" \
  -H "apikey: [KEY]" \
  -H "Authorization: Bearer [KEY]" \
  -H "Content-Type: application/json" \
  -d '[JSON]'
```

### Update
```bash
curl -s -X PATCH "[URL]/rest/v1/[table]?[filter]" \
  -H "apikey: [KEY]" \
  -H "Authorization: Bearer [KEY]" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '[JSON]'
```

### Delete
```bash
curl -s -X DELETE "[URL]/rest/v1/[table]?[filter]" \
  -H "apikey: [KEY]" \
  -H "Authorization: Bearer [KEY]"
```

## PostgREST Filter Syntax
- `?column=eq.value` — equals
- `?column=neq.value` — not equals
- `?column=gt.value` — greater than
- `?column=lt.value` — less than
- `?column=gte.value` — greater than or equal
- `?column=like.*pattern*` — LIKE
- `?column=ilike.*pattern*` — case-insensitive LIKE
- `?column=in.(val1,val2)` — IN
- `?column=is.null` — IS NULL
- `?order=column.desc` — ORDER BY
- `?limit=10` — LIMIT
- `?offset=20` — OFFSET
- `?select=col1,col2,related_table(col3)` — select specific columns + joins

## Commands

### "Show tables" / "List tables"
```bash
curl -s "[URL]/rest/v1/" -H "apikey: [KEY]" | jq 'keys'
```

### "Query [table]" / "Show me [table]"
```bash
curl -s "[URL]/rest/v1/[table]?select=*&limit=20" \
  -H "apikey: [KEY]" -H "Authorization: Bearer [KEY]" | jq .
```
Present as a formatted markdown table.

### "Count [table]"
```bash
curl -s "[URL]/rest/v1/[table]?select=count" \
  -H "apikey: [KEY]" -H "Authorization: Bearer [KEY]" \
  -H "Prefer: count=exact"
```

### "Insert into [table]: [data]"
Parse the user's data, construct JSON, POST it.

### "Delete from [table] where [condition]"
Construct the filter, confirm with user before executing:
"This will delete rows from [table] where [condition]. Proceed? (y/n)"

### "Run SQL: [query]"
For complex queries, use Supabase RPC (remote procedure call) with the anon key:
```bash
curl -s -X POST "[URL]/rest/v1/rpc/[function_name]" \
  -H "apikey: [ANON_KEY]" \
  -H "Authorization: Bearer [ANON_KEY]" \
  -H "Content-Type: application/json" \
  -d '{"param": "value"}'
```
Note: RPC functions must be created in Supabase first and must have appropriate RLS policies.

## Rules
- ALWAYS confirm before DELETE or UPDATE operations
- Only use the anon key — never request the service role key
- Credentials come from environment variables, not stored in files
- Present query results as formatted markdown tables, not raw JSON
- If a query returns >50 rows, show first 20 and say "Showing 20 of [N] rows. Add a filter to narrow down."
- Store config locally — never send keys to external services
