---
name: lwc-lightning-modal
description: "LightningModal base class (Winter '23+): extending LightningModal, open() static method, modal headers/bodies/footers, close() with result, size variants, accessibility. NOT for lightning-dialog legacy patterns (deprecated) — use lwc/lwc-modal-and-overlay."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - User Experience
  - Operational Excellence
tags:
  - lwc
  - lightning-modal
  - modal
  - dialog
  - accessibility
triggers:
  - "lightningmodal extend open method lwc"
  - "how to return result from lightning modal lwc"
  - "lightning modal size small medium large full"
  - "lightning modal close with value parent"
  - "lightning modal header body footer slots"
  - "lwc modal accessibility focus trap"
inputs:
  - Modal use case (confirmation, form, wizard)
  - Required inputs/outputs of the modal
  - Size and surface (desktop, mobile)
outputs:
  - LightningModal subclass LWC
  - Parent invocation pattern with result handling
  - Accessibility checklist
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-05-19
---

# LWC Lightning Modal

Activate when building a modal dialog in LWC — confirmation prompts, inline forms, multi-step wizards. `LightningModal` (GA Winter '23) replaces the earlier ad-hoc modal patterns and handles focus trap, accessibility, and lifecycle consistently.

## Before Starting

- **Extend `LightningModal`** from `lightning/modal` — not `LightningElement`.
- **Modal components are opened via the static `open()` method**, not rendered in the parent template.
- **Close via `this.close(result)`** — the returned promise resolves with `result`.

## Core Concepts

### Defining a modal component

```
import LightningModal from 'lightning/modal';
export default class MyConfirm extends LightningModal {
    @api label;
    handleOk() { this.close('ok'); }
    handleCancel() { this.close('cancel'); }
}
```

Template uses `<lightning-modal-header>`, `<lightning-modal-body>`, `<lightning-modal-footer>`.

### Opening the modal

```
import MyConfirm from 'c/myConfirm';
async handleOpen() {
    const result = await MyConfirm.open({
        label: 'Confirm Delete',
        size: 'small',
        description: 'Confirm deletion'
    });
    if (result === 'ok') { ... }
}
```

`open()` returns a Promise that resolves when `this.close(value)` is called.

### Sizes

`small`, `medium`, `large`, `full` — set via the `size` option.

### Accessibility

Header slot becomes the accessible label automatically. Focus trapping is built-in. First focusable element gets focus on open.

### Passing data in / out

- In: `@api`-decorated properties set via the `open()` options object.
- Out: `this.close(value)` resolves the promise with `value`.

## Common Patterns

### Pattern: Confirmation dialog

```
const ok = await ConfirmModal.open({ label: 'Delete record?' });
if (ok === 'confirm') { /* delete */ }
```

### Pattern: Inline form modal

Modal hosts a `lightning-record-edit-form`; on save, call `this.close(recordId)`. Parent refreshes its data.

### Pattern: Multi-step wizard

Maintain step state inside the modal class; each step is a different rendered fragment. Final step calls `this.close(allCollectedData)`.

## Decision Guidance

| Need | Mechanism |
|---|---|
| Confirmation or prompt | LightningModal |
| Inline-embedded panel | Regular LWC with SLDS panel classes |
| Full-screen takeover | LightningModal size='full' |
| Non-modal popover | SLDS popover utility CSS |
| Legacy dialog code | Migrate to LightningModal |

## Recommended Workflow

1. Create the modal component extending `LightningModal`.
2. Define `@api` inputs for data passed in.
3. Template uses modal header / body / footer slots.
4. Implement close paths with meaningful result values.
5. Parent calls `await MyModal.open(options)` and handles result.
6. Test keyboard navigation (Tab trap, Esc closes).
7. Test screen reader announces modal label.

## Review Checklist

- [ ] Extends LightningModal (not LightningElement)
- [ ] Uses modal header/body/footer slots for SLDS styling
- [ ] Header set via label or header slot for accessibility
- [ ] close() called with meaningful result values
- [ ] Parent handles user dismiss (no result / undefined)
- [ ] Focus trap verified; Esc closes
- [ ] Size option matches content density
- [ ] No direct DOM manipulation or raw z-index overrides

## Salesforce-Specific Gotchas

1. **Modal component must not render in parent template.** Use `open()` only.
2. **Dismissing via Esc or outside-click resolves with `undefined`.** Handle undefined as "cancelled."
3. **API not available before Winter '23.** Older orgs need alternative patterns.

## Output Artifacts

| Artifact | Description |
|---|---|
| Modal LWC | Subclass extending LightningModal |
| Parent invocation helper | `await MyModal.open(...)` wrapper |
| A11y test checklist | Keyboard + screen-reader verification |

## Related Skills

- `lwc/lwc-accessibility-patterns` — a11y fundamentals
- `lwc/lwc-forms-patterns` — form-in-modal patterns
- `lwc/lwc-wizard-patterns` — multi-step UX
