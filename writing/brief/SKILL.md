---
name: brief
description: The five shapes a human surface takes — work, change, update, decision, closure. Use before writing an issue, a pull request body, a comment, a question or a closing note. Never for a run record, which holds how the work was done.
---

# Brief

> "The writer proves it worked. The reader has to dig out what matters."

**A human surface is a decision interface.** It carries what becomes true, why it matters, what a
person must judge, and where the evidence is.

**The run record carries how you got there.** Link to it. Never paste it.

## The four questions

A reader must answer these in about twenty seconds:

1. What becomes true?
2. Why does it matter?
3. What judgement or action is wanted?
4. Where should I start?

If they cannot, no amount of trimming will fix it. The body is doing more than one job.

## Work brief

Someone wants something. An issue.

| Outcome | what should become true |
| Why now | the cost, the break, or the opening |
| Done when | checks a person can watch fail |
| Not this | one exclusion, only when it saves a wrong turn |
| Open | what genuinely blocks or changes the work |

A **defect** adds what happens, what should, and the smallest way to see it.
An **idea** adds who it would affect and what is still unknown.

## Change brief

A candidate wants a decision. A pull request body.

| Outcome | what this makes true, and why |
| Review | the judgement wanted, and where to look first |
| Change | one to three conceptual changes. Never a file tour |
| Evidence | results, bound to the final candidate |
| Limits | a risk or gap that is not obvious. Omit it rather than write *none* |

**Write it after the candidate is final**, and check each sentence against the diff. A body written
early describes work that may no longer exist.

## Update

Something moved. A comment.

| State | done, blocked, decision needed, no action |
| Delta | only what changed since the last one |
| Consequence | what that changes |
| Next | the action, its owner, or the smallest reply that unblocks it |

**Never restate the issue.** A comment repeating the body is a second contract that will drift.

## Decision brief

A person must choose. A question.

| Decision | the one thing to settle |
| Recommendation | your best answer, where you have one |
| Consequences | what each real option changes |
| Reply | the shape of the answer: yes or no, one of these, a number |
| Evidence | only what is needed to decide. Link the rest |

**One decision per ask.** Two questions in one comment get one answer.

## Closure record

Work ended. A closing note.

| Outcome | done, not done, or overtaken |
| Evidence | the checks that support it |
| Left over | links to work that owns the rest. No retelling |

**Tick the boxes that hold, and say which do not.** A box nobody can tick records nothing.

## The seam names the item, so you never do

**Never write `Closes #N` or `Refs #N` in a brief.** `run.sh deliver` appends one, under the body,
where a machine reads it. A brief that writes its own gets it twice.

That happened on the first delivery to use this skill. The body ended `Refs #377`, the seam added
`Refs #377`, and both shipped.

| Where it goes | What writes it |
|---|---|
| the body | you. What becomes true, and why |
| the line under it | the seam. `Refs #N`, or `Closes #N` where the run may close |
| the line under that | the seam. `floor-run:`, for a machine |

**Reference another item freely.** The rule is about the item this delivery answers, which the run
already knows.

## The budget

**Twenty seconds to orient, ninety to read.** For an ordinary change that is about 120 to 180 words.

**A design budget, not a bar.** A qualifier that makes a claim true always beats the count.

A body that keeps needing more than 250 words is telling you something. Either the change is too
broad, or another artefact is doing the wrong job.

## Two traps

**Structure is not clarity.** Bold turns, aphorisms and dense tables can make long prose feel
deliberate while the reader still carries everything. Memorable is not the same as clear.

**Fear of missing context is why bodies grow.** A fresh session copies history in to feel safe, and
that copy becomes the next session's input. Trust the link.
