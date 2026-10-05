---
name: harness-diagnostics
description: Assess whether an existing repo is ready for Codex-heavy development. Use before large harness work, when a user asks for an audit, roadmap, maturity score, or wants to know which Pax Fullstack Harness skills to apply first.
---

# Harness Diagnostics

## Purpose

Score repo harness maturity and produce a prioritized roadmap before changing broad project structure.

## Inspect First

- manifests, README, `AGENTS.md`, docs, scripts, CI, env examples, tests, runtime files, security docs, migration files, release docs, and recent diffs
- existing harness assessment or roadmap docs
- validation command output when safe to run

## Procedure

1. Inventory the repo.
   - Use manifests and files on disk, not assumptions.
   - Run `scripts/assess_harness.py` from this plugin when available.

2. Score maturity.
   - Agent instructions
   - Instruction signal-to-noise
   - Repo-local knowledge
   - Validation commands
   - Testing
   - Architecture boundaries
   - Local runtime
   - Observability
   - CI/CD
   - Security
   - Dependency governance
   - Migrations/schema
   - Release readiness
   - Review protocol
   - Entropy controls
   - Feature state and WIP control
   - Session continuity
   - Initialization readiness
   - Termination evidence
   - Process observability
   - Review-feedback promotion
   - Skill compliance, context budget, and daily-vs-library placement
   - Pre-edit investigation evidence for risky changes
   - Browser click-path QA for UI workflows
   - Research evidence for external API, dependency, security, or integration choices
   - Agent failure-loop risks: weak inspection, tool misuse, wrapper no-ops, hidden repair loops, and premature completion
   - Trajectory risk artifacts: task trace, policy, advisory risk wrapper, and risk report
   - Project-scoped subagents for explicit exploration, review, docs research, browser QA, and trajectory auditing
   - Five subsystem maturity: instructions, tools, environment, state, and feedback
   - Treat files as evidence only when they are usable: docs should not be empty placeholders, scripts should be executable, wrappers should not be unconditional no-ops, and validation should wire the expected commands.

3. Write outputs.
   - `docs/harness-assessment.md`
   - `docs/harness-roadmap.md`

4. Prioritize next skills.
   - Recommend the smallest sequence of harness skills that closes the highest-risk gaps.
   - Separate blockers from nice-to-have polish.
   - Recommend `feature-state-machine`, `session-continuity-harness`, `initialization-readiness-harness`, `termination-gatekeeper`, `sprint-contract-observability`, or `review-feedback-promoter` when control-loop evidence is missing.
   - Recommend `skill-compliance-auditor`, `agent-failure-introspection`, `pre-edit-investigation-gate`, `click-path-and-browser-qa`, or `research-first-change` when ECC-derived reliability gaps are found.
   - Recommend `trajectory-risk-supervisor` or `subagent-review-orchestrator` when traces, risky transitions, or parallel review/research would improve reliability.

## Validation

- Run `scripts/assess_harness.py <repo> --json` when possible.
- Confirm findings cite real files or missing files.
- Confirm a high score is backed by `evidence` and has no serious `warnings`; 100/100 means usable artifacts, not just matching filenames.
- Confirm subsystem scores identify weak instructions, tools, environment, state, or feedback layers.
- Confirm roadmap items map to named skills.

## Completion Criteria

- The repo has a clear maturity score, evidence, and ordered next steps.
- The assessment avoids speculative claims and does not mutate the repo except the requested report files.
