---
name: superpowers-sage:wp-cli-ops
description: >
  WP-CLI operations via Lando — lando wp db export, lando wp db import,
  lando wp search-replace, lando wp search-replace --dry-run, lando wp user create,
  lando wp post list, lando wp plugin install, database management,
  maintenance mode, lando wp maintenance-mode activate, lando wp cache flush,
  lando wp cron event run, lando wp option update, lando wp transient delete,
  deploy checklist, preflight checks, destructive operations safety
user-invocable: false
---

# WP-CLI Operations via Lando

## When to use

- Performing database operations (export, import, optimize, search-replace)
- Managing plugins, themes, or users from the command line
- Running maintenance tasks (cache flush, rewrite flush, cron)
- Building or executing deployment scripts
- Troubleshooting WordPress configuration issues

## Inputs required

- The specific operation to perform
- For search-replace: old and new values, scope (all tables or specific)
- For user management: user details (email, role, username)
- For deploy scripts: target environment and deployment steps
- Confirmation that backups exist before destructive operations

## Procedure

**All WP-CLI commands must be prefixed with `lando wp`** to execute inside the Lando container.

### Database operations

See [`references/db-operations.md`](references/db-operations.md) for export, import, and search-replace workflows.

Quick reference:

```bash
# Export backup
lando wp db export "backup-$(date +%Y%m%d-%H%M%S).sql"

# Search-replace (always dry-run first)
lando wp search-replace 'https://old.com' 'https://new.com' --dry-run --precise --all-tables
lando wp search-replace 'https://old.com' 'https://new.com' --precise --all-tables
```

Scripts: [`scripts/db-backup.sh`](scripts/db-backup.sh) and [`scripts/search-replace.sh`](scripts/search-replace.sh).

### User and content operations

See [`references/content-ops.md`](references/content-ops.md) for user management, post operations, and option manipulation.

Quick reference:

```bash
lando wp user create <username> <email> --role=<role> --user_pass=<password>
lando wp post list --post_type=<type> --fields=ID,post_title
lando wp option update my_option '{"key":"value"}' --format=json
```

### Maintenance and deploy operations

See [`references/maintenance-deploy.md`](references/maintenance-deploy.md) for the full deploy sequence.

Quick reference:

```bash
lando wp maintenance-mode activate
lando wp cache flush
lando wp transient delete --all
lando wp rewrite flush
lando wp maintenance-mode deactivate
```

### Preflight checks for destructive operations

See [`references/preflight-checks.md`](references/preflight-checks.md) for mandatory checks before any destructive WP-CLI command.

Key rules:
1. Always back up first: `lando wp db export`
2. Always dry-run search-replace before applying
3. Use `--format=json` when updating serialized options
4. Pipe post content via stdin to avoid backslash stripping

### Custom Acorn CLI commands

```bash
lando wp acorn <command-name>
lando wp acorn list
```

Cross-reference the **acorn-commands** skill for creating and running custom Acorn artisan commands within Lando.

## Verification

- [ ] Dry-run output reviewed before executing any search-replace
- [ ] Database backup exists before any destructive operation
- [ ] Plugin/theme activation confirmed with `lando wp plugin list` or `lando wp theme list`
- [ ] Cron events listed and verified after scheduling changes
- [ ] Rewrite rules flushed after permalink or route changes
- [ ] Cache cleared after configuration or content changes
- [ ] Deploy script steps completed without errors

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| `lando wp` command not found | Lando not running or misconfigured | Run `lando start`, check `.lando.yml` tooling |
| Search-replace corrupts serialized data | Missing `--precise` flag | Restore from backup, re-run with `--precise` |
| Database import fails | SQL file too large or charset mismatch | Split the file, check `max_allowed_packet`, verify charset |
| Plugin activation fatal error | PHP compatibility or dependency conflict | Check PHP version, review error log with `lando logs` |
| Cron events not firing | `DISABLE_WP_CRON` set without system cron | Add system cron or remove the constant in dev |
| Maintenance mode stuck | `.maintenance` file not removed | `lando wp maintenance-mode deactivate` or manually remove the file |
| `wp acorn` commands fail | Acorn not bootstrapped | Verify Acorn is installed and activated, check `app/Providers/` |

## Escalation

- If WP-CLI commands consistently fail inside Lando, check Lando service health with `lando info` and `lando logs`
- For database corruption beyond simple import/export, consult a DBA or restore from a known-good backup
- If search-replace produces unexpected results after dry-run looked clean, restore from backup immediately and investigate serialized data structures
- For deploy script failures in staging or production, halt the deployment, restore from backup, and debug in the Lando local environment first
