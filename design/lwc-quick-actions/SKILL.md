---
name: lwc-quick-actions
description: "Use when building a Lightning Web Component that runs from a record page quick-action button — either a screen action that renders UI in a modal or a headless action that invokes logic with no UI. Triggers: 'lwc quick action on record page', 'headless quick action no ui', 'closeactionscreenevent not working', 'how to pass recordid into quick action lwc'. NOT for Flow screen components — use lwc/lwc-in-flow-screens. NOT for global actions without a record context — use admin/global-actions-and-quick-actions."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Performance
  - Security
  - Operational Excellence
triggers:
  - "lwc quick action on record page"
  - "headless quick action no ui"
  - "closeactionscreenevent not working or modal will not close"
  - "how to pass recordid into quick action lwc"
  - "quick action vs flow action which should i use"
  - "quick action modal size too small or cannot resize"
  - "toast after quick action completes then navigate to record"
tags:
  - lwc-quick-actions
  - quick-action
  - record-action
  - headless-action
  - closeactionscreenevent
  - lightning-record-action
inputs:
  - "record context — object API name and fields the action will read or write"
  - "desired UX — modal screen action versus headless fire-and-forget"
  - "post-action expectations — toast message, navigation target, record-refresh semantics"
  - "security context — which Apex methods are called and what CRUD/FLS still applies"
outputs:
  - "compliant LWC quick-action bundle with correct `.js-meta.xml` target and `actionType`"
  - "post-action UX plan covering `CloseActionScreenEvent`, toasts, and navigation"
  - "checker output flagging headless-with-template, missing `@api recordId`, unsafe close timing"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-23
---

# LWC Quick Actions

Use this skill when a record-page button needs to launch a Lightning Web Component — either as a modal (screen action) or as silent on-click logic (headless action). The right choice depends on whether the user has to see or confirm anything, not on what is easier to code.

---

## Before Starting

Gather this context first:

- What object does this action run on, and what fields does it read or write?
- Does the user need to see or confirm anything, or is this a one-tap operation?
- After success, should the page toast, refresh the record, navigate, or stay where it is?
- Is the called Apex `@AuraEnabled (with sharing)` and does it still enforce CRUD/FLS?
- Is this invoked from a record page, a list view, or a related list — the injected inputs differ.

---

## Core Concepts

Quick-action LWCs are regular components with a specific meta.xml shape and a specific lifecycle contract. Two modes exist: screen actions (render UI in a modal) and headless actions (no UI, a single `invoke()` method).

### Declaration In `.js-meta.xml`

The bundle must declare the `lightning__RecordAction` target and, inside `<targetConfigs>`, set `actionType="ScreenAction"` for a modal or `actionType="Action"` for headless. Without that target config the component will not appear in the quick-action picker. The target also controls which inputs the platform injects — `lightning__RecordAction` is what causes `recordId` to flow in.

### `recordId` Is Auto-Injected As `@api`

When the target is `lightning__RecordAction`, Salesforce injects `recordId` into the component's `@api recordId` property before `connectedCallback`. If the property is not declared with `@api`, the value never lands. `objectApiName` is not auto-injected on quick actions — if you need it, pass it through the meta.xml config or look it up via `getRecord`.

### Screen Actions Close Through An Event

A screen action renders its template inside the quick-action modal. To dismiss the modal, the component imports `CloseActionScreenEvent` from `lightning/actions` and dispatches it: `this.dispatchEvent(new CloseActionScreenEvent())`. This event does not save anything — it is purely a close signal, so the save must complete before the dispatch, not after.

### Headless Actions Implement `invoke()`

A headless action has no template. Instead it exposes an `@api invoke()` method that Salesforce calls when the button is clicked. The platform dismisses the action when `invoke()` returns (or its returned promise resolves). Toasts fired via `ShowToastEvent` from within `invoke()` render on the host page — that is the supported way to give feedback from a headless action.

### Post-Action UX Must Be Deliberate

Screen actions do not automatically refresh the record. For an in-page refresh use `getRecordNotifyChange` from `lightning/uiRecordApi` or `refreshApex` on a wire. For a hard navigation use `NavigationMixin.Navigate` with `standard__recordPage` — do not reach for `window.location.reload()`, which breaks SPA navigation and destroys in-flight state.

### Security Still Applies

`@AuraEnabled` does not bypass CRUD/FLS. Use `WITH USER_MODE` in SOQL/DML or `Security.stripInaccessible` in the Apex called by the action. The quick-action surface does not change the permission model — the user runs the action as themselves.

---

## Common Patterns

### Screen Action — Confirm, Edit, Save, Close

**When to use:** The user needs to see current values, edit something, or read a warning before the save commits.

**How it works:** Declare `lightning__RecordAction` with `actionType="ScreenAction"`. Render UI bound to `@api recordId`. On submit, call imperative Apex or a `lightning-record-edit-form`, await the result, show a toast, and then dispatch `CloseActionScreenEvent`. Optionally call `getRecordNotifyChange([{ recordId }])` so the record page reflects the change.

**Why not the alternative:** A headless action cannot show the form. A Flow launched as a quick action is appropriate when the UI is declarative and low-code ownership is a goal, but it carries Flow-runtime overhead and a different debugging story.

### Headless Action — One-Tap Status Change

**When to use:** A single-field update, a confirmation toast, no form needed. Examples: "Mark as Read", "Approve", "Re-send Welcome Email".

**How it works:** Declare `actionType="Action"`. Omit the template. Implement `async invoke()` that calls the Apex method, awaits the result, fires `ShowToastEvent`, and returns. Do not dispatch `CloseActionScreenEvent` — there is no modal to close.

**Why not the alternative:** A screen action with an auto-submitting template flickers a modal for no reason. A Flow would be overkill for a single-field update.

### Screen Action With Post-Save Navigation

**When to use:** The action creates a related record and the user should land on it.

**How it works:** After the Apex save returns the new Id, call `NavigationMixin.Navigate({ type: 'standard__recordPage', attributes: { recordId: newId, objectApiName: 'Case', actionName: 'view' } })`, then dispatch `CloseActionScreenEvent`. The modal closes as the page transitions.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Simple confirm plus single-field update | Headless action with `invoke()` | No UI needed; platform closes on return |
| Multi-step UI, conditional branching, or form | Screen action | Modal template is the only place to render the form |
| Declarative owners, screen with validation, low code | Flow launched as a quick action | Flow Builder owns the UX without custom JS |
| Action needs to land the user on a new related record | Screen action with `NavigationMixin` before close | Navigation must fire before the modal is dispatched closed |
| Bulk action across a list view | List-view action wrapper (not a single-record action) | `recordId` is not injected on list actions — design for a list of ids |

---

## Recommended Workflow

1. Confirm the UX — modal or no modal? If no UI is needed, pick headless.
2. Write `.js-meta.xml` with `lightning__RecordAction` and the correct `actionType`. Add `<targetConfig>` entries only for targets you actually support.
3. Declare `@api recordId` (and `@api invoke` if headless). Read only the fields you need via `getRecord` or Apex.
4. For screen actions, do the save first, then fire the toast, then dispatch `CloseActionScreenEvent`. For headless, resolve from `invoke()` after the toast.
5. Decide the refresh strategy — `getRecordNotifyChange`, `refreshApex`, or `NavigationMixin`. Never use `window.location.reload()`.
6. Run `python3 scripts/check_lwc_quick_actions.py` over the bundle to catch headless-with-template, missing `@api recordId`, pre-save close, and `window.location` usage.
7. Add an Apex test for the called method and a Jest test for the JS — verify the close event fires only after the save resolves.

---

## Review Checklist

- [ ] `.js-meta.xml` declares `lightning__RecordAction` and a matching `<targetConfig>` with the correct `actionType`.
- [ ] `@api recordId` is declared in the JS — the component actually receives the record context.
- [ ] Screen actions save first and dispatch `CloseActionScreenEvent` only after the save resolves.
- [ ] Headless actions have no `<template>` and the action closes by returning from `invoke()`.
- [ ] Post-save refresh uses `getRecordNotifyChange`, `refreshApex`, or `NavigationMixin` — never `window.location.reload()`.
- [ ] The Apex called by the action enforces CRUD/FLS (`WITH USER_MODE` or `stripInaccessible`).
- [ ] Toasts use `ShowToastEvent` and fire before the close/return.

---

## Salesforce-Specific Gotchas

1. **`CloseActionScreenEvent` does not save** — it only dismisses the modal. Dispatching it before the Apex save resolves throws away the save because the component is destroyed mid-promise.
2. **Headless actions render nothing** — any `<template>` content in an `actionType="Action"` bundle is ignored; if you need a confirm dialog, use `LightningConfirm` from inside `invoke()` and still resolve the promise to close.
3. **`recordId` is only auto-injected under `lightning__RecordAction`** — switching the target (e.g., to `lightning__AppPage`) silently stops the injection and `recordId` becomes `undefined`.
4. **Modal size is not freely configurable** — quick-action modals follow the platform's sizing rules; a dedicated wide UI usually belongs in `lwc-lightning-modal` or a full page instead.
5. **List-view actions do not receive `recordId`** — they receive a list of record ids via the action target config. Reusing a single-record component on a list surface breaks silently.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Quick-action LWC bundle | JS, HTML (if screen), and `.js-meta.xml` with the correct target and `actionType` |
| Post-action UX plan | Notes on toast copy, refresh strategy, and navigation target |
| Checker report | Findings on template-in-headless, missing `@api recordId`, premature close, and `window.location` usage |

---

## Related Skills

- `lwc/lwc-lightning-modal` — use when the UI needs to be a modal invoked from outside a quick action, or when the quick-action modal sizing is insufficient.
- `lwc/lwc-imperative-apex` — use for the Apex-call patterns inside the action, including error handling and `@AuraEnabled(cacheable=true)` constraints.
- `lwc/navigation-and-routing` — use when deciding between `NavigationMixin`, `getRecordNotifyChange`, and `refreshApex` after the action completes.
- `lwc/lwc-in-flow-screens` — use when the component belongs inside a Flow screen rather than as a record-page quick action.
