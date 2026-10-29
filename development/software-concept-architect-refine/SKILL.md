---
name: software-concept-architect-refine
description: Analyzes and refines existing software concepts. Use when concept designs need evidence-led refactoring for overload, redundancy, narrowness, fragmentation, or synchronization problems.
metadata:
  language: en
  translation_of: software-concept-architect-refine-cn
  version: "1.0.0"
---

# Software Concept Architect · Refine

Make the smallest necessary change that helps a concept or concept system fulfill its purpose.
Read requirements, specifications, and relevant code; reconstruct purpose, state, actions,
operational principle, and synchronizations. Use actual scenarios and counterexamples to
investigate overloading, redundancy, excessive narrowness, fragmentation, and under/over-synchronization.
Compare split/merge, unify/specialize, and tighten/loosen against the root cause, keeping no change
as an option and explaining benefits, costs, and scope of impact. Investigate facts yourself and
label inferences. Discuss consequential choices kindly in rounds, only when their prerequisites
are settled; give recommendations and reasons. Once the approach is settled, complete authorized
changes, distinguishing preserved behavior from intentional changes. Synchronizations must respect
concept contracts; verify both local purposes and end-to-end scenarios. Stop when the agreed goal
is met without known major regressions, and identify anything not verified.

Before selecting moves, read [moves and evidence](references/moves.md).
