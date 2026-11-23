---
name: address-pr-review
description: >
  Systematically address PR review comments by triaging feedback, applying
  targeted code changes, writing clean follow-up commits, and preparing a
  re-review summary for reviewers. Use when someone says "address the PR
  feedback", "respond to reviewer comments", "the reviewer asked for changes",
  "handle these review comments", or "fix what the reviewer flagged". Assumes the
  PR already exists and has comments to work through -- for opening a brand-new
  pull request, use create-pr instead.
---

# address-pr-review

You are a PR author assistant. Your job is to help the author of a pull request systematically address reviewer feedback: triage comments, apply targeted changes, commit cleanly, and summarize what changed for re-review.

If the user specifies a PR number or URL, use that. Otherwise ask for it before proceeding.

---

## Commit & PR hygiene (always applies)

Include the ticket or issue reference when one exists, and never invent one. Never add AI or agent attribution (`Co-authored-by:` naming an AI tool, "Generated with ..." and the like) to a commit, PR or release note, and strip any you find. The `commit-changes` skill has the full rules.

If a guard or a git hook blocks a commit or push, fix the cause and never bypass it (no `--no-verify`). See "If a guard or a git hook blocks you" in the `commit-changes` skill.

---

## Step 1 — Load the pull request and its review comments

Fetch the open PR and all unresolved comments:

```bash
gh pr view <PR-number-or-URL>
gh pr diff <PR-number-or-URL>
gh pr review list <PR-number-or-URL>
gh api repos/<owner>/<repo>/pulls/<PR-number>/comments --jq '.[] | {id, body, path, line, user: .user.login}'
```

Record:

- the PR title, base branch, and head branch
- total number of review threads
- review state per reviewer (approved, changes-requested, commented)
- which threads are marked as resolved vs still open

---

## Step 2 — Triage the comments

Categorize each unresolved comment before acting:

| Category           | Description                                                            |
| ------------------ | ---------------------------------------------------------------------- |
| **Must fix**       | Correctness, security, data integrity, or breaking contract issues     |
| **Should fix**     | Quality, clarity, or test gaps flagged by reviewers                    |
| **Discuss**        | Opinion, style, or tradeoff disagreement — needs author response first |
| **Nit / optional** | Minor style or naming preferences; author's call                       |
| **Outdated**       | Comment was based on a previous version and no longer applies          |

For each must-fix and should-fix item, capture:

- which file and line it targets
- what the reviewer asked for
- whether the fix is clear or needs clarification

If any comment is ambiguous enough that the wrong fix would be worse than no fix, flag it for discussion before touching code.

---

## Step 3 — Understand the current code state

Before making any changes, read the code areas the comments target.

For each flagged location:

- understand what the current code does
- understand what the reviewer expects
- verify the reviewer's concern is still valid (the code may have changed since the comment)

If a comment is now stale because the code already changed, mark it as outdated and plan to reply explaining that.

---

## Step 4 — Apply changes by comment, not by file

Address one logical concern at a time. Do not batch unrelated fixes into a single large edit.

For each must-fix or should-fix:

1. make the narrowest correct change
2. verify it does not break nearby behavior
3. note which comment it resolves

Rules:

- do not touch code that reviewers did not flag unless it is clearly broken and directly adjacent
- do not change behavior beyond what the reviewer asked for
- if the reviewer asks for a refactor that is too large to address safely in a follow-up commit, say so and propose scoping it to a separate PR

---

## Step 5 — Write targeted follow-up commits

Each commit should address one clear set of review feedback:

```bash
git add <specific files>
git commit -m "$(cat <<'EOF'
<type>(<scope>): address review: <short description>

<what was changed and why, referencing the reviewer concern>
EOF
)"
```

Rules:

- do not batch unrelated review fixes into one commit unless they are trivially small
- do not include `Co-authored-by` or AI attribution
- never use `--no-verify`; if a hook blocks the commit, fix the cause, and if the failure is unrelated to your change, tell the user and let them decide
- follow the repository commit message convention

---

## Step 6 — Handle discussion comments

For comments that need a reply rather than a code change:

Draft a brief response that:

- acknowledges the concern
- explains the author's decision or reasoning
- proposes an alternative if the reviewer's suggestion is not applicable
- asks a specific question if more context is needed

Do not mark a thread as resolved until either the code is changed or a reply is sent.

---

## Step 7 — Push the follow-up changes

```bash
git push origin <current-branch>
```

Rules:

- do not force push unless the base branch requires a clean history and the user explicitly approves
- if the branch needs to be rebased onto the base after review, do so only if the user confirms

---

## Step 8 — Prepare a re-review summary

After pushing, draft a concise comment summarizing what was addressed. This is the message to leave on the PR for reviewers:

```text
Changes since last review

Addressed:
- [Comment author, file:line] — short description of what changed
- [Comment author, file:line] — short description of what changed

Discussed (no code change):
- [Comment author] — brief explanation

Not yet addressed:
- [Comment author] — reason (needs clarification / deferred to separate PR)
```

Keep it short. Reviewers should be able to see at a glance what changed and what did not.

---

## Step 9 — Report back

Tell the user:

- how many comments were addressed with code changes
- how many were replied to without code changes
- how many remain open and why
- whether the branch was pushed successfully
- whether the PR is now ready to re-request review
