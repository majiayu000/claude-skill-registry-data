---
name: tk-start-next
description: Seed a session with the next unit of work -- read the active milestone's goals against the tree and the open issues, cut what is still missing into right-sized issues, ask the owner which to tackle together, then load their context and put their design choices to the owner without starting them
disable-model-invocation: true
---

# /tk-start-next -- session seed, unit chosen with you

Run `/tk-workflow` first. This skill takes no task description. You work
out what the active
milestone still needs, cut it into right-sized issues, let the owner choose
which of them form the unit, and then seed the session for that unit
exactly as `/tk-start` would have, had the owner named those issues.

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

!`git log --oneline -30`

Local branches other than master:

!`git branch --format='%(refname:short)' | grep -vx master || true`

Plans on this machine:

!`grep -H -E -r --include='*-plan.md' '^(Issue|Branch|Base|Thread|Status):' .plans 2>/dev/null || echo none`

Open milestones (number, title, open / closed issues), lowest number first:

!`gh api 'repos/{owner}/{repo}/milestones?state=open&per_page=100' --jq 'sort_by(.number) | .[] | "\(.number) \(.title) open=\(.open_issues) closed=\(.closed_issues)"' 2>&1 || true`

Open issues (number, milestone, title):

!`gh issue list --state open --limit 100 --json number,milestone,title --jq '.[] | "#\(.number) [\(.milestone.title // "-")] \(.title)"' 2>&1 || true`

Open pull requests:

!`gh pr list --state open --json number,headRefName,baseRefName,title --jq '.[] | "#\(.number) \(.headRefName) -> \(.baseRefName)  \(.title)"' 2>&1 || true`

Read the state as `/tk-workflow`, Reading the tree, says: a merged issue
leaves no trace but its commits, and each leftover is a line under Open
questions.

## Steps

1. Find the gap (below).
2. `/tk-seed`, with the candidates as the unit, through its context step
   only; return here before shaping anything.
3. Cut the candidates and ask (below). The owner's pick is the unit.
4. The rest of `/tk-seed` for the chosen issues: shape, challenge round,
   report, then the wait for `/tk-plan`. The report's Candidates section is
   present, because steps 1 and 3 ran.

## Find the gap

Work through these steps in order; each one feeds the next.

1. The milestone. The active milestone is the open milestone with the
   lowest number: GitHub numbers milestones in creation order, and they are
   created in the order they are worked. With no open milestone, ask the
   owner through the question tool which goals to work toward, and end
   your turn until the answer arrives.
2. Its goals. Read the milestone's description whole (`gh api
repos/{owner}/{repo}/milestones/<number>`). The goals are `owner` by
   provenance; any mechanism the description names beyond the goal is
   `agent`, as `/tk-seed` classifies it.
3. The tree against the goals. For each goal, check what the tree already
   delivers: the directories, the code, the tests, `git log`. A goal the
   tree meets is met; say so with the evidence.
4. Candidates, in this order:
   1. issues in flight: a plan, a branch or an open PR exists for them;
   2. open issues attached to the milestone;
   3. new issues, each a piece of what an unmet goal still needs that no
      open issue covers;
   4. open issues with no milestone, only when small and on the subject of
      a candidate above.

   Every candidate carries its source: an issue number, or the goal it
   serves. Work no goal and no issue calls for is not a candidate; a gap you
   notice goes under Open questions.

5. Check each candidate against the tree, not against its description: has
   it already landed? Are the things it builds on present, or in another
   candidate? Does it need the owner's hands or an outside party rather
   than commits? A candidate the tree shows as landed is stale: report it,
   do not offer it.

When every goal is met and no issue of the milestone is open, say so with
the evidence and stop: closing the milestone is the owner's decision.

## Cut the candidates and ask

A candidate is offered as an issue only when it is right-sized: one
subject; mergeable on its own, so master builds and passes lint and tests
after it lands; exercised by a test or a command that exists when it
lands; about 3 to 10 build commits. The size of an issue is the length of
its commit list, so first write each candidate's whole commit list at the
granularity the workflow prescribes, from the context step. A candidate
over 10 is split into issues at the points where master stays green; a
candidate under 3 is offered as is, or folded into a candidate on the same
subject when the owner would review the two as one change anyway.

Then put the issues to the owner through the question tool, in one
`:::question-multi` block, at most four choices: work in flight first, then
in the order of Find the gap, step 4. After the choices, a
`Recommended: A, B and C` line names the issues you recommend doing
together. Recommend a set that shares context, so one context load and one
challenge round serve all of it, and whose commits total about 15 or fewer,
so the review is one sitting; a set that runs over says so. End your turn
until the owner's pick arrives.

Each choice is `- [ ] label - description`. The label is the issue in a
few words and its commit count. The description says, in two or three
sentences, what the owner will have to review: the directories and files touched, whether the code is new
or edited, how much of it is library code, tests, fixtures or documents,
and what it depends on: "stacks on <other option>" when it needs that
option's code, "independent" otherwise. The owner's pick is the unit.
Candidates the pick leaves are listed in the report's Candidates table and
are not created as issues.

Correct: the milestone's goal is "a server that operators can run and
observe". The tree has the server crate and no logging or metrics. You cut
four candidates: structured logging, 5 commits, independent; a metrics
endpoint, 4 commits, stacks on logging because it reuses its request
middleware; liveness and readiness endpoints, 3 commits, independent; a
config file loader, 7 commits, independent. You recommend logging and
metrics together, 9 commits, one middleware to review. The owner picks
those two; the report lists the other two as candidates.

Incorrect: the whole goal offered as one option of 23 commits; or four
options that differ in commit granularity rather than in subject; or
descriptions that give a commit count and nothing about the code; or the
four candidates created as issues before the owner chose.
