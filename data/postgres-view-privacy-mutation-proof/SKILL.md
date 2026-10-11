---
name: postgres-view-privacy-mutation-proof
description: "Use when adding or reviewing a Postgres/Supabase view (leaderboard, feed, board) over an RLS table, when a view leaks rows or a board reads empty for everyone, or when security_invoker=true is the only privacy evidence. Also when any privacy claim rests on a schema-level setting alone."
---

# Proving a view really hides rows

A view over an RLS-protected table is a privacy boundary. By default a view runs as
its owner, so it bypasses RLS and leaks every row unless it is created
`with (security_invoker = true)`. Schema-level checks are cheap and worth having,
but they do **not** prove the boundary holds. Read rows through the view, as real
roles.

## The schema-level check: necessary, not sufficient

Do NOT verify via `pg_class.relrowsecurity` — that column is always `f` for views
and proves nothing. Check `reloptions`:

```sql
select relname, reloptions from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public' and c.relkind = 'v';
-- expect {security_invoker=true}
```

## The two failure shapes a setting check misses

1. **Definer-wrapped board — leaks everything, setting still reads `true`.**
   ```sql
   create function all_board() returns setof profiles
     language sql stable security definer as $$ select * from profiles $$;
   create view leaderboard with (security_invoker = true) as
     select ... from all_board() p;      -- setting true, RLS bypassed inside
   ```
   Realistic because it arrives as a "fix" when a board looks empty.

2. **Narrowed predicate — board reads empty for everyone.**
   Tighten the visibility function (`can_view(owner) -> owner = auth.uid()`)
   and every *refusal* assertion still passes: nothing leaked, nothing worked.
   A suite that only asserts zeros passes a board that shows nobody anything.

## The assertion set

For each board, with real `set local role authenticated` + the probe uid:

| reader | expectation |
|---|---|
| stranger (no friendship) | **0** rows for the private hunter |
| accepted friend | **1** row — otherwise the zero above passes for the wrong reason |
| the reader themselves | **1** row |

The friend/self rows are the load-bearing half. Without them, mutation 2 is
invisible.

## Procedure

1. Throwaway database, migrations applied in order:
   ```bash
   docker run -d --rm --name pg -e POSTGRES_PASSWORD=probe postgres:16
   for i in $(seq 1 30); do docker exec pg pg_isready -U postgres && break; sleep 2; done
   for f in test/stub.sql migrations/*.sql; do
     docker exec -i pg psql -U postgres -q -v ON_ERROR_STOP=1 < "$f"
   done
   docker cp test/assert_all.sql pg:/tmp/a.sql
   docker exec pg psql -U postgres -v ON_ERROR_STOP=1 -f /tmp/a.sql
   ```
2. Add the assertions; confirm green.
3. **Mutate and attribute.** Apply each mutation with `psql -qc`, re-run, and
   record *which* assertion caught it — existing or new:
   - drop `security_invoker` from the view
   - broaden the visibility predicate to `select true`
   - wrap the board in a `SECURITY DEFINER` function
   - narrow the predicate to self-only
   Expect some to be caught by checks that already existed. Say so; the new
   coverage is only what the last two prove.
4. Restore each mutation immediately (`create or replace` back), and re-run the
   whole suite **three times**. The checks mutate the rows they depend on, so
   fixtures need `on conflict do update` or the suite poisons itself.
5. Tear the container down.

## Traps

- **Attribute the catch, don't assume it.** Grep the failure message; a
  pre-existing table-level assertion often fires first and hides whether the
  new one works at all.
- **Don't claim counts you didn't measure.** `grep -c assert_true` includes the
  helper's own definition; count `perform assert_true(` call sites.
