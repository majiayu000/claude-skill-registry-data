---
name: pr
description: >
  Create a well-structured GitHub PR with proper branching, testing, formatting, and documentation.
  Use when the user says "create a PR", "make a PR", "open a pull request", or wants to submit
  changes for review. Handles the full workflow: branch creation, implementation, testing,
  formatting, committing, and PR creation with comprehensive descriptions.
---

# Create a GitHub Pull Request

## Overview

This skill guides the complete PR workflow from branch creation to PR submission. Follow all steps
in order to ensure high-quality, well-documented contributions.

## Step 1: Branch Setup

### Pull latest main
```bash
git checkout main
git pull origin main
```

### Create feature branch
Use a descriptive branch name following the pattern: `{type}/{description}`

Types:
- `feature/` - New functionality
- `fix/` - Bug fixes
- `refactor/` - Code restructuring
- `docs/` - Documentation updates
- `test/` - Test additions/improvements

```bash
git checkout -b feature/descriptive-name
```

## Step 2: Understand the Problem

Before coding, clearly identify:
1. **Core problem**: What issue are we solving?
2. **Scope**: What files/modules will be affected?
3. **Approach**: What's the implementation strategy?
4. **Edge cases**: What scenarios need special handling?

If there's an associated GitHub issue, fetch it for context:
```bash
gh issue view <issue-number>
```

## Step 3: Implement Changes

- Make focused, incremental changes
- Follow existing code patterns and style
- Add docstrings and comments for complex logic
- Consider backwards compatibility

## Step 4: Write Tests

### Location
Tests go in the `tests/` directory, mirroring the source structure.

### Requirements
- Cover all new functionality
- Test edge cases and error conditions
- Test both success and failure paths
- Aim for high coverage of changed code

### Test file naming
- `test_{module_name}.py` for module tests
- Place in corresponding `tests/` subdirectory

## Step 5: Format Code

Check GitHub workflows for the project's formatting commands:
```bash
# Check .github/workflows/ for exact commands
# Typical formatting for this project:
uv run black sleap_nn tests
uv run ruff check sleap_nn/ --fix
```

## Step 6: Check Spelling

This repo runs `codespell` in CI (`.github/workflows/codespell.yml`) against the whole tree
(config in `pyproject.toml`'s `[tool.codespell]`), and it blocks merge on any hit — including in
test docstrings/comments, not just source. Check it locally before pushing so it isn't caught only
after CI runs:

```bash
uvx codespell sleap_nn tests docs *.md pyproject.toml
```

Fix any reported typos (codespell prints `word ==> suggestion`) and re-run until clean. Don't run
bare `uvx codespell .` — it will also scan `.venv`/`scratch` if present locally and drown real hits
in unrelated noise from vendored/third-party files that CI never sees.

## Step 7: Run Tests with Coverage

Run the full test suite with coverage:
```bash
uv run pytest -q --maxfail=1 --cov --cov-branch && rm -f .coverage.* && uv run coverage annotate
```

### Check coverage for changed files
The coverage annotate command creates `{module_name.py},cover` files next to each module.

To find which files changed:
```bash
git diff --name-only $(git merge-base origin/main HEAD)
```

Review the `,cover` files for your changed modules to ensure adequate coverage.

### Coverage markers in annotated files

| Marker | Meaning |
|--------|---------|
| > | Line was executed |
| ! | Line was NOT executed (needs test coverage) |
| - | Line is not executable (comments, blank lines) |

## Step 8: Commit Changes

### Commit structure
Make well-structured, atomic commits:
- Each commit should be a logical unit of work
- Write clear, descriptive commit messages
- Use conventional commit format when appropriate

### Commit message format
```
<type>: <short description>

<optional longer description>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

## Step 9: Push to GitHub

```bash
git push -u origin <branch-name>
```

## Step 10: Create Pull Request

### Create the PR
```bash
gh pr create --title "<descriptive title>" --body "$(cat <<'EOF'
## Summary
<1-3 bullet points describing the changes>

## Changes Made
- <detailed list of changes>

## Example Usage
```python
# For enhancements, show how to use the new functionality
```

## API Changes
- <list any API changes, new parameters, removed functionality>

## Testing
- <describe test coverage>
- <note any manual testing done>

## Design Decisions
- <explain key architectural choices>
- <note trade-offs considered>

## Future Considerations
- <potential improvements not in scope>
- <known limitations>

## Related Issues
Closes #<issue-number> (if applicable)

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### If updating an existing PR

Fetch current PR description:
```bash
gh pr view <pr-number> --json body -q '.body'
```

Update PR description:
```bash
gh pr edit <pr-number> --body "<new body>"
```

### Fetch associated issue for context
If an issue is linked:
```bash
gh issue view <issue-number>
```

Use issue context to ensure PR description addresses all requirements.

## PR Description Checklist

- [ ] Summary clearly explains the "what" and "why"
- [ ] All significant changes are documented
- [ ] Example usage provided for new features
- [ ] API changes explicitly listed
- [ ] Breaking changes highlighted
- [ ] Test coverage described
- [ ] Design decisions explained with reasoning
- [ ] Related issues linked

## Quick Reference Commands

```bash
# Branch setup
git checkout main && git pull origin main
git checkout -b feature/my-feature

# Format and lint
uv run black sleap_nn tests
uv run ruff check sleap_nn/ --fix

# Spelling (CI runs this on the whole tree, incl. tests/docs -- scope it locally to match)
uvx codespell sleap_nn tests docs *.md pyproject.toml

# Test with coverage
uv run pytest -q --maxfail=1 --cov --cov-branch && rm -f .coverage.* && uv run coverage annotate

# Find changed files
git diff --name-only $(git merge-base origin/main HEAD)

# Commit
git add <files>
git commit -m "feat: description"

# Push and create PR
git push -u origin <branch>
gh pr create --title "Title" --body "Description"

# View/edit existing PR
gh pr view <number>
gh pr edit <number> --body "New description"

# View linked issue
gh issue view <number>
```
