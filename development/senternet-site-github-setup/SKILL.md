---
name: senternet-site-github-setup
description: Initialize git, .gitignore, and GitHub repo conventions for a new site.
---

# GitHub Setup

Initialize a git repository, create a `.gitignore`, and establish a branching convention for a Vite + React + Firebase site. Safe to run on a fresh project or one that already has git initialized.

## Steps

### 1. Check if git is already initialized

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

If this returns `true`, skip `git init`. If it fails (not a repo), run:

```bash
git init
```

### 2. Create `.gitignore`

Write `.gitignore` to the project root. Do not overwrite if it already exists — instead read the existing file and append any missing entries.

```gitignore
# ── Dependencies ────────────────────────────────────────────────────────────
node_modules/

# ── Build output ─────────────────────────────────────────────────────────────
build/
dist/

# ── Environment / secrets ────────────────────────────────────────────────────
# Commit .env.example (if present) but never the real env files
.env
.env.local
.env.development
.env.production
.env.staging
.env.*.local

# Google Cloud / Firebase service account keys
service-account*.json
*-service-account.json
*-credentials.json
credentials*.json
*.pem
*.key
gcp-key*.json

# ── Firebase ─────────────────────────────────────────────────────────────────
# .firebaserc and firebase.json are project config — check those IN
# Only ignore the local debug log
.firebase/
firebase-debug.log
firebase-debug.*.log
firestore-debug.log
ui-debug.log

# ── Editors ──────────────────────────────────────────────────────────────────
# JetBrains (IntelliJ / WebStorm / PyCharm)
.idea/
*.iml
*.iws
*.ipr
out/

# VS Code — ignore workspace settings but allow shared extensions list
.vscode/*
!.vscode/extensions.json

# Vim / Emacs swap files
*.swp
*.swo
*~
\#*\#

# ── OS ───────────────────────────────────────────────────────────────────────
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
Desktop.ini

# ── Logs ─────────────────────────────────────────────────────────────────────
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# ── Misc ─────────────────────────────────────────────────────────────────────
*.tsbuildinfo
.eslintcache
.stylelintcache
```

### 3. Verify no secrets are staged

After writing `.gitignore`, run:

```bash
git status
```

Confirm that `.env*` files, `service-account*.json`, and any credential files are listed as **ignored** (not staged). If any appear untracked or staged, stop and investigate before proceeding.

### 4. Initial commit (optional)

Ask the user: "Do you want to create an initial commit with the project skeleton?"

If yes, create the commit using the first available method:
1. **MCP server** — use the GitHub MCP server if configured
2. **`gh` CLI** — use `gh` if available
3. **Git CLI** — fall back to plain `git commit`

Use this commit format for all commits on this project:

```
<title>: TICKET-ID Brief summary

# Problem
<what was broken or missing>

# Solution
<what was done to fix or address it>

# Additional Context
<optional — include only when non-obvious background is needed>
```

For the initial commit, omit the ticket ID segment (no placeholder):
```
init: Initial project scaffold

# Problem
No repository or project structure existed.

# Solution
Scaffolded Vite + React + TypeScript project with Firebase config and .gitignore.
```

If no, stop here — the repo is initialized and `.gitignore` is in place.

### 5. Branching convention

Enforce this branch naming scheme for all future branches on this project. Write it to `.github/CONTRIBUTING.md` so it's visible to collaborators and can be referenced later.

**Format:** `{prefix}/{ticket-id}/{change-summary}`

| Situation | Prefix | Ticket | Example |
|---|---|---|---|
| Team — feature work | developer first name | include if available | `matt/SITE-123/add-social-links` |
| Team — bug fix | developer first name | include if available | `sara/SITE-456/fix-nav-overflow` |
| Lone developer — feature | `feature` | include if available | `feature/SITE-123/add-social-links` |
| Lone developer — bug fix | `fix` | include if available | `fix/nav-overflow` |

Rules:
- Segment separator is `/`
- Change summary is lowercase kebab-case, max ~5 words
- Omit the ticket segment entirely if no ticket ID exists — never use a placeholder
- `main` is the production branch; never commit directly to `main`

Ask the user: "Is this a solo project or a team project?" to determine whether to default to `feature`/`fix` prefixes or developer names.

Create `.github/CONTRIBUTING.md`:

```markdown
# Contributing

## Branch naming

Format: `{prefix}/{ticket-id}/{change-summary}`

- **Team projects:** use your first name as the prefix (e.g. `matt/SITE-123/add-social-links`)
- **Solo projects:** use `feature` or `fix` as the prefix (e.g. `feature/add-social-links`)
- Omit the ticket segment if no ticket ID is available
- Change summary: lowercase kebab-case, ~3–5 words
- Never commit directly to `main`

## Examples

```
matt/SITE-123/add-social-links
sara/SITE-456/fix-nav-overflow
feature/SITE-123/add-social-links
fix/nav-overflow
```
```

### 6. GitHub tooling — MCP server or `gh` CLI

Ask the user:

> "Would you like to connect Claude to GitHub via the GitHub MCP server (lets Claude read/write issues, PRs, and repos directly), use the `gh` CLI instead, or skip this entirely?"

---

#### Option A — GitHub MCP server *(recommended)*

The MCP server lets Claude interact with GitHub's API without leaving the conversation. It requires a GitHub Personal Access Token (PAT).

**Step 6a — Get a Personal Access Token**

Tell the user:

> 1. Go to **github.com → Settings → Developer settings → Personal access tokens → Fine-grained tokens**
> 2. Click **"Generate new token"**
> 3. Give it a descriptive name (e.g. `claude-code-mcp`)
> 4. Set expiration to 90 days or longer
> 5. Under **Resource owner**, select your account (or org if needed)
> 6. Under **Repository access**, choose **All repositories** (or specific repos if you prefer)
> 7. Under **Permissions**, grant:
>    - **Repository permissions:**
>      - Administration: Read and write *(required to create repositories)*
>      - Contents: Read and write
>      - Issues: Read and write
>      - Pull requests: Read and write
>      - Metadata: Read-only (required, auto-selected)
>      - Commit statuses: Read and write
>    - **Account permissions:**
>      - Gists: Read and write (if you use gists)
> 8. Click **Generate token** and copy it — it won't be shown again
> 9. Paste it here so I can add it to your Claude config

Wait for the user to provide the token before proceeding.

**Step 6b — Add MCP server to `~/.claude.json`**

Read the existing file:
```bash
cat ~/.claude.json 2>/dev/null
```

If the file does not exist, create it from scratch. If it exists, merge the new entry into the existing JSON — do not overwrite any other keys.

The target shape (merging into whatever is already there):
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<TOKEN_FROM_USER>"
      }
    }
  }
}
```

Write the merged JSON back to `~/.claude.json`.

Then tell the user:

> "The GitHub MCP server is now configured globally. **Restart Claude Code** for it to take effect. After restart, I'll have direct access to GitHub — you won't need to run `gh` commands manually for most tasks."

---

#### Option B — `gh` CLI

Check if already installed:
```bash
which gh
```

If already installed, skip to authentication instructions. If not installed, ask:

> "The `gh` CLI is not installed. Want me to install it via Homebrew?"

If yes:
```bash
brew install gh
```

Once installed (or if already present), tell the user:

> Run the following command to authenticate:
> ```
> gh auth login
> ```
> When prompted:
> 1. Choose **GitHub.com**
> 2. Choose **HTTPS**
> 3. Choose **Login with a web browser** (easiest) or paste a token
> 4. Follow the prompts to complete auth
>
> Verify with: `gh auth status`

---

#### Option C — Skip

If the user wants neither, skip this step. GitHub operations will require manual `git remote` commands for pushing; note this in the session.

---

**Tooling preference recorded:** For all commits and GitHub interactions (issue lookups, PR creation, repo management), use this priority order: MCP server → `gh` CLI → plain `git`/CLI. If neither MCP nor `gh` is set up, use plain `git` commands and ask the user to run anything that requires GitHub API access manually.

### 7. Create GitHub remote (optional)

Ask the user: "Do you want to create a GitHub remote for this repo?"

If yes, ask for:
- **Repo name** (default: the site directory name)
- **Visibility**: public or private (default: private)

**If MCP server is available** — use it to create the repo via the GitHub API, then run locally:
```bash
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git
git push -u origin main
```

**If using `gh` CLI** — create the repo and push in one step:
```bash
gh repo create $REPO_NAME --$VISIBILITY --source=. --remote=origin --push
```

**If neither** — tell the user to create the repo manually on github.com, then run:
```bash
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git
git push -u origin main
```

## Notes

- `.env.development` and `.env.production` contain real GA IDs, pixel IDs, and other production values — they must never be committed
- `.firebaserc` and `firebase.json` contain no secrets and should be committed — they are not in the `.gitignore`
- `build/` is regenerated on every deploy so committing it wastes storage and causes noisy diffs
- The `.firebase/` cache directory is machine-local and grows large — always ignore it
- If the user later needs to share env variable names (without values), suggest creating a `.env.example` file and committing that instead
- When creating branches later in this project, always follow the established convention: solo → `feature/` or `fix/`; team → `name/`; append ticket ID when available
- The GitHub MCP server is configured globally in `~/.claude.json` — it applies to all projects on this machine, not just this one
- The PAT stored in `~/.claude.json` grants repo access; treat that file like a credentials file and never commit it

## Framework: Next.js track

On the `nextjs` track this step is **required, not optional, and must run before Firebase setup.** Firebase App Hosting builds from a connected GitHub repository and deploys on pushes to a branch, so `firebase apphosting:backends:create` cannot complete without a remote and at least one pushed commit.

Order of operations: `git init` → `.gitignore` → create the GitHub repo → push `main` → then run `/senternet-site-firebase`.

`.gitignore` additions specific to this track: `.next/`, `next-env.d.ts` is committed (not ignored), and `.env*.local` stays untracked. Everything else about the recommended ignore list is unchanged.

See `/senternet-site-framework` for the full convention map.
