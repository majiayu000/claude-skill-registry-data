---
name: lifecycle
description: The development method every role follows - the lifecycle, the definition of done, consent, the report and question formats. Load it once per session before planning, implementing or reviewing work that ends in a pull request.
---

# The method

One lifecycle, run by roles. implement runs it alone in one session; the orchestrator runs it
with implementer sessions. Whoever runs it, the review is made by another session.

## The lifecycle

1. **Spec.** What and why, its goals numbered under `## Goals`. Settled with the operator
   before any plan.
2. **Plan.** Phases, each with its scope, files, tests and definition of done; every figure
   comes with the command that measures it.
3. **Implementation.** Per step: a failing test first, the code, the project's gate run and
   its exit code read, one commit.
4. **Review on evidence.** By a session that did not write the code. A result without the
   command output that shows it is a claim, not a result.
5. **Ready.** The definition of done below, at the current head.
6. **Merge.** The operator's, unless the repository is in auto-merge.

## Done means ready

A pull request is done when, at its current head commit:

- a review by another session left no Critical or Important finding;
- the norms check passed;
- E2E passed, or the operator waived it in their own dated words;
- CI is green.

The github plugin's ready gate computes this; no role declares it. Written, green on one
machine, or "looks fine" is not done. A new commit voids ready until the four hold again.

## Consent

The operator's consent is a structured act (a dialog answer, a recorded ruling), never read
from the words of a prompt. Pushing a branch and opening a draft pull request need none.
Taking a pull request out of draft and merging it belong to the ready gate and the operator,
except in a repository in auto-merge.

## Reports

A unit of work ends with a report in the shape of `references/report.md`. Its last line is
`status: done|blocked|question — <one line>`:

- `done`: delivered; any concern is named under `deviations`.
- `blocked`: it cannot go on without what the line names.
- `question`: a decision only the operator can take.

## Questions to the operator

One question per message, in the shape of `references/questions.md`: the context, two to four
choices each with its cost and gain, one recommendation. Never ask what the spec, the plan or
the code already answers.

## The formats

- `references/plan.md`: the spec's goals, the plan, the state file.
- `references/report.md`: the report.
- `references/questions.md`: the question.

Read one when you write that artifact, not before.
