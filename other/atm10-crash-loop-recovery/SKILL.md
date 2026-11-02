---
name: atm10-crash-loop-recovery
description: "Stop repeated launch/server crash loops from obscuring the first failure and protect the world and evidence while narrowing the trigger. Use evidence from the actual modified installation and reversible tests."
---

# ATM10 Crash Loop Recovery

## Purpose

Stop repeated launch/server crash loops from obscuring the first failure and protect the world and evidence while narrowing the trigger.

## Required inputs

Exact Minecraft/loader/Java and modpack versions; installed JAR inventory; latest.log and any crash report; relevant configs/datapacks; recent changes; symptom timing; and steps to reproduce. Redact secrets. Make a backup or use a copied instance/save before state-changing tests.

## Workflow

1. Record the environment and reproduce the issue once under controlled conditions; preserve full logs and the original state.
2. Define the failure boundary: stop repeated launch/server crash loops from obscuring the first failure and protect the world and evidence while narrowing the trigger.
3. Locate the earliest causal exception or measurable event and correlate it with the reported symptom. Verify each named mod/resource exists in this installation.
4. Form ranked hypotheses and define a specific signal that would distinguish them; document observations separately from guesses.
5. Perform this focused experiment in a copied instance/save or staging environment: Preserve the first complete log, stop automatic relaunch where safe, and rerun once with controlled startup settings in a copy. Change one variable at a time.
6. Re-run the exact same action and compare the before/after evidence, including one adjacent healthy path where relevant.
7. If the evidence does not isolate the cause, revert the test and identify what additional capture or reduced reproduction is needed.
8. Record actions, exact artifacts/config keys, results, confidence, and rollback steps.

## Validation checklist

- [ ] Installed versions, artifact identities, and relevant file paths are confirmed.
- [ ] The earliest relevant event is supported by a log excerpt, measurement, or reproducible observation.
- [ ] A test plan with observable pass/fail criteria was recorded before the change.
- [ ] Original data is protected and every change can be reversed.
- [ ] Findings separate facts, hypotheses, and unknowns.
- [ ] The original symptom and a nearby normal scenario were retested.

## Required output

A crash-loop timeline, first causal failure, containment state, and minimal recovery sequence. Provide environment details, decisive evidence, ranked hypotheses, test result, confidence, limitations, and rollback instructions.

## Boundaries and failure handling

Do not delete a world or bulk-update/remove mods as an initial response. Do not claim an upstream or official ATM10 state unless verified against the actual profile. Missing or truncated evidence means the result remains provisional.

## Trigger examples

- **Positive:** A modified ATM10 installation shows the specific failure described in this skill and its logs or reproduction are available.
- **Negative:** The user asks for unrelated mod recommendations and has no diagnostic problem.
