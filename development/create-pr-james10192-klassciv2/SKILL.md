---
name: create-pr
description: Create a pull request. Use when the user asks to create a PR or push their branch.
---

Create a pull request following the team workflow.

## Step 1 — Verify state
```bash
git status
git log presentation..HEAD --oneline
git diff presentation...HEAD --stat
```

**For this project, the base branch is always `presentation`.**

## Step 2 — Push branch
```bash
git push -u origin HEAD
```

## Step 3 — Pre-PR sanity check
Before creating the PR, verify:
- No `.env`, secrets, or build artifacts committed
- All commits follow conventional format (`type(scope): description`)
- Commit author is `James10192 <djedjelipatrick@gmail.com>`
- No "Generated with Claude Code" or "Co-Authored-By" in any commit

## Step 4 — Detect epic/issue context

Check the conversation and commit messages for issue references:
- If commits contain `Refs #N` or `Closes #N`, extract the issue number
- If the user mentioned an issue number, use that
- If the branch name contains an issue number, use that
- Run `gh issue view N --json title,body 2>/dev/null` to get epic details if available

## Step 5 — Create the PR

**If linked to an epic with lots/phases**, use this template:
```bash
gh pr create \
  --base presentation \
  --title "<type>(<scope>): <description>" \
  --body "$(cat <<'EOF'
## Summary
- [What this PR does in 1-3 bullet points]

## Changes
- `file` — [what changed and why]

## Epic: #N — [Epic title]
**Lot progress:** X/Y

| Lot | Description | Status |
|-----|-------------|--------|
| 1 | ... | done/in-progress/planned |

## Type of change
- [ ] feat — new feature
- [ ] fix — bug fix
- [ ] refactor — no behavior change
- [ ] chore — maintenance

## Testing
- [ ] Tested on esbtp-abidjan.klassci.com after deploy
- [ ] No regressions

## Checklist
- [ ] No secrets or sensitive data committed
- [ ] PHP syntax verified (php -l) on all modified PHP files

Refs #N
EOF
)"
```

**If NOT linked to an epic**, use the standard template:
```bash
gh pr create \
  --base presentation \
  --title "<type>(<scope>): <description>" \
  --body "$(cat <<'EOF'
## Summary
- [What this PR does in 1-3 bullet points]

## Changes
- `file` — [what changed and why]

## Type of change
- [ ] feat — new feature
- [ ] fix — bug fix
- [ ] refactor — no behavior change
- [ ] chore — maintenance

## Testing
- [ ] Tested on esbtp-abidjan.klassci.com after deploy
- [ ] No regressions

## Checklist
- [ ] No secrets or sensitive data committed
- [ ] PHP syntax verified (php -l) on all modified PHP files
EOF
)"
```

## Step 6 — Output
Return the PR URL to the user.

After PR is created, inform the user:
> "PR créée. Après review et merge, lancez `/git:worktree-finish <N>`"

$ARGUMENTS
