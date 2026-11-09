---
name: codex-subagents-for-claude-code
description: >-
  Run named GPT tasks through the local codex-subagents-for-claude-code runner with Bash. Use for direct
  or parallel delegation, task-header syntax, continuation, recovery, cancellation
  and worktree jobs from Claude Code or a Claude subagent.
---

# Codex role runner: direct use

Use the runner to send a self-contained task to a GPT model through the installed Codex CLI. It reuses
native Codex authentication and returns the answer with a result footer. Any Codex version may be
selected; 0.166.0 is the tested reference, not a launch restriction. Executable safety, protocol and
retained executable identity checks still apply. Include all needed context: Codex does not receive
this conversation.

Run it with `node '<runner path>'`. Use `--help` for the options and `${CLAUDE_PLUGIN_ROOT}/docs/MANUAL.md` for the full
reference.

In this plugin, `<runner path>` is the `runner:` line that
`node '${CLAUDE_PLUGIN_ROOT}/run-codex-task.mjs' --prepare <role>` prints: this release's immutable copy of the
runner, kept outside the plugin cache, which the command makes when it is missing. Its
`task-file:` line names an unused task file in the temporary folder; run it again for each new
task file.

There is one role per model: `gpt-6-1-sol`, `gpt-6-1-terra`, `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna`,
`gpt-5-6-sol`, `gpt-5-6-terra` and `gpt-5-6-luna`. Every role defaults to `xhigh` unless the task
requests another effort.

## Effort: choose it per task

xhigh remains every role's default. Choose effort for the task and honor an explicit user choice;
higher effort can increase latency and usage. Put an `effort:` line in the task header:

| Effort    | Starting guidance                                                                             |
| --------- | --------------------------------------------------------------------------------------------- |
| `none`    | not offered by the tested models; use `low` for simple tasks                                  |
| `minimal` | not offered by the tested models; use `low` for simple tasks                                  |
| `low`     | simple lookups, one-line mechanical edits, smoke tests or bounded checks                      |
| `medium`  | a focused question, summary or small review                                                   |
| `high`    | a review across files or debugging with a clear failing case                                  |
| `xhigh`   | complex design, system-level diagnosis or an explicit user request                            |
| `max`     | above xhigh, when explicitly requested                                                        |
| `ultra`   | only when explicitly requested and offered by the model; not for luna in the tested catalogue |

Use `low` as the starting point for simple work. Do not choose `none` or `minimal` unless a current
catalogue explicitly offers it for the selected model. Parser acceptance does not mean model support.
These are task-selection suggestions, not latency promises. The exact effort is sent, never
downgraded. An available, complete CLI catalogue can reject an effort with
`CODEX_EFFORT_UNSUPPORTED` before sending a turn when a visible model has an explicit, nonempty
supported-effort list that excludes it. Hidden entries, missing effort metadata or an unavailable
catalogue leave effort validation to the backend, which can still reject the request. A catalogue
listing does not prove account access.

Catalogue refusal happens after the runner job starts, before any Codex thread or turn request.
The driver and a Codex app-server may already be running; no task is sent for model inference.
The failed job has a run record and failure output. Collection writes a durable result file;
with `--detach`, use `--run KEY --wait` or `--collect-finished` to collect it. A detached failure remains
listed until collected; `keep: yes` retains the collected run until `--close KEY`.

The 2026-10-31 catalogue observed with codex-cli 0.166.0 did not offer `ultra` for `gpt-6-luna`
or `gpt-5-6-luna`, or `none` and `minimal` for the listed models. Treat this as a dated observation;
the current catalogue and backend determine availability. The footer reports usage when available:

- `tokens=<input>/<cached>/<output>/<reasoning>` is this turn's share;
- `limit=<used>%/<window>` is account-wide Codex quota usage, not this job's share or a dollar cost.

Missing telemetry is `-`. Native reviews in the tested CLI 0.166.0 can omit token counts and context
usage because its internal review delegate suppresses token-count events. Reported review usage uses
ordinary cumulative-counter accounting; missing usage is never zero or copied from the parent turn.
Do not infer per-job cost from an account-wide limit change.
`--limits` prints the account's Codex quota on one `codex-subagents-for-claude-code-limits:` line
without a thread or a model call (one probe app-server, about 1-2 s); `--limits --cached` prints the
last snapshot and starts nothing. Cached quota has an age/source and does not prove current login.
The model catalogue is reused only for the same CLI build and UTC day, not keyed by account access;
a cached refusal is refreshed before rejection. Runtime snapshots and saved results support
execution stability and replay; they are not provider prompt caches. The footer's cached-token
count is provider-reported accounting, not a promise of cache hits, savings or faster execution.

On Windows, absolute task paths and `--cwd` need a drive-qualified or UNC path.
Do not put Git Bash `/c/...`, single-rooted `/tmp`, or drive-relative `C:tmp` paths in task
directives. The runner refuses these spellings before opening a workspace or input file.

## Which path

- **One job, with a free subagent slot:** use a forwarder such as `subagent_type: codex-subagents:gpt-6-1-sol`. This
  takes two main-thread rounds and uses a Haiku subagent. Runs are kept, so SendMessage to the
  finished agent continues the same Codex thread.
- **Several jobs, no free slot, or a long brief:** call Bash directly in the background (step 2a).
  This uses no subagent and takes three rounds: launch, receive the notice and Read, then act.
- **Inside a Claude subagent:** call Bash directly in the foreground (step 2b). Do not start a
  forwarder from a subagent.

## 1. Write the task file

Create a new file, such as the `task-file:` path that `--prepare` prints. Put optional directives first,
starting on line 1 with one directive per line. Add a blank line, then the task text. The runner
sends the task text verbatim.

| Header                           | Purpose                                                                                                                                                                                   |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `write: yes`                     | Allow edits. Jobs are read-only by default.                                                                                                                                               |
| `worktree: yes`                  | Create a fresh Git worktree. With `write: yes`, use a new `csfcc/<20 hex characters>` branch and commit each turn. Otherwise, use a read-only snapshot of one commit.                     |
| `worktree-ref: REF`              | Start the worktree from a local branch, fetched `origin/...` ref, tag or commit.                                                                                                          |
| `cwd: <abs path>` or `cwd: none` | Select the workspace. `none` uses an empty folder for tasks unrelated to the current repository.                                                                                          |
| `effort: <level>`                | Choose the reasoning effort: `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max` or `ultra`.                                                                                       |
| `model: <ID or role>`            | Override the model; model and effort may change on continuation.                                                                                                                          |
| `summary: <level>`               | Reasoning summaries: `auto`, `concise`, `detailed`, `none`. Inherited on continuation when omitted; initial omission preserves Codex's default.                                           |
| `output-schema: <abs path>`      | Per-turn JSON Schema object, at most 64 KiB. Parseable output gets a durable `.result.json` sidecar; native review cannot use it.                                                         |
| `tier: <ID>`                     | Per-turn `default` or a tier offered for the model, such as `priority`. Faster tiers may consume more quota. Never infer authorization for a faster tier.                                 |
| `compact: yes`                   | Explicit continuation-only summary before the next task. Makes an extra model call; never inherited or automatic.                                                                         |
| `review: <target>`               | Native read-only review: `uncommitted`, `base:REF`, `commit:HEX`, or `custom`. Structured targets require an empty body; only `custom` uses task text. Review is per-turn, not inherited. |
| `keep: yes`                      | Retain the run for another turn. Close it when finished.                                                                                                                                  |
| `request-id: ID`                 | Deduplicate launch retries. After continuation, the original ID can attach to a later turn.                                                                                               |
| `prompt-file: <abs path>`        | Send that file as the task instead. Useful for long briefs; the file is preserved.                                                                                                        |

The runner refuses these rather than ignoring part of the task: a directive after a blank line, a
misspelt directive name (`writ:`, `kept:`), a directive name with capitals (`Effort: low`; names
are lowercase), and a `prompt-file:` with task text beside it. Fix the file and run it again.

The runner normally consumes the command-line input file after launch if it is unchanged. Add
`--keep-prompt` for a reusable or user-owned task file; the unique temporary files above can be
consumed. `prompt-file:` targets are always preserved. Keep exact per-turn `result=` paths when
historical answers matter; request IDs are not immutable historical-turn addresses.

### Inspecting retained threads

To inspect a delivered, sleeping kept run without another model turn, use
`--transcript KEY [--turn N] [--json]`. Turn numbers follow persisted Codex history and can differ
from the footer for native reviews. Output is bounded and redacted; raw reasoning, user messages
and tool payloads are omitted. History is explicit inspection, not a complete audit.

`--fork KEY [--at N] [--request-id ID]` creates a kept context without a model turn.
Continue the returned key for its first task. Worktrees and locks are independent;
scratch forks start empty. Shared-checkout writer forks are refused. Use a request ID
for retry safety; an uncertain fork is never repeated automatically.

`--revert KEY --before-turn N` explicitly removes persisted conversation turns, while
retaining files, commits and local answers. Use transcript numbering, including review
and compaction turns. An uncertain revert blocks continuation; repeat the same command
to check its resulting prefix without resending the mutation.

`--doctor --verbose` adds bounded MCP, hook, defaults and managed-policy diagnostics.
MCP discovery can initialize integrations. `--bundle KEY` explicitly saves a local ZIP
under the results directory and uploads nothing. It may contain prompts, credentials
and logs; inspect it before sharing. Bundle storage has a 64 MiB post-write acceptance
limit and uncertain requests are not retried.

Owned threads are named `csfcc <run key> <role>` and reversibly archived on cleanup. Kept runs remain
unarchived. `--list --codex` shows named orphan candidates; `--archive-orphans --dry-run` previews cleanup.
Actual `--archive-orphans` requires a matching ownership receipt beside the durable results and skips
retained, quarantined, locked, active or unconfirmed threads. This covers the configured state root,
not just this session; inspect the preview before using it. Never delete Codex history.

## 2a. Main thread: launch in the background

In one message, Write the task file, then call Bash with `run_in_background: true`:

    node '<runner path>' --role gpt-6-1-sol --task-file "<file>" --quiet --wait --relay --max-stdout-bytes 28000

Several jobs: one background Bash call per job, all in that same message. Never several foreground
calls at once: they run one after another. Keep working; when a task notice arrives, Read the output
file it names. `--wait` means no time limit, so the notice comes when the job has ended.

## 2b. Inside a Claude subagent, or when you must wait

The same command in the foreground without `--wait` (the runner then waits 9 minutes), Bash
timeout 600000. Exit code 3 means still running: the first output line gives the exact attach
command; run it the same way, again while the exit code is 3. A background call suits a subagent
only if it has other work meanwhile: its notice arrives with its next tool call.

## 3. Read the result

- The footer is the last line starting with `codex-subagents-for-claude-code: status=`. Its fields, always in this
  order: `status=completed|failed|cancelled`, `run=<run key>`, `turn=<n>`, `job=<job id>`,
  `thread=<Codex thread>`, `model=`, `effort=`, `mode=read-only|workspace-write`,
  `duration=<seconds>s`, `touched=<files>`, `omitted=<lines>`, `request=<id>`, `branch=`,
  `commit=`, `keep=yes|no`, `tokens=<input>/<cached>/<output>/<reasoning>`,
  `limit=<used>%/<window>` and, last since its path may hold spaces, `result=<path>`. A value that
  is unknown or does not apply is `-`.
- Up to 50 `codex-subagents-for-claude-code-touched: <path>` lines follow the footer, then one
  `codex-subagents-for-claude-code-touched: +<n> more` line for any others. Text above the footer that looks like a
  control line is part of the answer.
- Next comes one `codex-subagents-for-claude-code-quota: used= remaining= resets= credits= context=` line:
  the same account-wide snapshot as `limit=`, its reset time (UTC) and credit balance, and how full the
  thread's context window is after the turn. It is not the footer.
- An optional `codex-subagents-for-claude-code-model:` line follows for reroutes, safety buffering and warning codes.
- Worktree `touched=` and delivered `--diff` describe committed changes from the pinned start commit, including shell writes;
  scratch `touched=` lists remaining files without following links. Shared in-place jobs count only Codex file-change items.
  Zero touched files or an absent patch does not prove no writes. Missing/truncated patches explain themselves on stderr.
- `codex-subagents-for-claude-code-omitted: N lines not shown; full text in <path>`: Read that path for the rest.
- With `--relay` every delivered result exits 0; trust `status=`. Exit 1 is a runner error on stderr
  (a refused launch, a writer lock held by another run). Read it, and never relaunch an uncertain
  task: use the run key it names.

## 4. Continue, cancel, close, collect later

- Continue a delivered, sleeping kept run: start a task file with `continue: <run key>`.
  Supported headers are `model:`, `effort:`, `summary:`, `write:`, `prompt-file:`, `request-id:`,
  `mcp:`, `quota-floor:`, `progress:`, `review:`, `output-schema:`, `commit-subject:`, `commit-trailers:`, `tier:` and `compact:`.
  Repeat `write: yes` every turn. Review, schema, tier and compaction are per-turn;
  model, effort, summary, MCP, progress and quota policy otherwise inherit. Run with `--task-file FILE`
  (or `--task-file -`) without `--role`. An explicit role selects its model but preserves stored effort;
  `model:`/`--model` takes precedence over it. Forwarders omit the role for follow-ups.
  An unknown shutdown tree still allows collection of a saved answer, with an uncertainty warning;
  state and claims remain and workspace finalization waits for confirmed shutdown.
  Collect it with `--run` before attempting a new continuation.
- `rq:<request id>` is accepted by `--run`, `--continue`, `--cancel`, `--close`, `--sleep`,
  `--steer`, `--transcript`, `--bundle`, `--revert` and `--fork`, and by the `continue:`, `cancel:`
  and `close:` task directives. These operations still require the appropriate run state and other
  arguments. Once the run is gone, `--run rq:<id>` can replay its saved result. After continuation,
  the original request ID can resolve to a later turn; retain exact result paths for historical answers.
  Use the printed full hexadecimal run key for `--inspect`, `--artifact`, `--finalize`, `--integrate`,
  `--discard`, `--verify-artifact` and `--verification`; these commands reject `rq:` aliases.
- Cancel: `--cancel <run key>`. Stopping your Bash call or TaskStop stops only the waiter; the Codex
  job keeps running.
- Close when the conversation with a thread is over: `--close <run key>`, or `--close-idle` for all
  of this session's finished runs (`--dry-run` first if unsure). `--list --mine` shows this
  session's runs.
- "This session" (`CLAUDE_CODE_SESSION_ID`) is the main thread and every subagent it started:
  they share one ID, so `--mine` and the session-wide sweeps also act on sibling subagents' runs.
  Inside a subagent, close your own runs by key with `--close <run key>`, never with a sweep.
- `--close` refuses when it cannot tell whether the job still runs, and when a finished job's result
  was never delivered. In that second case collect the result with `--run <run key>` first.
  `--close KEY --force` attempts identity-bound shutdown first. For an unknown descendant tree it
  can accept uncertainty, print unconfirmed PIDs and save mandatory `results/audit/KEY/forced-close.json`
  evidence before cleanup. Saved results and receipts retain the warning; repeated forced close is
  safe with the same state/results roots. Unconfirmed/reused PIDs are never signalled; known survivors
  and failed evidence writes still block cleanup. This is not proof that every descendant stopped.
- Sweeps, all manual, this session's runs only (subagents' included) unless
  `--all-sessions --older-than AGE`, each with `--dry-run`: `--collect-finished` delivers runs whose
  job ended while nobody waited (it writes the durable copies and prints one line per run, not the
  results); `--sleep-idle` stops the Codex processes of delivered runs that are still awake. Read a
  collected result from the `result=` path on its line. A run whose record is damaged has no
  session to compare, so every sweep reports it as skipped, whichever session started it.
- Launch now, collect later: `--detach` prints one
  `codex-subagents-for-claude-code-launched: run=<key> ... attach=<command>` line and exits 0; collect with
  `--run <run key> --wait --relay` in the background.
- `--doctor --read-only` checks discovery without write probes. Forwarders are optional for direct
  CLI use when none are installed; plugin or partial installations require their definitions.
  Doctor reports the namespace and local or snapshot evidence, not whether Claude has loaded agents.
  `node install.mjs --check` from the source directory separately verifies checkout definitions.
  Doctor checks login through `account/read` without a model call, but does not prove model access.

## Safety

- Read-only unless `write: yes`. On a checkout other sessions use, add `worktree: yes`, then review
  or merge the branch `csfcc/<20 hex characters>`. Without a worktree, one write job per repository runs
  at a time.
- To review one commit while the checkout keeps changing, use `worktree: yes` without `write: yes`.
- Runner-managed Git disables hooks and fsmonitor and refuses external filters. Developer Git hooks
  and user settings remain unchanged. Use trusted repositories, do not switch the worktree's branch,
  and verify the reported commit before merging. Explicit verification commands and model-issued
  shell commands are not protected merely because they invoke Git.
- The runner owns termination: it confirms process identity through OS start time and available
  command/endpoint evidence before stopping a driver or app-server. Unproved identity retains state
  without killing by PID alone. Inspect contradictory state before recovery; closing preserves
  durable results and audits.

## CLI configuration and privacy

Requires Node 22+, Git and a logged-in Codex CLI. Any version may be selected; 0.166.0 is the tested
reference. No allow-version override is needed. Unsafe/unidentifiable executables, missing protocol
support and a changed retained native payload still refuse execution. Start a new run after a
deliberate CLI change; never rewrite stored identity to resume an old one.

The default inherits Codex MCP servers, hooks, notify and OTEL exporters, including any prompt logging.
Add `mcp: off` to disable those integrations/exporters for a turn while preserving login. Write jobs may
add trusted-project entries. Background commands can outlive turn completion until app-server exit.
Sandboxed commands can read the state root, prompts and results included. Invalid records are
retained for inspection and refused for active work. `--close KEY --force` can quarantine ended state
only after process checks. Sweeps skip invalid records; locks and request claims remain respected.

## Batches, artifact finalization and verification

For explicit multi-model requests, `--batch RECIPE.json` starts independent worktree runs from one pinned
commit, at concurrency 1-4 and at most 16 children. The recipe names an absolute cwd and raw promptFile,
a requestId, and explicit model/effort pairs. It consumes the unchanged prompt once and saves a durable
manifest. `--batch-run ID` resumes collection/planned launches; `--batch-cancel ID` cancels only owned
children and preserves partial results. Collection/cancellation require exact child request-digest
ownership, not only a matching request ID or model. Never resend an uncertain child or retry it under
a new ID automatically. Unaffected planned children can progress when no-live-process evidence frees
an uncertain child's slot; possible-live children retain their slots. Missing identity is not proof
of termination. These calls use each selected model's quota; known totals and unknown counts stay distinct.

`--task-file -` and `--prompt-file -` accept bounded UTF-8 stdin before launch; ordinary files remain
supported. A write worktree accepts per-turn `commit-subject:` and `commit-trailers:` (a JSON file).
Specify real co-authors explicitly. These settings do not rewrite model-created commits.

`--artifact KEY` reads a durable Git receipt. `--finalize KEY` seals a delivered sleeping worktree;
a sealed run cannot continue. `--integrate KEY --target CHECKOUT` requires a completed sealed artifact
and a clean fast-forward target. `--discard KEY` retires its branch to a recovery ref after close.
Never infer ownership from a branch name or use these operations without the caller's requested scope.

Verification is a separate explicit action: `--verify-artifact KEY --recipe FILE --attempt ID
--execution-profile trusted-local`. It runs caller-approved executable/argv on a fresh exact-commit
checkout containing the complete sealed commit, without a model call or implicit dependency installation.
Before execution it captures an in-memory baseline. After owned processes settle, it compares actual
file bytes and checkout identity against that baseline, without trusting the post-command Git index,
ignore rules or assume-unchanged/skip-worktree flags. This is trusted local execution, not an OS sandbox.
Settled snapshots with confirmed identity are removed; bounded logs and receipts remain. Uncertain
process/checkout identity or cleanup failure retains the snapshot. The receipt records that outcome.
`--verification KEY --attempt ID` reads it; repeats never rerun a recorded attempt. Exit zero is evidence
about that command and final observed state only, not proof of no temporary edits or test correctness.
Do not start repair retries, install software or run checks on close automatically.
Read the manual's recipe formats and limits before using either batch or verification mode.
