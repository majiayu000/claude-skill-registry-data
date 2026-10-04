---
name: worktree
description: "Use before starting work that touches files: creating a worktree, claiming one, checking who owns one, releasing or handing one off, copying env files, picking ports, or running the app baseline. One task, one branch, one worktree, one owner. Keeps agents from colliding on the same path, branch, or port."
---

# Worktree

Every task gets its own worktree, and every worktree has exactly one owner. A lock is coordination data, not a substitute for looking. Always check git status before touching files.

## The registry

A JSON file listing who owns what, one entry per worktree.

- Default path: `~/.config/squirrel/worktree-locks.json`
- Override: `SQUIRREL_WORKTREE_REGISTRY=/path/to/file.json`
- Remote hosts keep their own registry at the same default path. A remote worktree operated from a local session also goes in the local registry, with the host name and the remote path.

Read and write it with `scripts/worktree_lock.py` from this skill. It takes a file lock so two agents can't clobber the file. Without the script, edit the JSON by hand in the same shape and keep everyone else's entries.

```bash
python3 scripts/worktree_lock.py list --status active
python3 scripts/worktree_lock.py claim --repo <name> --path <worktree-path> --branch <branch> --base-ref origin/<base> --owner "<agent or session>" --purpose "<task id and one line>" --ports web=3001,api=8081
python3 scripts/worktree_lock.py heartbeat --path <worktree-path>
python3 scripts/worktree_lock.py release --path <worktree-path> --status released
python3 scripts/worktree_lock.py release --path <worktree-path> --status handoff
```

On Windows, where `python3` isn't a command, use `py -3`.

Each entry:

```json
{
  "repo": "web-app",
  "host": "local",
  "path": "/Users/me/code/worktrees/web-app-1234-search",
  "branch": "1234-search",
  "base_ref": "origin/main",
  "owner": "agent:session-abc",
  "purpose": "1234 add search to the list page",
  "status": "active",
  "ports": { "web": 3001, "api": 8081 },
  "created_at": "2026-09-02T20:00:00Z",
  "updated_at": "2026-09-02T20:10:00Z",
  "notes": "env copied, baseline smoke passed"
}
```

Statuses: `active` (in use), `handoff` (left alive on purpose for the next agent), `released` (done), `stale` (looks abandoned, don't reuse until someone inspects it). Never put a secret in any field.

## The flow

### 1. Look before you touch

- Name the repo, the base branch, and the worktree's path: under a `worktrees/` directory near the repo, named for the task, never `tmp`.
- `git fetch origin <base> --prune`.
- Check the existing checkout without changing it. `git status --short --branch`, `git worktree list`, `git log --oneline -10 origin/<base>`.
- Dirty files in the existing checkout belong to someone else. Leave them alone.
- List active locks for the repo. Another agent's active lock on the path or branch you want means stop. Take it over only if the human says so.

### 2. Claim

Claim the lock before creating the worktree, starting services, or copying env files. Record the task id in the purpose.

### 3. Create from a clean base

```bash
git worktree add -b <branch> <path> origin/<base>
git -C <path> status --short --branch
```

Detached is fine for a throwaway check. If the new worktree isn't clean the moment it's created, stop and find out why.

### 4. Copy local config

Copy the ignored, local-only files the app needs: `.env`, `.env.local`, app-specific config. Confirm they're ignored first:

```bash
git -C <path> check-ignore -v .env .env.local
```

If those files hold absolute paths, ports, container names, or URLs pointing at the original checkout, change them inside the new worktree only, and write down what you changed. Never commit them.

### 5. Find the commands

Read the repo's own entry points instead of guessing: Makefile, package.json, the lockfile to pick the package manager, compose files, the README. Use the repo's commands; a backend Makefile is one of them.

### 6. Pick ports that don't collide

```bash
lsof -nP -iTCP -sTCP:LISTEN
docker ps --format 'table {{.Names}}\t{{.Ports}}\t{{.Status}}'
docker compose ls
rg -n "localhost:|127\.0\.0\.1:|PORT=|ports:|COMPOSE_PROJECT_NAME|container_name|API_URL|BASE_URL" <path>
```

Give every service the worktree runs a port nothing else is using. For compose, set a unique project name so containers and volumes don't collide with the other checkout. Change ports and names in the worktree only. Update the lock with the ports you chose.

### 7. Run the baseline

Install dependencies with the repo's conventions, only if needed. Start the services on your ports. Run migrations and seeds through the repo's wrapper. Then check it's usable: the API answers, the frontend loads on your port, the local test account from the seed or env logs in, and the frontend talks to your backend, not the other checkout's. Don't run the full test suite here. This is a working environment, not a green build.

### 8. Report

Before starting the task, tell the human: path and branch, local files copied (names, not contents), URLs and ports, compose project name if any, seed and login status, local-only edits, anything skipped.

### 9. During the work

Heartbeat the lock on long tasks. Update it when you start or stop a service.

### 10. Release

When the worktree is deleted or the human says it's done, release the lock. If it should stay alive for someone else, mark it handoff instead, with a note on where things stand.

## Never

- Reset, stash, or edit the original checkout to make setup easier.
- Remove containers or volumes without the human approving and understanding what goes with them. Their `/nuke` is that approval, and `nuke` does the whole teardown.
- Release or take over another agent's active lock without being told to.
- Commit local setup changes unless asked.
- Use a lock as a reason to overwrite someone's dirty files.
- Enter another agent's worktree. A lead reads a worker's branch from its own checkout, `git fetch` then `git diff origin/<base>...origin/<branch>` with the base the lock recorded, and builds it in a worktree of its own. A `cd` into someone else's tree is how a stray commit lands on their branch.

When several repos are involved, run the flow for each one and make ports and project names distinct across the whole set.
