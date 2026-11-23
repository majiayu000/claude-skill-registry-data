---
name: amend-safely
description: >
  Fix the most recent commit — its message, its staged content, or both — with hard
  guardrails against rewriting history that has already been shared. Trigger on "undo my
  last commit", "fix the commit message", "I forgot a file in my last commit", "reword
  the last commit", "amend that". Checks whether the commit has been pushed before
  touching anything, and refuses to quietly force-push over a shared branch. Only for
  commits that are still local or on your own unshared branch — once a commit is merged
  or others have pulled it, use revert-change-safely instead.
---

# amend-safely

You are a commit amendment assistant. Your job is to help the user fix the most recent commit — its message, its staged content, or both — while preventing accidental history rewriting on a shared branch.

---

## Commit & PR hygiene (always applies)

Include the ticket or issue reference when one exists, and never invent one. Never add AI or agent attribution (`Co-authored-by:` naming an AI tool, "Generated with ..." and the like) to a commit, PR or release note, and strip any you find. The `commit-changes` skill has the full rules.

If a guard or a git hook blocks a commit or push, fix the cause and never bypass it (no `--no-verify`). See "If a guard or a git hook blocks you" in the `commit-changes` skill.

---

## Step 1 — Inspect the current state

Run all of these before changing anything:

```bash
git log -1 --stat
git status --short
git diff --staged
git branch --show-current
```

Record:

- the current commit hash, subject, body, and author
- whether there are staged or unstaged changes in the working tree
- `CURRENT_BRANCH`

---

## Step 2 — Check whether the commit has been pushed

Check if the current commit exists on the remote:

```bash
git log --oneline @{u}..HEAD 2>/dev/null || echo "no upstream"
```

Interpret the output exactly as follows — this determines whether amending is safe,
so do not guess:

- **Non-empty output that includes HEAD's subject** — the commit is local-only and
  has not been pushed. Safe to amend directly.
- **Empty output** — HEAD already matches the upstream tip. The commit **has been
  pushed**. Go to the warning below.
- **`no upstream`** — the branch has no tracking ref, so the check above proved
  nothing. Confirm against the remote explicitly:

```bash
# Compare the CURRENT branch against the remote — not `git ls-remote origin HEAD`,
# which resolves the remote's default branch (usually main) and will silently
# report the wrong answer on any feature branch.
git ls-remote origin "$(git rev-parse --abbrev-ref HEAD)"
git rev-parse HEAD
```

If those two hashes match, the commit is on the remote — treat it as pushed.
If `git ls-remote` returns nothing, the branch does not exist on the remote and the
commit is local-only.

**If the commit has already been pushed to the remote:**

Stop and warn the user:

```text
Warning: this commit has already been pushed to origin/<branch>.
Amending it will require a force push, which rewrites shared history.

Force pushing to a shared branch can disrupt teammates who have already pulled.
Safe options:
  1. Make a new commit instead of amending
  2. If this branch is yours alone (no teammates have pulled), proceed with --force-with-lease

How would you like to proceed?
```

Do not amend until the user explicitly confirms they want to proceed despite the shared history risk.

**If the commit has NOT been pushed:**

Proceed to Step 3.

---

## Step 3 — Determine what the user wants to change

- **Message only**: fix a typo, change the type, update the scope, rewrite the body
- **Files only**: add a forgotten file, unstage an accidentally staged file, stage a new fix
- **Both**: change the message and update the staged content

---

## Step 4A — Amend the commit message

If the user wants to change the message:

Show the current message:

```bash
git log -1 --pretty=format:"%s%n%n%b"
```

Validate the proposed new message:

- does it follow Conventional Commits if the repo enforces it?
- is the subject line under 100 characters?
- does the type match the actual change?

Show a before/after comparison and ask for confirmation before running the amendment.

Run the amendment using a HEREDOC:

```bash
git commit --amend -m "$(cat <<'EOF'
<new subject line>

<new body if any>

<new footer if any>
EOF
)"
```

---

## Step 4B — Amend staged content

If the user wants to add or change files:

Stage only the files the user explicitly specifies:

```bash
git add <file1> <file2> ...
```

Show the resulting staged diff and ask for confirmation:

```bash
git diff --staged
```

If files need to be unstaged from the existing commit, use:

```bash
git restore --staged <file>
```

Run the amendment without changing the message:

```bash
git commit --amend --no-edit
```

---

## Step 4C — Amend both message and content

Combine Steps 4A and 4B:

1. Stage the intended files
2. Show the staged diff
3. Validate the new message
4. Show before/after comparison
5. Confirm
6. Run the amendment with the new message via HEREDOC

---

## Step 5 — Handle force push if needed

If the commit was already pushed and the user confirmed they want to proceed, use `--force-with-lease` instead of `--force`:

```bash
git push --force-with-lease origin <CURRENT_BRANCH>
```

`--force-with-lease` will abort if someone else has pushed to the branch since the last fetch, preventing overwriting teammates' work.

Never use `--force` (without `--lease`) unless the user explicitly requests it and understands the risk.

---

## Step 6 — Verify and report

```bash
git log -1 --stat
git status --short
```

Report:

- the updated commit hash
- the final commit message (subject + body)
- the files included in the commit
- whether a force push was performed and to which remote/branch
