---
name: sync-force-to
description: "Force-sync current branch into a remote target branch by deleting and re-pushing. Creates a backup PR before overwriting so the old state can be restored via GitHub's 'Restore branch'. Use when 'sync-to' failed due to conflicts, or when user says 'sync force to', 'force sync to', 'force push to branch'."
argument-hint: <target-branch> | --setup
allowed-tools: Bash(bash *), Glob, Grep, Read, Edit
---

> **DO NOT auto-invoke this skill.** This destructively overwrites a remote branch. Always ask for user confirmation before proceeding.

# sync-force-to

Overwrite a remote target branch with the current branch by deleting the remote target and re-pushing. Avoids `git push --force` by using delete + push instead.

Before overwriting, the script automatically:

1. Pushes the old target state as a `backup/YYYYMMDDHHMM-<target>` branch
2. Creates a PR for the backup branch against the default branch
3. Closes the PR and deletes the backup branch
4. The closed PR retains GitHub's "Restore branch" button for recovery

If the target branch doesn't exist yet (first-time push), backup steps are skipped.

## Usage

### Normal mode

Run the bundled script:

```bash
bash $HOME/.claude/skills/sync-force-to/scripts/sync-force-to.sh $ARGUMENTS
```

Report the script output to the user verbatim. Do not add extra commentary unless there was an error.

### Setup mode (`--setup`)

When `$ARGUMENTS` is `--setup`, do NOT run the script. Instead, configure the current project's GitHub Actions workflows to skip CI on `backup/*` branches:

1. Find all workflow files: `.github/workflows/*.yml` and `.github/workflows/*.yaml`
2. For each workflow file, check `on:` triggers (`push`, `pull_request`, etc.)
3. For each trigger that could run on `backup/**` branches:
- If the trigger has a `branches:` filter that already excludes `backup/**`, skip it
- If the trigger has a `branches:` filter, add `'!backup/**'` to the list to exclude it
- If the trigger has NO branch filter (runs on all branches), add `branches-ignore: ['backup/**']`
- If the trigger already has `branches-ignore:`, add `'backup/**'` to the existing list
4. Report what files were changed

Important notes for setup:

- Do not modify triggers for `workflow_dispatch`, `schedule`, or other non-branch triggers
- Only modify `push` and `pull_request` / `pull_request_target` triggers
- Preserve existing YAML formatting and comments as much as possible
- Show the user the diff of changes before committing
