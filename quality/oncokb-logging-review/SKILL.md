---
name: oncokb-logging-review
description: Review application logging for correct TRACE/DEBUG/INFO/WARN/ERROR/FATAL usage, mandatory level labels, and complete error-event coverage.
---

## Purpose

Use this skill to review logging quality and consistency so operators can triage issues quickly and trust log severity.

## When to use this skill

- Use when a change adds, removes, or modifies application logging statements.
- Use during PR review when behavior changes can affect error handling, retries, fallbacks, or operational visibility.

## Required checks

1. Level correctness for each log event
   - Validate each statement uses the correct level:
     - `TRACE`: highly detailed execution flow, loop-level internals, verbose diagnostics mainly for deep troubleshooting.
     - `DEBUG`: developer diagnostics useful in non-production or temporary investigation.
     - `INFO`: expected lifecycle/business milestones that help explain normal behavior.
     - `WARN`: recoverable anomalies, degraded behavior, retries, defaults, ignored errors, or suspicious states.
     - `ERROR`: failed operations affecting a request, task, or feature where execution can continue elsewhere.
     - `FATAL`: unrecoverable state requiring process shutdown, restart, or immediate operator intervention.
   - Flag over-severe logs (noise escalation) and under-severe logs (hidden risk).
   - Completion criterion: every changed log has a justified level.

2. Mandatory level labeling
   - Require every log event to include a recognized level label.
   - Do not allow unlabeled raw output for application events where structured logging is expected.
   - Completion criterion: no changed log event is missing a level label.

3. Error and fatal event coverage
   - Ensure every error path and fatal path in changed code is logged at least once.
   - Accept either direct logging at source or guaranteed logging at a centralized boundary (handler/middleware/worker wrapper).
   - Flag swallowed exceptions and return-error branches with no observable log trail.
   - Completion criterion: all changed `ERROR`/`FATAL` situations are observable in logs.

4. Ignored error handling
   - When code intentionally ignores, suppresses, or downgrades an error, require a `WARN` log.
   - The warning should include context and the reason the error is being ignored.
   - Completion criterion: every intentionally ignored error in changed code is logged as `WARN`.

5. INFO coverage suggestions
   - Propose missing `INFO` points for key milestones such as startup/shutdown, external dependency calls, cache refreshes, job begin/end, state transitions, and user-impacting decisions.
   - Avoid suggesting `INFO` for high-frequency low-value events.
   - Completion criterion: provide concrete `INFO` suggestions where observability gaps exist.

## Workflow

1. Enumerate changed execution paths.
   - List changed control-flow branches, error handlers, retry blocks, and integration boundaries.
   - Completion criterion: review scope for logging-impacting paths is explicit.

2. Map events to levels and labels.
   - For each changed log or missing log opportunity, record expected level and whether labeling is explicit.
   - Completion criterion: all changed log-relevant events have pass/fail notes.

3. Verify error observability.
   - Trace changed error/fatal branches end-to-end to confirm at least one reliable log emission.
   - Completion criterion: no changed critical failure path is silent.

4. Report findings and suggestions.
   - Separate blockers from non-blocking improvements.
   - Include path references and the expected level for each finding.
   - Completion criterion: author can apply fixes without extra discovery.

## Output format

- `Blockers`: mislabeled severity, missing labels, silent error/fatal paths, ignored errors not logged as `WARN`.
- `Non-blocking`: quality improvements and noise-reduction suggestions.
- `INFO suggestions`: concrete milestone logs to add with proposed message intent.
- `Checked`: confirmation that all required checks were completed.

## Quality bar

- Never approve unlabeled application logs.
- Never approve changed error/fatal paths that do not produce logs.
- Never approve intentionally ignored errors without `WARN` logging.
- Prefer specific level-change recommendations over generic feedback.
