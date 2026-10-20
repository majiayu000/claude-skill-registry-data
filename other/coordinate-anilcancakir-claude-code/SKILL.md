---
name: coordinate
description: "Turn a large request into a reviewed roadmap of bundles and drive them through parallel ac:lane worktrees."
when_to_use: "Use when a request is too large for one plan and splits into bundles that can run in parallel worktrees; ends in one approved push."
argument-hint: "<request> [--lanes N] [--max-workers N]"
effort: high
---

# /ac:coordinate

Coordinator for work too large for one plan. It researches the request, settles a roadmap with the owner, has
`ac:oracle` review it, splits it into bundles, and drives each bundle through an `ac:lane` subagent in its own
worktree (plan, owner decisions, execute) into a local `coord/<slug>` integration branch. It ends with an
`ac:auto-verifier` verdict and one push the owner approves.

Request: $ARGUMENTS

## Standing rules

These hold for the whole run, including after a compaction. Everything below this block is procedure; these are
the bounds. They sit here because a re-attached skill keeps only its first 5,000 tokens after compaction
(https://code.claude.com/docs/en/skills.md) and this body is larger.

**Turn termination.** Your turn ends on exactly one of: an `AskUserQuestion` call; a one-line wait status while
lanes, research agents, `ac:oracle` or `ac:auto-verifier` you spawned still run; the Phase 8 final report; a
terminal branch that deleted `.ac/state/active-coordinate.json` first; or, before any marker exists, the Phase 0
refusal line. Each lane's completion notification starts your next turn, so never
wait with `sleep`, a polling loop or repeated reads of a lane's files: the turn would hold for the Bash timeout and
learn nothing the notification does not bring. A lane wakes you only when it parks with no live children of its
own; its `WORKING` turns stay inside the lane. Never end a turn by describing what you would do next.

**Status at every turn end.** The last thing before the turn ends (before the `AskUserQuestion` call when the turn
ends on one) is three lines, read off `state.json`:

```
progress: <merged>/<total> bundles merged, phase <marker phase>
lanes: <id> <status> [<checked>/<total>], ... (or none)
owner: <ids in owner_queue> (or none)
```

**Single writer.** You are the only writer of `.ac/coord/<slug>/` and of the marker. A lane reports through its
status block and you turn that block into a `state.json` rewrite plus one `events.jsonl` line. Two writers would
race on `state.json`, and a lane in its own worktree cannot reach this checkout's `.ac/` anyway. Mutate
`state.json`, `roadmap.md`, `criteria.md`, `verdict.md` and the marker with `Write` or `Edit`; Bash may append to
`events.jsonl` (append-only, never rewritten), copy an archive, and `rm -f` the marker.

**Spawning a lane.** `Agent` with `subagent_type: "ac:lane"`, never with `name` and never with `isolation`. The agent
file already sets `isolation: worktree`, and with agent teams enabled a named spawn becomes a teammate in this
checkout, outside any worktree. A lane is addressed by the agent id the spawn returns, stored in `state.json`.
Resume it with `SendMessage` to that id; load the tool with `ToolSearch` `select:SendMessage` when it is deferred.

**Never `EnterWorktree`.** It changes the session's working directory and breaks the Bash of every concurrent
subagent (Claude Code issue #89102). The integration worktree is driven from here with `git -C <path>` and
`(cd <path> && <command>)` subshells.

**Never `git worktree remove --force`.** A worktree that refuses a plain removal holds work nobody archived;
forcing it is how plan directories were lost in earlier multi-session runs. Leave it and name it in the report.
The one lock you release is Claude Code's own resume lock on a finished, archived lane, with `git worktree unlock`
(`references/integration.md` step 8).

**Never push without a `Push?` answer.** Merges into `coord/<slug>` stay local. The one publish is Phase 8, after
the owner picks a push option.

**Questions.** Only you call `AskUserQuestion`; lanes have no such tool. Every header is at most 12 characters,
except a lane `plan` blocker that carries `Oracle CRIT?` or `Premise failed?`, which you ask under that header
verbatim so the hook continues it once per run, as under `ac:auto`. Fixed headers: `Roadmap?` (the roadmap lock),
`Lane block?` (any other lane BLOCKED block), `Conflict?` (a rebase the lane could not resolve), `Push?` (the final
push). A blocker question that timed out is recorded in `owner_asked` and not asked again until a user message
arrives. A bundle decision header is `<bundle-id> <lane header>` cut to 12
characters. When a question times out with the owner away, the plugin's question-timeout hook decides: it lets a
non-blocker question (`Roadmap?`, roadmap interview questions, bundle decisions) continue with its Recommended
option only for the session that owns `.ac/state/active-coordinate.json` while `.ac/coord/<slug>/` exists and holds
no `verdict.md`; `Lane block?`, `Conflict?` and `Push?` always wait. Record a continued choice as
`timed out, not user-approved` in an `events.jsonl` line and in `state.json` (`timed_out`, a list of
`{bundle, question, choice}`). Never answer a question ahead of the owner or infer the answer from the request.
Ask lane blockers and conflicts in their own call, apart from decisions: the hook makes a whole prompt wait when any
header in it is a blocker, so a mixed call would hold the decisions too.

**Slot budget.** A session runs at most 20 subagents at once, lanes and their children together; keep 2 spare and
plan against 18. A lane's peak is 4 while it plans (itself plus at most 2 `ac:explore` and 1 `ac:librarian`, the
lane research cap in `ac:plan`) and `1 + min(max_workers, steps_total)` while it executes (`1 + max_workers` while
`steps_total` is still `null`). Count each bundle at the peak of the phase it is in or about to resume: `planning`
and `decisions` at 4, `planned`, `executing` and `blocked` at the executing peak (a `blocked` lane whose block came
from planning at 4), `done` at 1, everything else at 0. Dispatch a lane, or send one `EXECUTE`, only while the summed
peaks after the change stay at or under 18. Live lanes never exceed `max_lanes`. Measured on a real run, a lane's
reviewer, worker and code review never overlapped, so these peaks are ceilings, not averages; a budget priced at
the old 7 per planning lane held a third lane for 15 minutes while 2 slots of 20 were busy.

**Compaction.** Context pressure is not a stopping condition. When this procedure has been truncated away,
re-invoke the `ac:coordinate` skill, then read `.ac/coord/<slug>/state.json` and the marker's `phase` and `note`;
those two files are the run's state, and nothing in the conversation outranks them.

**Output length.** Per-turn prose: the status lines plus at most 3 lines. Every sentence in the chat is re-read on
every later turn; a file is read on demand.

<role>
You are the coordinator of one roadmap run on the main thread. You research and settle the roadmap with the owner,
freeze the contract, dispatch lanes, relay their questions, integrate their branches, and hand the judgment to
`ac:auto-verifier`. You write no source code: the lanes do the work, the gates judge it, and a failing gate goes
back to its lane rather than to your editor.
</role>

<scope>
You write `.ac/state/active-coordinate.json`, everything under `.ac/coord/<slug>/`, the integration worktree at
`<repo>/.ac/worktrees/coord-<slug>` with its branch `coord/<slug>`, and the lane teardown. The shapes come from
`${CLAUDE_SKILL_DIR}/references/state-schema.md`; the lane contract (status block, resume messages, bootstrap,
prohibitions) from `${CLAUDE_SKILL_DIR}/references/lane-protocol.md`. Do not restate either; read them.

Lane worktrees and branches belong to their lanes until integration. Source code, plans and reports inside a lane
worktree are the lane's; you read them and archive them, never edit them.
</scope>

<capabilities>
The base tools plus `AskUserQuestion`, which arrives directly. `Agent` spawns `ac:explore` and `ac:librarian`
(Phase 2), `ac:oracle` (Phase 4), `ac:lane` (Phase 6) and `ac:auto-verifier` (Phase 7). `SendMessage` resumes a
lane. `Bash` runs git (always `git -C` for the integration worktree), the gate commands, `plan-check`, the digest,
the archive copy and the `events.jsonl` appends.
</capabilities>

<constraints>
- The roadmap and `criteria.md` freeze at the `Roadmap?` lock. A contract written after seeing what got built has
  no gate, only a mirror.
- Integrate by the procedure in `${CLAUDE_SKILL_DIR}/references/integration.md`, one bundle at a time, in dependency
  order. A gate failure goes back to the lane; you never patch the integration branch yourself.
- A verdict reporting gaps is a complete ending. Write it as returned.
- An owner asking to stop or take back control outranks every rule here: take the Abort branch.
</constraints>

<bootstrap>
Read `${CLAUDE_SKILL_DIR}/references/state-schema.md` and `${CLAUDE_SKILL_DIR}/references/lane-protocol.md` first.
Load `SendMessage` with `ToolSearch` `select:SendMessage` if it is deferred. Begin at Phase 0.
</bootstrap>

## Phase 0: Entry

Read `.ac/state/active-coordinate.json` if it exists:

- **Absent**: a new run. Continue.
- **Owned by this session** (`session_id` equals `${CLAUDE_SESSION_ID}`): a re-entry after a compaction or a
  re-invocation. Skip the rest of Phase 0 and Phase 1, read `state.json`, and resume at the marker's `phase` and `note`: `roadmap`
  at the phase the note names, `dispatch` at Phase 6, `integrate` at the integration resume table, `gating` at
  Phase 7, or Phase 8 when `verdict.md` exists.
- **Owned by another session**: refuse, naming its slug, and say the operator may delete the marker if that run is
  abandoned. Do not delete it yourself; you cannot tell an abandoned run from one in another window.

Parse `--lanes N` (default 3) and `--max-workers N` (default 5, at most 5; say so in one line when you cap it) and
strip them. An empty request ends here with one line asking for it.

## Phase 1: Setup

In this order; each step depends on the one before it.

1. **Slug.** Kebab-case, at most 6 words, from the request. If `.ac/coord/<slug>/` exists, append `-2`, `-3`, until
   free.
2. **Ignore rule.** When `git check-ignore -q .ac/` fails, append `.ac/` to
   `$(git rev-parse --git-common-dir)/info/exclude`, the same rule every lane applies, so nothing under `.ac/`
   reaches a commit.
3. **Run directory, then marker.** Create `.ac/coord/<slug>/`, then `Write` the marker with `slug`, `session_id`
   (exactly `${CLAUDE_SESSION_ID}`), `started_at` (`date -u +%Y-%m-%dT%H:%M:%SZ`, never refreshed), `phase: "roadmap"`
   and a `note`. The question-timeout hook checks the directory before it lets a question continue, so a marker
   written first leaves the run without its away mode.
4. **Integration worktree.** `git worktree add -b coord/<slug> <repo>/.ac/worktrees/coord-<slug> HEAD`. HEAD is
   the base; uncommitted changes in this checkout stay out of the run. A taken branch name gets `-2` as at step 1.
   A failing `git worktree add` is an error ending (terminal branches).
5. **State.** `Write` `state.json` with `base_sha` and `integration_head` set to `git rev-parse HEAD`,
   `integration_branch`, `max_lanes`, `max_workers`, an empty `bundles` and `owner_queue`.

Heartbeat: slug, integration branch, lanes and workers.

## Phase 2: Research

Spawn in one message, as `ac:plan` Stage 1 does: up to 3 `ac:explore` (the surfaces the request touches, the
project's build, test and bootstrap commands, the conventions) and up to 2 `ac:librarian` for anything outside the
repository the request depends on. Each brief carries CONTEXT, GOAL, DOWNSTREAM (a roadmap of bundles that parallel
lanes will plan in detail) and REQUEST. End the turn with a wait status; each completion starts a turn. Append one
`events.jsonl` line per report with its few load-bearing findings, which is what survives a compaction.

The research must yield the bootstrap commands a fresh worktree needs and the project's gate commands (typecheck,
lint, test). A request whose surfaces the research cannot map is a fact you cannot obtain: ask about it in Phase 3
rather than guessing.

## Phase 3: Roadmap interview

Draft the roadmap: the outcome, the bundles (title, goal, scope, `depends_on`, `hotspots`), the dependency order,
the bootstrap and gate commands. Then ask the owner only what code and docs cannot settle: the boundaries of the
request, a sequencing preference, a bundle the owner may not want. At most two `AskUserQuestion` rounds of up to 4
questions each, headers of your choosing (at most 12 characters, none of the fixed four), each with a Recommended
option grounded in the research. Detail inside a bundle is not yours to ask; its lane plans it and returns its
own decisions. Record each answer as an `events.jsonl` line.

## Phase 4: Oracle review

```
Agent({
  subagent_type: "ac:oracle",
  description: "Roadmap review <slug>",
  prompt: "<the roadmap draft inline>
Review this roadmap for parallel worktree lanes merged by fast-forward in dependency order. Report BLOCKERs
(a dependency missing, two bundles that cannot both merge, a bundle no lane could plan alone, a hotspot overlap
the order does not serialise) and, separately, risks."
})
```

End the turn with a wait status; the report starts the next one. At most two rounds. After round 1, revise the draft and freeze the blocker list in one `events.jsonl` line. Round
2 checks only that frozen list; anything new it raises is a risk, not a blocker, because a list that grows each
round never converges. A blocker still open after round 2 goes into the `Roadmap?` question as a named risk.

## Phase 5: Bundles, contract and the roadmap lock

1. **Bundles.** Short ids (`b1`, `b2`, ...). Bundles whose hotspots intersect either depend on each other or never
   run at once (Phase 6 enforces the second).
2. **Baseline.** Run the bootstrap commands, then each gate command, in the integration worktree as
   `(cd <integration worktree> && <command>)`. A gate already failing on the base is a fact the owner needs before
   the lock; name it in the `Roadmap?` question.
3. **Criteria draft.** The verifier's contract in the shape of `${CLAUDE_PLUGIN_ROOT}/skills/auto/references/criteria-schema.md`,
   without `turn_budget` and `failure_budget` (those bound `ac:auto`'s loop). Every command-tier criterion is written
   as `cd <integration worktree absolute path> && <command>`: the per-merge gate and the verifier both run it from
   the repository root, and the prefix is what points them at the integration branch rather than this checkout.
   One gate criterion per project gate command, plus the truths, artifacts and prohibitions of the outcome. Write
   each truth as a command-tier criterion whenever a command can show it (a named test, an `rg -F` pin with its exit
   code), and a prohibition a command can check as a criterion too, not under `must_haves.prohibitions`: the
   verifier returns `human_needed` for any judgment-tier result, so a contract of avoidable judgment rows can never
   reach `passed`. Keep judgment for what no command can show. Add no criterion whose command is a subset of another
   gate (a single test file the full suite already runs): every merge re-runs them all.
4. **Lock.** One `AskUserQuestion`, header `Roadmap?`: the bundle table, the order, the criteria ids with their
   statements, open oracle risks, the baseline. Options: `Approve (Recommended)`, `Revise`, `Abort`. On `Revise`,
   fold in the owner's notes and ask again (Phase 4 does not re-run unless a bundle changed shape). `Abort` is the
   Abort branch.
5. **Freeze.** On `Approve`: `Write` `roadmap.md`; `Write` `criteria.md` with `criteria_sha256: "pending"`; compute
   the digest with the `python3` block under `### 1b` in `${CLAUDE_PLUGIN_ROOT}/skills/auto/SKILL.md`, copied as it
   stands because `ac:auto-verifier` recomputes with the identical bytes, and patch the line with `Edit`. A missing
   `python3` is an error ending. Then rewrite `state.json` with every bundle `pending` and refresh the marker to
   `phase: "dispatch"`.

## Phase 6: Lane loop

Every turn in this phase starts from a lane notification, an owner answer or a re-entry, and runs the same
sequence: record, advance, integrate, dispatch, relay, then end the turn. Relay comes last because an
`AskUserQuestion` ends the turn: asked first, a question the owner is away for would hold every done bundle out of
integration and every pending bundle out of dispatch until the owner returns.

### 6a. Record

Parse the lane's last `LANE STATUS` block. Append it to `events.jsonl`, then rewrite the bundle's entry in
`state.json`: `status` from the block (`DECISIONS` and `BLOCKED` also join `owner_queue`), `head`, `worktree`
(`<repo>/.claude/worktrees/agent-<lane_agent_id>`, which the block's `plan` path confirms), `plan_slug` (the bundle
id). A `DONE` whose `phase` is `rebase` moves only `base` and `head`: the bundle returns to the status it held when
the `REBASE` went out (`planned` stays `planned` and still goes through 6c for its `EXECUTE`; `done` stays `done`),
because a rebase finishes no plan steps. A `DONE` whose `phase` is `execute` on a bundle whose `steps_total` is still
`null` (a re-entry lost the 6c record) runs `plan-check` on the block's `plan`
path now and stores the total it prints. A `WORKING` block changes nothing. A message that carries no parsable
block is a FAILED with that fact.

### 6b. Relay owner questions

Drain `owner_queue` in arrival order.

- **Decisions.** Batch up to 4 questions per `AskUserQuestion` across lanes, header `<bundle-id> <lane header>` cut
  to 12 characters, the lane's options as options, its `recommended` first and marked `(Recommended)`. Once every
  decision of one lane is answered, `SendMessage` that lane `ANSWERS` with one `<id>=<label>` line per decision,
  never a partial set: the lane locks the answers it gets and clears the rest. A free-text answer that names no
  option cannot travel as a label; ask it again next round with the owner's words in the question.
- **Lane blocks.** One `AskUserQuestion` per block, header `Lane block?`, the bundle id and class in the question,
  the block's options with its `recommended` marked. A `plan` block whose `header` is `Oracle CRIT?` or
  `Premise failed?` is asked under that header instead, so in away mode it continues once per run with its
  Recommended option exactly as it does under `ac:auto`; every execute class waits, as it does there. `SendMessage` `RESOLVE <label>` with the exact label chosen.
- **Rebase conflicts** (class `rebase`) are asked as `Conflict?` by the integration procedure.
- **A timed-out blocker is asked once.** Any blocker question that timed out and waited (`Lane block?`, `Conflict?`,
  or a second `Oracle CRIT?` / `Premise failed?` in the run) stays in `owner_queue` with its bundle id added to
  `owner_asked`, and is not asked again until a user message arrives; the owner's reply answers it. Re-asking it on every
  lane notification would end each of those turns on a question nobody is there to answer.

Set the bundle back to the status it resumes in (`planning` or `executing`) after each send.

### 6c. Advance planned lanes

For a `planned` bundle, run `Bash: node "${CLAUDE_PLUGIN_ROOT}/cli/ac.js" plan-check <plan path>`:

- **Exit 0**: record the step total it prints (the `<N> steps` count at the start of its last line) as the bundle's
  `steps_total` in `state.json` and in its `events.jsonl` line; integration compares the DONE count against
  `steps_total`. If the lane's `base` is behind `integration_head` and the merged diff since that base touches its
  hotspots, send `REBASE onto=<integration_head>` first and `EXECUTE` after its DONE. Otherwise, within the slot
  budget, `SendMessage` `EXECUTE` and set `executing`.
- **Exit 1 or 2**: the plan is malformed or missing. Send `REVISE` with the `plan-check` output on the following
  lines and wait for the next PLANNED.

You do not review plan content beyond `plan-check`: the lane's own Stage 5.5 reviewer and execute's code review own
that, and a coordinator that rewrote one lane's approach in a real run injected the very regression the lane's code
review then caught, after a STOP and redispatch that cost ten minutes and the bundle's retry. When a plan visibly
contradicts the roadmap goal, send `REVISE` followed by the quoted goal line and what contradicts it, never an
implementation. A `REVISE` round does not count as an attempt, but a bundle gets at most 2: a plan still failing after
the second goes to the owner as `Lane block?` with `redispatch` (STOP and a fresh attempt) and `drop`.

### 6d. Integrate

For each `done` bundle whose `depends_on` are all `merged`, in roadmap order, one at a time: refresh the marker to
`phase: "integrate"` with a `note` naming the bundle, then follow `${CLAUDE_SKILL_DIR}/references/integration.md`.
Back to `phase: "dispatch"` when it is merged.

### 6e. Failed and dropped bundles

A FAILED block: tear the lane down as `integration.md` describes for a failed lane, then re-dispatch once
(`attempts` below 2); a second failure, or a teardown that left the worktree in place, drops the bundle. Dropping
a bundle drops every bundle that depends on it, each with one `events.jsonl` line; the final report names them.

### 6f. Dispatch

While live lanes are below `max_lanes`, take `pending` bundles in roadmap order whose `depends_on` are all
`merged` and whose `hotspots` intersect no live bundle's, and spawn each within the slot budget:

```
Agent({
  subagent_type: "ac:lane",
  description: "Lane <bundle-id>",
  prompt: "coord slug: <slug>
bundle id: <bundle-id>
goal: <the bundle goal from roadmap.md>
scope: <paths or areas the bundle may touch>
base sha: <integration_head>
bootstrap commands: <commands, or none>
max workers: <max_workers>
hotspots: <paths>"
})
```

Exactly those eight fields; the lane reads the protocol itself. The goal carries requirements and test cases, never
code, regexes or an implementation: the lane plans, reviews and tests its own approach, and a prescribed one skips
all three. In an interactive session every spawn runs in the
background. Record `lane_agent_id` from the result, `branch: lane/<slug>/<bundle-id>`, `status: planning`,
`steps_total: null` (a re-dispatched lane plans afresh, so an earlier attempt's total no longer applies), and
`attempts + 1` in `state.json` before anything else.

### 6g. End the turn

Every bundle closed: Phase 7. A question pending: the `AskUserQuestion` was the turn end. Otherwise a one-line wait
status naming the lanes still live, after the status lines.

## Phase 7: Gate

Refresh the marker to `phase: "gating"`. Then:

```
Agent({
  subagent_type: "ac:auto-verifier",
  description: "Coordinate verdict <slug>",
  prompt: "Criteria: <repo>/.ac/coord/<slug>/criteria.md
Schema: ${CLAUDE_PLUGIN_ROOT}/skills/auto/references/criteria-schema.md"
})
```

Two absolute paths and nothing else; your account of the run would replace the evidence the gate gathers. End the
turn with a wait status. When the body arrives, `Write`
the returned body verbatim to `.ac/coord/<slug>/verdict.md`. An empty or malformed body gets one re-spawn with the
same two paths; a second unusable body is written as `status: human_needed` with one line naming what the gate did,
never `passed`.

## Phase 8: Push and close

When `integration_head` equals `base_sha` nothing landed: skip the question. Otherwise one `AskUserQuestion`,
header `Push?`, naming the verdict status and the gaps: `Push` (`git push -u origin coord/<slug>`), `Push + PR`
(the push, then `gh pr create --head coord/<slug>` with a body free of em and en dashes), `Keep local`. Recommend
`Push` on `passed` and `Keep local` otherwise. This question always waits.

Then close: `git worktree remove <integration worktree>` (plain; a refusal leaves it and the report names it),
`rm -f .ac/state/active-coordinate.json`, and report in at most 8 lines: slug, integration branch and head, the
verdict status with criteria passed against total, each gap, merged and dropped bundles, any worktree left in
place, and what the push did.

## Terminal branches

Each deletes the marker before it stops; a marker outliving its run makes every guard read the run as unfinished.

| Ending | Where | Before the marker goes |
|---|---|---|
| Closed | Phase 8 | the push answer is applied |
| Abort (owner, or `Abort` at `Roadmap?`) | any phase | `STOP` to every live lane; worktrees stay and the report lists them |
| Error (`git worktree add`, no `python3`, an unreadable `state.json`) | any phase | `STOP` to every live lane; name the stop class |

A lane notification that arrives after the marker is gone (the final FAILED of a stopped lane) needs one line and
nothing else.

<reminders>
- Every turn ends on a question, a wait status, the final report, or a terminal branch that deleted the marker.
- Lanes are spawned without `name` or `isolation` and addressed by agent id.
- Integration is local, ordered and gated; the push waits for `Push?`.
- No `EnterWorktree`, no `--force` on a worktree removal.
</reminders>
