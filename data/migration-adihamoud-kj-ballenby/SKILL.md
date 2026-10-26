---
name: migration
description: Create a new Supabase migration with RLS policies, update the hand-written Database types and the data model doc. Use for any schema change.
---

1. Create `supabase/migrations/<YYYYMMDDHHMMSS>_<snake_name>.sql` (UTC timestamp). Never edit an
   existing migration.
2. In the file: tables with `venue_id` + FK + `created_at`/`updated_at`, the `set_updated_at`
   trigger, indexes for every FK you will filter on, `enable row level security`, and policies
   using `public.is_venue_staff(...)` / `public.is_night_participant(...)`. If the UI subscribes to
   the table, add it to `supabase_realtime`. End with a `-- down:` comment describing manual
   rollback.
3. Update `packages/db/src/database.types.ts`: add the `Row` interface and the `Tables` entry.
4. Update `docs/DATA_MODEL.md`: column table, RLS summary, and the Mermaid diagram.
5. If Docker is available: `pnpm db:reset` and then `pnpm db:types` to regenerate types and
   confirm they match your hand-written version. If not, say so in the PR.
6. Run `pnpm check`.
