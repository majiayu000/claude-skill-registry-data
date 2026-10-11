---
name: lwc-modal-and-overlay
description: "Use when choosing or reviewing overlay patterns in Lightning Web Components, especially `LightningModal`, confirmation dialogs, toasts, focus handling, and overlay dismissal behavior. Triggers: 'lightning modal in lwc', 'toast or modal decision', 'focus trap in modal', 'overlay close result'. NOT for full Flow screen UX design or record-edit processes that should stay on-page."
category: lwc
salesforce-version: "Spring '25+'"
well-architected-pillars:
  - User Experience
  - Reliability
tags:
  - lightning-modal
  - overlay
  - toast
  - confirm-dialog
  - focus-management
triggers:
  - "how do i use lightning modal in lwc"
  - "should this be a modal or a toast"
  - "how do i return a result from lightning modal"
  - "focus trap is broken in my modal"
  - "legacy overlay library replacement in lwc"
inputs:
  - "what user action launches the overlay and whether the interaction is blocking or non-blocking"
  - "whether the component needs a return value, confirmation, form entry, or simple notification"
  - "how focus, dismissal, and save failure should behave"
outputs:
  - "overlay selection guidance for modal, confirm, toast, or inline messaging"
  - "review findings for focus handling, dismissal rules, and modal overuse"
  - "implementation pattern for opening, closing, and returning results from overlays"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-15
---

Use this skill when a component is reaching for an overlay and the team needs to choose the lightest interaction that still protects the workflow. A modal is appropriate when the user must complete, confirm, or cancel a focused task. It is a poor default for simple success messages, non-blocking feedback, or page-state that would be clearer inline.

---

## Before Starting

Gather this context before working on anything in this domain:

- Is the user being informed, confirming an action, or completing a focused secondary task?
- Does the overlay need to return data to the caller, or is a toast or inline message enough?
- What should happen if the user presses Escape, clicks cancel, or the save inside the overlay fails?

---

## Core Concepts

Overlay design is mainly about choosing the right interruption level. The more blocking the UI becomes, the stronger the justification must be. In LWC, `LightningModal` gives a supported modal contract, but good design still depends on focus behavior, dismissal rules, and resisting the urge to use a modal for every secondary interaction.

### Choose The Smallest Necessary Overlay

Use a toast for lightweight success or informational feedback, a confirmation dialog for short irreversible actions, and a modal when the user truly needs a dedicated task container. Many weak modal experiences are really status messages or one-line confirmations wearing the wrong component.

### `LightningModal` Is A Component Contract

`LightningModal` is not opened by inserting markup into the parent template. The modal component extends `LightningModal`, is opened through the static `open()` API, and returns control back to the caller when `close(result)` runs. That contract is what makes result-passing and lifecycle handling predictable.

### Focus And Dismissal Are Product Decisions

Every overlay needs a plan for initial focus, keyboard dismissal, and focus return. If closing is temporarily unsafe during a save, that should be brief and explicit, not the permanent state of the modal. A user should always understand how to exit and where they land after doing so.

### Avoid Stacking And UI Drift

Multiple nested overlays, page navigation behind modals, and custom SLDS dialog markup all increase failure risk. If a modal needs to host a complex multi-step workflow, it may be a sign the task belongs on a page or screen flow instead.

---

## Common Patterns

### Result-Returning Modal

**When to use:** The caller needs a focused subtask such as choosing a record, editing a small payload, or confirming a set of options.

**How it works:** Create a component that extends `LightningModal`, open it with `LightningModal.open()`, and return the selected value or outcome through `close(result)`.

**Why not the alternative:** Embedding conditional modal markup in every parent component spreads focus and dismissal logic everywhere.

### Toast Or Inline Message Instead Of A Modal

**When to use:** The UI only needs to acknowledge success, warn gently, or point the user to the next step.

**How it works:** Use toast or inline feedback and keep the user in the current context.

**Why not the alternative:** Blocking overlays slow users down and add accessibility work when the interaction is not truly modal.

### Temporarily Non-Dismissable Save Window

**When to use:** The modal launches a short-running save that should not be interrupted midway.

**How it works:** Disable dismissal only for the bounded save window, show clear progress, and restore close behavior as soon as the action settles.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Need lightweight success or status feedback | Toast or inline message | The user should stay in context |
| Need quick confirmation of a risky action | Confirmation-style overlay | Minimal interruption for a focused decision |
| Need a focused secondary task with a returned result | `LightningModal` | Clear lifecycle and result-passing contract |
| Need a large multi-step workflow | Consider a page or Flow-based experience | A modal may become cramped and hard to navigate |
| Team plans to hand-build all modal markup | Prefer `LightningModal` unless there is a real gap | Supported primitives reduce focus and dismissal bugs |

---


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] The overlay type matches the true interruption level of the task.
- [ ] `LightningModal` is used for real modal workflows instead of ad hoc SLDS dialog markup.
- [ ] Initial focus, dismissal behavior, and focus return are defined.
- [ ] Escape, cancel, and save-failure behavior are all tested.
- [ ] Modal stacking or nested overlay patterns are avoided.
- [ ] The modal returns a clear result or side effect contract to the caller.

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **`LightningModal` is opened through an API, not conditional markup in the parent** - teams coming from generic web patterns often model it the wrong way first.
2. **A modal without focus planning is functionally broken** - the overlay may look complete while still being hostile to keyboard users.
3. **`disableClose` should be temporary** - using it as a permanent guard creates an interaction the user cannot exit safely.
4. **Many modal requests are really toast or inline-message requests** - choosing the heavier interaction by default adds friction and complexity without better UX.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Overlay choice | Recommendation for modal, confirm, toast, or inline feedback |
| Modal lifecycle design | Open, close, result, failure, and focus behavior plan |
| Review findings | Concrete issues in dismissal logic, accessibility, and modal overuse |

---

## Related Skills

- `lwc/lwc-accessibility` - use alongside this skill when focus, labeling, and keyboard behavior are the highest risk.
- `lwc/lifecycle-hooks` - use when overlay bugs are really rerender or cleanup issues.
- `flow/screen-flows` - use when the task is large enough that it should probably become a guided flow instead of a modal.
