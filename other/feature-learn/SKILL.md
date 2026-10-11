---
name: feature-learn
description: Automatic per-feature lessons-learned promotion at session close, scoped mirror of /learn.
---

# Feature Learn

Runs automatically at the end of a feature command's **Session close (mandatory)** phase — no user
confirmation, same footing as the mandatory review handoff, because it only writes local docs. It is
a scoped mirror of `/devteam:learn`'s mechanics (`commands/learn.md`), not a replacement: `/learn`
stays the manual, full-session pass; this fires every time a feature closes, so knowledge compounds
feature-to-feature instead of aging inside `session-summary.md` until someone remembers to run `/learn`.

## Scope Derivation

The canonical answer to "what did this session, branch or worktree touch". It is used here and by
`/devteam:learn --auto` (`commands/learn.md`). Resolve top-down and stop at the first match:

| # | Condition | Touched set |
|---|---|---|
| 1 | `.dev-team-agents/.worktree-session` reads `worktree=yes branch=<base>`, **or** the current branch is not the default branch (`git symbolic-ref refs/remotes/origin/HEAD`) | **Branch scope:** `git diff --name-only $(git merge-base <base> HEAD)...HEAD` (`<base>` = the session file's branch, else the default branch) + the working tree |
| 2 | On the default branch | **Session scope:** files of the commits since the `.dev-team-agents/.learn-last-run` hash when it is an ancestor of `HEAD` (`git merge-base --is-ancestor`), otherwise of today's commits (the rule in `scripts/hooks/lib/touched-paths.sh`) + the working tree |
| 3 | The set is empty | Nothing in scope — stop with the "Nothing to update" outcome |

"The working tree" = `git status --porcelain` paths: staged, unstaged and untracked, rename destinations only.
Commits and docs that touch none of the set's paths are out of scope. From the session summary, read only
the entries written since the scope began (row 1: the merge-base commit date; row 2: the marker or today).

## Scoped Evidence (this task only, not full session history)

- `git diff <base>...HEAD --stat` for this task's branch/worktree (scope per § Scope Derivation, row 1)
- The linked spec's `### Amendment Log` (if any) — see `skills/shared/spec-gate/SKILL.md`
- Any `[SPEC-DRIFT]`, `[ARCH-DEVIATION]`, or `[BLOCKER]` finding raised during this task's review
  handoff
- Any decision made during this task's execution that isn't yet reflected in `docs/development/*.md`,
  `docs/wiki/`, or an ADR

## Classify and Promote

Apply the same bucket table `/devteam:learn` Step 2 uses (Doc patch / Wiki entry / ADR candidate /
Session summary / Nothing to update) — do not restate it here, reference `commands/learn.md`. Spawn:

- `technical-writer` — only if at least one bucket has content; writes doc patches and wiki entries
  per `skills/shared/docs-sync/SKILL.md`
- `software-architect` — only if an ADR candidate was identified; follows `skills/shared/adr/SKILL.md`

## Anti-Dead-Log Rule (hard gate)

<HARD-GATE>
An Amendment Log entry, a `[SPEC-DRIFT]` finding, or any other non-obvious discovery from this task
resolves to exactly one of: a wiki entry, a doc patch, an ADR, or an explicit "not worth keeping"
call made out loud to the user. It never sits only in the spec file or the session summary once the
task closes — that is what turns the memory system into a dead log instead of compounding knowledge.
</HARD-GATE>

## Commit

Fold the promoted files into this task's own Session-close commit(s) (layered per
`conventional-commits`), or as one trailing `docs:` commit — never leave promoted docs uncommitted
and unmentioned in the hand-off message.

## Nothing to Promote

If the scoped evidence yields no bucket hits, skip silently — no agent spawn, no commentary. Mirrors
`/devteam:learn`'s "Nothing to update" behavior so the gate never manufactures busywork on trivial
tasks.
