---
name: om-auto-fix-issue
description: Repo-local extension of om-auto-fix-issue - how an issue reference is recognised in a Cezar task prompt, this repository's route and UI decisions, and the branch and closing conventions.
---

# om-auto-fix-issue (money-tracker.online)

This file extends the shared `om-auto-fix-issue` skill installed at
`.claude/skills/om-auto-fix-issue/SKILL.md`. Follow its full workflow with the rules below layered
on top.

## An issue reference, not a brief

The Cezar cockpit prefills a run's task with free text such as
`Fix GitHub issue #16: <title> https://github.com/design4pro/money-tracker.online/issues/16`.
A task text that names **exactly one** issue of this repository, whether as a bare number, `#<n>`,
`issue #<n>` or an issue URL under `design4pro/money-tracker.online`, is an **issue reference**,
whatever else the text says: resolve `{issueId}` from it and continue with **get-issue**. Brief mode
(filing a new issue through `om-prepare-issue`) applies only to text that names no issue of this
repository. A text that names two or more is ambiguous: stop and ask.

## Route and UI decision

- The category label decides the route: `bug` takes the bug route, `feature` the feature route
  (Definition of Ready in `SDLC.md`). An unlabelled issue is classified from its body,
  conservatively, and the chosen category label is applied.
- A fix is UI-touching (step 10) when the PR diff reaches `src/routes/**`, `src/components/**`,
  `src/styles/**` or `src/lib/i18n/messages/*`.

## Rules

- No label starts this skill (ADR 0029): a person starts the `issue-autofix` workflow from the
  Cezar cockpit. Never add a label outside the Open Mercato taxonomy (`.ai/trackers/github.md`).
- Branch `fix/issue-<n>-<slug>` or `feat/issue-<n>-<slug>`, cut from `origin/develop`.
- The PR body carries `Closes #<n>`. Merging into `develop` does not close the issue natively;
  `om-close-fixed-issues` does, after the merge.
- Check `docs/agents/out-of-scope.md` before the feature route: a request listed there is closed
  with the row's ADR as the reason, never implemented.

## Unattended-run limits

`.ai/skills/om-pr-autopilot/SKILL.md` § Unattended-run limits applies to this skill when it runs on
its own too: a lesson goes into a `## Lessons` section of the PR body or the run handoff, never
into `~/.claude/CLAUDE.md` or any file outside the worktree; a fix that needs a file Claude Code
refuses under `dontAsk` (`.husky/*`, `.claude/settings.json`, `.claude/hooks/*`,
`worker-configuration.d.ts`) ends with the exact patch and a configuration guardian verdict from
`.ai/skills/afk-decide/SKILL.md` in the PR and the report, never a `cp` or `sed` workaround and
never a ticket routed to a human in advance; and the dev server URL is `baseUrl` in
`.ai/qa/test-env.json`, never anything read from `.dev.vars`.

## Readiness verifier

A ticket that fails the ticket-level tier of the Definition of Ready is not stopped at once. The
gap is usually one the repository already answers, and a human reading it used to write "ready as
is"; the `readiness-verifier` sub-agent (`.claude/agents/readiness-verifier.md`) now makes that
call. This replaces the stop in the feature route's triage gate (`references/fr-triage.md` step 4)
and nothing else - the bug route, the lock check and the already-implemented check are unchanged.

1. A human waiver on the ticket ("ready as is") still satisfies the tier without the verifier.
2. A `readiness verified` comment already on the issue, with no human comment newer than it, is the
   verdict: reuse it and do not run the verifier again.
3. Otherwise delegate to `readiness-verifier` with the issue number, title, body, labels, author,
   every comment (author, timestamp, whether it is an agent's) and the missing items. The verifier
   refuses `risk-high`, `security`, out-of-scope asks and a vetoed verdict itself, so pass every
   issue and let it decide. With no sub-agent tool on this backend, skip it and stop as the
   installed skill says - never verify your own triage.
4. `READINESS: VERIFIED` - post the table as one idempotent comment (find the marker via
   **list-issue-comments**, update it in place via **update-comment** when the table changed), treat
   the tier as satisfied, and continue:

   ```markdown
   🤖 `readiness-verifier` — readiness verified

   The ticket-level Definition of Ready items below were missing. They are resolved here so the
   pipeline can build this issue without waiting for a human.

   {the verifier's table}

   Reply `veto` to revoke this and send the issue back to a human.
   ```

5. `READINESS: NEEDS_HUMAN` - settle each row that is a decision through `.ai/skills/afk-decide/SKILL.md`,
   record it as a Resolved assumptions row and continue. Post the installed skill's not-ready comment
   and stop with `NOT_READY` only for the rows nobody but the reporter can answer, with both readings
   where the verifier named two.
