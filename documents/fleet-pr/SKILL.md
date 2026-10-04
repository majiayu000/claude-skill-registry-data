---
name: fleet-pr
description: >
  Create a publication-quality Pull Request with changelog, diff table, and
  cross-references. Use when completing a project worktree task and ready
  to push + create PR. Produces visually appealing, fully-linked PR bodies
  that exploit markdown formatting.
  Triggers on: "create pr", "fleet pr", "push and pr", "submit pr".
user-invocable: true
---

# Fleet PR Composer

Create a rich, publication-quality Pull Request. **Use this instead of raw `gh pr create`.**

## When to Use

After completing work in a project worktree, when you're ready to push your
branch and create a PR. This skill handles the entire process.

## Prerequisites

1. You have committed your changes to the worktree branch
2. You know: project name, task ID, task title
3. You have read `config/url-templates.yaml` (fleet-urls skill)
4. You have read TOOLS.md for BOARD_ID

## Steps

### 1. Gather Information

```bash
# Branch name
BRANCH=$(git branch --show-current)

# Commits on this branch
git log --oneline origin/main..HEAD

# Files changed with stats
git diff --stat origin/main..HEAD

# Detailed diff for file descriptions
git diff origin/main..HEAD --name-status
```

### 2. Push Branch

```bash
git push -u origin $BRANCH
```

### 3. Resolve URLs

Using fleet-urls skill and `config/url-templates.yaml`:
- Resolve: PR will be created (get the number after creation)
- Compare URL: `https://github.com/{owner}/{repo}/compare/main...{branch}`
- File URLs: for each changed file
- Commit URLs: for each commit
- Task URL: from BOARD_ID + task ID

### 4. Build Changelog

Parse each commit message. Group by conventional commit type:
- `feat(...)` → ✨ Features
- `fix(...)` → 🐛 Fixes
- `refactor(...)` → ♻️ Refactoring
- `docs(...)` → 📚 Documentation
- `test(...)` → 🧪 Tests
- `chore(...)` → 🔧 Maintenance

Each entry: `- {description} ([\`{sha_short}\`]({commit_url}))`

Remove empty sections.

### 5. Build Changes Table

For each changed file, describe WHAT changed (not just the filename):

```markdown
| File | Change | Lines |
|------|--------|-------|
| [`nnrt/core/engine.py`](file_url) | Added `from __future__ import annotations` for Python 3.8 compat | +1/-0 |
```

**Bad:** `engine.py | modified | +1/-0`
**Good:** `engine.py | Added future annotations import for 3.8 compat | +1/-0`

The description must tell the REVIEWER what changed without reading the diff.

### 6. Create PR

Read the template at `agents/_template/markdown/pr-body.md`.
Fill all placeholders. Then:

```bash
gh pr create \
  --title "fleet({agent_name}): {task_title}" \
  --body "$(cat <<'PRBODY'
{filled template}
PRBODY
)"
```

### 7. Capture PR URL

The `gh pr create` command outputs the PR URL. Save it — you need it for:
- Task completion comment
- Board memory PR notification
- IRC notification
- Task custom field update

### 8. Post-PR Actions

After PR is created:

a. Update task custom fields:
```bash
curl -s -X PATCH "$BASE_URL/api/v1/agent/boards/$BOARD_ID/tasks/$TASK_ID" \
  -H "X-Agent-Token: $AUTH_TOKEN" -H "Content-Type: application/json" \
  -d '{"custom_field_values": {"branch": "{branch}", "pr_url": "{pr_url}"}}'
```

b. Post completion comment using `agents/_template/markdown/comment-completion.md`

c. Move task to review:
```bash
curl -s -X PATCH "$BASE_URL/api/v1/agent/boards/$BOARD_ID/tasks/$TASK_ID" \
  -H "X-Agent-Token: $AUTH_TOKEN" -H "Content-Type: application/json" \
  -d '{"status": "review", "comment": "Ready for review. PR: {pr_url}"}'
```

## Quality Standard

The PR must be **publication quality**. Before creating, verify:
- [ ] Changelog has at least one section with entries
- [ ] Every commit is listed with clickable SHA link
- [ ] Every changed file has a DESCRIPTION (not just a path)
- [ ] Every reference (task, board, branch) is a clickable link
- [ ] Summary explains the WHY, not just the WHAT
- [ ] Verification checklist is present
- [ ] Footer has agent attribution and task reference

If any of these are missing, fix them before creating the PR.

## Example Output

See a real example: https://github.com/cyberpunk042/Narrative-to-Neutral-Report-Transformer/pull/4

The goal: produce PRs that are BETTER than what a human would write manually.