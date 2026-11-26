---
name: work-review
description: "Reviews the pull request of one issue in review requested as a fresh independent agent, posts the verdict and routes the label to done, changes requested, needs human or blocked. Use when asked to review, check or sign off the AI implementation of an issue."
context: fork
agent: reviewer
disallowed-tools:
  - AskUserQuestion
---

# work-review

Judge one pushed pull request as a different agent than the one that built it.

## When to use

- An issue carries `ai: review requested` and its pull request is open.

## Independence

- Independent: the review runs in a `reviewer` or `reviewer-boundary` agent that never saw the
  implementation, from a brief naming only repository, issue and pull request.
- Not independent: the session that wrote or supervised the code judges it inline. `approve` can
  still be the judgment, but the label never reaches `done` through it, see step 13.
- Boundary paths, from `gh pr diff <number> --name-only`, pick `reviewer-boundary`: agent
  settings, permissions and hooks, CI workflows and actions, release configuration, secret,
  token or authentication code, network exposure, or more than 800 changed lines outside lock
  and generated files. A `reviewer` that finds a match posts no verdict and reports `boundary`.

## Steps

1. Pick the issue: the one named, or the highest priority issue in `review requested`.
2. Move the label to `reviewing` when that label exists in config.
3. Read the issue body, the `## Plan` section, the pull request diff, and every review thread
   already on the pull request through `gh api graphql` (`reviewThreads`, with `isResolved` and
   each comment's body). A rework round starts from these, not from memory of the first pass.
4. Read CI from `gh pr checks <number>` or the commit's check-runs via `gh api`, never a branch
   filtered runs list. One `gh` per command. A `## Verification` naming no commit is unverified.
   A check still pending: post no verdict, keep the label, report it and stop. The orchestrator
   waits with `gh pr checks <number> --watch` as one background call and continues this reviewer.
5. Run config `verify` against the pushed branch, unless a CI job ran each of its targets green
   on the head commit. The verdict then names those jobs. A target without a job: run verify.
6. Judge in order: does the diff meet the acceptance criteria, is it correct and safe, does it
   need a human. Formatting, naming taste and wording belong to the linters and are no finding.
   For every open thread from step 3, decide whether its finding is now fixed.
7. Decide the verdict: `approve`, `changes requested`, `needs human` or `blocked`; nits alone
   are `approve`, named in the verdict for the orchestrator to fix. Name the commit CI
   was green on, part of the verdict text in steps 9 and 10.
8. Resolve every open thread from step 3 whose finding is now fixed, one GraphQL
   `resolveReviewThread` mutation per thread, before posting the new verdict. A finding that
   still stands keeps its thread open and is restated in this round's verdict instead of a
   second thread for the same problem.
9. Review only, per Guardrails: no edit to the code under review and no commit of its own,
   whichever posting path follows. The pull request's author differs from this review's
   identity, or config `review.token` names an environment variable holding a token of such a
   reviewer: post the verdict as a formal review,
   `POST /repos/{owner}/{repo}/pulls/{number}/reviews` through `gh api`, with `event` from the
   verdict, `commit_id` the pull request's full 40 character head SHA (a short SHA fails with
   422), `body` naming the commit CI was green on, and `comments`: one entry per finding,
   `{path, line, side: "RIGHT", body: "<Blocker|Should|Nit>: <problem and fix>"}`. This formal
   review is the verdict; post no separate comment.
10. Config `review.token` is unset, or the pull request's author is this review's own identity:
    GitHub refuses the review call. The comment path is the normal route for a single account
    setup, not a failure. Post the verdict with `gh pr comment`: first line `Verdict: <verdict>`,
    naming the commit CI was green on, then findings grouped `Blocker`, `Should`, `Nit`, each
    naming the file, the line and a concrete fix. Name the route in the report.
11. A finding's line falls outside every diff hunk in either path: anchor the inline comment at
    the nearest changed line in the same file and name the real location in its body, or, with
    no changed line in that file at all, put the finding in the top level review or comment body.
12. Verdict approve, independent per Independence: move the label to `done`, mark the pull
    request ready with `gh pr ready`.
13. Verdict approve, not independent: treat it like step 15, `needs human`, naming in the
    report that the judgment was approve but independence was missing.
14. Verdict changes requested: move the label to `changes requested`. The pull request stays
    a draft. A pull request that was ready stays ready, nothing is ever put back to draft.
15. Verdict needs human, or config `work.reviewRounds` is set and the round count reaches it:
    move the label to `needs human`. The round count is this skill's own verdict comments and
    formal reviews on the pull request, the one just posted included. Unset means no limit.
16. Label now `needs human`: mark the pull request ready with `gh pr ready` when the `pr`
    skill's ready condition holds and only a human decision is left, otherwise leave it a draft.
17. Verdict blocked: move the label to `blocked`.
18. Changes requested or blocked: point the issue comment at `implement` for the rework round.
19. Never merge the pull request. Never approve one implemented in this same session, formal
    review included.

## Guardrails

- Review only: no edit to the code under review, no commit, no merge.
- A reviewer may write a throwaway probe to settle a claim it cannot settle by reading. It is a
  file of its own, never the code under review, never committed, staged or pushed.
- It is deleted in the same task, the worktree left as found. A probe that starts no process,
  itself or through the code it calls, may be a temporary test file in the worktree.
- A probe that executes command shapes or real git behaviour follows the baseline: an empty
  temporary directory with a fake binary first on the path, or a throwaway repository, never
  the worktree. A review prompt that asks for such probes carries that rule.
- A claim settled only by reading, not by running, is named unverified in the verdict, with
  what it rests on, whether or not running it was attempted.
- Move the label with the snippet in `~/.claude/skills/README.md`: one `ai:` label remains.
- The boundary path list decides the agent. Config `models.review` or `models.reviewBoundary`,
  when set, overrides its model. A re-review continues the first reviewer, finding list only.
- `done` is a real acceptance, only through an independent review. Unsure: `needs human`.
- A `## Verification` section is a claim, not evidence. The pull request's own CI result for
  the current head decides. Every verdict names the commit CI was green on, in both paths.
- A round cap, when set, is a floor for a human decision, never a way to wave through work.
- A formal review or a `gh pr comment`, never both, for the same round's verdict. Resolving a
  thread never substitutes for stating whether its finding passed in the new verdict.
- A finding of the shape "does this write happen" is verified by counting the write at its
  source, a reflog entry, a call count on a fake, a log line, never by comparing state before
  and after: an identical write leaves the result identical.
- `review.token`'s value is read into `GH_TOKEN` for the review call only, never printed or logged.

## Config

Reads `.agent-skills.json` through the snippet in `~/.claude/skills/README.md`.

- `work.reviewRounds`: review rounds before escalating to `needs human`. Default unset, no limit.
- `models.review`: default `sonnet`. `models.reviewBoundary`: default `opus`.
- `labels.reviewing`, `labels.done`, `labels.changesRequested`, `labels.needsHuman`,
  `labels.blocked`: defaults in `~/.claude/skills/README.md`.
- `review.token`: environment variable holding a token of the review app, see the Apps section
  of `github-as-code`. Default: unset, the verdict stands as a comment.
- `verify`: command that proves a change is good.

## References

- `gh pr review`, `gh pr comment`, `gh pr ready`, `gh api graphql`:
  <https://cli.github.com/manual/>
- `pr` skill: the ready condition for leaving draft.
- `implement` skill: the rework round a `changes requested` or `blocked` verdict hands off to.
