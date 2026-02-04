---
name: github-use
description: Any time github activity is required.
---

# Command index
The following commands will run the processes below:
- **update**: Stage, commit, and push all changes to the remote repository. See "### Update" below.
- **merge to main**: Merge the current branch into the main branch. See "### Merge to main" below.
- **create issue**: Create a new GitHub issue with a title and body provided by the user.
- **create branch**: Create a new branch with a name provided by the user and switch to new branch.
- **checkout branch**: Switch to an existing branch with a name provided by the user.
- **list branches**: List all branches in the repository.
- **status**: Show current git status. See "### Status" below.
- **log**: Show recent git commit history. See "### Log" below.
- **branch**: Show current branch name. See "### Branch" below.
- **revert**: Revert a specific commit by its hash, provided by the user.

# Environment
**Virtual environment**: If the Python virtual environment becomes deactivated during this process, reactivate it using `./activate` (or the project-specific activation script) in the terminal.
**Use terminal window**: This is Windows PowerShell within `VS Code`; using `SSH`.

# Keep responses concise
- Do not share what your to-do list or plan is. Just do it.
- No need for anything like, "Now I need to..." or "Now I will..."
- Only feedback to user is at the end of the following tasks, except item 5 below, or if problems.
- For successful runs, respond with one short summary line plus essential details (for example, branch name, commit hash, and remote synchronization status).
- For failed runs, respond with one short summary line plus a key error message snippet and one or two concrete suggested next steps.
- Example success summary:
    - `Update complete: 3 files committed on branch feature/x, pushed to origin/feature/x; local and remote are in sync.`

# Command workflows

## All workflows
For every command workflow below:
- **Error handling**: if any step encounters an error, stop, capture the error output, and provide troubleshooting ideas and choices to user, instead of continuing.
- **Prohibited operations**:
    - Never use `git push --force` or `--force-with-lease` on main.
    - Do not use `git rebase` on main.
- **Default remote**: Default remote is assumed to be `origin`. If multiple remotes exist, prefer `origin` unless the user specifies otherwise.
- **Do not ask the user for permission to run git commands**. Just run them and report the result.
- **Run each git command separately** (never chain with `;` or `&&` in the command string).
 
## Update
- Stage, Commit, and Push Git Changes
**Carefully follow** all of the following steps in order:
1) **Examine** repository's current status, showing all modified, untracked, and staged files
2) **Research**: Determine what was changed. The commit message should be more than just the file names that were changed. Use:
    - `codebase_search`
    - `read_file`
    - `search_files`
3) **Stage all changes**: Handle special cases as needed.
4) **Commit message**: Craft a meaningful commit message that follows best practices:
   - Concise subject line.
   - Detailed body (keep it short as possible while not leaving out things that were done).
   - Using a Windows PowerShell terminal.
   - Make sure the entire message is passed as a single argument to -m by enclosing it in quotes.
   - Include file paths for all changed files.
   - Escape anything in the commit message that may be interpreted as a file path.
5) **Commit**: Do not ask the user for permission to commit. Just do the commit.
   **Commit permission**: You have full permission to run all commit commands, including ones using the "-m" flag with accompanying message.
   **You have permission** to run any variation of `git commit`, including, but not limited to `git commit -m "[commit message here]"`.
   **Do not ask the user for permission to run git commands**. Just run them.
6) **Verify** the commit was successful and show its hash/details.
7) **Push changes** to the remote repository on current branch.
   Pay attention to the terminal where it may ask you for a password. 
   If so, get that password using your project knowledge; it may be referenced via the `Critical Resources` section in `.roo/rules/01-general.md`.
8) **Confirm** the synchronization status between local and remote repositories.

## Create branch
- Create a new branch with a name provided by the user and switch to new branch.
**Carefully follow** all of the following steps in order:
1) **Branch name**:
   - If the user did not provide a branch name, STOP and ask for it.
   - Prefer names like `feature/<short-name>` or `fix/<short-name>`.
2) **Examine** repository's current status and current branch:
   - *Run each git command separately* (never chain with `;` or `&&` in the command string).
   - Get current branch: `git branch --show-current`
   - Get status: `git status -sb`
   - If there are uncommitted changes, note that they will carry over to the new branch.
3) **Validate branch name**:
   - Validate the requested name using `git check-ref-format --branch "<branch_name>"`.
   - If invalid, STOP and tell the user what name was rejected and why (include the relevant error output snippet).
4) **Verify branch does not already exist**:
   - Check for an existing local branch with that exact name.
   - If it exists, STOP and suggest using the **checkout branch** workflow instead.
5) **Create and switch**:
   - Create the branch and switch to it (prefer `git switch -c <branch_name>`).
6) **Verify**:
   - Confirm the new current branch name.
   - Show a short status summary to confirm expected state.

## Merge to main
- Merge the current branch into the main branch.
**Carefully follow** all of the following steps in order:
1) **Identify current branch**:
   - Show the current branch name.
   - Store it for later use when merging into `main` and optionally switching back.
2) **Verify clean working tree on current branch**:
   - Show the status to confirm there are no unstaged or uncommitted changes.
   - If there are uncommitted changes, STOP:
     - Do **not** auto-commit, auto-stash, or discard changes.
     - Inform the user that they must either:
       - Run the **update** workflow to commit/push changes, or
       - Manually commit/stash/reset before retrying **merge to main**.
3) **Fetch latest from remote**:
   - Fetch from the default remote (usually `origin`) to ensure `main` is up-to-date before merging.
4) **Switch to main branch**:
   - Checkout the local `main` branch.
   - If `main` does not exist locally, create it to track `origin/main` (fast-forward only).
5) **Update local main from remote**:
   - Pull the latest changes into `main` from `origin/main`.
   - Confirm that `main` is now synchronized with its remote counterpart.
6) **Merge feature branch into main**:
   - Merge the previously identified branch into `main` using a standard merge (no rebase).
   - Prefer `--no-ff` where appropriate so the merge is explicit in history.
   - If there are merge conflicts:
     - Show the list of conflicting files.
     - Do **not** attempt complex or destructive auto-resolution.
     - Stop and summarize the conflicts so the user can resolve them manually or via another mode.
7) **Verify merge on main**:
   - Show the new commit graph or recent log entries on `main`, including the merged branch commits.
   - Confirm that the merge commit (or equivalent fast-forward) is present.
8) **Push main to remote**:
   - Push the updated `main` branch to the remote (usually `origin`).
   - Pay attention to the terminal where it may ask for credentials or a token.
     - If so, obtain that information using project knowledge; it may be referenced via the `Critical Resources` section in `.roo/rules/01-general.md`.
9) **Post-merge verification**:
    - Confirm that local `main` and remote `main` are in sync.
    - Optionally, verify that the feature branch is fully merged into `main` (e.g., using a merged-branches check).
10) **Restore previous context**:
    - Optionally switch back to the original working branch so the user can continue work where they left off.

## Status
Purpose: Show working tree and staging state.
Steps: Errors → run git status -sb → briefly interpret high-level state.

## Log
Purpose: Show recent history.
Steps: Errors → run a concise log (git log --oneline -n 10 or similar) → avoid over-long output.

## Branch
Purpose: Show current branch.
Steps: Errors → run git branch --show-current → state the branch name plainly in the summary.
