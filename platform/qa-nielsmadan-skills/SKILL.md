---
name: qa
description: Exercise a developed feature through its real user or consumer interface, enumerate paths and edge/error/loading states first, and report evidence and coverage. Use for "qa", "QA the last feature", "test this feature end to end", "manual QA", or "check the user flows". Defaults to the last developed feature; accepts a feature, URL, command, app, or other scope. Covers web, native apps, CLIs, agent plugins, libraries, and backends. Use test for suite work and code-review for source review.
argument-hint: "[target or scope] [--fix]"
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# QA

Exercise the product as a user or consumer would. Default to reproducing and
reporting findings. `--fix` or an explicit repair request authorizes fixing confirmed
bugs and retesting. Keep small checks in the current agent; choose the execution
context below for substantial passes.

## Instructions

### 1. Resolve the feature and execution surface

An explicit target wins. Otherwise infer the **last developed feature** from the
current conversation and its acceptance criteria, corroborated by relevant local
changes. Read `AGENTS.md`, startup instructions, feature docs, and existing manual
test procedures. Inspect `git status --short`, staged/unstaged diffs, relevant
untracked files, and recent commits as needed. On a clean tree, follow the latest
coherent feature across commits; the newest commit may only be a fix or formatting.
Do not assume a feature branch, an upstream, or a branch named `main`.

State the selected feature, evidence for that choice, and affected interfaces.
Include adjacent behavior sharing the changed boundary. Avoid turning a default
run into a whole-project audit. If several unrelated features remain equally
plausible, ask one scope question while continuing environment discovery. In a
multi-repo workspace, resolve the target repository first.

Identify the actual build/URL/device/binary and the documented way to run it. Read
only the applicable adapter(s):

| Surface | Adapter |
|---|---|
| Web or Electron | [web](references/web.md): agent-browser |
| iOS, Android, macOS, native UI library | [native](references/native.md): agent-device and the existing sample app |
| CLI/TUI, agent plugin/skill, library | [CLI and plugin](references/cli-plugin.md): executable, real host, or consumer |
| API, service, worker | [backend](references/backend.md): client requests and observable state |

For mixed features, follow the affected path across boundaries. Existing tests
inform coverage; they do not prove the running build works. If there is no changed
consumer behavior and relevant tests already cover the internal change, explain
that runtime exploration adds little and run the appropriate checks instead.

#### Choose the execution context

For a substantial pass requiring many interactions in a large coding conversation,
prefer one fresh QA worker when the harness supports it. Give it this skill and only
the relevant adapters, repository/build/device identifiers, feature requirements and
expected outcomes, relevant changes, fixture state, launch commands, authorization
boundaries (including whether fixes are allowed), and evidence requirements. Link
supporting files instead of copying the coding transcript. Explicitly request a fresh
context through the dispatch tool's inheritance option (`fork_turns="none"` where
available); a subagent that forks the full conversation carries the same history.

The worker owns the remaining workflow, including the scenario matrix, execution,
retests, and cleanup. Reuse it across screens and related cases. Tell it: "Do not
dispatch sub-agents or launch other agent CLIs; do this work yourself." A worker
already assigned QA proceeds directly to step 2. Keep one owner of each device or
shared test environment; the parent must not drive it concurrently.

Return coverage, findings, blockers, cleanup status, and evidence paths to the parent,
keeping raw trees and image history in the worker. The parent closes unresolved
coverage with that worker before reporting completion. For short checks, tasks that
need extensive conversation history, or harnesses without fresh workers, run locally.
If context becomes unwieldy, compact at a phase boundary while preserving the matrix,
expected behavior, current state, and evidence paths; do not reset after every screen.

### 2. Enumerate paths before exercising them

Derive expected behavior from the request, specification, and existing contract;
do not use the current implementation as the sole oracle. Read code to discover
branches and dependencies, then translate them into observable scenarios.

Create a scenario matrix in the conversation, shaped like
[the run template](assets/run.md). Each row needs a stable ID, priority, entry
point/preconditions, actions/input, and expected intermediate and final outcome.
Include the setup needed to reach each state. Show the compact matrix before
execution and proceed without an approval gate.

Consider these dimensions, selecting cases relevant to this feature:

- **Paths:** normal completion, alternate entry/action, cancel/back, revisit,
  reload/relaunch, and the closest affected existing workflow.
- **Data:** empty/first-use, one/many items, boundary values, invalid/missing input,
  long text, Unicode, stale or conflicting data.
- **Async states:** initial loading and action pending → success; pending → error
  → retry/recovery; duplicate action, cancellation, or leaving during work.
- **Failures:** unavailable/slow dependency, offline, denied/expired authorization,
  validation errors, partial completion, and recovery without lost/duplicate work.
- **Presentation/lifecycle:** relevant viewport, keyboard/focus, permissions,
  background/resume, persistence, and multiple-user/session behavior.

Every async operation in scope needs a loading/pending case and an error/recovery
case, or a specific N/A reason. Enumerate meaningful branches and risky combinations,
not the Cartesian product of every input/device. Order core paths and high-impact
risks first. Add newly discovered paths to the matrix as testing proceeds.

### 3. Prepare controlled state and run the matrix

Use the project's local/test environment and disposable data. Reuse documented
fixtures, mocks, launch scripts, and per-checkout resources. Confirm the running
artifact contains the change before interpreting results. Record versions and
relevant local changes; a commit hash alone does not identify a modified build.

Use unique sessions, track processes/settings/fixtures you create, and keep
interactions on one shared target sequential. Use existing test credentials through
the project's normal mechanism. Keep secrets and private data out of reports.
Production mutations or real external sends need existing explicit authorization;
continue independent local cases if one action needs input.

Exercise each row through the real interface. Check both feedback and the final
effect: a success toast, HTTP 202, zero exit code, or loaded plugin manifest may
precede the actual result. Capture screenshots for visual states and inspect them;
use short recordings for timing or gesture defects and transcripts for CLI/API work.

**Make loading and errors happen.** Hold/delay a real request through a documented
test mechanism, supply a controlled failure, then restore it and test recovery.
Observe the pending state before waiting for completion. Check feedback, duplicate
actions, input preservation, and completion after retry/cancel as applicable. Record
the fault mechanism and its scope. A painted spinner or source-code branch is not
runtime evidence. If the required condition cannot be induced, record it as blocked.

Prefer reversible runtime controls to product-source edits. Label stubbed responses
and verify real integration separately. Wait on observable conditions with bounded
timeouts; do not let a hanging case consume the run. Retry suspected defects from
a known state and record attempts. Preserve intermittent observations with their
frequency and uncertainty rather than discarding them.

### 4. Record findings and close coverage

Record each finding when discovered: scenario ID, severity by user impact, exact
reproduction, expected/actual behavior, evidence, and reproducibility. Separate
runtime defects from source-only suspicions. Use no bug quota or invented score.

Mark every scenario **Pass**, **Fail**, **Blocked**, **Not run**, or **N/A**. Pass needs
observed evidence; explain the last three. Label automated-check evidence separately
from exploratory observations. Report zero bugs plainly when that is the result.

With repair authorization, preserve the failure evidence, make the smallest
confirmed fix, run the relevant checks, and repeat the failing path plus affected
neighbors. Add a regression test when it pins the defect through a useful boundary.
Retain the original failure and append retest evidence. Otherwise leave product
code unchanged and report the findings. QA alone does not authorize git mutations.

Restore injected faults and changed settings, remove only owned disposable state,
and stop only processes/sessions started for QA. Confirm cleanup rather than assuming
it happened. Preserve reproducible recipes and useful evidence before deleting temp
fixtures. Never reset the user's checkout or clear unrelated app/device state.

### 5. Report the result

Report in the conversation and write no file. A QA pass over a feature is routine
work, so it gets no `docs/tests/` entry by default, however many scenarios it covered.

Write a record only when asked for one, or when this run produced something a later
run would refer back to: measurements worth comparing against, or a fixture/fault
setup intricate enough that repeating it needs written instructions. A list of
scenarios that passed is not such a result. When the procedure is worth keeping but
the outcome is not, write the procedure alone.

For a run that does warrant one, follow the shared
[manual test record convention](../doc/references/manual-tests.md): reuse or create
`docs/tests/qa-FEATURE/README.md` for the repeatable procedure and
`runs/YYYY-MM-DD-HHMM.md` for this run, with a collision-safe suffix and relative
evidence links. The procedure records setup, fixture/fault creation, expected
outcomes, and cleanup; the dated record captures actual steps, the completed matrix,
and findings. Keep previous run results intact.

End with the tested scope, coverage counts, highest-impact findings, blockers, and
a link to the record if one was written. State whether coverage is complete or
partial; “no bugs found” is qualified by what was actually exercised. Research
provenance for maintainers is in [sources](references/sources.md).

## Examples

- **“qa” after a file-upload feature:** infer upload from the conversation/diff;
  enumerate valid upload, invalid/empty file, pending progress, double submit,
  interruption, server failure/retry, and revisit. Delay the local upload response,
  capture progress, then verify the saved file. Report any blocked fault setup.
- **“qa the new CLI export command”:** use a fixture workspace; test the documented
  invocation, empty and malformed input, stdout/file output, noninteractive mode,
  interruption, and rerun. Record output, exit status, and resulting file contents.
- **“qa the plugin's resume behavior --fix”:** verify the built plugin loads in the
  intended host, activate it, resume, and check the promised behavior and session
  isolation. Reproduce a defect, fix it, then repeat the same host sequence.
- **“qa the background import endpoint”:** create a test import; observe pending,
  completion, and fetched results; inject a dependency failure and retry. Existing
  parser tests help but do not establish the running worker's behavior.

## Troubleshooting

- **Wrong or stale build:** verify executable/package path, dev port, installed app,
  and host cache/version against the checkout. Rebuild using project instructions
  and rerun affected cases; do not blame the feature before identifying the artifact.
- **Cannot reach a loading/error/auth state:** use the documented fixture or fault
  mechanism. If absent, record the specific missing prerequisite and continue other
  rows. Never replace runtime observation with static inspection and call it passed.
- **Automation fails:** refresh stale refs and verify the selected app/surface before
  reporting a product defect. For EPERM or sandbox errors, rule out a sandbox
  denial (a sandbox-diagnosis skill, if you have one) before recording a blocker.
