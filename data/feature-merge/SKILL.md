---
name: feature-merge
description: Merge feature branches into main using squash commits with comprehensive commit messages. Use this skill when the user requests to merge, ship, or integrate a feature branch into the main branch. The skill analyzes all commits in the feature branch to understand the full scope of changes, then creates a single squashed commit with a proper conventional commit message that summarizes the entire feature.
---

# Feature Merge

## Overview

Merge feature branches into `main` using a squash merge strategy. Analyze all commits in the feature branch to understand the complete scope of changes, then create a single comprehensive commit message following the project's Conventional Commits format. After merging, clean up the feature branch from both local and remote repositories.

## When to Use This Skill

Use this skill when:
- The user requests to merge a feature branch into `main`
- The user asks to "ship" or "integrate" their current branch
- A feature branch is complete and ready to be merged with a clean history
- Multiple commits need to be consolidated into a single logical change

## Workflow

### Step 1: Validate Preconditions

Before beginning the merge process, verify the following:

1. **Confirm current branch**: Use `git branch --show-current` to identify the feature branch
2. **Check main branch existence**: Verify `main` branch exists (if not, check for `master`)
3. **Ensure clean working directory**: Run `git status` to confirm no uncommitted changes
4. **Verify branch divergence**: Ensure the feature branch has diverged from `main` with commits to merge

If any preconditions fail, inform the user and stop the process.

### Step 2: Analyze the Feature Branch

Gather comprehensive information about all changes in the feature branch:

1. **Review commit history**: Run `git log main..HEAD --oneline` to see all commits that will be merged
2. **Examine full diff**: Run `git diff main...HEAD` to understand the complete scope of changes
3. **Review individual commits**: Run `git log main..HEAD` (without `--oneline`) to see detailed commit messages

The commits serve as reference material ONLY to understand what was done. Do not incorporate the existing commit messages directly into the squash commit.

### Step 3: Determine the Commit Type

Based on the changes analyzed, determine the appropriate Conventional Commit type:

- **feat**: For new features or significant new functionality
- **fix**: For bug fixes
- **refactor**: For code restructuring without functional changes
- **perf**: For performance improvements
- **docs**: For documentation-only changes
- **test**: For test additions or updates
- **chore**: For maintenance tasks (dependencies, build scripts, etc.)

If the branch contains multiple types of changes, use the primary type that best represents the overall purpose of the branch.

### Step 4: Craft the Squash Commit Message

Create a comprehensive commit message that:

1. **Follows Conventional Commits format**: `<type>: <description>`
2. **Summarizes the complete feature**: Describes what the branch accomplishes as a whole
3. **Focuses on the "why" and "what"**: Explains the purpose and outcome, not implementation details
4. **Uses present tense**: "Add feature" not "Added feature"
5. **Is concise but complete**: One clear sentence for the subject line

For complex features, optionally include a body that provides additional context:

```
feat: Add automated release workflow

Implement GitHub Actions workflow with GoReleaser for automated
binary builds and release creation. Supports semantic versioning
and changelog generation from conventional commits.
```

Load the commit conventions from `references/commit_conventions.md` to ensure proper formatting.

### Step 5: Execute the Merge

Perform the squash merge with the crafted commit message:

1. **Switch to main branch**: `git checkout main`
2. **Update main**: `git pull origin main` to ensure local main is current
3. **Perform squash merge**: `git merge --squash <feature-branch>`
4. **Create the commit**: `git commit -m "<commit-message>"`

Use a HEREDOC for multi-line commit messages to ensure proper formatting:

```bash
git commit -m "$(cat <<'EOF'
<type>: <description>

<optional body>
EOF
)"
```

### Step 6: Clean Up the Feature Branch

After successful merge, remove the feature branch:

1. **Delete local branch**: `git branch -d <feature-branch>`
2. **Delete remote branch**: `git push origin --delete <feature-branch>`

If the remote branch doesn't exist (already deleted or never pushed), the delete command will fail gracefully - this is expected and acceptable.

### Step 7: Confirm Completion

Inform the user of the successful merge:

1. **Summarize what was done**: "Merged feature branch `<name>` into `main`"
2. **Display the commit message**: Show the final commit message used
3. **Remind about pushing**: "The merge is on local `main`. Push when ready with `git push origin main`"
4. **Confirm cleanup**: Note that the feature branch has been deleted

## Error Handling

### Merge Conflicts

If `git merge --squash` results in conflicts:

1. Display the conflicting files
2. Inform the user they need to resolve conflicts manually
3. Provide guidance: "After resolving conflicts, run `git add .` then `git commit`"
4. Do not proceed with automatic commit creation

### Branch Already Merged

If the feature branch has no commits ahead of `main`:

1. Inform the user the branch is already merged or has no changes
2. Ask if they want to delete the branch anyway
3. Do not attempt the merge

### Uncommitted Changes

If `git status` shows uncommitted changes:

1. Display the uncommitted changes
2. Ask the user to either commit or stash changes first
3. Do not proceed with the merge

## References

- `references/commit_conventions.md`: Detailed commit message format and examples
