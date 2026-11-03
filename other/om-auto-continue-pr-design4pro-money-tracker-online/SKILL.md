---
name: om-auto-continue-pr
description: Repo-local extension of om-auto-continue-pr - the PR state is re-read before every push, because a human may merge or close the PR mid-run.
---

# om-auto-continue-pr (money-tracker.online)

This file extends the shared `om-auto-continue-pr` skill installed at
`.claude/skills/om-auto-continue-pr/SKILL.md`. Follow its full workflow with the addition below.

## Re-read the PR state before every push

The claim step stops on a merged or closed PR only at the start. Immediately before each `git push`
to the PR head (after each Phase), run **get-pr** and read `state`, in the same command as the push.
Anything other than `OPEN` stops the run: do not push, release the claim, post one comment saying
why the run stopped, and report the commits that were not pushed. A push to a merged PR's head
recreates the branch GitHub deleted on merge (#447, 2026-09-24).
