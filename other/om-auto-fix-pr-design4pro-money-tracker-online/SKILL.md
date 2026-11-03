---
name: om-auto-fix-pr
description: Repo-local extension of om-auto-fix-pr - the open-thread exit criterion the stabilization loop gets.
---

# om-auto-fix-pr (money-tracker.online)

This file extends the shared `om-auto-fix-pr` skill installed at
`.claude/skills/om-auto-fix-pr/SKILL.md`. Follow its full workflow with the addition below.

## An open thread ends the loop, it does not pass it

One addition to the stabilization loop's exit criteria:

- Before declaring the review approvable, run **list-review-threads** and require zero threads that
  are unresolved and not outdated. An open thread that the `om-auto-review-pr --autofix` stage fixed
  but did not resolve is closed here with **reply-review-comment** and **resolve-review-thread**
  (the repo override of `om-auto-review-pr` says how). An open thread the stage declined is settled the
  way that override says, by a specialist's verdict, before the loop ends; only a thread still open
  after that ends it with `changes-requested`, never `merge-queue`, and counts as a failed round of
  `om-pr-autopilot`'s loop. After a fix for a `qa-failed` is pushed, run
  `node .ai/scripts/qa-panel-failed.mjs --repo {owner}/{repo} --pr {n}` and remove `qa-failed` only
  when `isPanelQaFailed` is true (the latest `labeled qa-failed` event is followed by a
  `🤖 QA-PANEL-FAILED head:<sha>` marker). Otherwise leave the label: it is a person's, and removing
  it would bypass the stop in ADR 0031. The script is the only definition of that predicate.

The live `develop` and `main` rulesets both set `required_review_thread_resolution: true`, so an
open thread blocks the merge. The criterion above also keeps the skill from reporting an
approvable PR while a finding still needs an answer.

## Re-read the PR state before every push

The claim step stops on a merged or closed PR only at the start. Immediately before each
`git push` to the PR head (base merge, CI fixes), run **get-pr** and read `state`, in the same
command as the push. Anything other than `OPEN` stops the run: do not push, release the claim,
post one comment saying why the run stopped, and report the commits that were not pushed. A push
to a merged PR's head recreates the branch GitHub deleted on merge (#447, 2026-09-24).

## Unattended-run limits

`.ai/skills/om-pr-autopilot/SKILL.md` § Unattended-run limits applies to this skill when it runs on
its own too: a lesson goes into a `## Lessons` section of the PR body or the run handoff, never
into `~/.claude/CLAUDE.md` or any file outside the worktree; a fix that needs a file Claude Code
refuses under `dontAsk` (`.husky/*`, `.claude/settings.json`, `.claude/hooks/*`,
`worker-configuration.d.ts`) ends with the exact patch and a configuration guardian verdict from
`.ai/skills/afk-decide/SKILL.md` in the PR and the report, never a `cp` or `sed` workaround and
never a ticket routed to a human in advance; and the dev server URL is `baseUrl` in
`.ai/qa/test-env.json`, never anything read from `.dev.vars`.
