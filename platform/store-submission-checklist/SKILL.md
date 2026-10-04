---
name: store-submission-checklist
description: Use when preparing a game for Steam, console, mobile, or other storefront submission with platform metadata, compliance, ratings, privacy, package, entitlement, and approval requirements.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic]
  versions: [any]
  platforms: [steam, xbox, playstation, nintendo, ios, android]
metadata:
  studio:
    type: gate
    lifecycle_stage: ship
    risk_level: high
    packs: [production-design-liveops]
    side_effects: external_publish
    artifact: store-submission-checklist.json
    required_evidence: [platform-requirements, candidate-package, metadata-review, human-approval]
    owner: HoaTV Studio
    reviewer: Release Manager
    maturity: beta
    last_reviewed: 2026-08-08
    provenance:
      derived_from: none
      patterns_from: [registry/capabilities.yaml production catalog, release-candidate-preflight]
      copied_text: none
---
# Store Submission Checklist

## Overview
Prepare an evidence-backed storefront submission package while keeping account actions, legal attestations, payments, signing, and final submission human-controlled.

## When to use
Use for platform package readiness, metadata review, age ratings, privacy declarations, entitlements, achievements, commerce, localization, screenshots, and certification checklists.

## When NOT to use
Do not use to log into a store account, accept legal terms, spend money, sign binaries, upload packages, or press submit without explicit human approval for that exact action.

## Required inputs and context discovery
Collect platform and program version, requirement source and date, account owner, candidate package hash, release preflight, metadata, assets, supported languages, ratings, privacy disclosures, commerce behavior, entitlements, test accounts, waivers, and submission window.

## Safety and risk level
High-risk external publication. Checklist work is read-only; credentials remain outside artifacts. Any account mutation, upload, legal attestation, fee, signing, or submission is `BLOCKED` until explicit human approval and a platform-specific dry run exist.

## Workflow
1. Bind the checklist to a platform, current requirement source, account owner, and candidate hash.
   Completion criterion: stale or ambiguous requirements are `BLOCKED`.
2. Review package, metadata, assets, localization, ratings, privacy, commerce, and entitlement requirements.
   Completion criterion: every applicable item has evidence, owner, and status.
3. Validate platform test results, known issues, waivers, and review notes.
   Completion criterion: exceptions name the authorized approver and expiry.
4. Prepare an exact submission dry run without authenticating or uploading.
   Completion criterion: fields, files, hashes, order, and expected confirmations are documented.
5. Request human approval for the exact external action.
   Completion criterion: without approval, final status remains `BLOCKED`; this skill never performs submission.

## Evidence and output contract
Produce `store-submission-checklist.json` with platform snapshot, candidate identity, applicable items, evidence paths, gaps, waivers, dry-run plan, reviewer, approval status, and `BLOCKED` external actions.

## Handoff contract
Record account owner, submission window, candidate hash, required files, unresolved certification risks, reviewer, approval scope, and the human-controlled next action.

## Pitfalls and anti-rationalization
- Store requirements change; record source dates and versions.
- A release-ready build is not automatically store-compliant.
- Never place credentials, recovery codes, or signing secrets in evidence.
- User enthusiasm is not approval to publish.

## Verification checklist
- [ ] Platform requirements are current and sourced.
- [ ] Candidate package hash matches preflight evidence.
- [ ] Metadata, ratings, privacy, and commerce items are covered.
- [ ] Dry-run scope and reviewer are explicit.
- [ ] External submission remains human-controlled.

## References and scripts
Use the current primary platform documentation and `release-candidate-preflight`. No storefront API or credentialed submission runner is bundled.
