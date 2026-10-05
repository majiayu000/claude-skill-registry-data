---
name: ui-state-completeness
description: Find and repair missing UI states or transitions in an interactive component or flow, including async ordering, stale data, partial failures, and interrupted actions when relevant. Use for behavior gaps, not merely screenshot polish.
---

# UI state completeness

Inspect what the component can actually do and how it moves between states. Do not add every imaginable state to a simple component.

## Build the relevant state map

Read the component, state ownership, request lifecycle, and product behavior. Record current states and the user/system events that change them. Include guards, pending work, visible feedback, available actions, and completion conditions. Mark unresolved product choices rather than silently making consequential new policies.

Use `assets/transition-cases.json` to choose relevant sequences. The cases are probes, not assumed requirements. Omit impossible transitions with a reason. Keep layout stress and broad accessibility audits scoped to what this behavior requires.

## Verify transitions, not just pictures

Exercise the main path and meaningful transitions into and out of loading, empty, error, populated, disabled, or partial states. For async work, control response ordering with existing local fixtures or network interception. Check that stale responses cannot replace current intent where latest-request behavior is required.

Check what happens when a component closes, navigates away, loses eligibility, or changes selection while work is pending. Verify the model and visible UI remain consistent. Cancellation of a client request does not prove cancellation of a server operation. Keep uncertain remote outcomes explicit.

For retained data during refresh, distinguish stale usable content from current results and full failure. For partial results, check that failed items are identifiable and any retry targets the intended work. Honor the application's real contracts for permissions, concurrency, and persistence.

## Repair and prove

For audits, report reproduced gaps and unresolved choices. For fixes, implement the smallest coherent state change using existing patterns. Avoid scattered flags that allow contradictory states; choose explicit state ownership when it materially simplifies correctness, without forcing a new state-machine library.

Re-run the failing event sequence and neighboring transitions. Record initial state, events in order, controlled response timing, final state, and evidence. Use deterministic tests for races and lifecycle failures when appropriate. A fixture proves simulated behavior; identify unavailable backend integration separately.

Deliver the important findings or repairs and the relevant transition coverage. Do not infer complete behavior coverage from a gallery of static state screenshots.
