---
name: commit
category: release-management
model: claude-haiku-5-5
userInvocable: true
description: Stage and commit changes with a conventional commit message. Runs pre-commit checks automatically. Optionally prefixes with a ticket number.
argument-hint: "[ticket-number]"
allowed-tools: "Bash(cat:*), Bash(echo:*), Bash(grep:*), Bash(git commit:*), Bash(git add:*), Bash(git reset:*), Bash(git status:*), Bash(git diff:*), Bash(git checkout:*), Bash(git branch:*), Bash(git log:*), Bash(./vendor/bin/php-cs-fixer:*), Bash(php-cs-fixer:*), Bash(test:*), Bash(which:*), AskUserQuestion"
---

# Git Commit Command

## Context

Recent commits for reference: !`git log --oneline -5 2>/dev/null || echo "No previous commits (this will be the first commit)"`

Current branch: !`git branch --show-current 2>/dev/null || echo "(not in a git repository)"`

## Your Task

Run everything inline — no agent delegation. The `git-mutation-guard.sh` PreToolUse hook runs the credential scan on staged files automatically at commit time; you do not need to scan separately.

### 1. Determine Ticket Number

Priority order (argument: $ARGUMENTS):

1. **From argument**: If provided, validate against `[A-Z]+-[0-9]+`.
2. **From branch name**: Extract with:
   ```bash
   branch=$(git branch --show-current)
   ticket=$(echo "$branch" | grep -oE '[A-Z]+-[0-9]+' | head -1)
   ```
3. **None**: Only if the branch has no ticket pattern.

The ticket MUST appear in the commit message as `[TICKET-123]` (brackets, original casing).

### 2. Check Branch Safety

If on `main` or `master`, create a feature branch before committing:

```bash
git checkout -b feature/[ticket]-description
```

### 3. Run PHP CS Fixer (if available)

```bash
test -f ./vendor/bin/php-cs-fixer && ./vendor/bin/php-cs-fixer fix --dry-run --diff <modified-php-files>
```

Skip silently if not available or no PHP files modified.

### 4. Review Changes and Stage

Use compact flags — never plain `git status` / `git diff`:

```bash
git status --short
git diff --stat HEAD
```

Identify files to stage, excluding `.env*`, `credentials.*`, `*.pem`, `*.key`. For files whose content you need to understand for the commit message, fetch the full patch per-file:

```bash
git diff HEAD -- <file>
```

Stage explicitly:

```bash
git add <file1> <file2> ...
```

### 5. Author Commit Message

Format:

```
[TICKET-123] type(scope): short description

Optional body wrapped at 72 chars explaining the WHY.
```

Types: `feat` | `fix` | `refactor` | `test` | `docs` | `chore` | `style` | `perf`

Rules:
- Imperative mood, subject line ≤ 50 chars
- NO `Co-Authored-By`, NO `Generated with Claude Code`, NO AI attribution
- One logical change per commit — if tempted to use "and", split it

### 6. Commit

```bash
git commit -m "$(cat <<'EOF'
[TICKET-123] type(scope): short description

Optional body.
EOF
)"
```

**If the hook blocks the commit due to a credential-scan finding:** surface the finding to the user verbatim (file:line — label, never the secret value). Ask whether it is a true leak or false positive. On confirmed false positive, re-run with `CREDENTIAL_SCAN_BYPASS=1 git commit …` and include the reason in the commit body so the override is traceable. Never override silently.

That prefix skips **this scan only**. Branch protection and the security-auditor state check still apply, and the skip is announced on stderr. It also applies per repository and fail-closed: if any other commit in the same command targets the same repository without the prefix, the scan runs anyway.

### 7. Report Results

Show:
- Commit hash (from `git log -1 --format='%h'`)
- Commit message subject line
- File count (from `git show --stat HEAD`)

## Important Notes

- **Single message execution** — complete all steps in one response.
- **Branch safety** — never commit directly to main/master.
- **Clean messages** — no AI attribution or footers.
- **Do NOT push** — user will push manually (the push hook requires a security-auditor confirmation).
