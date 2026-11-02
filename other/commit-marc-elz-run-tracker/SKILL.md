---
name: commit
description: >
  Review the diff, then commit with a message that explains why. Never amends, force-pushes or
  skips hooks unless asked. Use for "commit this", "commit my changes", "make a commit".
argument-hint: "[message hint: optional]"
allowed-tools: Bash(git status *), Bash(git diff *), Bash(git log *), Bash(git add *), Bash(git commit *), Bash(git branch *)
---

# commit

## Workflow

### Step 1: Survey the change

Run in parallel: `git status` (never `-uall` — it can exhaust resources on large repos),
`git diff` for unstaged changes, `git diff --staged` for anything already staged, and
`git log --oneline -10` to pick up the repo's existing message style/conventions, and
`git branch --show-current`. If that is the default branch and the project's `CLAUDE.md` says
work happens on branches, stop and offer to create the right branch first.

### Step 2: Screen for anything that shouldn't be committed

Before staging, scan the changed/untracked file list for likely secrets or credentials
(`.env`, `*credentials*`, `*.pem`, `*_key*`, etc.) — even if the filename looks innocuous,
skim the diff content itself for anything that looks like a token or password. If found,
exclude it and tell the user why, rather than silently including or silently dropping it.

Never stage with `git add -A` or `git add .` by default — name files explicitly, so an
unrelated WIP file or a secret doesn't ride along.

### Step 3: Draft the commit message

Identify the nature of the change (feature, fix, refactor, docs, test, chore) from the
diff. Write 1-2 sentences focused on *why* the change was made, not a restatement of what
the diff already shows line-by-line. Match the repo's existing style from Step 1 — if it
uses Conventional Commits (`feat:`, `fix:`, ...), follow that; otherwise match the
observed tone/format.

### Step 4: Stage and commit

`git add` the specific approved files, then commit with the message passed via a heredoc
(preserves formatting/line breaks reliably):

```bash
git commit -m "$(cat <<'EOF'
<subject line>

<optional body>
EOF
)"
```

Then run `git status` to confirm the commit landed and the tree is otherwise clean.

### Step 5: Handle a failing pre-commit hook

If the commit is rejected by a hook, the commit did **not** happen — fix the underlying
issue, re-stage, and create a new commit. Never reach for `--amend` here: with no
successful commit yet, `--amend` would rewrite the *previous* commit instead.

### Step 6: Report back

State the resulting commit hash and subject line. If anything was excluded in Step 2 or
skipped for any other reason, say so explicitly.

## Anti-patterns

- `git add -A` / `git add .` as the default staging move.
- Reaching for `--amend` instead of a new commit, outside an explicit user request.
- `--no-verify`, `--no-gpg-sign`, or any other hook/signature bypass without the user
  explicitly asking for it.
- Committing without having shown the user the diff/status first.
- A commit message that restates the diff mechanically instead of saying why it exists.
- Pushing as part of this flow — pushing is a separate, explicit action; this skill only
  commits locally.

## Rules

- Only ever commits — never pushes, never force-pushes, never touches remotes.
- If the diff touches files that look unrelated to what the user asked for, flag it and
  confirm scope before committing rather than assuming it's fine.
- If there's nothing staged or changed, say so — don't create an empty commit.
