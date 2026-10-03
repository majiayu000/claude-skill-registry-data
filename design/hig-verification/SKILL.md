---
name: hig-verification
description: "Verify UI/UX changes against baseline evidence, acceptance criteria, accessibility checks, adverse states, and protected feature behavior."
---

# Verify what the user can actually do

Follow the [root contract](../../SKILL.md). Use [verification.md](../../templates/verification.md), [state-matrix.md](../../references/state-matrix.md), and [numeric-and-web-rules.md](../../references/numeric-and-web-rules.md). The test-selection method is WORKFLOW; cited thresholds retain their original platform and standards context.

## Define the claim before testing

For each finding, state the expected repaired behavior and the old behavior that must remain intact. Connect finding → implementation → acceptance criterion → evidence. A test suite that never exercises the changed failure cannot verify its repair.

Record baseline and candidate revisions, environment, account role, data fixture, viewport/window, input method, locale, preferences, and network conditions. Capture equivalent states for comparison. Do not treat unrelated content differences as design improvement.

## Verification layers

### Static and automated checks

Run the project’s relevant lint, type, unit, integration, component, build, and accessibility tooling when available. Record commands, results, and pre-existing failures separately. A scanner finding is evidence to investigate, not an automatic complete diagnosis; a clean scan is not complete accessibility coverage.

### Real interaction checks

Execute the repaired flow from its real entry point. Complete the task, confirm its persisted or server-side result where applicable, leave, and return. Check that no hidden dead end, duplicate submission, lost draft, or invalid state appears.

Inspect console/runtime errors and network failures. Try immediate and delayed responses, retry, cancellation, and an interruption appropriate to the feature. Distinguish request cancellation from reversal of work already performed by a server.

### Input and accessibility checks

Complete relevant tasks by keyboard or alternate native input. Check names, roles, values, relationships, focus, and announcement behavior. Perform actual screen-reader tests when tools are available; do not describe an accessibility-tree inspection as a screen-reader test.

Measure target regions and contrast where required. Check enlarged text, web reflow, reduced motion, transparency/contrast adaptations, and alternate appearance within the supported scope. Apply exact exceptions and criteria rather than declaring every small icon a failure.

### Responsive and content stress checks

Test narrow, wide, and intermediate sizes relevant to the change. Include realistic dense data, long/localized labels, missing values, loading, error, and no-results states. Test the keyboard covering part of the screen when relevant.

For tables, charts, canvas, or 3D interfaces, verify both the main task and its accessible route. Preserve necessary two-dimensional relationships where allowed; a desktop screenshot is not proof of mobile usability.

### Regression and shared-consumer checks

Exercise representative consumers of changed shared components. Recheck authentication, roles, server validation, browser history, deep links, exports, saved settings, and other protected behavior affected by the diff. Sampling should follow the actual blast radius.

Compare performance against the existing budget or a documented baseline under equivalent conditions. Do not call one noisy timing sample a proven improvement.

## Test statuses and stop conditions

Use **pass**, **fail**, **blocked**, **not_run**, or **not_applicable**. Every non-pass needs a reason. “Not applicable” requires an explanation, not a wish to skip a difficult test.

Block an unqualified release recommendation when a changed critical flow fails, protected data behavior regresses, a serious access barrier is introduced, or consequential behavior remains unverified. A low-risk untested appearance variant may permit a qualified handoff; state the residual risk and who must accept it.

Differentiate **implemented** from **verified within stated coverage**. Do not claim actual user preference, comprehension, conversion, or retention improvements without the research or measurement that could support those claims.

## Output and gate

Deliver the evidence-linked test matrix, before/after comparison, unresolved findings, limitations, and release recommendation. State exactly which platforms and journeys were exercised. Include repeatable manual steps for blocked checks.

The completion gate is not “looks good.” It is that the authorized improvement meets its stated acceptance criteria, protected behavior survives, and remaining unknowns are visible rather than disguised as success.
