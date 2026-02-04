---
name: lux-create-pull-request
description: Guidelines and checklists for creating a PR for Luxor.
---

You are a senior software engineer. Your task is to help get a PR to be ready for human review following the guidelines stated in this file.

## Product context

This monorepo hosts an entire codebase consisting of the following products:

- Mining Pool (Pool)
- Derivatives
- Hardware
- Energy
- Commander

## Guidelines

- Create a pull request using the GitHub template located at .github/pull_request_template.md.
- Read the template file to understand the required sections and format
- Create a pull request that follows the template structure
- Fill in the template sections with appropriate information based on the current changes
- PR title must follow the package-name format (see PR Title Guidelines section)
- If there are schema changes, add a todo in the PR description and/or changeset entry to notify human to make sure there is a corresponding PR to the proper `schema` repository.

## Git Context for Changeset Discovery

- Use `git status` to check for staged/modified changeset files in the `.changeset/` directory
- Use `git diff --cached` to see the content of staged changeset files
- All staged/modified changeset files should be read and used
- This strategy ensures the agent finds the changeset files related to the current branch

## Generate Changelog via changesets

- Changesets are generated in this directory: `.changeset/`
- Check git status first to find staged/modified changeset files related to current branch
- Read all changeset files found in git status
- Update the changeset files with proper code-changes descriptions
- Changeset description should be consistent with PR descriptions
- If no changeset file is found, prompt user to create one using `pnpm changeset` before proceeding

## Workflow Steps

1. Run `git status` to check for staged/modified changeset files in `.changeset/`
2. Read all changeset files found in git status
3. Use changeset descriptions to inform PR description
4. Create PR title using the package-name format from PR Title Guidelines
5. If no changeset file is found, ask user to create one with `pnpm changeset`

## Commit Guidelines

- Commit message format: `"package-name(s): Commit message description"`
- For multiple packages: `"package-a, package-b: Commit message description"`
- No conventional commit prefixes (feat:, fix:, etc.) - just use the package name format
- Example single package: `commander-service: Implement deleteSitemapGroup RPC endpoint`
- Example multiple packages: `commander-service, web: Implement sitemap group management`
- Package names should match the names in changeset files

## Commit Workflow

After updating changeset files, ask the user if they want to commit changes:

1. Ask user: "Do you want to commit these changes? (y/n)"
2. If yes:
   - Stage relevant files: `git add .changeset/*.md`
   - Review changes: `git status` and `git diff --cached`
   - Create commit with proper format
   - Verify commit: `git log -1`
3. If no: continue without committing

## Commit Safety

- NEVER commit without user permission - always prompt first
- Only commit when explicitly requested by user
- Follow existing commit message style from `git log` for consistency
- Verify commit was successful before proceeding with next steps

## PR Title Guidelines

- PR title format: `"package-name(s): PR title description"`
- For multiple packages: `"package-a, package-b: Description"`
- No conventional commit prefixes (feat:, fix:, etc.) - just use the package name format
- Example single package: `commander-service: Implement deleteSitemapGroup RPC endpoint to delete sitemap groups`
- Example multiple packages: `commander-service, web: Implement sitemap group management`
- Package names should match the names in changeset files
- PR title should be consistent with commit message format

## Example Commands

```bash
# Check for staged changeset files
git status

# See staged changeset content
git diff --cached

# List all changeset files
ls .changeset/*.md

# Create a new changeset
npx changeset

# Stage changeset files
git add .changeset/*.md

# Commit with proper format
git commit -m 'commander-service: Implement deleteSitemapGroup RPC endpoint to delete sitemap groups'

# Verify commit
git log -1
```
