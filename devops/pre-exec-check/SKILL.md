---
name: pre-exec-check
description: >-
  Safety check before executing destructive or irreversible commands. Catches
  dangerous shell commands, risky git operations, secret exposure, and
  high-blast-radius actions before they run. Activates automatically when Claude
  is about to execute shell commands that match known risk patterns.
  Trigger phrases: "check before running", "is this command safe",
  "safety check", "pre-execution review".
user-invocable: false
allowed-tools: ""
---

# Pre-Execution Safety Check

Before executing any shell command, evaluate it against the risk categories below.
This check runs silently — only surface it to the user when a risk is detected.

## Risk Categories

### CRITICAL — Block and warn. Never proceed without explicit user confirmation.

**Destructive file operations:**
- `rm -rf` on any path outside a known temp/build directory
- `rm -rf /`, `rm -rf ~`, `rm -rf .` (catastrophic)
- Recursive delete on paths containing `..`
- `> filename` (truncating files) on non-build artifacts

**Irreversible git operations:**
- `git push --force` or `git push -f` to `main`, `master`, or `production`
- `git reset --hard` when there are uncommitted changes
- `git clean -fd` or `git clean -fdx` (deletes untracked files)
- `git branch -D` on branches with unmerged commits
- `git rebase` on already-pushed commits

**Database destruction:**
- `DROP TABLE`, `DROP DATABASE`, `TRUNCATE TABLE` without a WHERE or in production
- `DELETE FROM` without a WHERE clause
- Migration rollbacks in production

**Process/system operations:**
- `kill -9` on PIDs that aren't child processes of the current session
- `pkill` or `killall` on broad patterns
- `chmod -R 777` or `chmod -R 000`
- `chown -R` on system directories
- Writing to `/etc/`, `/usr/`, or other system paths

**Secret exposure:**
- `echo $API_KEY`, `cat .env`, `printenv` piped to files or network
- Any command that would print secrets to stdout in a logged session
- `curl` or `wget` with credentials in the URL

### HIGH — Warn user, explain the risk, suggest safer alternative.

**Risky git operations:**
- `git push --force` to any branch (suggest `--force-with-lease`)
- `git reset --hard` (suggest `git stash` first)
- `git checkout -- .` or `git restore .` (discards all changes)
- Amending commits that have been pushed

**Package management:**
- `npm publish` (publicly publishing a package)
- `pip install` from URL or `--extra-index-url` (supply chain risk)
- Removing lockfiles (`rm package-lock.json`, `rm poetry.lock`)

**Infrastructure:**
- `kubectl delete` on production namespaces
- `terraform destroy`
- `docker system prune -a` (removes all images)

**Network:**
- `curl -X POST` to external URLs with body containing local data
- `scp` or `rsync` to unfamiliar hosts
- `ssh` to production servers

### MEDIUM — Note the risk in passing. Proceed unless the context is unusual.

- Installing global packages (`npm install -g`, `pip install --user`)
- Running `sudo` commands
- Modifying dotfiles (`.bashrc`, `.zshrc`, `.gitconfig`)
- Creating world-readable files in shared directories

## Behavior

When a command matches a risk pattern:

1. **CRITICAL**: Stop. Tell the user: "This command [specific description] is destructive/irreversible. [Explain what could go wrong]. Do you want to proceed?"
2. **HIGH**: Warn: "Heads up — [command] carries risk because [reason]. Safer alternative: [suggestion]. Proceeding unless you object."
3. **MEDIUM**: Brief note only if the broader context makes it concerning.

When no risk is detected, proceed normally — do not mention this check.

## Anti-Patterns to Avoid

- Do NOT warn about every `rm` command. `rm file.txt` on a known temp file is fine.
- Do NOT block normal development workflows. `git push` to a feature branch is fine.
- Do NOT add friction to routine operations. The goal is catching genuine mistakes, not slowing down the user.
- Do NOT be paranoid about `curl` for fetching docs or APIs. Only flag when local data is being sent.

## Context Awareness

Use available context to reduce false positives:
- If in a git repo, check if the branch has been pushed before warning about force-push
- If a file was just created by the agent, deleting it is lower risk
- If running inside a Docker container or CI, destructive commands are lower risk
- `git status` output tells you if there are uncommitted changes worth protecting
