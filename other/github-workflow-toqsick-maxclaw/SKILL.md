---
name: github-workflow
description: >-
  Complete GitHub workflow: authentication (HTTPS/SSH/gh CLI), PR lifecycle (branch, commit, open, CI, merge), code review (local and PR-level), issue management (create, triage, label, assign), repository management (clone, create, fork, remotes, releases, secrets), and **read-only CI failure diagnosis from issue/PR + workflow YAML**. Plus skill conversion & config-sync workflow (push converted skill sets into populated repos via HTTPS+token URLs, flat-id namespaces, feature branches, secrets pre-flight). NEU 2026-07-03: gh repo create silent-failure, populated-repo push rejection, Hub↔Hermes skill conversion workflow. NEU 2026-07-07: Batch File Push via Contents API (PUT /repos/{o}/{r}/contents/{path}) — 409 stale-SHA pitfall, MD5 cross-check verification, domain-specific template reusability warning. NEU 2026-07-07: Read-only CI-Diagnose — `gh api` raw-body quirks (empty 404 / JSONDecodeError), tree-API ground-truth check, `needs:` skip chain, stale-issue table verification.
version: 1.2.0
author: Hermes Agent (curator consolidation)
license: MIT
platforms:
  - linux
  - macos
  - windows
metadata:
  hermes:
    tags: ['GitHub', 'Git', 'Pull-Requests', 'Code-Review', 'Issues', 'Repositories', 'CI/CD', 'Automation']
    related_skills: ['coding-agents']
lane: worker-flash
reasoning_effort: high
agent: Engineer
routing_hint: |
  **Agent-Scope:** Code-Tasks (build / fix / refactor / debug / review). Off-scope: visual design, long-form copy, data modeling — say 'this is Designer/Writer/Analyst's territory' and return to Yuno.
  
  Routing-Spec: `yuno-team-routing`.
  
---
# GitHub Workflow — Complete Guide

End-to-end GitHub operations: auth, PRs, code review, issues, and repo management. Each section shows `gh` first, then `curl` fallback.

## Auth Setup

See `references/github-auth.md` for full auth guide. Quick reference:
- **gh CLI:** `gh auth login` (interactive) or `echo "<token>" | gh auth login --with-token`
- **HTTPS token:** `git config --global credential.helper store` → paste token on first operation
- **SSH:** `ssh-keygen -t ed25519` → add public key at https://github.com/settings/keys
- **API without gh:** `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/...`

### MCP GitHub vs `gh` CLI Fallback (2026-06-30)

Hermes kann GitHub über zwei völlig getrennte Pfade ansprechen, und **die Credentials sind NICHT geteilt**:

| Pfad | Auth-Quelle | Token-Speicher |
|------|-------------|----------------|
| `mcp_github_*` Tools (MCP) | `mcp_servers.github.env.GITHUB_TOKEN` in `~/.hermes/config.yaml` | Docker-Container-Env |
| `gh api ...`, `gh issue ...` etc. | `gh auth login` (keyring) oder `~/.config/gh/hosts.yml` | System-keyring + Config |

**Symptom wenn MCP GitHub 401t während `gh` CLI funktioniert:**
```
mcp_github_get_me() → {"error": "failed to get user: GET https://api.github.com/user: 401 Bad credentials []"}
gh auth status       → ✓ Logged in to github.com account Toqsick
```

**Was dann zu tun ist (Pitfall-Pattern):**
1. **NICHT** mehrfach MCP-Tools retryen — das ändert nichts, weil MCP eigene Credentials hat.
2. **NICHT** blind `mcp_servers.github.env.GITHUB_TOKEN` patchen — kann Config-Drift zwischen MCP-Docker-Container und Host-`gh` Auth verursachen.
3. **Sofort auf `gh` CLI umsteigen** für read-only Operations:
   - User-Suche: `gh search users --json login,name`
   - Repo-Liste: `gh repo list Toqsick --json name,pushedAt,description`
   - Issues: `gh issue list --repo Toqsick/hermes-v7 --state open`
   - Issue-Body: `gh issue view 1 --repo Toqsick/hermes-v7 --json body | jq -r .body`
   - PR-Suche: `gh search prs --author Toqsick --state open --json number,title,repository`
   - API-generisch: `gh api "repos/Toqsick/hermes-v7/contents/ROADMAP.md" --jq .content`
4. **Verifizieren** mit `gh auth status` — zeigt aktiven Account + Token-Scopes.
5. **Bei MCP-Fix-Bedarf:** siehe `devops/hermes-admin` Skill → "Auth prüfen" Sektion (Container-Restart nach `config.yaml`-Patch nötig).

**Wann MCP reparieren statt umgehen:** Wenn der User explizit MCP-basierte Features nutzt (z.B. MCP-Tool-Routing via Plugin-Registry) oder wenn mehrere Sessions neu starten müssen. Für einmalige Research-Tasks: **`gh` CLI ist schneller und zuverlässiger** als MCP-Config-Debugging.

**MCP-tool response traps (verified 2026-07-07 batch CONTRIBUTING.md push):**
- **`mcp__github__create_or_update_file` may return "File already exists. Provide SHA." even when the file genuinely does NOT exist on the target repo.** Verified: file was missing (curl 404), MCP said "already exists", but the server-side write still went through and the file appeared on the next GET. Treat MCP write errors as **soft signals, not ground truth**. After any error from this tool, always curl-verify the resulting state with `curl -s -o /dev/null -w "%{http_code}" https://raw.githubusercontent.com/OWNER/REPO/BRANCH/PATH`.
- **`mcp__github__get_file_contents` returns a sentinel success with SHA `777035533703e3b24b90916e17598aeb2f8fb17a`** for files that don't exist (curl gives HTTP 404). Never trust MCP existence checks — always curl-confirm with `https://api.github.com/repos/OWNER/REPO/contents/PATH?ref=BRANCH` and parse the JSON.
- **`mcp__github__create_or_update_file` enters "MCP server 'github' is unreachable after 3 consecutive failures. Auto-retry available in ~32s." cooldown** after repeated failures. Do not keep hammering it — switch to `gh api -X PUT` or curl with `gh auth token` for the rest of the session. The cooldown is per-tool-call, not per-session, and the warning explicitly says "Do NOT retry this tool yet".
- When MCP and curl disagree on a file's existence, **curl wins**. MCP's success metadata is not authoritative for filesystem-shape questions (file present? which SHA? which size?).

**Beispiel-Workflow für Repo-Audit (read-only via `gh`):**
```bash
# Repo-Inventar
gh repo list Toqsick --limit 100 --json name,description,pushedAt

# Heutige Commits (alternative zu MCP search)
gh api "repos/Toqsick/$repo/commits?since=$(date +%Y-%m-%d)T00:00:00Z&per_page=100" --jq 'length'

# Issue-Triage mit Labels
gh issue list --repo Toqsick/$repo --state open --limit 20 --json number,title,labels,createdAt \
  | jq -r '.[] | "#\(.number) [\(.labels | map(.name) | join(","))] \(.title)"'
```

### "Was wurde kürzlich gepusht?" — Push-Audit-Recherche

Wenn User behauptet „du hast gestern gepusht" / „da wurde was committed" / „ich glaub mein Auto-Push ist gelaufen" — die Frage ist **„was sagt der Remote-Stand im Vergleich zu lokal?"**, nicht „was sagt mein lokales Log?".

**Ground-Truth-Reihenfolge:**
1. `git ls-remote origin` → autoritativ, zeigt direkt was remote existiert (SHA + Ref pro Branch/PR)
2. Vergleich mit `git rev-parse origin/main` und `git rev-parse HEAD` → identisch = nichts gepusht
3. Wenn MCP GitHub 401 wirft: **nicht** retryen, sondern direkt `gh api` oder `git ls-remote` nutzen
4. Wenn `curl https://api.github.com/repos/.../commits` **404** zurückgibt → Repo ist **privat**, das ist eine nützliche Diagnose, kein Fehler

Vollständige Verifikationsmatrix (MCP/ls-remote/gh/public-API Triangulation), häufige Fehler (z. B. „Working tree clean ≠ nichts gepusht") und Session-Recipes: siehe `references/push-audit-research.md`.

## PR Lifecycle

See `references/github-pr-workflow.md` for full guide. Quick reference:

```bash

set -euo pipefail
# Branch → Commit → Push → Create PR → Monitor CI → Merge
git checkout -b feat/description
git add . && git commit -m "feat: description"
git push -u origin HEAD
gh pr create --title "feat: description" --body "Summary\n\nCloses #42"
gh pr checks --watch
gh pr merge --squash --delete-branch
```

## Code Review

See `references/github-code-review.md` for full guide. Quick reference:

### Local Changes (Pre-Push)
```bash

set -euo pipefail
git diff main...HEAD --stat      # scope
git diff main...HEAD             # full diff
git diff main...HEAD | grep -n "print\|console\.log\|TODO\|FIXME"  # debug statements
```

### PR Review on GitHub
```bash

set -euo pipefail
gh pr view 123
gh pr diff 123
git fetch origin pull/123/head:pr-123 && git checkout pr-123  # local checkout
gh pr review 123 --approve --body "LGTM"
gh pr review 123 --request-changes --body "See inline comments"
```

### Inline Comments (curl fallback)
```bash

set -euo pipefail
# Get HEAD SHA, then POST to /repos/{owner}/{repo}/pulls/{number}/reviews
```

## Issue Management

See `references/github-issues.md` for full guide. Quick reference:

```bash

set -euo pipefail
# Create
gh issue create --title "Bug: X" --body "..." --label "bug" --assignee "@me"

# List
gh issue list --state open --label "bug"
gh issue list --assignee @me

# Manage
gh issue edit 42 --add-label "priority:high"
gh issue edit 42 --add-assignee username
gh issue comment 42 --body "Investigated — working on fix"
gh issue close 42
gh issue reopen 42
```

### Pitfalls

- **`gh issue view <N> --json ...` does NOT include `number`** (it also strips `repository`). The output gives title/body/labels/comments/state, but every field you'd reasonably expect from `gh issue list --json number,title,...` is *missing*. Python parsers that do `d['number']` get `KeyError`. Workarounds: (a) pair each `gh view` with the number you already know — `[{"number": <N>, **d}]`; (b) read numbers from `gh issue list --json number,title` separately and join. Verified 2026-07-07 on Toqsick/greyscripts triage — every per-issue read needed this fix.

- **Read-only vs mutating triage — ask before assuming.** When the user says "kategorisieren", "priorisieren", "review", "audit", default to **read-only** (categorize, write report, but do NOT add labels / comments / close anything). Explicitly note "read-only" in the report footer so the user knows. Only mutate when the user explicitly says "label them", "close the empty ones", etc. Many reviewer/external/audit profiles do not have mutation rights.

- **Cross-check the user's numerical assumptions.** If the user names a count ("alle 54 offenen Issues") or describes scope, verify against actual API state before diving in. The discrepancy is load-bearing context — the user may be working from a stale mental model, the repo was recently groomed, or they're testing whether you'll blindly trust framing. Surface the gap clearly at the top of the report; don't silently adjust and proceed. Verified 2026-07-07: user said "54", repo had 7 (other 47 closed) → flagging this upfront saved the session.

- **Triage-report shape — what the user actually wants.** A categorized, prioritized Markdown report, not just a list. Default deliverable: per-issue row with number/title/category/labels/priority/recommendation; activity check (`age_days` + `stale_days`, flag stale beyond threshold); empty-body issue detection (CI-badge-only or "[BUG]" placeholder → recommend `state_reason=not_planned`); recommended execution order based on dependency graph; summary table by category. Skip any of these only when the user signals a different deliverable.

## Repository Management

See `references/github-repo-management.md` for full guide. Quick reference:

```bash

set -euo pipefail
# Clone/Create/Fork
gh repo clone owner/repo
gh repo create my-project --public --clone
gh repo fork owner/repo --clone

# Settings
gh repo edit --description "..." --visibility public
gh repo edit --enable-auto-merge

# Releases
gh release create v1.0.0 --title "v1.0.0" --generate-notes

# Secrets
gh secret set API_KEY --body "value"
gh secret list

# Actions
gh workflow list
gh run list --limit 10
```

### Documentation Health Audit

When the user asks to update READMEs, check what's outdated, or audit repo docs, use the pattern from `references/documentation-health-audit.md` (10 phases).

**Core phases (1–7):** Parse claims → Count state → Count support files → Verify standalone deps → Find thin sub-READMEs → Cross-reference category listings → Verify CI badges

**Post-update phases (8–10):** Markdown verification → Thin README expansion → Category table enrichment

**Common pitfalls:**
- `find . -maxdepth 2` avoids counting nested build outputs and git-internal copies
- Always exclude `bin/`, `build/`, `src/`, `test/`, `tests/`, `includes/`, `scripts/` from tool counts — these are support, not tools
- `grep -l` + `xargs` avoids false positives from backup dirs; use `find -path './de/*' -prune` to exclude import snapshots
- standalone.md is usually the most stable doc (deps don't change), main README is the most drift-prone (numbers get stale)
- After updating READMEs, always run Phase 8 (Markdown verification) — even text-only changes can break links or introduce syntax errors
- Thin READMEs (< 500B) are often template placeholders; expand with real build paths and feature descriptions (600–1100B target)

See `references/documentation-health-audit.md` for the full shell script patterns, execute_code alternatives, and a session example.

## GitHub Automation Scripts

See `references/github-automation-patterns.md` for a complete pattern. Quick reference:

```bash

set -euo pipefail
# Build a reusable Python automation script
scripts/
  hermes-automation.py    # Main CLI: issue, branch, build, pr, status, etc.

# Typical commands:
python3 scripts/hermes-automation.py issue --title "Bug: X" --label bug --milestone v1.0.0
python3 scripts/hermes-automation.py branch --issue 42 --name feature/toolname
python3 scripts/hermes-automation.py pr --issue 42 --title "feat: tool Closes #42" --body "..."
python3 scripts/hermes-automation.py status --json > results/status.json
```

### GreyHack/Greybel CI addendum

For GreyHack repos that use `greybel-js`, see `references/greybel-ci-pattern.md`. It captures the current `greybel build  <output-dir>` syntax, the fact that the installed executable may be named `greybel` rather than `greybel-js`, how to avoid stale imported-tool directories in default CI, and safe issue/PR body handling with `--body-file`.

**Key patterns:**

1. **Single script, multiple subcommands** — use `argparse` with subparsers for `issue`, `branch`, `build`, `pr`, `status`, etc.
2. **`gh` CLI as primary interface** — all GitHub API calls through `gh api`, `gh issue`, `gh pr`
3. **Clean JSON output for cron jobs** — when `--json` is passed, output ONLY valid JSON (no status text, no progress logs). Put human-readable output in the non-JSON path.
4. **Build verification** — for code repos, add a `verify-all` command that builds/tests all source files and writes results to `results/`.
5. **Cron integration** — schedule daily status checks with `hermes cronjob create`. Use `[SILENT]` protocol when nothing changed.
6. **Shell escaping** — when passing multi-line strings to `gh pr comment --body`, wrap in single quotes or write body to a temp file to avoid shell interpreting backticks and `$`.

**Pitfalls:**

- **Backticks in shell strings**: `gh pr comment --body "Text with `code`"` will execute `code`. Use single quotes or `gh pr edit --body-file` / `gh pr create --body-file`.
- **JSON pollution**: If `--json` outputs anything before the JSON object, downstream parsers fail. Gate all print statements with `if not json_output`.
- **Subagent rate limits**: When using multi-agent orchestration for GitHub tasks, subagents may hit API rate limits. Parent should verify claims and complete critical fixes directly.
- **Working tree cleanliness**: Before JSON status reports, clean `__pycache__/` and other generated artifacts to avoid false "dirty" reports.
- **Duplicate PR cleanup**: When creating PRs programmatically across multiple branches, check for stale duplicate PRs before reporting status. Close duplicates with `gh pr close <num> --comment "Duplicate of #<target>"`.
- **Issue/PR state drift**: GitHub does not always auto-close issues when PRs merge. If the PR title has `(#3)` but the body doesn't contain `Closes #N`, the issue stays OPEN even after merge. Always use `Closes #N` or `Fixes #N` in the PR body, and manually close with `gh issue close <num>` if drift is detected.

## Batch File Push via Contents API

When the user wants the **same file** (e.g. `CONTRIBUTING.md`, `LICENSE`, `.github/CODEOWNERS`, a policy file) pushed to **multiple repos in one shot**, prefer the Contents API (`PUT /repos/{o}/{r}/contents/{path}`) over `git clone` × N: faster, no local working tree, atomic per-repo commit.

**Pattern (gh CLI, parallel across repos):**

```bash
# Pre-encode once, reuse for every repo
CONTENT_B64=$(base64 -w0 /path/to/file)
COMMIT_MSG="docs: add CONTRIBUTING.md"

push_one() {
  local repo="$1" branch="$2"
  local body
  body=$(jq -n --arg m "$COMMIT_MSG" --arg c "$CONTENT_B64" --arg b "$branch" \
    '{message:$m, content:$c, branch:$b}')
  local resp
  resp=$(gh api -X PUT "repos/OWNER/$repo/contents/PATH" \
    -H "Accept: application/vnd.github+json" \
    --input - <<<"$body" 2>&1)
  if echo "$resp" | jq -e '.commit.sha' >/dev/null 2>&1; then
    echo "OK  $repo@$branch  commit=$(echo "$resp" | jq -r '.commit.sha' | head -c7)"
  else
    echo "FAIL $repo@$branch  $(echo "$resp" | head -c 200)"
  fi
}

push_one repo-a main
push_one repo-b main
push_one repo-c master   # some repos use master, some main
```

### Pitfalls

- **`409 Conflict` "is at <real-SHA> but expected <stale-SHA>":** `gh api PUT contents/` caches a stale HEAD-SHA from an earlier fetch in the same process. The repo HEAD moved (parallel worker, CI, web commit) but the request still carries the old expected blob SHA. **Fix:** retry **without** the `sha` field — the API then treats the request as a fresh Create-or-Update against current HEAD. To overwrite an existing file intentionally, fetch the current `sha` first and pass it explicitly.
  ```bash
  # Retry without sha (Create path)
  body=$(jq -n --arg m "$COMMIT_MSG" --arg c "$CONTENT_B64" \
    '{message:$m, content:$c, branch:"main"}')
  gh api -X PUT "repos/OWNER/$repo/contents/PATH" --input - <<<"$body"

  # Or with current sha (Update path)
  CUR_SHA=$(gh api "repos/OWNER/$repo/contents/PATH" --jq .sha 2>/dev/null)
  body=$(jq -n --arg m "$COMMIT_MSG" --arg c "$CONTENT_B64" --arg s "$CUR_SHA" \
    '{message:$m, content:$c, branch:"main", sha:$s}')
  ```

- **Default branch matters.** `gh api repos/OWNER/REPO --jq .default_branch` is the source of truth — never trust user-supplied branch names in a batch task. Pushing to a non-existent branch returns 422, not 409.

- **Content field is base64-with-embedded-newlines.** GitHub inserts `\n` every 60 chars. `jq -r '.content' | base64 -d` works; `base64 -d` directly on the raw JSON string fails silently. Use `-w0` on encode side for round-trip determinism.

- **Push returning `200 OK` + `commit.sha` ≠ content-is-correct.** Verify byte-identicality after a batch push with an MD5 cross-check (catches CRLF/LF/BOM drift, truncation, accidental overwrites):
  ```bash
  SOURCE_MD5=$(md5sum /path/to/file | awk '{print $1}')
  for repo in repo-a repo-b repo-c; do
    remote_md5=$(gh api "repos/OWNER/$repo/contents/PATH" --jq '.content' 2>/dev/null \
      | base64 -d 2>/dev/null | md5sum | awk '{print $1}')
    [ "$remote_md5" = "$SOURCE_MD5" ] && echo "MATCH  $repo" || echo "DIFFER $repo"
  done
  ```

- **When NOT to use this pattern:** files > ~100 MB (Contents API truncates), repos with branch protection that block direct main commits (use a feature branch + PR), or files with merge-conflict potential (e.g. existing `CONTRIBUTING.md` with project-specific content — overwriting silently is destructive).

- **Domain-specific templates may not be reusable.** When copying a `CONTRIBUTING.md` / `LICENSE` / template from one repo, **read it first** and check that the language/structure fits the target repos. A GreyScript template with `importcode` / `fail()` / `shell` rules is useless in a TypeScript/React project. Fall back to a generic template if the source is too domain-specific. Verified 2026-07-07: greyscripts-`CONTRIBUTING.md` (38 lines, German, GreyScript conventions) was not reusable across 4 mixed repos (hermes-v7, MaxClaw, sse-dashboard, multi-agent-workflows) — fell back to a 14-line generic MIT-licensed template.

## Skill Conversion & Config-Sync Workflow

When user asks to 'push my skills to github', 'sync skills between devices', 'convert skills from <X> to <Y>' — these are common, distinct from PR work, and follow a non-obvious pattern. Apply this 7-step workflow:

1. **Inventory target repo first.** `gh repo view <name> --json name,description,pushedAt,defaultBranchRef`. Discover if repo exists or whether `gh repo create` would fail silently.
2. **If repo exists and has unrelated code:** `gh repo clone <name> ~/worktree`. Don't `gh repo create` — it errors with `Name already exists`.
3. **If repo doesn't exist** and you already have a local working tree ready (e.g. `/tmp` stage dir), use the **atomic pattern**:
   ```bash
   cd /path/to/local-working-tree
   git init -q
   git config init.defaultBranch main   # ← PREVENT master-branch issue
   git add -A && git commit -q -m "Initial commit"
   gh repo create <name> --private --description "..." --source=. --push
   ```
   The `--source=. --push` flag creates the remote AND pushes in one command — no separate `git remote add` needed. **BUT:** `gh repo create` with `--source=. --push` pushes the **local** branch name as-is. If you forget `config init.defaultBranch main`, the remote gets `master`. Fix:
   ```bash
   git branch -m master main
   git push origin main
   gh repo edit --default-branch main  # update GH's default ref
   ```
   **Simpler: set `init.defaultBranch main` before git init** — then the remote gets `main` directly.

   Without `--source=. --push` (older pattern, still valid):
   ```bash
   gh repo create <name> --public --description '...'
   git remote add origin "https://github.com/USER/<name>.git"
   git push -u origin main
   ```
4. **Use HTTPS-with-token from `gh auth token`** for push, not SSH:
   ```
   TOKEN=$(gh auth token)
   git remote set-url origin "https://Toqsick:${TOKEN}@github.com/Toqsick/<repo>.git"
   git push -u origin main
   ```
   This avoids SSH-host-verification failures which turn into long debugging.
5. **Pick a flat-id namespace under one umbrella dir.** For skill conversion (Hub ↔ Hermes, etc.), never merge categories — use e.g. `skills/hub-imported/<hub-id>/`. See `software-development/skill-format-conversion` for the canonical workflow.
6. **Commit on a feature branch if the default branch is populated.** Use `git switch -c feat/skills-import-<date>`. Then `gh pr create` for review.
7. **Always include secrets-preflight** when converting skills: many skill-system source trees carry `~/.hermes/auth.json` references or hardcoded tokens. `grep -rE '(api[_-]?key|secret|password|bearer|token)[^[:space:]]{0,5}[:=]["'"'"']?[A-Za-z0-9_-]{16,}'` over the source before committing.

**Pitfall — pushing to a populated repo on `main`:**
```
$ git push -u origin main
To https://github.com/<owner>/<repo>.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs
```
This means the repo has commits you don't have. Either:
1. `git fetch origin && git merge origin/main --allow-unrelated-histories` (if desired to add on top)
2. Branch instead: `git switch -c feat/skills-2026-07-03-import && git push -u origin feat/skills-2026-07-03-import && gh pr create`
- **Shell escaping in `gh pr comment`**: Multi-line bodies with backticks get executed by the shell. Use single quotes or `--body-file` to avoid command substitution.
- **Missing labels/milestones**: `gh issue create --label` fails if the label does not exist. Check labels first or create missing labels intentionally. Some `gh` versions lack `gh milestone`; use `gh api -X GET 'repos/{owner}/{repo}/milestones?state=all'` instead.
- **Workflow YAML linting**: Quote the GitHub Actions trigger key as `"on":` to avoid `yamllint` truthy-value warnings.

**Issue-to-PR workflow pattern:**

```

set -euo pipefail
1. Merge automation PR first
2. Create feature branch from develop
3. Build/verify target file
4. Fix syntax/import errors
5. Commit + push
6. Create PR with `Fixes #<issue>`
7. Clean up duplicate PRs if any
8. Show final status
```

This pattern was validated with Issue #5 (`routerinfo`) on 2026-06-18.

## GreyHack/Greybel CI pattern

For GreyHack repos that build GreyScript with `greybel-js`, treat CI as a first-class issue/PR flow, not just a script edit:

```bash

set -euo pipefail
# 1. Create explicit CI issues before coding.
gh issue create --title '[CI] Add Greybel build verification to CI' --body-file /tmp/issue-ci-greybel-build.md --label ci,enhancement,roadmap --milestone v0.5.0
gh issue create --title '[CI] Make ci-build.sh scan active .src directories' --body-file /tmp/issue-ci-build-script.md --label ci,bug,enhancement --milestone v0.5.0

# 2. Branch from develop and implement both sides of the CI contract.
git checkout -b feat/p0-ci-greybel-build

# 3. Update the build script to scan active source dirs, not stale bin/ paths.
# 4. Add a workflow job that installs greybel-js, runs the script, and uploads outputs.
# 5. Commit, push, and open a PR with `Closes #<issue>` lines in the body.
```

Use this shape:

- `scripts/ci-build.sh` scans active `.src` directories such as `src/`, `tools/`, and `greyhack-tools/` if present.
- CI installs `greybel-js` with `npm install -g greybel-js`.
- CI runs `bash scripts/ci-build.sh --out-dir .ci-build`.
- CI uploads `.ci-build/` as an artifact.
- `.gitignore` ignores `.ci-build/`.
- Quote the workflow trigger key as `"on":` to avoid `yamllint` truthy warnings.

**Pitfalls:**
- Workflow TODOs may live in docs/plans instead of `.github/workflows/*.yml`; scan docs and plans too.
- `gh api repos/OWNER/REPO/milestones` defaults to POST; use `gh api -X GET 'repos/{owner}/{repo}/milestones?state=all'`.
- `gh milestone` may be unavailable in the installed gh CLI; use `gh api` for milestones.
- `gh issue create --label roadmap` fails if the label does not exist; create the label first or use existing labels.
- Use `--body-file` for `gh pr create` / `gh pr edit` when the body contains backticks/code fences; otherwise the shell may execute code inside backticks.

See `references/greyhack-greybel-ci.md` for a concrete session reference with the issue/PR URLs, changed files, validation commands, and pitfalls.

## Read-only CI Failure Diagnosis (gh CLI workflow)

When the user reports "CI is red", "build fails", "issue #N says build broken", or asks to debug CI without committing anything — use this recipe. It is **read-only by design**: no commits, no workflow edits, no `--push`, no PR comments unless explicitly requested.

### Workflow

```bash
# 1. Find the failing run
gh run list -R OWNER/REPO --limit 10 --json databaseId,status,conclusion,name,headBranch,event,createdAt

# 2. Get the failed-step log (mixes labels + ANSI + real errors — filter)
gh run view <run-id> -R OWNER/REPO --log-failed 2>&1 | grep -E '##\[error\]|exit code [0-9]+|Process completed' | head -40

# 3. Read the workflow YAML that owns the failing job
gh api 'repos/OWNER/REPO/contents/.github/workflows/<file>.yml?ref=main' \
  -H 'Accept: application/vnd.github.raw'

# 4. Cross-reference with issue body (always read the actual issue body, not the summary)
gh issue view N -R OWNER/REPO --json title,body,labels

# 5. Verify every file path mentioned in the issue actually exists on main
#    (issue tables often cite stale paths after a rename or repo restructure)
gh api 'repos/OWNER/REPO/git/trees/main?recursive=1' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('\n'.join(e['path'] for e in d['tree'] if e['path'].endswith('.src')))"

# 6. Fetch each surviving file with raw endpoint + sed to the exact lines
gh api 'repos/OWNER/REPO/contents/<path>?ref=main' -H 'Accept: application/vnd.github.raw' | sed -n '20,32p'
```

### Output shape

The deliverable is a Markdown report in `~/docs/system/<repo>-ci-diagnose-<date>.md` with these sections:

1. **TL;DR table** — CI-Workflow / Helper-Skript / Issue A / Issue B / real root cause
2. **Which jobs fail?** — full job graph + which step inside each failing job, distinguishing "skipped because `needs:`" vs "actually failed"
3. **Root-cause analysis** — split into "actual CI killer" + "outdated issues that name the wrong files"  
4. **Concrete fix proposals** — patch-style diff snippets for each, ranked P0/P1/P2
5. **Verification commands** — what to run after the fix to confirm green
6. **Issue comment drafts** (do NOT post unless asked) — wording the user can copy into the issue thread
7. **Repro commands** — copy-pasteable for next session

Always footer the report with `**Analyse-Modus:** read-only (gh-CLI + GitHub-API only, keine Code-Mutation)` so it's clear no writes happened.

### Pitfalls — these all bit on 2026-07-07 Toqsick/greyscripts triage

**`gh api …/contents/<path>?ref=main` with `Accept: application/vnd.github.raw` returns empty body for paths that don't exist** — looks like a successful empty response, not an error. Combine with `git/trees/main?recursive=1` to verify path existence first; if the tree lists the path, the empty body means a different branch or a renamed file. Verified pattern: `bin/ps.src` from Issue #43 was a stale path — the file lived under `greyhack-tools/ps/ps.src` (and had already been fixed). Tree-API before raw fetch = zero wasted fetches.

**`gh api …/contents/<path>` (no `Accept: raw` header) returns JSON with `content_base64` field — NOT `content`.** Earlier docs and Stack Overflow snippets say `base64.b64decode(d['content'])`. That field doesn't exist on the Contents API — it's `content_base64`. Piping JSON to `python3 -c "import json,sys,base64; print(base64.b64decode(json.load(sys.stdin)['content']))"` returns `KeyError`. Use `content_base64` or, better, switch to the raw endpoint to avoid the dance entirely.

**JSONDecodeError "Extra data: line 1 column 128" from `python3 -c "json.load(sys.stdin)"`** — means `gh api` output got piped into something and `gh` wrote two JSON-like blocks to stdout (the API response + a status/log line). Switch to the raw endpoint (`-H 'Accept: application/vnd.github.raw'`) to skip the JSON wrapper entirely. Do not try to "fix" the JSON parser — the problem is the wrapper.

**`needs:`-chain jobs are skipped, not failed.** When job 1 fails with exit 1, job 2 (which has `needs: job-1`) shows as "skipped" in the run summary. Don't trust "skipped" as a green signal — trace back to find which upstream job actually failed. The "real" CI killer is often job 1, not the job the issue title names. Verified: Toqsick/greyscripts issue #30 said "Greybel build failt" but the actual red job was `lint-yaml` (yamllint default rules vs. no override) → `greybel-build` was only skipped.

**Stale issue tables — verify before fixing.** Issue bodies often contain tables with `| Datei | Zeile |` listings. Before patching any file at the listed line, verify the file exists at the listed path on the current `main` and the line still contains what the issue claims. Repos rename directories, move files into `core/` or `lib/` subfolders, and earlier bug-sweep commits fix issues without closing them. Treat issue tables as **hypotheses** until verified against `git/trees/main?recursive=1` + raw file fetch. Verified: Issue #43 listed 5 `bin/ps.src:24`-style sites — none of those paths existed on `main` (`bin/` was reduced to `.gitkeep`). The real fixes lived under `greyhack-tools/` and were already applied.

**Read existing helper scripts before flagging "missing tooling".** A repo may already have a helper script (e.g. `lint-workflows.sh`) that the CI workflow simply doesn't call. The diagnosis is "wrong wiring", not "missing tool". Check `.github/workflows/lint-*.sh` and `scripts/ci-*.sh` first. Verified: Toqsick/greyscripts had `lint-workflows.sh` with the correct yamllint override — `ci.yml` just didn't invoke it.

**`exit_code: 2` at the end of `gh run view … --log-failed` is normal.** The run failed (that's why you're reading the log). Don't report this as a new error.

**`process.completed with exit code 1` ≠ test failures inside the job.** GitHub Actions reports the step exit code as the job exit code. Look for `##[error]` markers in the log to find which command actually returned non-zero.

### When the real cause is upstream tooling, not the issue

A common pattern: issue A says "X is broken", issue B says "Y is broken", but the CI run they both point to failed in a completely different job (`lint-yaml`, `setup-node`, `setup-python`). Steps to take:

1. State explicitly: "Issue #A beschreibt X. Realer Fail-Stand ist Y (anderer Job, andere Ursache)." — don't bury the lede.
2. For each cited issue, check whether the cited fix would even be observable in the failing CI run. Often the cited failure mode is downstream of an upstream block.
3. Propose P0 fix for the actual CI killer (usually a 1-line workflow edit), then P1+ for the issue's original concern.
4. Suggest the issue gets a comment with status update rather than being closed prematurely.

See `references/ci-failure-diagnosis.md` for a worked example: Toqsick/greyscripts Issue #30 + #43 (yamllint override mismatch + stale issue tables).

## Cron Monitoring

```bash

set -euo pipefail
# Daily status check
hermes cronjob create \
  --schedule "0 9 * * *" \
  --name "repo-daily-status" \
  --prompt "Check git status, open issues, open PRs. If nothing changed: [SILENT]"
```

See `references/github-automation-patterns.md` for the full cron prompt template and `[SILENT]` protocol.

## References

- `references/github-auth.md` — Auth setup (HTTPS, SSH, gh CLI, API detection)
- `references/github-pr-workflow.md` — PR lifecycle (branch, commit, CI, merge)
- `references/github-code-review.md` — Code review (local, PR, inline)
- `references/github-issues.md` — Issue management
- `references/github-repo-management.md` — Repo management (clone, create, fork, releases, secrets, actions)
- `references/github-automation-patterns.md` — Automation scripts, clean JSON output, cron jobs, shell escaping
- `references/greybel-ci-pattern.md` — GreyHack/Greybel CI build verification patterns and pitfalls
- `references/greyhack-greybel-ci.md` — Session-specific GreyHack Greybel CI reference for `Toqsick/greyscripts`
- `references/documentation-health-audit.md` — Repo documentation audit: count verification, standalone dep check, thin READMES detection, category cross-reference (2026-06-25)
- `references/push-audit-research.md` — "Was wurde kürzlich gepusht?"-Recherche: `git ls-remote` als Ground Truth, MCP-401-Triangulation, `gh api`-Fallbacks, Diagnosetabellen für private/public Repos (2026-07-04)
- `references/batch-contributing-md-push-2026-07-07.md` — Session-Referenz: Batch-Push via Contents API über 4 Repos inkl. 409 stale-SHA-Pitfall, MD5-Verifikation, Domain-Template-Reusability-Lesson (2026-07-07)
- `references/mcp-github-quirks-batch-push-2026-07-07.md` — MCP-Tool-Antwort-Fallen: `create_or_update_file` "already exists"-Lügen, `get_file_contents`-Sentinel-SHA, "unreachable after 3 failures"-Cooldown; curl-Fallback mit `gh auth token`; 4-Repo-Contents-API-Push (2026-07-07)
- `references/ci-failure-diagnosis.md` — Session-Referenz: Read-only CI-Diagnose Issue #30 + #43 auf Toqsick/greyscripts (yamllint-Override-Mismatch als Root-Cause, stale issue-table Pfade via tree-API verifiziert, `needs:`-Skip-Chain, 1-Zeilen-Patch macht beides grün) (2026-07-07)