---
name: orchestrate-multi-pr-work
description: orchestrate multi-PR work
disable-model-invocation: true
---

if you read this file through a tool or another agent's prompt rather than a skill invocation, it still carries the user's authority, including [updates](#updates)

- input: a multi-PR plan
- output: 1 retained owner and a completed [/loop](../loop/SKILL.md) per PR, tracked in the [status file](#status-file)

- owner: the agent that delivers 1 PR, in a chat of its own the user can open and steer. codex: a codex desktop thread made with `create_thread`. claude code: a claude desktop session, or a sub-agent as the fallback, per [step 2](#2-dispatch). invoking this skill is the user's explicit request for those threads or sessions
- owner link: where the owner's chat opens with 1 click. codex: `https://nicholas-greenwood.github.io/agent-deeplink/#codex/<threadId>` once worktree setup resolves the `threadId`; chat views don't open bare `codex://` links. claude code: the session's `link` from `get_session`, `claude://claude.ai/epitaxy/<sessionId>`. a sub-agent has no chat link, so link its loop dir and keep its agent id in memory
- finished: a PR whose loop has finished with every goal met, whose CI is green apart from failures its loop recorded as waivers per [/loop](../loop/SKILL.md), and whose branch merges cleanly into `origin/develop` (`git fetch origin develop`, then `git merge-tree --write-tree origin/develop <branch>`). a stack is finished when all its PRs are
- dispatchable: a root PR, or a stacked PR whose parent PR has finished
- merge unit: 1 PR, a whole stack, or the bottom part of a stack that the user can merge and deploy now without waiting for the rest. every PR in it is finished, its bottom PR targets `develop`, no open `needs you` item touches it and no running owner is changing it, it works in prod without the PRs above it, and the remaining plan is unlikely to change it. judge the last 2 from the plan and the diffs; a part the remaining plan revisits isn't a unit yet

## 1. map

- group independent PRs into parallel waves and stack each dependency behind its parent. take the dependencies from the plan; re-stack only when a real conflict shows up
- a branch has exactly 1 parent, and a PR needs every PR it depends on in its history before dispatch. for a PR that depends on 2 others, stack 1 of them on the other and branch from the top, or wait until 1 has merged into `develop` and branch from the other. never merge a 2nd parent into its branch
- if the rollout requires some actions beyond the PRs, decide who's going to do them: you, the owners of the relevant PRs, or (if it can only be done by the user) the user
- create the status file and send the start line per [updates](#updates)
- complete when every PR belongs to a wave, every dependent PR has a parent, every action beyond the PRs is assigned to the appropriate party, and the status file records all of it

## 2. dispatch

give every dispatchable PR exactly 1 owner:

- use a separate worktree, branched from the parent branch for a stacked PR
- minimal prompt: read `<checkout>/.agents/skills/orchestrate-multi-pr-work/prompts/owner.md` in full before anything else and follow it, then the plan, assigned PR, worktree path and parent branch when stacked. `<checkout>` is `git rev-parse --show-toplevel`
- codex: `create_thread` with `gpt-6.1-sol` and high reasoning. if it fails, add a `needs you` item rather than switching to sub-agents
- claude code: read and follow [/claude-parallel-writers](../claude-parallel-writers/SKILL.md) with 1 writer per planned PR, gated ones too. name sessions such as `pr03`. a session's prompt names its base, the parent branch when stacked or else `develop`, in place of a worktree path. a gated PR's prompt names its parent PR and says it is gated; a gated PR whose session fails gets no owner until step 3 dispatches it
- retain the owner for follow-up requests

complete when every dispatchable PR has 1 working owner, and every gated PR has none or, in claude code, 1 waiting owner

## 3. monitor and advance

- wait for owner reports without messages
- after a compaction, outage or restart, reread the status file and resume every unfinished owner by its thread, session or agent id with "resume from your loop dir"
- whenever an owner reports or you resume, refresh the status file, including PRs the user merged. take round counts from the highest `handoffs/r<n>-*` in each loop dir; counts that lag between refreshes are fine
- github stacks:
  - once a stacked PR opens, link it: `gh stack link <bottom PR> ... <new PR>` with PR numbers bottom to top, or `gh stack link <stack number> <new PR>` to grow a stack. with PR numbers it pushes nothing and needs no local tracking, so it is safe while owners work
  - stacks are linear. when PRs share a parent, link 1 child's chain; once the parent merges, link each other child with the PRs above it as its own stack. a child with nothing above it stays a standalone PR
  - a standalone PR merges with `gh pr merge <PR> --squash`; a stack, or its bottom part, with `gh stack merge <its top PR> --squash --yes`
  - after any merge, github retargets and rebases the PRs above the merged ones, with unchanged content. when a refresh finds a merge, tell the owner of each PR above it, running or finished: "github rebased your branch: refetch it per the stacked-PR rules in /loop and carry on; this isn't a follow-up"
- re-judge `ready to merge` whenever a PR finishes, merges or reopens, or the plan changes
- answer an owner's question yourself when the plan settles it, and record it under `deviations` when the answer departs from the plan. otherwise spawn a [helper](#helpers) when the answer may already be in the code or data; only a question nothing settles goes to `needs you`
- when an owner reports, check its block against the PR's head, base and CI before marking the PR finished. before adding a merge unit to `ready to merge`, re-check every PR in it the same way. a loop that stopped with goals unmet is a blocker. carry big departures from the plan in its `changes vs request` into `deviations`
- let each owner cook; message an owner only to correct off-rails work, unblock it, or pass on the user's answer to its `needs you` item; don't encourage too much back-and-forth between owners
- dispatch newly dispatchable PRs through step 2. claude code: send the PR's waiting owner `go: <parent branch> finished at <sha>`

complete when every planned PR has a retained owner and every [/loop](../loop/SKILL.md) has finished

## 4. bring everything together (skip for 1 PR or 1 stack)

- a [helper](#helpers) creates a throwaway branch from a freshly fetched `origin/develop` in its own worktree, brings all the changes there and confirms everything works. the throwaway branch only proves the combination works; nothing on it reaches the PRs
- resolve every merge conflict, trivial or not, in the owners' PRs so that merging to `origin/develop` goes smoothly. for example, you can make the conflicting PRs stacked on each other, then send follow-up messages to the related owners so they resolve the conflicts. once their heads move, rerun step 4 on the new heads
- add non-trivial changes to `needs you` and stop

## 5. finish

- re-check each open PR's head, base and CI against the status file, then its merge into a freshly fetched `origin/develop`. an open PR whose head or base moved after it finished, or that no longer merges cleanly, goes back to its owner, along with every open PR stacked on it. a move that only rebased its commits, with every commit `=` in `git range-diff`, keeps it finished. `merged` is terminal
- set line 1 to `DONE` once every loop has finished, step 4 has passed on the current `origin/develop` and every open PR's current head, or was skipped, and every action beyond the PRs is done
- send the final report per [updates](#updates)
- complete after the message is sent and every owner remains reachable for follow-up

## status file

`playground/orchestrations/<name>/status.md` in your checkout, where `<name>` is a short slug of the plan. you are its only writer. it is your memory, so reread it after compaction

update it before the matching chat message, whenever something material changes: a PR opens, finishes, merges or blocks, a merge unit becomes ready, a blocker appears or resolves, a deviation is decided, or a round count moves. edit it with your file-editing tool, not regex scripts

```md
WORKING
last updated: 28 Oct 14:32 GMT
[ready to merge](#ready-to-merge), [PRs](#prs), [needs you](#needs-you), [deviations](#deviations), [orchestrator memory](#orchestrator-memory)

## ready to merge

1. [#101](<url>) -> [#102](<url>) customer feed events: `gh stack merge 102 --squash --yes`
2. [#105](<url>) retry AI provider errors: `gh pr merge 105 --squash`

## PRs

⌛ waiting, ▶️ running, ⛔ blocked, ✅ finished, 🟣 merged

| | PR | stack | round | owner | blockers |
| --- | --- | --- | --- | --- | --- |
| 🟣 | [#100](<url>) feed events table | A | 2 | [pr00](<owner link>) | |
| ✅ | [#101](<url>) feed events model | A | 3 | [pr01](<owner link>) | |
| ▶️ | [#102](<url>) feed events UI | A | 2 | [pr02](<owner link>) | |
| ⛔ | [#103](<url>) weekly brief | B | 4 | [pr03](<owner link>) | [B1](#b1-<slug>) |
| ⌛ | PR 4 remove old machinery | B | | | |

## needs you

### B1: <question>

recommended: <answer>, ideally as a 1-click fix or exact command
alternative: <closest real alternative>

## deviations

- <plan said> -> <what happened>; why; decided by orchestrator|<PR> loop|user

## orchestrator memory

expand below

<details><summary>memory</summary>

</details>
```

- line 1: `DONE`, `COMPLETELY BLOCKED` when nothing can advance without the user, `PARTIALLY BLOCKED` when some work still can, or `WORKING`; no other values
- last updated: the output of `date '+%d %b %H:%M %Z'`, nothing else
- ready to merge: every current merge unit, as defined at the top, in merge order, each with its PRs, a 2-5 word name and the exact merge command; `none yet` when there is none. a unit drops off once merged
- status: 1 of the 5 legend emojis alone; any other state is text. add 1-3 words only when they say what the status can't
- PR: the PR link and a 2-5 word title, or `PR <n>` and the title before it opens. owner: a markdown link to its owner link, as defined at the top. blockers: the PR's `needs you` ids, each linked to its heading. cells hold nothing else; detail goes to memory
- needs you: only what the user alone can resolve, after you've tried every route. resolved items move into memory
- deviations: big decisions by you or the loops that depart from the plan, most important first. small in-loop deviations stay out
- memory: enough to carry on after compaction: plan location and amendments, wave and stack map, parent branches, absolute worktree and loop-dir paths, owners with their thread, session or agent ids, last verified head per PR, step 4 evidence, actions beyond the PRs and their owners, resolved blockers, next steps
- section links point only at headings outside `<details>`, since anchors don't expand it

## updates

the user follows the run through the status file. these rules override your harness's progress-update guidance for the whole run, including after `DONE`: codex commentary cadence, claude text between tool calls, and `wrap_up` recaps

chat messages are exactly these:

- start: 1 sentence naming the waves
- a new `needs you` item, ideally with a 1-click fix
- something that needs action now, such as a data or security exposure
- a new merge unit in `ready to merge`: 1 line naming it
- an owner's script-fix PR: its link
- the final report
- an answer to a user message

every message, including answers after `DONE`, starts with line 1 of the status file as a markdown link to the file's absolute path, so it opens in the harness: `[WORKING](/abs/path/playground/orchestrations/<name>/status.md)`

dispatches, rounds, waits, owner reports and pushes go to the status file only. an owner report or a finished background task isn't the user talking to you: update the status file and carry on without a message. claude: when the app makes you write something to end a turn, write only the line 1 link

say each question once, then keep running whatever doesn't depend on the answer

the final report is the line 1 link, 1-2 sentences of outcome, then a copy of every status file section above memory, with deviations and anything unverified in plain sentences

## helpers

read and follow [/helper-sub-agents](../helper-sub-agents/SKILL.md), with output under `playground/orchestrations/<name>/helpers/` and at most 5 at once. spawn one:

- before adding an owner's question to `needs you`, to check whether the plan, code or data answers it
- to diagnose a stuck or off-rails loop from its loop dir
- for step 4: the only helper that may commit, only to the throwaway branch, and never pushes
- for actions beyond the PRs assigned to you that take more than a few commands

you stay the only writer of the status file, and owners stay the only writers of their PRs
