---
name: heroku-key-value-store
description: Operate Heroku Key-Value Store with a read-only-first workflow. Use when the agent needs to inspect Redis-backed state, review credentials, promote a store, tune maxmemory or timeout policies, configure keyspace notifications, or reason about Heroku Key-Value Store operational guardrails.
---

# Heroku Key-Value Store

Manage Heroku Key-Value Store safely by separating read-only inspection from state-changing operations.

## Start with store inspection

Resolve this installed skill's directory first. Do not assume the current workspace contains the skill source repository.

Run the bundled helper from this skill's `scripts/` directory:

```bash
python3 /path/to/heroku-key-value-store/scripts/store_snapshot.py --app <app>
```

If no app is known yet, run it without `--app` to inspect CLI readiness only.

## Read-only-first flow

Begin with:

- `heroku redis:info -a <app> --json`
- `heroku redis:credentials -a <app>`
- `heroku redis:wait -a <app>`

Use these results to confirm:

- which add-on is primary
- whether credentials are healthy
- whether the store is available before proposing a change

## Current connection guidance

- Treat `REDIS_URL` as the current TLS connection variable.
- Do not recommend `REDIS_TLS_URL` or `REDIS_TEMPORARY_URL`; they are obsolete guidance for current Heroku Key-Value Store workflows.
- Avoid printing raw credentials or connection URLs unless the user explicitly asks.

## Change operations

Ask for confirmation before:

- `redis:credentials --reset`
- `redis:promote`
- `redis:maxmemory`
- `redis:timeout`
- `redis:keyspace-notifications`
- `redis:upgrade`
- plan or add-on changes managed through `addons:*`

After a change, re-check `redis:info`, `redis:wait`, and any app behavior that depends on `REDIS_URL`.

## References

- Read `references/key-value-store.md` for connection notes, operational guardrails, and source links.
