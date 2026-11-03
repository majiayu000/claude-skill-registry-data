---
name: om-pr-autopilot
description: Repo-local extension of om-pr-autopilot - the PR state is re-read before every push, because a human may merge or close the PR mid-run, and the limits of an unattended run.
---

# om-pr-autopilot (money-tracker.online)

This file extends the shared `om-pr-autopilot` skill installed at
`.claude/skills/om-pr-autopilot/SKILL.md`. Follow its full workflow with the additions below.

## Re-read the PR state before every push

Diagnosis reads the PR state once, at the start, but a human may merge or close the PR while the
run works. This rule covers every push the run makes, including those of the skills it chains
that push to the PR head (`om-auto-continue-pr`, `om-auto-continue-pr-loop`, `om-auto-fix-pr`,
`om-auto-review-pr --autofix`), whether or not their own overrides were read:

- Immediately before each `git push` to the PR head, run **get-pr** and read `state`. Keep the
  check and the push in one command so nothing runs between them.
- Anything other than `OPEN` stops the run: do not push, release the claim, post one comment
  saying why the run stopped, and report the commits that were not pushed.

GitHub deletes a merged PR's head branch, and a push to it recreates that branch on the remote.
It happened on #447 (2026-09-24): the PR was merged while the base-merge gate ran, and the push
that followed brought `ci/vps-only-runners` back.

## "Approvable" follows the ruleset

A PR is approvable (state matrix row 9) when no review requests changes, no review thread is
unresolved, and the base branch's ruleset requirements for approvals and code-owner review are met.
With `required_approving_review_count: 0` and no code-owner review, that holds without any
approving review: read the ruleset as `.ai/skills/om-approve-merge-pr/SKILL.md` § Rules says. A
missing approval this run cannot give itself (its own account authored the PR) is not a reason to
stop at merge-ready under `--allow-merge` when the ruleset requires none.

`--allow-merge` means a merge into `develop` only. A PR whose base is not `develop`, or that
carries `do-not-merge`, ends at merge-ready under `--allow-merge` too: the `develop` -> `main`
promotion deploys production and is the owner's to merge.

## Nothing into `develop` waits for a person

Owner decision 2026-10-06 (ADR 0031): QA, `risk-high` and `security` are judged by specialist
sub-agents, and a rejection goes back to the agents. These rules cover the run and every skill it
chains:

- **QA runs through the unattended sign-off.** Where the chain reaches the QA stage (state matrix
  rows 7 and 10) of a PR that touches a user-facing surface, run
  `om-auto-qa-pr {pr} --self-qa-signoff` (the repo override of `om-auto-qa-pr` says how its panel
  decides). Row 10 never stops to request a person's sign-off: it runs that QA stage. After a
  successful sign-off, re-read the QA labels and continue with row 9 under `--allow-merge` in the
  same run.
- **A `risk-high` or `security` PR merges on a security verdict.** Before row 9 merges one (the
  label, or the risk `SDLC.md` infers from the diff: a label the author left off does not skip it),
  whether or not it touches a user-facing surface, ask `security-tenancy-reviewer` through
  `.ai/skills/afk-decide/SKILL.md` to judge the diff at the current head, and merge only on its
  approving verdict, recorded in the PR body's Resolved assumptions table with the head it judged.
  A refusal is a failed round of the loop below, its findings the fix list. A verdict on an older
  head does not count: merge with `gh pr merge --match-head-commit <the judged head>`, so a push
  after the verdict makes the merge fail instead of landing unjudged code.
- **Every rejection goes back to the agents, three rounds at most.** A failed check,
  `changes-requested`, a `qa-failed` the QA panel set and a refused security verdict all route to
  `om-auto-fix-pr {pr}` with the findings, and then to review, QA and the security verdict again on
  the new head - never to a stop that asks for a person. Judge the round and the panel label with
  one command, never by listing comments yourself:

  ```bash
  node .ai/scripts/qa-panel-failed.mjs --repo {owner}/{repo} --pr {n}
  ```

  That script is the only definition of the predicate. `nextRound` is
  max(count of surviving `Autopilot round` comments, count of `labeled` timeline events for
  `qa-failed` and `changes-requested`) plus one — a CI or refused-security round leaves no
  `qa-failed` event, so comments still count; deleting the 🤖 comments cannot reset the cap because
  the labeled events remain. `isPanelQaFailed` is true only when the latest `labeled qa-failed`
  event is followed by a `🤖 QA-PANEL-FAILED head:<sha>` marker. Row 0c's failed-QA stop applies
  only when `qa-failed` is present and `isPanelQaFailed` is false; a panel `qa-failed` routes to
  `om-auto-fix-pr`, which removes that label once its fix is pushed. Each round opens with a 🤖
  comment `Autopilot round <n>/3: <what failed>` using `nextRound`. When `exhausted` is true (the
  next round would be 4), add `blocked` and post one comment that starts `🤖 HUMAN-ONLY: ` and lists
  what each round tried and what still fails: that is one of two ways this loop hands a PR to a
  person (the other is a gate PR at the merge row). Residual risk: label and timeline events come
  from the shared account, so the timeline helps against deleted comments, not against a rogue
  agent.

## Gate-path PRs are Rafał's merge

Owner decision 2026-11-02 (ADR 0031 addendum, signed by Rafał): a PR whose file list matches a
gate-path glob is never merged by this skill or by `om-approve-merge-pr`. The globs and the
detect / fail-closed / hold procedure live in `.ai/skills/afk-decide/SKILL.md` § 5; this file
does not copy the list. Unattended runs still fix, review, QA, and record a security verdict.

Immediately before state-matrix row 9 under `--allow-merge` (after those steps), run that
procedure against **get-pr-files** and the `origin/develop` copy of `afk-decide`. On a gate PR
(or fail-closed): apply `blocked`, post the § 5 `🤖 HUMAN-ONLY:` comment if a trusted agent has
not already, do **not** invoke `om-approve-merge-pr`, stop at merge-ready, and report that
**Rafał** merges it. Do not apply `blocked` earlier in the chain. Detection never uses labels,
the author's risk claim, or `gh pr view --json files`.

## A spec PR the plan-to-spec run opened merges

The installed skill treats a spec-only design PR as draft-by-intent
(`.claude/skills/om-pr-autopilot/references/state-matrix.md`, `.claude/skills/om-auto-fix-pr/references/pr-finalize.md`),
and `om-approve-merge-pr` refuses a draft, so a spec-only PR ends at merge-ready and a person merges
it. One kind is the exception, because a specialist panel has approved it before the PR exists, or a
second specialist has settled the one disagreement it left and the PR body says so
(ADR 0030, which amends ADR 0027 and is itself amended 2026-10-11): a spec-only PR that **all** of these describe merges under
`--allow-merge` like any other PR into `develop`:

- its branch is `spec/<slug>` and the `plan-to-spec` workflow or `afk-plan-to-spec` opened it: the
  panel's verdicts and a Resolved assumptions table are in its body, and its spec's metadata table
  has a `Plan` row where an `Issue` row would be;
- it is ready for review (a draft is the not-approved path of `afk-plan-to-spec` step 5, which also
  puts `blocked` on it);
- it does not carry `blocked`, `do-not-merge` or any other hold.

Every other spec-only PR keeps the person's merge, the `spec` workflow's and a spec task's
(`implement-ticket`; an `Issue` row and no `Plan` row) among them. A docs-only PR on a `docs/plan-delivered-<slug>` branch (`afk-plan-to-spec` marking
stages the code already delivers) is not a spec-only PR: no draft-by-intent applies, and it merges
under `--allow-merge` like any docs-only PR.

## Unattended-run limits

These hold for every skill this run chains, whether or not its own override was read:

- **A lesson goes into the PR, never outside the worktree.** Write it in a `## Lessons` section of
  the PR body, or of the run handoff when no PR exists, where `afk-lessons` collects it. Never edit
  `~/.claude/CLAUDE.md` or any other file outside the worktree, and never end a run asking a human
  to move a lesson there: a cezar run is refused that write, and two runs failed trying.
- **A fix that needs a protected file ends with the patch, not a workaround.** Claude Code refuses
  writes to `.husky/*`, `.claude/settings.json`, `.claude/hooks/*` and `worker-configuration.d.ts`
  under `dontAsk` (ADR 0025). When the fix needs one, do the rest of the work, then put the exact
  patch for that file in the PR body and the report, together with a configuration guardian verdict
  from `.ai/skills/afk-decide/SKILL.md`, so applying it is one step for a human. Never retry the
  write through `cp`, `sed`, a heredoc or another path, and never route the whole ticket to a human
  in advance because one file is protected: #480-#482 went to a human only for
  `worker-configuration.d.ts` (run ee7c7d1a).
- **A denied command ends the run, so never try one.** `permissions.deny` in
  `.claude/settings.json` refuses it and `dontAsk` turns the refusal into a failed run: run d232173a
  (#499) died on `git reset --hard origin/<head>`. Use the allowed equivalent (AGENTS.md): move a
  worktree to a PR head with `git status`, `git fetch origin <head>`, then
  `git checkout -B <head> origin/<head>` (when another worktree holds `<head>`, a clean task
  branch takes `git merge --ff-only origin/<head>`); after a rebase, merge the base or push a new
  branch instead of force-pushing (`--force-with-lease` included); fix what a hook reports instead
  of using `--no-verify`.
- **Never open a file `permissions.deny` refuses to read**, not even redacted through `cat` or
  `sed`: it ends the run the same way (planned.travel run b6eb30ef died on
  `cat .ai/qa/test-env.env`). The login's `passwordEnv` name is in `.ai/qa/test-env.json`; load the
  values with `set -a; . "$(jq -r .credentialsFile .ai/qa/test-env.json)"; set +a` and use
  `"$TEST_OWNER_PASSWORD"` in the command (AGENTS.md).
- **The dev server URL is `baseUrl` in `.ai/qa/test-env.json`** (`om-prepare-test-env` writes it).
  Never derive it from `.dev.vars`, which the agent never reads.
- **Required checks stuck at `queued`: read the runner pool before waiting.** When
  `gh api repos/<owner>/<repo>/actions/runners --jq .total_count` is 0, nothing can pick the jobs up
  and the wait budget is wasted: apply the `ci.maxWaitMinutes` expiry procedure at once, and do not
  push again, because `ci.yml` cancels the queued run of the previous head on every push. #596,
  #598, #604, #608, #609 and #610 waited on an empty or idle self-hosted pool.
