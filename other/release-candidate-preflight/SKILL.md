---
name: release-candidate-preflight
description: Use when a release candidate or RC needs a go/no-go readiness decision across required artifacts, test summaries, known issues, approvals, compatibility, monitoring, and rollback.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic]
  versions: [any]
  platforms: [windows, macos, linux, console, mobile, web]
metadata:
  studio:
    type: gate
    lifecycle_stage: ship
    risk_level: read-only
    packs: [production-design-liveops]
    side_effects: none
    artifact: release-preflight.json
    required_evidence: [candidate-build, test-summary, rollback-plan, known-risks]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-08
    provenance:
      derived_from: none
      patterns_from: [registry/capabilities.yaml production catalog, build-and-runtime-verification, studio-handoff]
      copied_text: none
---
# Release Candidate Preflight

## Overview
Gate a release candidate on complete, build-bound evidence while keeping store upload, deployment, and publication outside the read-only decision.

## When to use
Use for milestone candidates, hotfix candidates, platform packages, server releases, content updates, and go/no-go review preparation.

## When NOT to use
Do not use to publish, deploy, submit to a store, sign binaries, or waive missing evidence without the named human authority.

## Required inputs and context discovery
Collect candidate version and hashes, source snapshot, build commands, artifact paths, test suites, defects, performance results, security checks, data migrations, compatibility matrix, release notes, monitoring, rollback plan, owners, and approvals.

## Safety and risk level
Read-only gate. Missing required evidence, mismatched build identity, unresolved release blockers, or unavailable rollback produces FAIL or `BLOCKED`, never assumed PASS.

## Workflow
1. Bind all evidence to the exact candidate build and source snapshot.
   Completion criterion: hashes, versions, and artifact paths agree across records.
2. Validate required build, test, security, performance, migration, and compatibility evidence.
   Completion criterion: every required gate has a command, exit code, artifact, and freshness status.
3. Review open defects, waivers, ownership, and player-impact risks.
   Completion criterion: each accepted risk names an approver, scope, expiry, and mitigation.
4. Verify monitoring, rollback, support, and incident readiness.
   Completion criterion: rollback target, trigger, owner, and validation steps are concrete.
5. Produce a go, no-go, or `BLOCKED` recommendation.
   Completion criterion: the recommendation lists all failed, blocked, and waived gates without performing release actions.

## Evidence and output contract
Produce `release-preflight.json` with candidate identity, gate results, defects, waivers, owners, monitoring, rollback, recommendation, limitations, and missing evidence.

## Handoff contract
Record the exact candidate, decision meeting owner, unresolved blockers, approved waivers, deployment runbook, rollback path, support contacts, and next authorized action.

## Pitfalls and anti-rationalization
- A green test run for another build is irrelevant.
- A waiver is not a PASS and must expire.
- Release notes do not replace rollback evidence.
- This skill recommends; it does not publish or deploy.

## Verification checklist
- [ ] All evidence matches the candidate hash.
- [ ] Required gates have fresh command evidence.
- [ ] Defects and waivers have named owners.
- [ ] Monitoring and rollback are actionable.
- [ ] No external release action was performed.

## References and scripts
Use the bundled [scripts/release_preflight.py](scripts/release_preflight.py) with Python 3.11+ and the `jsonschema` package for normalized evidence completeness checks. The helper loads its bundled strict schema from [schemas/release-preflight.schema.json](schemas/release-preflight.schema.json); use project release runbooks only for authorized execution.
