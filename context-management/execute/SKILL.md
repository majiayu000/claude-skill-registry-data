---
description: "Run an approved ac plan to completion, wave by wave, with cost-tiered workers, per-wave verification and a final review."
when_to_use: "Use after /ac:plan writes a plan you want built; takes a plan slug or path."
argument-hint: "<plan-slug | .ac/plans/<slug>/plan.md> [--auto] [--no-oracle] [--no-checkpoint-commits]"
effort: high
---

# /ac:execute

Executor that runs an approved plan to completion. Auto-continue between waves: never asks "should I continue". The wave is the unit of every orchestrator action, and manual review of the wave diff is non-negotiable. Final code-review gates the deliver.

Plan: $ARGUMENTS

## Standing rules

These hold for the whole run, including after a compaction. Everything below this block is procedure; these are the bounds. They sit here because a re-attached skill keeps only its first 5,000 tokens after compaction (https://code.claude.com/docs/en/skills.md) and this body is far larger, so a rule further down is gone from context on exactly the long runs that need it.

**Turn termination.** Your turn ends on exactly one of: an `AskUserQuestion` call, the Phase 4b execution summary, a named BLOCKER from `<auto_mode>`, or a one-line wait status while background workers you spawned still run (each task-notification starts your next turn; never wait with a `sleep` or polling loop). Nothing else ends it. Never end a turn by describing what you would do next, and never propose that the user open a fresh session to continue the run.

Every branch that terminates the run deletes `.ac/state/active-execution.json` first. That is not bookkeeping. While the marker exists and no background worker is running, the plugin's `Stop` hook blocks the turn from ending and returns the outstanding step count to you (`${CLAUDE_PLUGIN_ROOT}/hooks/stop-guard.sh`); the marker's absence is what permits a terminal stop.

**Context.** Auto-compaction summarizes older turns and the run continues. A filling context window is not a stopping condition, not a reason to hand the remainder back, and not a reason to suggest a new session. No compaction command is available to you: `/compact` is a local CLI command (`commands/compact/index.ts:5` sets `type: 'local'`; `tools/SkillTool/SkillTool.ts:421-427` rejects any command that is not prompt-based), so never plan around invoking it. When the procedure you need has been truncated away, re-invoke the `ac:execute` skill to restore this body, then read `PLAN_PATH` for the authoritative step state.

**A stop needs a name.** "I cannot verify this properly in the remaining context" is a stop wearing the clothes of a report. When a step genuinely cannot be completed to the plan's standard, the reason is one of: a fact you do not have and cannot obtain, a decision only the user can make, or a gate you cannot pass. Each maps to a BLOCKER branch (2i, 2j, 3c) that surfaces an `AskUserQuestion` and deletes the marker. Name the class, take the branch, report what did land. Never substitute a capacity limit for the real reason.

**No review loop needs bounding.** Phase 3 is one reviewer pass and the findings are yours to filter, so nothing counts iterations. Three bounded loops remain: one retry per step at 2e, at most two briefing-gap re-spawns per step at 2e, and the three-failures-across-two-waves halt at 2j. The first and third read their state from `STEP_FAILURES`; the second counts re-spawns for the step in front of you.

**Progress surface.** Two surfaces carry it and neither is a tool. The plan file's checkboxes are the per-step record, ticked at Layer D and counted with `grep -c '^- \[ \]'`, which is also what the `Stop` guard reads. Phase 2h prints the per-step table after each wave. Add one short line per phase and wave transition and that is the whole picture.

There are no task tools to build on: Claude Code leaves them out on Opus 4.8, Sonnet 5, Opus 5 and later ("the tools' definitions and reminders take up context"), and on the older models and background sessions that still get them, `CLAUDE_CODE_ENABLE_TASKS=false` (the `/ac:install` Group D trim) swaps them for `TodoWrite`. Do not write a procedure that depends on either.

**Output length.** Per-turn user-facing prose: at most 3 lines. The wave summary at 2f: at most 3 lines. Filter tool output before it lands: a passing test suite through `tail -20`, a diff scoped to the wave's files. The 2a strategy render, the 2h progress table, and the Phase 4b summary are the only long surfaces, and their templates fix their shapes. Anything a later reader needs goes in `wisdom.md` or `report.md`, not into the chat. This is a cost rule, not a style one: every token you write stays in context and is re-read as cache on every later turn, so one measured run paid 441k output tokens across 364 turns and carried each of them for the rest of the run. A file is read on demand; a sentence in the chat is read hundreds of times.

<role>
You are the Developer orchestrating execution of an approved plan at `.ac/plans/<slug>/plan.md`. You delegate every implementation step to a tier-routed worker subagent (`ac:plan-worker-quick` / `-junior` / `-junior-high` / `-senior`), verify each wave through the 4-layer check, commit after any wave that changed tracked files, then gate the final deliver with one code-review pass (and `ac:oracle` when a criticality surface is touched). The plan is the spec; you execute it precisely.
</role>

<scope>
Source code in the project, scoped to the files each step declares, plus these artifacts under
`.ac/plans/<slug>/`: `wisdom.md` (max 15 items, max 5 per wave), `evidence/<step-id>-<scenario>.<ext>`,
`review-log.md` (append-only, one entry per Phase 3 review, kept as a record rather than as a loop counter), and
`report.md`. The wave commit is a plain `git commit`; the final commit at Phase 4 goes through `/ac:commit`.

`plan.md` is read-only here except for Layer D checkbox ticks and a reviewer-flagged plan-spec fix. If the plan is
wrong, report and stop. Source outside a step's declared Files is out of scope; bonus refactors break atomicity.
</scope>

<capabilities>
The base tools plus `AskUserQuestion`, which arrives directly rather than deferred.
`Agent` spawns the four worker tiers, `ac:plan-code-review`, and `ac:oracle`. `Bash` takes the wave diff, which is Layer B's
input, and also runs build, test, lint, the wave commit, and the QA tools a step names. `Read`, `Grep` and `LSP`
are how the rest of Layer B happens, and none of it is optional. `Skill` invokes `/ac:commit` once, at Phase 4.

Subagents are separate HTTP calls with their own system prompt and inherit none of your context, so every worker gets
the full six-section briefing. Drive every chain from here: the four plan-workers cannot spawn anything (their
`tools:` allowlist omits `Agent`), and the code reviewer plus `ac:oracle` have `Agent` denied so their retrieval
stays inside the budget you gave them. A chain means the agent reports back and you make the next call, which is also
the only way its cost stays visible.
</capabilities>

<constraints>
- Auto-continue between verified steps and waves. Never ask "should I continue".
- Copy the step's `Description`, `Files`, `Done when`, `QA`, and `Must NOT` into the briefing verbatim. Paraphrase
  inverts opt-in and opt-out, which is the most common worker failure.
- The wave is the unit of every orchestrator action: one diff, one typecheck, one build, one test run, one linter
  pass, one commit per wave. The two exceptions are per-step and stay per-step: the Layer C QA scenario, which is
  the only evidence anything ran, and the Layer D checkbox, which the `Stop` guard reads as the progress signal.
- All four verification layers run on every wave, and none of them is optional. Layer B means reading the wave
  diff hunk by hunk and matching every hunk to a worker's claim, not sampling.
- Inject `TDD_MODE` into every briefing.
- Wave-after commits whenever the wave changed tracked files; the final commit always.
- Do not call `EnterPlanMode`; the plan is approved. Do not modify `plan.md` beyond Layer D ticks, and never rewrite
  it silently when a reviewer says the plan is wrong: surface it.
- Mutate a file with `Edit` or `Write`, never through `Bash`. Not `python3 -c`, not a `cat >>` heredoc, not `sed -i`,
  not `perl -pi`, not `tee`. Two reasons, both measured on one run: a Bash rewrite spends the old text AND the new
  text AND the script wrapper as output tokens, which put 34 `plan.md` rewrites among that run's largest payloads at
  7,000 to 11,000 characters each; and `Edit` is the only verb that fails loudly when the anchor it targets is not
  unique, which is the whole guarantee you want when patching a plan you are also reading. Appending to `wisdom.md`
  or `review-log.md` is the one exception where a heredoc is fine, because there is no anchor to match.
</constraints>

<auto_mode>
`--auto` in the argument string sets `AUTO_MODE = true` for the run, and `/ac:plan` Stage 6a passes it when it chains
here. Auto mode resolves flow gates; it never skips verification, the wave-after commit, or the final code-review.

| Call site | Class | Under `AUTO_MODE = true` |
|---|---|---|
| 2a Execute? | flow | auto-pick `Execute` |
| 2i Dep failed? | BLOCKER | surfaces |
| 2j Halted? (3 failures spanning 2+ waves) | BLOCKER | surfaces |
| 3c plan-spec issue | BLOCKER | surfaces |
| Wave checkpoint commit failed | BLOCKER | surfaces |
| Verification failed on a step a later wave needs | BLOCKER | surfaces |

Flow gates resolve to the `(Recommended)` option and emit one heartbeat line. BLOCKER gates surface whatever the mode,
because each needs judgment auto mode cannot supply: a dependency failure, three accumulated failures, a wrong plan, a
commit failure hiding repo state, or lost downstream work. Before surfacing one, emit a line naming which class fired.
`AUTO_MODE` stays set through a BLOCKER unless the user picks an option that stops the run.

Heartbeat: one short line per phase, wave, and iteration transition, and per auto-resolved gate.
</auto_mode>

<bootstrap>
Nothing to load. `AskUserQuestion` arrives directly on the main thread, and there is no task list to register (see Progress surface). Begin at Phase 1a.
</bootstrap>

## Phase 1: Load Plan

### 1a. Parse arguments

- Strip `--auto` flag if present → `AUTO_MODE = true`. Engages auto mode per `<auto_mode>` policy: auto-resolve auto-eligible `AskUserQuestion` calls, halt only on BLOCKER classes. If this skill was chained from `/ac:plan` Stage 6a auto-mode handoff (Skill tool invocation with `args: "<slug> --auto"`), the flag is passed as part of the argument string.
- Strip `--no-oracle` flag if present → `NO_ORACLE = true`. Phase 3 spawns `ac:oracle` beside the reviewer when the change touches one of the six criticality surfaces; this flag opts out of that.
- Strip `--no-checkpoint-commits` flag if present → `NO_CHECKPOINT_COMMITS = true`. Disables wave-after commits; Phase 4 final commit still runs.
- Resolve the remaining argument to `PLAN_PATH`:
  - If it contains `/` or starts with `.ac/`, use as full path.
  - Otherwise treat as slug: `.ac/plans/<slug>/plan.md`.
- If `PLAN_PATH` does not exist: print `Plan not found at <path>. Run /ac:plan first.` and stop.
- If `AUTO_MODE = true`, emit one user-visible line: `Auto mode engaged. Will run end-to-end, halting only on BLOCKER classes (Phase 2i dep-failed, Phase 2j 3-strike, Phase 3c plan-spec issue, error-handling halts).`

### 1b. Read and parse the plan

Read `PLAN_PATH` in full and hold: the frontmatter (`Steps`, `Waves`, `Codebase State`, `Generated`), `## Research Summary`, `## Codebase Conventions` including the `TDD` field,
`## Reuse Map`, `## Work Objectives` (Core Objective, Concrete Deliverables, Definition of Done, Must Have,
Must NOT Have), `## Execution Strategy` with its Dependency Notes, every step in `## Steps` with all its fields,
and `## Risks Accepted`. `## Tier Calibration` is referential; read it once, do not re-read per step.

### 1c. Tier routing and escalation

| Tier | Subagent | Model | Effort |
|---|---|---|---|
| `quick` | `ac:plan-worker-quick` | `haiku` | not supported on this model |
| `junior` | `ac:plan-worker-junior` | `sonnet` | high |
| `junior-high` | `ac:plan-worker-junior-high` | `sonnet` | high |
| `senior` | `ac:plan-worker-senior` | `opus` | medium |

`junior-high` runs junior's model and effort (both `high` since Sonnet 5.5), for work at the borderline of coupling or context depth. The
criticality rule never routes there; it escalates to `senior`.

When the plan's `Codebase State` is `legacy` or `chaotic`, route every `quick` step to `ac:plan-worker-junior`
whatever its declared tier: mechanical work in an inconsistent codebase is not mechanical, and Haiku has no effort
lever to compensate. The plan file is not modified; this is an in-memory routing decision. Record the count for the
Phase 4 report.

### 1e. Initialize execution state

```
ACCUMULATED_WISDOM = []                 # max 15 items total, max 5 added per wave
MODIFIED_FILES = []                     # tracked across waves; passed to Phase 3
STEP_FAILURES = []                      # {step, wave} per failure; 2j asks whether they span 2+ waves
WORKER_RETRY_PER_STEP = {}              # max 1 tier-escalation retry per step
```

No Phase 3 counters: the review is one pass and its outcome is appended to `review-log.md` as a record.

Then write `.ac/state/active-execution.json`. Three hooks read it: the file-scope guard scopes worker edits to
`wave_files`, the SessionStart hook names the active plan after a restart or compaction, and the `Stop` guard refuses
a turn end while it exists. Fields: `slug`, `session_id` (write exactly `${CLAUDE_SESSION_ID}`, which Claude Code substitutes with this session's id;
it scopes the `Stop` guard to this run), `started_at` (24-hour age bound; take it from `date -u +%Y-%m-%dT%H:%M:%SZ`,
never from your own sense of the time, since a local time with a `Z` reads as the future and disarms the guard), `pid` (advisory, write `0`), `current_wave`, `wave_files`, `note`. Schema and
per-field reasoning at `${CLAUDE_SKILL_DIR}/references/execution-state.md`.

Lifecycle: written here, refreshed at 2c and 2f, deleted at 4a and on every branch that ends the run early. A halt
that leaves it behind gets blocked by the `Stop` guard until its block budget is spent.

`.ac/state/active-auto.json` may coexist beside it. That marker belongs to `ac:auto`, not to this skill: never
delete it, and treat its presence only as the signal read at Phase 4a.

### 1f. TDD mode

Read the plan's `## Codebase Conventions` for `**TDD**` and set `TDD_MODE`: `"tdd"` directs each worker to write the
failing test first, `"tests-after"` to write tests after implementation for any behavioral change, `"none"` to write
tests only when a step's `Done when` demands testable behavior. A missing field defaults to `"none"` and gets noted
in the Phase 4 report. The value is injected into every worker briefing.

Read project `CLAUDE.md` and `CLAUDE.local.md` for build, test, and lint commands as `RUNTIME_CONTEXT`. Workers
receive `CLAUDE.md` automatically; `RUNTIME_CONTEXT` supplements it with the explicit commands briefings cite.

### 1g. Confirm the progress surface

No list to register. Read `Waves` and `Steps` from the plan frontmatter and hold both: `Steps` is what every
Layer D count gets compared against, and `WAVES` is how many barriers the run will pass. State both in the
Phase 2a render so the shape of the run is visible from the start.

Then run the shape gate once:

```
Bash: node "${CLAUDE_PLUGIN_ROOT}/cli/ac.js" plan-check <PLAN_PATH>
```

It prints the step counts on every exit and, when the plan deviates from what the rest of this body parses, one
line per deviation. `/ac:plan` runs the same command at Stage 5, so a clean exit here is the normal case and a
dirty one means the plan was written by hand, written by an older version of the planner, or edited since. Route
by what it reports, taking the FIRST route below that matches, except that a BLOCKER route always wins over a
continue route on the same step:

- **Exit 2**: the plan file is not where you looked, which is a different problem from a malformed plan and has a
  different fix. Re-derive `PLAN_PATH` from the argument and try once; if it still fails, say the path you tried
  and stop.
- **Exit 0**: continue. Hold the step counts it printed for Layer D; on a resume the unchecked number is what is
  left to run.
- **`All <N> Step N headings are present, so the step lines are missing their prefix`**: repair, do not stop.
  Every step is in the file and only its checkbox is absent, so the plan is gaining a record it should already
  have rather than changing its spec. Insert one `- [ ] **Step N**: <the heading's own title>` line per step with
  `Edit`, keeping the space after the bracket because the `Stop` guard greps for it, then re-run `plan-check` and
  say in one line that you repaired it and how many lines you added. Layer D would otherwise have nothing to tick
  and the guard would read a permanently satisfied count, so both controls would retire silently.
- **`step(s) are absent from the body rather than merely unticked`**: the plan is truncated, not unticked. Do not
  invent checkboxes and do not correct the frontmatter down to what survived: either edit runs a plan that is
  missing most of its work while reporting success. Say how many steps are missing and stop.
- **A worker step with no `Tier`, or a verification step with no `Commands` or `Evidence`**: a plan-spec defect
  rather than a formatting one. There is nothing to spawn or nothing to run, and picking a tier yourself
  substitutes your judgment for the planner's on a cost decision the plan was supposed to make. Take the 3c
  plan-spec BLOCKER branch, naming the steps and what each is missing. **This wins over the next route.** A step
  can report both an unrecognised `Type` and a missing `Tier`, and routing it on its fields first would read a
  code step as a verification step, run its `Commands`, tick its box, and never write the code.
- **A `Type` outside the three, on a step this list has not already blocked**: route on the step's fields instead
  of its label, and say in one line which steps you re-read and as what. A step carrying a `Tier` is a worker
  step, because `Tier` is meaningful on nothing else; a step carrying `Commands` and `Evidence` with no `Tier` is
  a verification step. `implementation` is the value this actually produces and it maps to `code`.
- **Any other ERROR** (a missing `Files`, `Description`, `QA` or `Must NOT`, a leftover placeholder, a missing
  `Auto mode` line): a plan-spec defect. The worker briefing inlines four of those five fields verbatim, so a
  step missing one sends a worker out with a hole in its contract. Take the 3c plan-spec BLOCKER branch and name
  the steps and fields.
- **A count mismatch the ticks do not account for**: the frontmatter and the body disagree about how many steps
  exist. Say which two numbers you got and stop; every later Layer D comparison rests on this one, and a count
  compared against a wrong total confirms nothing.

WARN lines never gate the run. Say how many there were in one line and continue.

## Phase 2: Execute Wave-by-Wave

Goal: run each step to verified completion, wave by wave, on auto-continue. The user sees progress through the plan file's checkboxes and the Phase 2h table; they do not approve each step.

### 2a. Present execution strategy

Render the wave breakdown once using the shape at `${CLAUDE_SKILL_DIR}/references/wave-orchestration.md` under
`## Phase 2a execution-strategy render`: plan title and path, complexity, codebase state, TDD mode, totals, one line
per step per wave with its tier and files, the review routing, and whether checkpoint commits are on.

Then `AskUserQuestion` (header `Execute?`, options `Execute (Recommended)` / `Adjust wave grouping` / `Cancel`).
`Adjust wave grouping` takes a freeform follow-up, re-renders, and asks again. This is the only user gate inside
Phase 2; once execution starts, auto-continue applies until Phase 4 or a BLOCKER. Auto mode skips it and proceeds.

### 2b. Worker briefing template (the 6-section prompt)

Every worker invocation receives the 6-section briefing. For the exact template (with VERBATIM/DERIVED field annotations), read `${CLAUDE_SKILL_DIR}/references/worker-briefing-template.md`.

**The briefing is the worker's whole world.** It no longer reads the plan, so Section 6 carries the step's
pattern references, the codebase conventions, the invariants it must preserve and the plan-wide guardrails
inline.

**Resolve every sibling-step pointer before you send it.** Measured across 1,914 steps, 23% of Descriptions
say things like "call Step 4's parser" or "same constraint as Step 10". Those resolved when the worker read
the plan and dangle now. Wherever the step's `Description`, `QA` or `Must NOT` names another step by number,
replace the pointer with what the worker actually needs: the sibling's `Files` path and a one-line statement
of the contract, or the `file:line` the thing will live at. A forward pointer to a step that has not run yet
is the dangerous case, because there is no source to fall back on. This applies to every plan, including the
ones written before the briefing changed. Assemble all four from the plan you are holding; anything you leave out, the worker cannot go and
find. Dropping the plan read saves roughly 8k tokens of subagent input per worker, which is where the cost
of a rich briefing is paid back.

Length rule: under 30 lines is too short; under-spec'd briefings produce drift. Copy the contract fields
verbatim rather than paraphrasing, because paraphrase inverts opt-in and opt-out.

### 2c. Launch workers in parallel within the wave

**Refresh the marker first**: `current_wave` to this wave's index, `wave_files` to the union of every absolute path
in this wave's steps' `Files`. That set is exactly what the file-scope hook allows a worker to touch, so a path the
wave needs but does not declare cannot be written. The union has to be complete before any spawn.

**Route on `Type`**: `code` and `infra` spawn a tier-routed worker; `verification` does NOT spawn. Run its `Commands`
directly via Bash and capture to its `Evidence` paths. For a verification step Layer A blends with your Bash output,
Layer B is largely n/a, Layer C IS the evidence file, and Layer D still applies. A `Type` outside the three was
resolved at Phase 1g by reading the step's fields; use what 1g decided rather than re-deciding per step.

**Check invocation reachability before the wave launches.** When a step's Description tells you to run a slash
command, confirm you can: a component whose frontmatter carries `disable-model-invocation: true` is kept out of
your own list by design and can only be typed by the user. Read the component's frontmatter rather than grepping
the whole file, since several skills discuss the flag without setting it, and if it is set there, take the
plan-spec BLOCKER branch in 3c and say which command and which step. Do not quietly
substitute executing the command's body yourself: that tests the procedure and not the dispatch, which is a
different claim from the one the step is making.

Spawn every `code` and `infra` step of the wave in ONE message, one `Agent` block each, each with
`run_in_background: true`. Then wait for all of them before verifying any, and wait by ending the turn with a
one-line status: each worker's completion arrives as a task-notification that starts your next turn, and when one
arrives while others still run, end the turn again. Never wait with a `sleep` or `until` loop, a file-stability
check, or repeated reads of evidence files: that holds the turn for up to the Bash timeout and learns nothing a
notification would not, and the Stop guard allows the stop while workers run. Do not spawn one step, verify it, and then
spawn the next: a wave whose steps share no files has no reason to serialize, and the 4-layer check reads a finished
wave better than a finished step. A wave the plan declares as an ordered track (its Execution Strategy says the steps
must run in sequence) is the one exception, and there the steps run one at a time in the declared order.
Say which steps the wave is running in one line before the spawns, so a reader can follow without a task list.

### 2d. Wave verification (4-layer, runs once per wave)

Every worker in the wave has returned. Now verify, once, for the whole wave. You are the QA gate.
Subagents lie. Automated checks alone are NOT enough.

The unit is the wave, not the step. One typecheck, one build, one test run, one `git diff`, one linter
pass for the wave, however many steps it held. The step-level record is Layer D's checkbox and the
per-step QA evidence in Layer C, both of which stay per-step because they are cheap and because
something downstream reads them.

**Confirm no mutation survived.** Run `git status --porcelain` in the same message as the diff and the
Layer A commands; it does not depend on their results and they do not depend on its.

The allowed set is `wave_files` (this wave's declared union, from 2c) plus `MODIFIED_FILES` (earlier
waves) plus anything under `.ac/`. A dirty path outside all three is an unreverted mutation or an
out-of-scope edit: restore it from git, and record it as a `[REMEDIATION]` wisdom line naming the step.
Compare against `wave_files`, NOT against `MODIFIED_FILES` alone: that list is only appended at 2e, after
this check, so at this point it holds the previous waves and none of the current one. Compare against it
alone and every file this wave legitimately changed reads as a mutation to be reverted.

What this catches is an out-of-scope mutation arriving through `Bash`, which the file-scope hook cannot
see because it gates `Edit` and `Write`. It does NOT catch the temporary patch a worker uses to prove
its test really fails (`cp x /tmp/x.bak && perl -0pi -e ... && <test> && cp /tmp/x.bak x`): that file is
inside the step's own `Files`, hence inside the allowed set. That technique is worth keeping anyway, and
the diff is what shows whether the patch survived it.

Ordering does not matter here, which is why it is batched. The diff is taken with a pathspec limited to
`wave_files`, so an out-of-scope mutation cannot enter it whether this check ran first or not.

Then take the wave diff, which is Layer B's input:

```
Bash: git add -A -- <wave_files> && git diff --cached -U8 -- <wave_files>
```

Stage first, and diff the index. A plain `git diff` shows nothing at all for a file the wave CREATED,
because an untracked path has no committed side to compare against: verified in this repository, where
`git diff -U15 -- <new file>` returns zero lines while `git status --porcelain` reports it as `??`.
Without the staging step every file a wave creates is invisible to Layer B, and every claim its worker
made becomes a false "claim with no hunk" finding. Staging does not commit; 2g still decides that.

Measured on one 24-step run, the old per-step shape spent 261 Bash calls and 69 whole-file reads across
389 turns, with the same test suite running scoped per step, again at the barrier, and a third time in
Phase 3. The wave suite is a strict superset of the scoped runs, so the scoped runs bought nothing that
this shape does not.

**This barrier is mandatory and cannot be skipped.** It is now the only place a failure surfaces, which
is the trade the per-step checks were dropped for.

**Issue the wave's independent actions in ONE message.** The mutation check, the diff, the typecheck,
the build, the test run and the linter do not depend on each other's results, so they are one message
with six tool calls, not six turns. Same for the wave's checkbox ticks in Layer D, and for the QA
scenarios in Layer C that touch different surfaces. Batching is where the turn count actually falls:
collapsing per-step work to per-wave cuts the number of CALLS, but only issuing independent calls
together cuts the number of TURNS, and a turn on the plateau costs the whole resident context again.
Serialize only where one call's output decides the next one's arguments.

**Layer A: Automated**

**Layer A authority**: when the changed files sit under a sub-project root (its own `package.json` AND `tsconfig.json`,
and not the orchestrator's cwd), that sub-project's local typecheck wins: `cd <sub-project-root> && bun run tsc
--noEmit` or the language equivalent. The outer LSP runs against the outer repo's config and cannot resolve
sub-project deps, so its diagnostics on those files are Class 5 boundary noise. With no sub-project boundary, the
orchestrator's LSP is authoritative.

1. Run the appropriate typecheck (sub-project local OR orchestrator LSP per the authority rule above). Classify each diagnostic into one of six noise classes before deciding:

   Classify every diagnostic into one of six noise classes before acting on it. The classes, with what each one
   looks like and how to tell a transient from a real error, are at
   `${CLAUDE_SKILL_DIR}/references/lsp-noise-classes.md`. Classes 1 and 3 are transient and get re-run at the wave
   barrier; classes 2, 5, and 6 are persistent false positives that never block; class 4 is a real error and routes
   to Phase 2e. The plan's `**LSP false-positive whitelist**` field, when present, is the authoritative skip list.

   WARNING severity (regardless of class) is logged in Issues and continues.
2. Run the project's build command (from `RUNTIME_CONTEXT` or `CLAUDE.md`). Exit code 0 required. For sub-project layouts: use the sub-project's `package.json` scripts (`bun run build` / `npm run build` / etc.) inside the sub-project dir.
3. Run the full test suite and the repo-wide linter, once, for the wave. There is no scoped per-step run: the wave
   suite covers every file the wave touched and more, so a scoped run before it is a check you are about to repeat.
   Verify once; do not re-run a check that already passed to build confidence. All tests must pass; pre-existing
   failures unrelated to the wave are noted, not blocking. For sub-project layouts use the sub-project's command
   (`bun test` / `npm test`) inside the sub-project dir.

   Filter what the run admits into context, because a passing suite's output is noise you pay for on every later
   turn: pipe through `tail -20`, or the runner's own quiet or summary flag. On failure, admit the failing cases and
   nothing else. A failure the wave suite catches that no single step explains is a cross-step interaction, which
   routes to remediation below rather than to one step's retry.

**Layer B: Manual Code Review (read the wave diff, do not skip)**

This is the layer you are most tempted to skip. Do not skip it. What changed is that you review the
DIFF rather than re-reading whole files. The diff is the stronger instrument against a worker that
overstates what it did: it is the delta itself, where a full read shows an end state and asks you to
remember the before.

1. Read the wave diff taken above, hunk by hunk. Open a full file only on one of these four triggers,
   which are the whole list:
   - the file was created by this wave, so there is no before to diff against;
   - the file is under 150 lines, where reading it whole costs no more than reading its hunks;
   - the diff carries deletion hunks, where what was removed matters as much as what replaced it;
   - the step declares a contract in its `References` that the hunk appears to change.

   "When it looks ambiguous" is not a trigger. If you find yourself opening files outside this list,
   the plan's `Files` were wrong and that is a finding, not a reason to read more.

2. For each hunk:
   - Does the logic actually implement the step Description?
   - Are there stubs, TODOs, placeholders, hardcoded values that the step did not authorize?
   - Are there logic errors or missed edge cases evident from the data flow?
   - Does the change follow the plan's Codebase Conventions and `my-coding`?
   - Are imports correct and unused imports removed?

3. **Attribute every hunk, file first.** Attribution is by FILE: each hunk belongs to the step whose
   `Files` declares that path, which is deterministic from the plan. Fall back to the workers'
   `path:start-end` claims only when two steps of the same wave share a file.

   Line ranges cannot carry attribution on their own, and it is worth knowing why before trusting one.
   The wave's workers run concurrently in undefined order, so a worker inserting ten lines near the top
   shifts every range another worker reported; each is correct against the tree it saw and only the last
   writer's ranges survive into the final diff. `-U8` also merges nearby regions into one hunk with two
   claimants, and nothing bounds a claim's width, so a single `file:1-500` would swallow the file.

   Then check the claims against the diff. Three outcomes, and the first two fail the step:
   - a hunk in a file NO step declares: an out-of-scope write. The file-scope hook permits it because it
     gates on the wave's union rather than on one step's `Files`, so this check is the only thing that
     sees it. Treat as failed and route to 2e.
   - a claim the code contradicts: the worker described something it did not do. Treat as failed.
   - a claim with no hunk, or a hunk no claim mentions, inside a file the step does own: a reporting
     gap, not a code defect. Record it and continue; a formatter the worker ran leaves exactly this.

4. **Run the two checks the diff cannot give you**, because duplication lives in files you were never
   going to open: `LSP findReferences` on each newly exported symbol, and one repo-wide `Grep` for each
   new function name. A second definition of something the wave just wrote is the failure this catches,
   and neither the diff nor a whole-file read would have shown it.

5. If you cannot explain what each hunk does in one sentence, you have not reviewed it. Read again.
6. **Cross-file consistency check** (mandatory whenever the wave produced two or more files that share an interface). The worker sees one file; you see the whole wave, and the wave diff is a better input for this than sequential single-file reads were, because every side of a shared boundary sits in one artifact. This is also the check that covers the diff's known weakness, that a hunk does not show what the surrounding code now does, so it is not optional just because the diff read quickly. Apply it to every shared-interface boundary the wave's files declare or consume, not just the first. The seven boundaries, each with the concrete failure it catches, are at `${CLAUDE_SKILL_DIR}/references/cross-file-review.md`: shared data shapes, URL and path composition, component and function name match, template engine interop, front-matter is data not template, asset paths, link target reachability. Read that file at the first wave where the check applies.

**Layer C: Hands-on QA (per step, run here at the barrier)**

This layer stays per-step, because each step names its own scenario and its own evidence path, and the
evidence is the only proof anything actually ran. What changed is when: run every step's scenario here,
in one pass over the wave, rather than interleaved between spawns.

Skip the scenario for any step Layer B already failed. Its QA would exercise code that is about to be
retried, so the evidence would describe work that no longer exists. Run it after the retry instead,
alongside that step's re-verification in 2e.

When the step's `QA` field names a tool, run the scenario and gate it on four checks:

- **Reproducer-validity**: one command, fails on HEAD before the change (for a fix or regression step), deterministic
  across 3 runs, no external service that can flip the result. Mark a dimension n/a rather than skipping it.
- **Evidence, not assertion**: record the command AND its output, or an artifact path. A bare "verified" is not evidence.
- **Lowest layer that proves it**: a unit test beats an integration test beats an end-to-end run when all three would
  prove the same thing. Escalate only when the lower layer cannot reach the behavior.
- **Browser as a human user**: for any UI-touching step, walk it through the browser (navigate, interact, assert on
  rendered state), not just `curl`. `curl` proves the endpoint answered; only the walk-through proves the surface works.

Capture to `.ac/plans/<slug>/evidence/<step-id>-<scenario>.<ext>`: `.png` for a browser screenshot, `.json` for a
curl body, terminal output for a CLI or test run. Steps with no `QA` field, or `QA: none`, skip this layer.

**Layer D: Plan state check (per step)**

Run each step's provable `Done when` criterion first: the one command it names, batched into the same
message as the ticks. These are greps and single targeted assertions, not scoped suite runs, so a wave of
six costs one message. This is what the criterion was written to be, and running it is what stops the tick
from being a claim.

Tick each verified step's checkbox from `- [ ]` to `- [x]` with `Edit`, one edit per step. Confirm the wave's
ticks landed with `grep -c '^- \[ \]' <PLAN_PATH>` and check the number against what you expect, which is
the plan's total step count minus every step ticked so far. A count you do not compare against anything
confirms nothing. Do not re-read the plan to check: the plan runs to tens of thousands of characters and you already hold it from Phase 1b.

The tick stays per-step rather than batching with the rest of the wave, for a reason that is not
bookkeeping. The `Stop` guard derives "no progress" from this count falling between blocks
(`${CLAUDE_PLUGIN_ROOT}/hooks/stop-guard.sh`), and it latches permanently once no-progress fires under a
forced continuation. Batch the ticks to one edit per wave and a long wave shows the guard a frozen
count, which retires it for the rest of the run. It is also the only durable record of which steps
inside a wave finished, which the marker's `current_wave` cannot express after a restart.

### 2e. Verification outcome routing

Verification now runs per wave, so route per step off what Layer B attributed. A wave-suite failure or a
Layer B finding belongs to the step whose claimed hunks explain it; a failure no step's hunks explain is a
cross-step interaction and goes to 2f remediation, not to a retry. That attribution is what the per-step
scoped test used to provide, and it is why Layer B's hunk-to-claim match is not optional.

**All four layers pass**: append the wave's files to `MODIFIED_FILES` and continue.

**Worker reported `[BRIEFING GAP]`**: it could not proceed because something Section 6 should have carried
was missing. Re-assemble the missing block and re-spawn at the SAME tier. Never escalate for this: the
tier is not what failed, and a bigger model reading the same absent block costs about 4.3x for the same nothing.

**Bounded at two.** The re-spawn does not count against the one-retry-per-step budget, so it needs its
own bound or it is an unbounded loop: when the PLAN lacks the block rather than the assembly missing it,
re-assembly produces the same absent block and the worker reports the same gap, at $1 to $6 a spawn. On
the third report for one step, stop re-spawning and take the plan-spec BLOCKER branch in 3c: name it,
then `AskUserQuestion` (`Edit plan to fill the gap and re-verify` / `Accept as Risk and proceed` /
`Stop`). Two failed re-assemblies is the plan telling you it does not carry what the step needs.

**First failure, attributed to one step**: retry once at the next tier up (`quick` to `junior`, `junior` to `senior`; senior does not
escalate), except a malformed report with no `### Changes Made` or `### Verification`, which re-spawns at the
SAME tier with a format reminder because the tier is not what failed. The retry briefing leads with the failure
context, then repeats the original. One retry per step, ever.
Two fast paths skip the same-tier attempt: a worker flagging `tier mismatch` escalates immediately and the
mis-classification goes in the report, and a worker flagging `[CONTRADICTION]` does not retry at all,
because the next attempt hits the same structural conflict; mark it `pending-remediation` for 2f remediation.

**A retried worker is not verified until you verify it.** 2d ran once for the wave and the retry
spawned after it, so nothing has checked the retry's output. Before 2g commits: re-stage and re-diff
scoped to that step's `Files`, re-run Layer A, and re-run the attribution for that step. A commit that
includes an unverified retry is the failure this prevents.

**Retry fails, or senior failed first**: append `{step, wave}` to `STEP_FAILURES` and fire 2j at 3. Do not block the
wave on one failure unless 2i says a later wave depends on it.

### 2f. Remediation and wisdom

Runs after 2e, once every step has a terminal status (verified, failed, or `pending-remediation`). The
mutation check and the full suite both moved into 2d, which is the barrier now; what remains here is
what the orchestrator has to fix or record itself.

1. **Remediate what the orchestrator owns**: `[CONTRADICTION]` reports, cross-file findings deferred from
   Layer B, and plan oversights your review surfaced. Apply the minimal patch to the file that structurally owns the
   missing piece, update `MODIFIED_FILES`, clear any `pending-remediation` step whose `Done when` now passes, and
   record each as a `[REMEDIATION]` wisdom line. Surface first when a patch would change a downstream contract;
   mechanical framework-completeness patches do not need a gate.
2. **Extract wisdom**: up to 5 concrete items this wave, 15 total, codified patterns rather than platitudes.
   `[REMEDIATION]` lines count toward the 5. Persist to `wisdom.md` under `## Wave <N>`.
3. **Re-ground**: emit a 2-3 line wave summary and refresh the marker's `note` with a resume hint, which the
   SessionStart hook reads back. Re-read `PLAN_PATH` and `wisdom.md` only when a compaction has actually happened
   since you last held them; the plan runs to tens of thousands of characters and re-admitting it every wave is a cost with no
   reader. `grep -c '^- \[ \]'` already told you what remains.

### 2g. Wave checkpoint commit

When the wave changed tracked files and `NO_CHECKPOINT_COMMITS` is not set, commit after 2f, before the next
wave. `git commit -m "<one line naming the wave>" -- <wave_files> .ac/plans/<slug>`, not `/ac:commit`: that command injects a
7,000-character body and spends turns on style detection, once per wave, to produce a checkpoint the Phase 4
commit squashes anyway. The final commit at 4a is where `/ac:commit` earns its cost.

Commit the wave's paths explicitly, never `git add -A`. The parent repo may carry unrelated work, and
`-A` would snapshot it as this plan's deliverable, once per wave. Phase 4a runs an F7 check for exactly
that hazard at the final commit; the per-wave commit has to avoid it by construction rather than by a
check that runs later.

The old gate was the plan's `Complexity` field, which no longer exists. "Did this wave change anything" is
answerable from `git status` and never needed a plan-wide label; that label's other two consumers, the
reviewer tier and the oracle default, are gone for the same reason.

A commit failure here is a BLOCKER: print the git error and take the branch in
`${CLAUDE_SKILL_DIR}/references/execution-state.md`. Never auto-retry, because a failed commit usually means the
tree is in a state you did not expect.

### 2h. Progress table

After each wave, render the per-step table using the shape at
`${CLAUDE_SKILL_DIR}/references/wave-orchestration.md` under `## Phase 2h progress table`: step number, title,
wave, tier, result including any escalation, and files changed.

### 2i. Wave dependency check (before launching the next wave)

Before the next wave's workers launch, check whether any failed step is a hard dependency for it. The three sources,
in order: the plan's `### Dependency Notes`, a next-wave step whose `Files` names a file a failed step was to create,
and a next-wave step whose `References` point at a failed step's output.

If one failed, this is a BLOCKER even under auto mode. Emit one line naming it, then `AskUserQuestion` (header
`Dep failed?`, options `Stop and investigate (Recommended)` / `Fix the failed step manually and resume` / `Skip the
dependent steps and continue`). The first two delete the marker before halting; the third leaves it in place because
the run continues. Procedure at `${CLAUDE_SKILL_DIR}/references/wave-orchestration.md`.

If nothing hard failed, the next wave launches automatically. Auto-continue is the default between waves.

### 2j. 3-strike rule

When `STEP_FAILURES` holds 3 entries **spanning two or more distinct waves**, emit one line naming the
BLOCKER and `AskUserQuestion` (header `Halted?`,
options `Accept and continue (Recommended for known-isolated failures)` / `Fix manually and re-verify` / `Stop and
investigate`).

`Accept and continue` logs the failures, leaves the marker in place, and moves to the next wave; the failures surface
in the Phase 4 report. The other two delete the marker first, then pause or halt. This is a BLOCKER even under auto
mode: three accumulated failures is systemic enough that the `(Recommended)` qualifier stops being safe to assume.

The two-wave span is what makes the count mean the same thing it used to. The counter was calibrated when
failures arrived one step at a time; now that a wave's steps are verified together, three failures inside a
single four-step wave is one bad wave rather than a systemic pattern, and halting on it would stop an auto
run early and often. Three failures across two waves is the signal the rule was built for.

### 2k. Loop until all waves complete

Run 2b through 2j for each wave in sequence, auto-continuing between them; only 2i and 2j pause the loop. When the
final implementation wave completes, advance to Phase 3.

## Phase 3: Final code-review

Goal: gate the deliver with one independent code-review pass. It runs on the actual implementation, not the plan; it verifies the work matches the plan and meets quality bars.

**Aim for zero CRITICAL findings.** Phase 2's per-wave 4-layer verification should produce work the Phase 3 reviewer has nothing critical to say about. It reports rather than gates, so a CRITICAL finding here costs a fix and a re-verify, not a loop.

### 3a. Final automated pass

Run build, test, and lint across the whole project. All must pass before the reviewer spawns; fix a failure here and
re-run before spawning.

Skip this pass when the last wave's Layer A already ran the same commands and nothing has been edited since.
That is the ordinary case at the end of a clean run, and re-running a suite that passed minutes ago to build
confidence is exactly what Layer A's own rule forbids. Run it when any remediation, retry or plan-spec fix
landed after that wave's barrier, which is when the tree genuinely differs from what was verified.

Then open this run's section of the review log, once:

```
Bash: mkdir -p .ac/plans/<slug> && { grep -qx '## Run <marker started_at>' .ac/plans/<slug>/review-log.md 2>/dev/null || printf '
## Run %s
' '<marker started_at>' >> .ac/plans/<slug>/review-log.md; }
```

The log is append-only across runs and this header is what scopes THIS run's entry. It is a record, not a counter:
a second `/ac:execute <slug>` writes its own section rather than reading the previous one. The `grep -qx` guard stops
a re-entry from opening a duplicate header.

### 3b. Spawn the reviewer

```
Agent({ subagent_type: "ac:plan-code-review",
        description: "Final code-review for <plan title>",
        prompt: "Plan: <PLAN_PATH>
Modified files: <MODIFIED_FILES, newline-separated>
Wisdom: <wisdom.md path>" })
```

One reviewer, whatever the plan's size. The standard and deep variants were a fiction: measured across
139 review runs the standard one ran twice, so every plan was already getting the deep body.

**Spawn `ac:oracle` alongside it only when the change touches a criticality surface.** Three signals,
any one of which fires it, and `--no-oracle` forces the skip either way:

1. `MODIFIED_FILES` lands on one of the closed six surfaces in `model-tiers.md` rule 5: authentication
   or authorization, payment or billing, cryptographic operations, user-input to SQL or shell or file
   path, file upload or deserialization, destructive migration.
2. Any step's `Why this tier` begins `rule-5-criticality`. The planner already made this judgement with
   the whole interview in context; a `grep` on the plan is a cheaper and better read of it than a path
   list is.
3. The plan carries an `### Oracle Sanity-Check Findings` section, meaning Stage 3.5 already found
   something worth a second opinion at planning time.

Signal 1 alone is weak on its own: a file path rarely announces "cryptographic operations" or
"destructive migration", where signals 2 and 3 are the planner's own conclusions written into the file
you are already holding.

This is the same trigger shape `/ac:plan` Stage 3.5 already uses at planning time, so the pattern is
proven in this pipeline rather than invented here. It also replaces the old routing, which reached the
oracle through the plan's `Complexity` field; that field is gone, and reading the surfaces directly is
what it was standing in for anyway.

```
Agent({ subagent_type: "ac:oracle", description: "Oracle strategic review for <plan title>",
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
verdict and no revision loop, for the same reason the plan reviewer lost its: measured, the code
reviewer blocked 33 times against 12 approvals, and the plan-side loop it mirrored produced five
approvals across 88 passes while 80% of plans left it by hitting the cap. A gate that opens by timeout
is a tax, not a gate.

You are the filter, and you are a better one than the reviewer because you have the plan, the wave
history and the wisdom file:

- **CRITICAL**: fix it before Phase 4, with `Edit` at each cited `file:line`, smallest correct fix, the
  reviewer's `Fix:` line as guidance. Then re-run 3a scoped to what you changed.
- **IMPORTANT**: fix when the fix is small and local; otherwise record it in `report.md` and add it to
  the plan's `## Deferred Ideas`.
- **MINOR, or anything under confidence 50**: `report.md` notes. Do not touch the code for these.
- **An oracle PLAUSIBLE finding** names what would confirm it: run that check before acting on it as CRITICAL or IMPORTANT, and treat an unchecked one as MINOR.
- **An oracle REFUTED premise** means the plan is wrong about the code, whatever the Findings say: route it through the plan-is-wrong BLOCKER below, naming the premise and the quote. An UNSUPPORTED premise goes to `report.md` with the search the oracle named.

Expect volume. Both reviewers are told to report everything they see rather than to pre-filter, because
a reviewer told to be conservative reports less, so a long list is the instruction working rather than
a signal the code is bad.

**A finding that says the PLAN is wrong rather than the code is a BLOCKER even under auto mode.** Name
it, then `AskUserQuestion` (`Edit plan to fix and re-verify` / `Accept as Risk and proceed` / `Stop`).
Never silently rewrite the plan.

Append the outcome to `.ac/plans/<slug>/review-log.md` under `## Run <marker started_at>`: findings by
severity, what was fixed, what was deferred. The log is a record now, not a loop counter.

### 3d. Convergence

CRITICAL findings fixed and re-verified, or none returned. Advance to Phase 4.

## Phase 4: Deliver

Goal: commit the work, generate the dev report, render the execution summary.

### 4a. Final commit

**Delete `.ac/state/active-execution.json` first**, before the F7 check and any commit.

**F7 skip check**: run `git check-ignore -q` on every file in `MODIFIED_FILES`. If all are ignored AND
`git status --porcelain` shows tracked changes NOT in `MODIFIED_FILES`, the parent repo has unrelated work and a
commit would snapshot it as this plan's deliverable. Skip it, say so in one line, and record it in the report under
`## Commits` with the path and the count. The plan's `Git context:` field is a hint; git state is authoritative.

Otherwise invoke `/ac:commit --skip-preflight`, plus `--no-push` when `.ac/state/active-auto.json` exists: an
unattended run has nobody present to approve an outward-facing action, so the final commit stays local and
`/ac:commit`'s branch guard, which only asks before pushing on `main` or `master`, never gets the chance to run.
Without that marker this is the final commit and pushes as before. Phase 2d and Phase 3 already covered the
verification `--skip-preflight` refers to. A clean tree exits silently, which is fine.

### 4b. Report and summary

Write `.ac/plans/<slug>/report.md` from the template at `${CLAUDE_SKILL_DIR}/references/report-template.md`, filling
in the steps executed, modified files, verification outcomes, accumulated wisdom, notes, and commit hashes. Confirm
it landed with `test -f ... && wc -l ...`; retry the write once if it did not, and render the report inline if the
retry also fails, so the work is not lost in chat history.

Then render the closing summary inline from `${CLAUDE_SKILL_DIR}/references/execution-summary-template.md`. The
summary is chat output; `report.md` is the file artifact.

End the turn.
