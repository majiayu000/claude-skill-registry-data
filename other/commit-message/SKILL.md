---
name: commit-message
description: >
  Use ANY time the user signals they want to commit staged changes — including
  bare "commit", "/commit", "commit this", "commit these changes", "let's commit",
  "make a commit", "git commit", "write a commit message", "make a conventional
  commit", "use conventional commits", or any equivalent phrasing in context
  (e.g., right after staging files, "ready to commit", "okay ship it").
  Composes a Conventional Commits message with a gitmoji prefix: reads the
  staged diff, decides type, scope, emoji, subject, body, and footer using the
  rubrics in this file, shows one assembled message in a fenced block, and
  commits after a single yes/no confirmation. It writes the commit message
  only — NOT other prose about the staged changes: not PR/MR descriptions,
  not release notes, not changelogs or summaries. Also do NOT use for
  questions *about* git or *about* conventional commits, amending, rebasing,
  cherry-picking, reverting/undoing commits, or viewing log history.
---

# Commit Message Generation

Read the staged diff, decide every field yourself using the rubrics below, and surface **one** assembled message for a single yes/no confirmation. Don't prompt field-by-field (a GUI extension can afford that; a chat turn can't), and don't short-circuit to a bare `git commit -m "fix stuff"` — if this skill loaded, run the full flow and never bypass hooks.

## Repo defaults

```text
Format:           <type>(<scope>): <emoji> <subject>
Emoji style:      Unicode glyph (e.g. 🐛 not :bug:)
Scope default:    none (include only if the diff points clearly at one)
Co-Authored-By:   off (this repo's history doesn't use the trailer)
Body default:     skip unless the diff is non-trivial (>~10 lines, multi-file, or non-obvious why)
Footer default:   skip; reserve for `BREAKING CHANGE:` or `Closes #N`
Subject limits:   warn at >50 chars; hard cap at 72
Hooks:            gitleaks runs pre-commit; do not bypass on failure
```

These are bootstrap defaults from this repo's history. In a different repo, re-detect during preflight (Phase 1 step 5) and adjust silently — observed in-repo history wins.

## When to ask the user

Only stop and ask in these cases — otherwise decide and continue:

1. **Nothing staged.** Offer to stage by filename (never `git add -A`/`-u`/`.`).
2. **On `master`, `main`, or detached HEAD.** Offer to create a new branch, move the staged changes there, then resume on that branch. Refuse to commit directly to master/main.
3. **Suspicious staged content** (`.env*`, `*.key`, `*.pem`, files ≥1 MB, secrets in diff). Show the offending file/line, ask whether to unstage or proceed.
4. **Genuinely ambiguous type or emoji choice** — i.e., two options are equally defensible from the rubric and the choice changes how a reader will interpret the commit (e.g., `feat` vs `fix` when the change adds a new code path that also corrects bad behavior). State the options and the tradeoff in one line, then wait. If the rubric picks a clear winner, do not ask.
5. **Final assembled message.** Always show the complete commit message in a fenced block and wait for explicit confirmation before running `git commit`.

Specifying a type, scope, subject, or complete message in the invoking request
does not waive step 5. Only a new affirmative user response after the assembled
message is shown authorizes `git commit`.

## Phase 1 — Preflight (silent unless something fails)

Run these checks in parallel where possible. Surface results to the user only if one fails or trips an "ask" condition above.

1. **Staged changes.** `git diff --cached --stat`. If empty, follow ask-condition #1.
2. **Branch.** `git rev-parse --abbrev-ref HEAD`. If `master`, `main`, or `HEAD` (detached), follow ask-condition #2. Any other branch name is fine — feature/, fix/, chore/, bare names, prefixed names, all acceptable.
3. **Stage summary.** `git diff --cached --name-status` + `--stat`. Flag suspicious paths per ask-condition #3.
4. **Sensitive-content sniff.** Scan the whole staged diff for likely-live credentials, not just the top:

   ```bash
   git diff --cached | grep -E -i \
     '(password|secret|api[_-]?key|BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}|aws_secret_access_key)[[:space:]]*[=:]' \
     | head -20
   ```

   Any hit → follow ask-condition #3. The `[=:]` anchor avoids false positives on the bare word "password" appearing in prose or comments.
5. **Repo-convention sniff.** `git log --pretty=%s -20` and `git log -20 --format=%B`:
   - Count Unicode glyphs vs `:code:` in subjects → output emoji style.
   - Count `(scope)` parens → scope-default on/off.
   - Look for `Co-Authored-By:` → trailer default.

   If detected defaults differ from the "Repo defaults" block above, prefer the detected ones; note the mismatch in the final-confirmation summary but don't block on it.

### Moving off master/main

If the branch check trips, propose a branch name derived from the staged diff (e.g., from the most-changed top-level dir, or the subject about to be drafted). Confirm the name. Record the staged diff hash, create the branch directly, and verify that the staged diff is unchanged:

```bash
git diff --cached --binary | git hash-object --stdin
git switch -c <new-branch>
git diff --cached --binary | git hash-object --stdin
git status --short
```

`git switch -c` preserves staged, unstaged, and untracked work because the new
branch starts at the same commit. Require the two hashes to match. If branch
creation fails or the hashes differ, reproduce the full error or mismatch and
stop. Do not stash, commit, or retry automatically. Resume preflight only after
the branch and staged-diff postcondition checks pass. Don't commit on the original
branch under any circumstances.

## Phase 2 — Decide every field

Work through these in order using the rubrics below and produce a single assembled commit message. No per-field prompts.

### Type rubric

Paths below are illustrative — match on the *signal* (only tests touched, mostly renames, new behavior), not the exact paths, so this generalizes across repos.

| signal in diff                                                                                              | type                |
|-------------------------------------------------------------------------------------------------------------|---------------------|
| Only test files touched (e.g., `tests/**`, `**/*_test.go`, `**/*.spec.ts`)                                  | test                |
| Only `**/*.md`, `doc/**`, and the file is genuinely docs (not operational instructions)                     | docs                |
| Only CI config (`.github/workflows/**`, `.gitlab-ci.yml`, `.circleci/**`)                                   | ci                  |
| Only build configs, dependency manifests (`pyproject.toml`, `package.json`, `Dockerfile`), or setup scripts | build               |
| Mostly `R` status (renames/moves) in `git diff --cached --name-status`                                      | refactor (emoji 🚚) |
| New file with new behavior; new template/role/module; new agent/skill definition                            | feat                |
| Modifies existing behavior to fix wrong output, error, regression                                           | fix                 |
| Reorganization without behavior change                                                                      | refactor            |
| Speed / resource-use improvement with no behavior change                                                    | perf                |
| `git revert`-style change (HEAD~1 is a "Revert ..." or message starts with `revert:`)                       | revert              |
| Whitespace / formatting only                                                                                | style               |
| Catch-all                                                                                                   | chore               |

Operational `.md` files (skills, agent instructions, runbook-style READMEs) lean **feat**/**chore**, not **docs**. The `docs` type is reserved for genuine documentation *of* something else (READMEs about code, architecture notes, charter docs).

### Scope rubric

Default: **omit**. Include a scope only if all the staged paths cluster under one directory that maps to an obvious name. Spans multiple top-level dirs → no scope. If repo history overwhelmingly skips scope (detected in Phase 1 step 5), only include if the diff really demands it.

### Emoji rubric

Pick the contextual emoji if one fits, else the type default:

- **feat** ✨ — alternates: 🎉 (initial commit), 🚸 (UX), 🏗️ (architecture), 🧑‍💻 (DX tooling / `.claude/` changes)
- **fix** 🐛 — alternates: 🚑️ (critical hotfix), 🩹 (non-critical/one-liner), 🔒️ (security: auth, secrets, CVE)
- **docs** 📝 — alternates: 💡 (in-code comments), 📄 (license)
- **style** 🎨 — alternates: ✏️ (typo)
- **refactor** ♻️ — alternates: 🚚 (mostly `R` renames/moves), 🔥 (deleted code dominates), ⚰️ (dead code removal)
- **perf** ⚡️
- **test** ✅ — alternates: 🧪 (failing test added), 📸 (snapshots)
- **build** 👷 — alternates: 📦️ (compiled output), ⬆️/⬇️/➕/➖/📌 (only lockfile/manifest changes)
- **ci** 💚 — alternates: 👷 (build system)
- **chore** 🔧 — alternates: 🔨 (dev scripts), 🙈 (.gitignore), 🏷️ (types)
- **revert** ⏪️

For the full glyph list and `:code:` mapping (used if the repo-convention sniff in Phase 1 detects `:code:` style, or if the user requests a different emoji by name), see `references/gitmoji.md`.

**Emoji glyph integrity:** several glyphs include a U+FE0F variation selector that forces emoji-style rendering (🚑️, 🔒️, ♻️, ⚡️, ✏️, ⏪️, 🏷️, 📦️, 🗑️, 🔍️). Copy the glyph as-is — do not strip the variation selector or these will render as monochrome text on some clients.

### Subject rules

- Imperative mood ("Add X", not "Added X").
- No trailing period.
- Capitalize the first word.
- Do not repeat the type ("Add X", not "feat: Add X").
- Target ≤50 chars. Warn (in the final summary) at 50, hard-refuse at 72.
- The diff is the source of truth — describe the change, not the motivation.

### Body rules

Include a body only if:

- Diff is ≥10 lines changed, **or**
- Spans multiple files, **or**
- The *why* is non-obvious from the diff (constraint, prior incident, ticket context).

When included: 1–3 sentences, wrapped at 72 cols, focused on *why*, not *what*.

### Footer rules

Include only when:

- Diff includes a breaking change (public API change, schema/migration, removed config key) → `BREAKING CHANGE: <one-line description>`.
- User mentioned a ticket number in conversation → `Closes #N` or `Refs #N`.

## Phase 3 — Confirm and commit

1. **Assemble:**

   ```text
   {type}({scope}): {emoji} {subject}

   {body}

   {footer}
   ```

   Drop `(scope)` if no scope. Single space between emoji and subject. Blank line before body and before footer; omit either block entirely if empty. No `Co-Authored-By:` trailer unless repo-convention sniff demanded it.

2. **Show the full message** in a fenced code block. Note any caveats inline: "subject is 58 chars (over 50 warn line)", "convention sniff disagrees with repo defaults — using detected style". Ask once: confirm or revise?

3. **On confirm, commit via heredoc:**

   ```bash
   git commit -m "$(cat <<'EOF'
   <type>(<scope>): <emoji> <subject>

   <body>

   <footer>
   EOF
   )"
   ```

   Single `git commit` call. Do not stage anything new at this step.

4. **Verify** with `git log -1 --format=%B` so the user sees what actually landed (including any hook-injected trailers).

5. **If the user revises** something on the confirmation step, apply the change and re-show the full message. Don't restart the flow.

## Failure modes

Nothing staged, on master/main, and suspicious staged content are decision gates — handle them per *When to ask the user*. The rest:

- **Hook failure (gitleaks etc.).** Never offer, suggest, ask about, accept, or execute a hook bypass, even when the user explicitly requests one. Don't retry with `--no-verify` and don't `--amend` (nothing to amend). Run no more tools. Respond in exactly this order:
  1. Reproduce the full hook output verbatim in a `text` fenced block.
  2. Write exactly: `The commit did not land.`
  3. Write exactly: `Fix the hook's root cause, re-stage the intended files, and invoke the commit-message skill again.`
  End the response immediately after step 3. Do not omit, merge, reorder, or add to these elements.
- **User abandons mid-flow** ("never mind", "cancel"). Stop without committing; leave staging untouched.
- **User asks for `--amend`.** This skill only creates new commits. Direct them to `git commit --amend` manually, or `git reset --soft HEAD~1` + re-invoke.
- **Subject exceeds 72 chars.** Hard refuse. Trim or move detail to the body before confirming.
- **Multi-line subject pasted.** Treat the first line as the subject; move everything after it into the body.

## Out of scope

No commitlint integration (no config in this repo — the rubrics here are the contract; revisit if `.commitlintrc*` lands). No persistent scope cache — re-derive from the diff each time. No `[skip ci]`, no interactive `git add -p` (stage first), no amend/rebase, and no bypass flags (`--no-verify`, `--no-gpg-sign`, `-n`).
