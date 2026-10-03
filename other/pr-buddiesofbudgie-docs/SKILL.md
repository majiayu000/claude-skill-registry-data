---
name: pr
description: Create a pull request for the current branch
disable-model-invocation: false
allowed-tools: Bash(git *), Bash(gh pr create *), Skill(commit)
---

# Create a Pull Request

You are creating a pull request for the current branch on Buddies of Budgie docs (Docusaurus / React / TypeScript site).

## Step 1: Gather Context

Run these commands to understand the current state:

```bash
git status
git log --oneline main..HEAD
git diff main...HEAD --stat
git diff main...HEAD
git branch --show-current
```

If there are uncommitted changes, run the `/commit` skill first before proceeding.

## Step 2: Determine PR Type

Based on the changes, choose the conventional commit prefix:

- **`feat:`** - New feature or functionality
- **`fix:`** - Bug fix
- **`chore:`** - Maintenance, dependency updates, refactoring
- **`docs:`** - Documentation content changes
- **`refactor:`** - Code restructuring without behavior change

## Step 3: Generate PR Content

**Title format**: `<type>: <short description>` (under 70 characters)

**Body format**:

```markdown
## Summary

- <bullet point describing key change 1>
- <bullet point describing key change 2>
- <bullet point describing key change 3>

## Test plan

- [ ] `yarn build` completes successfully
- [ ] `yarn typecheck` passes
- [ ] `yarn lint` passes
- [ ] Verified locally with `yarn start`
- [ ] <additional specific test steps>
```

If any commits include `Assisted-by` trailers, note that in the PR description (e.g., "AI-assisted - see commit trailers for details").

## Step 4: Create the PR

Push the branch and create the PR:

```bash
git push -u origin HEAD
gh pr create --title "<title>" --body "$(cat <<'EOF'
<body content>
EOF
)"
```

**Target branch**: `main` (default)

## Notes

- Review all commits since divergence from main, not just the latest one
- Ensure the title accurately reflects the overall change
- Test plan should include `yarn build`, `yarn typecheck`, and `yarn lint`
