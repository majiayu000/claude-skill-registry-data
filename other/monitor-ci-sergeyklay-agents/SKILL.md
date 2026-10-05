---
name: monitor-ci
description: "Drive a long-running GitHub Actions run to a trustworthy conclusion without burning the session on polling. Use when asked to wait for a pipeline, watch a build, babysit a release or deploy run, restart it if it fails, or report whether it went green. Also use when a run must finish before a follow-up step such as a push, a tag, or a dependent job in another repository. Covers confirming the run is the intended one, bounded waiting instead of open-ended blocking, reading the real per-job outcome rather than the summary icon, extracting facts from logs without matching the workflow's own echoed source, and deciding between a re-run of failed jobs and a fresh dispatch. Do NOT use for authoring or debugging workflow YAML, for proving that a green result was capable of failing (that is prove-checks), or for reviewing pull request feedback (that is babysit-pr)."
metadata:
  author: Serghei Iakovlev
  version: "1.0"
  category: ci
---

# Babysit a CI Run

Waiting on a pipeline looks like a one-line job and is not. Three things go wrong, and each one produces a confident but wrong report: the wrong run gets watched, the waiting strategy exhausts the session before the run finishes, or the run's outcome is read off a summary that hides a suppressed failure.

This skill is the mechanics of getting from "it is running" to "here is what actually happened". Whether the green that comes out is *evidence* is a separate question, and it belongs to `prove-checks`.

## Trigger

- A run must reach a conclusion before the next step can start.
- The task says wait for, watch, babysit, or monitor a build, release, deploy or pipeline.
- A failed run must be restarted, possibly more than once.
- Another party is blocked on the answer "did it go green?"

## Procedure

### 1. Confirm the run is the one you were asked about

A run URL or id identifies a run, not an intent. Before waiting on it, read back what it actually is and check it against the request:

```
gh api repos/<owner>/<repo>/actions/runs/<run-id> \
  --jq '{name, event, status, conclusion, head_branch, head_sha, attempt: .run_attempt}'
```

Watch for a run that is a previous attempt, that is on an unexpected branch, or whose event is not what the task described. When the run was dispatched with inputs that matter — a version, an environment, a dry-run flag — those inputs are not in this payload. They appear in the dispatching step's logs, which are unavailable until the run completes (see step 3), so verify them against the artifact the run produces rather than assuming.

### 2. Wait in bounded blocks, not one open-ended call

A blocking watcher is the obvious tool and the one that fails: `gh run watch` does not return until the run ends, so on a long run it outlives whatever timeout wraps it and the wrapper kills it with nothing to show. Budget explicitly instead.

- Wrap any blocking watch in a timeout comfortably shorter than the tool call's own limit, and treat a timeout as "not finished yet" rather than an error: `timeout 580 gh run watch <run-id> --exit-status`.
- Re-issue it, or fall back to polling `--jq .status` on an interval, until `status` reads `completed`.
- Keep a detached poller writing to a log file when the wait may span several turns. It costs nothing and survives the foreground call being cut short.

Poll on an interval of tens of seconds. Faster adds nothing — jobs take minutes — and burns API quota.

### 3. Read the outcome, not the icon

Two separate traps live here, and both report success.

**Suppressed failures.** A job declared with `continue-on-error: true` renders as a green check and cannot fail the run, so a run-level `conclusion: success` is compatible with that job having done nothing. The same applies to steps ending in `|| true` or `set +e`. Read every job's own conclusion:

```
gh api repos/<owner>/<repo>/actions/runs/<run-id>/jobs --paginate \
  --jq '.jobs[] | "\(.conclusion)\t\(.name)"'
```

Then assert the count of non-success jobs is zero rather than eyeballing the list. Whether a green job proves anything is `prove-checks`'s question; this step only ensures you are reading the real status.

**Skipped jobs.** A conclusion of `skipped` is not `success`. A job gated behind an `if:` may silently not run, so a pipeline can go green having never executed the step the task cared about. Check that the jobs you were promised are present, not merely that none failed.

### 4. Extract facts from logs without matching the workflow's own source

`gh run view --log` refuses while a run is in progress — it returns `logs will be available when it is complete` and exits `0`. A grep against that output finds nothing and the empty result reads as "the step did not print it". Wait for completion before concluding anything from a log.

Once logs exist, a further trap: the log contains both the *command echo* — the workflow's script as written, wrapped in ANSI colour sequences — and the *runtime output*. Grepping for a message finds the `echo` statement in the source before it finds what the step printed. Filter the echoed source out:

```
gh run view <run-id> --log | grep -a '<pattern>' | grep -av '36;1m'
```

`grep -a` is a cheap safeguard, since the stream carries control characters and a tool that infers binary input will suppress matches. When a search comes back empty, confirm the scope is live with a pattern that must match before reporting absence.

### 5. Restart deliberately

Before re-running anything, read the failing step's log and classify the failure.

| Failure | Action |
|---|---|
| Infrastructure or network flake, timeout, runner loss | Re-run failed jobs: `gh run rerun <run-id> --failed` |
| Deterministic — compile error, assertion, missing secret | Do not re-run. Re-running a real failure wastes the cycle and hides the cause. Fix, then dispatch fresh. |
| Partial success where later jobs never started | Re-run failed jobs; completed jobs are not repeated |

A re-run creates a new attempt against the **same commit**. When the fix is a code or config change, a re-run will not pick it up — dispatch a new run. Note also that a pipeline guarded by a `concurrency` group may queue rather than start, so a dispatch that appears to do nothing may be waiting on the previous run to release the group.

Cap the restarts. Two attempts at the same deterministic failure is the signal to stop and report, not to try a third time.

### 6. Report what happened

State the run's conclusion, that per-job conclusions were checked, and any job that was skipped or suppressed. When restarts occurred, say how many and why. When something remains unverified because its evidence was not reachable, name it rather than rounding it to green.

## Anti-patterns

- **Treating run-level `success` as job-level success.** `continue-on-error` and `|| true` make the summary a claim, not a measurement.
- **Reading a `skipped` job as a passed job.** The work never happened.
- **One unbounded blocking call.** It gets killed by the wrapper and yields nothing; bounded retries yield partial progress every time.
- **Concluding from an empty log grep during a run.** The log is not merely empty, it is refused — and the refusal exits `0`.
- **Matching the workflow's echoed script instead of its output.** The answer looks present when only the source line matched.
- **Re-running a deterministic failure.** Identical inputs, identical result.
- **Re-running after a code fix.** The attempt replays the old commit.
