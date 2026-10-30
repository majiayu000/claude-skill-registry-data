---
name: healing-water
description: Katara's healing for bugs. Use for a reported defect, a failing test, a crash, a regression, "this is broken", or "bug fix". Reproduces it on the reported surface, binary-searches the cause with runtime evidence, ships the smallest fix the evidence justifies, and proves it on the same surface.
---

# Katara's healing water

A healer does not treat the symptom she can see. She finds where the energy is blocked and works there, with the least force that heals. Every line of a fix traces to evidence.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## You own this task

Plan, review, and verify. When you are the top-level session, dispatch the investigation and the fix to characters and stay in the lead. When you are Katara running as a subagent, do those parts yourself, one after another. Pick each dispatch's reasoning effort for the job (the Agent tool's `effort` parameter on Claude Code).

Be scientific. Every shipped line traces to runtime evidence. Belt-and-suspenders code that "might help" is a hypothesis, not a fix, and it does not ship. When evidence refutes a hypothesis, revert what it motivated. The smallest change the evidence justifies ships, nothing more.

## Steps

1. **Reproduce it yourself on the matching surface.** Drive the surface where the bug was reported with the project's driver skill. That is the repo's own `verify` skill when it has one (generate it with `vital-signs`), and otherwise Claude Code's `run` skill for CLIs, TUIs, servers, and browser or Electron apps. Do this even when a debug or instrumentation protocol says to ask the user to reproduce. Capture the exact failing output. Ask the user only with a stated, specific reason the driver cannot reach the target, and only after driving it as far as it goes. If it will not reproduce directly, synthesize the trigger, tighten the conditions, or instrument until it fires.
2. **Binary-search the cause.** Form the candidate hypotheses, then rule them out until one survives. Seed them with `seismic-sense` over the affected subsystem and with `past-lives` for the regression history (`git log`, `git bisect`). Each pass, take the split that cuts the most remaining problem space, get runtime evidence (logs, a debugger, a bisect, a minimal input), and eliminate. When program state is unclear, add instrumentation or logging and read it as the code runs. Do not guess. Drive a long or stubborn hunt with Claude Code's `loop` skill.
3. **Name the mechanism.** Write one sentence: "X happens because Y, introduced by Z." Confirm the surviving mechanism with runtime evidence before planning the fix. A plausible story is a hypothesis, not a cause.
4. **Plan the fix at the root.** Change the first place the system went wrong. A guard downstream is a fix only when the state it handles is legitimate (Fix Root Causes, Water in `four-elements`). If the fix crosses a function boundary, run `war-room` first. When the design is contested, run `lie-detector` before shipping. Dispatch the implementation to `team-avatar:katara` with Katara's model from the avatar-setup sheet and a specific scope, or implement it yourself when you are already the subagent.
5. **Verify on the same surface.** The original repro now passes, and the nearby tests still pass. "Inconclusive" or a different surface is not a pass. Flag it. Unit tests show branch behavior, not bug absence.
6. **Order the history.** Stage the commits so the failing repro lands before the fix. Use `push-and-pull` for the failing-test-first cadence when the bug has a cheap local test path. Skip the new test when it would be expensive, integration-heavy, or unclear, and say so. This is Sequence Work into Verifiable Units (Fire in `four-elements`). The failing test comes first, the fix on top.
7. **Hand to `yip-yip`** to open the PR.

## Rules

- When evidence refutes a hypothesis, revert the changes it motivated.
- No belt-and-suspenders code that "might help". It is a hypothesis, and it does not ship.
- No suppressed errors, no deleted tests, no `as any` to make red turn green.
- Two failed fixes on one premise means stop and test the premise (Attack the Premise, Air in `four-elements`).
- Before review, run `purify` and `clear-water` over the diff.

## Reply

What was broken, the root cause, the fix, and how you verified it. Quote the decisive failing and passing output, trimmed to the assertion and the counts.
