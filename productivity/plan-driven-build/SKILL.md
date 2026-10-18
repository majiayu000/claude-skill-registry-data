---
name: plan-driven-build
description: Use when a task is large enough to benefit from bounded multi-agent planning, critique, implementation, and verification, and a second AI CLI is available via aimux for dispatch.
---

# Plan-Driven Build (plan-driven-build)

You are the **orchestrator**. You sequence the flow, exercise the project's delegated authority,
hold only material impact gates, and dispatch the thinking and building elsewhere. You write no
production code and you never read the codebase or the full diff — you read bounded distillates
produced by agents that did that reading for you.

| Level | Does | Must not |
| --- | --- | --- |
| **Orchestrator** (you) | Sequences, holds gates, writes the run journal, runs the verification commands and the product itself and records the result as evidence | Read code or diffs, write production code |
| **Reasoning** | Drafts and revises the plan (steps 1 and 3), verifies the diff against it (step 5) | Change documented project intent or cross an authority boundary |
| **Implementation** | Builds an approved plan (step 4) | Change Goal/Included/Excluded, requirements, or architectural boundaries; write the plan, the journal, or run state; may resolve local reversible plan gaps |

Reasoning and Implementation must run under **a different aimux profile than you**. That is the
point of the workflow: not context isolation, but moving token spend off the metered interactive
session. A Claude subagent shares your account and does not achieve this. Review does not need a
different profile from Reasoning; a different prompt file is what keeps it from repeating
Reasoning's blind spots.

This file is the procedure. Two companions are read **only when their situation arises**:

| File | Read it when |
| --- | --- |
| `setup.md` | A prerequisite check fails, or a profile, sandbox, or permission needs configuring |
| `reference.md` | A dispatch fails or stops, a build has to be continued or restarted, you adapt a snippet, or a `NOTE`, `MISSING`, or `FALLBACK` line needs interpreting. Its first table maps each situation to one section — read that section, not the file |

## The budget (the hard rule)

Everything below exists to keep **your** context small. Per round you may read:

| Artifact | Ceiling |
| --- | --- |
| `docs/00-ai-context.md` | 1 page, once |
| Context pack | Generated mechanically; do not read unless diagnosing a pack failure |
| The plan | Once, after step 1 |
| Critique report | 40 lines |
| Build log | `tail -45`: the summary the supervisor appends when the build ends |
| Event stream | `dispatch-tail.sh --events FILE --lines 15`, only on failure |
| Evidence file | The `EVIDENCE` summary lines; one entry's tail when a command failed |
| Verification report | One line per Definition of Done condition + 10 lines of deviations |
| Run journal | ~30 lines, on resume |
| `reference.md` | The one section the situation names |

If the plan sets a `Report budget` other than the default, pass it to `--max-lines` instead.
Dispatched agents have their own budgets: a frozen context pack (64 KiB by default) and, for
Implementation, a pinned model and a positive rollout-token ceiling.

You may **not** read: `git diff`, source files, the full build log, the prompt files, or a report
that exceeds its budget — truncate it and say you did. If you find yourself reading the codebase
"to be sure", the workflow has already failed; say so rather than continue. A dispatch's stdout is
a JSONL event stream: never `tail` or `grep` a `*.events.jsonl` or `*.raw.log` file.

**Running is not reading.** The ban covers source and diffs. It does not cover executing the
project: you run the plan's verification commands, and the product itself on real input, and you
look at what comes out. That is the one thing no read-only agent can do for you. Keep the output
out of your context with `evidence.sh`; read its summary line, not the log.

## Choose the path

Not every change needs every step. Decide after step 1, when the plan shows the real size, and
record the path and the reason in the journal.

| Path | When | Steps |
| --- | --- | --- |
| **None** | The user can review the change in five minutes | Do not run this workflow; say so |
| **Short** | Every condition below holds | 0, 1, 3a, 3c, 4, 4b, 5, 6–8 — no critique (2), no revision (3b) |
| **Full** | Everything else, and whenever you are unsure | All steps |

The short path applies only when **all** of these are true of the plan that came back:

- at most 3 steps and at most 5 files created or changed;
- no change to a requirement, an ADR, a data schema or migration, a public interface, a security
  boundary, or a dependency line;
- no change to how outside input is parsed or interpreted;
- every row of its Verification table is a command, and each is green on the baseline (step 3a),
  so a regression shows as a red command rather than as an opinion;
- no open question classified Escalation or Reserved.

Choosing the path is Delegated. The short path drops the cold critique, not the evidence: steps
3a, 4b, and 5 run exactly as on the full path. **Leave it** — run step 2 on the plan as it stands
and continue on the full path — as soon as the build stops with `steps_complete=no`, verification
returns `not done`, or a second build round is needed for any reason. A small change that needs
two rounds was not small.

## Authority and gates

**Authority comes first.** Classify every decision as Delegated, Escalation, or Reserved from
`docs/00-ai-context.md`. Execute Delegated work end-to-end; stop only for Escalation or Reserved
decisions. Scope decomposition derived from documented intent is Delegated, and so are commits and
merges from an orchestrator-created worktree back into the work branch. A push to a shared branch,
a release, or a deployment is gated only when the project's authority contract reserves it.

The plan's `Gate profile` (`semi-automatic` by default, `interactive`, or `unattended`) only
controls how much routine execution is surfaced. When
`docs/plans/.runs/project-driver-mission/active.tsv` reports an active mission, that mandate wins
over any gate-profile pause: Delegated work is never turned into a human checkpoint, an Escalation
returns to the outer project-driver orchestrator rather than to the user, and only a Reserved
action with an issued `HUMAN_GATE` may become a user-facing question.

The five discipline skills (`systematic-debugging`, `verification-before-completion`,
`requesting-code-review`, `receiving-code-review`, `finishing-a-development-branch`) are invoked
where the steps name them. `reference.md` § Gate profiles and discipline hooks has both tables.

## Prerequisites

Check, and if anything is missing: report it and stop.

- `command -v codex`, `command -v aimux`, and `AGENTS.md` in the project root. **This workflow
  needs a second CLI**; `codex` is the only dispatch adapter implemented.
- This skill exists at `.agents/skills/plan-driven-build/` or `.claude/skills/plan-driven-build/`.
  When both exist, the copies must be identical.
- A clean owning branch. In a standalone run a dirty tree is a repository-safety condition: report
  it. Under an active project-driver mission do not ask the user merely because the tree is dirty —
  leave it untouched and build in an orchestrator-created clean worktree; if the work depends on
  uncommitted content that cannot be isolated, return a repository-safety blocker to
  project-driver. Never stash, reset, or overwrite.
- `docs/00-ai-context.md` names an aimux profile pool for each level: one profile or several,
  comma-separated, tried in priority order.

Templates are `plan-template.md` and `journal-template.md` in this skill's directory. Copy them,
never edit them in place; a project has no `templates/` directory.

## Step 0 — Open the run journal

Set the identifiers once and reuse them. `ID` starts with today's date from `date +%F`, never
from memory.

```bash
ID=YYYY-MM-DD-short-name
if [ -f .agents/skills/plan-driven-build/SKILL.md ]; then
  SKILLDIR=.agents/skills/plan-driven-build
elif [ -f .claude/skills/plan-driven-build/SKILL.md ]; then
  SKILLDIR=.claude/skills/plan-driven-build
else
  printf '%s\n' 'plan-driven-build is not installed for Codex or Claude Code' >&2
  exit 2
fi
PLAN="docs/plans/${ID}.md"
JOURNAL="docs/plans/${ID}.run.md"
RUN="docs/plans/.runs/${ID}"
CONTEXT_PACK="$RUN/context.md"
EVIDENCE="$RUN/evidence.md"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
MAX_CONTEXT_PACK_BYTES=65536
MAX_CONTEXT_FILE_BYTES=24576
mkdir -p "$RUN" && cp "$SKILLDIR/journal-template.md" "$JOURNAL"
sh "$SKILLDIR/project-health.sh"
```

`project-health.sh` prints one `NOTE` line per rule the project has drifted from and never blocks.
Copy the `NOTE` lines into the journal and act on the ones that bear on this run before step 1;
`reference.md` § Project health notes says what each one calls for.

Then bind each level to a profile pool. **The profile names are the project's own aimux
profiles** — read them from the runtime contract in `docs/00-ai-context.md`. The skill has no
defaults to fall back on:

```bash
PROFILE_REASONING=<profile pool from docs/00-ai-context.md, e.g. codework1,codework2>
PROFILE_IMPLEMENTATION=<profile pool from docs/00-ai-context.md>
PROFILE_REVIEW=<profile pool from docs/00-ai-context.md, or reuse $PROFILE_REASONING>
MODEL_REASONING=          # from docs/00-ai-context.md; may be empty to use the profile default
MODEL_IMPLEMENTATION=     # REQUIRED: exact model from docs/00-ai-context.md, e.g. gpt-5.6-luna
MAX_ROLLOUT_TOKENS_IMPLEMENTATION= # REQUIRED: positive execution ceiling from docs/00-ai-context.md
REASONING_EFFORT_REASONING=      # optional: none, low, medium, high, or xhigh
REASONING_EFFORT_IMPLEMENTATION= # optional: none, low, medium, high, or xhigh

aimux_config="${AIMUX_CONFIG:-$HOME/.aimux/config.yaml}"
for pool in "$PROFILE_REASONING" "$PROFILE_IMPLEMENTATION" "$PROFILE_REVIEW"; do
  found=0
  for p in $(printf '%s' "$pool" | tr ',' ' '); do
    case "$p" in cli:*) found=1; continue ;; esac
    grep -qE "^  ${p}:[[:space:]]*\$" "$aimux_config" && { printf 'ok       %s\n' "$p"; found=1; }
  done
  [ "$found" -eq 1 ] || printf 'MISSING  %s\n' "$pool"
done
```

A `MISSING` line means the dispatch will fail: fix the pool before the run starts (`reference.md`
§ Profile pools). For Implementation, the profile answers **who pays**; `MODEL_IMPLEMENTATION` and
the rollout budget answer **what may run and how much it may consume**.

Three rules hold for every command below:

- **The variables above must be set in the shell that runs a snippet.** If your harness starts a
  fresh shell per command, keep the assignments in `$RUN/vars.sh` and begin each command with
  `. "$RUN/vars.sh"`.
- **Every dispatch goes through `$SKILLDIR/dispatch.sh`**, which takes its instructions from
  `$SKILLDIR/prompts/`. Do not read the prompt files; you fill their placeholders with `--var`.
  The script sets sandbox and approval policy, closes stdin, runs a watchdog, reports profile
  fallbacks, and prints the report's line count against its budget. Never call `codex` directly,
  and never wrap a dispatch in your own timeout, redirect, or backgrounding.
- **Run the snippets as written.** They work unchanged in `sh`, `bash`, and `zsh`. Before adapting
  one, read `reference.md` § Shell rules.

When a dispatch exits non-zero, its summary line carries a `failure_class`. Do not improvise:
`reference.md` § Failure classes says which are retryable and what each one calls for.

The journal is committed; `docs/plans/.runs/` is local scratch and belongs in `.gitignore`.
**Update the journal after every step, before the next dispatch**, including `total_tokens` from
each dispatch. It is the only place the flow's state exists — your context disappears at a usage
limit or a session boundary.

## Step 1 — Dispatch the plan

Do not read the project's documents or code beyond what you need to state the task. Let Reasoning
read what it needs — that is the context you are not paying for twice.

```bash
set --
[ -n "${MODEL_REASONING:-}" ] && set -- "$@" --model "$MODEL_REASONING"
[ -n "${REASONING_EFFORT_REASONING:-}" ] && set -- "$@" --reasoning-effort "$REASONING_EFFORT_REASONING"

"$SKILLDIR/dispatch.sh" --profile "$PROFILE_REASONING" "$@" --mode read-only \
  --phase planning \
  --prompt-file "$SKILLDIR/prompts/1-plan.txt" \
  --var TASK="<one or two sentences: what should be true when this is done>" \
  --var PLAN_TEMPLATE="$SKILLDIR/plan-template.md" \
  --var PLAN="$PLAN" --var BRANCH="$BRANCH" \
  --var DATE="$(date +%F)" \
  --out "$PLAN" --max-lines 220
```

`TASK` is the only thing you contribute here, so make it carry the intent — the plan is only as
good as this sentence. Build nothing in this step.

- **State the requirement and the milestone in `TASK` when you know them.** `Delivers: None –
  maintenance` is for work with no behavior a user can observe. If the plan comes back `None` for
  work that changes observable behavior, or cannot name a milestone, that is an **Escalation**:
  write the requirement first, or record the deviation as a decision. Use `Track: research` for an
  experiment.
- **Size.** A plan that creates or changes more than about 12 files or needs more than 8 steps
  will not finish in one build dispatch. Split it now.
- **A defect that may recur across a family** of similar units (test classes, endpoints,
  migrations): run or dispatch a diagnostic sweep of the whole family before writing `TASK`, so
  the plan covers every affected instance instead of the first one found.

Immediately compile the plan's document references into the bounded context pack:

```bash
sh "$SKILLDIR/context-pack.sh" --plan "$PLAN" --out "$CONTEXT_PACK" \
  --max-bytes "$MAX_CONTEXT_PACK_BYTES" \
  --max-file-bytes "$MAX_CONTEXT_FILE_BYTES"
```

A pack failure is a planning defect, not permission to raise the ceiling: narrow an oversized
whole-file reference to an exact heading, remove irrelevant context, or split the increment. A
heading reference matches the heading text as written, without backticks, or any unique part of
it; an ID is enough (`#FR-017`). Record the byte count and `git hash-object "$CONTEXT_PACK"` in
the journal. The pack is local run state and never a new source of truth.

Now choose the path (see **Choose the path**) and record it. On the short path, skip to step 3a.

## Step 2 — Dispatch a critique of the plan

*Full path only.* A fresh, stateless invocation reads the plan cold against the code, under a
different prompt file from the one that drafted it. `$PROFILE_REVIEW` may be the same pool as
`$PROFILE_REASONING`; listing the latter second only guards against an unresolved review pool.

```bash
set --
[ -n "${MODEL_REASONING:-}" ] && set -- "$@" --model "$MODEL_REASONING"
[ -n "${REASONING_EFFORT_REASONING:-}" ] && set -- "$@" --reasoning-effort "$REASONING_EFFORT_REASONING"

"$SKILLDIR/dispatch.sh" --profile "${PROFILE_REVIEW},${PROFILE_REASONING}" "$@" --mode read-only \
  --phase review \
  --prompt-file "$SKILLDIR/prompts/2-review.txt" \
  --var PLAN="$PLAN" --var CONTEXT_PACK="$CONTEXT_PACK" \
  --out "$RUN/review.md" --max-lines 40
```

The command prints `budget=within budget (n/40)` or `OVER BUDGET`. If it is over, read the first
40 lines only and note the truncation in the journal.

## Step 3 — Measure the baseline, revise, and classify decisions

### 3a — Measure what the plan claims about today

Every row of the plan's **Verification** table whose Baseline says `measure` is run now, on the
commit the build will start from, before anything is approved:

```bash
sh "$SKILLDIR/evidence.sh" --out "$EVIDENCE" --label baseline-e2e \
  --timeout-seconds 1800 --cmd '<the command from the Verification table>'
```

Add `--env-file .agents/build-env.sh` when the project has one. The script prints one `EVIDENCE`
line with the exit code and keeps the output in `$RUN/evidence/`. Write the result into the plan's
Baseline column (`green`, or `18 of 24 failing — evidence: baseline-e2e`) and make the Definition
of Done relative to it: a plan that demands "exits 0" from a suite that is already red cannot be
met by a correct build, and neither the planner nor the reviewer can see that. A command that
cannot run here cannot run for the verifier either — fix the command or the environment first.

On the short path a red baseline row ends the short path: go to step 2.

### 3b — Revise

*Full path only.* Review objections that turn on the code — a parser rule, an invariant, a data
shape — go back to the planner, who has read the code. You have not, and a rule you write in from
outside is a guess. Marked **SPEC** in the review, they are revised by dispatch:

```bash
set --
[ -n "${MODEL_REASONING:-}" ] && set -- "$@" --model "$MODEL_REASONING"
[ -n "${REASONING_EFFORT_REASONING:-}" ] && set -- "$@" --reasoning-effort "$REASONING_EFFORT_REASONING"

"$SKILLDIR/dispatch.sh" --profile "$PROFILE_REASONING" "$@" --mode read-only \
  --phase planning \
  --prompt-file "$SKILLDIR/prompts/3-revise.txt" \
  --var PLAN="$PLAN" --var REVIEW="$RUN/review.md" \
  --var NOTES="<which objections you accept, which you dismiss and why; measured baselines>" \
  --var PLAN_TEMPLATE="$SKILLDIR/plan-template.md" \
  --out "$RUN/plan.revised.md" --max-lines 220
```

On exit 0, replace the plan with the revision (`cp "$RUN/plan.revised.md" "$PLAN"`). What you may
write into the plan yourself is bounded: header fields, measured baselines, a resolved open
question, wording — and, under **Follow-up rounds**, what you observed as a case: input, what
happened, what should have happened. Never a rule about how the code must behave. Briefly justify
the objections you dismiss; silent dismissal hides that the review happened.

A revision that alters a step's description, the Verification table, or the Definition of Done is
a new plan: run step 2 once more against it. One that only tightens wording or fills a baseline is
not. Stop after two revision rounds; a plan that still draws substantive objections is too large
or rests on an unresolved decision — split it or escalate.

### 3c — Scan and classify

Scan the plan itself once more: placeholders ("TBD", "handle appropriately", a step with no file
path or verification command), tasks that contradict each other or the `Excluded` list,
requirements a reader could take two ways, a step whose Verification line needs a browser or GUI
process instead of an Orchestrator-owned row, and a change that handles outside input with no
**Real input for self-check**. Fix what you can inline.

Classify every open question. Resolve Delegated ones from repository evidence, documented intent,
and the least-consequential reversible assumption; write the assumption into the plan and
continue. Stop only for Escalation or Reserved questions — a plan that materially changes intent
is presented as that single delta. Record the goal, `Included` / `Excluded`, material assumptions,
and what the review changed in the journal, then set `Status: Approved`: it means executable under
the authority contract, not that a human checkpoint occurred.

If revision changed any `Context to read first` reference, rebuild `$CONTEXT_PACK` now with the
same limits. From this point through verification the pack is frozen.

## Step 4 — Dispatch the build

Commit the plan and journal first, and record the commit SHA in the journal — step 5 diffs against
it. The build runs in the background under a supervisor, with network access for dependency
resolution and with the journal and the plan protected against the build agent's own edits.

```bash
test -n "${MODEL_IMPLEMENTATION:-}" || printf '%s\n' 'STOP: MODEL_IMPLEMENTATION is required' >&2
test -n "${MAX_ROLLOUT_TOKENS_IMPLEMENTATION:-}" || printf '%s\n' 'STOP: MAX_ROLLOUT_TOKENS_IMPLEMENTATION is required' >&2

STALL_TIMEOUT_IMPLEMENTATION=${STALL_TIMEOUT_IMPLEMENTATION:-1800}
WALL_TIMEOUT_IMPLEMENTATION=${WALL_TIMEOUT_IMPLEMENTATION:-7200}
HEARTBEAT_IMPLEMENTATION=${HEARTBEAT_IMPLEMENTATION:-30}

set -- --model "$MODEL_IMPLEMENTATION" --max-rollout-tokens "$MAX_ROLLOUT_TOKENS_IMPLEMENTATION"
[ -n "${REASONING_EFFORT_IMPLEMENTATION:-}" ] && set -- "$@" --reasoning-effort "$REASONING_EFFORT_IMPLEMENTATION"
if [ -f .agents/build-env.local.sh ]; then set -- "$@" --env-file .agents/build-env.local.sh
elif [ -f .agents/build-env.sh ]; then set -- "$@" --env-file .agents/build-env.sh
fi
[ -f .agents/preflight.sh ] && set -- "$@" --preflight .agents/preflight.sh

"$SKILLDIR/dispatch.sh" --profile "$PROFILE_IMPLEMENTATION" "$@" --mode workspace-write --background --network \
  --phase implementation \
  --stall-timeout-seconds "$STALL_TIMEOUT_IMPLEMENTATION" \
  --wall-timeout-seconds "$WALL_TIMEOUT_IMPLEMENTATION" \
  --heartbeat-seconds "$HEARTBEAT_IMPLEMENTATION" \
  --protect "$JOURNAL" --protect "$PLAN" \
  --prompt-file "$SKILLDIR/prompts/4-build.txt" \
  --var PLAN="$PLAN" --var CONTEXT_PACK="$CONTEXT_PACK" \
  --log "$RUN/build.log"
```

The command returns immediately and prints the **supervisor PID** and the sentinel, health, and
report paths; record them in the journal. It refuses to start while an earlier supervisor for the
same `--log` is alive — that is a running build, not an obstacle to remove. The build agent writes
its own account to `$RUN/build.report.md` and ends it with `IMPLEMENTATION_STEPS_COMPLETE` once
every step is implemented.

Do not tail a running build. Track the supervisor task if the harness has task notifications, and
on every notification or resumed session ask for state mechanically:

```bash
set +e
HEALTH=$(sh "$SKILLDIR/dispatch-health.sh" --log "$RUN/build.log")
HEALTH_RC=$?
set -e
printf '%s\n' "$HEALTH"
```

| Health result | Action |
| --- | --- |
| exit 0 / `state=finished` | The line carries `exit`, `reason`, `steps_complete`, and `total_tokens`. With `exit=0`, continue to step 4b. Otherwise `tail -45 "$RUN/build.log"` is the readable summary; then see the table below |
| exit 10 / healthy running | Keep waiting; do not read the log |
| exit 20 / stale heartbeat | The supervisor itself is unhealthy — an environment failure, not progress |
| exit 30 / lost or unknown | Lost infrastructure state; never wait indefinitely for a sentinel that may never arrive |

When a build does not end with `exit=0`, read the one matching section of `reference.md`:

| What the health line or log summary says | Section |
| --- | --- |
| `reason=budget` | Budget stop — `steps_complete=yes` means **do not re-dispatch**, go to step 4b |
| `timeout.stalled` or `timeout.wall` | Timed-out build |
| The build report names a plan gap or a needed decision | Plan gap |
| A usage or rate limit stopped the dispatch | Usage limit |
| `environment.*`, `model-routing`, `configuration` | Failure classes |
| No task notifications in this harness | Waiting without notifications |

For any other build or verification failure, apply `systematic-debugging` when installed, using
the bounded failure report and reproduction command. Raising the rollout ceiling is never the
first move. The orchestrator does not take over production coding.

## Step 4b — Run the verification and record the evidence

The verification agent is read-only. It cannot build, start a browser, or run the gate, so a
condition that needs a command result reaches it only through what you record here. Skip this step
and the honest answer to most of the Definition of Done is "uncertain".

Run every row of the plan's **Verification** table, whoever owns it. The build agent's own run of
an Implementation-owned command is its claim; yours is the evidence.

```bash
sh "$SKILLDIR/evidence.sh" --out "$EVIDENCE" --label gate \
  --timeout-seconds 1800 --cmd '<command from the Verification table>'
```

One call per command, with a label the verifier can cite (`gate`, `e2e`, `real-input`). Add
`--env-file` as in step 4. The script returns 0 whatever the command returned: a failing command
is a finding to record, not a reason to stop recording.

**Then run the product on real input** when the plan has a **Real input for self-check** row —
the import, the conversion, the page, the command a user would run:

```bash
sh "$SKILLDIR/evidence.sh" --out "$EVIDENCE" --label real-input \
  --cmd '<the product command on the real file, printing the properties the plan names>'
```

Compare what it prints with the plan's expected properties yourself. This check is yours alone:
the build agent and the verifier both work from fixtures and code.

| Result | Do |
| --- | --- |
| Fails the same way the baseline did | Not this plan's failure. The evidence shows it; continue |
| A new failure, or the real input is wrong | Record it under the plan's **Follow-up rounds** as input / observed / expected, commit, and dispatch step 4 again. Do not write the fix or the rule |
| The command cannot run on this machine | An environment finding. Fix the environment or record the condition as unproven; never report it as passed |

Record each `EVIDENCE` line in the journal.

## Step 5 — Dispatch verification against the plan

Do not read the diff yourself. Apply `verification-before-completion` when it is installed; it
owns the evidence check for each Definition of Done condition.

```bash
set --
[ -n "${MODEL_REASONING:-}" ] && set -- "$@" --model "$MODEL_REASONING"
[ -n "${REASONING_EFFORT_REASONING:-}" ] && set -- "$@" --reasoning-effort "$REASONING_EFFORT_REASONING"

"$SKILLDIR/dispatch.sh" --profile "$PROFILE_REASONING" "$@" --mode read-only \
  --phase verification \
  --prompt-file "$SKILLDIR/prompts/5-verification.txt" \
  --var PLAN="$PLAN" --var CONTEXT_PACK="$CONTEXT_PACK" \
  --var SHA="<baseline SHA from the journal>" \
  --var BUILD_LOG="$RUN/build.log" \
  --var EVIDENCE="$EVIDENCE" \
  --out "$RUN/verification.md"
```

The report answers each Definition of Done condition with `done`, `not done`, `not in evidence`,
or `uncertain`. Only `done` closes a condition:

- **`not in evidence`** — the condition needs a command result nobody recorded. Go back to step
  4b, run it, and dispatch verification again.
- **`uncertain`** — the verifier could not decide from the diff and the evidence. Resolve it with
  a recorded run or a spot-check of one hunk; an increment is not complete with an open
  `uncertain`.
- **`not done`** — a follow-up round: step 4b's table applies.

In a standalone run, report to the user what is done, what is not, and what was built outside
`Included`. Under an active project-driver mission, return that same bounded result to the outer
orchestrator; `INCREMENT_COMPLETE` is an inner-workflow result, and only Mission Mandate state may
declare `MISSION_COMPLETE`. You may spot-check a single hunk for a high-risk change or a report
that looks wrong — a judgment call, not the default.

**Say what was proven, not only what was built.** "Implemented and tests pass" and "run on real
input with this result" are different claims. Use the second only when step 4b recorded it, and
set a story to `Done` at closeout only then; otherwise it is `Built`.

## Step 6 — Commit and integrate internally

Never leave the build as an ambiguous dirty tree. Commit verified Delegated work automatically.
First look at `git status --short`: a file whose name ends in a space and a number
(`dispatch 2.sh`, `SKILL 3.md`) is a sync-conflict copy — remove it rather than commit it. If the
work ran in an orchestrator-created temporary branch or worktree, integrate it into the owning
branch, verify the resulting commit contains the work, and remove the temporary worktree when
safe. Do not merge unrelated concurrent work or overwrite a dirty target branch.

## Step 7 — Impact handoff

Determine the next transition from the project's authority contract. If it is Delegated, perform
it and continue. Under an active project-driver mission, return an Escalation to project-driver as
orchestrator work and a Reserved action as a candidate human gate — **do not ask the user from
this inner workflow**. In a standalone run, present the smallest unresolved material decision.
There is no universal merge gate and no "should I continue?" gate.

If an external code review is requested, use `requesting-code-review` to prepare the package and
`receiving-code-review` to disposition the findings before a fix round. The plan critique in step
2 does not replace it.

## Step 8 — Close out

Answer the plan's **At closeout** section from the run evidence and project documents. Write
durable results immediately: architectural decisions to `docs/03-sad.md`, status and traceability
to the requirements, and durable change records where applicable. Write each into the section
where the subject already lives, replacing what it supersedes; never append a dated section
("Update 2026-…") to the end of a document. Confirm `Current status` in `docs/00-ai-context.md`
still describes the project, and run `sh "$SKILLDIR/project-health.sh"` once more.

Use `finishing-a-development-branch` when it is installed. Then delete the plan and its journal in
their own commit, and remove `$RUN` when that cleanup is Delegated; if plan deletion is Reserved,
leave the artifacts and report that single pending transition. Under an active project-driver
mission, closeout returns control to project-driver; it does not end the mission.

## Resuming an interrupted run

If you are picking up a run you did not start — a new session, or another CLI taking over at a
usage limit — read `docs/plans/*.run.md` and nothing else. It tells you the path, the last
completed step, whether a build is still running, and where the reports are. If it records a
running build, ask `dispatch-health.sh` before anything else. Continue from the next step. Do not
re-dispatch a step the journal records as done, and do not reconstruct context by reading code.

Claude Code discovers this skill under `.claude/skills/` and invokes `/plan-driven-build`; Codex
discovers it under `.agents/skills/` and invokes `$plan-driven-build`. The rationale for the
workflow is in the framework's `ai-usage-guide.md` § 5 and is not needed to run it.
