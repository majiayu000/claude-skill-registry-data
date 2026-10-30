---
name: night-watch
description: Suki's night watch for one long task. The warrior on watch holds her post until dawn and does not wake the camp for anything she can handle. Use for autonomous-run, "run until done", "/loop until X", "keep going while I sleep", or any single task to drive to a checkable exit condition without stopping.
---

# Suki's night watch

The camp sleeps and one warrior keeps the watch. She knows what dawn looks like before the night starts, she checks the perimeter on a schedule, and she handles every small thing herself. She wakes the camp only for what no warrior can decide alone. You own the exit condition. Define done, then drive to it without stopping.

One task driven to a predicate belongs here. A standing program of many PRs and many sessions belongs to `kyoshi-command`. One ambitious run that needs its own bespoke workflow belongs to `day-of-black-sun`.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## Steps

1. **Name dawn.** State the exit condition as a checkable predicate before the first iteration (tests green, the repro fixed, all N PRs merged, a pixel diff of zero).
2. **Pick the wake mechanism** with Claude Code's built-in `loop` skill. An event to watch (CI, a merge, a ref advancing) gets a watcher subagent that wakes you on the event, with a long time-based heartbeat as a fallback. A PR or stack to watch can use `bun ../../tools/watch-pr/watch-pr` (see `long-flight`). No event gets a fixed-interval heartbeat sized to when the result is worth re-checking. Pick each subagent's reasoning effort for the job, as the dispatch rules in `avatar-mode` describe.
3. **Each iteration makes the smallest change the evidence justifies.** Verify it against the predicate, commit if it advanced, and discard changes that did not help. Belt-and-suspenders code that "might help" gets reverted, not left to ride. Follow Sequence Work into Verifiable Units (Fire in `four-elements`), and verify each unit before the next instead of batching checks at the end.
4. **Mid-run discoveries are yours.** Fix broken skills, related bugs, flaky verifiers, review noise, tooling failures, orphaned follow-ups, and fixable drift yourself through `avatar-mode`. Put each out-of-band fix in its own PR. Do not park reversible work for the human, and do not ask fixed-choice questions. Surface only irreversible actions, genuine product or preference calls no experiment can settle, or a real dead end. Keep the predicate as the main drive, and return to it after each side fix.
5. **Log every round of the watch** with `battle-map`. Each iteration writes a row for what changed and whether the predicate moved.
6. **Stop at dawn, and only at dawn.** Stop when the predicate is met. A plateau is not a stop. Keep going and pivot the approach to push past it. Surface a genuine dead end rather than spinning, and never relax the predicate to declare victory.

## Autonomy

The watch keeps going through "don't stop", "going to bed", and "run until done". It still pauses for the irreversible list in `avatar-mode` (force-push to a shared branch, merge to the default branch, deploys, data deletion, messages that leave the project).

## Reply

The exit condition, the iterations run, what landed, what was discarded, and the final predicate state. Write it per `tea-time`.
