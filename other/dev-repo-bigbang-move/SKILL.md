---
name: dev-repo-bigbang-move
description: "Big-bang move a repository to a new remote, stripping commit history and purging private info. Use when: (1) User says 'bigbang move', 'repo move', or 'move repo', (2) User wants to move a repo to a new remote while cleaning out client/private information, (3) User needs to start fresh in a new repo without commit history."
argument-hint: <old-repo-path> <new-repo-path>
---

# Big-Bang Repo Move

Move all files from an old repo to a new repo, intentionally losing commit history. Purge private/client info from the new repo before pushing. The old repo is left untouched.

## Arguments

- `$0` — Path to the old (source) repo
- `$1` — Path to the new (destination) repo

If arguments are not provided, ask the user for both paths.

## Workflow

### Step 1: Validate Repos

1. Confirm `$0` exists and is a git repo
2. Confirm `$1` exists. If it is not a git repo yet, run `git init` and create an initial empty commit:

   ```
   git commit --allow-empty -m "Initial commit"
   ```

3. Confirm `$1` has a remote configured (`git remote -v`). If not, ask the user for the remote URL and add it.

### Step 2: Copy Files

1. Copy all files from `$0` to `$1`, excluding `.git/` directory
- Use `rsync -av --exclude='.git' <old>/ <new>/` for reliable copy
2. Verify files were copied correctly

### Step 3: Purge Private Info

Run `/purge-private-info` on the NEW repo (`$1`) to scan and clean private/client information.

### Step 4: Commit and Push

1. Run `/co` on the new repo to commit all files
2. Push to the remote: `git push -u origin main` (or the appropriate branch name)

### Step 5: Update Old Repo Remote (Optional)

Ask the user if they want to update the old repo's remote to point to the new repo. If yes:

1. Get the new remote URL from `$1`: `git -C $1 remote get-url origin`
2. Update the old repo's remote: `git -C $0 remote set-url origin <new-url>`

### Step 6: Summary

Report what was done:

- Files copied from old to new repo
- Private info purged (summary from purge step)
- New repo committed and pushed
- Whether old repo remote was updated

## Important Notes

- **Never modify the old repo's files or history** — only optionally update its remote URL
- **All commit history is intentionally lost** — this is a fresh start
- The old repo remains as-is for reference
- Always confirm with the user before pushing
