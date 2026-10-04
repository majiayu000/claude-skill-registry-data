---
name: prod-debug
description: Production debugging skill. Pre-loads DB schema, container registry, and prod environment facts from .claude/prod-debug/ in the current project root. Use when the user invokes /prod-debug or /prod-debug bootstrap.
---

# prod-debug

## Invocation

Two modes:

- `/prod-debug` — load context and enter debugging mode
- `/prod-debug bootstrap` — (re)build schema.md and containers.md from source files

---

## On `/prod-debug`

### Step 1: Find project root

Determine the project root — use the current working directory, or if inside a git repo, use `git rev-parse --show-toplevel`.

### Step 2: Check for data directory

Check whether `.claude/prod-debug/config.json` exists at the project root.

- If **missing**: tell the user that prod-debug is not set up for this project yet, and suggest running `/prod-debug bootstrap` after creating `.claude/prod-debug/config.json`.
- If **present**: continue to Step 3.

### Step 3: Load context files

Read all three data files using the Read tool:

1. `{project_root}/.claude/prod-debug/schema.md`
2. `{project_root}/.claude/prod-debug/containers.md`
3. `{project_root}/.claude/prod-debug/prod-env.md`

If any file is missing, note it and proceed with what's available.

### Step 4: Check schema staleness

Run:

```bash
~/.trimkit/bin/trimkit-prod-debug-staleness {project_root}
```

It compares the newest migration matching `migrations.glob` against the `prod-debug:last-migration` marker in schema.md. It prints nothing (exit 0) when schema.md is current, and a one-line warning (exit 1) when it is stale or has no marker, e.g.:

```
[prod-debug] schema.md is stale (068_foo.sql vs 085_bar.sql) — run /prod-debug bootstrap.
```

If it prints a warning, include it verbatim at the top of the Step 5 announcement. If it exits 2 (or any other code), report its stderr verbatim instead: config.json or schema.md is unreadable, and the auto-sync hook is also disabled until that's fixed.

The check reads the local checkout the glob points at. Migrations merged by others don't show up until that checkout is pulled. Don't bootstrap automatically; offer to. If the script is not installed, do the same comparison by hand: newest matching migration filename vs the marker.

### Step 5: Announce

Report a brief summary:
```
Prod-debug loaded.
  Schema: {N} tables (through {last-migration marker, or "unknown" if absent})
  Containers: {M} services
  Env: {hostname or domain from prod-env.md}
Ready — ask me to query the DB, inspect logs, or diagnose an issue.
```

### Step 6: Enter debugging mode

Use the loaded context to assist with:

**DB queries** — Build SQL using the pre-loaded schema. No `\d` or `INFORMATION_SCHEMA` queries needed — the schema is already in context. For queries on remote prod, prefix with the SSH + docker exec command from prod-env.md.

**Container operations** — Use container names and commands from containers.md. Common patterns:
- View logs: `docker logs {service} --tail 100 -f`
- Shell in: `docker exec -it {service} sh` (or bash)
- Restart: `docker restart {service}`

**SSH to prod** — Use the SSH alias/command from prod-env.md. Remote docker commands are typically run via `ssh {alias} docker ...`

**Stale schema** — If the user mentions a table or column that isn't in schema.md, flag it and suggest running `/prod-debug bootstrap` to rebuild from migrations.

---

## On `/prod-debug bootstrap`

This rebuilds the data files from source. Run when setting up a new project or when schema.md/containers.md have drifted.

### Step 1: Read config

Read `{project_root}/.claude/prod-debug/config.json`. It has this shape:

```json
{
  "migrations": {
    "glob": "src/db/migrations/*.sql"
  },
  "containers": {
    "composeFiles": [
      "docker-compose.yml",
      "../path/to/compose.production.yaml"
    ]
  }
}
```

### Step 2: Build schema.md

1. Find all migration files matching `migrations.glob` (resolved from project root)
2. Read them **in natural filename order**: compare numeric runs as numbers, so `100_x.sql` comes after `99_y.sql`. This is the same order `trimkit-prod-debug-staleness` uses to find the newest migration.
3. Parse each migration to extract DDL: `CREATE TABLE`, `ALTER TABLE ADD COLUMN`, `ALTER TABLE DROP COLUMN`, `CREATE INDEX`, `CREATE EXTENSION`
4. Build a cumulative schema — start from empty, apply each migration in sequence
5. Write the result to `{project_root}/.claude/prod-debug/schema.md`

**Output format for schema.md:**

```markdown
# DB Schema
<!-- Last bootstrapped: {ISO date} from {N} migrations -->
<!-- prod-debug:last-migration: {basename of the newest migration file, e.g. 085_add_widgets.sql} -->

## Extensions
- pgvector
- pgAudit

## TABLE: {table_name}
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PRIMARY KEY | |
| ... | | | |

**Indexes:**
- {index_name} ON ({columns}) [{UNIQUE}]

---
```

One section per table, ordered by first appearance in migrations.

The `prod-debug:last-migration` line is machine-read by `trimkit-prod-debug-staleness`. Always write it, exactly in that form, with the newest migration's basename ("newest" = last in natural filename order).

### Step 3: Build containers.md

1. Read each file in `containers.composeFiles` (resolved from project root)
2. Parse service definitions: service name, image or build context, ports, key environment variables, healthcheck
3. Write to `{project_root}/.claude/prod-debug/containers.md`

**Output format for containers.md:**

```markdown
# Container Registry
<!-- Last bootstrapped: {ISO date} -->

## {service_name}

- **Image/Build:** {image or Dockerfile path}
- **Ports:** {host:container mappings}
- **Key env vars:** {comma-separated list of var names, not values}
- **Healthcheck:** {healthcheck command or "none"}

**Commands:**
- Logs: `docker logs {service_name} --tail 100 -f`
- Shell: `docker exec -it {service_name} sh`
- Restart: `docker restart {service_name}`

---
```

### Step 4: Check prod-env.md

If `prod-env.md` does not exist, print a reminder:

```
Bootstrap complete. One more step:
  Create .claude/prod-debug/prod-env.md with your production environment facts.
  This file is written by hand — it captures things not in any config file:
  SSH alias, domain, VPS specs, key env var names, etc.

  Template:
  # Prod Environment
  - SSH: ssh <alias> (port <port>)
  - Domain: https://<domain>
  - Health check: curl https://<domain>/api/health
  - VPS: <provider>, <region>, <instance type>
  - DB connect: docker exec -it <postgres-container> psql -U $DB_USER -d <dbname>
  - Key env vars: <list var names>
```

---

## Hook integration

When the `prod-debug.sh` PostToolUse hook fires after a migration or compose file is written, it prints an update instruction to stdout. You will see it as context in the same response. Act on it immediately:

- **Migration update instruction** → read the new migration file and apply the delta to `schema.md` (add new table or columns, note dropped columns). If the migration sorts after the current `prod-debug:last-migration` marker, update the marker to its basename.
- **Compose update instruction** → re-read the relevant compose file and update the affected service entry in `containers.md`

Do these updates inline without waiting to be asked — the point is that schema.md stays in sync automatically.

The hook is worktree-aware. `config.json` globs usually point into a main checkout (e.g. `repos/app/src/db/migrations/*.sql`), but the hook also fires for writes inside a linked git worktree of that repo (e.g. `worktrees/app-feat/src/db/migrations/086_x.sql`). It maps the path back to the main checkout before matching. Migrations that arrive only via `git pull` still skip the hook. The Step 4 staleness check catches those.
