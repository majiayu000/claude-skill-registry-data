---
name: speedrun
description: Finds the shortest path to done and takes it — no detours, no nice-to-haves; invoke via /speedrun when the only goal is to complete the task as fast as possible with nothing extra.
---

# Speedrun

Any% completion. This mode plots the most direct line from here to done and runs it, skipping every optional side quest. No gold-plating, no scope creep, no "while I'm in here." Just the fastest legitimate route to the finish.

## When to use
- The only goal is to finish the task quickly with nothing extra.
- You explicitly do not want polish, refactors, or bonus features.

## Behavior
1. Define "done" in one sentence before starting, then refuse to do anything outside it.
2. Pick the most direct implementation route, even if a fancier approach is tempting.
3. Skip nice-to-haves entirely: no extra features, no refactors of nearby code, no speculative robustness.
4. Avoid context-gathering you don't strictly need — read only what's required to finish.
5. Batch and parallelize independent steps instead of doing them one at a time.
6. Don't gold-plate the finish — the moment it meets "done," stop.
7. Keep correctness on the target path intact; fast is not the same as broken.

## Output
The completed task by the most direct route, plus a one-line confirmation that it meets the "done" definition and nothing extra was added.
