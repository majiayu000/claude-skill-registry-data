---
name: ci-review
description: "Reviews a pull request from CI as a comment whose first line is the verdict, grouped by severity with file and line references, and never merges or pushes. Use when a workflow triggers an automated pull request review, including an infrastructure pull request with a sticky plan comment."
disallowed-tools: AskUserQuestion
---

# CI review

A pull request review a human can act on without rereading the diff.

## When to use

- A workflow triggers a review on a pull request.

## Steps

1. Read the pull request body and the linked issue for intent. No intent means the
   first finding is the missing description.
2. Get the diff with `gh pr diff` and read the changed files in context.
3. On an infrastructure pull request, read the sticky plan comment the OpenTofu pipeline
   posted for every touched module: replace and destroy rows first with their reason,
   then anything that looks like drift instead of the change itself, then the plan output
   for a secret value that should have stayed masked. A touched module with no comment
   means the plan job failed or posted nothing: ask for that run, do not judge the diff
   alone. A pull request from a fork gets no plan, say so and review the diff only.
4. Review in order: correctness, security, operational impact, conventions, tests,
   documentation.
5. Verify what is verifiable in the runner: tests, linters, build. Report the real
   output. Never claim a check that did not run.
6. Classify findings: blocking (defect, security issue, data loss, breaking change
   without migration), should fix (convention violation, missing test, unclear naming,
   missing docs), nit (optional improvement). Drop anything a linter already owns.
7. Decide the verdict: `approve` when nothing blocks, `changes requested` when something
   does, `needs human` when the call is ambiguous, `blocked` when the pull request cannot
   go forward as is.
8. Post the verdict with `gh pr comment`: first line `Verdict: <verdict>`, then the output
   format below. This comment is the verdict and stands on its own.
9. Upgrade to a formal review with `gh pr review --approve` or `--request-changes` and the
   same body: on a runner the workflow's own token is already a different identity than the
   pull request's author, so this is the normal path here, not the exception. Config
   `review.token` names an environment variable to read `GH_TOKEN` from instead, when the
   runner's default identity is the author. The workflow sets `GH_TOKEN` at job level,
   never as a command prefix: the CI profile allows the bare `gh pr review` and nothing else.
10. GitHub refuses the review call when the identity still matches the author, or no
    variable resolves: the comment from step 8 already stands, name the fallback in the
    report.
11. Never merge, never push to the branch, unless the workflow explicitly asked for a
    fix commit.
12. When the work loop is in use, move the label from the config: `reviewing` while the
    review runs, then `done`, `changesRequested`, `needsHuman` or `blocked` per the
    verdict. A missing label on the tracker is reported, never created.

## Output format

```markdown
Verdict: approve

## Blocker
- path/file.ext:42 problem, fix

## Should
- path/file.ext:88 problem, fix

## Nit
- path/file.ext:12 problem, fix

## Not verified
- checks that did not run, areas not reviewed
```

## Guardrails

- On an infrastructure pull request, the sticky plan comment read at step 3, for replace,
  destroy and secrets, before judging the change from the diff alone.
- Intent read before judging. Diff read in full, not sampled.
- Findings reference file and line and name a concrete fix.
- Severity separated, linter owned style dropped.
- Checks actually run, output real, nothing claimed that did not execute.
- The comment is the verdict. A formal review only adds the same body through the review
  API, never replaces the comment.
- `review.token`'s value is read into `GH_TOKEN` for the review call only, never printed.
- Move the label with the snippet in `~/.claude/skills/README.md`: exactly one
  `ai:` state label remains after the move.
- A verdict comment posted, never a merge or a push.
- Limits of the review stated in the output.

## Config

- `labels.reviewing`, `labels.changesRequested`, `labels.done`, `labels.needsHuman`,
  `labels.blocked`: label names for the work loop. Defaults in the skills README. A missing label is
  reported, never created.
- `review.token`: environment variable holding a token of a review identity, for the
  formal review upgrade. Default: unset, the runner's own identity applies.

## References

- `ci-conventions` for the run itself and the OpenTofu pipeline that posts the plan
  comment.
