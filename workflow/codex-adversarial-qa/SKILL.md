---
name: codex-adversarial-qa
description: Use when a solution, paper claim, experiment pipeline, prompt, workflow, or UI needs hostile scenario testing before being trusted; build a native Codex adversarial matrix, verify evidence, fix in-scope issues, and report residual risk.
---

# Codex Adversarial QA

Try to break the work before users, reviewers, or future you do.

This is the native Codex adaptation of OMX `$ultraqa` and code-review loops as of upstream `oh-my-codex` main `f947e3a`: keep hostile dynamic scenarios, real evidence, fix-and-rerun discipline, independent review posture, and cleanup reporting; replace OMX lifecycle state and Stop-hook retries with bounded native Codex verification.

## Promise Under Test

Start by stating the promise in one sentence:

- behavior or user flow
- paper/research claim
- experiment metric or resume guarantee
- prompt/workflow safety property
- visual/design acceptance property

If the promise is vague, clarify or turn it into a small set of testable promises before QA.

## Scenario Matrix

Create or mentally maintain a matrix before testing. Each row should have:

- id
- user/attacker/reviewer model
- scenario
- setup
- command, harness, rendered artifact, source search, or manual check
- expected signal
- actual result
- fix applied
- evidence
- cleanup status

Include normal-path coverage plus hostile cases when relevant:

- boundary, malformed, missing, duplicate, or contradictory inputs
- partial output, stale cache, rerun, resume, cancel, or interrupted state
- dirty worktree and unrelated user changes
- slow network, API failure, dependency drift, or offline mode
- hung command, flaky check, misleading success output, or exit-code mismatch
- mobile/narrow layout, clipped text, broken images, font/rendering drift
- prompt injection, instruction conflict, or privilege-boundary attempts
- reviewer objections, terminology mismatch, unsupported claims, and source drift

## Execution

- Inspect enough context to find runnable surfaces, state files, cleanup paths, and existing tests.
- Run highest-risk and cheapest-disconfirming scenarios first.
- Prefer real commands, rendered outputs, repo searches, and source-backed checks over speculation.
- Use bounded timeouts for commands that can hang.
- Generate temporary tests, scripts, or fixtures only when they materially improve confidence and can be cleaned up.
- Classify harness/setup failures separately from product defects; fix the harness before accusing the product.

## Fix And Rerun

When execution is requested, fix in-scope failures and rerun the relevant scenario plus a regression check. When the user asked for review only, do not edit; report findings by severity with file/path/evidence.

Avoid self-approval for high-risk authored work. Use an independent review lane or `$codex-consensus-plan`/`$codex-native-subagent-team` when the result needs another perspective.

## Cleanup

- Remove temporary harnesses, fixtures, logs, spawned processes, and local state unless intentionally kept.
- Record intentionally kept artifacts and why.
- Never exfiltrate secrets, bypass auth, write to production, or run destructive cleanup just to satisfy a scenario.

## Output Shape

- Promise under test
- Scenario matrix summary
- Findings by severity
- Fixes or recommendations
- Verification evidence
- Cleanup status
- Residual risk and future regression guard

## References

Read `references/qa-scenarios.html` for scenario prompts tailored to code, papers, figures, and benchmarks.
