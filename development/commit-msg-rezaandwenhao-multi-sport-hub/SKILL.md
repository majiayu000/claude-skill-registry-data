---
name: commit-msg
description: Use when someone asks to draft a commit message for staged changes, write a commit message, summarize what's staged, or review staged diffs before committing.
---

# Commit Message Drafting

Produces a single Conventional Commits message summarizing **all staged changes**.
Draft only — never runs `git commit`.

## Context

Run from the repo root. The skill needs the current git index state:

- `git status --short` — what's staged vs. unstaged vs. untracked
- `git diff --cached --stat` — summary of staged changes
- `git diff --cached` — full staged diff (the source of truth)

## Steps

1. **Verify staged changes exist.**
   Run `git status --short` and `git diff --cached --stat`.
   - If the index is empty (nothing staged): **stop here.** Tell the user nothing is staged, show `git status --short`, and suggest running `git add` first or using `git diff` for unstaged work. Do not fabricate a message.
   - If both staged and unstaged changes exist: focus **only** on staged. Briefly note that unstaged files are excluded.

2. **Read the staged diff.**
   Run `git diff --cached`. If it's very large (roughly >400 lines), read `--stat` plus a sample of hunks and rely on file paths + line counts to understand the change. Never dump the full diff back at the user.

3. **Classify the change type** (Conventional Commits). Pick the type that best matches the dominant change in the staged set:
   | Prefix | When |
   |---|---|
   | `feat` | new feature / endpoint / field / capability |
   | `fix` | bug fix |
   | `refactor` | behavior-preserving restructuring |
   | `docs` | documentation only |
   | `test` | tests only |
   | `chore` | build config, dependency, tooling (e.g., removing the maven wrapper) |
   | `perf` / `style` / `ci` / `build` / `revert` | when clearly the dominant change |

   If the batch mixes types, the summary line takes the most significant type; secondary types are named in the body bullets.

4. **Write the summary line.**
   - Format: `<type>: <summary>` (e.g., `feat: add local MySQL datasource profile`)
   - Imperative mood ("add", "fix", "remove" — not "added", "adds").
   - Keep it under ~72 characters, no trailing period.
   - If the staged change is **breaking** (removed config key, changed API/URL, changed table schema), use `<type>!:` and add a `BREAKING CHANGE:` note in the body.

5. **Add a body when it earns it.** If the staged set is multi-faceted (>1 theme), touches non-obvious areas, or is breaking, add a blank line then bullets grouping by theme, naming key files:
   ```
   feat: add local MySQL profile and drop maven wrapper

   - add mysql-connector-j dependency and a `mysql` datasource profile in application.yml
   - remove broken mvnw/mvnw.cmd wrapper; docs now use system `mvn`
   - stop auto-seeding NBA/EPL defaults; add idempotent `/api/dev/seed` + scripts/seed-defaults.ps1
   ```
   Skip the body for tiny/obvious single-file changes.

6. **Present the result.** Output the message in a fenced code block, copy-paste ready, followed by the equivalent command (using multiple `-m` flags so the message is quoted safely):
   ```
   git commit -m "feat: add local MySQL profile and drop maven wrapper" -m "- add mysql-connector-j ..."
   ```
   Ask the user if they'd like the summary tightened, split differently, or a different type. **Do not run `git commit`** — this skill drafts only.

## Notes

- Describe **only** what the staged diff actually shows. Never invent changes, features, or intent.
- Ignore unstaged changes, untracked files, and commits entirely — the message must match exactly what the index contains.
- Summary line is imperative, lowercase first word after the colon (unless a proper noun), no trailing period.
- For binaries or large generated files, rely on the file path and `--stat` — don't try to paraphrase content you can't see.
- If a type is ambiguous, prefer `chore` for tooling/config and ask the user rather than guessing wrong.
- Works on any OS; commands are plain `git`, run from the repo root.
