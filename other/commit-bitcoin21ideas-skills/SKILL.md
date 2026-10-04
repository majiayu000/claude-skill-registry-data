---
name: commit
description: Multi-step git commit workflow. Gathers state, triages sensitive content and secrets, groups changes into logical units, runs the project's test/lint gate, proposes a plan for approval, and commits with conventional messages and no AI attribution. Use when changes need to be committed — when the user says "commit", "/commit", or asks to commit staged or working-tree changes. Both user- and model-invocable.
license: MIT
metadata:
  version: "1.0.0"
  author: "bitcoin21ideas"
---

# Smart Git Commit

A careful, project-agnostic commit workflow: understand what changed, keep secrets out of history, verify the tree passes the project's gate, and write clean conventional commits — only after you approve the plan.

This skill is **both user- and model-invocable**: run it explicitly with `/commit`, or the model may start it when you express commit intent. It never commits without showing a plan and getting your approval (Step 6).

> This file is the generic template. It works as-is on any repo. To produce a leaner copy hard-wired to one project's gate, scopes, and conventions, see [tailoring.md](./tailoring.md) — that step bakes in the specifics and removes the detection prose. <!-- tailor:strip -->

## Step 1: Gather state

Run in parallel:

- `git status` (never `-uall`)
- `git diff --stat` (unstaged summary)
- `git diff --cached --stat` (staged summary)
- `git log --oneline -20` (recent history — the style reference for commit messages; if there are no commits yet, follow the format below)

If the user passed arguments via `$ARGUMENTS`, treat them as a hint for the commit message or scope.

## Step 2: Triage

- **Nothing to commit** (clean tree, nothing staged, nothing untracked): report "Nothing to commit." and stop.
- **Merge conflicts**: list the conflicted files and stop.
- **Sensitive files by name** — `.env`, `.env.*` (except `.env.example`), `*.pem`, `*.key`, `id_rsa*`, `credentials*`, `*secret*`, `**/secrets/**`. Never read, `cat`, `echo`, or otherwise print their contents. Warn the user, exclude by default, and only stage one if the user explicitly overrides. `.env.example` is the only env file safe to inspect. <!-- tailor:sensitive -->
- **Sensitive content scan** — for each staged or about-to-be-staged text file (especially `.md`, `.json`, `.yml`, and source files), grep the diff for secret-shaped strings:
  ```
  git diff --cached -U0 -- <file> | grep -iE '(BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|xox[baprs]-[A-Za-z0-9-]+|Bearer[[:space:]]+[A-Za-z0-9._-]{20,}|(api[_-]?key|secret[_-]?key|access[_-]?token|client[_-]?secret|password|passwd)[[:space:]]*[=:][[:space:]]*["'"'"']?[A-Za-z0-9/_+.\-]{8,}|postgres(ql)?://[^:]+:[^@]+@)'
  ```
  If anything matches, **do not print the matched value** when it looks like a real key, token, password, or connection string — report it as `<file:line — matched pattern>`. Then offer: (1) move the secret to an env var / ignored config (preferred), (2) replace the value with `<REDACTED>` (docs only, never source), or (3) override after explicit confirmation. A private repo is not a safe place for secrets — once committed, removal needs a history rewrite.
- **Generated / vendored artifacts** — `dist/`, `build/`, `node_modules/`, `target/`, `.next/`, `coverage/`, `playwright-report/`, `test-results/`, `.DS_Store`. Flag any that are staged or untracked and exclude them.

## Step 3: Respect staging intent

If the staged summary from Step 1 is non-empty:

- Read full diffs for staged files (`git diff --cached -- <file>`) to understand what they contain.
- If staged files clearly span unrelated concerns (e.g. a feature change mixed with a docs-only edit), flag it in the Step 6 proposal and offer to split. Do not split without the user's approval.
- If the user confirms commit as-is, honor that. Do not unstage or rearrange without explicit permission.
- Only analyze unstaged/untracked files for additional commits after resolving the staged unit.

If nothing is staged, analyze all changed and untracked files.

## Step 4: Analyze and group

Read full diffs for all changed files (`git diff -- <file>` / `git diff --cached -- <file>`). For binary files the Step 1 stat line is enough — skip the full diff. Group into logical commit units:

- Same area/topic together (e.g. a backend change plus the matching caller).
- Unrelated changes split into separate commits.
- Order logically: structural/renames first, then code, then docs, then meta (config, skills, scripts).
- One logical change = one commit.

## Step 5: Verify before committing (test/lint gate)

Run the project's gate on the working tree **before** proposing, and report the result in Step 6.

<!-- tailor:gate -->
Determine the gate by inspection (the tailored copy replaces this block with a concrete command):

- **Node** — read `package.json` scripts. Prefer a composite (`qa`, `check`, `verify`, `ci`); otherwise run whichever exist: `lint`, `typecheck` / `tsc --noEmit`, `test`.
- **Python** — `pre-commit run --all-files` if `.pre-commit-config.yaml` exists; else `ruff`/`flake8`, `mypy`, `pytest` as available; or `make test` / `make lint`.
- **Rust** — `cargo clippy` and `cargo test`.
- **Go** — `go vet ./...` and `go test ./...`.
- **Makefile** — `make check` / `make test` / `make lint` if present.
- If no gate is discoverable, say so in the proposal and skip it.

Scope: if the change is **docs/config only** (only `.md`, `docs/`, `.gitignore`, `.env.example`, or other non-executable files), **skip the gate** and say so ("no code changed, gate skipped").
<!-- /tailor:gate -->

Rules:

- Run the gate **once on the whole working tree**, not per planned commit — it verifies the exact state you are about to commit.
- If you already ran the gate earlier this session and nothing relevant changed since, reuse that result instead of re-running.
- Report only pass/fail counts and real failures — filter build/tool noise.
- **On failure: STOP. Do not commit.** Report which check failed (with the failing test/lint names), then offer (1) fix first (preferred) or (2) commit anyway only after an explicit user override. Never use `--no-verify` and never bypass a git `pre-commit` hook.

## Step 6: Propose the plan

Present:

- The Step 5 result (gate passed / skipped for docs-only / no gate found / failed-and-overridden).
- Number of commits and the rationale.
- For each commit: the files included and the proposed message.

Wait for explicit approval. If the user rejects or requests changes, revise and re-propose. If the user wants to skip a commit, drop it and proceed with the rest.

## Step 7: Execute

For each commit:

1. Stage specific files: `git add <file1> <file2> ...` (never `git add -A` or `git add .`).
2. Commit with a HEREDOC:

   ```bash
   # Single-line
   git commit -m "$(cat <<'EOF'
   type(scope): subject
   EOF
   )"

   # Multi-line
   git commit -m "$(cat <<'EOF'
   type(scope): subject

   - first change
   - second change
   EOF
   )"
   ```

3. Run `git status` to verify.

## Commit message format

```text
type(scope): lowercase subject, imperative mood, no period
```

- **Types**: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `build`, `ci`, `chore`, `style`, `revert`.
- **Scope** (optional): derive from project structure and recent `git log` — top-level dirs, package names, module names. <!-- tailor:scopes -->
- **Subject**: lowercase, imperative ("add X", not "added X"), no trailing period, max ~72 chars.
- **Body** (optional): bullet points for multi-change commits; a short paragraph for non-obvious changes.
- **No em dashes** in commit messages — they read as an AI tell. Use commas, colons, or parentheses to list related items: `feat(auth): login, logout, session refresh`.
- **Never** add a `Co-Authored-By` trailer or mention Claude, Anthropic, or any AI agent anywhere in the message.
- **Never** use `--no-verify` or skip hooks.

Match the style of the recent commits from Step 1. For the very first commit in a repo, use `chore: initial commit`.
