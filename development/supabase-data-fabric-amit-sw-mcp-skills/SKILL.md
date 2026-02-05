---
name: supabase-data-fabric
description: Use when Codex needs to query Supabase Postgres, manage auth, or trigger Edge Functions via the Supabase MCP server.
---

# Supabase Data Fabric

## Purpose
Provide a repeatable workflow for reading/writing Supabase data and invoking project automation endpoints through the hosted server configured in `servers/supabase`.

## Setup Checklist
1. Export `SUPABASE_PROJECT_REF` and `SUPABASE_ACCESS_TOKEN` (service role or personal access token).
2. Confirm row-level security policies allow the automation key to perform the planned operations.
3. Sync table schemas into `docs/supabase/schema.md` whenever the database changes (manual step).

## Environment Loading
If `SUPABASE_PROJECT_REF` or `SUPABASE_ACCESS_TOKEN` are not present, source `load_env.sh` from the repository root before invoking MCP tools.

## Workflow
1. **Clarify** – define the exact SQL or auth change needed and the safety checks (e.g., limit clause, expected row count).
2. **Prepare** – if making schema changes, draft the SQL inside `packages/migrations/` and have reviewers sign off before execution.
3. **Execute** – call the MCP `query`, `functionCall`, or `auth` tools. Always pass an explicit `timeoutSeconds`.
4. **Verify** – re-run a read-only query or health check to confirm the change took effect.

## Notes
- Avoid destructive statements without a backup; prefer temporary tables or `BEGIN; ...; ROLLBACK` dry runs first.
- Document every data change in pull requests or `docs/changelog.md` for auditability.
- Rotate service-role or access tokens quarterly and update `SUPABASE_ACCESS_TOKEN` in the deployment pipeline.
