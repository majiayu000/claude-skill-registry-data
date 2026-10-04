---
name: pr
description: >-
  Create or update a pull request for the current branch. Trigger when the user
  asks to create/open/make a PR, or to edit/update/rewrite/fix the PR
  description, body, or summary — for both new PRs (`gh pr create`) and
  existing ones (`gh pr edit --body-file`). Use for any verb that lands on a
  PR's text content: "open a PR", "make a PR", "update the PR description",
  "rewrite the PR body", "fix the description".
allowed-tools: Bash, Read, Glob, Grep
---

# Pull request workflow

Create or update a pull request for the current branch.

## Workflow

### 1. Gather branch state

Run in parallel:
- `git status` (no `-uall`)
- `git diff main...HEAD --stat`
- `git diff main...HEAD --name-only`
- `git log main..HEAD --oneline`
- `EXISTING_PR=$(gh pr view --json number,url,title 2>/dev/null)` — capture for step 2.

If the branch has no commits ahead of `main`, stop and tell the user.

### 2. Build the summary body and create/update the PR

Write a summary of the change (2–5 bullets based on the diff and recent commits) to a temp file. Follow the repo's existing PR body style — look at the last few merged PRs (`gh pr list --state merged --limit 5 --json body,title`) to match tone and length. Keep the title under ~70 chars.

Bias toward brevity. Reviewers skim. A bullet that fits on one line beats one that wraps three times — push detail down to the diff or commit log, not the body. If a per-file bullet starts feeling like an essay, compress to a single sentence naming the *kind* of change (e.g., "tightened description, trimmed unused allowed-tools, consolidated duplicated snippets") rather than enumerating each edit. Aim for under ~6 bullets total across the whole body, including any nested ones; if you're past that, regroup by category until you fit.

Describe the end state, not the journey. Reviewers want to know what the PR does *now* — the diff that will land — not the order in which it was built. Avoid framings like "first pass" / "second pass", commit-hash references for stages of work that all merge into the same shipped diff, "originally we tried X then switched to Y", or play-by-play of how the conversation evolved. The git log preserves that. If a discarded approach is genuinely load-bearing context for the reviewer (e.g., explains why the chosen approach is structured oddly), one line is enough; otherwise omit. The same applies when *updating* an existing PR body: rewrite to describe the current diff, don't append a changelog of edits made since the last revision.

**No "Test plan" section unless the user asks.** Don't list things CI already covers (e.g. `bundle exec rspec`). Those belong to CI, not the PR body. Only add a Test plan when there's reviewer-facing manual verification a human needs to do, and only when the user requests it.

**No Claude Code attribution footer.** Don't append the "🤖 Generated with [Claude Code](https://claude.com/claude-code)" line (or any variant of it) to the body. The PR body should read like the human author wrote it.

Push the branch: `git push -u origin HEAD`.

- If `$EXISTING_PR` from step 1 was non-empty: `gh pr edit <num> --body-file <tmp-body-file>` (don't overwrite the title unless the user asks).
- Otherwise: `gh pr create --draft --base main --title "..." --body-file <tmp-body-file>`. Create as a draft by default; only omit `--draft` (or mark ready) if the user explicitly asks for a ready-for-review PR. Capture the PR number from the output.

Always pass the body via `--body-file` (not inline `--body`) to preserve formatting.

Return the PR URL.
