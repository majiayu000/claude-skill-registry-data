---
name: clarila-frontend
description: "Investigate and implement a scoped web frontend issue in its verified worktree. Not for backend/mobile ownership, automatic PR publication or release."
---

# Repair or implement the web behavior

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Resolve the issue/worktree using clarila-branch and existing work helpers. Read repository instructions, requirements, reproduction and relevant UI/framework skills.
2. Inspect responsible components, state/data boundaries and existing test patterns. State a short plan and capture original evidence before visible changes when required.
3. Implement the smallest coherent correction. Preserve accessibility, loading/error behavior and existing project conventions.
4. Run focused checks and the actual affected browser flow where available. Read [rendered web checks](../clarila-test/references/web.md): verify page identity, meaningful content, no error overlay, actual console health and the target interaction after reload. For UI changes, retain and inspect before/after screenshots and a short actual recording for interactive behavior, including changes to which data is visible or selectable. Use clarila-capture and publish inspected media in the verified Clarila thread with returned attachment receipts. Inspect relevant viewports; if the runtime/capture/upload is unavailable, report the concrete evidence gap rather than claiming UI capture complete. Record unavailable evidence rather than treating compilation as UI acceptance. Use clarila-test when test strategy, regression writing or test maintenance needs focused work.
5. Provide the source/diff, executed checks, before/after scenario and handoff to independent Verify/Review and Capture as needed.

## Trace the rendered behavior

Follow the user's action through the component, query/cache or form state, request result and rendered selection. For asynchronous changes, exercise the relevant initial, refresh, empty and failure states. Check that stale responses respect the current input and that failed saves preserve recoverable user work.

Bind browser observations to the candidate actually served, with the fixture and viewport recorded. Use interaction assertions for data and focus changes, alongside the required visual evidence. Retain a specific missing runtime or data prerequisite when the original flow cannot be exercised.

Reuse an applicable repository verifier and feature map. Load the relevant React, composition or accessibility rule for the changed boundary; a padding or data-visibility fix does not require importing every framework guideline or redesigning the page.

For overlapping requests, stale results, draft recovery or selection changes, read [asynchronous UI decisions](references/async-state.md). Use the [expert catalog](../clarila/references/expertise.md) to resolve `react-performance`, `react-composition` or `accessibility` only for the affected boundary.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record.

## Deliverable

Return changed source, cause/design, executed checks, actual browser evidence and remaining independent checks.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.
