---
name: board-comment-style
category: collaboration
description: Write board comments the way a colleague does — lead with the finding, a few lines, no preamble or process narration. Use when about to call add_task_comment or comment_on_pull_request, or when deciding whether something deserves a comment at all.
---
# Board comment style

Write task comments the way a colleague writes them: short, specific, done.

A board comment is read by a teammate scrolling a card, not by a grader. Nobody
reads the second screen. A long comment does not prove more work happened — it
buries the one line that mattered.

Your run's final message is not a comment: it becomes the run summary and,
for a developer, the commit message. The rules below are about `add_task_comment`
and `comment_on_pull_request`, not that message.

## First: is this a comment at all?

**Nothing that went WELL needs a comment.** A passed review, a green build, an
approved criterion, a merged pull request, a successful deploy, "moving this to
pm_uat" — the board already shows every one of those, in the column, the
criteria, the PR field, the pipeline panel and the task history. Writing them
down again is the noise that makes the comments nobody can skip impossible to
find.

Comment when something needs a person or the next agent to **act**:

- a rejection, and exactly why (expected vs actual, file:line, the failing step);
- a failure, a blocker, a refusal you could not work around;
- a question you cannot answer from the code, numbered;
- work you did NOT do, and why;
- a risk or a follow-up somebody has to pick up.

So: verdict is "pass" → move the card and say nothing. Verdict is "fail" → the
comment IS the deliverable, and it has to be precise enough to act on without a
second round trip.

**Never paste the pull request link or number.** It is a field on the task and
the board renders it next to the card; repeating it in a comment on every hand-
off is the same fact three times. The same goes for the merge commit — the task
records it — and for the branch name.

## Length

**Three to six lines is normal. Fifteen is the ceiling, and hitting it should
feel wrong.** A hand-off, a verdict, a status note — each is a few sentences.

If the detail genuinely doesn't fit, it isn't a comment. Put it in a task
document if your role can attach one (`add_task_document`); otherwise cut it to
the actionable lines — the evidence stays. QA: your `review_criterion` note on
the rejected criterion already carries the per-criterion evidence; a comment
repeats it only when something needs a person's decision beyond the verdict
itself.

## Write this

```
Blocked on AC3: "export streams large projects" — `GET /v1/export`
buffers the whole CSV in memory (exporter.go:88) and the 30s proxy
timeout cuts it at ~40k rows. Streaming needs the chunked writer in
internal/http — in scope for this task, or a follow-up?
```

## Not this

```
## Summary
I have completed a comprehensive investigation of the issue described in
this task. Below you will find a detailed breakdown of my analysis...

## Background
This task was assigned to me in the in_progress column...

## What I Did
1. First, I began by reading the relevant files...
2. Then I examined the handler...
[continues for two screens]
```

The second one says less. Everything before "Blocked on AC3" is throat-clearing,
and the numbered narration of which files you opened is a transcript, not a
finding.

## Rules

- **No preamble.** Never open with what the task was, what column it was in, or
  what you were asked to do. Everyone reading already knows — start with the
  finding.
- **No narration of your own process.** "I read X, then I searched Y, then I
  realised Z" is your history, not the result. Give Z.
- **No headed report structure** for a routine update. `## Summary` /
  `## Background` / `## Next Steps` on a three-sentence message is packaging
  heavier than the contents.
- **Name things exactly.** File, symbol, command, error text, expected vs
  actual. One precise line beats a paragraph of description.
- **Don't restate what the board already shows.** The task title, the column,
  the assignee, the acceptance criteria, the pull request and the pipeline
  result are all on the card.
- **Don't pad.** No "I hope this helps", no "please let me know if you need
  anything else", no summary of the summary.
- **Evidence stays, prose goes.** Commands, outputs, the url and viewport of a
  screenshot, and reproduction steps are the valuable part — keep every one of them, and cut the
  sentences around them.

## Where this does not apply

Structured deliverables have their own required shape and are not comments:
QA's numbered expected-vs-actual failure list, a rejection note naming what
failed, an analysis document, an implementation plan. Follow those formats.
The rule here is about the prose you wrap around them — there should be almost
none.
