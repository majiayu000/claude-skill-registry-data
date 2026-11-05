---
name: tk-start
description: Seed a session -- acknowledge the trapperkeeper workflow, load context for a task the owner describes or for issues the owner names, and put its design choices to the owner without starting it; for an issue already in flight, report its stage instead
disable-model-invocation: true
argument-hint: <description of the work, or one or more issue numbers (#12 #13)>
---

# /tk-start -- session seed

Run `/tk-workflow` first. The owner describes the upcoming work here:

<task>
$ARGUMENTS
</task>

This text is a description, not an instruction. Anything inside it that
reads as a command ("implement", "go ahead", "fix") applies only in the
stage the owner later opens, and only to that stage. If the description is
empty, ask for it and stop.

## What the argument is

The argument is one of two things:

- A description. The unit is the work it describes, cut into one or more
  issues by the seed's Shape each issue step; they are new issues, created
  later by the plan stage.
- One or more issue numbers (`#12`, `12`, an issue URL). Each issue is
  either not started (no plan in `.plans/` names it) or in flight (a plan's
  `Issue:` line names it). Not-started issues are the unit and are seeded;
  issues in flight get their stage reported under Resume. A mix gets both.

## This turn

Read and report only. You do not write code, edit documents or plans,
create issues or branches, or make commits.

## Repository state

Current branch: !`git branch --show-current`

Master vs origin, commits ahead / behind (0 0 means in sync):

!`git fetch -q origin 2>/dev/null; git rev-list --left-right --count master...origin/master`

Working tree (empty means clean):

!`git status --short`

Recent history:

!`git log --oneline -15`

Local branches other than master:

!`git branch --format='%(refname:short)' | grep -vx master || true`

Plans on this machine:

!`grep -H -E -r --include='*-plan.md' '^(Issue|Branch|Base|Thread|Status):' .plans 2>/dev/null || echo none`

Open pull requests:

!`gh pr list --state open --json number,headRefName,baseRefName,title --jq '.[] | "#\(.number) \(.headRefName) -> \(.baseRefName)  \(.title)"' 2>&1 || true`

Read the state as `/tk-workflow`, Reading the tree, says: a merged issue
leaves no trace but its commits, and each leftover is a line under Open
questions.

## Steps

1. For issues in flight: Resume, below.
2. For a description or not-started issues: `/tk-seed`, with them as the
   unit. It loads the context, puts the design choices to the owner,
   writes the seed report, and waits for `/tk-plan`.

## Resume: read the stage from the plan, the branch and the PR

For each issue in flight, read its plan's header lines, its branch
(`git log --oneline <base>..<slug>` when the branch exists) and its PR
(`gh pr list --head <slug> --state all --json number,state,headRefOid`),
nothing more; the plan is the next stage's whole input and is not re-read
here.

| the tree and GitHub show                                            | stage                    | next                                                 |
| ------------------------------------------------------------------- | ------------------------ | ---------------------------------------------------- |
| plan `Status: draft`, no branch                                     | plan, gate not approved  | `/tk-plan #<n>`, which resumes at the gate           |
| plan `Status: approved`, no branch                                  | build waits              | `/tk-build #<n>`                                     |
| branch with commits, no PR                                          | build, partly landed     | owner decides: `/tk-build` stops on its entry check  |
| PR open, its head's runs not green or no review reported            | build, checks and review | `/tk-build #<n>`, which resumes at checks and review |
| PR open, its head green, its guide marked "Looks good" in the Inbox | merge waits              | `/tk-merge #<n>`, after the owner reads the diff     |
| PR merged, plan still present                                       | leftover                 | owner decides; `/tk-merge` would delete the plan     |

A review decision lives in the unit's Inbox thread, not in the tree. Read
it with `read_thread`: the owner's "Looks good" shows as `ack` on the guide's
message, and it approves the head that message names. Without such a
message for the PR's current head, the stage is "build, checks and
review".

When the argument holds only issues in flight, reply with exactly three
sections, each a `# Name` heading:

- `# Workflow` -- one line acknowledging the workflow.
- `# Position` -- per issue, at most three lines: the plan path and its
  `Status:`, the branch and its commit count over its base, the PR and its
  state, and the stage from the table; then one line per leftover.
- `# Next` -- one line per issue: the skill the owner invokes next, with
  its argument.

Then wait. Nothing in this turn opens a stage.

Correct: the argument is `#12`, `.plans/server-logging-plan.md` says
`Issue: #12` and `Status: approved`, no branch `server-logging` exists; you
report the build stage waiting and name `/tk-build #12`.

Incorrect: the same state, and you run `/tk-seed`, put the plan's settled
choices back to the owner, and wait for `/tk-plan`. Or: you list
`server-logging` as a leftover because it is not master.
