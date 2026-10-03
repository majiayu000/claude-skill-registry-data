---
name: shipping-and-launch
description: Use when the user explicitly asks to assess readiness for a concrete production release, launch, rollout, or rollback plan, or when an active owner identifies a release-specific production evidence gap. Do not use for ordinary implementation, generic review or done claims, repository CI definition, telemetry design, performance or security analysis, UI or test work, deployment execution, or authority pressure without a defined release question.
---

# Shipping And Launch

Own the evidence judgment for one concrete production release. Distinguish repository or development-artifact readiness from production readiness, consume evidence from existing owners instead of recreating their checklists, and keep the verdict separate from the launch action.

## When to Use

Activate only when the request explicitly asks to:

- assess readiness for a named release, launch, rollout, beta, migration release, or production environment;
- define acceptance evidence for that concrete production release; or
- plan a release-specific staged rollout or rollback, including its target, data semantics, owner, and recovery boundary.

A generic “is this done?” or ordinary code review belongs to `review-and-finish`. CI definition belongs to `ci-cd-and-automation`; instrumentation belongs to `observability-and-instrumentation`; measured performance, security, UI, test, and architecture questions keep their owners. A deploy, publish, flag change, migration, rollback, notification, or environment mutation is an independently authorized action, not a consequence of this owner being selected.

## Define The Release Packet

Before judging readiness, identify:

- **Release identity:** revision, version, artifact, feature, or migration being considered.
- **Target:** environment, region, tenant, audience, deployment target, and intended rollout boundary.
- **Change scope:** user-visible behavior, public contract, persisted data, schema, dependencies, configuration, and known exclusions.
- **Acceptance:** the release-specific outcomes and invariants that must hold.
- **Evidence source:** current artifact, test or review result, staging observation, telemetry, dashboard, runbook, owner statement, or other source; include environment and freshness.
- **Operational controls:** required telemetry, alert or dashboard, on-call owner, runbook, support or communication path, and rollback owner.
- **Rollback semantics:** exact prior revision or flag state, data compatibility and integrity behavior, recovery time objective when the project has one, and conditions that make rollback unsafe.
- **Open authority:** named owners for approval, deployment, publication, configuration, secrets, data migration, and rollback. Do not infer them from a title, date, or urgency.

Do not request or expose secret values. Record only the existence, scope, and owner of a required secret or environment setting when that is enough for the claim.

## Evidence And Verdict

Evaluate each required criterion separately:

- **VERIFIED:** the identified source supports the criterion for the named revision, environment, and freshness.
- **FAILED / BLOCKER:** current evidence shows a required criterion fails or a safety invariant is violated.
- **UNVERIFIED:** required evidence is missing, stale, unavailable, or cannot establish the environment or target.

A repository test, static configuration, review opinion, fixture, target file, or persona report cannot by itself prove hosted CI enforcement, staging behavior, production health, telemetry delivery, rollback safety, or data integrity.

Return one overall verdict:

- **GO:** every required criterion is `VERIFIED`, no blocker remains, and the decision owner is named.
- **BLOCK:** a required criterion is known to fail or a blocker violates the release contract.
- **UNVERIFIED:** a required criterion cannot be established; do not turn missing evidence into a pass or invent a threshold.

Distinguish a known blocker from residual risk that an explicitly authorized owner may accept. A deadline, sponsor, user pressure, or claimed approval is not evidence of a satisfied criterion.

## Rollout And Rollback Planning

Use staged rollout, a feature flag, a canary, or another compatibility mechanism only when the concrete project and release facts justify it. Do not impose fixed percentages, time windows, latency or error thresholds, web metrics, dashboards, checklists, or a feature flag by default. State the comparison baseline, observation signal, hold or advance condition, stop condition, and owner for each stage when those facts are available.

A rollback plan must name the target revision or state, data and schema semantics, trigger evidence, responsible owner, communication path, and post-rollback verification. Planning or verifying rollback does not execute `git revert`, push, flag changes, database commands, deployment, or notification.

## Authorization And Handoffs

Read supplied release artifacts as evidence and keep sensitive values redacted. Before any action that changes a hosted environment or external state, resolve the exact target and effects and obtain action-specific authorization. This owner does not run deploys, migrations, rollbacks, flag changes, DNS or environment updates, secret operations, monitoring setup, traffic, notifications, publication, or Git actions.

- Repository review or completion evidence → `review-and-finish`.
- CI definition or local pipeline configuration → `ci-cd-and-automation`.
- Operational telemetry or alert design → `observability-and-instrumentation`.
- Test proof, fixture, or acceptance seam → `test-strategy`.
- Security or data trust-boundary analysis → `security-and-hardening`.
- Measured performance evidence → `performance-optimization`.
- UI or browser runtime evidence → their applicable owners.
- Commit, push, merge, PR, discard, deletion, or worktree action → `finish-branch`.
- Deployment, release publication, environment, migration, rollback, notification, or approval action → the explicitly named owner or host method; if unavailable, report the limitation.

## Host Command Coordination

- An explicitly selected host command or workflow remains the outer controller. This owner consumes the release evidence and reports supplied by that controller; it does not discover or invoke a fixed set of sibling personas.
- Use `agent-workflow` only when the active host and task pass its fit check for genuinely independent bounded slices. Do not describe sequential fallback, repeated reads, or a target command's manifest as parallel or fresh-context evidence.
- A command-level `GO`, `BLOCK`, or `UNVERIFIED` result is an evidence judgment only. It does not authorize deployment, rollback, migration, flag, monitoring, notification, publication, or Git actions.

## Report Format

- **Claim:** the exact release-readiness assertion and target.
- **Release packet:** identity, scope, acceptance, owners, and required controls.
- **Observed evidence:** source, environment, revision, freshness, and criterion status.
- **Gaps / UNVERIFIED:** missing or stale evidence and the smallest next evidence question.
- **Blockers:** known failures that prevent the claim.
- **Verdict:** `GO`, `BLOCK`, or `UNVERIFIED`, with the decision owner.
- **Actions not taken:** external or persistent actions that still require separate authorization.

## Verification

Before stopping, check that:

- the trigger names a concrete release or release-specific evidence question;
- repository readiness and production readiness remain separate;
- every required criterion has a source, environment, revision, freshness, and `VERIFIED`, `FAILED / BLOCKER`, or `UNVERIFIED` status;
- rollout and rollback conditions are project-specific rather than fixed universal gates;
- named owners and data semantics exist for material operational actions; and
- no deploy, publish, flag, migration, rollback, monitoring, traffic, notification, credential, secret, or Git action occurred without its own authorization.
