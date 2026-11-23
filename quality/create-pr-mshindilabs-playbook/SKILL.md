---
name: create-pr
description: >
  Open a pull request from the current branch to any target branch, defaulting to the
  repository's main branch. Validates branch state, commits pending work safely, shows
  what will be published and waits for a yes, then pushes and opens the PR with gh pr
  create. Use this for every single-change PR regardless of target — feature branches to
  main, and also to dev, staging, or release lines. Trigger on "open a PR", "create a
  pull request", "raise a PR for this branch", "put this up for review". Run
  run-pre-pr-checks first if the local quality gate has not passed yet; use
  ship-release-candidate instead when the branch bundles multiple changes into a
  versioned release.
---

# create-pr

Determine `TARGET_BRANCH`:

- If the user named a branch, use it.
- If the user said "ship it", "open a PR", or similar without naming a branch, default
  to the repository's main branch — detect it rather than assuming the name:

```bash
base=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
echo "${base:-main}"
```

- Only ask when the repo has several plausible integration branches (for example both
  `develop` and `main` receive feature work) and the intent is genuinely ambiguous:

> "Which branch should this PR target? (for example `dev`, `staging`, or `main`)"

---

## Commit & PR hygiene (always applies)

Include the ticket or issue reference when one exists, and never invent one. Never add AI or agent attribution (`Co-authored-by:` naming an AI tool, "Generated with ..." and the like) to a commit, PR or release note, and strip any you find. The `commit-changes` skill has the full rules.

If a guard or a git hook blocks a commit or push, fix the cause and never bypass it (no `--no-verify`). See "If a guard or a git hook blocks you" in the `commit-changes` skill.

---

## Step 1 — Preflight checks

Inspect the repository before staging, committing, pushing, or creating a PR:

```bash
git branch --show-current
git status --short
git diff
git diff --staged
git status -sb
git fetch origin
git log --oneline --decorate -5
git log origin/$TARGET_BRANCH..HEAD --oneline
git diff --stat origin/$TARGET_BRANCH...HEAD
```

Record:

- `CURRENT_BRANCH`
- whether there are staged changes, unstaged changes, or untracked files
- whether `CURRENT_BRANCH` already tracks a remote branch
- whether the branch is ahead, behind, or diverged from its upstream

Stop and ask the user if:

- `CURRENT_BRANCH` is empty, detached, or equals `TARGET_BRANCH`
- the working tree contains suspicious unrelated changes
- the branch is behind its upstream and a rebase/merge decision is needed

If there are no changes to commit **and** no commits on `CURRENT_BRANCH` that are not already in `TARGET_BRANCH`, stop and tell the user there is nothing to open a PR for.

---

## Step 2 — Validate the target branch and PR state

Before creating the PR, confirm the target branch exists on the remote and that a PR is not already open for the same branch pair.

Run checks equivalent to:

```bash
git ls-remote --heads origin <TARGET_BRANCH>
git log origin/<TARGET_BRANCH>..HEAD --oneline
git diff --stat origin/<TARGET_BRANCH>...HEAD
gh pr list --head <CURRENT_BRANCH> --base <TARGET_BRANCH> --state open
```

Rules:

- If `origin/<TARGET_BRANCH>` does not exist, stop and report it
- If there are zero commits between `origin/<TARGET_BRANCH>` and `HEAD`, stop and tell the user there is nothing new to propose
- If an open PR already exists for `CURRENT_BRANCH` -> `TARGET_BRANCH`, do **not** create a duplicate; return that PR instead

---

## Step 3 — Look for a repository PR template

Before writing the PR body, check for a repository template in `.github/`, including:

```text
.github/pull_request_template.md
.github/PULL_REQUEST_TEMPLATE.md
.github/PULL_REQUEST_TEMPLATE/*.md
```

If a template exists:

- Read it and use it as the default structure
- Preserve its section headings unless the repository clearly prefers a different format
- Fill in only the sections supported by the actual diff and evidence available
- Leave placeholders or unchecked items only when the information is genuinely unavailable

Prefer the detected template over any generic fallback.

If there is no PR template in this repo, use the fallback structure in Step 7.

---

## Step 4 — Review the full change set

Build a complete understanding of what the PR will contain:

```bash
git diff origin/<TARGET_BRANCH>...HEAD
git diff --name-status origin/<TARGET_BRANCH>...HEAD
git diff --stat origin/<TARGET_BRANCH>...HEAD
git log origin/<TARGET_BRANCH>..HEAD --oneline
```

Understand:

- the full file-level diff
- all commits included in the PR, not just the latest one
- whether the branch mixes unrelated work that should be split first
- whether there are migrations, config changes, docs changes, or breaking changes

If the branch contains multiple unrelated concerns, stop and ask the user before creating a broad PR.

---

## Step 5 — Handle local changes before PR creation

If there are uncommitted local changes, decide whether a commit is needed first.

Rules:

- Never stage secrets, `.env`, `.env.*`, private keys, or similar sensitive files
- Never use `git add -A` or `git add .` unless the user explicitly confirms every changed file belongs
- Prefer explicit staging paths
- If the current work is intentionally incomplete and the user only wants a PR for already committed work, do not auto-commit local changes
- If the PR requires the local changes, create a commit first using the repository commit rules

When committing:

- Use a proper conventional commit message if the repo enforces it
- Prefer a HEREDOC for multi-line commit messages
- Do not add AI attribution or `Co-authored-by`
- If hooks fail, inspect the failure, fix what is reasonable, and retry safely

If there is nothing new to commit, skip this step.

---

## Step 6 — Confirm with the user, then push

Pushing and opening a PR publish the work. Before the first push, draft the PR title (rules in Step 7) and show the user:

- the head branch (`CURRENT_BRANCH`) and the base branch (`TARGET_BRANCH`)
- the commits that will be in the PR (`git log origin/<TARGET_BRANCH>..HEAD --oneline`)
- the PR title
- whether the branch still has to be pushed

Then stop and wait for a yes. The request that started this skill is not that yes, because the user had not seen this summary. Without a yes, do not push and do not create the PR. If the base, the commits or the title change after the yes, show the summary again and ask again.

After the yes, push:

```bash
git push -u origin <CURRENT_BRANCH>
```

If the upstream already exists and is healthy:

```bash
git push origin <CURRENT_BRANCH>
```

Rules:

- Never force push unless the user explicitly asks for it
- If the push is rejected because the remote moved, stop and report the reason
- If authentication or permission fails, report it clearly

---

## Step 7 — Draft the PR title and body

### PR title

Use the best summary of the branch:

- If the PR contains one main commit, the title can closely follow that commit subject
- If the PR contains multiple commits, summarize the overall change rather than copying only the latest commit
- Keep the title concise and reviewer-friendly

### PR body

If a repository PR template exists, use it.

If there is no PR template in this repo, use this fallback and delete every section that does not apply:

```markdown
## Summary

<brief description of the change set>

## Changes Made

- <main change>
- <main change>

## Related Issue(s)

- <Fixes/Closes/Refs ... issue or ticket, if known>

## Type of Change

- [x] <relevant type>

## Testing

- [x] <only if actually verified>

<describe the tests that were run>

## Database Changes

- [x] <relevant option>

<describe migration/schema impact if any>

## Deployment Notes

<special deployment considerations if any>

## Checklist

- [x] <only for items you can support with evidence>

## Screenshots (if applicable)

<only when relevant>

## Additional Notes

<reviewer context, risks, or follow-up>
```

Rules:

- Do not claim tests passed unless you ran them or the user explicitly confirmed them
- Do not invent issue numbers, tickets, screenshots, migrations, or deployment steps
- Mention risks, missing verification, or follow-up work explicitly

---

## Step 8 — Create the PR safely

Use `gh pr create` with a HEREDOC body so formatting is preserved:

```bash
gh pr create \
  --base <TARGET_BRANCH> \
  --head <CURRENT_BRANCH> \
  --title "<title>" \
  --body "$(cat <<'EOF'
<body>
EOF
)"
```

Before running it:

- Ensure the user said yes in Step 6 to this base and this title
- Ensure there is no existing open PR for the same `head` and `base`
- Ensure the branch has been pushed successfully
- Ensure the body reflects the repository template if one exists

After running it, capture the PR URL.

---

## Step 9 — Report back

Show the user:

- the PR URL
- the base branch and head branch
- whether a new commit was created, and the commit message if so
- a concise diff summary from `git diff --stat origin/<TARGET_BRANCH>...HEAD`
- major risks, missing tests, migration notes, or deployment concerns

If anything blocks completion, stop and explain the exact failure:

- invalid target branch
- push rejected
- hook failure
- existing PR already open
- no diff against target branch
