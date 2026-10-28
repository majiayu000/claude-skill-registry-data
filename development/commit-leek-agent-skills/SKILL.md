---
name: commit
description: Commit the work done in this session, skipping files a parallel session also touched.
disable-model-invocation: true
allowed-tools: "Bash(git status *) Bash(git diff *) Bash(git add *) Bash(git commit *) Bash(git show *) Bash(git log *) Bash(git apply --cached *)"
model: sonnet
effort: medium
---

# Commit

Commit **only what you changed in this session**. Other sessions may be working in the same
repo at the same time; that is expected, and none of their work is yours to commit.

## Process

1. **List your files.** From this conversation, write down every file *you* created, edited, or
   deleted. Changes under `.claude/agent-memory/` are always yours too, whoever wrote them: they are the notes of agents with `memory: project`, not a parallel session's work in progress, so they ride along in your commit (`git add -- .claude/agent-memory`). If you touched nothing, say so and stop.
2. **Check the tree.** Run `git status --porcelain`. Anything not on your list belongs to someone
   else, ignore it completely.
3. **Drop the overlaps.** For each of your files, `git diff -- <path>` (`git diff --cached` too if
   it is already staged). If it contains changes you did not make, leave that file out, the other
   session will commit it. If a file mixes your hunks with foreign hunks, stage only yours: `git add -p -- <path>`
   needs an interactive terminal, so where the shell has none (Claude Code's Bash, most agent
   harnesses), write your hunks to a patch (`git diff -- <path> > "$TMPDIR/mine.patch"`, then
   delete the foreign hunks from it) and `git apply --cached "$TMPDIR/mine.patch"`. Never include a
   foreign hunk because it is small. Note which files you skipped.
4. **Commit by path, without touching the index.** Use
   `git commit --only -m "<subject>" -- <path> <path> …` (options before the `--`). `--only` commits exactly the named paths
   and ignores whatever another session has already staged, so a foreign `git add` can never ride
   along. Never `git add -A`, `git add .`, or `commit -a`. For a partially staged file from step 3,
   `git commit -m "<subject>" -- <path>` after staging your hunks instead.
   **New files are the exception:** `--only` silently skips untracked paths, so `git add -- <new-path>`
   each file you created first, then include it in the same `--only` list. Check
   `git status --porcelain` afterwards; a `??` line for one of your files means it was skipped.
5. **Subject.** Conventional Commits: `type(scope): summary`: imperative mood, lowercase,
   no trailing period, under 72 chars. Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`,
   `perf`, `build`, `ci`. Scope optional. Add a short body only when *why* is not obvious from the
   diff. No attribution or co-author trailers.
6. **Report.** One line: the commit subject, the short SHA, and any files you deliberately left out
   and why. Do not push unless asked.

## Guardrails

- **Commit to the current branch, whatever it is.** Never switch, create, or suggest a branch, 
  not even when the current branch is `main`/`master`. No `git checkout`, `git switch`, `git branch`.
- One session's work, one commit. Do not amend, rebase, or touch existing history.
- If the changes are genuinely two unrelated things, make two commits, still your files only.
- Never `git stash`, `git checkout --`, or `git reset`: a parallel session's uncommitted work is
  unrecoverable if you discard it.
- Need a pre-change baseline of a file? Copy it aside and `git show HEAD:<path> > <path>`, run
  what you need, then restore the copy. A scoped stash plus immediate pop is still a stash.
