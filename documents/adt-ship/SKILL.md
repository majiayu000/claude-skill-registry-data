---
name: ship
description: Commit, push, and open a pull request with a conventional commit message
triggers:
  - ship
  - create PR
  - commit and push
  - ready to merge
---

# Ship

Run verify first. Then commit, push, and open a PR.

## Steps

```bash
# 1. Verify quality gates pass
# (run /verify or equivalent)

# 2. Stage specific files
git add <files>

# 3. Conventional commit
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>
EOF
)"

# 4. Push
git push -u origin <branch>

# 5. PR
gh pr create --title "<type>: <description>" --body "..."
```

## Commit Types

`feat` | `fix` | `refactor` | `chore` | `docs` | `style` | `ci` | `test`

## PR Body Template

```markdown
## Summary
- <what changed>

## Test plan
- [ ] CI passes
- [ ] Manually tested: <scenario>
```

## Rules

- Never push directly to main
- Never use `--no-verify` unless change is docs/config only
- Stage specific files — not `git add .` blindly
- Delete local branch after merge
