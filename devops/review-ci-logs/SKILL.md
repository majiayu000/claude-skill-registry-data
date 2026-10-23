---
name: review-ci-logs
description: Diagnose CI failures and noise without weakening diagnostics.
---

# Review CI logs

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/review-ci-logs/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Use when investigating a CI failure, repeated workflow noise, or misleading diagnostics. Read local
`AGENTS.md`, workflow guidance, and CI documentation before inspecting runs.

1. Confirm the repository. Select representative failed and successful runs inside a bounded window.
   For a supplied run, inspect only that run.
2. Download logs to a temporary directory. Do not stream archives into the working context. Inspect
   failed steps and representative large entries, then remove the temporary artifacts.
3. Classify each finding as a real error, misleading output, a downstream cascade, a necessary
   diagnostic, or a volume-only concern. Identify the first repository-owned root cause.
   Compare the first failing run/job, its exact head revision, and scope with the pre-push verification record.
   Establish whether the relevant local verification was omitted, passed under a different scope
   or environment, genuinely CI-only, or unknown. A shared command name does not prove shared
   project, target, fixtures, or configuration. Do not infer an omission from missing evidence or
   label an external infrastructure failure a harness miss.
4. For a persistent-workspace failure, name the producer of sparse state or unsafe ownership before
   proposing cleanup. Reject an unconditional pre-checkout workspace traversal. A compliant repair
   is the one in [github-actions-checklist](../github-actions-checklist/SKILL.md).
5. Prefer one bounded fix that preserves non-zero exits, primary errors, artifacts, summaries, and
   diagnostic evidence. Do not hide stderr, globally quiet output, or add a retry that masks the
   cause.
6. Add focused regression evidence, run local workflow validation, and compare before and after
   output where that comparison is meaningful. Report deferred findings. Do not create issues unless
   authorized.
7. Update [the PR description](../pr-description/SKILL.md) before handoff with confirmed omitted
   verification or proven local/CI mismatch. Link the first failed run/job and its exact revision, the actual local
   scope, the reason it missed the failure, and the durable harness correction or authorized
   follow-up. Keep the distinction between omitted and locally passed checks explicit, and retain
   confirmed gap records after CI turns green. Classify CI-only and unknown coverage separately.

Consumer wrapper owns: workflow names, log retention, the CI provider command, retry policy, and
scheduled automation.
