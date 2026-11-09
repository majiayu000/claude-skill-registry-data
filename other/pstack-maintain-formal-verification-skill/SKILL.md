---
name: pstack-maintain-formal-verification-skill
description: "Reconcile project-local formal verification with changed source, rerun it, and distinguish stale models or harnesses from product defects. Use after changes to covered code or when asked whether a model, proof, or verification skill still describes the implementation."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/88d47514b82e7c44f00f2b2a72ff6dd12158038c/pstack/skills/maintain-formal-verification-skill
  upstream-commit: 88d47514b82e7c44f00f2b2a72ff6dd12158038c
  adaptation: portable-chat-inherited
---

# Maintain a formal verification skill

Keep the verification faithful to current source. An unchanged model can keep passing after the implementation has moved on; that pass is not evidence about the new code.

## Environment contract

Use the active chat model and its current reasoning settings. Work directly by default. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Discover available source-control, file, terminal, and verification tools. Follow the user's scope, repository instructions, authorization, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

Edit the owned verification instructions, models, harnesses, and properties. Product fixes require the user's authorization. Preserve the intended property when current code violates it; a passing check is not a reason to weaken the contract.

## Establish the baseline

Find project skills by what they do: running a model checker, prover, or code-level verifier against named source. Use the user's target when given and bound the review to its covered properties. If none exists, report that prerequisite and point to pstack-create-formal-verification-skill when available.

For each check, collect the property, source mapping, tool version, command, bounds, assumptions, exclusions, and last confirmed source snapshot. Record current revision and relevant uncommitted changes. If no synchronization revision was recorded, use the last verification-file change only as a disclosed provisional baseline; it is not proof that correspondence was established then.

Run the existing check before editing and retain its result. A pass establishes only what that check currently describes. If tooling or prerequisites prevent execution, report the exact gap and continue source inspection where useful.

## Reconcile source and verification

Read changes from the last confirmed snapshot through the current one, including relevant working-tree edits. Follow covered functions through moves, renames, and splits, and find new writers of the state the property guards. Read associated commit context, then verify its claims against source.

Classify each relevant change:

- No effect on the check's modeled behavior or assumptions, confirmed against the model or harness.
- Verification drift: actions, ranges, branches, synchronization, or reachable writers no longer match the implementation.
- An intentional contract change supported by explicit requirements, tests, documentation, or commit context.
- A possible contract violation with no evidence that the intended promise changed.

Update the model or harness from source before using a rerun to judge correctness. Preserve source-backed atomicity. Change a property only for an evidenced intentional contract change, recording its old wording, new wording, and supporting reference. Keep bounds and assumptions unless the implementation requires a documented adjustment; report any reduced coverage.

## Rerun and investigate

For a pass, demonstrate that each affected property still detects a representative defect in a task-owned scratch copy or isolated checkout. Preserve existing work and services. For model-based verification, mirror the source defect in its mapped modeled action and state that limitation. Restore only owned scratch changes and rerun to recover the baseline result.

For a failure, replay the counterexample against actual source, including the environment and synchronization assumptions. An impossible modeled step is evidence of modeling error. A reachable violation of the intended contract is a product finding. Unresolved reachability or unavailable evidence remains unproven. Give the introducing commit only when history supports it; otherwise label its origin unknown. A cheap reproduction against real code can strengthen the finding, but do not silently turn maintenance into a product fix.

## Record and hand off

Update source coverage, commands, tool versions, bounds, assumptions, exclusions, and the verified snapshot in the project skill. Preserve chat-model and reasoning inheritance in generated instructions. Relevant dirty changes need a retained diff or fingerprint alongside the commit. Advance a check's synchronization record only after correspondence has been established; leave blocked checks at their previous confirmed snapshot.

Follow the updated project skill once to confirm its documented procedure runs. Keep verification edits distinct from any separately authorized product fix.

Report each check as in sync, updated, bug, or blocked; updated and bug can both apply. Include source coverage and reviewed revisions, baseline and rerun outcomes, defect-sensitivity evidence, unresolved gaps, and the rerun command. Explain each bug as a short counterexample and user harm. Distinguish drift from defects, and state when an old passing result described stale code. A model or bounded pass does not establish whole-system or production correctness.
