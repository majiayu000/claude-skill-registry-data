---
name: creating-pr-from-branch
description: Create a pull request from the current branch. Analyzes commits, generates title+body from PR template, pauses for approval, then pushes and creates PR. Use after committing changes.
compatibility: Designed for Claude Code
metadata:
  model: haiku
  argument-hint: [base-branch]
  disable-model-invocation: true
  allowed-tools: Bash, Read, Glob, Grep
---

# Create PR from Current Branch

**Base branch**: $ARGUMENTS (default: `main`)

## Step 1: Analyze Branch

Run using the Bash tool:

- `git branch --show-current` — current branch name
- `git log --oneline <base>..HEAD` — commits to include
- `git diff --stat <base>..HEAD` — overall diff stats
- `git remote -v` — verify remote exists

If no commits ahead of base, stop and inform the user.

## Step 2: Generate PR Title and Body

**Title**: Derive from commits using conventional commit format.

- Single commit: use commit subject as-is
- Multiple commits: synthesize a summary title (`type[(scope)]: description`)
- Keep under 72 characters

**Body**: Use the first PR template found, then populate its sections:

1. **Local repo** — `pull_request_template.md` (any case) in `.github/`, the repo root, or
   `docs/`; or a file in `.github/PULL_REQUEST_TEMPLATE/` (ask which one if several).
2. **Owner-level default** — the `<owner>/.github` repo. GitHub applies it only in the web UI,
   never to `gh pr create --body`, so fetch it explicitly. The contents API is case-sensitive:
   try both spellings, and skip on 404 (no repo or no file):

   ```bash
   OWNER=$(gh repo view --json owner --jq .owner.login)
   for f in PULL_REQUEST_TEMPLATE.md pull_request_template.md; do
     t=$(gh api "repos/$OWNER/.github/contents/.github/$f" --jq .content 2>/dev/null) \
       && { printf '%s' "$t" | base64 -d; break; }
   done
   ```

3. **Last resort** — this minimal format:

```markdown
## Summary

<1-3 bullet points describing what and why>

## Commits

<list commits from git log>
```

**Body guidelines:**

- Fill template checkboxes where applicable (check items that are done)
- Include `Closes #N` if the branch name contains an issue number
- Keep it concise — the diff speaks for itself

## Step 3: Pause for Approval

Present the title and body. Ask the user:

- **Approve**: "yes", "y", "create", "go ahead"
- **Edit**: Provide changes to title or body
- **Cancel**: "no", "cancel", "stop"

## Step 4: Push and Create PR

Once approved:

```bash
# Push branch (set upstream)
git push -u origin <branch-name>

# Create PR
# In Codespaces: override token if GH_PAT is needed for cross-repo
gh pr create --base <base> --title "<title>" --body "$(cat <<'EOF'
<body>
EOF
)"
```

**Auth handling**: If `gh pr create` fails with 403/422, retry with
`GITHUB_TOKEN="" GH_TOKEN="${GH_PAT}"` prefix (Codespaces token override).

After creation, output the PR URL.

## Step 5: Post-Create

- `gh pr view --web` — open in browser (optional, ask user)
