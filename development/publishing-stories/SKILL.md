---
name: publishing-stories
description: Guides commit, push, and draft PR creation for stories. Use when ready to commit changes, pushing to remote, or creating a pull request for review.
---

# Committing and Publishing

## Timing Flexibility

Acceptance testing can occur at different points depending on team workflow:

| Workflow | When to Accept |
|----------|----------------|
| Pre-commit | Developer verification → PO accepts → Commit |
| Pre-push | Commit locally → PO accepts → Push |
| Post-PR | Commit → Push → Draft PR → PO accepts → Ready for review |

Choose based on:
- How quickly PO can review
- Whether you need a deployed preview
- Team conventions

## Pre-Commit Checklist

```
Before Commit:
- [ ] Developer verification complete
- [ ] All tests pass
- [ ] Linting passes
- [ ] Story log updated with completed work
```

## Commit Message

Use Conventional Commits format:

```
<type>(<scope>): <summary>

<body explaining why this change is necessary>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

Example:
```
feat(sync): implement workspace Git initialization

Enable users to sync their notes to GitHub by
initializing the workspace as a Git repository.
```

Guidelines:
- Title: what changed and why it matters (imperative mood)
- Body: why this change is necessary in broader context
- Avoid restating what the diff shows

## Push

```bash
git push -u origin <branch-name>
```

## Draft Pull Request

For post-PR acceptance workflow:

```bash
gh pr create --draft --title "<title>" --body "$(cat <<'EOF'
## Summary
- [Key change 1]
- [Key change 2]

## Story
[Link to story log if applicable]

## Test Plan
- [How to verify this works]

**Status: Awaiting acceptance testing**
EOF
)"
```

Mark as ready after acceptance:
```bash
gh pr ready
```

## Post-Acceptance

After product owner accepts:
1. Update story log status to "Accepted"
2. If using draft PR workflow, mark PR as ready
3. Request code review if required
