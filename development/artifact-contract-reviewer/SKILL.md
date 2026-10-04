---
name: artifact-contract-reviewer
description: Review or plan changes that affect schemas, payloads, serialized artifacts, persisted records, event contracts, or downstream consumers.
metadata:
  short-description: Protect schema and interface contracts
---

# artifact-contract-reviewer

## Purpose During Development

Use this skill when Codex and similar AI coding agents are changing or reviewing serialized artifacts, API payloads, schemas, persisted records, event contracts, or any interface consumed by other code.

This is a reusable development-time reasoning framework. It is not runtime code and must not be coupled into the product being reviewed.

## When To Apply

- schema or payload changes
- new persisted artifact types
- interface changes between producer and consumer modules
- PRs that rename, remove, reorder, or reinterpret contract fields

## What To Inspect

- producer code
- consumer code
- schema definitions and validation logic
- fixtures, snapshots, or existing artifacts
- migration notes or compatibility assumptions

## Rules To Enforce

- define the contract before implementing around it
- review producers and consumers together
- prefer additive evolution over silent breakage
- make backward-compatibility risk explicit
- keep machine-readable outputs stable and inspectable

## Common Anti-Patterns To Catch

- changing payload fields without updating consumers
- silent schema drift hidden behind permissive parsing
- mixing presentation formatting into persisted artifacts
- widening a contract without validation
- breaking compatibility without a migration plan

## Expected Output From The Agent

- contract summary
- compatibility findings
- downstream risks
- migration or rollout concerns
- suggested tests for producer-consumer alignment

## Output Structure

- Summary
- Key Findings
- Risks
- Affected Files
- Affected Contracts
- Suggested Improvements
- Suggested Tests
- Skills applied

## Example Usage

"Review this schema change for downstream compatibility and migration risk."

"Use this skill to check whether a new artifact type is stable and consumable."
