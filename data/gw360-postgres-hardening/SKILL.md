---
name: postgres-hardening
description: Harden a PostgreSQL deployment whether managed or self-hosted. Covers pg_hba network and authentication rules, role separation (read-only, read-write, migration), row-level security for multi-tenant data, TLS configuration, backup encryption, and pg_audit logging. Invoke when provisioning a new Postgres, before opening it to a new app, or when reviewing a multi-tenant schema for isolation gaps.
---

# PostgreSQL Hardening

A practical baseline for a single Postgres instance (self-hosted or managed) that backs a web app. Skews toward small-team realities — not a regulated-environment DBA's playbook.

## When to invoke

- New Postgres provisioned (Docker, package, RDS, Supabase, Neon — same threat model)
- Inheriting an existing Postgres with no documented hardening
- Adding a new application or service that connects to an existing Postgres
- After a Postgres security advisory
- Reviewing a multi-tenant schema where one tenant should not see another's data
- Planning a major-version upgrade (14 → 15 → 16 → 17)

## Step 1 — Network reachability

Postgres listening on `0.0.0.0:5432` open to the internet is one of the most common misconfigurations in shared/cloud environments.

```bash
# What is the listener bound to?
sudo ss -tlnp | grep 5432

# From outside the VPS — can the world reach it? (this should fail)
nc -zv <vps-ip> 5432
```

Acceptable bindings:

- `127.0.0.1` only — app on same host, no remote access (best for single-VPS deployments)
- VPC-internal IP only — apps in same private network
- Public IP **only with TLS-required + IP allowlist at firewall** — last resort, document why

In `postgresql.conf`:

```
listen_addresses = 'localhost'        # or 'localhost,10.0.0.5' for private LAN
port = 5432
```

Restart Postgres after change.

## Step 2 — `pg_hba.conf` (host-based auth)

This file is the primary access-control surface. Order matters: the first matching rule wins.

```
# TYPE    DATABASE        USER            ADDRESS         METHOD

# Local Unix socket — for admin tasks
local     all             postgres                        peer
local     all             all                             scram-sha-256

# App connections from same host
host      app_db          app_user        127.0.0.1/32    scram-sha-256
host      app_db          app_user        ::1/128         scram-sha-256

# Private LAN, TLS required
hostssl   app_db          app_user        10.0.0.0/24     scram-sha-256

# Read-only analytics user, scoped
hostssl   app_db          readonly_user   10.0.0.0/24     scram-sha-256

# Catch-all reject — explicit deny at the end
host      all             all             0.0.0.0/0       reject
host      all             all             ::/0            reject
```

Auth method recommendations:

- `scram-sha-256` for passwords (replaces older `md5`). Force this in `postgresql.conf`: `password_encryption = scram-sha-256`
- `peer` for the `postgres` superuser on the local socket — convenient and safe
- `cert` (client certificate) for service-to-service when feasible
- Never `trust` outside a freshly-isolated provisioning step

Apply: `SELECT pg_reload_conf();`

## Step 3 — Role separation

Default deployments use one all-powerful user for the app. Split the responsibilities:

```sql
-- Application owner — owns schema, runs migrations (used by CI / deploy, not the running app)
CREATE ROLE app_owner LOGIN PASSWORD :'pw_owner';
GRANT CONNECT ON DATABASE app_db TO app_owner;
GRANT CREATE ON DATABASE app_db TO app_owner;

-- Running app — read/write data only, no schema changes, no superuser anywhere
CREATE ROLE app_user LOGIN PASSWORD :'pw_app';
GRANT CONNECT ON DATABASE app_db TO app_user;
-- After schema is in place:
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;

-- Read-only — analytics, BI tools, AI agents reading prod
CREATE ROLE readonly_user LOGIN PASSWORD :'pw_ro';
GRANT CONNECT ON DATABASE app_db TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT ON TABLES TO readonly_user;
```

Benefits:

- An app SQL-injection cannot drop tables (only the migration role can)
- Analytics / LLM agents get `readonly_user` — they cannot accidentally mutate prod
- Credential rotation per role is independent

## Step 4 — Row-Level Security for multi-tenant data

If multiple tenants share tables, RLS makes tenant-isolation enforced by the database, not just the app.

```sql
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices FORCE ROW LEVEL SECURITY;   -- applies even to table owner

CREATE POLICY invoice_tenant_isolation ON invoices
  USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- In the app's connection setup, per request:
-- SET LOCAL app.current_tenant = '<uuid>';
```

Watch for:

- `BYPASSRLS` attribute on any role except a specific maintenance role — audit `SELECT rolname FROM pg_roles WHERE rolbypassrls;`
- Policies that only have `USING` and no `WITH CHECK` — `INSERT` may bypass the intended row constraint
- Connection pooling: if the same connection is reused across tenants, `SET LOCAL` discipline is mandatory; otherwise tenant data leaks across users

## Step 5 — TLS

```
# postgresql.conf
ssl = on
ssl_cert_file = '/etc/ssl/postgres/server.crt'
ssl_key_file  = '/etc/ssl/postgres/server.key'
ssl_min_protocol_version = 'TLSv1.2'
```

In `pg_hba.conf` use `hostssl` (not just `host`) for any non-localhost entry. Test from a client:

```bash
psql "host=db.example.com user=app_user dbname=app_db sslmode=verify-full sslrootcert=/path/to/ca.pem"
```

Client-side: app connection strings should set `sslmode=verify-full` in production — `require` (the common copy-paste) does not validate the cert.

## Step 6 — Backup + encryption

The backup story is part of the security story. A leaked plaintext dump is the same as a leaked database.

```bash
# Daily dump, gzip + age-encrypt before leaving the host
pg_dump -Fc app_db | gzip | age -r <recipient-public-key> > /backups/app_db-$(date +%F).sql.gz.age

# Upload encrypted backups to off-site storage (S3/R2/B2)
```

- Encrypt **before** the data leaves the host
- Test restore quarterly — a backup you have not restored is a wish, not a backup
- Retain a chain: daily 7 days, weekly 4 weeks, monthly 12 months — tune to your tolerance

## Step 7 — Audit logging

Built-in logging is good enough for most teams; `pg_audit` adds structured per-statement detail when needed.

```
# postgresql.conf
log_destination = 'stderr'
logging_collector = on
log_directory = '/var/log/postgresql'
log_filename = 'postgresql-%Y-%m-%d.log'
log_rotation_age = 1d
log_rotation_size = 100MB
log_min_duration_statement = 500ms     # slow-query log
log_connections = on
log_disconnections = on
log_statement = 'ddl'                  # log all DDL; 'all' is noisy but useful in regulated envs
log_line_prefix = '%m [%p] %q%u@%d '
```

For higher detail, install `pg_audit`:

```sql
CREATE EXTENSION pgaudit;
ALTER SYSTEM SET pgaudit.log = 'write, ddl';
SELECT pg_reload_conf();
```

Forward logs off-host so a compromise cannot wipe its own audit trail.

## Step 8 — Version upgrades

- **Pin to a major version intentionally**; do not let `docker pull postgres:latest` decide for you
- **Postgres has a 5-year support window per major version** — track end-of-life
- **Test upgrades on a copy of prod data**, not just an empty DB
- **`pg_upgrade` is the standard tool**; `pg_dump`/`pg_restore` for major version jumps if `pg_upgrade` not viable
- After an upgrade, `VACUUM ANALYZE` the whole DB before opening to traffic

## Step 9 — Common findings on inherited instances

When auditing a Postgres you did not provision, these are the high-frequency hits:

- `pg_hba.conf` has a `host all all 0.0.0.0/0 md5` line because some tutorial said so
- One `postgres` superuser is used for the running app
- TLS is off, or `sslmode=require` without `verify-full`
- No backups, or backups stored next to the database
- `log_statement = 'all'` left on with no rotation — disk fills, then either Postgres or alerts die
- A development seed user still exists with a weak password
- `BYPASSRLS` granted to the app role "for convenience"

Each is a finding; prioritize by exposure.

## Quick audit queries

```sql
-- Roles with login + superuser
SELECT rolname, rolsuper, rolcreatedb, rolcreaterole, rolbypassrls
FROM pg_roles WHERE rolcanlogin ORDER BY rolname;

-- Tables without RLS where you expect it
SELECT schemaname, tablename, rowsecurity
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY rowsecurity, tablename;

-- Extensions installed (audit periodically — unfamiliar extensions are suspicious)
SELECT name, installed_version FROM pg_available_extensions WHERE installed_version IS NOT NULL;

-- Recent failed connections (in the log) — set up a log-tail alert
-- grep 'authentication failed' /var/log/postgresql/*.log | tail
```

## What this skill will not do

- Help bypass Postgres authentication on systems you do not own
- Recommend `trust` auth or `host all all 0.0.0.0/0` outside an isolated provisioning step
- Replace a regulated-environment DBA's full hardening guide for HIPAA/PCI/etc.
