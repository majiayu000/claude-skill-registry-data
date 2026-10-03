---
name: delegate
description: Delegate bounded grunt work to cheap open-weight models via opencode (docs flips, standup drafts, lint fixes, report assembly, pre-review diff critique, well-specified gated implementation). Returns EVIDENCE (diff, transcript, tokens), never a success claim — the caller verifies via build/tests/diff. Use to conserve Claude budget; never for last-line-of-defense judgment (physics parity, ABI reachability, merge decisions, visual inspection).
---

# delegate

Runs a bounded task on a cheap open-weight model through `opencode`, with
evidence capture. Claude stays the orchestrator and judge; the worker is never
trusted to self-report success.

## When to use

| Tier | Use for | Worker agent |
|------|---------|--------------|
| `grunt` | docs status flips, standup drafts, fixing /lint findings, report assembly, summarization | `grunt` |
| `implement` | a well-specified package spec or small fix in an ISOLATED worktree, with build+pytest+lint gates downstream | `worker` |
| `verify` | cheap pre-review critique of a diff before spending Claude review budget | `critic` |

Current tier→model mapping lives in `config/tiers.json` — update it there as
the model landscape shifts; never hardcode model ids elsewhere.

**Never delegate:** architect/spec judgment, cycles-parity review, cpp-abi-guard
reachability, gate-failure root-cause, the merge decision, visual PNG
inspection (workers are text-only), or anything whose mistake ships silently.

## How

```powershell
python .claude/skills/delegate/scripts/delegate.py --tier grunt --dir <workdir> --prompt "<task>"
python .claude/skills/delegate/scripts/delegate.py --tier implement --agent worker --dir <worktree> --prompt-file <specprompt.md>
python .claude/skills/delegate/scripts/delegate.py --tier verify --agent critic --prompt "Review the diff of main...HEAD for defects."
```

- `--agent grunt|worker|critic` selects the restricted opencode agent from
  `.opencode/agents/` (push/gh denied for all; critic is read-only). Always
  pass the matching agent for the tier.
- `--fallback` switches to the tier's fallback model (use after a primary
  failure or bad output).
- Long prompts: write to a file and use `--prompt-file`.
- `--dir <worktree>` is how you delegate into an isolated worktree. The wrapper
  forwards it to opencode's own `--dir` flag, which is **load-bearing**:
  opencode IGNORES the subprocess cwd and otherwise roots its shell/file tools
  at the git *project* worktree — which for any linked worktree resolves (via
  the shared `.git` common dir) to the MAIN checkout. Without `--dir`, every
  edit is silently redirected into main (contamination, not a rejection) while
  the wrapper watches the worktree and reports `files_changed: []` — a false
  "completed". Sibling (`../Astroray-<pkg>`) and in-tree
  (`.claude/worktrees/<pkg>`) worktrees both work once `--dir` points at them.
  Verified end-to-end 2026-08-25. See memory `parallel_agent_worktree_contamination`.

## Prompt composition rules

Worker prompts must be **self-contained**: absolute file paths, exact expected
output, explicit "do not touch anything else". Weak models do not infer intent.
Bound the task: one package, one doc, one findings list — never "and anything
else you notice".

## The evidence contract (non-negotiable)

The wrapper prints a JSON summary: `status` (`completed|timeout|errored|
no_clean_finish`), `files_changed`, `tokens`, `cost`, `transcript`
path, plus two additive fields introduced by pkg232:

- `termination_reason` — `normal|timeout|cancelled|error`, the structured
  initiating event. A cleanup failure cannot erase it: `status: timeout` stays
  `timeout` even if the orphaned worker would later have completed.
- `cleanup` — a cleanup-evidence object `{method, confirmed, error}`.
  `method` is `windows_job_object` on Windows, `direct_child` elsewhere, or
  `not_started` when command resolution failed before launch. For a Windows
  Job, `confirmed: true` means the wrapper verified zero active processes and
  awaited its helper before taking the final snapshot. For `direct_child`, it
  proves only the immediate child exited; descendants may remain. If `confirmed: false`, the wrapper
  reports `error`, skips the final git snapshot and transcript-derived claims,
  and emits `files_changed: null` / `git_head: null` / `tool_calls: null` rather
  than misleading empty evidence. The task file is retained for diagnosis.
  Cancellation uses `status: errored` with `termination_reason: cancelled`.

- `status: completed` means the PROCESS finished — **not that the task
  succeeded**. opencode has documented exit-0-on-error bugs; open models
  over-claim under uncertainty.
- After every delegation, verify with your own eyes/tools: read the diff,
  run the build/tests for code changes, grep the claimed edits. For
  `implement` tier, the full gate stack (build, pytest, /lint, CI, HW verify)
  applies unchanged.
- The full JSONL transcript is kept for diagnosis — read it when the result
  looks wrong before re-dispatching.

## Process-tree containment (platform boundary)

On **Windows**, the wrapper launches the worker inside an unnamed Job Object
with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` and no breakaway flags, so every
ordinary `CreateProcess` descendant of the worker inherits Job membership. On
timeout/cancellation/error — and on ordinary completion — the wrapper
terminates and awaits the full Job tree, confirms `ActiveProcesses == 0`, and
only then takes the final git snapshot and parses the transcript. No owned
process keeps writing files after a return with `cleanup.confirmed: true`.
If confirmation fails, the evidence explicitly remains unavailable. Ordinary
completion now ends leftover background subprocesses; delegated tasks are
bounded, so persistent servers/daemons are not supported.

The configured timeout is a **worker-runtime budget after launch-gate payload
delivery**, not a strict whole-launch deadline. OS process creation and the
synchronous control-pipe handoff precede that budget. A stalled helper startup
or very large single-line prompt can therefore delay the timeout or handled
cancellation checkpoint. The bounded cleanup/exit-evidence contract applies
when teardown runs; it does not prove a bound on pre-delivery startup latency.

On **non-Windows** (Linux/macOS), the wrapper keeps its existing
`subprocess.run(timeout=)` direct-child path: it kills and waits only the
immediate child, with no descendant-tree supervisor. The full-tree containment
guarantee is Windows-only; it does not imply that an escaped/brokered process
is contained on any platform.

## Failure handling

- `timeout`: known Windows hang classes exist (stuck "Loading plugins",
  unnoticed process completion). Re-dispatch once; if it repeats, do the task
  yourself or escalate tier.
- Garbage/wrong output twice from the primary → `--fallback`, then give up and
  do it on Claude. Do not loop a weak model more than twice on the same task.

## Privacy

Free-tier models (`*-free`) may train on submitted data. Only route
`.astroray_plan/` docs and public-content tasks through the free variant;
anything touching `src/`, `include/`, or unpublished algorithm notes uses paid
endpoints only.
