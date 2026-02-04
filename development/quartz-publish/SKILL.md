---
name: quartz-publish
description: Publish changes to the Quartz notes repository.
allowed-tools: Read, Write, Bash, Glob
---

# Quartz Publish

This skill helps publish Quartz notes to the live site by running the Quartz sync command and verifying successful completion.

## Helper Scripts

This skill includes a bash utility script for reliable publishing:

- `scripts/publish.sh` - Run Quartz sync and verify completion

### Script Usage

```bash
# Publish all changes to the live site
bash scripts/publish.sh
```

The script will:

- Navigate to the project root directory
- Run `npx quartz sync` to sync changes
- Capture the exit code and output
- Report success or failure with appropriate messaging

## Instructions

When the user requests to publish, sync, or deploy their Quartz notes, follow these steps:

### 1. Check for Uncommitted Changes

Before publishing, verify that all changes are committed to git:

```bash
git status
```

If there are uncommitted changes:

- Inform the user about the uncommitted files
- Ask if they want to commit them first or proceed anyway
- Quartz sync typically commits and pushes changes automatically, but it's good practice to be aware of what's being published

### 2. Run the Publish Script

Execute the publish script to sync changes:

```bash
bash scripts/publish.sh
```

### 3. Verify Success

The script will:

- Output the sync progress in real-time
- Report whether the sync completed successfully
- Exit with code 0 on success, non-zero on failure

If the sync fails:

- Display the error message to the user
- Check common issues:
  - Network connectivity problems
  - Git authentication issues
  - Merge conflicts
  - Invalid configuration in `quartz.config.ts`

### 4. Confirm Publication

After successful sync, inform the user:

- That their changes have been published
- The approximate time it takes for changes to appear (usually a few minutes)
- Remind them they can view their site at their configured domain

## Complete Workflow Example

User request: "Publish my notes to the live site"

```bash
# Step 1: Check git status
git status

# Step 2: Run publish script
bash scripts/publish.sh

# Step 3: Confirm success
# "Successfully published to live site! Changes should appear in a few minutes."
```

## Common Issues and Solutions

### Authentication Errors

If you see authentication errors:

- Ensure git credentials are configured correctly
- Check that SSH keys are set up for GitHub (if using SSH)
- Verify GitHub personal access token is valid (if using HTTPS)

### Merge Conflicts

If there are merge conflicts:

- The sync will fail with a merge conflict error
- User needs to manually resolve conflicts
- After resolving, run the publish script again

### Build Errors

If Quartz fails to build:

- Check for syntax errors in markdown files
- Verify all frontmatter is valid YAML
- Look for broken links or invalid references
- Check the `quartz.config.ts` for configuration issues

## Examples

### Example 1: Simple Publish

User request: "Sync my changes"

```bash
bash scripts/publish.sh
```

Output:

```
Publishing Quartz site...
npx quartz sync
[Quartz sync output...]
Successfully published! Changes are live.
```

### Example 2: Publish with Uncommitted Changes

User request: "Publish my notes"

```bash
# Check for uncommitted changes
git status

# If there are uncommitted changes:
# "You have uncommitted changes in the following files:
#  - content/notes/new-note.md
#  - content/notes/updated-note.md
#
# Would you like to commit these first, or proceed with publishing?
# (Quartz sync will commit and push these automatically)"
```

### Example 3: Handling Errors

User request: "Deploy to production"

```bash
bash scripts/publish.sh
```

If it fails:

```
Publishing Quartz site...
npx quartz sync
Error: Failed to push to remote repository
Authentication failed

The publish failed due to authentication issues.
Please check your git credentials and try again.
```

## Important Notes

- Always run from the project root directory
- The script automatically handles `npx quartz sync` execution
- Quartz sync will build the site and push to the configured remote
- Changes typically appear on the live site within 2-5 minutes (depending on hosting)
- The sync process commits all changes automatically with a default message
- If you want custom commit messages, commit changes manually before running sync

## Integration with Quartz Workflow

This skill integrates with the Quartz publishing workflow:

1. Create/edit notes using the quartz-note-creator skill
2. Preview changes locally with `npx quartz build --serve`
3. Publish changes to production using this skill
4. Verify changes on the live site

## Configuration

The publish script uses the configuration from `quartz.config.ts` in the project root. Ensure that:

- The `baseUrl` is correctly set
- GitHub repository is properly configured
- Branch names are correct (typically `v4` for content, `upstream` for framework)
