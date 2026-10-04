---
name: heroku-logging-drains
description: Inspect Heroku logs and configure persistent log forwarding safely. Use when the agent needs to review recent Heroku logs, plan or change log forwarding, inspect a drain target, add or remove classic log drains for Common Runtime apps, inspect current drain configuration, or choose between legacy drains and Fir telemetry workflows on Heroku.
---

# Heroku Logging and Drains

Separate bounded log inspection from persistent log forwarding and drain target changes.

## Identify the runtime first

Before recommending a drain workflow, confirm whether the app is a Common Runtime app or a Fir-generation app.

Start with:

- `heroku apps:info -a <app> --json`
- dashboard metadata if the CLI output does not make the generation obvious

Use classic `drains:*` guidance only for Common Runtime apps. For Fir apps, do not default to `drains:add`; pivot to telemetry drains instead.

## Start with inspection

Resolve this installed skill's directory first. Do not assume the current workspace contains the skill source repository.

Run the bundled helper from this skill's `scripts/` directory:

```bash
python3 /path/to/heroku-logging-drains/scripts/logging_snapshot.py --app <app>
```

If no app is known yet, run it without `--app` to inspect CLI readiness only.

## Read-only-first flow

For Common Runtime apps, use bounded log reads before proposing drains or tails:

- `heroku logs -a <app> --num 200`
- `heroku drains -a <app> --json`

Prefer bounded reads over `--tail` unless the user explicitly wants live streaming.

For Fir apps:

- treat `heroku logs` as a live stream, not a historical buffer
- avoid proposing classic log drains
- use telemetry drain guidance instead, such as `heroku telemetry:add <endpoint> --app <app> --signals logs`

## Drain management

For Common Runtime apps, use persistent drains intentionally:

- `heroku drains:add <url> -a <app>`
- `heroku drains:remove <url> -a <app>`

Treat `drains:get` and `drains:set` as space-specific references rather than part of the default common-runtime workflow. Treat `telemetry:add` as the Fir reference path for app or space telemetry forwarding.

## Guardrails

Ask for confirmation before:

- adding a new drain endpoint
- removing an existing drain
- routing logs to third-party systems that may receive secrets or personal data
- turning a short investigation into a persistent forwarding change

## References

- Read `references/logging-drains.md` for runtime selection, log format notes, drain patterns, and source links.
