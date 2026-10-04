---
name: query-loki-project-logs
description: Query Grafana Loki logs that are organized by labels such as `project_name` or `project`, `env`, and `filename`, where `filename` distinguishes `nginx`, `web`, `worker`, `stdout`, and `stderr` streams. Use when Codex needs to inspect logs with `logcli`, discover available projects or environments, list a project's log files, narrow to a specific component such as web or worker, or check a recent time window for errors in test or local environments.
---

# Query Loki Project Logs

Use this skill to inspect Loki logs with the house convention:

- `project_name` identifies the service or deployment and usually matches the git repository name
- `env` identifies the deployment environment such as `dev`, `test`, or `prod`
- `filename` identifies the concrete stream, such as `pd_router-web-stderr.log` or `pd_router-nginx-stdout.log`

The helper script is compatible with both:

- newer Loki setups that use `project_name`
- older Loki setups that still use `project`

It auto-detects the project label unless `--project-label` or `LOKI_PROJECT_LABEL` is set.

If the user prefers dashboards over CLI triage, Grafana dashboards can use the same labels and keywords:

- project filter: `project_name` or `project`
- environment filter: `env`
- stream filter: `filename`
- free-text filter: the request path, trace keyword, or error signature

## Quick Start

1. Resolve the Loki address and credentials.
2. List available project values.
3. List available environment values if needed.
4. List the target project's `filename` values.
5. Pick the stream that matches the question.
6. Query the time window and summarize findings.

Prefer the helper script first:

```bash
export LOKI_ADDR="https://your-loki.example.com"
export LOKI_USERNAME="your-basic-auth-user"
export LOKI_PASSWORD="your-basic-auth-password"

python3 scripts/loki_project_logs.py projects --since 720h
python3 scripts/loki_project_logs.py envs --since 720h
python3 scripts/loki_project_logs.py files --project pdrouter --env test --since 24h
python3 scripts/loki_project_logs.py errors --project pdrouter --env test --component web --since 1h
```

Run these commands from the skill root directory.

The `errors` subcommand narrows to matching `stderr` streams by default.
When `errors` or `query --component ...` cannot find a filename inside the exact query window, the helper falls back to a 24h discovery window so quiet streams such as `nginx stderr` are still discoverable.
The helper also escapes `--grep` and `--regex` strings for LogQL, so patterns containing quotes or backslashes are safer to pass through the CLI.

If the script is not appropriate, use raw `logcli` commands from [references/query-patterns.md](references/query-patterns.md).

## Workflow

### 1. Resolve Loki

Prefer `LOKI_ADDR` from the current environment.
For deployments behind BasicAuth, also prefer `LOKI_USERNAME` and `LOKI_PASSWORD`.
If they are missing, the helper checks common shell config files such as `~/.zshrc` for `export LOKI_ADDR=...`.
Do not assume `http://localhost:3100` is correct unless the user confirms it.

### 2. Discover Projects

List project label values before guessing names.
This gives the set of known deployments in Loki for the chosen lookback window.
In the current internal convention, the project value usually matches the git repository name.

### 3. Discover Environments

If the user did not specify the environment, list `env` values first.
Common values include `dev`, `test`, and `prod`.

### 4. Discover Streams

List `filename` values for the chosen project and environment.
Use the filename to distinguish the stream type:

- `*-web-stderr.log`: application errors and Python tracebacks
- `*-web-stdout.log`: application request and info logs
- `*-worker-stderr.log`: worker exceptions
- `*-worker-stdout.log`: worker info logs
- `*-nginx-stderr.log`: nginx errors
- `*-nginx-stdout.log`: access logs or proxy output
- `init.log`: startup output

Use exact filenames when querying once the right stream is known.

### 5. Triage Errors

When the user asks whether there are errors:

1. Start with `stderr` for the requested component.
2. Search for obvious error markers such as `ERROR`, `Exception`, `Traceback`, `panic`, `sqlalchemy.exc`, and `asyncpg.exceptions`.
3. Pull a broader context query if the first pass shows stack traces or repeated failures.
4. Report the result with exact timestamps, stream filename, and the dominant error type.

If the request is about web issues, check both:

- `*-web-stderr.log` for exceptions
- `*-web-stdout.log` for the request path or surrounding request logs

If the request is about nginx, include both nginx streams because routing failures often show up in `stdout` access logs while configuration issues show up in `stderr`.

## Response Pattern

When answering the user, include:

- Whether errors were found
- The exact time window used
- The project name
- The environment, if one was part of the query
- The exact filename(s) queried
- One or two representative error lines or a concise paraphrase
- A short root-cause hypothesis when the logs support it

Avoid claiming absence of errors unless you checked the relevant stream for the requested component.

## Resources

- Scripted helper: [scripts/loki_project_logs.py](scripts/loki_project_logs.py)
- Query cookbook: [references/query-patterns.md](references/query-patterns.md)
