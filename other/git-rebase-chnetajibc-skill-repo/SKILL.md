---
name: git-rebase
description: "Rebase private branches safely: when to rebase vs merge, interactive cleanup, conflict handling, force-with-lease. Never rewrite shared history."
---

# git-rebase

Rebase is for private branches. Shared history is append-only.
## Inspection

Confirm the branch is private (no dependents, no mid-flight CI on its SHAs) before any rewrite.

## Decision rules

Private → rebase + force-with-lease; shared → merge/revert; messy private history → interactive squash keeping bisect-worthy units.


## Activate when

- Updating a feature branch, cleaning private commits before review.

## Do NOT activate for

- Shared/main/release branches, or undoing published mistakes (use revert → git-recovery).

## Decision

| Situation | Action |
|---|---|
| Private feature branch behind main | Rebase onto main, push `--force-with-lease` |
| Branch others build on | Merge main in (or coordinate a rewrite window) |
| Published mistake | `git revert`, never rebase |
| Messy private commits for review | Interactive rebase: squash/fixup noise, keep bisect-worthy units |

## Procedure

1. Confirm privateness: no other branches/forks depend on it; CI not mid-run on its SHA.
2. `git rebase main` (or `-i` for cleanup); resolve conflicts per git-conflicts; `git rebase --continue`.
3. Push with `--force-with-lease` only; re-request review after the rewrite.
4. Abort cleanly (`--abort`) if the surface exceeds understanding.
5. Verify: log shows intended shape, tests green, reviewers notified.

## Failure modes

Rebasing branches others build on; --force instead of --force-with-lease; rewriting without re-requesting review.

## Escalation

Shared-history mistakes → git/git-recovery (revert, don't rewrite).
