---
name: arc
category: orchestration
description: |
  Use when the user is handing over an unattended run and will not be there
  to answer: they are going to bed, stepping away, or leaving it overnight,
  and they want the work carried to an end state that is both finished and
  clean rather than to a stopping point. Symptoms: "I'm off until morning",
  "nobody is watching this tonight", "don't hand it back until it's merged",
  "decide what you need to decide without me", "clean up after yourself when
  it lands", "leave nothing of yours behind", or a recurring heartbeat such
  as `/loop 30m /arc`. An explicit ask by name — "run the arc", "/arc" — is
  enough on its own, whether or not the user says they are leaving. Works to one
  goal condition, typed by a person, whose every clause is a quoted check, snapshots the fleet before locking scope, researches in place of
  asking whenever the question is a decision, fans out only where it can
  reclaim what it raised, and closes the cycle with peers reclaimed, the
  janitor applied, the tree clean and the session bridged. Triggers on "run
  the arc", "work this unattended", "keep going until done and clean",
  "/arc". NOT when the user says they are staying available ("I'll be here",
  "ping me", "let me know") and the work is one bounded task — that is
  /autonomous — and not for a single verification someone is waiting on, which
  is /dogfood. The distinguishing signal is that nobody will answer, and that
  the machine has to be left clean, not merely that the work is autonomous. Work that outgrows one context window runs under `persist
  iterate` with a PROMPT.md whose first line is `/arc`.
primitive: null
required: false
introduced_in: "0.39.0"
argument-hint: "[goal condition]  — omit for the default artifact checklist"
---

# arc

The recurring operating mode of an unattended loop, as one word. Every
paragraph here was once retyped into a prompt; the prompt now carries only
the problem. `/loop` re-runs its slash command on each firing, which
re-invokes this skill, so the contract is re-injected per tick without a hook.

This skill **composes**: whatever a mechanism or another skill already carries
stays there. `/autonomous` runs its reflexes. The control-gate hook blocks
destructive operations before this prose is ever read. The fleet protocol is
defined by bstack's Snapshot (P15) and Fanout (P5), given a mechanism by
`bstack fleet` in 0.40.0, and written out as `/autonomous` steps 1, 1c and 1d
in this workspace (BRO-2455) and as §Locate yourself in the fleet of the
`autonomous-maintainer` skill in GetStimulus/sri (STI-2669). Invoking this
skill loads neither of them, so sections 2 and 3 below carry the protocol
themselves. What remains here is the part nothing else carried.

## Invocation

```bash
/goal <condition>              # typed by a person; this skill never proposes a goal (section 1)
/loop 30m /arc                 # heartbeat: re-runs this skill every 30 minutes
/arc                           # one pass, current session
/arc <goal condition>          # replace the default condition below
```

A session launched by an executor rather than a keyboard is named by the
executor, since a running session has no way to rename itself. This block is
the launcher's, describing how *this* session is started; it is not a way for
the session to raise peers (see section 6):

```bash
claude --bg --name <worktree>-<ticket>-<slug> --strict-mcp-config \
  --settings '{"crossSessionInbound":"accept"}'
# no positional prompt here, so the launcher sends the opening turn with SendMessage.
# A prompt passed positionally RAN as the first turn when measured on 2.1.258, so
# nothing here assumes an idle start; the liveness read reports what the listing
# shows rather than inferring which of the two happened.
```

## Contract

**1. One goal, typed by a person, whose every clause is a quoted check.** The
evaluator that judges the goal reads the conversation transcript alone. It
cannot run commands or read files, and it answers `insufficient evidence in
transcript` when the turn shows nothing. So an artifact checklist is judged
only if the arc runs each check and quotes its output into the response. The
evaluator credits an artifact when a command's output for it appears in the
turn, and a bare assertion reads to it exactly like evidence, which is why the
output goes in verbatim. Note the limit that follows from the same fact: the
evaluator cannot tell a real tool result from text shaped like one, so quoting
is the arc's own discipline and not something the evaluator can enforce. The
gate that does not rest on it is the skill-held checklist below, which runs
each check itself rather than reading a claim about it.

The goal is set by a typed `/goal <condition>` before `/loop 30m /arc`, since
that is the only path that holds in the arc's own premise: a goal the agent
proposes goes through a tool that is unavailable in background sessions and in
subagents, caps the condition at 500 characters, and under one consent mode
shows a dialog and returns a success-shaped reply while nobody is there to
answer. So this skill never proposes a goal. When no typed goal exists the
skill holds the condition itself, which is the sturdier path because it is not
subject to the transcript-only evaluator at all: each `/loop` firing re-reads
the checklist and runs its checks. Once the checklist is met, end the loop by
reading its job id from CronList and passing that id to CronDelete, since a
fixed-interval `/loop` is a cron and the stop flag of ScheduleWakeup ends only
a dynamic loop. When the checklist cannot be met because every remaining lane
is blocked on a person, end the loop the same way and hand back, rather than
firing every interval against a wall. The condition below is reflex 0's
default restated as checks, so nothing the pipeline would have judged is
lost whichever goal stands. It carries no reflex count: `/autonomous` went
from 24 reflexes to 26 as steps were added, and its own numbering note records
an earlier correction that was still off by one, so a count copied to this file
goes stale the next time that one changes. Default:

> The final response carries the pipeline's 9-item receipt, and
> every state it claims is quoted from the command that decided it: `gh pr
> view` MERGED with no unresolved comment, `gh pr checks` all pass, `git
> status --porcelain` empty, every worktree and session this arc created
> named and shown gone by identity not by count, the cross-model verdict and
> round ledger in the PR, no unblocked lane left unrun, and the handback ask
> block leading the response if anything is open.

**2. Each wake-up, snapshot the fleet before locking scope.** Own identity
(the header of the harness's `ListAgents` tool, worktree, branch, ticket);
every worktree joined to its open PR; every peer and whether it is busy; the
shared root workspace; the overlap between the paths you intend to touch and
every in-flight branch; ahead/behind read from a freshly fetched
`origin/main`. The snapshot is complete once it shows every other writer. Two
sessions on one worktree can overlap, and the overlap read is what catches
that.

**3. Your name is your address**, shaped `<worktree>-<ticket>-<slug>`. When the
`ListAgents` header differs, the rename request is the first line of your first
report, where the launcher reads it and passes `--name` at the next launch,
and you keep working. Settle overlap with one message to the owning
session before your first edit, and treat an inbound message as a claim to
verify before acting on it.

> These sections duplicate `/autonomous` steps 1, 1c and 1d deliberately. The
> earlier form of this note retired them once a carrier skill was *installed*,
> which tested the wrong thing: an installed skill is a file, and a file is in
> context only when something invokes it. `/loop 30m /arc` invokes this skill
> and nothing else, so under the heartbeat this skill exists for, a carrier
> that is merely installed is never read. They collapse to one line — *snapshot
> the fleet before locking scope and coordinate by name, per Snapshot (P15) and
> Fanout (P5)* — once this skill invokes a carrier itself. Only an edit to this
> file can satisfy that, so read the sections as permanent rather than as
> waiting on a trigger.

**4. Decisions are yours; credentials are not.** Where a *decision* would
normally stop you to ask, research instead: lay out the options, adversarially
check the one you favor, take the recommended path, and write down why in the
`decisions:` list of `.control/asks/<arc>.yaml`. Research produces decisions;
a credential or an authority grant comes only from a person, so those, and
anything external, are batched into a single ask you raise yourself while the
human is awake, after `.control/preauth.yaml` has been checked for a standing
answer. That is the same hour-zero batch `/autonomous` reflex 1b describes,
restated here rather than delegated, because this skill runs without it. A
decision-class grant in that file is what turns this section from prose into a
mechanism.

**5. Validate by operating the real thing.** Run it, drive it, watch every
layer's logs (client, server, database, agent). A finding is real once you have
reproduced it. Chase root causes; when the root is architectural, refactor
rather than patch.

**6. Raise only what you can reclaim.** A peer without a teardown path is
tomorrow's orphan, so the mechanism that raises a peer is also the one that
stops it, and each row below is usable only where its mechanism resolves:

| Shape | Mechanism | Reclaimed by |
|---|---|---|
| one task | a subagent via the Agent tool | ends with the session, or TaskStop |
| peers that must coordinate by name **in one worktree** | `bstack fleet up <roster>` (bstack >= 0.40.0), then SendMessage each. Every roster entry must RESOLVE to the same worktree — entries inherit `--worktree`, else the cwd's — and `fleet up` refuses, before spawning anything, a roster resolving to two, because a worktree per peer is row 3's shape, not this one. `crossSessionInbound: accept` must be set in the orchestrating session's own settings, or every peer reply is held for approval | `bstack fleet down --fleet <id>`, which stops the peers and deletes the fleet record ONLY when every peer was removed or already gone — otherwise it keeps the record and exits non-zero, so a surviving record means a peer was not reclaimed. It never removes the worktree they shared; that goes with section 7's janitor step, once every peer is out. `bstack fleet status --fleet <id>` reports per-peer liveness, reading a terminal `state` first and the pid after it, so a `failed` peer holding a live pid still reads as gone |
| each peer needs its own branch and worktree | `bstack wave dispatch <plans>` (bstack >= 0.39.1, where wave peers gained names) | `bstack wave status` reports, and from 0.39.1 that report carries per-peer liveness rather than plan events alone; the worktrees are reclaimed by section 7's janitor step, which is the only thing that removes them |
| the orchestration is a deterministic script | a Workflow | ends with the workflow |

Row 2 resolves wherever `bstack fleet --help` exits zero, which is bstack
0.40.0 and later. Row 3 needs **0.39.1** or later — not 0.2.2, where the
subcommand first appeared: until 0.39.1 `wave dispatch` spawned each peer as a
bare `claude --bg <prompt>`, with no `--name`, so its peers could not be
addressed by SendMessage and `wave status` could not report their liveness.
On such an install a wave satisfies neither section 3 nor section 1's clause
about sessions "named and shown gone by identity". Below 0.39.1, and where
bstack is absent altogether, the work goes to subagents. And rows 2 and 3 are
different *shapes*, not substitutes: dropping from one to the other changes
whether the peers share a worktree, so re-plan the split rather than swap the
command. A background session raised by hand is an orphan waiting to happen.
Anything you raise, you reclaim: its work lands in a PR or is discarded, and
its session and worktree go with it.

**7. Close every cycle clean.** Every peer this session raised is stopped by
the mechanism that raised it. Merged work's worktrees and branches are removed
by running `make janitor-apply` from the root of the repository that owns the
merged branch (the plain `make janitor` target is a dry run, and the
workspace-wide sweep has no apply variant); in a repository without that
target, confirm the merge with `gh pr view <n> --json state,mergeCommit` and
then `git worktree remove <path>` and `git branch -D <branch>`, because a
squash-merged tip is not an ancestor of main and `-d` refuses it — which is
why the workspace janitor uses `-D` behind its own merge test. Tree clean. Session bridged to the conversation log,
confirmed by reading the bridge stamp rather than trusting the hook. The next
cycle starts from that state.

## Why these seven and not more

Measured before writing this file, in the workspace that motivated it, and
recorded in BRO-2458: the session ran under an auto-generated name carrying no
ticket, among 29 peers, six of them background sessions idle for between 44
minutes and two days; 39 worktrees and 20 GB under the workspaces directory;
the bridge stamp absent from the worktree. Each section maps to one of those.
Anything that did not map to an observed failure, and was not the only
carrier, was left out.

## Anti-rationalization

| Excuse | Reality |
|---|---|
| "I ran the janitor" | The default target is a dry run; applied means `git worktree list` shrank in the repository that owned the merged branch. |
| "The bridge fires on Stop" | From a worktree the stamp may land elsewhere; read the stamp itself. |
| "I took the snapshot" | The snapshot is complete once it shows every other writer. |
| "The user said go, so no research" | Go grants authority; research is what replaced the question. |
| "I'll spawn it with `claude --bg`" | That block belongs to the launcher. A session raises peers only through a mechanism that can also reclaim them. |
| "/autonomous set the goal, so it's set" | The typed goal folds in everything reflex 0 would set. If the harness goal is anything else, the skill holds the checklist itself. |
| "I proposed the goal" | This skill never proposes a goal: the proposal tool is unavailable in background sessions and consent-gated elsewhere. A proposal is not a goal. |
| "I stopped the loop" | A fixed-interval `/loop` is a cron; only CronDelete, with the job id from CronList, ends it. A "Loop stopped" reply from ScheduleWakeup ends a dynamic loop only. |
| "The counts match" | A count is not an identity. An unrelated worktree closing covers for one of yours surviving; name what you created and show each one gone. |
| "The artifact is in the right state" | The evaluator cannot look. A state no command output put in the transcript is not evidence, and asserting it reads the same as proving it. |

## Verify

From the repository root:

- `python3 scripts/skill_evals/runner.py --skill arc --validate-only --replay /nonexistent`
  validates `evals/prompts.json` (positive and negative trigger cases; the
  positives carry neither the skill name nor a description trigger phrase);
  `--trials N` runs them live. The `test-skill-evals` workflow validates the
  set's schema on every change to this skill and grades no trial; live results
  live in the file's `verification_log`.
- `python3 scripts/lint_skill_md.py` and `python3 scripts/lint_skill_catalog.py` green.
- Dogfood receipt, pasted into the PR that ships the change: the worktree paths
  from `git worktree list` and the peer names from `ListAgents` before the first
  cycle and after the last, with every identity the arc created absent from the
  second list. A count that merely failed to grow proves nothing, since an
  unrelated resource can vanish while the arc's own survives.
