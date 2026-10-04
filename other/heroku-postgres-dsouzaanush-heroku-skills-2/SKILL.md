---
name: heroku-postgres
description: Operate Heroku Postgres with a safe inspection-first workflow. Use when the agent needs to provision, inspect, attach, promote, back up, restore, diagnose, or reason about credentials and data movement for Heroku Postgres.
---

# Heroku Postgres

Manage Heroku Postgres by separating inspection from destructive database changes.

## Start with a database snapshot

Resolve this installed skill's directory first. Do not assume the current workspace contains the skill source repository.

Run the bundled helper from this skill's `scripts/` directory:

```bash
python3 /path/to/heroku-postgres/scripts/postgres_snapshot.py --app <app>
```

If no app is known yet, run it without `--app` to inspect CLI and auth readiness only.

## Read-only-first flow

Begin with:

- `heroku pg:info -a <app>`
- `heroku pg:backups -a <app>`
- `heroku pg:credentials -a <app>`
- `heroku pg:psql -a <app>` only when the user explicitly wants direct SQL inspection
- `heroku pg:diagnose -a <app>` when available and appropriate

Use the inspection results to identify the attached database, the current role of each attachment, and the backup posture before proposing a change.

## Change operations

Ask for confirmation before:

- provisioning a new database
- promoting a follower or attachment
- restoring a backup
- rotating credentials
- unlinking or destroying a database
- running `pg:push` or `pg:reset`

When moving data, explain source, destination, downtime risk, and rollback posture first.

## Secret handling

- Do not print database URLs unless the user explicitly asks for them.
- Prefer credential rotation workflows over sharing long-lived credentials.
- Summarize attachment names and roles without exposing secrets.

## References

- Read `references/postgres-ops.md` for command catalogs, safety gates, and source links.
