---
name: coolify-cli
description:
  Operate Coolify instances through the official coollabsio/coolify-cli. Use for CLI setup and authentication, resource
  inspection, deployments, logs, application configuration, environment variables, databases, services, backups, and
  infrastructure management in Coolify.
---

# Coolify CLI

Use the official `coolify` executable for the requested Coolify operation. Keep this skill portable across projects and
instances; discover names, UUIDs, credentials, branches, and environments from the current task.

## Establish the target

1. Check `coolify version` and the relevant command's `--help`. The version command is a subcommand, not `--version`. If
   installation or authentication is missing, read [setup.md](references/setup.md).
2. Inspect saved contexts with `coolify context list`. Select the instance established by the request and project
   configuration. If several targets remain plausible, ask for the missing target before issuing requests to one.
3. Use `--context "$COOLIFY_CONTEXT"` on remote operations. This variable represents the resolved saved context name.
   Avoid changing the persistent default just to execute a task.
4. Verify connectivity with `coolify --context "$COOLIFY_CONTEXT" context verify`. Read the relevant resource or team to
   establish access to that operation. `context version` reports the server version, which is separate from
   `coolify version`.
5. Resolve the resource through inventory and detail commands. Check its project, environment, server, and type before a
   mutation. Use returned resource UUIDs, not internal numeric IDs; team commands use numeric team IDs.

## Execute and verify

- Honor the requested action and existing authorization. An authorized deployment or update does not need another
  confirmation simply because it uses Coolify. Inspection or diagnosis does not authorize a redeployment or
  infrastructure change.
- Read only the relevant reference: [operations.md](references/operations.md) for inventory, deployment, logs, creation,
  backups, or infrastructure; [environment.md](references/environment.md) for resource and shared environment variables.
- Inspect current settings, apply the smallest requested change, and read the resource back. Distinguish a saved
  configuration, a queued job, a finished deployment, and a healthy endpoint.
- Database deletion defaults to removing volumes and other associated data. Establish whether data removal is in scope
  and inspect the exact command's cleanup flags. `--force` means different things across subcommands and is not a
  general automation flag.
- After an uncertain write response, inspect current state or the job list before retrying. The client already retries
  some failed requests, including mutations. Stop further writes when the result cannot be determined; do not create
  duplicate deployments or resources to test connectivity.

## Handle output deliberately

- Prefer `--format json` for supported structured reads and deployment responses. Check exit status and actual shape.
  Context verification, environment sync, and some other commands still emit text.
- Keep `--show-sensitive`, `--debug`, and `--debuglogs` off by default. JSON and pretty formatters do not provide
  universal redaction; masking depends on the command. Logs, connection URLs, application details, and error bodies can
  contain secrets.
- Filter sensitive responses to needed fields within the local process before returning tool output. Use an allowlist of
  fields, not merely removal of a field named `password`. Do not print or copy entire CLI configs, API tokens, private
  keys, or `.env` contents into the conversation or artifacts.
- Separate stderr from machine-readable stdout and preserve failed exit statuses when piping. A masked value such as
  `********` is never a replacement value for an update.
- Bound logs and polling. Follow the exact deployment UUID when available and report a still-running operation honestly
  if verification cannot finish.

## Documentation and compatibility

Start with installed help for available syntax. Use the upstream
[README](https://raw.githubusercontent.com/coollabsio/coolify-cli/refs/heads/main/README.md) for workflows,
[llms.txt](https://raw.githubusercontent.com/coollabsio/coolify-cli/refs/heads/main/llms.txt) for orientation, and
[llms-full.txt](https://raw.githubusercontent.com/coollabsio/coolify-cli/refs/heads/main/llms-full.txt) when the full
flag catalog is needed. If a command is absent or the API rejects a supported flag, check CLI and server compatibility
before proposing an upgrade or API fallback.

Checked on 2026-09-09 against installed CLI 1.8.0 help and upstream revision `76ca47187a0c34b6f68c5c44b192fc457749e2c7`.
This is a reference baseline, not a required version pin. Source files in the repository are not necessarily registered
public commands.

Finish with the resolved target, action, verification result, and any remaining limitation. Omit secrets and raw
configuration dumps.
