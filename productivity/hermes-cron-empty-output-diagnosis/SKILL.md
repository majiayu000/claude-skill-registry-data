---
name: hermes-cron-empty-output-diagnosis
description: Diagnose Hermes cron jobs that ran successfully at scheduler level but produced empty, missing, or non-actionable user output.
---

# Hermes Cron Empty Output Diagnosis

## Purpose
Provide a safe, read-only workflow for diagnosing Hermes cron jobs that show an apparently successful run but deliver an empty response, no response, or an output file with no useful content.

## When to use
- A scheduled Hermes job delivered `(empty)`, `No response generated`, or a blank message.
- A user asks why a scheduled inspection, health report, or reminder produced no content.
- Cron metadata says the job ran, but the final user-facing response is missing or useless.
- A cron job is intentionally quiet-on-green, and you need to verify whether silence was expected.

## Safety rules
- Default workflow is read-only.
- Do not update, pause, resume, remove, or manually run cron jobs unless the user explicitly approves.
- Do not reveal tokens, API keys, chat IDs, private delivery targets, raw logs, or private prompt contents.
- Redact job IDs, paths, delivery targets, and project names when preparing public reports.
- Treat silence-on-green jobs separately from broken jobs; do not "fix" intentional silence.

## Read-only workflow
1. Identify the affected job from cron metadata or user-provided context.
2. Inspect job metadata only: enabled state, schedule, last run time, last status, next run time, delivery mode, model/toolset bindings, prompt length, script setting, and no-agent mode.
3. Inspect recent output artifacts for the affected job. Look for whether files exist, whether they contain empty output, errors, tool failures, or intentional silence markers.
4. Compare several recent runs to distinguish a one-off empty response from a recurring prompt/design issue.
5. Check whether the job uses a script, no-agent mode, a long prompt, or heavy skill bindings that may produce no final answer.
6. Determine which bucket fits:
   - scheduler did not trigger;
   - script failed before agent response;
   - agent ran but returned empty;
   - no-agent script stdout was empty by design;
   - prompt allowed silence;
   - output existed but delivery failed.
7. Prepare a diagnosis without changing the job.

## Evidence to collect
- Job name or redacted job identifier.
- Schedule and enabled state.
- Last run timestamp, next run timestamp, and last status.
- Whether output artifacts exist for the latest run and several prior runs.
- Output class: non-empty, empty, error, intentional silence, or delivery-only failure.
- Whether job uses script, no-agent mode, skills, context injection, or restricted toolsets.
- Whether the task prompt explicitly requires non-empty output on failures.

## Stop conditions
- The job contains secrets or private delivery targets that cannot be safely summarized.
- You cannot confidently distinguish intentional silence from failure.
- Diagnosis requires changing a cron definition, running the job, or reading sensitive raw output.
- The job affects production operations and user approval has not been granted.

## Optional user-approved actions
Only after explicit user approval:
- Run the job once for verification.
- Update the prompt to require non-empty failure output.
- Remove unnecessary skill bindings from the job.
- Change no-agent/script behavior so empty stdout means intentional silence only.
- Pause or resume a broken job.

## Final report format
```text
Summary: <one-line finding>
Job: <redacted job name/id>
Current state: <enabled/scheduled/last status>
Latest run: <timestamp and output class>
Pattern: <one-off or recurring>
Likely cause: <scheduler/script/prompt/no-agent/delivery/intentional silence>
Evidence: <bullets, no raw secrets or logs>
Recommended next step: <read-only follow-up or user-approved action>
Needs approval: <yes/no, and why>
```
