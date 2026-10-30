---
name: steady-flight
description: Appa's steady flight for executing a plan and for behavior-preserving refactors. Use when a plan, spec, or list of units already exists and needs faithful step-by-step implementation, or for a refactor (rename, extract, inline, dedupe, move) that must change structure and keep behavior. Pins the behavior first, executes each unit with its check, and stops rather than improvising when the plan stops matching reality.
---

# Appa's steady flight

Appa carries the whole team across the world, one steady wingbeat at a time. He does not take detours, and he does not drop anyone. Execute the plan the same way.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## Steps

1. **Load the plan.** Read the full plan from `master-plan`, the spec, or the user's list. Copy each unit into the todolist with its check.
2. **Confirm the ground.** Run the existing tests and the build once before changing anything. Record what already fails so you do not take blame for it, or credit for fixing it.
3. **For each unit, in order:**
   1. Read every file the unit touches before you edit.
   2. Make the change, matching the patterns already in the code.
   3. Run the unit's check. Then run the nearby tests and the linter or type checker.
   4. Mark the unit done only when its check passes on the real artifact.
   5. Commit when the work spans several units, one commit per unit, so each is reviewable.
4. **Parallelize only what is disjoint.** Units that touch different files and do not depend on each other can be dispatched at once (see `avatar-mode`). Units that share a file run one after another.
5. **Finish clean.** Remove debug output and scratch files. Run the full check suite one more time. Hand to `yip-yip`.

## When the plan stops matching reality

Stop. Do not fill the gap with a guess. Write what you expected, what you found, and the smallest plan change that would fix it. Send that back to the planner (`master-plan`), or to the user if they wrote the plan. Then continue with the revised unit.

## Refactor

You own the contract. The structure changes. The behavior does not. A feature adds behavior and a bug fix corrects it. A refactor does neither.

If the cleanup reveals a missing feature or a real bug, split it out. Ship the structural change first against the pinned contract. A redesign is allowed, but name it and route it to `avatar-mode` as new behavior. Large or cross-cutting structural work belongs to `day-of-black-sun`. This section covers the focused-to-medium change.

1. **Pin the behavior contract first.** Run `seismic-sense` over the affected subsystem to learn the contract. Then write a characterization test, a snapshot, or an equivalence harness that captures current behavior before any structure moves. If the area has no coverage, write the pin before you touch structure. A type check and a lint are not a pin.
2. **Name the structure the code is missing.** Use Model the Domain (Water in `four-elements`). Boring code stays when the shape is already clear and local. The reshape must delete branches or invalid states, not add indirection.
3. **Name the target shape.** State what the module layout, types, and call graph would be if built today (Model the Domain and Redesign from First Principles, Water in `four-elements`). If the target crosses a function boundary, run `war-room` to explore the shape in parallel before the move.
4. **Subtract before you add.** Delete dead code, collapse one-caller wrappers, drop redundant validators, and remove orphan references before you introduce the new shape (Subtract Before You Add, Air in `four-elements`). The smallest change that reaches the target shape ships. A speculative cleanup that "might help" gets reverted.
5. **Move in small behavior-preserving steps.** Each step keeps the pin green. For an API reshape, migrate every caller and delete the old API in the same wave (Migrate Callers Then Delete Legacy APIs, Water in `four-elements`). No compatibility shims, and no parallel old and new paths. Spot-check every rename against the actual files, because renames silently miss usages in strings, prose, and back-references. Dispatch the mechanical edits to Appa on Appa's model from the avatar-setup sheet, with a scope that names the file paths, the names being moved, and the behavior to hold. Pick each dispatch's effort for the job, as `avatar-mode` describes.
6. **Prove behavior is unchanged on the real artifact.** "It compiles" is not proof (Prove It Works, Earth in `four-elements`). For a larger reshape, run an equivalence check. That can be a script that diffs old and new outputs, a recorded baseline replayed against the new code, or a smoke run on the matching surface through the project's driver (its own verify skill when it has one, otherwise Claude Code's `run`). An empty diff of the captured behavior is the proof.
7. **Confirm the change is worth keeping.** The success measure is reduced reader load (Minimize Reader Load, Air in `four-elements`). If the diff does not lower reader load somewhere, revert it.
8. **Rebase into small ordered commits.** A subtraction commit, then the reshape, then any follow-on cleanup. Shape them with Sequence Work into Verifiable Units (Fire in `four-elements`), so each behavior-preserving slice stays green before the next. Then run `yip-yip`.

## Rules

- No unplanned features, no drive-by refactors, no architecture changes.
- No suppressed type errors, no skipped tests, no empty catch blocks.
- Three failures on one unit means stop, revert to the last green state, and report what failed.

## Reply

For a plan, report each unit, its check, and its result. For a refactor, report the structure that changed, the pin you held it against, the equivalence proof, the reader-load change, and what shipped and what got reverted. A refactor reply names no new behavior.
