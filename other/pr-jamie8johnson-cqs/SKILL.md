---
name: pr
description: Create a pull request with WSL-safe workflow. Uses --body-file to avoid heredoc permission corruption.
disable-model-invocation: true
argument-hint: "[branch-name]"
---

# Create Pull Request

Create a PR from the current branch using WSL-safe patterns.

## Process

1. **Check state**:
   - `git status` — note any uncommitted changes
   - `git log main..HEAD` — review commits to include
   - `git diff main...HEAD --stat` — files changed

2. **Prepare**:
   - If uncommitted changes exist, ask user whether to commit first
   - Push the branch directly from WSL: `git push -u origin BRANCH` (the Windows credential manager is wired into WSL git). Fallback ONLY if GCM crashes ("could not read Username"): `powershell.exe -Command 'cd C:\Projects\cqs; git push -u origin BRANCH'`

3. **Write PR body** to `/mnt/c/Projects/cqs/pr_body.md`:
   ```markdown
   ## Summary
   - Bullet points summarizing changes

   ## Test plan
   - [ ] cargo test passes
   - [ ] cargo clippy clean
   - [ ] Manual verification steps
   ```

4. **Create PR** via PowerShell:
   ```
   powershell.exe -Command 'cd C:\Projects\cqs; gh pr create --title "..." --body-file pr_body.md'
   ```

5. **Clean up**: Delete `pr_body.md`

6. **Wait for CI — pin the run ID** (`gh pr checks --watch` latches onto the previous commit's completed run after a push; do not use it):
   ```
   sleep 45   # new run needs ~45s to register after the push
   powershell.exe -Command 'cd C:\Projects\cqs; gh run list --branch BRANCH --workflow CI --limit 1'
   powershell.exe -Command 'cd C:\Projects\cqs; gh run watch RUN_ID --exit-status'
   ```

7. **Report**: Show PR URL

## Critical rules

- **ALWAYS use `--body-file`** — never inline heredocs in `gh pr create --body`
- Heredocs get captured as permission entries in `settings.local.json`, corrupting startup
- `git push` works directly from WSL (credential helper wired); PowerShell is the fallback when GCM crashes. All `gh` commands still go through PowerShell (with `cd C:\Projects\cqs` or `-R jamie8johnson/cqs`)
- main is protected — all changes require PR
