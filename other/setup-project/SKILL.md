---
name: setup-project
description: "Bootstraps a new project directory with base configuration files, MCP servers, API connections, and template skills from OutworkOS. Use when setting up a new project, initializing a workspace, or configuring MCP integrations for a new directory."
argument-hint: "<project-name>"
---

# /setup-project

Bootstrap a new project directory under `$OUTWORKOS_PARENT` with base configuration files from `$OUTWORKOS_ROOT` (the OutworkOS repo — source of truth for shared skills and credentials).

**Key concepts:**
- `$OUTWORKOS_ROOT` — the OutworkOS repo (where you run Claude from, contains scripts/, skills/, .mcp.json)
- `$OUTWORKOS_HOME` — data directory (e.g., ~/.outworkos)
- `$OUTWORKOS_PARENT` — where project folders live (e.g., ~/.outworkos/projects/)
- These CAN be the same directory if the user configures it that way

## Trigger

User invokes `/setup-project` or `/setup-project <project-name>`

## Steps

### 1. Validate Environment & Create Project Directory

1. Confirm `$OUTWORKOS_ROOT` is set and the template directory exists with these files:
   - `$OUTWORKOS_ROOT/.mcp.json`
   - `$OUTWORKOS_ROOT/skills/context-map/`
   - `$OUTWORKOS_ROOT/skills/log/`
   - `$OUTWORKOS_ROOT/skills/todoist/`
   If any are missing, warn but continue (some may not be needed).

2. Confirm `$OUTWORKOS_PARENT` is set. If not, default to `$OUTWORKOS_HOME/projects` or ask the user.

3. Get the project name:
   - If provided as argument, use it
   - Otherwise, ask: **"What's the name of this project?"**
   - Slugify the name for the directory (lowercase, hyphens for spaces, strip special chars)

4. Create the project directory at `$OUTWORKOS_PARENT/<slug>/`:
   - If the directory **already exists and is not empty**, stop with an error: "Project directory already exists. Use a different name or remove it first."
   - If the directory exists but is empty, proceed
   - If it doesn't exist, create it with `mkdir -p`

5. Set `PROJECT_DIR=$OUTWORKOS_PARENT/<slug>` for use in all subsequent steps.

**Note:** The user runs Claude from `$OUTWORKOS_ROOT` (the repo) to get skills loaded. This step creates the project directory elsewhere — that's expected.

### 2. Check for Existing Files

Check whether these already exist in the project directory:
- `.mcp.json`
- `.claude/skills/context-map/`
- `.claude/skills/log/`
- `.claude/skills/todoist/`

For each one that exists, ask the user whether to **skip** or **overwrite** it. Use a single AskUserQuestion with multiSelect for efficiency.

### 3. Verify Vault Access

Verify that `outwork init` has been run and Vault secrets are accessible. Test by retrieving a known secret:

```bash
"$OUTWORKOS_ROOT/scripts/get-secret.sh" todoist_api_token > /dev/null 2>&1 && echo "Vault: OK" || echo "Vault: FAILED — run outwork init first"
```

If Vault access fails, tell the user to run `$OUTWORKOS_ROOT/scripts/outworkos-auth-login.sh` first.

### 4. Link Skills and Hooks

Symlink key directories from `$OUTWORKOS_ROOT` into the project so skills, hooks, and environment variables work when running Claude from the project directory.

```bash
mkdir -p "$PROJECT_DIR/.claude"

# Skills — makes all /commands available
ln -sf "$OUTWORKOS_ROOT/skills" "$PROJECT_DIR/.claude/commands"

# Hooks — SessionStart sets $OUTWORKOS_ROOT, $OUTWORKOS_HOME, $OUTWORKOS_PARENT
ln -sf "$OUTWORKOS_ROOT/.claude/hooks" "$PROJECT_DIR/.claude/hooks"

# Settings — hook config (SessionStart, SessionEnd)
# Copy (not symlink) so the project can customize hooks later
if [ ! -f "$PROJECT_DIR/.claude/settings.json" ]; then
  cp "$OUTWORKOS_ROOT/.claude/settings.json" "$PROJECT_DIR/.claude/settings.json"
fi
```

This ensures:
- All skills are available (context-map, log, todoist, scan, whats-next, etc.)
- `$OUTWORKOS_ROOT`, `$OUTWORKOS_HOME`, `$OUTWORKOS_PARENT` are set on session start
- Vault scripts (`get-secret.sh`, `set-secret.sh`) are reachable via `$OUTWORKOS_ROOT/scripts/`
- Stays in sync with the repo — no need to copy or update individual files

If `.claude/commands` or `.claude/hooks` already exists:
- If it's a symlink pointing to the same target, skip
- If it's a symlink pointing elsewhere, ask the user before replacing
- If it's a regular directory, ask the user whether to replace it with a symlink

### 5. Supabase Picker (Optional)

Ask the user: **"Do you want to add Supabase database connections?"**

If **no**: skip to Step 6 with zero Supabase entries.

If **yes**:

1. Read `SUPABASE_ACCESS_TOKEN` from Vault: `$("$OUTWORKOS_ROOT/scripts/get-secret.sh" supabase_access_token)`
2. Call the Supabase Management API to list projects:
   ```
   curl -s -H "Authorization: Bearer <TOKEN>" https://api.supabase.com/v1/projects
   ```
3. Filter the JSON response to only projects where `status` is `"ACTIVE_HEALTHY"`
4. Present a numbered list showing each project's `name` and `ref` (the project reference ID)
5. Ask the user to select which projects to add (comma-separated numbers, e.g. "1,3,4")
6. Store the selected projects for Step 6

### 6. Assemble `.mcp.json`

1. Read the base `.mcp.json` from `$OUTWORKOS_ROOT/.mcp.json` — this contains the 6 base servers (github, netlify, context7, perplexity, fireflies, google-workspace)
2. Parse it as JSON
3. For each Supabase project selected in Step 5, add an entry using the project's `name` as the key:
   ```json
   "<project-name>": {
     "command": "npx",
     "args": [
       "-y",
       "@supabase/mcp-server-supabase@latest",
       "--project-ref",
       "<project-ref>"
     ],
     "env": {
       "SUPABASE_ACCESS_TOKEN": "<token-value-from-env>"
     }
   }
   ```
4. Write the assembled JSON to `.mcp.json` in the current directory (pretty-printed with 2-space indent)

**Important**: Use the `env` field for the access token, NOT `--access-token` in args. This keeps secrets out of process arguments.

### 7. Test Connections

After assembling all files, test each API token/key by making a lightweight curl call. Read credentials from Vault via `$OUTWORKOS_ROOT/scripts/get-secret.sh` and from `.mcp.json` for MCP-specific tokens.

Run ALL test calls in parallel using separate Bash tool calls for speed.

**Tests to run:**

| Service | Test command | Pass | Fail action |
|---------|-------------|------|-------------|
| GitHub | `curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token <GITHUB_PERSONAL_ACCESS_TOKEN>" https://api.github.com/user` | `200` | Token expired or invalid — regenerate at https://github.com/settings/tokens |
| Netlify | `curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer <NETLIFY_AUTH_TOKEN>" https://api.netlify.com/api/v1/user` | `200` | Token invalid — regenerate at https://app.netlify.com/user/applications#personal-access-tokens |
| Perplexity | `curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer <PERPLEXITY_API_KEY>" -H "Content-Type: application/json" -d '{"model":"sonar","messages":[{"role":"user","content":"ping"}]}' https://api.perplexity.ai/chat/completions` | `200` | API key invalid or expired — check https://www.perplexity.ai/settings/api |
| Supabase | `curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer <SUPABASE_ACCESS_TOKEN>" https://api.supabase.com/v1/projects` | `200` | PAT invalid — regenerate at https://supabase.com/dashboard/account/tokens |
| Fireflies | `curl -s -o /dev/null -w "%{http_code}" -H "Content-Type: application/json" -H "Authorization: Bearer <FIREFLIES_TOKEN>" -d '{"query":"{ user { name } }"}' https://api.fireflies.ai/graphql` | `200` | Token invalid — check https://app.fireflies.ai/integrations |
| Context7 | MCP call: `mcp__context7__resolve-library-id` (see below) | Returns results | API key invalid — check with Upstash |

**How to extract each credential (use these exact methods):**

1. Read `.mcp.json` with the Read tool and parse as JSON. Extract:
   - `GITHUB_PERSONAL_ACCESS_TOKEN` → `mcpServers.github.env.GITHUB_PERSONAL_ACCESS_TOKEN`
   - `NETLIFY_AUTH_TOKEN` → `mcpServers.netlify.env.NETLIFY_AUTH_TOKEN`
   - `PERPLEXITY_API_KEY` → `mcpServers.perplexity.env.PERPLEXITY_API_KEY`
   - `FIREFLIES_TOKEN` → from `mcpServers.fireflies.args`, find the string that starts with `"Authorization: Bearer "` and extract everything after that prefix

2. For Supabase, extract from any Supabase entry in `.mcp.json` → `mcpServers.<any-supabase-server>.env.SUPABASE_ACCESS_TOKEN`. This is reliable because it's already a clean JSON string value. If no Supabase server was added, fall back to Vault: `$("$OUTWORKOS_ROOT/scripts/get-secret.sh" supabase_access_token)`.

**Important**: Prefer reading from `.mcp.json` JSON values or Vault for all credential access.

**Context7 test (MCP-based, not curl):**

Context7 has no public REST endpoint, but the MCP server is typically already connected in the current session. Test it by making a lightweight MCP tool call:

1. Use `ToolSearch` to load `mcp__context7__resolve-library-id`
2. Call it with `libraryName: "nextjs"` and `query: "test connection"`
3. If it returns library results → pass
4. If it errors (auth failure, timeout) → fail — API key invalid, check with Upstash

Run this in parallel with the curl tests above (it's independent).

**Services NOT tested** (note in report but don't fail):
- **Google Workspace**: Uses OAuth refresh tokens — the workspace-mcp server handles token refresh internally. If the refresh token is expired, the server will prompt for re-auth on first use.

**Handling failures:**

For each failed test:
1. Report which service failed and the HTTP status code received
2. Show the specific URL where the user can regenerate the token
3. After listing all failures, ask: "Would you like to update any of these tokens now?"
4. If yes, for each token the user provides:
   - Update the value in Vault via `set-secret.sh` and/or `.mcp.json` as appropriate
   - Re-run that specific test to confirm the new token works
   - Repeat until the token passes or the user chooses to skip
5. If all tests pass, continue to Step 8

### 8. Todoist Sections (if applicable)

If a Todoist project ID is already known for this project (e.g., from a previous `/context-map` run or from the user), ensure the standard status sections exist:

1. Fetch sections via Sync API: `resource_types: ["sections"]`
2. Check if "Triage" section exists for the project ID
3. If missing, create all four sections (Triage, Do, Waiting, Defer) in a single batch:
   ```python
   import json, uuid
   sections = ["Triage", "Do", "Waiting", "Defer"]
   commands = [{"type": "section_add", "uuid": str(uuid.uuid4()), "temp_id": str(uuid.uuid4()), "args": {"name": s, "project_id": PROJECT_ID}} for s in sections]
   with open("/tmp/todoist_batch.json", "w") as f:
       json.dump({"commands": commands}, f)
   ```
4. If no Todoist project ID is known yet, skip — `/context-map` will handle section creation when it sets up the Todoist project

**Standard sections:**
| Section | Purpose |
|---------|---------|
| Triage | New tasks, needs decision |
| Do | Committed, actively working |
| Waiting | Blocked on someone else |
| Defer | Parked for later |

### 9. GitHub Backup Repository (Optional)

Ask the user: **"Do you want to set up a GitHub backup repository for this project?"**

If **no**: skip to Step 10.

If **yes**:

#### 9a. Prerequisites

1. Verify `gh` CLI is available: `gh --version`
2. Verify `gh` is authenticated: `gh auth status`
3. If either fails, stop and tell the user to install/authenticate `gh`

#### 9b. Detect Existing Git State

1. Check if `.git/` already exists in the project directory
   - If yes, ask: "This directory already has a git repo. Skip GitHub backup setup?" — if they want to skip, go to Step 10
2. Scan for subdirectories that contain their own `.git/` (app repos):
   ```bash
   find . -mindepth 2 -maxdepth 3 -name ".git" -type d
   ```
3. Record these paths — they'll be excluded via `.gitignore`

#### 9c. Generate `.gitignore`

Create `.gitignore` with:

```gitignore
# Local config
.mcp.json

# OS files
.DS_Store
Thumbs.db

# Dependencies and caches
node_modules/
__pycache__/
.cache/
*.pyc

# Large binary files
*.zip
*.tar.gz
*.dmg
```

For each subdirectory with its own `.git/` detected in 9b, append a line:
```gitignore
# App repo (has its own git)
subdirectory-name/
```

#### 9d. Initialize and Push

1. `git init`
2. Derive repo name from the project directory name (lowercase, hyphens for spaces, strip special chars)
3. `git add .`
4. `git commit -m "Initial project backup"`
5. `gh repo create MattVOLTA/<repo-name> --private --source=. --push`
6. Verify: `gh repo view MattVOLTA/<repo-name> --json url -q .url`

#### 9e. Create Backup Script

Write `.claude/hooks/backup.sh`:

```bash
#!/bin/bash
# Auto-backup project to GitHub on session end
cd "$CLAUDE_PROJECT_DIR" || exit 0

# Skip if no git repo
[ -d .git ] || exit 0

# Skip if no changes
if git diff --quiet HEAD 2>/dev/null && [ -z "$(git status --porcelain)" ]; then
  exit 0
fi

git add -A
git commit -m "Auto-backup $(date +%Y-%m-%d\ %H:%M)" --no-gpg-sign 2>/dev/null
git push origin HEAD 2>/dev/null
```

Make it executable: `chmod +x .claude/hooks/backup.sh`

#### 9f. Add SessionEnd Hook

Read the project's `.claude/settings.json` (create if missing). Add a `SessionEnd` hook entry:

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/backup.sh\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

If `settings.json` already has hooks (e.g., SessionStart), merge the new SessionEnd entry alongside existing hooks — do NOT overwrite.

#### 9g. Verify

Confirm the repo exists and the hook file is in place:
- `gh repo view MattVOLTA/<repo-name> --json url`
- `ls -la .claude/hooks/backup.sh`

### 10. Report

Confirm all created files exist by reading them. Then print a summary:

```
Project setup complete!

Directory: $OUTWORKOS_PARENT/<project-name>/

Files created:
  .mcp.json
  .claude/commands → $OUTWORKOS_ROOT/skills/  (symlink — all skills available)

Connection tests:
  ✓ GitHub
  ✓ Supabase
  · Google Workspace (OAuth — tested on first use)
  ...

MCP servers configured:
  supabase, google-workspace, github, ...

GitHub backup:
  ✓ Repo: github.com/<user>/<repo-name> (private)
  ✓ SessionEnd hook: .claude/hooks/backup.sh
```

If GitHub backup was skipped, show:
```
GitHub backup:
  · Skipped
```

Use ✓ for passed, ✗ for failed (with note), · for skipped/untestable.

**Next step:** Suggest: "Run `cd $OUTWORKOS_PARENT/<project-name> && claude` then `/context-map` to configure this project."
