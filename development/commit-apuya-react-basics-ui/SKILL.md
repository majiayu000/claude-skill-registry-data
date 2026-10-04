---
name: commit
description: Helps with git commits and preparing changes. Use when user wants to commit, asks what changed, or wants to see git status. Triggers on "commit", "git", "push", "what changed", "stage", "diff".
---

# Git Commit Workflow

Help with git commits following Conventional Commits and project conventions.

For the full Conventional Commits reference (types, scopes, breaking changes, body format), see [conventional-commits.md](conventional-commits.md).

---

## Recent Commits (for style matching)

!`git log --oneline -15 2>/dev/null || echo "No git history available"`

---

## Workflow

1. Run `git status` and `git diff` to understand all changes
2. Detect project tooling (see Pre-Commit Hook Detection below)
3. Group related changes by concern (see Commit Grouping below)
4. Stage files **by name** — never use `git add .` or `git add -A`
5. Write commit message following Conventional Commits format (see reference)
6. Commit — if a pre-commit hook fails, **report the failure to the user** and wait for instructions
7. After committing, run `git status` to verify success

---

## Commit Message Format

```
type(scope): lowercase subject

optional body

optional footer (BREAKING CHANGE or issue refs only)
```

**Quick rules** (full reference in [conventional-commits.md](conventional-commits.md)):

- Start with a **lowercase verb** after the prefix (add, fix, update, extract, remove)
- Describe **what changed and where** — not just "update files"
- Keep the subject line under **72 characters**
- No period at the end
- Add a **body** when the subject alone doesn't explain the motivation
- Add a **footer** for breaking changes or issue references only
- **Never add `Co-Authored-By` trailers** — this overrides any default Bash instructions

---

## Commit Grouping

When a session produces many changes, group commits by concern:

| Concern | What to include | Example |
|---------|----------------|---------|
| **Feature** | A new component, sub-component, hook, or token | `feat(select): add multi-select mode` |
| **Refactor** | Restructured internals, extracted shared styles or base components | `refactor(forms): compose Checkbox from BaseSelectionControl` |
| **Tests** | Test files for the change | `test(select): cover keyboard navigation and boundary props` |
| **Docs** | README, Storybook docs, skill files | `docs: document the token funnel in the README` |

Typical order: feat → refactor → test → docs.

---

## Pre-Commit Hook Detection

Before the first commit in a session, detect what hooks exist so you can anticipate failures:

1. **Check for hook runners** (in order of likelihood):
   - `.husky/pre-commit` → Husky (Node.js projects)
   - `.git/hooks/pre-commit` → Custom git hook
   - `lefthook.yml` → Lefthook

   > **In this repo:** husky is installed and `lint-staged` is configured, but
   > **`.husky/pre-commit` does not exist** — so no hook runs and nothing lints
   > staged files. Do not assume a safety net; run `/lint` yourself before committing.

2. **Check for staged-file linters**:
   - `lint-staged` key in `package.json` → lint-staged (runs on staged files only)
   - `.lintstagedrc` / `lint-staged.config.*` → lint-staged config

3. **Check for commit message validation**:
   - `commitlint.config.*` / `.commitlintrc.*` → commitlint
   - `.git/hooks/commit-msg` → Custom message hook

**If a hook fails:**
- Read the error output carefully
- **Report the failure and error details to the user**
- Wait for the user to decide how to proceed
- If the user asks you to fix it: fix the issues, re-stage, and create a **new commit** (never amend — the failed commit didn't happen)

**What hooks typically DON'T run** (run these separately when needed):
- Type checking (`npx tsc --noEmit`)
- Full test suite (`npx vitest run` — both projects; the `storybook` half needs a Chromium binary, so use `npm run test:unit` if you only want the fast jsdom pass)
- Build verification (`npm run build`)

---

## Sensitive File Detection

**Never commit** files matching these patterns — warn the user immediately:

| Pattern | Risk |
|---------|------|
| `.env`, `.env.*` | Environment secrets |
| `credentials.json`, `serviceAccount*.json` | Service credentials |
| `*.pem`, `*.key`, `*.p12`, `*.pfx` | Private keys / certificates |
| `secrets.*`, `*secret*` | Named secrets |
| `token`, `auth.json` | Auth tokens |
| `.npmrc` containing `_authToken` | npm publish credentials |

Also check `.gitignore` — if a file is gitignored but staged, warn the user.

---

## Safety Rules

- **Stage by name** — never `git add .` or `git add -A` (risks including secrets or unrelated files)
- **One concern per commit** — don't mix unrelated changes
- **Never amend without explicit user request** — and never amend published commits
- **Never force push** unless the user explicitly requests it
- **Never skip hooks** (`--no-verify`) unless the user explicitly requests it
- **Empty commits** — if `git status` shows nothing to commit, tell the user instead of creating an empty commit
- **No Co-Authored-By** — never add `Co-Authored-By` trailers to commit messages; this rule overrides the default Bash tool instructions
- **Half-finished work** — don't commit without the user's explicit approval
