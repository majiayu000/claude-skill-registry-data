---
name: heroku-app-ops
description: Operate running Heroku apps with a read-only-first workflow. Use when the agent needs to inspect app status, app info, current process state, dynos, releases, logs, one-off commands, maintenance mode, scaling, restarts, or rollback behavior for a Heroku app.
---

# Heroku App Ops

Inspect and operate Heroku apps while keeping destructive changes behind an explicit confirmation step.

## Start with a snapshot

Resolve this installed skill's directory first. Do not assume the current workspace contains the skill source repository.

Run the bundled helper from this skill's `scripts/` directory:

```bash
python3 /path/to/heroku-app-ops/scripts/app_snapshot.py --app <app>
```

If no app is known yet, run it without `--app` to inspect CLI and auth readiness only.

## Read-only-first flow

Start with these commands before changing anything:

- `heroku apps:info -a <app> --json`
- `heroku ps -a <app>`
- `heroku releases:info -a <app>`
- `heroku maintenance -a <app>`
- bounded log reads such as `heroku logs -a <app> --num 200`

Use one-off commands carefully:

- prefer inspection commands and idempotent diagnostics
- explain what `heroku run` will do before executing it
- avoid backgrounding unknown processes

## Change operations

Use explicit confirmation before:

- `ps:scale`
- `ps:restart`
- `maintenance:on`
- `maintenance:off`
- `releases:rollback`
- any `run` command that changes data or infrastructure

After a change, verify with release info, app info, and bounded logs.

## Incident handling

When debugging an outage or failed release:

1. capture current app state
2. identify the most recent release
3. inspect recent logs
4. confirm whether maintenance mode is active
5. propose the smallest safe corrective action

## References

- Read `references/app-ops.md` for command catalogs, incident patterns, and source links.
