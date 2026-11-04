---
name: supabase
description: >-
  Use when working with Supabase database, auth, migrations, edge functions, or advisors via Supabase MCP or plugin skills.
---

# Supabase

Thin adapter for digital workers. See `skills/org/TOOL-REGISTRY.md`.

## Preferred access
Supabase MCP + `skills/plugins/supabase/`

## Env / secrets
`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `DATABASE_URL`

Resolve via `skills/integrations/obsidian-secrets/` then `.env.local`.

## MCP
`plugin-supabase-supabase`, `user-supabase`

## Primary ops
1. list_tables / get_advisors before schema changes
2. Prefer local CLI + migrations for durable changes
3. Never expose service role key to client code

## Fallback
Supabase CLI / SQL against DATABASE_URL

## Common failures
Apply migration carefully on remote — confirm project first
