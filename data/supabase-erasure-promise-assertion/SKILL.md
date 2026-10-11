---
name: supabase-erasure-promise-assertion
description: "Prove an app's \"delete my cloud data\" promise actually erases everything, by asserting the cascade in SQL against a real Postgres — covers the silent orphan case a schema review misses, the two different failure shapes, and keeping the assertion re-runnable. Use when a privacy policy or Play Data Safety sheet claims in-app deletion, or after adding any table to a Supabase schema."
---

# Asserting an erasure promise

A privacy policy or Data Safety sheet that says "you can delete your cloud data"
is a load-bearing claim. The usual evidence — an `on delete cascade` in the
schema and a button in the UI — does not prove it, because the dangerous
regression is a table added **later** without the cascade.

## Why a schema review is not enough

Two regressions, and only one is loud:

| regression | symptom |
|---|---|
| cascade replaced by a plain FK | `ERROR: update or delete on table "profiles" violates foreign key constraint` — the delete is refused, impossible to miss |
| FK removed entirely / table never referenced owner | **silent**: the profile row disappears, the app reports success, and the user's rows sit orphaned forever |

The second is the one that ships. It cannot be caught by reading migrations
one at a time, because the omission is in the *newest* file.

## The assertion

Put it at the end of the backend assertion suite, after the fixtures exist.
Delete as the **user themself** (via RLS), not as the migration owner —
deleting as owner proves nothing about what the app can do:

```sql
set local role authenticated;
perform set_config('request.jwt.claims', json_build_object('sub', victim)::text, true);
delete from profiles where id = victim;
reset role;
perform assert_true(
    (select count(*) from sessions where user_id = victim) = 0
        and (select count(*) from child_rows c
             where exists (select 1 from sessions x
                           where x.id = c.session_id and x.user_id = victim)) = 0
        and (select count(*) from every_other_user_table where user_id = victim) = 0,
    'erasing a profile left rows behind in another table'
);
```

Enumerate the tables from the migrations rather than memory:

```bash
grep -h "create table" supabase/migrations/*.sql
grep -h "on delete cascade" supabase/migrations/*.sql
```

Tables reachable only indirectly (child rows keyed by `session_id`, not
`user_id`) need the `exists (...)` form — a direct `user_id` filter silently
passes because the column does not exist on them.

## Prove it fires, both ways

Against a throwaway Postgres, reopen each hole in turn:

```bash
# loud shape: cascade downgraded to a plain reference
psql -c "alter table t drop constraint t_user_id_fkey;
         alter table t add constraint t_user_id_fkey
             foreign key (user_id) references profiles(id);"
# expect: delete refused with a foreign-key error

# silent shape: no constraint at all
psql -c "alter table t drop constraint t_user_id_fkey;"
# expect: ASSERTION FAILED: erasing a profile left rows behind in another table
```

If only the loud shape was tested, the assertion has not been shown to do
anything the database was not already doing.

## Keep it re-runnable

The assertion **deletes a fixture**, so the suite must recreate it. Run the
whole file three times in a row on one database and expect the same pass each
time; fixtures need `insert ... on conflict do update`, not
`insert ... on conflict do nothing`, or the second run asserts against rows
that were never restored.

## Then fix the document, not just the code

Upgrade the claim in the policy/Data Safety sheet from an assertion of fact to
a reference to the check, e.g. "asserted in `supabase/test/assert_all.sql`".
Note separately what deletion does **not** cover — an auth identity (email)
usually needs service-role credentials, so it is a server-side action by the
project owner rather than something the app can offer.
