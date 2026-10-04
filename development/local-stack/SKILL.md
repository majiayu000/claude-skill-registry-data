---
name: local-stack
description: "Run a regelrecht branch locally end-to-end (worktree + Docker stack + DB), with the workarounds needed when developing inside the dev container against Docker Desktop. Accepts a branch name or a PR number. Subcommands: bare arg = start, `stop <arg>` = shut down, `clean <arg>` = shut down and remove worktree."
user-invocable: true
---

# Local Stack

Spin up a regelrecht branch in a self-contained Docker stack so the user can test it from their browser. Works on any branch — a PR number is just a convenient way to look one up. Handles the quirks that show up when Claude Code is running inside the dev container against Docker Desktop on Windows.

## Context: why this skill exists

`just local` (introduced in PR #274) assumes you run it on a host Docker daemon — when you run it from the dev container against Docker Desktop, three things bite:

1. **Bind mounts break for `prometheus` + `grafana`.** Docker Desktop's daemon doesn't see paths under `/workspace/...` (the dev container's filesystem); it silently creates empty directories at the mount source. The two services that bind-mount config files (`./dev/prometheus.yml`, `./dev/grafana-datasource-local.yaml`, the dashboards/alerting dirs) crash on start. The other services have no bind mounts.
2. **Ports 7100-7300, 3000-3001, 8000 are already claimed** by the dev container on the Windows host, so any `docker-compose` `ports:` mapping in those ranges fails with "port is already allocated". We use 18000+ instead (free on the Windows host, reachable from Windows).
3. **`~/.docker/config.json` may reference a `credsStore` helper** that doesn't exist inside this container (e.g. `dev-containers-...`). Even pulling a public image then fails with `error getting credentials - err: exit status 255`.

## Instructions

### 1. Parse argument

The argument is either:

- A **branch name** (anything containing `/` or matching a local/remote ref) → use directly.
- An **integer** → look up the corresponding PR's branch.

Action depends on the leading verb:

- `<arg>` (no verb) → **start** the stack for that branch.
- `stop <arg>` → shut down the stack (worktree kept).
- `clean <arg>` → shut down and remove the worktree.

If the user invoked the skill without an argument, ask which branch or PR.

### 2. Resolve to a branch name

If the argument is a pure integer, treat as a PR:

```bash
gh pr view <N> --json number,title,headRefName,state,author
```

Confirm `state == "OPEN"` (warn but proceed otherwise). Use `headRefName` as the branch.

If the argument is a branch name, use it as-is. Verify it exists on origin:

```bash
git -C /workspace/regelrecht ls-remote --exit-code --heads origin <branch>
```

For `stop`/`clean`: if the worktree already exists at the predictable path, skip resolution and reuse the existing path; otherwise still resolve to derive the worktree directory.

### 3. (start only) Pre-flight: Docker credential helper

Read `~/.docker/config.json`. If it has a `credsStore` field, run a quick public-image pull to test:

```bash
docker pull alpine:3 >/dev/null 2>&1
```

If that fails with `error getting credentials`, back up the file and reset:

```bash
cp ~/.docker/config.json ~/.docker/config.json.bak
echo '{}' > ~/.docker/config.json
```

Tell the user: "Reset broken Docker credsStore (backup at config.json.bak)."

### 4. (start only) Fetch + worktree

Per project AGENTS.md, **always** fetch before working with any branch:

```bash
git -C /workspace/regelrecht fetch origin <branch>
```

Derive a worktree slug from the branch: replace `/` with `-`, cap at ~40 chars. The worktree path is `.worktrees/<slug>`. Create it on the branch (not detached):

```bash
git -C /workspace/regelrecht worktree add .worktrees/<slug> -B <branch> origin/<branch>
cp -r /workspace/regelrecht/.claude /workspace/regelrecht/.worktrees/<slug>/
```

If the worktree already exists, reuse it but `git -C <worktree> pull --ff-only origin <branch>` to bring it up to date — abort if there are local uncommitted changes (the user may be mid-fix).

### 5. (start only) Pick free ports

Default ports: `FRONTEND_PORT=18130`, `ADMIN_PORT=18180`. Before using them, check they aren't held:

```bash
docker ps --format '{{.Ports}}' | grep -E ':(18130|18180)->'
```

If either is taken (e.g. another PR is already running), increment by 100 (`18230`, `18280`, …) until a free pair is found. Record the chosen pair for the final URL output.

### 6. (start only) Bring up the stack

Skip `prometheus` and `grafana` (bind-mount issue — see Context). Start exactly the runtime services:

```bash
FRONTEND_PORT=<frontend> ADMIN_PORT=<admin> \
  docker compose \
    -f /workspace/regelrecht/.worktrees/<wt>/docker-compose.dev.yml \
    -f /workspace/regelrecht/.worktrees/<wt>/dev/compose.local.yaml \
    --project-directory /workspace/regelrecht/.worktrees/<wt> \
    up -d --build postgres admin harvester-worker enrich-worker pipelineapi frontend
```

`--project-directory` is required when invoking compose from outside the worktree — without it, the compose project name collides with other PR worktrees.

The first build is slow (Rust release build for 5+ services, ~5-10 min on a clean cache). Run in the background and stream key events: `Building`, `Built`, `Started`, `Healthy`, `Error`, `error:`, `failed`, `panic`, `unhealthy`. If a build fails, surface the failing target and the last error block — don't blindly retry.

### 7. (start only) Verify the stack

After compose returns, check container health:

```bash
docker ps --filter 'name=<slug>' --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

`postgres` should report `(healthy)`. `pipelineapi` may briefly show `(unhealthy)` while its first healthcheck runs — that's only a problem if it stays unhealthy for >30s. Tail the editor-api logs to confirm migrations applied and the OIDC mode:

```bash
docker logs --tail 30 <slug>-frontend-1 2>&1 | tail -10
```

Look for `editor-api ... listening on 0.0.0.0:8000`. The line `OIDC authentication is DISABLED — editor is unprotected` is **expected** locally — both admin and editor are designed to run auth-loose without OIDC env vars.

Verify the latest migration:

```bash
docker exec <slug>-postgres-1 \
  psql -U regelrecht regelrecht_pipeline \
  -c 'SELECT version, description FROM _sqlx_migrations ORDER BY version DESC LIMIT 3;'
```

If the PR adds a migration, point out whether it's the top row.

### 8. (start only) Report URLs and warnings

Print:

```
✅ Branch <branch> running locally
   Editor:  http://localhost:<frontend>
   Admin:   http://localhost:<admin>

   Stop:    /local-stack stop <arg>
   Cleanup: /local-stack clean <arg>   (also removes the worktree)
```

If the branch's diff vs `origin/main` suggests an auth-gated feature (anything touching `person_sub`, `useAuth`, login menu items, OIDC), warn explicitly:

> ⚠️ This branch's feature appears to require an authenticated user (`person_sub`). Locally OIDC is **off**, so anonymous calls will hit 401. Auth-gated UI elements (e.g. account-menu items keyed on `authenticated`) will not appear locally.

Detection heuristic: `git -C <worktree> diff origin/main...HEAD | grep -E 'person_sub|useAuth|authenticated|OIDC|session'` returning matches → emit the warning.

### 9. (stop) Shut down

```bash
docker compose \
  -f /workspace/regelrecht/.worktrees/<wt>/docker-compose.dev.yml \
  -f /workspace/regelrecht/.worktrees/<wt>/dev/compose.local.yaml \
  --project-directory /workspace/regelrecht/.worktrees/<wt> \
  down
```

Volumes (`pgdata`, repo-clones, etc.) are preserved by default — pass `-v` only if the user explicitly asks for a clean DB next time.

### 10. (clean) Shut down + remove worktree

After `down`, also:

```bash
git -C /workspace/regelrecht worktree remove .worktrees/<wt>
```

If the worktree has uncommitted changes, **stop and ask** before removing — the user may have in-flight edits to commit. Do not pass `--force`.

## What this skill does **not** do

- Doesn't enable OIDC locally. If the user wants to test auth-gated behavior, they need real OIDC creds + a Keycloak client whose redirect URI includes `http://localhost:<frontend>/auth/callback`. That's out of scope here.
- Doesn't run prometheus/grafana. If observability is needed, that's a separate workflow (see the Grafana component page).
- Doesn't run the test suite, lint, or formatters — use `just check` or the relevant `just` recipes for that.
- Doesn't push, comment, or modify the PR. Read-only locally.

## Failure recovery

- **`port is already allocated`**: another stack is running. Run `docker ps` to identify it, then either stop that stack (`/local-stack stop <other>`) or pick a higher port pair manually.
- **`bind for ... failed`** on a service other than prometheus/grafana: a regression — investigate which new bind mount was added; don't silently work around it.
- **Migrations didn't apply**: check `pipelineapi` and `editor-api` logs for `acquiring migration lock` / `migrations completed`. A schema mismatch (renumbered migration) requires `down -v` to wipe `pgdata`, then start again.
- **Build fails on a Rust target**: report the actual cargo error. Don't suggest `--no-cache` or retry without a real cause.
