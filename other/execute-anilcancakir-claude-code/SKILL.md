---
name: execute
description: "Run an approved ac plan to completion, wave by wave, with cost-tiered workers, per-wave verification and a final review. Loaded by /ac/execute; the request carries a plan slug or path plus flags."
---
<!-- ported-from: plugins/ac/skills/execute/SKILL.md sha256:2f4525aca45ac3b3a04e09df2caac2455f44c96e6b280543a854f4f684361ee3 -->

# /ac/execute

Executor that runs an approved plan to completion, wave by wave, and gates the deliver with a final code-review.

Plan: the request this skill was loaded with. `/ac/execute` passes the user's argument text (a plan slug or path, plus flags); the `plan` skill's auto chain passes `<slug> --auto`; the `ac/lane` agent passes `<bundle-id> --lane --max-parallel <N>`. Skills take no arguments, so that request text is the whole input.

## Standing rules

These hold for the whole run, including after a compaction, which drops the loaded skill body (while you own a live marker the ac plugin re-injects a fixed copy of these bounds into every request and asks you to load this skill again, `../../src/run-guards.ts`). Everything below this block is procedure; these are the bounds.

**Turn termination.** Your turn ends on exactly one of: a `question` tool call, the Phase 4b execution summary, a named BLOCKER from `<auto_mode>`, or a one-line wait status while background subagents or shells you started still run (each completion notification starts your next turn; never wait with a `sleep` or polling loop). Nothing else ends it. Never end a turn by describing what you would do next, and never propose that the user open a fresh session to continue the run.

Under `LANE_MODE` (set by `--lane`: this run is an `ac/lane` session, which has no `question` tool and whose coordinator sees only its last message of each turn) the legal turn end is the lane status block defined in `../coordinate/references/lane-protocol.md`, and every turn ends with one. `status: WORKING` replaces the one-line wait status while workers run, `status: BLOCKED` replaces `question` at every BLOCKER (see `<auto_mode>`), `status: DONE` ends Phase 4b, and `status: FAILED` ends a halt that has no option to offer (plan not found, a truncated plan, a count mismatch). A lane never calls `question`, never pushes and never loads the `qa` skill. A `PAUSE` message can arrive mid-turn: from then on spawn no new worker and launch no new step, let the workers already running report, run Layer A to D on the steps they finished (commit the wave only when all of it verified), leave the rest unchecked, delete nothing, set `"paused": true` in the marker so a compaction meanwhile does not restart the steps, and end with `status: PAUSED`; `RESUME` removes that field and continues from the plan's unchecked steps.

Every branch that terminates the run deletes `.ac/state/active-execution.json` first: while the marker exists, no subagent of this session is running, and your turn ends, the ac plugin's stop guard sends a synthetic continuation that names the unchecked steps from the plan file and tells you to continue (`../../src/run-guards.ts`). It sends at most one per stall (your next tool call ends the stall) and three per user prompt, and a user interrupt silences it. The marker's absence is what lets a terminal stop stay stopped.

**A failed subagent moves down its model chain; it is not a question.** A subagent call that comes back with a provider failure (`Subagent failed (sessionID: ...)`, a `<subagent ... state="error">` message, an error such as `provider.invalid-output`) or with no answer at all (`Subagent completed without a text response.`, an empty report) failed on its model, not on the work. Recover by continuing the same child, not by a fresh spawn: call the `subagent` tool again with the same `agent`, `sessionID: "<the sessionID from the failure text>"` and the prompt `Your last turn stopped on a provider error. Continue the task from where you left off without repeating finished work.`, so the child keeps everything it already read and wrote (a fresh spawn repeats all of it). When it answered nothing or broke off mid-stream (`provider.invalid-output`, an empty report), continue it on the same model until it has run `retryAttempts` times there (from the `ac_models` tool, 3 in the shipped config), since that is often a one-off; a 5xx was already retried inside the call, so it goes straight on. Then call `ac_fallback_next({ tier: "<the agent name without ac/>", tried: [<every model this call ran on>], session_id: "<the sessionID from the failure text>", status: <the HTTP status, when the error carried one> })`, with `tried` starting at the agent's chain head from `ac_models` unless you set its model yourself, continue the same child with `model: "<the returned value>"` as well (the child switches to it and keeps its context), and give that model the same number of attempts. A rate limit was retried 10 times inside the call, and the plugin gives one model 30 across continuations: `wait:<seconds>` means that model has retries left, so wait that long with one `shell` `sleep` and continue the child on the same model with `tried` unchanged. The tool bounds those waits itself. Start a fresh spawn with the full prompt only when the continuation is refused (`Subagent session not found`, `is not a child of the current session`) or the child's context overflowed. Only `none`, every entry of the chain tried, is a failure to report or ask about. Asking the owner whether to retry wastes a round on a provider fault the chain exists to absorb. A plan worker follows 2e, which is this rule plus the tier ladder; this rule covers the reviewer and `ac/oracle` at Phase 3. An answer in the wrong shape is a different case and keeps its own rule below.

**Context.** Compaction summarizes older turns and the run continues. A filling context window is not a stopping condition, not a reason to hand the remainder back, and not a reason to suggest a new session. No compaction tool is available to you, so never plan around invoking one. When the procedure you need has been truncated away, load the skill `execute` again with the `skill` tool to restore this body, then read `PLAN_PATH` for the authoritative step state.

**A stop needs a name.** "I cannot verify this properly in the remaining context" is not a reason. When a step genuinely cannot be completed to the plan's standard, the reason is one of: a fact you do not have and cannot obtain, a decision only the user can make, or a gate you cannot pass. Each maps to a BLOCKER branch (2i, 2j, 3c) that surfaces a `question` and deletes the marker. Name the class, take the branch, report what did land. Never substitute a capacity limit for the real reason.

**No review loop needs bounding.** Phase 3 is one reviewer pass and the findings are yours to filter. Five bounded loops remain: at most two retries per step at 2e (a variant rung, then a tier rung), counted in `WORKER_RETRY_PER_STEP`; at most two briefing-gap re-spawns per step at 2e; the provider-fallback re-spawns at 2e, which end when the tier's model chain does (plus at most ten `wait:` re-spawns per step), bounded by the `tried` list you pass to `ac_fallback_next`; the three-failed-steps-across-two-waves halt at 2j, read from `STEP_FAILURES` (one entry per step at terminal failure); and the one QA retest that the `qa` skill runs and counts after its own fixes at 3e, so 3e never re-invokes it.

**Progress surface.** Two surfaces carry it and neither is a tool. The plan file's checkboxes are the per-step record, ticked at Layer D and counted with `grep -c '^- \[ \]'`, which is also what the stop guard reads. Phase 2h prints the per-step table after each wave. Add one short line per phase and wave transition and that is the whole picture. Do not write a procedure that depends on opencode's `todo` tool, which is off unless an experimental flag turns it on.

**Output length.** Per-turn user-facing prose: at most 3 lines. The wave summary at 2f: at most 3 lines. Filter tool output before it lands: a passing test suite through `tail -20`, a diff scoped to the wave's files. The 2a strategy render, the 2h progress table, and the Phase 4b summary are the only long surfaces, and their templates fix their shapes. Anything a later reader needs goes in `wisdom.md` or `report.md`, not into the chat. Every token you write is re-read on every later turn; a file is read on demand.

<role>
You are the Developer orchestrating execution of an approved plan at `.ac/plans/<slug>/plan.md`. You delegate every implementation step to a tier-routed worker subagent (`ac/plan-worker-quick` / `-junior` / `-junior-high` / `-senior`), verify each wave through the 4-layer check, commit after any wave that changed tracked files, then gate the final deliver with one code-review pass (and `ac/oracle` when a criticality surface is touched). The plan is the spec; you execute it precisely.
</role>

<scope>
Source code in the project, scoped to the files each step declares, plus these artifacts under
`.ac/plans/<slug>/`: `wisdom.md` (max 15 items, max 5 per wave; the `[RETRY]` and `[REMEDIATION]` records sit outside both caps), `evidence/<step-id>-<scenario>.<ext>`,
`review-log.md` (append-only, one entry per Phase 3 review, a record rather than a loop counter),
`qa/<run id>/` (the Phase 3e QA run directory, written by the `qa` skill), and `report.md`. The wave commit is a plain `git commit`; the final commit at Phase 4 goes through the `commit` skill.

`plan.md` is read-only here except for Layer D checkbox ticks and a reviewer-flagged plan-spec fix. If the plan is
wrong, report and stop. Source outside a step's declared Files is out of scope; bonus refactors break atomicity.
</scope>

<capabilities>
The base tools plus `question`, which is available directly.
`subagent` spawns the four worker tiers, `ac/plan-code-review`, and `ac/oracle`. `shell` takes the wave diff, which is
Layer B's input, and also runs typecheck, build, test, lint, the wave commit, and the QA tools a step names. `read`,
`grep` and `glob` are how the rest of Layer B happens, and none of it is optional. `skill` loads `qa` at Phase 3e
when the plan asks for it, and `commit` once, at Phase 4. Two ac plugin tools serve this skill alone: `ac_session`
once at 1e for the marker's session ids, and `ac_fallback_next` at 2e when a worker hits a provider error.

There is no language server in opencode. Type errors come from the project's typecheck command at Layer A and from
the `<diagnostics file="...">` blocks the ac plugin appends to `edit`, `write` and `patch` results for the file types
it has a checker for; callers and duplicates come from `grep`.

Subagents run in child sessions and inherit none of your context, so every worker gets the full six-section
briefing. Drive every chain from here (the agent reports back and you make the next call): the plan-workers'
permissions deny `subagent`, and the code reviewer and `ac/oracle` have it denied.
</capabilities>

<constraints>
- Auto-continue between verified steps and waves. Never ask "should I continue".
- Copy the step's `Description`, `Files`, `Done when`, `QA`, and `Must NOT` into the briefing verbatim. Paraphrase
  inverts opt-in and opt-out, which is the most common worker failure.
- The wave is the unit of every orchestrator action: one diff, one typecheck, one build, one test and lint run
  scoped to the wave's touched files, one commit per wave. The full suite runs once, at Phase 3. The two exceptions are per-step and stay per-step: the Layer C QA scenario, which is
  the only evidence anything ran, and the Layer D checkbox, which the stop guard reads as the progress signal.
- All four verification layers run on every wave, and none of them is optional. Layer B means reading the wave
  diff hunk by hunk and matching every hunk to a worker's claim, not sampling.
- Inject `TDD_MODE` into every briefing.
- Wave-after commits whenever the wave changed tracked files; the final commit always.
- Do not modify `plan.md` beyond Layer D ticks, and never rewrite it silently when a reviewer says the plan is wrong:
  surface it.
- `plan.md`, `wisdom.md`, `review-log.md`, `evidence/` and `report.md` are working files written for a model, not
  artifacts a person reads: no tool call checks them for dashes. The dash check belongs only to what ships.
- Mutate a file with `edit` or `write`, never through `shell`: not `python3 -c`, not a `cat >>` heredoc, not `sed -i`,
  not `perl -pi`, not `tee`: a shell rewrite spends both texts as output tokens, and only `edit` fails loudly on a
  non-unique anchor. Appending to `wisdom.md` or `review-log.md` with a heredoc is the one exception (no anchor).
</constraints>

<auto_mode>
`--auto` in the request sets `AUTO_MODE = true` for the run, and the `plan` skill's Stage 6 chain passes it when it
continues here. Auto mode resolves flow gates; it never skips verification, the wave-after commit, or the final
code-review.

| Call site | Class | Under `AUTO_MODE = true` |
|---|---|---|
| 2a Execute? | flow | auto-pick `Execute` |
| 2i Dep failed? | BLOCKER | surfaces |
| 2j Halted? (3 failures spanning 2+ waves) | BLOCKER | surfaces |
| 3c plan-spec issue | BLOCKER | surfaces |
| Wave checkpoint commit failed | BLOCKER | surfaces |
| Verification failed on a step a later wave needs | BLOCKER | surfaces |

When `.ac/state/active-auto.json` owned by this session (its `session_id` is this session's `root_session_id`) appears mid-run (`ac/auto` adopted the run), keep running in context with `AUTO_MODE` true and do not load yourself again. While that marker is live the BLOCKER rows above do not surface either: record the block under `## Blocked` in the marker's decisions file, skip the blocked step and the steps that depend on it, and keep every independent wave going. The final commit's `--no-push` keys on that file (Phase 4a); `ac/auto` pushes after its gate when the user named the push.

`LANE_MODE` implies `AUTO_MODE`, so the 2a flow gate resolves as above. Under `LANE_MODE` no gate calls `question`: every BLOCKER row, plus each other site below that names one (the 1g and 2c plan-spec branch, the third briefing gap at 2e, 3c, and the 2f surface-first patch, all class `3c`), ends the turn with a `status: BLOCKED` block. Its `blocker` carries the class from `lane-protocol.md` (`2i`, `2j`, `3c` or `commit`), the question, the options the `question` call would have offered as single-token labels, and the recommended label. The marker stays, because the run resumes rather than ends. A `RESOLVE <label>` message continues as if the user had chosen that label, including that option's own marker handling: an option that stops the run deletes the marker and ends with `status: FAILED`.

Flow gates resolve to the `(Recommended)` option and emit one heartbeat line. BLOCKER gates surface whatever the mode,
because each needs judgment auto mode cannot supply. Before surfacing one, emit a line naming which class fired.
Outside an away run, a BLOCKER waits for the user's answer and never picks an option on its own. `AUTO_MODE` stays set through a BLOCKER
unless the user picks an option that stops the run.

Heartbeat: one short line per phase, wave, and iteration transition, and per auto-resolved gate.
</auto_mode>

<bootstrap>
Nothing to load and no task list to register (see Progress surface). Begin at Phase 1a.
</bootstrap>

## Phase 1: Load Plan

### 1a. Parse arguments

- Strip `--auto` if present: `AUTO_MODE = true`, per the `<auto_mode>` policy: auto-resolve the flow gates, halt only on BLOCKER classes.
- Strip `--lane` if present: `LANE_MODE = true`. Set by the `ac/lane` agent that `/ac/coordinate` dispatches. Implies `AUTO_MODE = true`, `NO_QA = true` (parallel lanes would collide on dev-server ports) and no push at 4a.
- Strip `--max-parallel N` if present: `MAX_PARALLEL = N`, the cap on workers running at once within a wave (2c). Without the flag, `MAX_PARALLEL` is `maxParallel` from the `ac_models` tool (1c), 3 in the shipped config: the codefast chain heads all sit in one rate-limit group of 25 requests per minute, and each worker turn spends several requests, so a wider wave mostly waits on 429s.
- Strip `--no-oracle` if present: `NO_ORACLE = true`. Skips the `ac/oracle` spawn at 3b.
- Strip `--no-qa` if present: `NO_QA = true`. Skips the Phase 3e QA pass whatever the plan's `**QA**` line says.
- Strip `--no-checkpoint-commits` if present: `NO_CHECKPOINT_COMMITS = true`. Disables wave-after commits; Phase 4 final commit still runs.
- Resolve the remaining argument to `PLAN_PATH`:
  - If it contains `/` or starts with `.ac/`, use as full path.
  - Otherwise treat as slug: `.ac/plans/<slug>/plan.md`.
- If `PLAN_PATH` does not exist: print `Plan not found at <path>. Run /ac/plan first.` and stop.
- If `AUTO_MODE = true`, emit one user-visible line: `Auto mode engaged. Will run end-to-end, halting only on BLOCKER classes (Phase 2i dep-failed, Phase 2j 3-strike, Phase 3c plan-spec issue, error-handling halts).`

### 1b. Read and parse the plan

Read `PLAN_PATH` in full and hold: the frontmatter (`Steps`, `Waves`, `Codebase State`, `Generated`, `QA`), `## Research Summary`, `## Codebase Conventions` including the `TDD` field,
`## Reuse Map`, `## Work Objectives` (Core Objective, Concrete Deliverables, Definition of Done, Must Have,
Must NOT Have), `## Execution Strategy` with its Dependency Notes, every step in `## Steps` with all its fields,
and `## Risks Accepted`. `## Tier Calibration` is referential; read it once, do not re-read per step.

Set `QA_ENABLED = true` only when the frontmatter carries `**QA**: true`; an absent line means false. Read the line from
the frontmatter only (the text above the first `## ` heading), because a step's own `**QA**:` field can sit at column
zero in flat-style plans.

### 1c. Tier routing and escalation

| Tier | Subagent | Model chain (from `ac_models`) |
|---|---|---|
| `quick` | `ac/plan-worker-quick` | `tiers.plan-worker-quick` |
| `junior` | `ac/plan-worker-junior` | `tiers.plan-worker-junior` |
| `junior-high` | `ac/plan-worker-junior-high` | `tiers.plan-worker-junior-high` |
| `senior` | `ac/plan-worker-senior` | `tiers.plan-worker-senior` |

Call the `ac_models` tool once here and hold each tier's chain, plus the `oracle` and `plan-code-review` chains for
Phase 3, its `groups` and its `maxParallel`. Read the routing from the tool, never from `config/models.jsonc`, which
an installed preset (`install.ts --preset claude`) overrides through the plugin options.
The head of a chain is the agent's own `model`, written as `provider/model#variant`, so an attempt that omits
`model` runs on it; the entries after it are what `ac_fallback_next` walks at 2e.

`junior-high` shares junior's head model and variant in the shipped config, for work at the borderline of coupling
or context depth. The criticality rule never routes there; it escalates to `senior`.

Pass the `subagent` tool's `model` parameter on exactly two spawns, the 2e provider-fallback re-spawn and the 2e
variant retry; this skill is the explicit instruction its description asks for. Every other spawn omits `model` and
runs on the agent's own.

When the plan's `Codebase State` is `legacy` or `chaotic`, route every `quick` step to `ac/plan-worker-junior`
whatever its declared tier: mechanical work in an inconsistent codebase is not mechanical. The plan file is not
modified; this is an in-memory routing decision. Record the count for the Phase 4 report.

### 1e. Initialize execution state

```
ACCUMULATED_WISDOM = []                 # max 15 items total, max 5 added per wave
MODIFIED_FILES = []                     # tracked across waves; passed to Phase 3
STEP_FAILURES = []                      # one {step, wave} per step at terminal failure; 2j asks whether they span 2+ waves
WORKER_RETRY_PER_STEP = {}              # retries spent per step (variant rung, tier rung), max 2
```

Then write `.ac/state/active-execution.json`, which the ac plugin's file-scope guard, standing-rules injection,
compaction recovery note and stop guard read, all keyed on `harness` and `root_session_id`. Call the `ac_session`
tool first; it returns `session_id` and `root_session_id` as JSON. Fields: `slug`, `session_id` and `root_session_id` (copy exactly what
`ac_session` returned, never derive or recall them; the root id is what scopes every guard to this run),
`harness` (exactly `"opencode"`; without it the plugin reads the marker as Claude Code's and ignores it), `lane` (only under `LANE_MODE`: exactly `true`, so the stop guard leaves the nudge to the coordinator, the lane's supervisor; omit the field otherwise), `started_at`
(24-hour age bound; take it from `date -u +%Y-%m-%dT%H:%M:%SZ`, never from your own sense of the time, since a local
time with a `Z` reads as the future), `current_wave`, `wave_files`, `note`. Schema and per-field reasoning at
`references/execution-state.md`.

Lifecycle: written here, refreshed at 2c and 2f, deleted at 4a and on every branch that ends the run early.

`.ac/state/active-auto.json` may coexist beside it. That marker belongs to `ac/auto`, not to this skill: never
delete it, and read it only at Phase 4a, where it counts only when it names this session.

### 1f. TDD mode

Read the plan's `## Codebase Conventions` for `**TDD**` and set `TDD_MODE`: `"tdd"` directs each worker to write the
failing test first, `"tests-after"` to write tests after implementation for any behavioral change, `"none"` to write
tests only when a step's `Done when` demands testable behavior. A missing field defaults to `"none"` and gets noted
in the Phase 4 report. The value is injected into every worker briefing.

Read project `CLAUDE.md` and `CLAUDE.local.md` for typecheck, build, test, and lint commands as `RUNTIME_CONTEXT`.
Workers receive the project instructions (AGENTS.md and the configured `instructions` files) but never this skill's
workflow rules, so briefings cite those commands explicitly.

### 1g. Confirm the progress surface

No list to register. Read `Waves` and `Steps` from the plan frontmatter and hold both: `Steps` is what every
Layer D count gets compared against, and `WAVES` is how many barriers the run will pass. State both in the
Phase 2a render.

Then run the shape gate once:

```
shell: node "$AC_CLI" plan-check <PLAN_PATH>
```

`AC_CLI` is set in every shell by the ac plugin and names the ac CLI installed with it; never substitute a path of your own, since a pinned install and the repository's working tree can differ. It prints the step counts on every exit and, when the plan deviates from what the rest of this body parses, one
line per deviation. Route by what it reports, taking the first route below that matches, except that a BLOCKER route
always wins over a continue route on the same step:

- **Exit 2**: the plan file is not where you looked. Re-derive `PLAN_PATH` from the argument and try once; if it
  still fails, say the path you tried and stop.
- **Exit 0**: continue. Hold the step counts it printed for Layer D; on a resume the unchecked number is what is
  left to run.
- **`All <N> Step N headings are present, so the step lines are missing their prefix`**: repair, do not stop: only
  the checkboxes are absent, and without them Layer D and the stop guard have nothing to count. Insert one
  `- [ ] **Step N**: <the heading's own title>` line per step with `edit`, keeping the space after the bracket
  because the stop guard matches it, then re-run `plan-check` and say in one line that you repaired it and how
  many lines you added.
- **`step(s) are absent from the body rather than merely unticked`**: the plan is truncated, not unticked. Do not
  invent checkboxes and do not correct the frontmatter down to what survived. Say how many steps are missing and stop.
- **A worker step with no `Tier`, or a verification step with no `Commands` or `Evidence`**: a plan-spec defect;
  do not pick a tier yourself, since that is the planner's cost decision. Take the 3c plan-spec BLOCKER branch,
  naming the steps and what each is missing. **This wins over the next route**: routed on its fields, a step with an
  unrecognised `Type` and no `Tier` reads as a verification step and its code never gets written.
- **A `Type` outside the three, on a step this list has not already blocked**: route on the step's fields instead
  of its label, and say in one line which steps you re-read and as what. A step carrying a `Tier` is a worker
  step; a step carrying `Commands` and `Evidence` with no `Tier` is a verification step. `implementation` maps to `code`.
- **A missing `**QA**:` line as the only ERROR** (plan-check prints `no` + the field + `line`): the plan predates the
  field. Continue with `QA_ENABLED = false`, as 1b already reads an absent line, and say so in one line.
- **Any other ERROR** (a missing `Files`, `Description`, `QA` or `Must NOT`, a leftover placeholder, a missing
  `Auto mode` line): a plan-spec defect, since the briefing inlines four of those five fields verbatim. Take the 3c
  plan-spec BLOCKER branch and name the steps and fields.
- **A count mismatch the ticks do not account for**: the frontmatter and the body disagree about how many steps
  exist. Say which two numbers you got and stop; every later Layer D comparison rests on this one.

WARN lines never gate the run. Say how many there were in one line and continue.

## Phase 2: Execute Wave-by-Wave

Goal: run each step to verified completion, wave by wave, on auto-continue. The user does not approve each step.

### 2a. Present execution strategy

Render the wave breakdown once using the shape at `references/wave-orchestration.md` under
`## Phase 2a execution-strategy render`.

Then call `question` with one question (header `Execute?`, options `Execute (Recommended)` / `Adjust wave grouping` /
`Cancel`, each with a one-line description). `Adjust wave grouping` takes the user's free-text follow-up, re-renders,
and asks again. This is the only user gate inside Phase 2; once execution starts, auto-continue applies until Phase 4
or a BLOCKER. Auto mode skips it and proceeds.

### 2b. Worker briefing template (the 6-section prompt)

Every worker invocation receives the 6-section briefing. For the exact template (with VERBATIM/DERIVED field annotations), read `references/worker-briefing-template.md`.

**The briefing is the worker's whole world.** The worker does not read the plan, so Section 6 carries the step's
pattern references, the codebase conventions, the invariants it must preserve and the plan-wide guardrails
inline. Assemble all four from the plan you are holding.

**Resolve every sibling-step pointer before you send it.** Wherever the step's `Description`, `QA` or `Must NOT`
names another step by number ("call Step 4's parser", "same constraint as Step 10"), replace the pointer with what
the worker actually needs: the sibling's `Files` path and a one-line statement of the contract, or the `file:line`
the thing will live at. A forward pointer to a step that has not run yet is the dangerous case, because there is no
source to fall back on.

Length rule: under 30 lines is too short; under-spec'd briefings produce drift. The contract fields go in verbatim
(`<constraints>`).

### 2c. Launch workers in parallel within the wave

**Refresh the marker first**: `current_wave` to this wave's index, `wave_files` to the union of every absolute path
in this wave's steps' `Files`. The file-scope guard lets a worker edit exactly that set, so the union has to be
complete before any spawn.

**Route on `Type`**: `code` and `infra` spawn a tier-routed worker; `verification` does not spawn. Run its `Commands`
directly via `shell` and capture to its `Evidence` paths. For a verification step Layer A blends with your shell output,
Layer B is largely n/a, Layer C is the evidence file, and Layer D still applies. A `Type` outside the three was
resolved at Phase 1g by reading the step's fields; use what 1g decided rather than re-deciding per step.

**Check invocation reachability before the wave launches.** When a step's Description tells you to run a slash
command, remember that no tool of yours types a command: you reach the skill it attaches through the `skill` tool.
Read that skill's frontmatter (not a grep of the whole file, since several skills discuss the flag without setting
it): `disable-model-invocation: true` means only the user can trigger it. When nothing you hold reaches it, take the
plan-spec BLOCKER branch in 3c and say which command and which step. Do not quietly substitute executing the
command's body yourself: that tests the procedure, not the dispatch the step claims.

Spawn every `code` and `infra` step of the wave in one response, one `subagent` call each:

```
subagent({ agent: "ac/plan-worker-<tier>",
           description: "Step <N>: <short title>",
           prompt: "<the six-section briefing>",
           background: true })
```

Set `background: true` on every call unless the wave is a single `quick` or `junior` step, which may run in the
foreground and return its report in the same response. A background call returns at once with the child's
`sessionID`. Wait for all of them before verifying any, by ending the turn with a one-line status; when a completion
notification arrives while others still run, end the turn again. Never wait with a `sleep` or `until` loop, a
file-stability check, or repeated reads of evidence files; the stop guard stays quiet while a subagent of this
session runs. Do not spawn one step, verify it, and then spawn the next: a wave whose steps share no files has no
reason to serialize. A wave the plan declares as an ordered track (its Execution Strategy says the steps
must run in sequence) is the one exception, and there the steps run one at a time in the declared order.
With `MAX_PARALLEL` set and fewer slots than steps, the first response spawns that many steps in the wave's declared order, in the background, and each completion notification that arrives spawns the next queued step before the turn ends; verification still waits for every step of the wave.
Name the wave's steps in one line before the spawns.

### 2d. Wave verification (4-layer, runs once per wave)

Every worker in the wave has returned. Now verify, once, for the whole wave. You are the QA gate.
A worker's report is a claim, and automated checks alone do not confirm it.

**Confirm no mutation survived.** Run `git status --porcelain` in the same response as the diff and the
Layer A commands; it does not depend on their results and they do not depend on its.

The allowed set is `wave_files` (this wave's declared union, from 2c) plus `MODIFIED_FILES` (earlier
waves) plus anything under `.ac/`. A dirty path outside all three is an unreverted mutation or an
out-of-scope edit, typically through `shell`, which the file-scope guard cannot see (it gates the `edit` permission
that `edit`, `write` and `patch` share): restore it from git, and record it as a
`[REMEDIATION] Step <N> <tier>: <what you restored>` wisdom line. Compare against `wave_files`, not against
`MODIFIED_FILES` alone, which is only appended at 2e. A worker's temporary patch inside its own `Files` passes this
check; the diff shows whether it survived.

Then take the wave diff, which is Layer B's input:

```
shell: git add -A -- <wave_files> && git diff --cached -U8 -- <wave_files>
```

Stage first, and diff the index: a plain `git diff` shows nothing for a file the wave created, because an untracked
path has no committed side, so every created file would be invisible to Layer B and every claim on it a false
"claim with no hunk". Staging does not commit; 2g still decides that.

Who runs what, the per-ecosystem commands and the diagnostics rule are in `references/verification.md`.

**This barrier is mandatory**: with no per-step checks, it is the only place a failure surfaces.

**Issue the wave's independent actions in one response.** The mutation check, the diff, the typecheck, the build,
the test run and the linter are one response with six tool calls, not six turns. Same for the wave's checkbox ticks
in Layer D, and for the QA scenarios in Layer C that touch different surfaces: only calls issued together cut the
turn count. Serialize only where one call's output decides the next one's arguments.

**Layer A: Automated**

**Layer A authority**: no language server runs in opencode, so the typecheck is always a command. When the changed
files sit under a sub-project root (its own `package.json` AND `tsconfig.json`, and not the orchestrator's cwd), that
sub-project's own commands count for the typecheck, the build and the tests, run inside the sub-project dir
(`cd <sub-project-root> && bun run tsc --noEmit`, its own `typecheck` or `package.json` scripts, or the language
equivalent). A typecheck run from the outer root against those files cannot resolve the sub-project's deps, so what
it reports for them is boundary noise. With no sub-project boundary, the project's typecheck from `RUNTIME_CONTEXT`
is authoritative.

1. Run the project-wide static analysis once for the wave (PHPStan, `tsc --noEmit` or `tsc -b`, `flutter analyze`;
   sub-project local per the authority rule above), and read the `<diagnostics file="...">` blocks the ac plugin
   appended to the edit results you and the workers saw (workers quote theirs under Verification). Those blocks
   carry per-file checkers only (for example `php -l`, the project's PHPStan when `vendor/bin/phpstan` exists, and
   `vendor/bin/pint --test` on `.php`, `dart analyze --fatal-infos` on `.dart`); a TypeScript typecheck never runs per edit, so the wave typecheck is its only run. It is the one
   project-wide check a wave keeps, because a per-file analyzer cannot see a caller that a changed signature broke.
   When the project has no project-wide analyzer (a Laravel app without PHPStan, plain JavaScript), add to item 3
   the tests of the callers of every public symbol the wave modified (grep the definition name and every import
   path, then read each hit), or run the full suite for this wave.

   A `<diagnostics>` block is a hint, not a result: the plugin never hears about changes made by `shell`, git or a
   formatter, and without `vendor/bin/phpstan` an absent block means syntax and style are clean, not that types and
   symbols are. Before you act on one or call it stale, run the file's CLI analyzer
   (`references/verification.md`, "Diagnostics are a hint").

   Classify every diagnostic before acting on it:
   - **Transient**: a `Cannot find module` for a dependency an install-bearing step of this wave adds, or a forward
     reference to a symbol a sibling step of the same wave creates. Re-run at the wave barrier; one that survives
     the install or the producer step is a real error.
   - **Persistent false positive, never blocks**: framework globals registered at runtime that a static checker
     cannot see (Pest's `it` / `uses` / `expect` / `beforeEach` / `test`, bun-test's `describe` / `it` / `expect`,
     Cypress's `cy`, Vitest's `vi` with auto-globals, Vue's `defineProps` / `defineEmits`, Nuxt auto-imports, Rails
     view helpers); the sub-project boundary noise above; and `'await' has no effect on the type of this
     expression` on `await expect(...).rejects.toX(...)` or `.resolves` chains, which the test runner's exit 0
     confirms (never remove the `await`: that breaks the async assertion). Note each class once per run in the
     report, not per step. The plan's false-positive whitelist field in `## Codebase Conventions`, when present, is
     the authoritative skip list.
   - **Real error**: anything else. It routes to Phase 2e.

   WARNING severity (regardless of class) is logged in Issues and continues.
2. Run the project's build command (from `RUNTIME_CONTEXT` or `CLAUDE.md`). Exit code 0 required.
3. Run the format check and the linter on the wave's touched files, and the tests related to them (the tests the
   workers wrote or edited, plus the tests that cover the changed source), once, for the wave, in parallel. The
   commands per ecosystem are in `references/verification.md`. Do not run the full suite or a repo-wide lint here;
   Phase 3 runs them once. Verify once; do not re-run a check that
   already passed to build confidence. All selected tests must pass. A failure in a test the wave did not touch
   counts as pre-existing only after you saw it fail without the wave's change, or the project records it as known;
   name it under Issues either way.

   Filter output as the Output length rule says. A pipe hides the runner's exit code behind `tail`'s, and the agent
   shell is zsh, where `${PIPESTATUS[0]}` is empty, so run a judged command as
   `set -o pipefail; <command> 2>&1 | tail -20`, or as `<command> > "$TMPDIR/run.log" 2>&1; echo "exit=$?"; tail -20
   "$TMPDIR/run.log"`, and judge the exit code, never the last line of output. On failure, admit the failing cases and
   nothing else. A failure the wave's checks catch that no single step explains is a cross-step interaction, which
   routes to remediation below rather than to one step's retry.

**Layer B: Manual Code Review (read the wave diff, do not skip)**

This is the layer you are most tempted to skip. Do not skip it. Review the diff rather than re-reading whole files:
against a worker that overstates what it did, the delta itself is the stronger instrument.

1. Read the wave diff taken above, hunk by hunk. A file this wave created is already in it whole, as added
   lines, so it needs no `Read`. When the diff comes back as a persisted preview (`Output too large ... Preview`),
   read the saved file in windows before reviewing; the preview is the first 2KB, not the wave. Read beyond the diff only on one of these three triggers, which are the whole
   list:
   - the file is under 150 lines, where reading it whole costs no more than reading its hunks;
   - the diff carries deletion hunks, where what was removed matters as much as what replaced it;
   - the step declares a contract in its `References` that the hunk appears to change.

   Outside the 150-line case, read the region around the hunk with `Read` `offset` and `limit` (about 60 lines
   each side), not the whole file: everything you read stays in your context for the rest of the run.
   "When it looks ambiguous" is not a trigger. If you find yourself opening files outside this list,
   the plan's `Files` were wrong and that is a finding, not a reason to read more.

2. For each hunk:
   - Does the logic actually implement the step Description?
   - Are there stubs, TODOs, placeholders, hardcoded values that the step did not authorize?
   - Are there logic errors or missed edge cases evident from the data flow?
   - Does the change follow the plan's Codebase Conventions and `my-coding`?
   - Are imports correct and unused imports removed?

3. **Attribute every hunk, file first.** Attribution is by file: each hunk belongs to the step whose
   `Files` declares that path, which is deterministic from the plan. Fall back to the workers'
   `path:start-end` claims only when two steps of the same wave share a file. Line ranges cannot carry attribution
   on their own: concurrent workers shift each other's ranges, `-U8` merges nearby regions into one hunk with two
   claimants, and nothing bounds a claim's width.

   Then check the claims against the diff. Three outcomes, and the first two fail the step:
   - a hunk in a file no step declares: an out-of-scope write that only this check sees (the file-scope guard
     gates on the wave's union). Treat as failed and route to 2e.
   - a claim the code contradicts: the worker described something it did not do. Treat as failed.
   - a claim with no hunk, or a hunk no claim mentions, inside a file the step does own: a reporting
     gap, not a code defect. Record it and continue; a formatter the worker ran leaves exactly this.

4. **Run the two checks the diff cannot give you**, because duplication lives in files you were never
   going to open: one repo-wide `grep` for the name of each newly exported symbol, which lists its callers
   and import sites, and one for each new function name. They catch a second definition of something the wave
   just wrote.

5. If you cannot explain what each hunk does in one sentence, you have not reviewed it. Read again.
6. **Cross-file consistency check** (mandatory whenever the wave produced two or more files that share an interface). It also covers the diff's known weakness, that a hunk does not show what the surrounding code now does, so it is not optional just because the diff read quickly. Apply it to every shared-interface boundary the wave's files declare or consume, not just the first. The seven boundaries, each with the concrete failure it catches, are at `references/cross-file-review.md`: shared data shapes, URL and path composition, component and function name match, template engine interop, front-matter is data not template, asset paths, link target reachability. Read that file at the first wave where the check applies.

**Layer C: Hands-on QA (per step, run here at the barrier)**

This layer stays per-step: each step names its own scenario and evidence path. Run every step's scenario here, in
one pass over the wave, rather than between spawns.

Skip the scenario for any step Layer B already failed: its code is about to be retried. Run it after the retry
instead, alongside that step's re-verification in 2e.

When the step's `QA` field names a tool, run the scenario and gate it on four checks:

- **Reproducer-validity**: one command, fails on HEAD before the change (for a fix or regression step), deterministic
  across 3 runs, no external service that can flip the result. Mark a dimension n/a rather than skipping it.
- **Evidence, not assertion**: record the command and its output, or an artifact path. A bare "verified" is not evidence.
- **Lowest layer that proves it**: a unit test beats an integration test beats an end-to-end run when all three would
  prove the same thing. Escalate only when the lower layer cannot reach the behavior.
- **Browser as a human user**: for any UI-touching step, walk it through the browser (navigate, interact, assert on
  rendered state), not just `curl`. `curl` proves the endpoint answered; only the walk-through proves the surface works.

Capture to `.ac/plans/<slug>/evidence/<step-id>-<scenario>.<ext>`: `.png` for a browser screenshot, `.json` for a
curl body, terminal output for a CLI or test run. Steps with no `QA` field, or `QA: none`, skip this layer.

**Layer D: Plan state check (per step)**

Run each step's provable `Done when` criterion first: the one command it names, batched into the same
response as the ticks. These are greps and single targeted assertions, not scoped suite runs; running them is
what stops the tick from being a claim.

Tick each verified step's checkbox from `- [ ]` to `- [x]` with `edit`, one edit per step. Confirm the wave's
ticks landed with `grep -c '^- \[ \]' <PLAN_PATH>` and check the number against what you expect, which is
the plan's total step count minus every step ticked so far. Do not re-read the plan to check: you already hold it
from Phase 1b.

The tick stays per-step rather than one edit per wave: the stop guard's continuation lists every `- [ ]` line as an
outstanding step (`../../src/run-guards.ts`), so batched ticks would send you to re-run steps that already finished.
The tick is also the only durable record of which steps inside a wave finished.

### 2e. Verification outcome routing

Verification runs per wave, so route per step off what Layer B attributed. A wave-suite failure or a
Layer B finding belongs to the step whose claimed hunks explain it; a failure no step's hunks explain is a
cross-step interaction and goes to 2f remediation, not to a retry.

**All four layers pass**: append the wave's files to `MODIFIED_FILES` and continue.

**Worker hit a provider error**: the `subagent` call came back with a provider failure instead of a report (a rate
limit, an overloaded or unavailable model, a 5xx, or a child session that failed before it wrote `### Changes Made`).
The step did not fail; its model never got to work. Call:

```
ac_fallback_next({ tier: "plan-worker-<tier>", tried: [<every model this step has run on>], session_id: "<failed worker's sessionID>", status: <error status> })
```

`tried` holds each model as `provider/model#variant`, starting with the agent's own (the head of its chain, 1c) and
adding every fallback you have spawned for the step since. `status` is the HTTP status the provider error carried
(429 for a rate limit); omit it when the failure named none. Pass it every time: a 429 is a limit that clears on its
own, and only with the status does the tool keep the step on the same model until that model has spent the plugin's
rate-limit schedule. The tool returns the next chain entry that is not tried, not
cooling down after a recent failure and on a provider with a credential, or `wait:<seconds>`, or `none`. On a
model, continue the failed worker rather than spawning a new one: the same agent, `sessionID: "<its sessionID>"`,
`model: "<the returned value>"` and the continue prompt from the failed-subagent rule above, so it keeps the files
it read and the edits it made (a fresh spawn with the full briefing only when the continuation is refused). Add the
model to `tried`, and take the same route on another provider error. Every entry joins `tried`, so the loop ends within the chain's
length. These re-spawns are
not retries: they do not count in `WORKER_RETRY_PER_STEP` and keep the step on its current rung. On `none` the
tier's chain is exhausted: count it as the step's failure and take the tier rung below directly, because the variant
rung would re-run a model that is not answering; for a senior step it is terminal. The tier-rung spawn starts a fresh
`tried` on its own tier's chain.

`wait:<seconds>` comes back only on a 429 while the failed model has not yet spent the rate-limit schedule (30
retries in the shipped config; each call runs 10 inside it, so two waits cover it). The continuation carries the
count on, and once it is spent the tool answers the next chain entry instead. Wait that long in one
`shell` call (`sleep <seconds>` with the call's timeout above it), then continue the same worker on the same model
the same way, leaving `tried` as it is. A wait is not a step failure and not a retry: it adds nothing to
`WORKER_RETRY_PER_STEP` or `STEP_FAILURES` and keeps the step on its rung. The tool bounds the waits per model (two
in the shipped config, more when a worker meets a second throttle after a clean stretch), so take its answer each
time; only as a guard against a loop, treat the answer as `none` once one step has waited ten times. Only `none`
counts as the step's failure.

**Worker reported `[BRIEFING GAP]`**: it could not proceed because something Section 6 should have carried
was missing. Re-assemble the missing block and re-spawn at the same tier. Never escalate for this: the
tier is not what failed.

**Bounded at two.** The re-spawn does not count against the two-retry budget below, so it has its own bound (when
the plan itself lacks the block, every re-spawn reports the same gap). On the third report for one step, stop
re-spawning and take the plan-spec BLOCKER branch in 3c: name it, then `question` (`Edit plan to fill the gap and
re-verify` / `Accept as Risk and proceed` / `Stop`).

**Failures attributed to one step** climb two rungs at most, each counted in `WORKER_RETRY_PER_STEP`:

1. **Variant rung, first failure** of a `quick`, `junior` or `junior-high` step: re-spawn at the same tier with
   `model` set to the model the failed attempt ran on, one reasoning variant up (`#low` to `#high`, `#high` to
   `#max`). Skip the rung when the variant cannot rise: the model already runs at `#max`, or it has no variant at
   all (the `subagent` tool rejects a variant the model does not offer and lists the ones it does). Then the first
   failure goes straight to rung 2. The rung follows the model actually spawned: a `quick` step routed to
   `ac/plan-worker-junior` by the codebase-state rule in 1c retries on junior's model at `#max`, and a step that is
   running on a fallback model raises that model's variant.
2. **Tier rung, second failure** (or the first when rung 1 is skipped): re-spawn one tier up (`quick` to `junior`,
   `junior` and `junior-high` to `senior`) on the new tier's own model, with no `model` argument.

Record each rung as it fires, as a wisdom line for the current wave: `[RETRY] Step <N> <tier>: rung <1|2>, <one-line
cause>`, with the tier that failed, and nothing when no rung fired. `[RETRY]` lines do not count toward the five
wisdom items in 2f; `ac plan-stats` reads them to measure what each tier costs in quality.

`senior` has no rung 1, because its chain already runs at `#max`, and no rung 2, because nothing sits above it: a
senior step's first failure is terminal. A failure after rung 2 is terminal too. Record a terminal failure the same
way, `[RETRY] Step <N> <tier>: terminal, <one-line cause>`.

These re-spawns keep the step's current model and do not advance the ladder: a malformed report with no
`### Changes Made` or `### Verification` (re-spawn at the same tier with a format reminder; a second malformed
report counts as the step's first failure), a `[BRIEFING GAP]` re-spawn, and a provider-fallback re-spawn, which
changes the model but not the rung.
The retry briefing leads with the failure context, then repeats the original.
Two fast paths skip rung 1: a worker flagging `tier mismatch` goes straight to rung 2 and the
mis-classification goes in the report, and a worker flagging `[CONTRADICTION]` does not retry at all,
because the next attempt hits the same structural conflict; mark it `pending-remediation` for 2f remediation.

**A retried worker is not verified until you verify it.** 2d ran before the retry spawned. After each retry, variant
rung, tier rung or provider fallback: re-stage and re-diff scoped to that step's `Files`, re-run Layer A, and re-run
the attribution for that step, before 2g commits.

**Terminal failure** (the tier rung failed, or a senior step failed first): append exactly one `{step, wave}` to
`STEP_FAILURES` for the step, however many retries it spent, and fire 2j at 3. Do not block the
wave on one failure unless 2i says a later wave depends on it.

### 2f. Remediation and wisdom

Runs after 2e, once every step has a terminal status (verified, failed, or `pending-remediation`).

1. **Remediate what the orchestrator owns**: `[CONTRADICTION]` reports, cross-file findings deferred from
   Layer B, and plan oversights your review surfaced. Apply the minimal patch to the file that structurally owns the
   missing piece, update `MODIFIED_FILES`, clear any `pending-remediation` step whose `Done when` now passes, and
   record each as a `[REMEDIATION] Step <N> <tier>: <what you fixed>` wisdom line (`Step - -` when no step owns
   it). Surface first when a patch would change a downstream contract;
   mechanical framework-completeness patches do not need a gate.
2. **Extract wisdom**: up to 5 concrete items this wave, 15 total, codified patterns rather than platitudes.
   `[REMEDIATION]` and `[RETRY]` lines are records, outside the 5 and the 15. Persist all of them to `wisdom.md`
   under `## Wave <N>`.
3. **Re-ground**: emit a 2-3 line wave summary and refresh the marker's `note` with a resume hint, which is what you
   read back after a compaction. Re-read `PLAN_PATH` and `wisdom.md` only when a compaction has actually happened
   since you last held them; `grep -c '^- \[ \]'` already told you what remains.

### 2g. Wave checkpoint commit

When the wave changed tracked files and `NO_CHECKPOINT_COMMITS` is not set, commit after 2f, before the next
wave. `git commit -m "<one line naming the wave>" -- <wave_files> .ac/plans/<slug>`, not the `commit` skill: loading
it admits a long body and spends turns on style detection, once per wave, to produce a checkpoint the Phase 4
commit squashes anyway. The final commit at 4a is where the `commit` skill earns its cost.

Commit the wave's paths explicitly, never `git add -A`: the parent repo may carry unrelated work, and `-A` would
snapshot it as this plan's deliverable, once per wave.

The gate is "did this wave change anything", which `git status` answers; no plan-wide label decides it, the
reviewer tier or the oracle default.

A commit failure here is a BLOCKER: print the git error and take the branch in
`references/execution-state.md`. Never auto-retry, because a failed commit usually means the
tree is in a state you did not expect.

### 2h. Progress table

After each wave, render the per-step table using the shape at
`references/wave-orchestration.md` under `## Phase 2h progress table`.

### 2i. Wave dependency check (before launching the next wave)

Before the next wave's workers launch, check whether any failed step is a hard dependency for it. The three sources,
in order: the plan's `### Dependency Notes`, a next-wave step whose `Files` names a file a failed step was to create,
and a next-wave step whose `References` point at a failed step's output.

If one failed, this is a BLOCKER even under auto mode. Emit one line naming it, then `question` (header
`Dep failed?`, options `Stop and investigate (Recommended)` / `Fix the failed step manually and resume` / `Skip the
dependent steps and continue`). The first two delete the marker before halting; the third leaves it in place because
the run continues. Procedure at `references/wave-orchestration.md`.

If nothing hard failed, the next wave launches automatically. Auto-continue is the default between waves.

### 2j. 3-strike rule

When `STEP_FAILURES` holds 3 entries **spanning two or more distinct waves**, emit one line naming the
BLOCKER and `question` (header `Halted?`,
options `Accept and continue (Recommended for known-isolated failures)` / `Fix manually and re-verify` / `Stop and
investigate`).

`Accept and continue` logs the failures, leaves the marker in place, and moves to the next wave; the failures surface
in the Phase 4 report. The other two delete the marker first, then pause or halt. This is a BLOCKER even under auto
mode: three accumulated failures make the `(Recommended)` qualifier unsafe to assume.

The two-wave span keeps the count meaningful: three failures inside one wave is one bad wave, not a systemic
pattern. An entry is one step at terminal failure, so a step that spent both retries before failing counts once.

### 2k. Loop until all waves complete

Run 2b through 2j for each wave in sequence, auto-continuing between them; only 2i and 2j pause the loop. When the
final implementation wave completes, advance to Phase 3.

## Phase 3: Final code-review

Goal: gate the deliver with one independent code-review pass on the actual implementation: does the work match the plan and meet quality bars.

**Aim for zero CRITICAL findings** from Phase 2's verification. The reviewer reports rather than gates, so a CRITICAL finding here costs a fix and a re-verify, not a loop.

### 3a. Final automated pass

Run the build in the foreground; the reviewer reads code that must at least build. Then start the full test suite
and the repo-wide lint with `background: true` on the `shell` call, in the same response that spawns the reviewer in
3b (a project script whose name does not say test or lint, such as `make ci` or `composer qa`, goes under `timeout
3600` so the stop guard counts it as work that will finish), so the two run side by side. Both must be green before
Phase 4: when the background run notifies you, a failure there is a finding like the reviewer's and goes through 3c.
When the reviewer finishes first, end the turn with a one-line status; the suite's notification starts the next one.

Then open this run's section of the review log, once:

```
shell: mkdir -p .ac/plans/<slug> && { grep -qx '## Run <marker started_at>' .ac/plans/<slug>/review-log.md 2>/dev/null || printf '
## Run %s
' '<marker started_at>' >> .ac/plans/<slug>/review-log.md; }
```

The log is append-only across runs and this header scopes this run's entry; a second `/ac/execute <slug>` writes
its own section rather than reading the previous one, and the `grep -qx` guard stops a re-entry from opening a
duplicate header.

### 3b. Spawn the reviewer

```
subagent({ agent: "ac/plan-code-review",
           description: "Final code-review",
           prompt: "Plan: <PLAN_PATH>
Modified files: <MODIFIED_FILES, newline-separated>
Wisdom: <wisdom.md path>
<only when signal 1 below fired alone: Criticality surfaces by path: <the surfaces>. Weigh failure scenarios there.>" })
```

One reviewer, whatever the plan's size.

**Spawn `ac/oracle` alongside it, in the same response, only when the planner judged the change critical.** Three
signals: signal 2 or signal 3 fires it, signal 1 alone does not, and `--no-oracle` forces the skip either way:

1. `MODIFIED_FILES` lands on one of the closed six surfaces in `../plan/references/model-tiers.md` rule 5:
   authentication or authorization, payment or billing, cryptographic operations, user-input to SQL or shell or file
   path, file upload or deserialization, destructive migration.
2. Any step's `Why this tier` begins `rule-5-criticality`, the planner's own judgement written at Stage 5.
3. The plan carries an `### Oracle Sanity-Check Findings` section, meaning Stage 3.5 already found
   something worth a second opinion at planning time.

Signal 1 alone is weak, since a file path rarely announces "cryptographic operations" or "destructive migration":
it adds the `Criticality surfaces by path` line to the reviewer brief above and spawns no oracle. When signal 2 or 3
fired, the oracle runs on its own model.

```
subagent({ agent: "ac/oracle", description: "Oracle strategic review",
           prompt: "Plan: <PLAN_PATH>
Modified files: <MODIFIED_FILES>
Research the plan was built on: <.ac/plans/<slug>/research/>
Wisdom from the run: <.ac/plans/<slug>/wisdom.md>
The change touches <the surfaces that fired>. Review the diff for failure scenarios on those surfaces,
and test the plan's claims about what the code does against the code: they are premises, not findings.
Plan compliance, reuse and caller impact are the code reviewer's; do not repeat them. Use your standard
report (Coverage, Premises, Findings with severity and CONFIRMED or PLAUSIBLE, scenario and fix, Bottom
line, Confidence)." })
```

### 3c. Act on the findings

The reviewer returns findings tagged CRITICAL, IMPORTANT or MINOR, each with a confidence. There is no
verdict and no revision loop. You are the filter, holding the plan, the wave history and the wisdom file:

- **CRITICAL**: fix it before Phase 4, with `edit` at each cited `file:line`, smallest correct fix, the
  reviewer's `Fix:` line as guidance. Then re-run the per-file checks and related tests on what you changed
  (`references/verification.md`), and the full suite again only when the fix touched code other modules call.
- **IMPORTANT**: fix when the fix is small and local; otherwise record it in `report.md` and add it to
  the plan's `## Deferred Ideas`.
- **MINOR, or anything under confidence 50**: `report.md` notes. Do not touch the code for these.
- **An oracle PLAUSIBLE finding** names what would confirm it: run that check before acting on it as CRITICAL or IMPORTANT, and treat an unchecked one as MINOR.
- **An oracle REFUTED premise** means the plan is wrong about the code, whatever the Findings say: route it through the plan-is-wrong BLOCKER below, naming the premise and the quote. An UNSUPPORTED premise goes to `report.md` with the search the oracle named.

Expect volume: both reviewers report everything rather than pre-filter, so a long list does not mean bad code.

**A finding that says the plan is wrong rather than the code is a BLOCKER even under auto mode.** Name
it, then `question` (`Edit plan to fix and re-verify` / `Accept as Risk and proceed` / `Stop`).
Never silently rewrite the plan.

Append the outcome to `.ac/plans/<slug>/review-log.md` under `## Run <marker started_at>`: first one line per
reviewer that ran, exactly `Review: <ac:plan-code-review | ac:oracle> CRITICAL <n> IMPORTANT <n> MINOR <n>`
counting the findings it returned, then what was fixed and what was deferred. `ac plan-stats` reads those lines to
judge a reviewer's effort level against what it finds.

### 3d. Convergence

CRITICAL findings fixed and re-verified, or none returned. Advance to 3e.

### 3e. QA pass

Runs when `QA_ENABLED` is true and `NO_QA` is unset. Otherwise emit one heartbeat line naming which of the two skipped
it and go straight to Phase 4. A plan step that already walked the app live does not replace the pass: its Layer C
evidence reaches the tester as `Existing evidence`, and the tester skips those scenarios and still runs the rest.

1. Emit one heartbeat line (`QA pass: running qa for <slug>`) and refresh the marker's `note` so a resume knows
   where the run stands (`Phase 3e QA in progress; load the qa skill with --plan <slug> again or go to 4a`).
2. Load the skill and run it on the request `--plan <slug>`. Skills take no arguments, so the loaded body reads its
   flags from that request. It never asks the user anything, so no `--auto` is passed:

   ```
   skill({ id: "qa" })        // then continue with the request: --plan <slug>
   ```

   Its tester, `ac/qa-tester`, runs in the background, so `qa` may end a turn with `QA: tester running for run
   <run id>; resuming on its notification`. That wait is expected: the notification resumes inside `qa`, and the
   stop guard stays quiet. Do not poll, sleep or read the tester's output, and do not treat that turn end as the
   QA result.
3. When the skill finishes, read `result.txt` (written by `qa` in the directory of the block's `report:` path) and
   append its content to `.ac/plans/<slug>/review-log.md` under `## Run <marker started_at>`, the header 3a opened.
   With `report: none` the printed block is the record. When the file is missing, append the printed block plus
   `result.txt missing`, and still apply the rule below. Append its `fixed files` to `MODIFIED_FILES` (nothing for
   `none`). The skill has already triaged and fixed by the 3c rules and run its one retest, so do not re-triage or
   re-run it here. When `fixed files` is not `none`, re-run 3a (build, full suite and lint, in the foreground) before
   4a, because 4a commits with `--skip-preflight` on the strength of 3a having covered those edits.
4. Continue to 4a in the turn the block prints. Under `--plan` the block is a hand-back to this skill, not a turn end;
   ending the turn on it would meet the live marker's stop guard.

Every QA status (`passed`, `findings`, `could-not-run`, `skipped`) continues to Phase 4, and none is a BLOCKER: a
dev server that would not boot or a missing QA tool goes into the QA and Phase 4b reports. Findings the skill left
unfixed live in its report, with open lows and unfixed mediums added to the plan's `## Deferred Ideas`.

The pass sits before 4a, which deletes the marker and then commits and pushes, so QA runs inside the stop guard
and its fixes reach the final commit.

## Phase 4: Deliver

Goal: commit, write the report, render the summary.

### 4a. Final commit

**Delete `.ac/state/active-execution.json` first**, before the F7 check and any commit.

**F7 skip check**: run `git check-ignore -q` on every file in `MODIFIED_FILES`. If all are ignored and
`git status --porcelain` shows tracked changes not in `MODIFIED_FILES`, the parent repo has unrelated work that a
commit would snapshot as this plan's deliverable. Skip it, say so in one line, and record it in the report under
`## Commits` with the path and the count. The plan's `Git context:` field is a hint; git state is authoritative.

Otherwise load the `commit` skill and run it on the request `--skip-preflight`, plus `--no-push` when `LANE_MODE` is true or `.ac/state/active-auto.json` names this session (its `harness` is `opencode` and its `session_id` is this session's `root_session_id`; a marker without `harness` was written by Claude Code and is not this run's): an unattended run has nobody present to approve a push, and the `commit` skill's branch guard only asks on `main` or `master`. A lane checks `LANE_MODE` on its own because `.ac/` is gitignored, so its worktree never holds `active-auto.json`; only the coordinator publishes.

```
skill({ id: "commit" })    // then continue with the request: --skip-preflight (plus --no-push under LANE_MODE or an away marker)
```

Without either, the final commit pushes as the `commit` skill does. Phase 2d and Phase 3 already covered the
verification `--skip-preflight` refers to. A clean tree exits silently, which is fine.

### 4b. Report and summary

Write the report, `.ac/plans/<slug>/report.md` (under `LANE_MODE` `.ac/plans/<slug>/outcome.md`, the name the Claude
Code side must use because its host refuses a subagent's `report*.md`), from the template at
`references/report-template.md`. Confirm
it landed with `test -f ... && wc -l ...`; retry the write once if it did not, and render the report inline if the
retry also fails, so the work is not lost in chat history.

Then render the closing summary inline from `references/execution-summary-template.md`. The
summary is chat output; `report.md` is the file artifact.

End the turn. Under `LANE_MODE` the last thing written is the `status: DONE` block, with `outcome.md` in `artifacts`.
