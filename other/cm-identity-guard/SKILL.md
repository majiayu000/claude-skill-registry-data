---
name: cm-identity-guard
description: Verify and lock project identity before ANY git push, Cloudflare deploy, or Supabase operation. Essential when working with multiple GitHub accounts (personal + work), multiple Cloudflare accounts, or multiple Supabase/Neon projects. Prevents wrong-account deploys, cross-project secret leaks, and git history contamination.
token_budget: 800
compressed: true
deprecated: false
---

# Identity Guard — Multi-Account Safety Protocol

## TL;DR
- **Use before** any git push, Cloudflare deploy, or Supabase op
- **Verifies**: GitHub account, CF account, Supabase project match expected
- **Prevents**: wrong-account deploys, cross-project secret leaks

## Overview

Working across multiple projects, clients, and platforms means one wrong `git push` or `wrangler deploy` can publish work to the wrong account. This skill establishes a mandatory identity check before any operation that touches external services.

> [!CAUTION]
> **Real incidents this skill prevents:**
> - Pushed client code to personal GitHub repo
> - Deployed to wrong Cloudflare account (different org's Pages project, billing confusion)
> - Used personal Supabase `ANON_KEY` in a client project (wrong DB entirely)
> - `git config user.email` was personal email → commits show wrong author in client repo

## The Iron Law

```
NEVER push, deploy, or use secrets WITHOUT verifying identity first.
ASK: Which account? Which project? Which database?
ONE command verifies all three. Run it. Always.
```

## When to Use

**ALWAYS** before:
- `git push` or `git commit` in a project with multiple account contexts
- `wrangler pages deploy` or any Cloudflare operation
- Creating or accessing a Supabase/Neon client
- Setting up a new project from scratch
- Resuming work after switching between personal and work projects

---

## Account Registry (Your Known Accounts)

Maintain this table in your head (or in `.project-identity.json`):

### GitHub Accounts

| Account | Purpose | Email | When to Use |
|---------|---------|-------|-------------|
| `my-personal` | Personal projects, experiments | personal email | Personal repos, side projects |
| `my-work-org` | Client work | `dev@workdomain.com` | All client projects |

### Cloudflare Accounts

| Account ID | Purpose | Projects |
|-----------|---------|---------|
| `abc123def456ghi789jkl012mno345pqr` | Client A / Org | project-1, project-2, app |
| (personal) | Personal experiments | personal side projects |

### Database Accounts

| Service | Account | Purpose |
|---------|---------|---------|
| Supabase (Org) | org account | All Client A apps |
| Supabase (personal) | personal account | Experiments |
| Neon | per project | If used |

---

## Phase 0: Project Identity File

Every project MUST have a `.project-identity.json` in the project root:

```json
{
  "name": "my-awesome-project",
  "description": "An awesome internal tool",
  "github": {
    "account": "my-work-org",
    "org": "my-work-org",
    "repo": "my_project_repo",
    "remoteUrl": "https://github.com/my-work-org/my_project_repo.git",
    "userEmail": "dev@workdomain.com"
  },
  "cloudflare": {
    "accountId": "abc123def456ghi789jkl012mno345pqr",
    "projectName": "my-frontend-app",
    "stagingUrl": "https://my-app-staging.pages.dev",
    "productionUrl": "https://myapp.workdomain.com",
    "productionBranch": "production"
  },
  "database": {
    "provider": "supabase",
    "projectName": "my-database-project",
    "urlVar": "SUPABASE_URL",
    "anonKeyVar": "SUPABASE_ANON_KEY",
    "serviceKeyVar": "SUPABASE_SERVICE_KEY",
    "secretsStore": "cloudflare-secrets"
  },
  "i18n": {
    "primary": "vi",
    "languages": ["vi", "en", "th", "ph"],
    "dir": "public/static/i18n"
  }
}
```

> [!IMPORTANT]
> Add `.project-identity.json` to git but NEVER put actual secrets in it — only variable NAMES and account IDs. Secrets live in `.dev.vars` (local) or Cloudflare Secrets (production).

---

## Phase 1: Identity Verification

### The One-Liner Check

Run this before any push or deploy:

```bash
# Full identity check — GitHub + Git user + CF account + DB config
echo "=== GitHub CLI ===" && gh auth status 2>&1 | grep -E "Logged in|github.com" && \
echo "=== Git Remote ===" && git remote get-url origin && \
echo "=== Git User ===" && git config user.name && git config user.email && \
echo "=== Cloudflare ===" && cat wrangler.jsonc | grep -E "account_id|project|name" | head -5 && \
echo "=== DB Config ===" && cat .dev.vars 2>/dev/null | grep -E "URL|SUPABASE" | sed 's/=.*/=***/' && \
echo "=== Expected ===" && cat .project-identity.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('GitHub:', d['github']['account'], '| CF:', d['cloudflare']['accountId'][:8]+'...', '| DB:', d['database']['provider'])"
```

### What to Verify (Checklist)

```
☐ GitHub CLI: logged in as <EXPECTED ACCOUNT>
☐ git remote origin: points to <EXPECTED REPO URL>
☐ git config user.email: matches <EXPECTED EMAIL>
☐ wrangler.jsonc: account_id matches <EXPECTED CF ACCOUNT ID>
☐ .dev.vars: SUPABASE_URL points to <EXPECTED SUPABASE PROJECT>
```

---

## Phase 2: Fix Wrong Identity

### Wrong GitHub Account

```bash
# Check current
gh auth status

# Switch to work account
gh auth logout
gh auth login
# → Login with web browser → select my-work-org

# Fix git user for THIS repo (not global)
git config user.name "my-work-org"
git config user.email "dev@workdomain.com"

# Fix remote URL
git remote set-url origin https://github.com/my-work-org/REPO_NAME.git
```

### Wrong Cloudflare Account

```bash
# Check current CF account
wrangler whoami

# Look for account_id in wrangler.jsonc
grep account_id wrangler.jsonc

# Expected for Your Project: abc123def456ghi789jkl012mno345pqr
# Fix: update account_id in wrangler.jsonc
```

### Wrong Supabase Project

```bash
# Check which Supabase URL is in .dev.vars
grep SUPABASE_URL .dev.vars

# The URL pattern reveals the project: https://<PROJECT_ID>.supabase.co
# Compare with the project in .project-identity.json

# Fix: update .dev.vars with correct values
# Then restart wrangler dev
```

### Wrong git author on recent commits

```bash
# See who authored the last few commits
git log --format="%h %an <%ae>" -5

# If wrong — amend last commit's author (before push only!)
git commit --amend --author="my-work-org <dev@workdomain.com>" --no-edit

# For multiple commits: rebase and re-author
git rebase -i HEAD~N  # Then for each commit: edit → amend author → continue
```

---

## Phase 3: Project Setup (New Projects)

When starting a new project, answer these questions FIRST:

```markdown
Before writing any code or creating any repo, I need to lock identity:

1. **GitHub account**: Personal (my-personal) or Work (my-work-org)?
2. **Cloudflare account**: Which account ID?
3. **Database**: Which Supabase org? New project or existing?
4. **Languages**: Single locale or multi-language from day 1?
   → If multi-language: list all target languages now
```

Then create `.project-identity.json` BEFORE the first commit:

```bash
# Lock git identity to this project immediately
git config user.name "my-work-org"
git config user.email "dev@workdomain.com"
git remote set-url origin https://github.com/my-work-org/NEW_REPO.git

# Verify before first push
git config user.email  # Must match expected
git remote get-url origin  # Must match expected
gh auth status  # Must show correct account
```

---

## Phase 4: Multi-Account Git Setup (OS Level)

### Using SSH Keys per Account

```bash
# Generate separate keys for each account
ssh-keygen -t ed25519 -C "dev@workdomain.com" -f ~/.ssh/id_my_work_org
ssh-keygen -t ed25519 -C "personal@..." -f ~/.ssh/id_personal

# ~/.ssh/config — route by host alias
Host github-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_my_work_org

Host github-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_personal
```

### Using SSH, reference by alias in project:

```bash
# For work projects:
git remote set-url origin git@github-work:my-work-org/REPO.git

# For personal projects:
git remote set-url origin git@github-personal:my-personal/REPO.git
```

### Global vs Local git config

```bash
# Global: personal (default for new repos)
git config --global user.name "my-personal"
git config --global user.email "personal@email.com"

# Per-repo override for work projects (run inside each work repo):
git config user.name "my-work-org"
git config user.email "dev@workdomain.com"
```

> [!TIP]
> Use `includeIf` in `~/.gitconfig` to auto-apply work identity for repos in specific directories:
> ```ini
> [includeIf "gitdir:~/Builder/ClientA/"]
>     path = ~/.gitconfig-work
> ```
> `~/.gitconfig-work`:
> ```ini
> [user]
>     name = my-work-org
>     email = dev@workdomain.com
> ```

---

## Phase 5: Token Lifecycle Management 🔄

> **NEW — Secrets don't just need to be hidden. They need to be ROTATED.**
> **Full rotation playbooks now live in `cm-safe-deploy`.**

### Rotation Schedule

| Platform | Token Type | Max Lifetime | Where to Rotate |
|----------|-----------|-------------|----------------|
| **Supabase** | `anon_key` | 90 days | Dashboard → Settings → API |
| **Supabase** | `service_role_key` | 30 days | Dashboard → Settings → API |
| **Cloudflare** | API Token | 90 days | Dashboard → My Profile → API Tokens |
| **GitHub** | Personal Access Token | 90 days | Settings → Developer Settings → PAT |
| **OpenAI/Gemini** | API Key | 90 days | Platform dashboard |

### After Rotation

```bash
# 1. Update Cloudflare Secrets with new values
wrangler secret put SUPABASE_ANON_KEY
wrangler secret put SUPABASE_SERVICE_KEY

# 2. Update local .dev.vars
# 3. Redeploy
npm run deploy:staging

# 4. Verify: test staging URL
```

> For emergency rotation (leaked secret), see the emergency rotation guidance in `cm-safe-deploy`.

---

## Red Flags — Identity Confusion

```
❌ git push and see "Repository not found" or "Permission denied"
   → Wrong account. Run identity check.

❌ wrangler deploy succeeded but can't find it in your CF dashboard
   → Deployed to wrong CF account. Check wrangler.jsonc account_id.

❌ Authentication fails with correct password
   → `gh auth status` shows wrong account. Logout and login to correct one.

❌ Production app shows the wrong data / can't connect to DB
   → Wrong SUPABASE_URL or key. Check Cloudflare Secrets for the project.

❌ git log shows wrong author email on commits
   → git config user.email is wrong. Fix and amend before pushing.

❌ New repo was created under wrong GitHub org
   → Delete and recreate under correct org, then update remote URL.
```

---

## Recovery Playbook

### "I pushed to the wrong GitHub repo"

```bash
# 1. Delete the push (if repo is private, remove sensitive data)
git push origin --delete <branch>  # Remove the branch

# 2. If sensitive data was exposed: contact GitHub support immediately
#    Also rotate any secrets that appeared in the code

# 3. Push to the correct repo:
git remote set-url origin https://github.com/CORRECT_ORG/CORRECT_REPO.git
git push origin <branch>
```

### "I deployed to the wrong Cloudflare account"

```bash
# 1. Log into correct CF account
# 2. Deploy immediately to overwrite:
CLOUDFLARE_ACCOUNT_ID=<CORRECT_ID> wrangler pages deploy dist --project-name <CORRECT_PROJECT>

# 3. Go to WRONG account's CF dashboard and delete the project or rollback deployment
```

### "I used wrong Supabase keys in production"

```bash
# 1. Update Cloudflare Secrets with correct values:
wrangler secret put SUPABASE_URL           # Enter correct URL
wrangler secret put SUPABASE_SERVICE_KEY   # Enter correct key
wrangler secret put SUPABASE_ANON_KEY      # Enter correct key

# 2. Redeploy to pick up new secrets
npm run deploy

# 3. Rotate the accidentally exposed keys in Supabase dashboard
```

---

## Integration with Other Skills

| Skill | When |
|-------|------|
| `cm-project-bootstrap` | Identity lock is Phase 0 of every new project |
| `cm-safe-deploy` | Gate 0 secret hygiene checks wrangler.jsonc |
| `cm-quality-gate` | Phase 4 verification and secret hygiene checks |
| `cm-safe-deploy` | Token lifecycle and release safety extend identity management |

## The Bottom Line

**One `.project-identity.json`. One verification command. Every push, every deploy.**

Wrong account = wasted time, broken deployments, exposed client code. The check takes 3 seconds.

This is non-negotiable.
