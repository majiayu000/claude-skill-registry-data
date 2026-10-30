---
name: kyoshi-command
description: Suki's command of the Kyoshi Warriors for a standing program. She holds the island for days, writes every order, and reads every report, and she never picks up a fan herself. Use for orchestrate, "run this whole project", "own this migration until it lands", or a multi-day program of many stacked PRs and dozens to hundreds of subagents under one coordinator chat with minimal human turns.
---

# Suki's Kyoshi command

When Suki commands the island's defense, she does not fight on the beach. She writes clear orders, posts warriors where they belong, reads every runner's report at set times, and keeps the front line holding. You own the program, never the code. Author briefs, drain the queue, keep the frontier green, and decide.

This skill is for a whole project handed to one standing coordinator chat. It runs for days, spans many stacked PRs, and uses dozens to hundreds of subagents, with the human checking in twice a day instead of every five minutes. One task driven to a predicate belongs to `night-watch`. One ambitious run that needs a bespoke workflow belongs to `day-of-black-sun`. Route here only when the work outlives any single agent. Work one agent could finish inside the session's budget is not a program, however program-shaped the request sounds.

Prove behavior with the project's verify skill (see `vital-signs`), or with Claude Code's `run` skill when the repo has none. Every brief names the resolved skill path or the exact commands.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

Ceremony must scale with the program. On cheap, near-identical units, collapse it as each section directs.

Three rules carry the rest.

- Completions are queue events, not interrupts.
- Every spawn and every resume carries the standing orders verbatim.
- The brief is the product. A vague brief fails quietly, because a worker cannot ask you a question.

## Roles and placement

- **Coordinator (this chat).** Frames, authors briefs, drains the inbox, owns the human report, and makes judgment calls. It never authors or edits code. Conflicted merges, chain rebases, and code changes are always tasks. Mechanically landing a verified unit (a fast-forward or clean cherry-pick of a worker's commit, then a push) is bookkeeping the coordinator may do itself on repos where local git is cheap. Queueing finished work behind an idle stacker is how a deadline harvests nothing. The loop is agentic end to end. Agents are spawned and drained only through the Agent tool. Pick each subagent's character, model, and reasoning effort for the job, as the dispatch rules in `avatar-mode` describe. State reads and writes go through the `orch` CLI at drain points, one command in and one line out. The CLI never spawns, waits, or wakes anything.
- **Sub-coordinator.** Durable, one per track, and only when the program exceeds what one coordinator's drains can manage. A track the coordinator can drain itself needs no middle layer. Each nested layer re-pays a full orientation preamble, and a blocking sub-coordinator hides its children while the parent idles. It owns its track's units and boards, authors its workers' briefs, and spawns its own workers and verifiers where the runtime lets a subagent spawn one. Where it cannot, it owns its track's units directly with the same review separation. It rolls up aggregates at wave boundaries and never forwards raw child reports. Cap in-flight children at what one drain can process, roughly ten, as a rolling window. Never use blocking batches, which cost the slowest child of every batch.
- **Worker and verifier.** Background subagents (`run_in_background: true`), each dispatched as the character whose discipline fits the unit (`team-avatar:<character>`). Claude Code has no remote worker environment, so isolation is a worktree or branch per writer, not a separate machine. A subagent never sees this chat, so its brief inlines what it needs or points at repo and store paths. Prefer fewer, broader workers. Keep one writer per worktree or branch, so no two actors share a file. Run a unit's verifier on a different model family from its worker, taking the family from the avatar-setup sheet's `panel` line.

Depth stays at coordinator, track, worker. Author the track decomposition per project. Build, landing, and verification are common cuts, not a required shape. Hard-coded formation trees were tried and parked as too rigid.

## The orch CLI

`orch` is `bun ../../tools/orch/orch.ts` from this file, under the installed plugin. It keeps the store's plain TSV and JSON files, which stay readable without the CLI. Pass the store with `--store <dir>` or the `ORCH_STORE` environment variable. Commands:

| Command | Does |
|---------|------|
| `orch init` | Create the store files. |
| `orch standing show`, `orch standing add <line>` | Read or append the standing orders. |
| `orch unit add <id>`, `orch unit set <id>`, `orch unit get <id>`, `orch unit list`, `orch unit counts` | Keep `units.tsv`. |
| `orch ledger record <pr> <sha> <verdict> [--evidence PATH] [--verifier NAME]`, `orch ledger check <pr> <sha>`, `orch ledger summary` | Keep `ledger.tsv`. |
| `orch inbox push <agent> <unit> <status> [--report PATH]`, `orch inbox drain`, `orch inbox count` | Queue completion pointers. |
| `orch gate park <id>`, `orch gate list`, `orch gate resolve <id>` | Park human gates. |
| `orch frontier set --repo <dir> [--forge gh\|origin] [--prs <n,...>]`, `orch frontier show` | Compute the merge frontier. |
| `orch status` | Regenerate `status.md` and print a three-line summary. |

Run `orch <command> --help` for every option. Add `--json` for complete rows.

## Store layout

Create `${CLAUDE_CONFIG_DIR:-~/.claude}/orchestrate/<project-slug>/` (on Codex, `${CODEX_HOME:-~/.codex}/orchestrate/<project-slug>/`), outside the repo and outside the session. The store has to outlive this chat. The program runs for days, a session restart is expected (see Liveness and failure), and the store is the postmortem. The session scratchpad is not a candidate, however convenient. It is session-scoped and temporary, so a restart takes the program's only state with it. Every file has exactly one writer. Owners publish facts, and readers aggregate at read time.

- `preferences.md` is the standing-orders register. It holds numbered lines, one constraint each (model policy, stack shape and count, verification bar, forbidden paths, escalation policy). For a human ruling, keep the human's original wording and say who gave it and where. Label your own interpretations, and label a ruling whose original you cannot find. A copy of a ruling is not a new decision. Paste the register verbatim into every spawn and every resume. Directives decay across resumes, and each dropped one costs a human turn. When you catch yourself restating an instruction, append the line before you act (Encode Lessons in Structure, Fire in `four-elements`).
- `overview.md` is the durable PR and issue database. Append. Never rewrite it wholesale per event.
- `units.tsv` has one row per unit with its id, track, state, branch, PR, head SHA, and brief path. Update rows in place.
- `frontier.json` is the computed merge frontier, per Stack safety.
- `ledger.tsv` is the verification ledger, per Verification.
- `inbox/` holds completion pointers. `gates.md` parks human gates (the question, the options, the default on no answer).
- `decisions.tsv` is the decision trail, kept with `battle-map`.
- `status.md` is derived from `units.tsv` and `ledger.tsv` at each drain, never hand-maintained. Regenerate it from the tables instead of narrating events into it.

## The brief

Your prompts to agents are your only product, and a sloppy brief compounds into slop across the whole tree. Every spawn carries all of it. A field you cannot fill is a unit you have not scoped yet.

```
GOAL         one sentence, the outcome, executable by a stranger with no chat access
SCOPE        paths this unit may write; paths it may not; its exclusive worktree or branch
CONTEXT      pointers to files and PRs; upstream reports pasted in full when this unit
             depends on them, because workers cannot see siblings
ACCEPTANCE   checkable criteria, one per line
VERIFY       exact commands or the resolved verify skill path, plus known gotchas
TIMEBOX      rough cap on runtime; on expiry, return partial findings and stop rather than run on
FORBIDDEN    no PR retargets or merges, no rebase, no force-push, no fixes outside scope,
             plus unit-specific bans
REPORT       status, branch, head SHA, PRs, verdict, what you actually ran, deviations,
             suggested follow-ups
STANDING     <preferences.md pasted verbatim>
```

Size the brief to the unit. A one-command unit gets the template collapsed to a paragraph that still names the goal, the scope, the verify command, and the report shape. A 4 KB scaffold around a two-line edit costs more to write and obey than the edit. A spawn may reference the standing-orders file by store path. Verbatim paste is for every resume and for any brief that has to stand alone.

A sub-coordinator brief adds its track boundary and unit list, its spawn budget, the drain protocol, and the rollup format. The rollup gives, per child, the name, status, PR, head SHA, verdict, and one line, plus the track status and the frontier delta.

A dependency is a context relay, not just ordering. Undeclared upstream context makes the worker guess. Missing fields are a refuse-to-spawn condition. Audit one sampled worker brief per sub-coordinator per wave, concurrently with the wave it samples, never as a gate in front of it. A failing brief stops that track and fixes the sub-coordinator's instructions, not just the worker, because brief quality decays late in a run. Never resume-chain a brief. Respawn fresh with consolidated scope.

## Steps

1. **Frame.** State the done predicate as something countable ("all 126 units merged, each ledger-verified `unit-test-verified` or better"). Quantify the scope: units, rough effort, expected stacks, and the wall-clock budget. If one agent could finish inside that budget, stop here and run `night-watch` instead. Collapsing must not depend on another document being present. It means doing the work directly in this session, with plain workers where they help, verification inline, landing as you go, and none of the store, register, or pilot machinery below. Schedule landing against the budget. By roughly 70% of it, stop spawning and land what is verified. Name the tracks per project. A contested decomposition or a one-way door goes through `agni-kai` before the pilot. Present the framing once. Reversible prep proceeds without waiting.
2. **Install the runtime.** Run `orch init`. Open the trail with `battle-map`, write the standing orders before any spawn, and seed `frontier.json` from existing PRs with `orch frontier set --repo <repo-dir>`, adding `--forge origin` when the forge is Origin.
3. **Pilot.** Push one unit through the whole path: brief, worker, verification, stack entry, ledger row, merge. The pilot exists to falsify the brief template, the verify recipe, and the unit size while that costs one agent instead of fifty. Fix the contract from pilot evidence before any fan-out. Scale the pilot to the unit. On programs of near-identical cheap units, the first unit is the pilot. Run it as a normal unit with its verify command inline, and start the fan-out the moment it lands. The dedicated pilot pipeline (a separate verifier agent, an audit gate) is for expensive or novel unit shapes, not for clone units where a serialized pilot has nothing to falsify.
4. **Scale.** Spawn a rolling window of workers up to the in-flight cap, refilling as children finish. Blocking batches pay the slowest child of every batch. Spawn track sub-coordinators only past the one-drain threshold in Roles. Recompute ready work after each drain. Relay upstream reports into downstream briefs. Keep sibling communication upward only. The sampled brief audit runs alongside the wave it samples, and on failure it stops the next refill, not the current one. Use `kyoshi-formation` for a coverage or verifier fan-out inside a wave.
5. **Drain.** Run the queue discipline below at every drain point.
6. **Land.** Landing is continuous, never a terminal phase. Integration starts with the first verified unit and runs alongside the remaining waves. On heavy repos the stacker is a standing role from wave one, integrating as units verify. On repos where local git is cheap, the coordinator lands verified units itself, per Roles. Keep the frontier green before upper-stack work. Stack safety governs. Advance `frontier.json` only on a merge or on reported new head SHAs.
7. **Close.** Drain the final inbox. Reconcile every spawned agent to a terminal row (done, abandoned, zombie-reconciled). Confirm the predicate on the real artifact. Confirm every landed PR has a verdict for its current head SHA. Audit the trail per `battle-map`, including its cross-model review. Encode recurring corrections into `preferences.md` or the brief template. Leave the store intact. It is the postmortem.

## Queue and drain

- On a completion notification, run `orch inbox push <agent> <unit> <status> [--report PATH]` and return to what you were doing. Never deep-review inline. A completion that needs review becomes a verifier unit. Never review a diff inside a drain.
- Drain in batches at four points: the end of a critical section, a track rollup, a frontier watcher wake (arm it with Claude Code's `loop` skill, with a long heartbeat fallback, or watch the stack with `bun ../../tools/watch-pr/watch-pr` per `long-flight`), and before a human report. Begin each batch with `orch inbox drain`. Arrivals during a drain wait for the next one.
- Finish a critical section before you drain. Critical sections are authoring a brief, a stack operation, a conflict decision, writing a gate, and updating the ledger or the frontier.
- Each drain classifies every pointer (landed, needs-verify, failed, zombie, noise), writes the resulting rows through `orch unit add`, `orch unit set`, and `orch ledger record`, runs `orch status`, then spawns the next wave in one message.
- Account for every spawned child at its track's rollup: arrived, respawned, or its scope explicitly absorbed. Silently redoing a missing child's work hides both the wasted spend and the coverage gap its result existed to close.
- A drain turn ends with the three lines from `orch status`: counts against the states, what changed, and gates open. Detail lives in `status.md`. The full reply contract applies at checkpoints and at close.

## Stack safety

- The frontier is a computed object, never narrative. Recompute `frontier.json` after every merge and stack mutation. It holds the ordered PR list, branch names, head SHAs, a generation number, and the lowest unmerged PR. `orch frontier set` walks the PR base chain through the checkout's current branch, so chain order and PR states come from the forge. It uses `gh` by default. Pass `--forge origin` when the program resolved the forge to Origin. Head SHAs come from local branch refs, so run it from the stacker's clone. A branch with no PR errors rather than guessing.
- Exactly one stacker per stack may mutate topology (chain rebases, force-pushes, base retargets, merges), serialized within its stack. Record the holder in the standing orders. A chain rebase at this scale is slow and blocks whoever runs it, so give it its own unit and keep the coordinator out of it. Follow [Merge and restack safety](../safe-landing/references/merge-safety.md) for every rewrite.
- Workers never rebase, and never retarget or merge PRs. PR watchers follow `long-flight`, one per stack, scoped to one immutable frontier generation. They report conflicts to the stacker rather than rebasing.
- PR closes and retargets go through the stacker only. Closing a base PR orphans every chain above it. Merges and stack surgery are units with briefs like any other.
- One retro watcher follows merged PRs for reverts, post-merge CI breaks, and orphaned follow-ups.

## Verification

Scale verification to the unit. When VERIFY is a single cheap command, the worker runs it and reports the output, and the coordinator spot-checks receipts. A dedicated verifier agent, on a different model family from the worker, is for units whose verification is expensive, judgment-laden, or high-blast-radius. A verifier agent whose entire product would be rerunning one command is ceremony, not verification.

Write ledger rows with `orch ledger record`. Check the current PR and head SHA with `orch ledger check`. `ledger.tsv` has one row per verdict, keyed by PR number plus head SHA. The verdicts are:

- `live-ui-verified`
- `unit-test-verified`
- `type-check-only`
- `verifier-blocked`
- `verifier-failed`

CI green is an input to a verdict, not a verdict. Behavioral work needs better than `type-check-only`. `verifier-blocked` is not a pass. Respawn the verifier when the environment heals. `verifier-failed` gets a fix unit, not a re-verify. A worker may self-report, and a verifier overrides it on the same key. A new head SHA voids the row, so re-verify after a restack. The ledger answers "was this verified", not memory and not the transcript.

A unit is not done until its output is externalized, the moment it lands, never batched to the end of the run. A worker pushes its branch, a verifier writes its ledger row, and receipts land in the store. Work that exists only on one machine when that machine dies was never done.

## Liveness and failure

- Never resume an agent to check on it. A resume restarts an idle agent. Probe read-only: the ledger, `units.tsv`, `gh`, pushed branches, and the background task list. Transcript mtime is not liveness.
- A silent death gets a synthetic postmortem row in the inbox (unit, failure mode, last evidence, options). Replan on evidence as it arrives. Never wait for full quiescence.
- Retry by failure mode. A cap hit or out-of-memory respawns with smaller scope. A network drop retries as-is. A tool error retries on a different model. An unknown failure retries once. After two retries, abandon the unit and replan around it.
- A zombie that returns hours late reconciles against the current frontier and ledger before anything is accepted. Salvage unique findings through a fresh unit, never a blind merge.
- When continued spawning would produce garbage tree-wide (bad upstream output, broken acceptance, dead infrastructure), write a stop line at the top of the standing orders, let in-flight work finish, fix the cause, and clear the line.
- Bound your own infrastructure retries the way you bound a child's. After a few consecutive tool aborts, stop retrying. Write a terminal handoff to durable state (what is done, where it lives, the exact command to resume) and end the run.
- After a session restart, in-flight subagents are dead. Pushed branches, open PRs, and the store are not. Re-read the standing orders and `units.tsv`, recompute the frontier, reattach in-flight work by PR and branch rather than by agent id, respawn one sub-coordinator per track from its stored brief plus the current state, drain, and resume. The dead session's store lock clears itself on the next write, because `orch` replaces a lock whose holder pid is gone.

## Escalation

These reach the human, batched into the status page rather than sent per item:

- irreversible actions (force-push to a shared branch, deploys, deletions, closing someone else's PR)
- genuine product or preference calls no experiment settles
- a standing order that contradicts observed reality
- a program-level dead end that survived a replan

Park each as a `gates.md` entry with `orch gate park` before asking, and route work around it.

These never reach the human: frontier nudges, rebase mechanics, retries, CI flake triage, review-thread triage, format fixes, scope the brief already forbids (refuse it and continue), and "should I keep going". When in doubt, act and log.

Mid-run discoveries fix only what blocks the frontier. Everything else parks in follow-ups. At this fan-out a small scope leak multiplies into PRs nobody asked for.

## Reply

At checkpoints and at close, report:

- the predicate and the count against it, from `units.tsv` and `ledger.tsv`
- the tracks and what each landed
- the frontier (PR list plus SHAs)
- a summary of the verdicts
- what was abandoned and why
- gates awaiting the human (the only asks)
- the store path and the trail path

Take numbers from the tables, not narrative. Link each PR as `https://github.com/<owner>/<repo>/pull/<number>`. Write it per `tea-time`.
