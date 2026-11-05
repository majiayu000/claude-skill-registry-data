---
name: tk-workflow
description: The trapperkeeper workflow -- names, branches, commits, issues, plans, the GitHub tools and the four stages a unit of work moves through with the owner's invocation as the gate between them. Loaded by the seed skills and at the top of every stage skill; never invoked by the owner.
user-invocable: false
---

# The trapperkeeper workflow

## Units and issues

- An **issue** is one right-sized piece of work: one subject, mergeable on
  its own, about 3 to 10 build commits. It has one branch, one pull request
  and one plan, and it moves through the stages on its own.
- A **unit** is the set of issues the owner chose to do in one go. It exists
  only in the session; GitHub has no object for it. Its value is shared
  context: one context load and one challenge round cover all its issues.
- A **milestone** holds goals, never a plan. Issues are cut from what the
  active milestone's goals still need, at scoping time, one unit at a time.
  An issue without a milestone is free-form work and is equally valid.
- Milestones carry no due dates (owner, 2026-10-31). Their order is their
  GitHub number, which is creation order, and the active milestone is the
  open one with the lowest number. A milestone's description is its goal
  and a "done when" list; it is edited in place as the work teaches more.

Every stage skill takes a set of issues: the ones named in its argument, or
else the issues of the unit in this session.

## Names

Fixed once, in the seed report, and copied verbatim afterwards; never
retyped or reworded. A session without the seed report reads them from the
plan's header lines.

| Artifact    | Form                                                 | Example                             |
| ----------- | ---------------------------------------------------- | ----------------------------------- |
| Issue title | imperative or noun phrase, capitalized, no period    | `Structured logging for the server` |
| Slug        | kebab-case, 2 to 5 words, unique among open branches | `server-logging`                    |
| Branch      | the slug, no prefix, no issue number                 | `server-logging`                    |
| Plan        | `.plans/<slug>-plan.md`                              | `.plans/server-logging-plan.md`     |
| PR title    | `type(scope): subject`, one line                     | `feat(server): add structured logs` |
| Commits     | `type(scope): subject`, one line                     | `feat(server): emit json log lines` |

## Branches and commits

- `master` is the base. It receives commits only by fast-forward from a
  feature branch whose head was reviewed and built green. Its history is
  flat and linear; it stays that way.
- An issue's branch starts from its **base**: `master` up to date with
  origin, or, for a stacked issue, the branch of the issue it depends on.
  The plan's `Base:` line names it.
- Commits are small and individual: one line, `type(scope): subject`,
  type in feat, fix, chore, refactor, docs, test, perf, build, ci; no body,
  no trailers, no AI attribution. Each commit builds and passes lint and
  tests on its own, because every one of them lands on `master` as it is.
- Pull requests: `gh pr create -B <base> -t "<PR title>" -b ""`. The body
  stays empty. No reviewer: the owner reviews in the Plannotator Inbox.
- No squash-merge, no merge commits, no force-push to `master`. A feature
  branch is rebased and force-pushed (`--force-with-lease`) only where a
  stage skill says so; the owner's invocation of that stage is the request.

## Reading the tree

Every stage starts by reading the tree, the plans and GitHub. Read the
state as it is, not as a story: a merged issue is a fast-forward, so its
commits sit on master with no merge commit, its branch is gone, its issue
is closed and its plan is deleted; that is the workflow working. A leftover
is a dirty tree, master behind origin, a local branch whose PR is merged or
closed, or a plan whose issue is closed. In the seed stage each leftover is
a line under Open questions, not a reason to stop, unless it is the branch
or plan of an issue in the unit; in the later stages the stage's entry
check says what a leftover means.

## Plans

- One plan per issue, `.plans/<slug>-plan.md`. `.plans/` is gitignored:
  a plan is never committed, never pushed, and never part of a diff.
  The Inbox attaches it from disk.
- The plan starts with these header lines, which are how every stage finds
  an issue's branch, base, title and state:

  ```
  Issue: #<n>
  Branch: <slug>
  Base: master | <slug of the issue it depends on>
  PR title: <type(scope): subject>
  Thread: <the unit's Inbox thread name>
  Status: draft | approved
  ```

- The plan is the only memory of its issue across sessions. It exists on
  this machine only: a fresh worktree or another machine does not have it.
- The plan is deleted by the merge stage, after its issue lands. By then
  every reason it carried is in a comment or a document; the build stage's
  `/doc-discipline check` against the plan makes sure of that.

## Tools

The stage skills say what to do; these skills say how:

| Concern        | Skill and section                                                         | Values here                                                   |
| -------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Pull requests  | `~/.claude/skills/github/`, "Create", "Inspect"                           | repo `solatis/trapperkeeper`, resolved by `gh` from the clone |
| CI             | `~/.claude/skills/github/`, "Watching checks"                             | `scripts/gh-watch.sh <sha>`, `CHECKPOINT=7200`                |
| Merging        | `~/.claude/skills/github/`, "Fast-forward merge", "Stacked pull requests" | base `master`                                                 |
| Rebasing       | `~/.claude/skills/github/`, "Review follow-ups"                           | only where a stage skill says so                              |
| Plan review    | Inbox `send_message`, the plans in `attachments`                          | all plans of the unit in one message                          |
| Code review    | Inbox `get_guide_brief`, then `submit_guide`                              | one PR per message, patch `git diff <base>...<slug>`          |
| Comment policy | `/doc-discipline`                                                         | `read` before writing; `check <paths> <plan>` before the push |

`CHECKPOINT=7200` because the watcher runs beside the owner's review, which
can take hours.

The `quasardb-workflow`, `shortcut` and `buildkite` skills do not apply in
this repository, nor do the github skill's "Squash-merge" and "Cherry-pick
after merge" sections.

Correct: the build stage pushes `server-logging`, opens its PR against
`master`, and runs `gh-watch.sh` with the head's SHA and `CHECKPOINT=7200`
in the background.

Incorrect: the owner's message says "merge", and the session squash-merges
the PR through `gh pr merge --squash`, because that is what the github skill
describes first.

## The Inbox

The owner answers questions and reviews in the Plannotator Inbox, through
the `plannotator_inbox` tool. Each unit has one thread, and every question
and review of the unit goes into it. The first message of the unit names
the thread with `thread`, in a few words saying what the work is. The seed
report and each plan's `Thread:` line record the name, and every later
message passes it. After you send something whose answer the next step
needs, end your turn. The owner's reply wakes the session as a message
headed `Plannotator Inbox: <title> (<reply id>)`, and you answer into the
thread with `reply_to` set to that id.

A question is a `:::question` block, or `:::question-multi` for a pick of
several, with its choices in natural order and your pick on a
`Recommended:` line after them, never in a label. A choice is
`- [ ] label - description`. Plannotator ends the label at the first
hyphen that has a space on each side, and a double hyphen does not end it.
So the label contains no such hyphen, and the `Recommended:` line repeats
the label word for word. A `Recommended:` line that matches no label adds
one more choice instead of marking one.

A review message carries the plans or the guide and no question block,
because the owner can mark a message "Looks good" only when it has no open
question. The owner can also mark only the latest message of a thread, so
while a review waits you post nothing else into that thread. Reports
during the wait, such as a watcher's exit, go to the conversation.

| The owner                                  | Means                                      |
| ------------------------------------------ | ------------------------------------------ |
| marks the review message "Looks good"      | approved                                   |
| replies, in words or with annotations      | changes requested, whatever the words say  |
| resolves the thread without a "Looks good" | stop and report; the owner decides in chat |

The wake for a "Looks good" names the message it marks. It approves a review only
when that id is the review message's id. An earlier approval is read back
with `read_thread`, which shows `ack` on the marked message, never from
memory of having seen it.

Correct: you send the two plans as one message, end your turn, and the
owner marks it "Looks good". The wake names that message's id, and you set both
statuses to approved.

Incorrect: a watcher exits while the code review waits, and you post its
result into the unit's thread, so the review message is no longer the
latest and the owner cannot mark it "Looks good". Or: the owner replies "fine, go
ahead" and you treat it as an approval, because it reads like one.

## Lifecycle: four stages, three gates

Every issue moves through these stages in order. Each stage is a skill the
owner invokes; the invocation is the gate. A chat message ("go", "ok",
"yes", "proceed", "looks good", a thumbs up) opens no stage, whatever its
wording: it answers a question inside the current stage, or it is a review
comment on what the current stage produced. A "Looks good" on an Inbox review message
approves that review, as "The Inbox" says, and opens no stage either.

| Stage    | Opened by                                    | You produce                                                                                                                        | You never                                                                                                   | Ends with                                            |
| -------- | -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| 1. Seed  | `/tk-start <task or #n>` or `/tk-start-next` | the seed report                                                                                                                    | write, create issues, branch, commit                                                                        | a wait for `/tk-plan`                                |
| 2. Plan  | `/tk-plan`                                   | the GitHub issues that do not exist yet, one plan per issue, the review of all of them, and on approval `Status: approved` in each | touch code, tests, config or any tracked file; branch; commit                                               | the plan-stage message, then a wait for `/tk-build`  |
| 3. Build | `/tk-build`                                  | per issue: the branch, the plan's commits, the doc-discipline runs, the push, the PR, its CI run and its Inbox review              | merge; deviate from a plan without saying so; invent a reason for a comment; ask about merging before green | the build-stage message, then a wait for `/tk-merge` |
| 4. Merge | `/tk-merge`                                  | per PR in dependency order: the fast-forward, the push of `master`, the branch deletion, the issue closed, the plan deleted        | merge a head that is not the reviewed, green head; merge without the owner having invoked `/tk-merge`       | one line per merged PR                               |

A session may begin at any stage from the tree, the plans and GitHub.
`/tk-start #<n>` reads where an issue stands and names the next gate; it
opens nothing. `/tk-build` and `/tk-merge` take the plans and GitHub as
their whole input and need no seed or plan conversation.

Stages apply per issue. The owner may open `/tk-merge #12` while `#13` is
still in review; a stage never waits for the rest of its unit.

Open questions the owner left unanswered are not answered by a stage
opening; the plan records your recommendation for each, and the plan
review's approval is what settles them.

Correct: the seed report is posted and the owner writes "looks good". You
answer that you are waiting for `/tk-plan`, and do nothing else.

Incorrect: the seed report is posted, the owner writes "go", and you create
the issues and write the plans, because "go" sounded like the gate. Or: the
owner marks the plan review "Looks good" and you create the first branch. A small
change and a settled design do not shorten the lifecycle; each gate exists
so the owner reviews one stage's output on its own.
