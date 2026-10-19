---
name: dify-local-sync
description: Configure a local self-hosted Dify Docker deployment for trusted Inner API access, then import, overwrite, optionally publish, and strictly verify validated Workflow or Chatflow DSL. Use only when the user explicitly asks to synchronize a DSL to a local Dify they control. Do not use for Dify Cloud, arbitrary remote hosts, or production deployment.
---

# Dify Local Sync

Synchronize a pre-import validated DSL to a user-controlled local Dify Docker stack. Creation and Draft export use Dify's internal DSL endpoints from inside the API container. Dify 1.17.1's Inner API does not expose overwrite, import confirmation, or publish operations, so those operations use the API container's Dify Service Layer.

Read [references/inner-api-boundary.md](references/inner-api-boundary.md) before setup or synchronization.

## Authorization Boundary

- Read-only inspection and dry-run are allowed when the user asks about local sync.
- Writing `docker/.env`, generating/rotating a key, recreating services, importing, overwriting, and publishing are separate mutations.
- Run `setup --apply` only after the user explicitly authorizes local Inner API configuration.
- Run `sync --apply` only after the user explicitly authorizes creating or overwriting the named local App.
- Add `--publish` only when the current user instruction explicitly authorizes publishing. Prior setup or import approval does not authorize publication.
- Never use these scripts for Dify Cloud, an arbitrary remote URL, or a host the user does not control.

## Prerequisites

- Host Python 3.10+ and PyYAML for the launcher and DSL validation; install the repository's `requirements.txt` in the project environment.
- Docker Engine/Desktop with Docker Compose v2 and permission to run `docker compose exec`.
- A local Dify source/deployment directory containing Docker Compose and its `.env` file.
- Dify 1.17.1 is the tested baseline. Recheck internal interfaces before using another release.
- Running Docker with permission to execute commands in the Dify API container.
- A validated Workflow or Chatflow DSL.
- An active local Dify account. The script auto-selects it only when exactly one active account exists.

This Skill does not install Dify or host Docker. The API container supplies the Dify-internal Python runtime used by Service Layer calls; do not install a second copy inside the container. Run a read-only preflight before mutation:

```bash
python3 --version
docker --version
docker compose version
docker compose -f /path/to/dify/docker/docker-compose.yaml \
  --env-file /path/to/dify/docker/.env ps
```

Resolve scripts relative to this Skill directory before running them.

## 1. Inspect Setup

Default setup is read-only:

```bash
python3 <skill-dir>/scripts/setup.py --dify-root /path/to/dify
```

It reports paths and whether Inner API/key are configured, but never prints the key.

After explicit authorization:

```bash
python3 <skill-dir>/scripts/setup.py --dify-root /path/to/dify --apply
```

Setup refuses Git-tracked secret/config targets, creates a mode-600 backup, generates a high-entropy key when needed, writes `INNER_API=true`, and creates the ignored `docker/docker-compose.override.yaml` needed to inject both variables into the API service. It recreates only API and verifies the loaded settings. A failed verification restores the previous files and API container.

If that override path already contains user-managed configuration, setup stops. Pass an unused local `--override-file` path instead; the sync and verify commands must then receive the matching `--compose-override-file` path.

## 2. Prepare DSL

Apply `dify-dsl` and `dify-python-code-node` first. Code source sync, ELK layout, and static validation must pass before local import.

Keep portable source values in DSL. Put local Secret/value overrides in an ignored environment profile such as `config/dify-env.local.yml`:

```yaml
allow_undeclared_variables: true
environment_variables:
  API_BASE_URL:
    value: http://host.docker.internal:8080
    value_type: string
  API_KEY:
    value: local-secret
    value_type: secret
```

The syncer applies only variables declared by the DSL and never prints values.

## 3. Dry Run

Without `--apply`, sync resolves the account/workspace and prints the planned create/overwrite/publish action:

```bash
python3 <skill-dir>/scripts/sync.py dev-dsl/app.yml \
  --project-root /path/to/dsl-project \
  --dify-root /path/to/dify \
  --via-container \
  --account-email user@example.com
```

The script reads the Inner API key from `DIFY_INNER_API_KEY` or the Compose env file. Do not pass it on the command line unless unavoidable.

## 4. Import Or Overwrite

After explicit authorization:

```bash
python3 <skill-dir>/scripts/sync.py dev-dsl/app.yml \
  --project-root /path/to/dsl-project \
  --dify-root /path/to/dify \
  --via-container \
  --account-email user@example.com \
  --apply
```

The first successful sync creates an App through container-local Inner API and records its ID in the DSL project's `dev-dsl/.dify-sync-map.json`. Later syncs overwrite that mapped App through the container Service Layer because the upstream 1.17.1 Inner API import endpoint is create-only. Use `--force-create` only when the user explicitly asks for a separate App.

## 5. Publish

Publishing is optional and consequential:

```bash
python3 <skill-dir>/scripts/sync.py dev-dsl/app.yml \
  --project-root /path/to/dsl-project \
  --dify-root /path/to/dify \
  --via-container \
  --account-email user@example.com \
  --apply --publish
```

Import writes Draft. `--publish` creates a versioned Workflow snapshot, moves `apps.workflow_id` to it, and can update Dataset joins, Triggers, and Schedules.

## 6. Verify

```bash
python3 <skill-dir>/scripts/verify.py dev-dsl/app.yml \
  --project-root /path/to/dsl-project \
  --dify-root /path/to/dify \
  --via-container \
  --strict-sha \
  --require-published
```

Do not report completion until verification passes. Report Draft and Published status separately, plus the local App URL.

## Security Rules

- Keep Inner API container-local; do not expose `/inner/api` through a public reverse proxy.
- Keep the generated Compose override loaded whenever recreating API, or rerun setup after Dify upgrades/recreation.
- Never commit Compose `.env`, environment profiles, sync maps, or backups containing local identity/configuration.
- Never print or return the Inner API key.
- Do not confuse `INNER_API_KEY` with `INNER_API_KEY_FOR_PLUGIN`.
- Require the selected account to be a member of the selected Workspace before import.
- Preserve the current App mapping unless the user explicitly requests rebinding or force-create.

## Natural-Language Handoff

When a user asks to install or use this Skill, keep installation and Dify mutation separate:

```text
Install `dify-dsl`, `dify-python-code-node`, and `dify-local-sync` from
https://github.com/LeeHoo29/dify-dsl-skill.
Only install and verify Skill discovery; do not configure Docker or modify Dify yet.
```

After installation, request the Dify path and target account/workspace explicitly. A useful setup handoff is:

```text
Use $dify-local-sync with my local Dify at /path/to/dify.
First inspect the setup and run a sync dry-run for /path/to/dsl-project/dev-dsl/app.yml.
Ask before changing Inner API configuration, creating or overwriting the App, and publishing.
```

Never interpret installation of this Skill as authorization for any of those Dify mutations.
