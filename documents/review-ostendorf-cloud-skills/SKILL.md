---
name: review
description: "Reviews a diff, a branch or a pull request and posts the verdict as a comment with findings grouped by severity. Use when asked to review code, before merging a pull request, or before approving your own earlier work from a different session."
---

# Review

Review a change the way a peer does who has to maintain it afterwards.

## When to use

- Before merging a pull request.
- Asked to look over a diff, a branch or a file.

## Steps

1. Establish the scope: `git diff <base>...HEAD`, or `gh pr diff <number>`. Read the issue or
   the pull request body for the intent before judging the code. The description becomes the
   merge commit's record. A claim it makes that the branch itself refutes is a finding, filed
   like any other.
2. Read the changed code in its context, not only the diff hunks. A hunk that looks fine can
   still break a caller.
3. Check, in this order, and stop guessing where something cannot be verified:
   - correctness: edge cases, error paths, empty values, concurrency, idempotency
   - security: input validation, secrets, injection, permissions
   - operational impact: migrations, rollout, rollback, blast radius
   - conventions: the matching convention skill, naming, layout, Conventional Commits
   - tests: do the new paths have coverage, do the tests assert behaviour
   - documentation: README, docs, ADR or concept doc where the decision deserves one
4. Verify claims instead of asserting them. Run the verify command, run the linter, check the
   symbol that is supposedly unused. A finding of the shape "does this write happen" is verified
   by counting the write at its source, a reflog entry, a call count on a fake, a log line,
   never by comparing state before and after: an identical write leaves the result identical.
5. Compare the change's author to the current session's own work. Never approve your own work.
6. Decide the verdict: `approve`, `changes requested`, `needs human` or `blocked`.
7. Review only, per Guardrails: no file edit and no commit of its own, whichever posting path
   follows. On a pull request where this review's identity differs from the author: post the
   verdict as a formal review, `POST /repos/{owner}/{repo}/pulls/{number}/reviews` through
   `gh api`, with
   `event` from the verdict, `commit_id` the pull request's full 40 character head SHA (a short
   SHA fails with 422), and `comments`: one entry per finding, `{path, line, side: "RIGHT",
   body: "<Blocker|Should|Nit>: <problem and fix>"}`, severity as the first word. This formal
   review is the verdict; post no separate comment. A line outside every diff hunk: anchor at
   the nearest changed line in the same file and name the real location in the body, or, with
   no changed line in that file, put the finding in the top level review body instead.
8. The review is of the current session's own earlier work, or config `review.token`'s
   environment variable is absent: GitHub refuses the review call. Post the verdict with
   `gh pr comment` instead, same structure: first line `Verdict: <verdict>`, then findings
   grouped `Blocker`, `Should`, `Nit`, each naming the file, the line, the problem and a
   concrete fix. Without a pull request, report the same structure as the response.
9. A rework re-review: resolve every open review thread whose finding is now fixed, one
   GraphQL `resolveReviewThread` mutation per thread, before posting the new verdict. A finding
   that still stands keeps its thread open and is restated in the new verdict.
10. State plainly what was not reviewed and what could not be verified.
11. Approve only when no blocker and no should fix finding remains.

## Guardrails

- Review only: no file edit, no commit, no merge. It posts the verdict, nothing else.
- Never approve a change authored by the current session.
- Never approve while a blocker or a should fix finding stands.
- A claim about test results or a symbol's use is verified by running something, not recalled.
- A formal review or a `gh pr comment`, never both, for the same verdict. Resolving a thread
  never substitutes for restating whether its finding passed in the new verdict.
- `review.token`'s value is read into `GH_TOKEN` for the review call only, never printed.
- Posting a review needs no confirmation. It is a comment, reversible like any other.
- A spawned review runs in the `reviewer` agent, or in `reviewer-boundary` when the boundary
  path list in `work-review` matches. The list decides, not a feeling about the change. A
  re-review continues the first reviewer and checks the finding list only.

## Config

- `verify`: command used to check a claim about tests or lint. Default: `task check`.
- `models.review`: default `sonnet`. `models.reviewBoundary`: default `opus`.
- `review.token`: environment variable holding a token of a review identity, for the formal
  review upgrade. Default: unset, the verdict stands as a comment.

## References

- `git-conventions` for the conventions a review checks against.
- `ci-review` for a review that runs non interactively in CI.
- `gh api`: <https://cli.github.com/manual/>. GraphQL `resolveReviewThread`:
  <https://docs.github.com/en/graphql/reference/mutations#resolvereviewthread>.
