---
name: sign-off
description: "Guide a human acceptance review of a specific build and record explicit criterion-level decisions."
metadata:
  category: Review
---

# Sign Off

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Resolve the feature, acceptance criteria, exact build/commit, and relevant review and QA records. Check the project's actual readiness requirements. Missing required evidence is a blocker, not an implied pass.
2. Prepare the build without disturbing unrelated work. Discover the correct launch/test environment from the project: UI, command line, API, service, or hardware as applicable. Use existing local or shared preview tooling; do not assume a build script or device platform.
3. Demonstrate every acceptance criterion with its preconditions and expected result. Capture evidence appropriate to the behavior. Ask the human for an explicit decision per criterion and record approved, rejected, or blocked.
4. Never substitute an agent verdict for human acceptance, infer approval from silence, or approve behavior that was not demonstrated. Reuse earlier acceptance only with the user's agreement and evidence that it remains valid for this build.
5. If the head/build changes, identify affected criteria and revalidate them. Do not fix the implementation during sign-off; record feedback for a separate development pass.
6. Save a record containing criteria, decisions, evidence, environment, SHA, and unresolved feedback. Post it or update a configured board only within the user's authorization, using the project's actual states.
7. On full acceptance, state which completion steps remain. Human acceptance does not itself authorize a merge or deployment; carry out those actions only if they were also authorized and their own gates pass.

## Deliverable

Report the exact accepted build, each decision, any rejected/blocked criteria, and the remaining action. Clean up only preview resources created for this demonstration.
