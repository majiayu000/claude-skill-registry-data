---
name: atm10-mod-entity-ai-freeze
description: "Investigate a mod-owned entity that freezes, loops an action, or repeatedly fails its goal logic in a controlled environment. Use isolated evidence and repeatable tests before assigning the defect to a specific mod release."
---

# ATM10 Individual Mod Entity AI Freeze

## Purpose

Investigate a mod-owned entity that freezes, loops an action, or repeatedly fails its goal logic in a controlled environment.

## Required inputs

Verified mod ID/version, exact game/loader/Java versions, sanitized full logs or crash report, reproduction environment, expected and actual outcomes, and recent changes. Protect world/player data with a copied save and test account when state can be altered.

## Workflow

1. Verify the owning mod candidate from stack frames, resource identifiers, event source, or feature-specific logs; a nearby frame alone is not proof.
2. Specify one action sequence and measurable expected/actual result: investigate a mod-owned entity that freezes, loops an action, or repeatedly fails its goal logic in a controlled environment.
3. Capture the baseline and the earliest visible divergence, exception, or persisted-state change.
4. Build a minimal test case and record relevant environment plus any feature prerequisites.
5. Run this targeted experiment: Reproduce with one target entity in a bounded area and compare goal/state/path evidence, tick exceptions and behavior with optional AI interactions removed.
6. Hold all unrelated versions and settings constant, repeat the test, and record both successful and failed attempts.
7. Check obvious external causes such as input binding, client/server authority, data migration, renderer configuration or invalid item state as appropriate.
8. Summarize confirmed observations, hypotheses, tested releases, confidence, safe workaround, and a regression case suitable for future validation.

## Validation checklist

- [ ] Mod identity/version and all test prerequisites are recorded.
- [ ] Logs or before/after state capture the earliest meaningful divergence.
- [ ] The issue reproduces from documented steps or inconsistency is explicitly stated.
- [ ] Client/server and persistent-state boundaries are checked where relevant.
- [ ] Potential environment-level causes are distinguished from the suspected mod defect.
- [ ] Recovery/rollback is defined before any state-changing test.

## Required output

An entity behavior timeline, repeatability evidence, and the smallest failing AI condition. Include reproduction steps, artifacts/log references, tested conditions, confidence and limitations, plus a regression test case.

## Boundaries and failure handling

Do not publish private player data, credentials, or unredacted server details. Do not claim source-code root cause unless that code path was actually inspected; unresolved findings remain hypotheses.

## Trigger examples

- **Positive:** A bug associated with a specific mod feature can be reproduced or instrumented in the modified ATM10 environment.
- **Negative:** The behavior has no relation to an individual mod feature, or the user only wants a general installation checklist.
