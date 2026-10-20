---
name: run-agentic-workflow
description: >-
  Load this skill when repeated work runs from its `flow.yaml`: stages in order, approvals, gates,
  run state on disk, interactive or headless. Trigger on "run the flow.yaml", or when a generated
  `<name>-flow` skill hands over its config.
argument-hint: "config=<path> [mode=interactive|headless] [resume=latest|new] [approve=<stage-id>,...] [<input>=<value> ...]"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Only for flows with a `workflow` stage: Claude Code v2.1.269+ with the Workflow tool on. Interactive:
  turn on Dynamic workflows in /config. Headless: pass --settings '{"enableWorkflows": true,
  "disableWorkflows": false}'. Without the tool that stage runs its declared fallback or fails.
license: Apache-2.0
---

# Run an Agentic Workflow

Run the stages of one `flow.yaml` in order, exactly as written. The runner owns ordering, approvals,
gates, run state and resume; each stage owns its own work. It ends every run with one line,
`FLOW STATUS: done`, `FLOW STATUS: awaiting-approval <stage-id>` or `FLOW STATUS: failed <stage-id>
<reason>`, because a headless caller has nothing else to branch on.

**Native first, the runner only for the delta.** Each stage's work goes to the Claude Code
capability the config names: the Skill tool, the Agent tool, Bash, the Workflow tool. The runner
does not reimplement any of them. It keeps only what Claude Code does not provide across stages:
approvals asked mid-run between stages, world checks before a stage re-runs, run state that
survives the session for resume, and the `FLOW STATUS:` line. Ordering and gates exist to carry
those four. The reason is that native capabilities keep growing: when Claude Code covers one of the
four, that part of the runner goes, so the runner shrinks rather than competes with it.

The config format, the validation rules, the `run-state.md` layout and the status line are in
`${CLAUDE_PLUGIN_ROOT}/references/flow-config-schema.md`. Read it before step 1; this skill does not
restate it.

## Procedure

1. **Load and check the config.** Read `config`, then check it against every rule under Validation
   rules in the schema doc, and the `.js` of each `workflow` stage for carriage returns (a CRLF
   file fails at launch with "control characters that would be hidden in the approval dialog").
   Resolve relative paths against the directory holding `config`. On the first failure end with
   `FLOW STATUS: failed - config invalid: <rule>, <stage>`. Do this before anything runs, because a
   failure at stage 4 of a cheap flow is a smaller loss than one at stage 4 after an irreversible
   stage 3.
2. **Resolve inputs.** Fill each input from the arguments, then its `default`. A missing required
   input is asked for with `AskUserQuestion` in interactive mode and ends the run as
   `FLOW STATUS: failed - missing input <name>` in headless mode.
3. **Preflight capabilities.** For each `workflow` stage, check the Workflow tool is in your tool list
   (search deferred tools for `Workflow` if it is not listed). For each `skill` stage naming a
   plugin skill (`plugin:skill`), check it appears in the available skills. When the capability is
   absent: run the stage's `fallback`, or end with `FLOW STATUS: failed - <stage-id> needs
<capability>` if it is `fail`. Record each fallback chosen in the stage's note. **Never imitate:**
   do not read a workflow's `.js` and do its work by hand to look successful. Files on disk do not
   prove a workflow ran.
4. **Find or create the run.** The run directory is `<run-dir>/<name>/<run-id>/`, where `<run-dir>` is
   `$CEH_WORKFLOW_RUN_DIR`, defaulting to `.agents_workspace/`, and `<run-id>` is the start time
   `YYYYMMDD-HHMM`. Create it unless the flow is not `resumable`, writes no artifact and has no
   `fan_out`, in which case it has no run directory at all.
   - A flow that is not `resumable` always starts a new run and ignores `resume`.
   - Otherwise take the newest run under `<run-dir>/<name>/` whose `run-state.md` has a stage that is
     not `done`. `resume=latest` resumes it, `resume=new` starts a new run, and with neither,
     interactive mode asks and headless mode starts new. With no such run, start new.
   - On resume, take the inputs recorded in `run-state.md`; a re-passed input that differs ends the
     run as `FLOW STATUS: failed - inputs changed on resume`.
   - Check now that the repo's `.gitignore` ignores the run directory, and append it if not. Run
     artifacts are never committed.
5. **Walk the stages** in order, skipping those already `done`. For each stage:
   1. **Check `reads`.** Every input file must exist, else `failed <id> missing-input <artifact>`.
   2. **Approval.** If the stage has `approval` and is not covered by an earlier approval, see
      Approvals below.
   3. **World check.** If `unsafe_to_rerun`, evaluate `world_check` now, on every attempt and every
      resume. It runs before dispatch and ahead of the run state, because state is only a record.
      When it is false the effect may already exist: stop with `failed <id> world-check-failed`. Do
      not skip the stage and do not guess that it finished.
   4. **Dispatch** per `run.kind`, below.
   5. **Gate**, below.
   6. **Record** the stage in `run-state.md` right away, with the gate evidence in its note.
6. **End** with the status line, under Output.

### Launch arguments

The arguments are `key=value` tokens. Quote values that contain spaces.

| Argument  | Meaning                                                                                                                                                                                            |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `config`  | Required. Path to `flow.yaml`. Unset or unreadable: `FLOW STATUS: failed - config unreadable`.                                                                                                     |
| `mode`    | `interactive` (default) or `headless`. Explicit, never guessed: a skill cannot tell which it runs in, and a wrong guess either hangs on a question or skips a confirmation. Any other value fails. |
| `resume`  | `latest` or `new`. Default: ask in interactive mode, `new` in headless.                                                                                                                            |
| `approve` | Comma-separated stage ids approved in advance. Honoured in both modes and recorded with source `approve=<id>`.                                                                                     |
| other     | The flow's own `inputs`. An unknown key fails the run, so a typo is not silently ignored.                                                                                                          |

A resumed session may instead carry the message `APPROVED <stage-id>`. Treat it as approval of that
stage when `run-state.md` shows it `awaiting-approval`, with source `resume-prompt`; otherwise ignore
it.

### Dispatch

Pass `{run}`, every input path and the path of every schema the stage reads or writes, since an
isolated stage sees nothing else. Substitute placeholders in every value first.

- **`skill`** — invoke the Skill tool with the named skill and `args` plus `run=<run path>`. The
  call runs in your own context, so write its artifact to the `writes` file yourself if it does not.
- **`agent`** — dispatch the Agent tool with the stage's `subagent_type`. The prompt carries the
  `instructions` (or the instruction to load the named skill), `{run}`, the `reads` paths with their
  schema paths, the `writes` paths with theirs, and these three rules: it cannot ask the user, it
  must not invoke `run-agentic-workflow`, and a result that only exists in its reply is lost, so it
  writes its artifact to the stated path.
- **`script`** — run `bash <script path> <args>` with Bash through the path as resolved against
  `config`'s directory. A non-zero exit is a red gate.
- **`inline`** — do the `instructions` yourself.
- **`workflow`** — call the Workflow tool by name with `args`, and wait for its result. Never launch
  it with a `/<name>` slash command, which fails headless. Write the result to the stage's one
  `writes` file in the form its schema gives. A launch that is denied or errors is
  `failed <id> workflow-denied`; the fallback is for an absent tool only, because a fallback there
  would hide a missing permission. Drop `null` results.
- **`fan_out`** — read the item list from `items_from` using its schema. More than `max_items` fails
  the stage as `too-many-items`. Derive each item id as `item_id` says. Dispatch one `agent` per item
  with no output file yet, at most `max_parallel` at once, each writing its own `output` file. After
  they return, count the files against the item list, which is the first half of the gate: a worker
  that died leaves no file, not a failing one.

### Approvals

The approval belongs to the runner, never to a stage: `AskUserQuestion` is stripped from every
subagent, so a dispatched stage cannot ask and would run straight through. Never let a stage ask.

If the stage id is in `approve=` or recorded as approved in `run-state.md`, proceed and record the
source. Otherwise:

| Mode        | Behaviour                                                                                                                                                                                                                                                                                                                          |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| interactive | Ask with `AskUserQuestion`, showing what `show` names: the exact data, the whole batch once. If it cannot be answered, end as `failed <id> no-user-to-ask`. Approve proceeds. Decline ends as `failed <id> declined` with the stage `pending`, so a resumed run asks again.                                                        |
| headless    | Follow `approval.headless`: `stop` writes `{run}/approval-<id>.md` with the `show` content, marks the stage `awaiting-approval`, prints that content above the status line and ends as `awaiting-approval <id>`. `preapproved-only` does the same unless the id was in `approve=`. `fail` ends as `failed <id> approval-required`. |

A stage named in another stage's `covers` shares that approval and does not ask again. Record each
approval in `run-state.md` with its source and time. Never proceed on silence.

### Gates

After a stage, evaluate `gate.check` with Read, Grep or Bash, and record one line of evidence in the
stage's note. Do not accept "looks right".

- **Green** — mark the stage `done` and continue.
- **Red, `stop`** — mark the stage `failed` and end as `failed <id> <what the check found>`. Never
  continue degraded and never skip a stage to reach a later one: the order is the only reason a later
  stage's inputs are valid.
- **Red, `retry`** — re-run the stage with `retry.changes` applied and the failure output in front of
  it, at most `retry.max` more times, recording the attempt in the note. Run `world_check` again
  before each attempt. When the bound is spent, stop as above. Never raise the bound. If an attempt
  fails with the same check output as the attempt before it, stop early as
  `failed <id> no-progress`: the change between attempts did nothing, so the remaining attempts
  would spend the budget on the same result.

A green gate counts only if the stage left the check alone. Before dispatching a stage, record
`git hash-object` for the files its `gate.check` names, the script it runs, and the tests it runs.
Hash them again before marking `done`. If any changed, end as `failed <id> gate-edited`, because a
stage that rewrites its own check can turn any result green. Skip this for a stage whose stated job
is to edit those files.

## Rules

- **Run the config as written.** Do not reorder stages, merge them, add a stage, or tune a bound.
  Where the config is wrong, fail and say which rule. The stages and gates are what was approved,
  so a run that edits them is no longer the approved workflow.
- **Never imitate an absent tool and never fall back after a denial.**
- **One level deep.** A stage may not run this skill, and a stage you dispatch is told so.
- **No secrets on disk.** Run artifacts and `run-state.md` hold references to secrets, never values.
- **In headless mode, ask only through the approval path above.**

## Output

### Run state and the status line

When the flow is `resumable`, keep `{run}/run-state.md` in the layout the schema doc gives: stage
states, approvals, and the status line. Update it after every stage change, not at the end, because
context that dies mid-run takes anything unwritten with it. A resumed run skips stages marked `done`
and re-enters the first that is not.

The last line of your reply is the status line, and with `run-state.md` it is the last line of that
file too. Say nothing after it.

## Stop conditions

- The config fails a validation rule, an input is missing or a capability is absent → end before
  any stage runs with `FLOW STATUS: failed - <reason>`.
- A gate is red and stops the run, a retry makes no progress, a stage edited its own gate's check,
  a world check fails, an input file is missing or an approval is declined →
  `FLOW STATUS: failed <stage-id> <reason>`.
- A headless approval is needed and not given → `FLOW STATUS: awaiting-approval <stage-id>`.
