---
name: pstack-create-formal-verification-skill
description: "Create and prove a project-local verification skill for a costly invariant or concurrency property that ordinary tests rarely reach. Use when asked to model-check a race, prove an invariant, or create a reusable formal verification workflow."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/88d47514b82e7c44f00f2b2a72ff6dd12158038c/pstack/skills/create-formal-verification-skill
  upstream-commit: 88d47514b82e7c44f00f2b2a72ff6dd12158038c
  adaptation: portable-chat-inherited
---

# Create a formal verification skill

Verify one consequential property grounded in the actual code, then leave project-local instructions that another agent can follow. State the property and the harm from breaking it in plain language.

## Environment contract

Use the active chat model and its current reasoning settings. Work directly by default. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Discover available source-control, file, terminal, and verification tools. Follow the user's scope, repository instructions, authorization, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages. Keep product fixes separate from verification work unless the user authorizes them.

## Ground the target

Start with the area or bug the user names. Otherwise inspect the repository for a costly promise whose failure ordinary tests rarely exercise: interleavings, retries, state transitions, parsers, or unsafe operations. Choose by actual user harm and verification value rather than convenience.

Record the checkout, exact revision, relevant uncommitted changes, and existing checks. Identify the functions, state owners, callers, and real synchronization or transaction boundaries that implement the promise. Resolve observable facts from source; leave business choices with the user.

## Select the least costly adequate method

Prefer existing reproducible tooling that the repository's maintainers can run. A model checker such as TLA+ can explore event ordering in a small design model. A code-level verifier can establish properties of actual code; a proof assistant can address a property beyond a finite bound. Choose according to the question, and explain the scope and cost.

If an appropriate verifier is unavailable, report that limitation. Generated-input tests against real code can provide useful evidence, but label them as tests rather than formal proof. Do not substitute a hand-written copy of the function and claim that checking it proves the implementation.

Map each modeled action and assumption to source locations. Treat a step as indivisible only when the code's synchronization or execution semantics justify it. Record excluded behavior, bounds, fairness or environment assumptions, and the difference between checking a model and verifying code. A passing bound or model does not prove the whole deployed system.

## Build and challenge the verification

Write the property from the intended contract, independently of whether the current implementation satisfies it. Run the check and retain its result and counterexample. When it fails, trace the counterexample through the actual code; distinguish a reachable defect from a modeling error or an unconfirmed assumption. Report defects without weakening the property to obtain a pass.

Demonstrate that each property can fail for a representative defect it is meant to detect, such as removing a guard or reordering steps. Use a task-owned scratch copy or isolated checkout; preserve existing edits and services. For a model-based check, reflect the same source defect in the corresponding modeled action and explain that mapping. This demonstrates sensitivity to the modeled defect, not automatic synchronization with future source edits.

Remove only the scratch change you introduced, then rerun the baseline. It must return to its prior result: passing, or failing only on the reported findings. An unexplained failure or an unchecked variant remains a verification gap.

## Generate and exercise the project skill

Use the requested location or the host's discovered project skill location. Write standard name and description frontmatter and concrete repository commands, with no placeholder procedures. The generated instructions preserve the active chat's model and reasoning settings and discover host capabilities rather than pinning models or editor APIs.

Include the property, source coverage, tool version, prerequisites, bounded execution command, expected results, assumptions, excluded paths, counterexample interpretation, sensitivity procedure, and owned cleanup. Reuse existing verification commands instead of creating a redundant harness.

Record the exact source revision at which each check was confirmed to describe the implementation. If relevant uncommitted changes are included, retain their diff or fingerprint; a clean commit alone does not identify that snapshot. Tell future agents to reassess source correspondence whenever covered code or another writer of the guarded state changes, and advance the synchronization record only after that reassessment.

Follow the generated skill once from its instructions, including the isolated defect check and restoration. If execution or source correspondence cannot be established, deliver a labeled draft with the missing prerequisite rather than claiming a proven workflow.

## Deliver

Explain the property, chosen method, checked source snapshot, bounds and assumptions, observed result, demonstrated defect sensitivity, and one rerun command. Translate counterexamples into the repository's own terms. For TLA+ models, explain each violation as a sequence of states and actions; when useful, show the reachable transitions with an available visualization tool. State any omitted paths and bounds. Separate formal proof, bounded exploration, generated-input testing, runtime evidence, and unknowns. Mention pstack-maintain-formal-verification-skill for later upkeep when available.
