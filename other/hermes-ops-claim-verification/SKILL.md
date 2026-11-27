---
name: hermes-ops-claim-verification
description: >-
  Check whether a Hermes cron job really ran, a fix actually landed or a CI or review-bot verdict
  applies. When a maintenance check is green after manual reruns, find timestamped scheduler output
  or deployment receipts and recheck the auditor's verdict. Not for report-claim-audit.
metadata:
  revision: "5"
  areas: "software-development,work-management"
  targets: "hermes"
  summary: "verify Hermes scheduled-job, repair or deployment claims: find the recording surface, separate manual from scheduled runs, audit the auditor"
  summary_zh: "验证 Hermes 定时任务、修复或部署的说法：找准记录面、区分手动与调度运行、审查审计者"
  kind: "entry"
---

# Verify an operational claim

Quote the exact authorization clause and name adjacent actions it does not
authorize. Permission to sync is not permission to change configuration,
schedules, persistent memory, or live sessions.

1. State the claim, environment, commit or deployment, and observation window.
   Find the artifact that owns the outcome. Missing evidence in a summary is
   not proof the event did not occur.
2. For scheduled execution, change attribution, restoration, or a claim that a
   failure is unrelated, use the [operational proof appendix](references/operational-proof.md).
   Use [Hermes scheduler evidence](references/hermes-scheduler-evidence-2026-11-21.md)
   to locate receipts for the affected profile.
3. For a landed repair, distinguish an applicable patch, a committed diff, a
   published commit, and the deployment actually serving traffic. Inspect each
   required artifact, then rerun the gate at that revision. If attribution is
   disputed, search the candidate review streams for the exact changed paths
   and cite the matching source.
4. For a batch, map each recommendation to its plan and recheck each claimed
   completion against the current tree. Use the
   [batch audit](references/plan-batch-status-audit.md) for per-plan verdicts.
   For CI and bot claims, pin the workflow run or marker to the exact head;
   [review-bot gates](references/ci-and-review-bot-gates.md) covers readback.
5. Give a read-only external auditor parsed records, exact excerpts, population
   sizes and command exit codes. Keep its input beside its verdict. Verify each
   finding against the owning artifact, including false positives caused by the
   input bundle. A zero over an empty population proves nothing.

Report verified results with timestamps and source locations, then gaps and
one owner decision when needed. Quote computed output, label units and time
points, and distinguish intentionally undeployed changes from regressions.
