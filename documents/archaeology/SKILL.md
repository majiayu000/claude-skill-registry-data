---
name: plan-mode-archaeology
description: Find what changed, when, and why. Use when behavior regresses and the cause must be found in the history rather than guessed from the current code.
license: MIT
---

# Archaeology

When behavior regresses, the answer is in the history. Find the change that caused it rather than guessing from the current code.

1. State the symptom precisely: the expected behavior, the observed behavior, and when it was last known to work. A symptom without a last-good time cannot be bisected.
2. Use the history to narrow the window: commits, deploys, dependency bumps, config changes, and data migrations that fall between last-good and now.
3. For the candidates, inspect the actual diff and identify which one touches the code path the symptom exercises. Prefer the change that explains the symptom over the change that is merely nearby.
4. Report the cause with the commit or change that introduced it, the mechanism, and the evidence that links it to the symptom. If no single change explains it, say so and list the remaining candidates.

Archaeology is read-only. Report the cause; do not fix it as part of the investigation.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
