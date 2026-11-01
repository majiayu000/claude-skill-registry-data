---
name: orchestration
description: "Leads Puck lanes and partners. Use for briefs, choosing agents or Codex models, landing lanes, Antigravity, GPU and build scheduling, idle partners, routing findings; review-passes runs passes."
---

# Orchestration

This skill is the lead's procedure for coordinating assignments, machines,
merges and reviews. [AGENTS.md](../../../AGENTS.md) owns branch authority and
repository rules; this skill routes verification and review execution to their
owners. The user's current instruction outranks this skill; a rule that argues
against a requested change is stale and is corrected in the same change. What
the owner says in a session overrides this skill and is written into it in that
session.

Load [lane work](references/lane-work.md) before branch operations, delegation or a long run; it owns the detailed procedures.

## Plan from the milestone

Plan backward from the milestone's critical path. Find the least-prepared item
on it and put the best-fit partner there. Busy is not progress: never queue
filler to make a partner look busy. Idleness is a prompt to re-read the path, not
to create work.

## Spend verification, not writing

Writing is cheap and verifying is expensive: builds, boots, suites and GPU
windows on one shared machine set the pace, so the work in flight is bounded by
what the machine can verify. The owner's direction:

- **Review before landing where a defect does damage before review lands.** Code
  that deletes files, crosses a trust boundary (grants, federation, admission,
  credentials) or rewrites persisted data gets its cross-family review before it
  lands; everything else lands on its evidence and is reviewed alongside. A
  pruning change that could delete outside its install root and a cap that
  trusted the sender both landed first and had to be reverted or refixed.
- **The lead's verification window outranks lane legs.** Windowed checks owed by
  several lanes are one session the lead runs with GPU priority; it is never
  queued behind the lanes it verifies.
- **Speed claims get a quiet window.** The machine is never idle while lanes
  run, so the lead holds a short quiet window at a natural pause (lanes parked at
  WIP commits) to re-measure the speedups landed since the last one; a speed
  claim stands only once measured there.
- **An Antigravity lane is bounded and always reviewed before it lands**: its
  output has carried fabricated claims and high findings.

- **Batch, including unrelated areas.** Several lanes work independent areas at
  once, and the integration lane verifies them together in one sweep of the
  debug world
  ([decision](../../../docs/decisions/engine-design.md#the-debug-world-is-the-engines-instrument)),
  which also shows breakage in partner systems that a single-feature check
  misses. Isolate a change only for a benchmark against a baseline, a
  determinism or fixed-point change, or a regression hunt.
- **Brief along the whole path a change travels**, not one system: the lane maps
  the systems its change reaches (`puck references`, the owning skills) and
  checks those partners before handing back.
- **Review adversarially across families, concurrently.** An engine change's
  cross-family review is required and never blocks landing. A Claude author's
  change is reviewed by Codex, a Codex author's by Claude, and Argon takes
  security, large-context and UI reviews. The reviewer gets the diff and the
  author's claim, not the author's reasoning, and tries to break it with a repro,
  a counterexample or a missed caller. Review depth follows risk: determinism,
  maths and renderer changes get an Astra- or `principal`-grade reviewer, ordinary
  engine code Sol or `specialist`, docs and world content none or a scout's
  spot-check.
  - The author starts its next item when it hands back and is never paused; the
    change lands in its batch whether or not the review has finished.
  - Findings go into the open items'
    [work packets](../../../docs/plans/open-items.md#work-packets), each with its
    severity, one owner, its file and line and its failing case. Filing a
    finding places it: into the packet that shares its cause or area, or into a
    new packet with an owner role and a next action, never a list of its own. A
    high finding goes to the top of [Next](../../../docs/plans/open-items.md#next)
    and so into the next integration batch.
  - The reviewer's fixes are a follow-up branch of their own in that batch
    (review-and-fix, [`review-passes`](../review-passes/SKILL.md)), never edits
    to the author's branch.
  - The integration lane may revert a landed change when leaving it in is worse
    than removing it.
  - The only blocking review gate is before the owner pushes `main`: every high
    finding from the milestone is resolved or explicitly deferred by the owner.
- **One integration lane, fed in batches.** It is the only heavy job on the
  machine. It takes ready branches and batches unrelated changes together on
  purpose; it isolates a change only for a benchmark against a baseline, a
  determinism or fixed-point change, or a regression hunt. It merges the batch,
  builds what the merge touched, runs the batch's sweep, bisects a red batch, and
  hands the lead the green head to fast-forward
  ([land in batches](#land-in-batches)).

## Own tracks, not tasks

Partners own tracks and outcomes. A brief gives the outcome and the
constraints, never the method, the design or the order of the edits. A partner
picks its next work from its track or a shared ready queue and announces it. The
lead keeps cross-track conflicts, merges, owner-level calls, and scope and
order. Every brief ends with the partner's own next one or two items, and the
partner works its queue without waiting for the lead between items. A wait (a
GPU leg, the next batch) blocks the lane, never the partner: the
partner takes its next item from its track or the ready queue and announces
it. A queue the
partners cannot read is no queue: keep the lead's queue where partners can reach
it, or delegate it to them. Every queue item has exactly one recorded owner, and
a handoff records the new one; an item with two owners is a defect to resolve
before either partner continues.

A delegated lane does its brief itself and starts no sub-agents of its own. A
lane that fans out hands back before its children finish, their reports never
reach it, and the integration it owed falls to another round. When work splits,
the lead splits it into lanes.

## Write and track assignments

[Lane work](references/lane-work.md#delegated-work) owns what a brief holds and how
shared-file edits are sequenced; its report shape is the three headings that
[Running long tasks](references/lane-work.md#running-long-tasks) names. Add to every
brief:

- an id, used in the brief file name, the commit trailer and every message;
- the base commit, verified by the lead before the brief goes out;
- a fresh read of the worktree's AGENTS.md and owning skill, correcting stale
  startup repository text while preserving current owner and system precedence.

When a lane demonstrates stale-rule behavior, the lead starts a fresh session
before launching its continuation. Editing a skill alone does not require a new session.

Verify each premise of a brief yourself before sending it; a wrong premise costs
every lane that received it. When a brief proves wrong, recall every lane working
from the same premise before replying to the lane that found it, and say that a
stop is a stop, not a pause.

Verify any base claim yourself with
`git merge-base --is-ancestor <base> <integration-head>`, checking its exit
status, and count the commits behind with
`git rev-list --count <base>..<integration-head>`
([why a two-dot range is not ancestry](../verification/SKILL.md#branches)).

Only the assignment's last commit carries one of these trailers, as the last
line of its message:

```text
Brief: <id> done
Brief: <id> blocked: <question>
```

Progress and WIP commits carry no `Brief:` trailer, and no other value follows
`Brief: <id>`. The lead checks the final commit's trailer and subject format
before merging a lane.

The lead's ledger and plan files that a delegate never writes are the lead's
own scratch checklists under `<worktree>/.claude/scratch/<lane>-*`. The repository's documents,
`docs/plans/open-items.md` and the plans under `docs/plans` among them, belong
to no one lane: a delegate edits them for what its change delivers, deleting an
item it closed (after moving the durable fact it carries to its owning home),
placing what it found and left into a work packet, and correcting text its
change made stale, and the brief says so.

The message is the notification; git is the record. Inspect the reported
changes and what the lane ran to show them working before merging
([landing bar](../verification/SKILL.md#the-landing-bar)).

## Land in batches

A lane is ready when it meets its own focused checks
([landing bar](../verification/SKILL.md#the-landing-bar)): it builds what it
touched, its commit body says what it ran to show the change working, and it has
merged the integration tip. A ready lane joins the integration lane's next batch
and is held for nothing else: not another lane, not its review. The integration
lane merges the batch, builds what the merge touched, runs the batch's sweep and
bisects a red result; the lead fast-forwards the integration branch to the green
head. "What the merge touched" includes what consumes it:
- a change to a shader, interface or generated header builds `Puck.slnx`, test projects included;
- a change to a world document runs the shipped-source suites (`Puck.World.Transpiler.Tests`, `Puck.Cli.Worlds.Tests`) and shows itself in the sweep;
- a change to simulation state, maths or determinism also runs the `worlds/debug/*-tests.puck` files it touches with `--reproduce`;
- every check runs from a CLI and test binaries rebuilt after the merge, never stale copies.

The sweep is the batch's proof: the whole debug world, every signal compared with
the previous sweep ([decision](../../../docs/decisions/engine-design.md#the-debug-world-is-the-engines-instrument)).
`puck sweep --tour --baseline <previous report.json>` runs it under the GPU lease
(or `--attach` names a World `puck_world_start` started) and writes the report
and contact sheets ([CLI reference](../../../docs/reference/cli.md#puck-sweepthe-debug-worlds-sweep)).
The full debug-world replay (every test world, about 45 minutes) is the
integration lane's next heavy job after a batch lands, never beside another heavy
job and never a condition of a landing (the owner's ruling: "The whole idea was
to be EFFICIENT"); what it finds is ordinary work for the next lane. A red check
on the integration branch is the next piece of work, not a reason to stop
landing, and the integration lane may revert a landed change when leaving it in
is worse than removing it.

The open items are the batches' queue
([work packets](../../../docs/plans/open-items.md#work-packets)):
- each batch's lanes take the top packets of its
  [Next](../../../docs/plans/open-items.md#next) list, one packet a lane, with
  any high finding first;
- the lead re-ranks Next at each batch by payoff, folding in what the batch
  landed and what its sweep and reviews found;
- a finished packet is deleted, not ticked, and so is a closed sub-point, once
  the durable fact it carries is in its owning home (AGENTS.md rule 9);
- a programme's phase-scale work stays in its plan's open items, and a packet
  points at it.

### Coding lanes and the integration lane

Heavy verification runs in one place, one job at a time; this is the owner's
direction, after concurrent whole-solution builds exhausted the machine's memory.
- **Coding lanes** build only the projects they touch, with `-m:2`, and run only
  their focused tests. They run no whole-solution build, no full suite and no
  GPU leg, and they hand back a branch that builds and passes those tests.
  Several run at once (the owner's direction: don't over-serialize for
  memory), within the WIP limit: about three building writers, one heavy
  integration job and one GPU leg. A windowed debug World holds about 10 GB of
  working set (15 GB private) within a minute of boot. On a 32 GB machine, while
  one runs, only a couple of building lanes fit beside it. Keep windowed capture
  batches short (boot, capture, stop), and tune on a headless World. A lane that
  runs scenario files (`puck test <file>`) names the files and passes `--jobs 1`:
  this serializes headless worker processes, including reproduce replicas, with
  one independent native host live at a time, where a higher `--jobs` beside a
  replay can exhaust memory and kill it. Every brief, a read-only review's
  included, says so.
- **Reaping** is prevented by that limit, because Claude Code reaps background
  jobs when memory runs critically low. A reaped lane is handled once: the lead
  saves its tree as a WIP commit, removes the cause, and restarts it with a
  continuation note. A second reap of the same lane stops it; it goes into its
  work packet in the open items with what was running, and the owner decides.
- **The integration lane** is one long-running lane. It takes ready branches in
  the order the lead names, batches unrelated changes together on purpose,
  merges each batch onto its own staging branch, and resolves generated-file
  conflicts by running their generators. It builds `Puck.slnx` when the merge
  reaches shared projects. Then it runs, once on the merged result, the builds
  and suites that [the merge touched](#land-in-batches) and the batch's sweep:
  the whole debug world as the
  [instrument decision](../../../docs/decisions/engine-design.md#the-debug-world-is-the-engines-instrument)
  defines it, every signal it produces compared with the previous sweep, plus
  the workloads the batch's changes declare. Under a granted GPU leg it reads the
  windowed frame-time and patrol readings
  ([landing bar](../verification/SKILL.md#the-landing-bar)); the lead first
  clears the machine of other lanes' builds, suites and World runs for the quiet
  frame-time reading. It reports green or
  red per batch and splits a red batch to find the culprit. It also lists each
  branch's deleted files (`git diff --diff-filter=D` against the integration tip)
  and compares them with what the brief allowed. A deletion the brief didn't name
  is reported to the lead before landing, never merged silently.
- **Briefs** that allow deletion say what may be deleted. A finding capture names
  its settle state: bakes settled and irradiance settled, or marked partial. A
  capture taken before settling can't support a lighting finding.
- **The lead** fast-forwards the integration branch to each green staging head,
  routes a red result back to the lane that owns it, and decides any merge
  conflict that needs judgement.

A ready branch is never held back for others to arrive. A lane that cannot land
alone is a dependency to name in the brief. Review follows its own rule
([spend verification](#spend-verification-not-writing)): it runs beside the
batch and never holds a branch or its author. Gates, parity, canaries and
counters checks run when the owner asks for a qualification, on the head the
owner names.

Use [verification](../verification/SKILL.md#what-uses-the-gpu) for GPU grants,
lease acquisition, time boxes and failure handling. Load it before a GPU leg or
classifying a flake. Investigation of a failure is a lane of its own.

### Launch capabilities

This table describes configured capabilities and known launch behavior; a grant
is not proof a command succeeded. Record runtime probes in the landing commit.

| Launch | Network | Git writes | Push | GPU | MCP | Hooks | Skills |
|---|---|---|---|---|---|---|---|
| Native `codex exec` | Configured on | Own-branch commits; checkout and common Git directory granted by profile | Refused for a lane | Lead grant and lease | Project `puck` registration | Current definitions trusted through `/hooks` | `.agents/skills` link |
| Codex companion `task --write` | Sandbox has no network | `workspace-write` excludes Git; lead commits | Refused | No sandbox GPU; lead verifies | Project `puck` registration | Same per-user trust, on supported tool paths | Same link |
| Claude worktree agent | Harness permissions | Own-branch commits; own-tree isolation | Refused | Lead grant and lease | Shared `puck` server | Project registration | `.claude/skills` |
| Antigravity `agy -p` | Terminal sandbox has no network | Own-branch commits | Refused by git-safety | No sandbox GPU; lead verifies | Workspace plugin registration (server `puck_operator`) | `.agents/hooks.json`; hooks start in `.agents/` | `.agents/skills.json` |

A native Codex lane commits directly; git-safety and git.rules guard shared
state. Linked worktrees need a grant to their separate common Git directory
and the main checkout's shared lease directory; discover them rather than
requiring one machine's checkout path. An untrusted Codex hook is skipped:
review and trust each current definition and re-review changed definitions.
Hooks cover supported activated tool paths, not every possible execution path.
See [machine setup](../../../docs/development/contributing.md#setting-up-a-machine).

Codex and Antigravity resolve their hooks from the worktree they run in, so a
branch older than the current `.claude/hooks/` has none, and Codex runs a command
whose hook fails. Claude Code runs the main session's
`${CLAUDE_PROJECT_DIR}/.claude/hooks` for every worktree agent, whatever the
agent's branch holds. Before handing an old branch to any lane (its skills and
rules come from the branch too), the lead merges the integration tip into it,
leaving any conflicts for the lane to resolve. A worktree another agent
created can deny a Codex lane its `.git/worktrees/<name>` writes; give the lane a
worktree the lead creates.

Before launching Codex in a main checkout or fresh worktree, build/copy its CLI
as [verification](../verification/SKILL.md#run-verbs-from-your-own-cli-copy)
describes and run `dotnet <lane>-cli/Puck.Cli.dll agents link` there. Then launch
`codex exec --cd <worktree> -m <model> -c model_reasoning_effort='"<effort>"' "$(cat <brief>)" < /dev/null`.
Without the `< /dev/null`, a background launch can stop at "Reading additional input from stdin..." and never
start. Keep the output in a lane-named log. A resumed Codex session retains its launch
sandbox; after changing permissions, start a fresh continuation instead of
`--resume-last`. Companion restrictions are specific to `task`, not native exec.

A Codex lane that needs the `puck` World tools launches without `--sandbox` (the
project's `puck` permission profile) or with `--sandbox workspace-write`. Under
`--sandbox read-only` the same prompt that lists all eight `mcp__puck__*` tools
in those two launches lists none of them, though the project registration is
enabled (`codex mcp list`), the launcher runs (it installs the worktree's
`.claude/mcp-install`) and other servers stay visible (probed with codex-cli
0.164). A read-only review lane therefore reads sources and cannot drive a World.

An Antigravity lane runs `agy -p "$(cat <brief>)" --output-format text` from
its worktree, without `--mode`: headless flag validation rejects `--mode auto`
before sign-in, while the user-level `agentMode: "auto"` applies afterwards.
Auto mode ignores the ask list; git-safety refuses pushes and shared-state Git
operations. A headless run executes only commands its user-level allow list
names. The owner-approved list allows every command
([contributing](../../../docs/development/contributing.md#antigravity-user-settings));
a machine whose list names only `git`, `dotnet`, `pwsh` and `node` auto-denies any
other command, such as `rm` or `Remove-Item`, and the run ends with no output, so
a brief that deletes files says to use `git rm`. A headless run also ends when the agent
goes idle waiting on a background task of its own (a background build), leaving
its edits uncommitted, so a brief tells it to build and test in the foreground.
A headless run can also stall with its process alive and its log empty, so the
lead watches the lane's worktree for file writes and applies [no bad
loops](#no-bad-loops). The home policy is the block contributing
records; login and trust material stay local. The workspace plugin exposes the MCP
configuration because a bare `.agents/mcp_config.json` is not a discovery root.

Antigravity lists the `puck_operator` tool names in its context and loads their
input schemas lazily, from `<appDataDir>/mcp/puck_operator/<toolName>.json`; it calls
them through `call_mcp_tool`. A brief for an Antigravity lane that drives a World
says to read the schema file of each `puck_operator` tool before its first call,
to pass the `world` argument on every call, and to wait for a start with
`puck_world_start_wait` `timeoutMs` 60000 or more, so a cold build costs few polls.

The lead machine's local agents can build on an unpushed lane head, so a lane
that depends on another starts there before it lands; merge the landed head into
it afterwards.

Partners cannot see unpushed lanes. When a partner designs against code that
exists only on the lead's machine, send it those lanes' contracts and answer its
contract questions from the local code; a stale remote makes false "failing"
claims.

The lead runs any merge an agent is denied. Agents resolve conflicts in
generated files by running their generators, never by hand-merging: the world
schemas and the portal's TypeScript (`puck schema`), the name registry
(`puck registry`), the vocabulary page (`puck vocabulary`), the console verb
catalog (`puck verbs`, which boots a headless and a windowed World, a GPU leg) and
`packages.lock.json` (`puck locks`).

The integration branch is where the lead lands work. Work reaches `main` in
complete milestones, only when the owner asks and never on a lane's request,
because a push to `main` deploys to Azure, under
[lane branch procedures](references/lane-work.md#branches-commits-and-pushes).

## Schedule machines

Allocate by each machine's fixed capability (CPU class, GPU, RAM, OS, network),
mapped once and checked every turn. Free-memory and free-disk snapshots
fluctuate with what else is open and do not define a machine's capability.
Allocate one GPU leg per GPU at a time, and let CPU work, builds included, run
beside it: a correctness leg's verdict does not depend on load, and a leg that
times out under load is re-run once alone and reported as a flake. Only
wall-clock work needs a quiet machine, and the lead takes it: a lane judges
by counts and lists the timing reads it wants, and the lead runs them in a
window it has cleared of every other lane's builds, suites, evals and World
runs. A brief that measures boot, compile or frame time grants no GPU and
takes no timing while other lanes run. Booting a windowed `Puck.World` is a GPU
leg even when only its startup is measured; a headless one is not. Use
[`verification`](../verification/SKILL.md#what-uses-the-gpu) for GPU work
classification and execution.

A brief's finish line follows [the integration lane](#coding-lanes-and-the-integration-lane):
a coding lane's brief names its touched projects and focused tests, never a
whole-solution build, a full suite or a debug-world replay, which the
integration lane (or the lead acting as it) runs one at a time. A finish line
shows a feature by running it or by a sweep signal; it asks for a `test`
scenario only by naming the invariant running cannot show
([puck-world](../puck-world/SKILL.md#running-it)), never one per demonstration. Writing the
landing bar into every coding brief turns each lane into an integration lane:
heavy jobs then run side by side and Claude Code reaps every background command
when memory runs critically low. Reaped worktrees survive and Codex lanes resume
by session id; [reaping](#coding-lanes-and-the-integration-lane) owns what the
lead does next.

Run a load governor on any machine that hosts many agents, through
`puck host load`, which samples the machine's load and names its state. Under a
watcher, `puck host load --watch` prints one line per transition (`CAPACITY`,
`LOADED` when capacity ends without pressure, `PRESSURE`, `GPU busy` and
`GPU idle`), so each change arrives once:

- On capacity, admit the next job. A heavy job (a solution build plus a full
  suite, about 7 GB at its peak) is one at a time per machine: a full
  `Puck.World.Tests` or `Puck.World.Presentation.Tests` run never runs beside
  another. `puck gate` and `puck affected` acquire the existing heavy lease
  around each heavy suite, sample headroom while holding it, and release it on
  every exit. Nested runs under `puck lease heavy` serialize on child leases
  after validating the ancestor holder's process identity.
- Lease admission is a queue that rotates between lanes, not a race:
  `puck lease` waiters take tickets, and the lease goes to the oldest ticket of
  the lane that held it least recently. A lane is the first word of `--holder`
  (or `--lane`), so start every holder with your lane's name
  (`--holder "bars-and-pick timing"`); one lane with several runs queued gets one
  turn per round, and a lane that releases and re-acquires waits behind every
  other lane already queued. `puck_world_start` takes the same `holder` and
  `lane`, defaulting to the checkout's directory name. A waiter that is killed
  leaves a ticket the next waiter drops; a stale `<name>.queue` entry needs no
  manual cleanup
  ([CLI reference](../../../docs/reference/cli.md#puck-leaseexclusive-machine-work)).
- The GPU is the scarce resource (the owner's direction): most running lanes are
  GPU-free (CPU work shown headless), and a lane whose finish line needs a
  windowed World is started only when the GPU queue can take it. Windowed checks
  owed by several lanes are batched into one lead verification window rather than
  each lane waiting on the lease.
- Refresh private CLI copies when lease admission changes. A FIFO waiter and a
  lane-rotating waiter can each select the other's ticket and leave an idle
  resource unclaimed. Stop the old queued caller and use one scheduling policy;
  `puck lease gpu --help` states the policy. Do not keep retrying World starts
  against that mixed queue.
- A check that needs the owner present (their hardware, their eyes on a window)
  goes ahead of the GPU queue for its short run: the owner's time is the scarcest
  resource. The lead keeps it to a minute or two and discounts any lane timing
  it overlapped.
- On pressure, admit nothing. `puck gate` and `puck affected` admit each heavy
  step only with more free memory than the capacity threshold and more free
  disk than the pressure threshold, so a running agent waits rather than being
  killed.
- On GPU idle, start the next GPU leg. A device test host counts as GPU work.
- The thresholds scale with the machine; the code is their source of truth
  (`HostLoadThresholds.For`, [CLI reference](../../../docs/reference/cli.md#puck-host-loadadmission-lines-for-the-machine)).

Deliberate CPU contention, such as a burner for a flake proof, is CPU work like
any other and may run beside another lane's GPU leg. A leg of that lane that
times out under it is re-run once alone and reported as a flake
([`verification`](../verification/SKILL.md#flake-or-failure)); a wrong value
under load is a failure whatever ran beside it.

An agent stops only the processes it started, by the PIDs it recorded at launch,
and never kills by a command-line pattern. On a shared box a filter on a common
string (a scratchpad path, a lane prefix) matches processes the agent cannot
attribute, other lanes' build and test commands among them, and those fail with
verdicts that are not evidence, so a lane that failed while the kill ran re-runs
its failed legs alone before anyone acts on them. A brief that starts background
work says to record each PID and to stop only those.

Every build, a Codex brief's included, passes `-nodeReuse:false`
([`verification`](../verification/SKILL.md#build-before-you-test) says why).

## Select models and route findings

All three families implement, and model selection is by fit. Choose the model and effort per lane by fit: put the strongest available
model on subtle or correctness-heavy work. Codex's two models, Astra
(`gpt-6-astra`, the frontier model) and Sol (`gpt-6.1-sol`, the workhorse), are
both free to use and encouraged, for implementation and for review-and-fix
passes; pass `--model` and `--effort` on every launch
([`review-passes`](../review-passes/SKILL.md#before-launching)). Use Codex
slots both to implement and to review Claude authors' changes
([spend verification](#spend-verification-not-writing)).
Delegating to subagents needs no one's permission. A follow-on wave much larger
than the last (dozens of agents, or a second full fan-out) is a spend decision:
state its plan and cost to the owner in one sentence before launching it.

### The Claude roster

When the owner pairs with the lead, the lead stays free for that conversation
and subagents do the work: implementation, investigation, verification runs and
reviews. The lead writes briefs, inspects results, merges and reports. The
project agents under `.claude/agents/` carry the four Claude models the owner
allows, in order of rising cost:

| Agent | Model | Effort | Use for |
|---|---|---|---|
| `scout` | Haiku 5.5 | medium | Read-only search, log triage, live-World probes and captures. No source edits or commits; authorized CLI bootstrap is allowed. |
| `implementer` | Sonnet 5.5 | high | A specified brief with a finish line. It is the default writer. |
| `specialist` | Opus 5.5 | high | Design judgement across projects, diagnosis of an unknown cause, review-and-fix passes. |
| `principal` | Fable 5.1 | high | Correctness-critical or long-horizon work: determinism and fixed-point maths, the bake and its kernels, renderer architecture, a defect other lanes failed to crack. |

Route each brief to the cheapest role that fits it (the owner's ruling): a
brief with a known cause or a specified result, such as content, a document
change, a world edit or a fix with a repro, goes to `implementer`, even when it
is large. `specialist` is for an unknown cause or a design call across projects.
`principal` is for the problems the table names and nothing else, and its usage
is conserved (the owner's ruling): an unknown cause starts on `specialist` or
Astra, and `principal` takes a problem only after one of them has failed to
crack it. When a lane on
a cheaper role stalls, escalate that lane; never start on the expensive role
because a brief is long. Codex is part of the same lineup: Sol is a peer of
`implementer` and takes the same briefs, and Astra is comparable to `principal`
and takes only what `principal` would. Spread implementer briefs across
`implementer` and Sol, so both families' slots stay busy. Concept art and
other image generation go to Codex as the primary artist and judge (the
owner's ruling): its built-in `image_generation` tool makes the images and its
verdicts decide which to keep, and a Claude partner writes the brief and
checks verifiable constraints, overruling only a hard-constraint violation.
Every panel passes the written audit in
[concept art review](../../../docs/game/art/README.md#concept-art-review), and
the lead reviews every panel before merging.

Pass `effort` on the Agent call to move one lane up or down: `xhigh` for long
agentic coding on a hard lane, `max` only when correctness outweighs cost.
Opus 5.5 and Haiku 5.5 run at `medium` when nothing sets an effort, which is
why each agent file names one. Pass `model` only to put a role on another
model.

Writers run in their own worktree (`isolation: worktree`), branched from the
lead's HEAD (`worktree.baseRef` in `.claude/settings.json`), so their edits
never touch the checkout the owner is pairing in. A Claude agent writes only
inside its own worktree: the harness refuses its writes to another one. To
continue a branch another lane holds (a Codex branch, say), brief the agent to
fast-forward its own branch to that branch first, then land its branch. Every agent reaches the live
World through the session's `puck` MCP server. That World runs the main
checkout's build and sources, so a lane sees its own edits running only after
the lead merges and reloads, or in a World of its own, named by `world` on
every call. A brief tells such a lane to start that World with
`puck_world_start` (`checkout`: the worktree's absolute path; it boots the build
of the worktree's current sources, building it first when no run has) and to end it with `puck_world_stop`, never with a hand-written
boot line or a PID kill; the tool passes `--devices none`, a state directory
of its own and `--control`, and a `windowed: true` start, the GPU grant's leg,
holds the GPU lease until the World exits. Reads and captures of the live World are always
allowed; a brief names the live mutations a lane may make. The machine belongs
to the agents (the owner's ruling): the lead boots a World for a check and stops
it when the check ends, and it leaves one running for the owner only when the
owner asks to play or pair in it.

Codex lanes reach the same World: the repository's `.codex/config.toml` starts
the same `puck` MCP launcher, so a companion `task` run in this checkout or a
worktree of it can call `puck_worlds` and the rest.

| Codex model | Id | Role | Effort |
|---|---|---|---|
| Astra | `gpt-6-astra` | The frontier model, for the most demanding work | `low` to `max`; refuses `none` |
| Sol | `gpt-6.1-sol` | The workhorse, near Astra for complex coding | `low` to `max`, default `medium`; refuses `none` and `minimal` |

The companion's `--effort` stops at `xhigh`; `max` needs `codex exec -c
model_reasoning_effort='"max"'`, which the Codex CLI applies (its header prints
the effort). Codex draws on the plan's allowance. Effort is not capability
across models: OpenAI's Codex guidance says Astra at `low` can outperform Sol at
`high`, so a lane that needs Sol at `high` or above tries Astra at `low` or
`medium` first. Raising effort never supplies a missing file, tool or
permission; fix the brief first. Astra asks more questions when input
could change the result and follows `AGENTS.md` and skills more literally, so an
Astra brief states its authority and finish line outright. The owner's own Codex Desktop thread holds a writer lock while it is
open, so the lead never resumes it with `codex exec resume`; the lead and that
thread talk through the owner, or through a file both read.

Antigravity is the third family, running Gemini 4 Argon (Google's flagship,
on the owner's Google AI Ultra plan; an Antigravity lane launches as above). It
is strong at repository issue fixing, app and UI generation, security
remediation and large-context analysis, and weaker on long terminal-driven and
long-horizon work. Route it accordingly:

| Give Argon | Keep from Argon |
|---|---|
| Independent review and audit passes (a third family's blind spots differ from Claude's and Codex's) | Long implementation lanes with many build/test/World steps |
| Security review of a change or an area | Lanes that need network or GPU legs from inside its sandbox |
| Whole-area analysis that needs a large context | Anything that must push or mutate shared Git state |
| Portal, dashboard and other TypeScript/UI work | |
| Research synthesis | |

Judge the family balance lane by lane. It is not a quota and not a reason to
reassign work already under way. Owner steering adjusts judgement; do not harden
a small direction into a quota or an always rule.

Every finding goes into a
[work packet](../../../docs/plans/open-items.md#work-packets) in the open items
with a severity and one owner: the packet that shares its cause or area, or a
new one. The lead rules on what a review raises: a scoped fix, a recorded open
item, or a dismissal with its reason; a finding called out of scope still sits
in its packet with its owner. There is no second round.

Route reviews by where the work lives. A pushed branch can be reviewed in any
machine's Codex slot; a local-only lane needs the lead's own slots. When the
lead's slots are full, send reviews of pushed branches to partners.

## Audit the process before the owner does

The lead's job is throughput of landed, correct code. Finding a process defect
is the lead's work; one the owner has to point out is a lead failure. Measure the
thing the owner cares about, not machine load alone:

- time from a lane's last commit to its landing on the integration branch;
- implementation slots (Codex and agent) not implementing right now;
- each family's implementation and review turns in the current wave, as a
  check that routing still follows fit rather than habit (a reading, not a
  quota);
- the board's age against the newest lane change.

Read lane state with `puck lanes` ([reference](../../../docs/reference/cli.md#puck-lanesone-line-per-worktree)),
never an ad hoc scan of the worktrees: one line per worktree with its commits
ahead, changed files, last commit, newest write, log exit, GPU lease state and a
`STALL` mark, in seconds, read-only, and without walking `bin/` or `obj/`.
`puck lanes --watch 0` is the stall watcher: run it as the one background
monitor, and it prints only a lane finishing, stalling or resuming, a lease
changing, or a lane appearing or leaving.

In Claude, arm a recurring audit as a background monitor, which reports while the lead is
busy; a session cron fires only when the lead is idle and misses exactly the
drift it exists for. On each audit, act on what degraded in the same turn: a
ready lane waiting more than an hour for a batch, an idle slot with ready work,
a lane held for anything but the integration lane's next batch, a lane that
repeats a failure or has made no writes for 30 minutes ([no bad
loops](#no-bad-loops)), or a stale board.

When an owner correction reveals a process rule, change the repository skill
that drives the behavior (this one, `review-passes`, `verification`) in the
same turn. Agents and the lead's own briefs read the skills; a private note
beside a skill that still says otherwise changes nothing.

## No bad loops

Every lane and the lead follow five rules, so that a failure costs one retry and
not a spiral:

- Retry a failing step (a build, test, boot, start, review or restart) once. If
  it fails again, stop, record what failed and what was tried, and take the next
  item.
- Every poll has a deadline and a spacing that fits the work. A lane waits on a
  run of minutes by starting it in the background and checking every few
  minutes (or blocking on its exit), never by re-running a status script every
  few seconds: each check is a model turn, and a boot-once run of 40 file legs
  polled that way spent hours of tokens and wrote a 2 MB log saying "still
  running". A brief with a long run says how to wait for it.
- The lead starts each lane as its own background task, so each lane's end
  arrives as its own notification. Lanes launched together in one background
  command report only when the last one ends: a lane that finished first sat
  unseen for an hour and a half that way.
- Findings never bounce between a reviewer and an author: a finding goes into
  its work packet with its owner and is not argued back and forth.
- The lead's audit stops a lane that repeats a failure or makes no writes for 30
  minutes, saves its tree as a WIP commit, and hands the work to another lane.
- When the review of a fix finds more instances of the class it fixed, the next
  fix is structural: one check that holds the invariant everywhere and a test
  over every case, not another path-by-path round. When the structural round
  still draws same-class highs, stop patching: either settle the threat model
  in a decision (pruning's three rounds were all hostile same-user
  interleavings, outside the install root's model) or have a design memo
  written and reviewed before any more code (the companion custody rework).
- "Conserve Fable" means no new principal (Fable) lane without the owner's
  go-ahead, however hard the problem: route it to specialist (Opus) and say so.
  Twice the lead started principal lanes after that instruction, and the owner
  found Fable past half its usage.
- A defect the owner can see (a walkthrough, a sweep still, a capture) ranks
  at the top of Next and gets a lane at once, aimed at the root cause, not a
  packet line: the hall stairs' holes sat as "dark patches" in the sweep packet
  for weeks while engine work ran, and the owner found them unfixed.
- At each landing the lead checks that the top of Next has lanes on it. Review
  rounds, fix lanes and landings fill a lead's attention without filling the
  machine: once, only three review-bound lanes ran for hours while Next's top
  packets sat idle.
- After each landing, the lead runs `puck compile worlds/debug/debug.puck
  --validate` on the merged head before the next landing: two lanes that each
  fit a shared budget (the rule-work ceiling) can exceed it together, as the
  card table and a corrected influence price did.
- A Codex run that ends `Selected model is at capacity` is retried once on the
  other Codex model (Sol to Astra or back), not on the same one.
- A read-only lane in a worktree commits what it writes or returns it as text:
  an uncommitted file in an auto-cleaned worktree is gone when the lane ends.

## Rule on collisions

When two lanes' contracts collide at a merge, bisect to the exact field, then
rule from the principle, not the convenient option. For example, a replay is a
function of its tape, and the authoritative hash covers everything that drives
play. When no written contract settles it, rule by the long-term principle in
[AGENTS.md](../../../AGENTS.md#core-rules), write the ruling into the contract's
owning document in the same change, and let the owner review it with the
delivered batch; take it to the owner first only when it is a product
trade-off. Change a test only to match the ruled behavior.

## Message partners

Cross-session messaging below is Claude-only. Codex's in-session agent messaging
is not a bridge to an independent peer session. Codex and Antigravity use a
shared lane-named file, the hand-back report and the `Brief:` trailer when no
peer-session transport is available.

Keep messages short, with a self-contained first line:

```text
[<brief id>] <started|progress|done|blocked|question>: <sentence>
```

Put large content in a lane-named file under `<worktree>/.claude/scratch/<lane>-*`, and carry its path in the message. Large content never goes on a
pushed branch: a branch carries the lane's commits, not its analyses, logs or
notes. Silence is not agreement.

A message arrives in the partner's session as a user turn, so state your role,
the ask and where to reply. Message only the lane the owner named, and never
relay through a third agent what the recipient can read itself. Work already in
flight can land after a stop order, so expect one more report. The
session-messaging tools load on demand in each session, so a brief that expects
a reply says to load them. A session cannot read its own id: ask for replies to
the session the message came from, and address a peer on another machine by its
listed name, which survives a restart where its bridge address does not.

## Route adjacent work

| Skill | Route there for |
|---|---|
| [`verification`](../verification/SKILL.md) | The landing bar, optional checks, private CLI copies and GPU execution. |
| [`review-passes`](../review-passes/SKILL.md) | Review-and-fix passes: briefs, companion launch commands and the follow-up branch a pass hands over. |
| [`boy-scout`](../boy-scout/SKILL.md) | Keeping agent-facing documents and skills in step with a change; [Writing documentation](../../../docs/development/documentation.md) owns their prose and the skill evaluation procedure. |
