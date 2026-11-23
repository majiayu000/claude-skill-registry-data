---
name: commit-changes
description: >
  Create a clean, intentional git commit with Conventional Commits formatting --
  inspects the working tree, stages files explicitly, validates the message, and
  commits safely without AI attribution. Use when someone says "commit this",
  "commit my changes", "write a commit message", "make a clean commit", or "git
  commit this". For fixing the message or contents of a commit that already
  exists, use amend-safely instead -- this skill is for creating one new commit,
  not editing the previous one.
---

# commit-changes

You are a commit assistant. Follow these steps **in order** every time. The goal is to create a clean, intentional commit that is ready to support a pull request later.

If a repository-specific convention conflicts with this file, prefer the repository convention.

---

## Commit & PR hygiene (always applies)

Include the ticket or issue reference when one exists, and never invent one. Never add AI or agent attribution (`Co-authored-by:` naming an AI tool, "Generated with ..." and the like) to a commit, PR or release note, and strip any you find. Read the full rules in [references/commit-and-pr-hygiene.md](references/commit-and-pr-hygiene.md) before writing a message.

---

## Step 1 — Inspect the repository before changing anything

Run all of these before staging or committing:

```bash
git branch --show-current
git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null
git status --short
git diff
git diff --staged
git log -5 --oneline
```

The second command prints the remote's default branch as `origin/<name>`; if it prints nothing, treat `main` or `master` as the default. If the current branch is the default branch, or a branch the project documents as protected, stop. Do not stage or commit. Hand off to the `new-branch` skill to move the work onto a branch, then come back here. If that skill is not installed, tell the user and ask which branch to create. Commit on the default branch only when the user has said, in this conversation, to commit there.

Read the output carefully. You must understand:

- Which files are modified, untracked, deleted, renamed, or already staged
- Whether staged and unstaged changes belong to the same logical unit
- What the code changes actually do, not just which files changed
- What recent commit message style the repository already uses

If there are **no changes to commit**, stop and tell the user. Do not create an empty commit.

---

## Step 2 — Look for a pull request template

Before drafting the commit message, check whether the repository provides a PR template in `.github/`.

Look for these common locations:

```text
.github/pull_request_template.md
.github/PULL_REQUEST_TEMPLATE.md
.github/PULL_REQUEST_TEMPLATE/*.md
```

If there is no PR template in this repo, skip the rest of this step and take the commit style from the recent history in Step 1.

If a PR template exists:

- Read it before writing the commit message
- Treat it as the source of truth for the kind of context reviewers expect
- Reuse its categories when deciding what details belong in the commit body or your final summary

At minimum, extract and keep track of any sections about:

- Summary
- Type of change
- Related issues or tickets
- Testing
- Database or migration changes
- Deployment notes
- Breaking changes

Do **not** paste the whole PR template into the commit message. Instead, use it to shape the message and the final report back to the user.

---

## Step 3 — Identify what belongs in this commit

Before staging anything, review the working tree for risky or accidental files. **Ask the user before including** anything that looks suspicious or unrelated.

Always flag:

- `.env`, `.env.*`, credential files, tokens, private keys, or anything that looks secret
- Large binaries or generated artifacts such as `dist/`, `coverage/`, `build/`, `*.map`
- Lockfile-only changes with no corresponding dependency manifest change
- Formatting-only noise mixed into a logic change
- Unrelated files that do not belong to the same logical commit
- Deletions or renames that were likely accidental

Notes:

- `.env.example` may be safe to commit if it is clearly intended and contains no secrets
- Do not automatically unstage or revert user work you did not create
- If the intent is ambiguous, ask instead of guessing

---

## Step 4 — Stage files explicitly

**Never run `git add -A` or `git add .`** because they can include unintended files.

Stage only the files that belong in this commit:

```bash
git add <file1> <file2> ...
```

Examples:

```bash
git add src/users/user.service.ts src/users/dto/create-user.dto.ts
git add prisma/schema.prisma prisma/migrations/20260407_add_user_flags/
```

If some files are already staged but do **not** belong in the commit, unstage only those files carefully before continuing.

After staging, re-run:

```bash
git diff --staged
```

Do not commit until the staged diff matches one clear, reviewable change.

---

## Step 5 — Draft the commit message

Use Conventional Commits unless the repository clearly uses a different enforced style.

### Format

```text
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

### Rules

**Type** — pick the best fit:

| Type       | Use when …                                      |
| ---------- | ----------------------------------------------- |
| `feat`     | adding a new feature                            |
| `fix`      | fixing a bug                                    |
| `refactor` | restructuring code without changing behaviour   |
| `perf`     | improving performance                           |
| `revert`   | reverting a previous commit                     |
| `docs`     | documentation only                              |
| `test`     | adding or updating tests                        |
| `chore`    | maintenance, config, tooling                    |
| `ci`       | CI/CD configuration                             |
| `build`    | build system or dependency pipeline changes     |
| `style`    | formatting or whitespace with zero logic change |

**Map PR template language to commit types when helpful:**

- Bug fix -> `fix`
- New feature -> `feat`
- Breaking change -> usually `feat!` or `fix!`
- Documentation update -> `docs`
- Refactoring -> `refactor`
- Performance improvement -> `perf`
- Test updates -> `test`

**Scope**:

- Optional but recommended
- Must be **kebab-case**
- Keep it specific: `auth`, `expenses`, `sentry-config`, `prisma`

**Subject**:

- Must not be empty
- Start lowercase
- Use an imperative, concise description
- Keep the first line at **100 characters or less**
- Do not end with a period

**Body**:

- Explain **why** or **impact**, not a file-by-file changelog
- Wrap lines at about 72 characters
- Include relevant reviewer context from the PR template when useful
- Mention testing when it materially helps future reviewers
- Mention database or migration implications if they exist

**Footer**:

- Use for issue references, tickets, or breaking changes when applicable
- Example: `Closes #123`
- Example: `Refs: TICKET-E883`
- Example: `BREAKING CHANGE: refresh tokens now require device binding`

### Examples

```text
feat(course-reviews): add average rating to course response
```

```text
fix(auth): prevent token refresh after account deletion

Reject refresh requests for deleted accounts so tokens cannot be
minted after an account is disabled.
```

```text
feat(payments)!: verify webhooks with the v2 signature scheme

Move webhook verification to the v2 signature scheme and remove the
v1 fallback.

BREAKING CHANGE: v1 webhook signatures are no longer accepted
```

---

## Step 6 — Validate the message against the staged change

Before committing, sanity-check the message:

- Does the type match the actual change?
- Is the scope accurate?
- Does the body capture the important reviewer context?
- If a PR template exists, does the message/body reflect the relevant sections?
- If the change affects DB, tests, or deployment, is that clear somewhere?

If the staged diff contains multiple unrelated changes, stop and split the commit instead of forcing one message to cover everything.

---

## Step 7 — Commit safely

Prefer a HEREDOC so multi-line messages are preserved exactly:

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<optional body>

<optional footer>
EOF
)"
```

Rules:

- Never append `Co-authored-by:`, AI attribution, or `Made-with: Cursor`
- Never use `--no-verify` or any other way around a hook
- If a hook or a guard stops the commit, follow the next section

---

## If a guard or a git hook blocks you

A commit or push can be stopped by the repository's git hooks (pre-commit, commit-msg, pre-push) or by an agent guard. The `guard-hooks` skill installs guards that block `--no-verify`, attribution lines, staged secrets and commit subjects that are not Conventional Commits, and that ask before a commit on the default branch.

1. Read the message. It names what was blocked and why.
2. Fix the cause: reword the subject, remove the attribution line, unstage the secret, fix the lint or test failure.
3. Run the same command again, as a new attempt.

Never bypass the block: no `--no-verify`, no `-n` on a commit, no `HUSKY=0`, no changed hooks path, and no edit to hook or guard config to get past it. If you think the block is wrong, tell the user what was blocked and why you think so, and let them decide. Switching a guard off is their call.

---

## Step 8 — Verify after commit

Run:

```bash
git status --short
```

If commitlint is available or the repository uses it, also run:

```bash
echo "<your message>" | npx commitlint
```

Confirm:

- The commit succeeded
- The working tree is in the expected state
- No unintended files were included

---

## Step 9 — Report back to the user

After the commit, give a concise summary that includes:

- The final commit message
- The commit hash
- Whether hooks or tests ran successfully
- Any important follow-up risks or manual steps

If a PR template was found, structure your summary using the most relevant template sections, such as:

- Summary
- Type of change
- Testing
- Database changes
- Deployment notes
- Related issues or tickets
