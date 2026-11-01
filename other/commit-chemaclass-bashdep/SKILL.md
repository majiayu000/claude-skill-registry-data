---
name: commit
description: Stage and commit changes using conventional commits format
user-invocable: true
argument-hint: "[message hint]"
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob
---

# Commit with Conventional Commits

Stage and commit current changes using the conventional commits format.

> **IMPORTANT:** This skill MUST be used for ALL commits - even when the
> user just says "commit" without `/commit`. Never commit without
> following these steps.

## Current State
- Branch: !`git branch --show-current`
- Status: !`git status --short`
- Staged diff: !`git diff --cached --stat 2>/dev/null`
- Unstaged diff: !`git diff --stat 2>/dev/null`
- Recent commits: !`git log --oneline -5 2>/dev/null`

## Arguments
- `$ARGUMENTS` - Optional hint for the commit message
  (e.g., `clean orphan files race`)

## Instructions

1. **Review the state above** - understand what changed and why.

2. **Stage files** - add only the relevant changed files by name. Never
    use `git add -A` or `git add .`. Never stage files that contain
    secrets (`.env`, credentials, `lib/` artifacts, `local/`, `tmp/`).

3. **Determine the commit type** from the nature of the changes:
    - `feat` - new feature or capability
    - `fix` - bug fix
    - `docs` - documentation only
    - `style` - formatting, whitespace (no logic change)
    - `refactor` - code restructuring (no behavior change)
    - `test` - adding or updating tests
    - `chore` - maintenance, tooling, config
    - `perf` - performance improvement
    - `ci` - CI/CD config (`.github/workflows/`)

4. **Determine the scope** from the area of the codebase affected:
    - `install` - `bashdep::install` / `install_from`
    - `lock` - lockfile read/write helpers
    - `doctor` - `bashdep::doctor`
    - `clean` - `bashdep::clean`
    - `uninstall` - `bashdep::uninstall`
    - `setup` - `bashdep::setup`
    - `cli` - CLI dispatch / flags
    - `release` - `release.sh` and release tooling
    - `docs` - `docs/`, `README.md`
    - `ci` - `.github/workflows/`
    - Use the most specific scope that fits. Omit if changes span many areas.

5. **Write the commit message**:
    - Format: `<type>(<scope>): <description>`
    - Description: imperative mood, lowercase, no period, under 70 chars
    - Focus on **why**, not what
    - Add a body (separated by blank line) only when the why isn't
      obvious from the description
    - **Never mention AI, Claude, or automation** in the message
    - **Never** add a `Co-Authored-By` trailer (repo
      `settings.json` sets `includeCoAuthoredBy: false`)

6. **Create the commit**:
    ```bash
    git commit -m "$(cat <<'EOF'
    <type>(<scope>): <description>

    <optional body>
    EOF
    )"
    ```

7. **Verify** the commit was created:
    ```bash
    git log --oneline -1
    ```

## Examples

```
feat(doctor): report orphan files in dev dir
fix(lock): preserve trailing newline on lockfile rewrite
test(clean): cover dry-run output for orphan removal
refactor(install): extract _classify_dep helper
docs(api): document bashdep::self_update target_path arg
chore(ci): bump shellcheck to v0.10
perf(install): skip re-download when lock + file are in sync
```

## Rules

- **One logical change per commit** - don't mix unrelated changes
- **Never use `--no-verify`** - if hooks fail, fix the underlying issue
- **Never amend** unless the user explicitly asks
- **Always create a NEW commit** - even after a hook failure
- **Author**: use the git config identity (never commit as default user)
