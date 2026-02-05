---
name: publish
description: Publish the easier package to PyPI. Validates versions, checks git state, updates files, and guides through the complete release workflow. Use when ready to release a new version.
---

# Publish to PyPI

This skill guides you through publishing the easier package to PyPI with full validation and safety checks.

## Workflow

### Step 1: Show Current State

First, gather version information from all sources:

1. **Fetch PyPI version**: Use WebFetch to get `https://pypi.org/pypi/easier/json` and extract the latest version from the response
2. **Read pyproject.toml**: Find the `version = "X.Y.Z"` line in the `[project]` section
3. **Read easier/__init__.py**: Find the `__version__ = "X.Y.Z"` line

Display all three versions to the user and note any mismatches between local files.

### Step 2: Prompt for New Version

Ask the user: "What version would you like to release? (e.g., 1.10.0)"

Validate the response:
- Must match semantic versioning format: X.Y.Z (digits only, separated by dots)
- Should be greater than the current PyPI version

If validation fails, explain the issue and ask again.

### Step 3: Pre-flight Validation

Run these checks and report results. All must pass before proceeding:

1. **Version not on PyPI**: Confirm the requested version doesn't already exist in PyPI releases
2. **Clean working directory**: Run `git status --porcelain` and check that output has no lines (ignoring lines starting with `??` for untracked files)
3. **No unpushed commits**: Run `git status -sb` and verify the output doesn't contain "ahead"

If any check fails:
- Clearly explain which check failed and why
- Stop the workflow and ask the user to fix the issue before retrying

### Step 4: Update Version Files

Update both files with the new version:

1. **Edit pyproject.toml**: Replace the existing `version = "..."` line with `version = "X.Y.Z"`
2. **Edit easier/__init__.py**: Replace the existing `__version__ = "..."` line with `__version__ = "X.Y.Z"`

### Step 5: Git Operations

Perform git operations with user confirmation at each step:

1. Run `git status` to show the changes
2. Ask: "Stage pyproject.toml?" - If yes, run `git add pyproject.toml`
3. Ask: "Stage easier/__init__.py?" - If yes, run `git add easier/__init__.py`
4. Create commit with message: `[Release]: Bump version to vX.Y.Z for PyPI release`
5. Run `git push origin` to push the commit
6. Run `git tag X.Y.Z` to create the version tag
7. Run `git push origin X.Y.Z` to push the tag

**Safety rules:**
- NEVER use `git add .` - always add files individually
- NEVER use `git diff` without flags (causes vim to open)
- Use `git status` and `git diff --stat` for showing changes

### Step 6: Build and Publish

Execute the publish commands:

```bash
rm -rf dist/ build/
pip install build twine
python -m build
twine upload dist/*
```

After successful upload, report:
- Success message
- Link to the package: `https://pypi.org/project/easier/X.Y.Z/`

## Error Handling

- If any git command fails, stop and report the error
- If twine upload fails, the tag and commit are already pushed - inform user they may need to manually fix
- If version already exists on PyPI, stop before making any changes

## Example Session

```
User: /publish

Claude: Let me check the current versions...

PyPI version: 1.9.9
pyproject.toml: 1.9.9
easier/__init__.py: 1.9.9

All versions are in sync. What version would you like to release?

User: 1.10.0

Claude: Running pre-flight checks...
- Version 1.10.0 not on PyPI
- Working directory is clean
- No unpushed commits

All checks passed! Updating version files...

[Updates files]

Here's the current git status:
M pyproject.toml
M easier/__init__.py

Stage pyproject.toml?

User: yes

Claude: Staged. Stage easier/__init__.py?

User: yes

Claude: Creating commit...
[Commits, pushes, tags, publishes]

Successfully published easier 1.10.0 to PyPI!
https://pypi.org/project/easier/1.10.0/
```
