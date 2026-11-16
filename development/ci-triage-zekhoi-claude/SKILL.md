---
name: ci-triage
description: Diagnose a failing continuous integration run by reading its logs, classifying the failure as a code defect, a flaky test, an environment or configuration problem, or an infrastructure outage, and fixing or reporting it with evidence. Use when the user says CI, a pipeline, a GitHub Actions or GitLab CI job, or a build check is failing or red, or shares a CI log or run link. Do not use for bugs reproduced locally without CI involvement (use agent-kit:debugging), for writing new pipelines (use agent-kit:ci-pipeline), or for reviewing code.
---

# CI triage

## 1. Get the failure

- Find the failing run and job: `gh run list`, `gh run view <id> --log-failed`, `gh pr checks`, or `glab ci status`, `glab ci get`, and `glab ci trace <job-id>` (avoid the interactive `glab ci view`). If no CLI or access is available, ask the user for the log.
- Read the first real error, not the last line: the failing test with its assertion, the compiler or linter message, or the step that exited non-zero. Note the job, runner OS, and versions.

## 2. Classify

- **Code defect:** the failure reproduces locally with the same command and versions, or follows directly from the change under test.
- **Flaky test:** it passes on a rerun of the same commit; look for timing, ordering, shared state, network calls, or timeouts.
- **Environment or configuration:** a different runtime or tool version, missing secret or permission, cache corruption, a changed lockfile, or an OS-specific path or line-ending difference.
- **Infrastructure:** runner or registry outages and rate limits. Check whether other runs failed the same way.
- Compare with the last green run on the same branch or the base branch to find what changed.

## 3. Act

- For a code defect, reproduce locally and fix it at the root cause with a regression test, following agent-kit:debugging's approach.
- For a flaky test, show the evidence (pass and fail runs) and fix the nondeterminism rather than adding retries or longer timeouts, unless the user agrees to a stopgap.
- For environment problems, fix the workflow configuration or pin the version, keeping job permissions minimal.
- Do not rerun jobs, cancel runs, change secrets, or push without the user's instruction. Never weaken or skip a check to make the pipeline green.

## 4. Report

Report the failing job and step, the classification with evidence (log lines, the comparison run), the fix or the recommended action, and how it was verified.

## Examples

- Use: "CI is failing on my PR." "Why is the Windows job red?" "Here is the GitHub Actions log."
- Skip: "This function returns the wrong value locally." (agent-kit:debugging) "Write a GitHub Actions workflow for this repo."
