---
name: heroku-connect
description: Manage Heroku Connect sync operations between Salesforce and Heroku Postgres. Use when the agent needs to provision Heroku Connect, install or inspect the Heroku Connect CLI plugin, review mappings, import or export config, diagnose sync failures, or reason about Heroku Connect API limits and operational guardrails.
---

# Heroku Connect

Manage Heroku Connect as a stateful sync system between Salesforce and Heroku Postgres.

## Start with plugin and connection inspection

Resolve this installed skill's directory first. Do not assume the current workspace contains the skill source repository.

Run the bundled inspection helper from this skill's `scripts/` directory:

```bash
python3 /path/to/heroku-connect/scripts/plugin_status.py
```

Use the output to determine:

- whether the Heroku CLI is installed
- whether the Heroku Connect CLI plugin is installed
- whether Connect subcommands are available in the current shell

## Preferred workflow

1. confirm the app has both Heroku Postgres and Heroku Connect provisioned
2. install the Connect plugin if needed with `heroku plugins:install @heroku-cli/heroku-connect-plugin`
3. set the target database with `heroku connect:db:set DATABASE_URL -a <app> [--resource <resource>]`
4. authenticate to Salesforce with `heroku connect:sf:auth -a <app> [--resource <resource>]`
5. inspect the connection with `heroku connect:info`
6. run `heroku connect:diagnose` before changing mappings or attempting recovery
7. prefer dashboard-created mappings for new setups, and CLI import/export for repeatable configuration
8. verify sync state after every change

## Mapping and recovery guidance

- Use `connect:export` and `connect:import` for repeatable config moves.
- Prefer `connect:mapping:diagnose` before `connect:mapping:reload`.
- Treat `pause`, `resume`, `recover`, `mapping:delete`, and config import as state-changing operations.
- If an app has more than one Heroku Connect add-on, specify `--resource`.
- Treat `connect:db:set` and `connect:sf:auth` as setup operations for new connections, not read-only inspection.

## Guardrails

Ask for confirmation before:

- provisioning Heroku Connect or changing plans
- importing mapping configuration into a live connection
- pausing or resuming production sync
- deleting mappings
- running reloads that will repopulate large datasets

Keep API rate limits in mind if scripting against the Connect API.

## References

- Read `references/connect-workflows.md` for plugin commands, API notes, and source links.
