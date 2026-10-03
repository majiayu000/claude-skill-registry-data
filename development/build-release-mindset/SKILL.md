---
name: build-release-mindset
description: Use when touching build scripts, release or packaging steps, publish flows, or CI config.
---

## The rule

Build and release code has a different discipline than feature code: it must be reproducible, abortable, and reversible. A build that depends on whatever the last run left behind is unreliable by definition. Before you change a build step, ask what happens if it crashes halfway, and whether you could undo the release after it ships.

## Fires when

Editing a build script, a release or packaging step, a publish flow, or CI config.

## How to apply

- Start from a guaranteed clean state: remove stale artifacts and intermediates, restore any patched config, before you begin.
- Smoke-test the smallest case first and abort fast if it fails; don't run the full matrix on a setup you haven't proven.
- Version artifacts into timestamped outputs instead of overwriting, so rollback is trivial.
- Validate outputs, not just inputs. A silently-empty artifact, or a "0 tests passed" nobody asserted on, is the worst failure mode and the easiest to miss.
- Protect any global state you patch-and-restore with a lock, so a half-finished run doesn't leave the machine broken.
- Know the rollback before you ship.

## Worked example

A release script builds against eight SDK versions over an hour, then you discover the first one was broken from the start — the whole hour is wasted. A canary fixes it: build the smallest target first, and abort the run if it fails, so a broken setup costs two minutes instead of sixty. The same instinct catches a "0 tests passed" that would otherwise ship green because nobody asserted the count was above zero — a loud failure is always better than a silent bad artifact.

## Red flags

| Thought | Reality |
|---|---|
| "The machine's probably clean" | Probably is not a guarantee; start clean. |
| "It built, so it's good" | Built is not the same as validated. Check the output. |
| "I'll just overwrite the last build" | Then you can't roll back when this one's bad. |
| "All eight will be fine" | Smoke-test one before you spend an hour on eight. |
