---
name: pre-commit
description: Commit pass — staged-diff review, stray files, debug leftovers, message format per git standard, version bump. Trigger before any git commit or on "commit", "ship it", "save this".
---

# Pre-Commit — Nothing Accidental Ships

A commit is the one operation where sloppiness becomes permanent history. This pass takes ~1 minute and catches the classics: stray files, debug leftovers, mixed concerns, vague messages.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — what this pass caught, or a check that never fires and could be dropped. Merge instead of duplicating; delete disproven bullets.

## Step 1 — Survey before staging
`git status` + `git diff` (and `git diff --stat` for shape):
- **Untracked strays:** screenshots, scratch files, `*.log`, editor droppings, test assets dumped in root. Each one: belongs in the commit (move to its proper location first), in `.gitignore`, or deleted. Never `git add .` past unexplained untracked files.
- **Debug leftovers in the diff:** `console.log`/`print` probes, commented-out blocks, hardcoded test values, TODO-without-ticket. Remove or justify.
- **Unrelated changes mixed in:** if the diff serves two purposes, split into two commits — stage selectively (`git add -p` is unavailable here; stage by file, or split files' changes deliberately).

## Step 2 — Project standards
- Read the project's git standard if one exists (`coding-standards/git-standards.md`, CONTRIBUTING, etc.) and follow its message format exactly — otherwise default to imperative summary ≤72 chars + body explaining *why* when non-obvious.
- **Versioning:** if the project has a versioning standard/changelog, check whether this change class requires a bump/entry — do it in the same commit.
- Branch check: if on the default branch and the project's flow uses feature branches, branch first.
- Hooks: never bypass (`--no-verify` is off the table); a failing hook is a bug to fix, not an obstacle.

## Step 3 — Message
- First line answers "what does this commit do" in imperative mood; body answers "why" and flags anything a reviewer would trip on.
- No "fix stuff", no "WIP" on shared branches, no message that just restates the diff.
- If the session's work maps to a plan/handover item, phrase the message so it's findable later (name the feature, not the files).

## Step 4 — Final gate
- Re-run `git status` after staging: staged set = exactly the intended set, nothing left half-staged.
- If tests/build exist and the change is non-trivial: run them before committing, not after.
- Commit only when asked or durably authorized; report the hash + one-line summary, not a re-narration of the diff.
