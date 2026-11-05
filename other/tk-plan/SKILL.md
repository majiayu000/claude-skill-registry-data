---
name: tk-plan
description: Open the plan stage of the current unit -- create the GitHub issues that do not exist yet, write one uncommitted plan per issue in .plans/, and put all of them to the owner in one Inbox review. Invoked by the owner after the seed report; the invocation is the gate.
disable-model-invocation: true
argument-hint: "[#n ... , only when resuming plans written in another session]"
---

# /tk-plan -- the plan stage

Run `/tk-workflow` first. This stage opens on this invocation and only this
invocation. It writes plans and GitHub issues; it touches no tracked file,
creates no branch and makes no commit.

## Entry check

Current branch: !`git branch --show-current`

Master vs origin, commits ahead / behind (0 0 means in sync):

!`git fetch -q origin 2>/dev/null; git rev-list --left-right --count master...origin/master`

Working tree (empty means clean):

!`git status --short`

Plans on this machine:

!`grep -H -E -r --include='*-plan.md' '^(Issue|Branch|Base|Thread|Status):' .plans 2>/dev/null || echo none`

Issues named in the argument (empty means the seed report's):

<issues>
$ARGUMENTS
</issues>

A seed report for this unit is in the conversation; its Brief, Issues,
Decisions, Open questions and Proposed commits are the inputs here. Without
one, stop and say so, unless the argument names issues whose plans exist
with `Status: draft`: then the plans are the input, and the stage resumes
at the review (step 5). A plan with `Status: approved` for an issue in the
unit is already through this stage: say so and leave it out.

## Step by step

1. Create the issues the seed report marks "new", one at a time, each with
   its title verbatim from the report:

   ```
   gh issue create -t "<Issue title>" -b "<the issue's paragraph>" [-m "<active milestone title>"]
   ```

   The body is one paragraph in plain words: what the issue delivers and
   why, taken from the report's Brief and Issues sections, plus one line
   `Depends on #<n>` for a stacked issue. `-m` is set when the unit serves
   the active milestone. Note each new issue's number.

2. `/doc-discipline read`.
3. Read `plan-shape.md` and write one plan per issue,
   `.plans/<slug>-plan.md`, in that shape, with `Status: draft`. Create
   `.plans/` if it is missing; it is gitignored, so nothing here shows in
   `git status`.
4. Check the plans. A why you cannot verify, or a function you cannot place
   under the comment rules, is a question to the owner through the question
   tool, asked now; the answer goes into the plan. What the owner leaves
   unanswered is an open question of the plan-stage message.

   Read each plan as the executor would: for each commit, can each comment
   be composed from its specification alone, with every claim traceable to
   its evidence, and can each of its choices be defended from the Rationale
   alone? Each "no" is a gap in the Design, Rationale or Knowledge section,
   filled now. Then read the plans side by side: a decision two plans rest
   on is a row in both, worded the same; a stacked plan's Base names the
   other plan's slug, and its commits assume only what the other plan's
   commits deliver.

5. Put all of the unit's draft plans to the owner in one Inbox message,
   with `send_message` in the unit's thread, as `/tk-workflow`, The Inbox,
   says. `attachments` lists the plans in landing order, and the body says
   in one line per plan what its issue delivers. The message carries no
   question block, so the owner can mark it "Looks good". Then end your turn.

   The owner's answer is one of three, by The Inbox's table:
   - "Looks good" on this message: the owner's yes on these plans, and on the plans
     alone. Change each plan's `Status:` line from `draft` to `approved`,
     so a session seeded fresh reads them as approved. Then post the
     plan-stage message and wait. The build stage opens when the owner
     invokes `/tk-build`.
   - A reply: the owner's redirect, also when its words sound like a yes.
     Fold every annotation and every point of the reply into the plan it
     concerns, and send all of the unit's plans again from step 5, with
     `reply_to` set to the reply's id. Never start code on a plan the
     owner redirected.
   - The thread resolved without a "Looks good": stop and report. The owner decides
     in the conversation.

The plan-stage message, posted on approval, is exactly: one line per issue
with its number, URL, slug and plan path, in landing order; the owner's
`feedback` quoted, if any, with how the build will honor it; the open
questions the plans recorded, each with the recommendation the approval has
now settled; one line saying the build waits for `/tk-build`. The message
goes to the conversation, not to the Inbox thread.

Correct: you create issue #14 for the one new issue, read doc-discipline,
write `.plans/server-logging-plan.md` and `.plans/metrics-endpoint-plan.md`,
check them, send both to the Inbox in one message and end your turn. The
owner marks it "Looks good"; you set both statuses, post the message and wait; the
owner invokes `/tk-build`.

Incorrect: the owner marks the plans "Looks good" and you create the first branch
because the plans are approved. Or: you send each plan in its own message,
so the owner approves the metrics plan before seeing the logging plan it
stacks on. Or: you add an "Approve the plans?" question to the message, so
the owner cannot mark it "Looks good". Or: the owner replies with annotations and you
start code while addressing them.
