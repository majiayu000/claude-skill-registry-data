---
name: kanso-commit
description: Use when the user asks to commit changes, stage their work, write commit messages, or split the working tree into logical commits.
argument-hint: "[optional: scope hint or message style]"
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git reset *)
---

# kanso-commit

Splits the working tree into logically atomic commits and writes messages that answer *why* rather than *what*. Detects and matches the repo's existing convention.

The principles from `kanso-principles` apply. Messages earn their place the same way code does.

## The atomic unit

An atomic commit is one logical change. Not one line, not one file — one thought. The test: can the commit be described in a single short imperative sentence without using "and"?

Each atomic commit must be:

- **Independently revertable.** Reverting it doesn't cause collateral damage.
- **Independently cherry-pickable.** It can move to another branch cleanly.
- **Stable.** Tests pass (or at least don't newly fail) at this commit.
- **Single-concern.** Refactor and feature are separate commits, always. Formatting and logic are separate commits.

Over-atomising is a real failure mode. A three-line bug fix does not need three commits.

## Before doing anything

1. **Check the status.** `!git status --short` and `!git diff --stat` to see what's staged and unstaged.
2. **Detect the convention.** `!git log -n 30 --oneline` and read 3-5 recent commits in full. The repo's existing style wins over any default.
3. **Detect the tooling.** Look for `commitlint.config.*`, `.commitlintrc*`, `cz-config*`, `package.json` scripts mentioning `commit`. These hard-constrain the format.

## Convention detection

The repo's commit history dictates the format. In priority order:

1. **commitlint config present** → use whatever it enforces. No exceptions.
2. **Conventional Commits pattern in recent history** (`feat:`, `fix:`, `chore:`) → match it.
3. **Custom scoped pattern** (`[Component] subject`, `subsystem: subject`, `Fixed #NNNNN --`) → match it exactly. Don't modernise.
4. **Plain imperative subjects with no prefix** → match that. Don't introduce prefixes.
5. **No clear pattern, fewer than 10 commits in history** → use Conventional Commits as a sensible default and tell the user.

Don't impose a new convention onto an existing repo. If the history is messy, match the least-bad recent pattern rather than inventing a new one.

Django uses past tense (`Fixed #NNNNN --`). Linux kernel uses `subsystem: summary`. React uses `[Component] description`. All valid. All match-what's-there.

## Splitting the working tree

If multiple logical changes are staged or unstaged together:

1. **List them.** Show the user: "I see three logical changes — a typo fix in `README.md`, a new `getUser` endpoint in `src/api/user.ts`, and a refactor of the auth middleware. Split into three commits?"
2. **Get confirmation before splitting.** The user decides the granularity.
3. **Use `git add -p` or `git add <file>` to stage each unit.** Never bulk-stage with `git add .` when splitting.
4. **Commit each unit with its own message.** One message per logical change.

If the working tree is a single logical change, stage and commit directly.

## The seven rules for the message

1. Subject and body separated by a blank line.
2. Subject under 50 chars. Hard limit at 72.
3. Capitalise the subject (unless the convention is Conventional Commits lowercase).
4. No period at the end of the subject.
5. Imperative mood: "Add X", "Fix Y", "Remove Z". Never past tense (unless the repo is Django-style).
6. Body wrapped at 72 chars.
7. Body explains *what* and *why*, not *how*. The diff shows how.

Imperative test: "If applied, this commit will _____". Fill the blank with the subject. If it doesn't grammatically fit, rewrite.

## Body content

Body is optional for trivial changes (typo, formatting, rename of a local variable). Required for:

- Any bug fix (explain the bug, its impact, the fix)
- Any architectural change (explain the reasoning, alternatives considered, tradeoffs)
- Anything that changes behaviour visible to users or API consumers
- Anything removing code that isn't obviously dead

Good body content:

- What problem existed before this commit
- Why this approach was chosen over alternatives
- What side effects or unintuitive consequences exist
- Links to issues, RFCs, or prior discussion

Bad body content:

- Line-by-line walkthrough of the diff
- Restatement of the subject in longer form
- Filler like "This commit does X" (just say X)
- "As per the user's request" or similar AI artefacts

## Breaking changes

If the change breaks an API:

- Conventional Commits: `feat(api)!: remove deprecated endpoint` + `BREAKING CHANGE:` footer
- Other conventions: use whatever the repo's history shows for breaking changes. Usually explicit in the body.

Always explain the migration path in the body.

## Trailers and references

- `Fixes: #NNN` or `Closes: #NNN` — link to issue trackers
- `Co-authored-by:` — when pairing or when the user names collaborators
- `Signed-off-by:` — if the repo uses DCO (check for `.gitsignoff` or CONTRIBUTING notes)

Don't invent trailers the repo doesn't use. Don't add `Co-authored-by: Claude` or any AI attribution unless the user explicitly asks for it.

## Writing from the diff

The message must answer what the diff cannot:

- Why was the change needed? (The diff shows what changed, not why.)
- What alternative was considered and rejected? (Often invisible in the code.)
- What business constraint, SLA, regulation, or downstream consequence is at play?
- What invariant is being preserved or established?

If the user hasn't explained any of this, ask before committing. A good commit message cannot be generated from the diff alone. AI-generated messages are consistently weak on *why* because *why* lives outside the code.

## The working process

1. Run `!git status --short` and `!git diff --stat`.
2. Detect the convention (history + tooling).
3. Identify logical groups in the working tree.
4. If more than one group, ask the user whether to split.
5. For each group:
   a. Stage the files/hunks.
   b. Draft the subject (imperative, under 50 chars, matching convention).
   c. If body is needed, draft it — ask the user for the *why* if it's not obvious.
   d. Show the user the full message before committing.
   e. Commit on approval.
6. Report: show the final `git log -n <N> --oneline` for what was committed.

## Output format

Before any commit, show:

```
Proposed commit 1 of 2:

  fix(auth): reject tokens older than 24h

  The previous implementation only checked the signature, not the
  issuance time, allowing replay attacks with captured tokens.
  The 24h window matches the session timeout in src/config/auth.ts.

  Fixes: #312

Files: src/auth/verify.ts, src/auth/verify.test.ts

Approve? (y/n/edit)
```

Wait for the user's approval before running `git commit`.

## What this skill never does

- Force-push, rebase, or rewrite public history.
- Amend a commit that's been pushed to a shared branch.
- Commit code that the user hasn't seen and approved (always show the message first).
- Invent a *why* the user didn't provide. Ask.
- Run linters, formatters, or tests as part of committing. Those are pre-commit hooks' job.
- Add AI co-authorship attribution unless explicitly requested.
- Use emoji unless the repo's recent history uses emoji.

## Failure modes to avoid

- "fix: bug" and similar empty messages that pass linting but say nothing.
- Messages that restate the diff ("Changed X constant from 5 to 10").
- Tense inconsistency (imperative in some, past tense in others).
- Massive commits that touch five unrelated concerns.
- Over-atomised commits that fragment a single thought.
- Introducing Conventional Commits into a repo that never used it.
- Silently bulk-staging with `git add .` when splits were warranted.
