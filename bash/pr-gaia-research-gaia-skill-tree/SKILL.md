---
name: pr
description: Push committed changes and create a draft PR on GitHub. Use when you have staged changes ready to push and want to open a draft PR for early feedback or documentation.
---

# PR

Quickly push changes and open a draft pull request on GitHub.

## When to Use

- You have staged changes ready to push and want to create a draft PR
- Early feedback needed on work-in-progress
- Want to document and track changes before final review
- Need to open a PR for discussion or CI validation

## Instructions

### Step 1: Verify Staged Changes

Check what will be committed:
```bash
git status
```

Ensure all changes you want are staged with:
```bash
git add <files>
```

Or add everything:
```bash
git add .
```

### Step 2: Create Commit Message

Write a clear, conventional commit message. Use the format:
```
<type>(<scope>): <description>

<optional body with details>
```

Types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, etc.

Examples:
- `feat(registry): add new skill category`
- `fix(cli): resolve version mismatch`
- `chore: regenerate artifacts`

### Step 3: Commit Changes

```bash
git commit -m "your commit message here"
```

### Step 5: Push to Remote

```bash
git push -u origin <branch-name>
```

If you're on `main` or pushing to an existing branch:
```bash
git push
```

### Step 6: Create Draft PR

```bash
gh pr create --draft
```

This will prompt you for:
- **Title** — auto-filled from commit, edit as needed
- **Body** — add context, description, or leave blank
- **Assignees** — optional
- **Labels** — apply by judgement; see Step 7

For multiline descriptions, use a body file with real newlines. Do **not** pass literal `\\n` sequences or rely on shell `$'...'` quoting; malformed quoting can make GitHub display `\\n` (and sometimes a stray `$`).

```bash
cat > /tmp/pr-body.md <<'EOF'
## Summary

Describe the change here.
EOF
gh pr create --draft --title "Your PR Title" --body-file /tmp/pr-body.md
```

After creating or editing the PR, verify the stored body:

```bash
gh pr view <number> --json body --jq .body
```

Or specify details inline for a one-line body:
```bash
gh pr create --draft --title "Your PR Title" --body "Description here"
```

### Step 7: Apply Labels by Judgement

Labels are how humans and automation triage the PR queue, so choose them deliberately — but **never hardcode a fixed label list**. Repos define their own labels and rename or retire them over time; a memorized set rots and won't transfer across repos. Instead, read the live set and reason about fit each time.

1. **Read the repo's actual labels** (names *and* descriptions — the description tells you the intended use):
   ```bash
   gh label list --limit 200 --json name,description --jq '.[] | "\(.name) — \(.description)"'
   ```

2. **Pick the smallest set that is actually true of this PR.** Match the diff's substance against label descriptions:
   - What *kind* of change is it? (bug fix, enhancement, refactor, docs, dependency bump …)
   - What *area* does it touch? (frontend, backend, CLI, schema, CI …)
   - Does a *cross-cutting* label genuinely apply? (performance, security, tech-debt …) — only if the PR materially does that, not aspirationally.
   - Is there a *state/process* label the repo uses for triage or gating? (needs-review, awaiting-assets, blocked …) Apply one only if it reflects reality.

3. **Prefer precision over coverage.** Two labels that are exactly right beat five that are loosely related. If nothing fits, apply nothing — a wrong label misroutes triage worse than a missing one.

4. **Skip labels you can't justify.** Roadmap/sprint/phase tags, auto-merge eligibility, ownership cosign labels, etc. usually require context the PR author must supply — don't guess them. If a required-by-process label is missing (e.g. the repo gates on a scope or migration-notes label) and you can't satisfy it, say so rather than applying it falsely.

5. **Apply, then confirm:**
   ```bash
   gh pr edit <number> --add-label "<label-1>" --add-label "<label-2>"
   gh pr view <number> --json labels --jq '.labels[].name'
   ```

State briefly *why* each label was chosen (and note any you deliberately skipped) so the reasoning is auditable.

## Tips

- **Accidental staging leakage:** if a PR contains unrelated staging changes, do not force-push blindly. Start a clean branch from current `origin/main`, apply only the intended files, verify `git diff --stat origin/main...HEAD`, then push and create a replacement draft PR. Close the contaminated PR and cross-reference the replacement in a comment.
- **Draft PRs** show as "Draft" and won't trigger auto-merge workflows
- **Rebase before final PR** — `git rebase -i origin/main` to clean up commits
- **Ready to review?** — Use `gh pr ready` to convert from draft to ready-for-review
- **Add more commits** — Just push again with `git push`, the PR updates automatically

## Troubleshooting

**"fatal: The current branch has no upstream branch"**
- Use `git push -u origin <branch-name>` on first push

**"Permission denied" when pushing**
- Check your git credentials: `gh auth status`
- Re-authenticate if needed: `gh auth login`

**PR creation fails**
- Ensure you're in a git repository: `git rev-parse --show-toplevel`
- Check GitHub CLI is installed: `gh version`
