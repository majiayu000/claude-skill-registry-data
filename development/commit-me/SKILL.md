---
name: commit-me
description: Use whenever the user asks to commit, save changes, prepare a commit, wrap up work, or finish up a chunk of code — even if they don't say the word "commit" explicitly. Formats code if a formatter is configured, generates a conventional commit message, stages the relevant files, and commits — unless the user says not to commit, in which case it stops at the staged message for review.
---

# Commit

This skill commits by default. Generate the message, stage the right files, and land the commit — unless the user has said they don't want it committed this time, in which case stop after staging and show them the message to run themselves. Either way, always print the full commit message in your response. A sibling covers an adjacent job:

- **`aa-commit-clarity`** — advisory only. Use first when the diff feels mixed, to decide whether the changes belong in one commit or several.
- **`land-pr`** — user-invoked only. Takes the reviewed branch from ready to merged: history cleanup, merge-strategy verdict, the merge itself.

## Workflow

### Step 0: Format the code

If formatting already ran *after the last code edit* in this conversation (e.g. the previous step ran the formatter or a linter with `--fix`), skip this step — rerunning is redundant. If any code was edited after the last format run, run it again.

Otherwise, detect the project's formatter and run it. Check in this order and use the first match:

- **Node** — if `package.json` exists and has a `format` script: run it via the matching package manager (`pnpm format` if `pnpm-lock.yaml`, `yarn format` if `yarn.lock`, `bun run format` if `bun.lockb`, otherwise `npm run format`).
- **Rust** — `cargo fmt` if `Cargo.toml` exists.
- **Go** — `gofmt -w .` if `go.mod` exists.
- **Python** — `ruff format .` if `pyproject.toml` or `ruff.toml` exists; otherwise `black .` if it's available.
- **Otherwise** — skip silently.

If a formatter is configured but the run fails (not just missing), briefly tell the user it failed and continue. Don't block the commit on formatter trouble.

### Step 1: Review changes

Run `git diff` and `git status` to understand everything staged and unstaged.

Before staging, scan for files that probably shouldn't be committed: `.env*`, `credentials.json`, `*.key`, `*.pem`, `*.p12`, secret-looking paths, large binaries, build artifacts. If any are present and unignored, surface them to the user and confirm before including them.

Leave planning, review, critique, and investigation docs out of the commit — plans, design docs, review reports, analysis write-ups, research and debugging notes. Include them only when the user explicitly asks for them in this commit. If you leave any out, say so in one line.

After the secrets scan, do a quick read of the diff for commit cohesion: does this span multiple independent concerns? Common signals — a refactor mixed with an unrelated behaviour change, formatting noise mixed with semantic edits, an obvious bugfix tucked into a feature commit, two changes that just happen to be sitting in your working tree together. If you spot a mix, pause before generating the message and surface a one-liner:

> "This diff looks like it might benefit from `aa-commit-clarity` before I write the message. Want me to run it, or just commit as-is?"

If the user says "just commit" (or anything that means proceed), don't push back further — they may have intentional WIP, end-of-day snapshots, or other legitimate reasons to commit a mixed diff. If the diff reads as cohesive, skip this check entirely and proceed straight to message generation.

### Step 2: Create the commit message

Use this conventional-commit shape. Treat it as a **maximum, not a minimum** — size the message to the change. A typo fix is one line. A multi-file refactor may need bullets and a paragraph. Use what genuinely adds information.

```
<type>(<scope>): <short description>

- <key technical change, if it adds info the diff doesn't already show>
- <another, only if useful>

<Optional paragraph explaining the WHY: what problem this solves and how>
```

Rules:

- Conventional types: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`.
- Scope is short and concrete (`auth`, `api`, `ui`, `seo`, etc.). Omit scope if there isn't a meaningful one.
- Short description: imperative mood, lowercase, no period.
- The body explains **why**, not what — the diff already shows what.
- **Do not** list modified files in the body. Git already tracks this via `git show --stat`, `git log --name-status`, and `git diff --stat`. Duplicating it goes stale and bloats history.
- **Do not** include `Co-Authored-By`, "Generated with…", or any other attribution footer.
- **Issue reference (optional):** if the issue number can be confidently determined — the user mentioned it in the conversation, or the branch name encodes it (`123-fix-login`, `fix/issue-123`, `feature/GH-123`) — add a final line `Refs #123` after the body, separated by a blank line. Always use `Refs`, never `Closes`/`Fixes` (issues are triaged and closed manually after implementation). If the number can't be confidently determined, skip this line silently — don't ask and don't guess.

For multi-line messages, prefer a HEREDOC when invoking `git commit -m` later, so newlines survive shell quoting:

```sh
git commit -m "$(cat <<'EOF'
feat(auth): add JWT refresh flow

- introduces /auth/refresh endpoint
- swaps in-memory session store for signed cookies

Refresh tokens were never rotated, so a leaked token stayed valid
until expiry. The new flow rotates on every refresh.
EOF
)"
```

### Step 3: Stage and commit

Stage the files that belong to this commit (don't use `git add -A` — be specific so secrets and unrelated edits don't slip in).

Then commit, using the HEREDOC form so newlines survive shell quoting:

```sh
git commit -m "$(cat <<'EOF'
<your message here>
EOF
)"
```

If the user said they don't want it committed this time, stop after staging and hand them the ready-to-run command instead.

Either way, print the full commit message in your response so the user always sees exactly what landed (or what's queued).

## Comment Guidelines

This section lives in the skill rather than only in a project's `CLAUDE.md` because this skill is used across many projects, and not all of them document comment conventions.

When adding comments to code, focus on explaining **why** code works the way it does, not what changed.

Good comments explain:

- Complex logic or algorithms
- Non-obvious design decisions
- Business rules or constraints
- Purpose of functions/classes
- Edge cases being handled

Comments should help someone understand the code 6 months later, not track edit history.
