---
name: credentials
description: Remote environment credentials (staging, production) — access and read-only enforcement.
---

# Credentials — Remote Environment Access

Use this skill whenever a task requires accessing a remote environment (staging, production, QA, etc.).

## File Location

`.dev-team-agents/credentials.local.json` in the **main checkout** — every linked git worktree shares that one file (see § 1 for resolving it).

This file is **gitignored** and **never committed**. It is created only via an explicit action: `devteam cred local init` or the app's Credentials tab. If the file does not exist, tell the user to create it via one of those methods — never create it yourself.

## Structure

The file is **free-form**: the user names, nests and removes groups and fields as they like. Nothing in it is a fixed category, environment or agent mapping — find what you need by key name and context. `devteam cred local init` writes a small example the user is expected to edit or delete.

Two reserved keys may appear in any object; every other key is the user's own:

| Key | Value | Meaning |
|-----|-------|---------|
| `$production` | `true` | This object and everything nested below it is **production** — see § 5 |
| `$secrets` | list of sibling key names | Those keys hold secrets. The app keeps them write-only; never echo, log or paste them |

Two flat top-level keys are settings, not credentials: `work_feedback_active` and `work_feedback_interval_minutes`, consumed by `skills/shared/work-feedback/SKILL.md`.

Strip the `$`-prefixed keys before using an object as connection data. Treat any other key as valid; never reject, rename or remove user structure.

## How to Use

### 1. Locate the File

Ask the CLI for the path — it resolves the main checkout (worktrees, monorepo subprojects) and prints no secret value:

```bash
CRED_FILE=$(devteam cred local show --json 2>/dev/null \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["path"])' 2>/dev/null)
[ -n "$CRED_FILE" ] || CRED_FILE=".dev-team-agents/credentials.local.json"
[ -f "$CRED_FILE" ] || echo "MISSING"
```

If the file does not exist, tell the user to create it via `devteam cred local init` or the app's Credentials tab.

### 2. Read the JSON

```python
import json
with open(CRED_FILE) as f:  # the path resolved in step 1
    creds = json.load(f)
```

### 3. Find the Relevant Credentials

- Find the group that matches the task by its key names and nesting (e.g. a `staging` group under `api`, a `jira` group with a `token`)
- Work out whether it is production: `$production: true` on it **or on any ancestor**. A group merely *named* `production` without the flag is not marked, so ask when the name and the flag disagree
- Check if the required fields are filled in

### 4. Handle Empty Fields

If a required field is empty (`""`, `{}`, `null`, or missing):

> Ask the user: "The field `<field>` under `<group path>` is empty. How should I access this environment?"

Use `AskUserQuestion` with relevant options (SSH key path, password, token, etc.) or let the user type free-form input.

### 5. Read-Only Enforcement

**By default, you may only READ from remote environments.** This includes:
- Browsing HTTP endpoints (GET requests via browser or curl)
- Running read-only CLI commands (`ssh user@host ls`, `docker ps`, `kubectl get pods`, database `SELECT`)
- Inspecting logs, configs, or state

**You MUST ask for explicit user permission before:**
- Writing or modifying any file on the remote environment
- Executing commands that change state (`rm`, `mv`, `sed -i`, `kubectl apply`, database `INSERT/UPDATE/DELETE`)
- Restarting services or deploying code
- Running destructive operations

When you need write/execute access, pause and ask:

> "I need to `<action>` on `<environment>`. This is not read-only. Do you authorize this operation?"

Proceed only after the user explicitly confirms.

**Under `$production`**, the same rule tightens: ask before **every** state-changing action, one action per question, and name it as production in the question. An earlier approval — for another action, for staging, or "for this session" — never carries over.

### 6. Protocol-Specific Access

| Protocol | Read-only patterns |
|----------|--------------------|
| HTTP/HTTPS | `curl -s <url>`, browser GET, API calls without side effects |
| SSH | `ssh <user>@<host> <command>` with read-only commands |
| Docker | `docker exec <container> <read-command>`, `docker logs`, `docker ps` |
| Database | `SELECT` queries only (via `psql`, `mysql`, `sqlite3`, etc.) |
| Kubernetes | `kubectl get`, `kubectl describe`, `kubectl logs` |

### 7. No Matching Environment

If the target environment is not in the file, ask the user for connection details and suggest they add it to `credentials.local.json` for future use.
