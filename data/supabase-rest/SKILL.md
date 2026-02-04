---
name: supabase-rest
description: Inspect Supabase database schemas and data. Use when the user asks to "check table", "list columns", or "query data" in Supabase. READ-ONLY.
allowed-tools: Bash
---

# Use Supabase (read-only)

## Instructions
1) Load env vars (without printing secrets): `set -a; source .env; set +a` or equivalent so `SUPA_URL` and `SUPA_SERVICE_ROLE_KEY` are set.
2) Never echo or log `SUPA_SERVICE_ROLE_KEY`; only pass it via headers.
3) Base headers for REST calls:
   - `-H "apikey: $SUPA_SERVICE_ROLE_KEY"`
   - `-H "Authorization: Bearer $SUPA_SERVICE_ROLE_KEY"`
   - `-H "Accept-Profile: ${SUPA_SCHEMA:-public}"`
   - Optional: add `-H "Prefer: count=exact"` when you need counts.
4) List tables (scoped by schema):
   ```bash
   curl -s "$SUPA_URL/rest/v1/pg_catalog.pg_tables?schemaname=eq.${SUPA_SCHEMA:-public}&select=schemaname,tablename,tableowner" \
     -H "apikey: $SUPA_SERVICE_ROLE_KEY" -H "Authorization: Bearer $SUPA_SERVICE_ROLE_KEY"
   ```
5) Inspect columns for a table:
   ```bash
   TABLE="your_table"
   curl -s "$SUPA_URL/rest/v1/information_schema.columns?table_schema=eq.${SUPA_SCHEMA:-public}&table_name=eq.${TABLE}&select=column_name,data_type,is_nullable,column_default,udt_name,character_maximum_length" \
     -H "apikey: $SUPA_SERVICE_ROLE_KEY" -H "Authorization: Bearer $SUPA_SERVICE_ROLE_KEY"
   ```
6) Pull sample rows (read-only) with sane limits/ordering:
   ```bash
   curl -s "$SUPA_URL/rest/v1/${TABLE}?select=*&limit=50&order=created_at.desc" \
     -H "apikey: $SUPA_SERVICE_ROLE_KEY" -H "Authorization: Bearer $SUPA_SERVICE_ROLE_KEY"
   ```
7) For joins or filters, use PostgREST query params (e.g., `?select=id,profile(id,name)&user_id=eq.123`). Keep requests GET/HEAD for read-only.
8) If `SUPA_HOST`, `SUPA_ORIGIN`, or `SUPA_REFERER` are set, include matching headers to satisfy Supabase CORS constraints.
9) Avoid writes (`POST/PATCH/DELETE`) unless explicitly asked; this skill is for inspection.

## Example prompts
- "Show the columns and types for table chat_logs in Supabase"
- "Fetch 20 newest rows from public.messages"
- "List all tables under the public schema"
