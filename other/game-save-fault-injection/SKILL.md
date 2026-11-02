---
name: game-save-fault-injection
description: Test save/load durability under interrupted writes, storage errors, partial serialization, version mismatch, and recovery failures.
---

# Game Save Fault Injection

## Goal

Demonstrate how save data behaves at known failure boundaries and ensure recovery never silently overwrites the only recoverable copy.

## Inputs to inspect

Save pipeline, temporary/backup files, serialization stages, write/flush/rename operations, schema versions and recovery logic.

## Workflow

1. Map the save transaction from snapshot capture through serialization, temporary file creation, flush, atomic replacement, index update and acknowledgement.
2. Inject failures before and after each important write/rename/flush boundary, including insufficient space, truncated files, permission changes and corrupted metadata.
3. Restart/load using the resulting filesystem state and verify the loader selects a complete committed version or reports a controlled recovery failure.
4. Test schema upgrades and rollback using preserved original save fixtures; make sure failed migration never replaces the source copy.
5. Record the expected outcome for every injection point and add automated tests that check integrity, recoverability and user-visible diagnostics.

## Validation checklist

- [ ] A save is not reported as successful before its required durability/commit boundary.
- [ ] Recovery does not destructively replace original data before candidate data is validated.
- [ ] Interrupted writes result in a known previous save, a known new save or an explicit recovery error.
- [ ] Failure logs identify the phase and file/save slot without exposing sensitive path or account information unnecessarily.

## Required output

A save transaction diagram, fault-injection matrix, recovery outcomes and automated durability regression tests.

## Boundaries and failure handling

Do not promise crash-proof durability without validating the filesystem/platform semantics on supported targets.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
