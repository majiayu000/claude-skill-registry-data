---
name: om-auto-review-pr
description: Repo-local extension of om-auto-review-pr - QA routing for user-facing changes and the human-only visual judgement this repository keeps (ADR 0016).
---

# om-auto-review-pr (money-tracker.online)

This file extends the shared `om-auto-review-pr` skill installed at
`.claude/skills/om-auto-review-pr/SKILL.md`. Follow its full workflow (claim, worktree, review
engine, verdict, labels, bounded CI follow-up) with the rules below layered on top.

## QA routing

- A PR whose diff reaches `src/routes/**`, `src/components/**`, `src/styles/**` or
  `src/lib/i18n/messages/*` is user-facing: make sure it carries `needs-qa` and not `skip-qa`.
- A PR that only touches docs, CI, tests, `scripts/**`, `.ai/**` or dependencies gets `skip-qa`.

## The visual judgement is a human's

Nothing in CI compares a pixel (ADR 0016). For every `needs-qa` PR, the review body ends with a
section `## 👀 Visual check for the QA reviewer` that names each screen the diff touches and gives
the capture command for it:

```
node scripts/visual/capture.mjs --url http://127.0.0.1:3010/<route> --out <scratchpad>/pr-<n>/<screen> --viewports 360x800,1280x900
```

Frames belong outside the repository. Evidence from `om-auto-qa-pr` complements the pair; it never
replaces it. `qa-approved` comes from the unattended sign-off in `om-auto-qa-pr`, a specialist panel,
`risk-high` included (ADR 0031) - never from a review.

## Review personas

On a `needs-qa` PR, dispatch the personas the diff matches before writing the verdict; on any PR
reaching `src/server/repos/**`, `src/server/auth/**`, `src/server/ledger/**`, billing or a
migration, dispatch `security-tenancy-reviewer`; on any PR touching `docs/plans/**` or carrying
acceptance criteria on its issue, dispatch `product-owner`, whose own trigger no `needs-qa` diff
reaches. The table and the boundary are in `CODE_REVIEW.md`
-> **Review personas**, and `om-code-review` is where their findings are re-ranked and merged into
the report. A persona that could not run is named as not run.

This needs the `Task` tool. Every cezar workflow step that reaches this skill grants it; where it
is absent the review runs without personas and the report says so, in one line.

## Review threads are answered, then resolved

The threads other reviewers leave (a human, an earlier agent pass) are resolved by nobody unless
this skill does it, and a thread nobody answers is feedback that disappears at the squash. Three
additions to step 2 and step 11:

- Step 2, collecting `INHERITED` findings: take the open set from **list-review-threads**
  (unresolved and not outdated), not from **list-review-comments** alone; keep each thread's `id`
  and its first comment's `id` with the finding.
- Step 11, accounting: a finding **fixed** in this run ends with **reply-review-comment** (what
  changed, in which commit) followed by **resolve-review-thread**. A finding **filed as a
  follow-up** ends with a reply naming the follow-up issue, then resolve. A finding **declined**
  goes to an independent specialist through `.ai/skills/afk-decide/SKILL.md` (picked by what the
  finding is about), with the finding and the reason to decline: when it sides with the finding,
  fix it as above; when it sides with the decline, reply with the reason and its verdict, then
  resolve. The pipeline, not a person, closes a disagreement on a PR into `develop` (owner
  decision 2026-10-06, ADR 0031).
  Never resolve a thread without replying in it first, and never resolve one this run did not act
  on.
- Step 11, the fourth outcome: **agreed but out of the run's reach.** Declining is for a
  disagreement, and only a disagreement. A finding you agree with but cannot act on - a hook
  refuses the file, the change belongs upstream, the fix needs a credential a run does not hold -
  ends with a reply that carries **the exact edit as a diff block**, the verdict
  `changes-requested` on the PR, and the thread **resolved**. Resolving is what makes the state
  terminal: an open thread blocks the merge and nothing but a human clicking will ever clear it,
  so a run that agrees and walks away has converted a one-line correction into a permanent stall.
  `changes-requested` is what says a human still owes something; the resolved thread carries what
  they owe. Try the edit before you use this outcome: it is for what is still refused after that.
- On a pass without autofix (another author's PR, no `--autofix`) the threads are left as found;
  the report lists them by path so the autopilot's next chain can pick them up.

## Rules

- Never apply `qa-approved` or `qa-self-verified`.
- When the reviewing GitHub identity also authored the PR, GitHub refuses an `APPROVE` review.
  Submit the same full approving verdict as a `COMMENTED` review, then move to `merge-queue`.
  This changes only the GitHub review state, not the review work.
- Pending CI is not a reason to wait: the browser suite runs on every PR and finishes in minutes.
  Report it as pending and let the bounded follow-up correct the label.
- The `develop → main` promotion PR is reviewed like any other; when its diff is only merge
  commits already reviewed on `develop`, say so and approve.
- Immediately before each push to the PR head in step 11, **get-pr** reads `state` in the same
  command as the push. Anything other than `OPEN` stops the run without pushing (see
  **Re-read the PR state before every push**).

## Re-read the PR state before every push

The claim step stops on a merged or closed PR only at the start. A standalone `--autofix` run
(`.ai/cezar/workflows/pr-review.yml`, `implement-ticket.yml`) still pushes in step 11 after that.
Immediately before each `git push` to the PR head (autofix commits, conflict-resolution merges),
run **get-pr** and read `state`, in the same command as the push. Anything other than `OPEN` stops
the run: do not push, release the claim, post one comment saying why the run stopped, and report
the commits that were not pushed. A push to a merged PR's head recreates the branch GitHub deleted
on merge (#447, 2026-09-24).

## Unattended-run limits

`.ai/skills/om-pr-autopilot/SKILL.md` § Unattended-run limits applies to this skill when it runs on
its own too: a lesson goes into a `## Lessons` section of the PR body or the run handoff, never
into `~/.claude/CLAUDE.md` or any file outside the worktree; a fix that needs a file Claude Code
refuses under `dontAsk` (`.husky/*`, `.claude/settings.json`, `.claude/hooks/*`,
`worker-configuration.d.ts`) ends with the exact patch and a configuration guardian verdict from
`.ai/skills/afk-decide/SKILL.md` in the PR and the report, never a `cp` or `sed` workaround and
never a ticket routed to a human in advance; and the dev server URL is `baseUrl` in
`.ai/qa/test-env.json`, never anything read from `.dev.vars`.
