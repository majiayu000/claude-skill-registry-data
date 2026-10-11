---
name: postgres-rls-mutation-hardening
description: "Audit and prove fixes for Postgres/Supabase UPDATE-policy holes where a row's identity columns can be rewritten by a legitimate updater — covers the WITH CHECK cannot see OLD trap, the before-update trigger that actually enforces immutability, and proving the exploit dead by running it inside a rolled-back transaction as a real authenticated role. Use when auditing RLS on any table whose rows grant access to other rows (friendships, memberships, shares, invites)."
---

# Postgres RLS mutation hardening

RLS audits usually check "can a stranger SELECT this?". The higher-yield hole is
an **UPDATE policy that pins the wrong column**, letting a legitimate updater
rewrite the row's *identity* and thereby grant themselves access to someone
else's data.

Applies to any table where a row is itself a grant: friendships, memberships,
team/org invites, shares, ACL rows.

## 1. The bug shape

```sql
create policy friendships_accept on friendships
    for update to authenticated
    using       (addressee_id = auth.uid())
    with check  (addressee_id = auth.uid());
```

Reads as "only the addressee may accept". It actually means "the addressee may
rewrite **any other column**, including `requester_id`".

Exploit: anyone who ever sent you a request leaves a row where you are the
addressee. Update it, repoint `requester_id` at a stranger, set `accepted` true.
If visibility is decided by a helper like:

```sql
is_friend(a,b) -- accepted row in EITHER direction
can_view(owner) -- public OR (friends AND is_friend(auth.uid(), owner))
```

…the attacker now passes `can_view` for a victim who never consented, and reads
every table gated on it (profile, sessions, history).

**Generalise the check:** for every `for update` policy, ask *which columns can
change*, not *who may update*. Any column that appears in a grant predicate
(`is_friend`, `is_member`, `owner_id`) must be immutable.

## 2. Why `with check` cannot fix it

`with check` sees only the **NEW** row. It can assert `addressee_id = auth.uid()`
but can never compare NEW to OLD, so it cannot detect a rewritten identity
column. Do not accept a policy-only "fix" — verify the mechanism.

The enforcement is a row-level trigger:

```sql
create or replace function friendships_no_identity_swap()
returns trigger language plpgsql security definer set search_path = public as $$
begin
    if new.requester_id is distinct from old.requester_id
       or new.addressee_id is distinct from old.addressee_id then
        raise exception 'friendship rows are immutable except for accepted';
    end if;
    return new;
end;
$$;

create trigger friendships_guard_update
    before update on friendships
    for each row execute function friendships_no_identity_swap();
```

Fire it for *all* updaters (including service role) so the invariant is a
property of the table, not of one policy.

## 3. Prove the exploit is dead — do not reason about it

Reasoning is not evidence, and a vacuous test passes for the wrong reason (no
matching precondition row exists → `UPDATE 0` → looks blocked). **Create the
precondition explicitly**, attack, and roll back:

```sql
begin;
-- setup as owner: victim's request lands with the attacker as addressee
insert into friendships (requester_id, addressee_id, accepted)
values ('<third-party>','<attacker>', false) on conflict do nothing;
select 'precondition rows: ' || count(*) from friendships
 where addressee_id = '<attacker>';

set local role authenticated;
set local request.jwt.claims = '{"sub":"<attacker>","role":"authenticated"}';

savepoint atk;
update friendships set requester_id = '<victim>', accepted = true
 where addressee_id = '<attacker>';      -- MUST raise
rollback to atk;

-- the legitimate action must still work
update friendships set accepted = true
 where requester_id = '<third-party>' and addressee_id = '<attacker>';
select 'legit accept: ' || count(*) from friendships
 where addressee_id = '<attacker>' and accepted;
rollback;
```

Pass = attack raises the exception AND the legitimate accept reports 1. Both
halves matter: a fix that blocks the attack by breaking the feature is not a fix.

Traps:
- `set local` outside a transaction only warns and runs as **owner**, silently
  bypassing RLS — always `begin;` first, and treat `WARNING: SET LOCAL can only
  be used in transaction blocks` as "this test proved nothing".
- Verify the precondition count is non-zero before believing `UPDATE 0`.

## 4. Companion checks on the same table

- **Pair uniqueness.** A PK of `(a_id, b_id)` does NOT stop both directions
  existing. Enforce with
  `unique index on (least(a_id,b_id), greatest(a_id,b_id))`, and delete existing
  duplicates first or the index creation fails on live data. State the keep-rule
  and make the comparison match it — `(accepted, created_at) < (…)` deletes the
  *oldest* row, which is usually the opposite of what the comment claims.
- **Unbounded user text** that surfaces in a shared feed: add
  `check (char_length(col) <= N)`, truncating offenders in the same migration so
  the constraint can be added.

## 5. Applying it

Migrations touching live data need explicit per-run consent, and destructive
steps must be named — a dedupe `delete` is not covered by "apply the migration".
Make every statement idempotent (`drop … if exists`, `if not exists`, guarded
`do $$` blocks) so a re-run is safe.
