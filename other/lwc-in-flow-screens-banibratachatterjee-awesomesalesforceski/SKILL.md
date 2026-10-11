---
name: lwc-in-flow-screens
description: "Use when building, reviewing, or troubleshooting a custom Lightning Web Component that runs inside a Flow screen element, covering @api props exposed to Flow, FlowAttributeChangeEvent for output, validate() for user input validation, and flow navigation events. Triggers: 'lwc in flow screen', 'FlowAttributeChangeEvent', 'flow screen component not updating', 'flow validate method', 'flow navigation from lwc'. NOT for custom property editors (use custom-property-editor-for-flow), NOT for embedding a flow inside an LWC (use flow/screen-flows), NOT for auto-launched flows."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - User Experience
  - Reliability
triggers:
  - "how do i pass data back from a custom lwc component to a flow screen"
  - "my flow screen component output variable is not updating when the user changes a value"
  - "flow validation not running on my custom lwc screen component"
  - "how do i fire a FlowAttributeChangeEvent from a lightning web component"
  - "lwc in flow screen not reactive when input property changes"
  - "how do i navigate to next screen from inside a custom lwc in flow"
tags:
  - flow-screen
  - lwc-in-flow
  - flow-attribute-change-event
  - flow-navigation
  - flow-validation
  - screen-flow
inputs:
  - "existing or new LWC component intended for a Flow screen target"
  - "which @api properties are inputs from Flow and which are outputs back to Flow"
  - "whether the component needs custom validation before the user can navigate forward"
  - "whether the component needs to trigger navigation itself"
outputs:
  - "LWC component scaffolded or reviewed for correct Flow screen integration"
  - "FlowAttributeChangeEvent usage wired to the right @api output properties"
  - "validate() method implemented with correct return shape"
  - "navigation events connected to available-actions guard"
  - "checklist of common data-flow and reactivity issues resolved"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

Use this skill when a custom LWC component needs to participate in a Flow screen — receiving input from Flow variables, sending output back to Flow variables, validating user input before navigation, or controlling navigation programmatically. It covers the complete LWC-to-Flow contract: `@api` properties, `FlowAttributeChangeEvent`, the `validate()` method, and `FlowNavigationXxxEvent` events. This skill does not cover custom property editors, auto-launched flows, or embedding a flow inside an LWC.

---

## Before Starting

- Confirm the component will be used in a **Screen Flow**, not an auto-launched flow — screen components only run in screen flows. Auto-launched flows cannot render UI.
- Know which properties are **inputs** (Flow passes a value in), which are **outputs** (the component sends a value back to Flow), and which are both.
- Know whether the component must perform **validation** before the user can move forward, and whether it should drive **navigation** itself (Next, Back, Finish) or leave that to the standard screen buttons.
- Check that the org is on API 55.0+ (Spring '22) for full `lightning/flowSupport` support; reactive screen flow features required Spring '24 or later.

---

## Core Concepts

### Mode 1 — Building a New LWC for a Flow Screen

The component must declare `lightning__FlowScreen` as a target in its `.js-meta.xml` file. Properties meant to receive Flow variable values are decorated with `@api`. Properties meant to send values back to Flow are also `@api` but are updated via `FlowAttributeChangeEvent` rather than direct mutation.

```xml
<!-- lwc-screen-comp.js-meta.xml -->
<targets>
  <target>lightning__FlowScreen</target>
</targets>
<targetConfigs>
  <targetConfig targets="lightning__FlowScreen">
    <property name="inputValue" type="String" role="inputOnly" />
    <property name="outputValue" type="String" role="outputOnly" />
  </targetConfig>
</targetConfigs>
```

In JavaScript, never mutate `@api` properties directly. Fire `FlowAttributeChangeEvent` to notify the runtime that an output property has a new value. The flow runtime applies the change; the component does not write to its own `@api` prop.

```js
import { LightningElement, api } from 'lwc';
import { FlowAttributeChangeEvent } from 'lightning/flowSupport';

export default class MyFlowComp extends LightningElement {
  @api inputValue;
  @api outputValue;

  handleChange(event) {
    const newVal = event.detail.value;
    this.dispatchEvent(new FlowAttributeChangeEvent('outputValue', newVal));
  }
}
```

### Mode 2 — Reviewing / Auditing an Existing Flow Screen Component

When reviewing an existing component, check these four contracts:

1. **Target declared** — `lightning__FlowScreen` is in `.js-meta.xml`.
2. **Output path** — output values are communicated only via `FlowAttributeChangeEvent`, not by direct `@api` assignment.
3. **Validation contract** — if the component has internal validation, a `validate()` method exists and returns `{ isValid, errorMessage }`.
4. **Navigation guard** — if the component fires `FlowNavigationNextEvent` or `FlowNavigationBackEvent`, it first checks that `availableActions` includes `NEXT` or `BACK` respectively.

### Mode 3 — Troubleshooting Data-Flow Issues

The most common data-flow symptoms and their root causes:

| Symptom | Root cause |
|---|---|
| Output variable in Flow is always blank after the screen | Component is setting `this.outputValue = x` instead of firing `FlowAttributeChangeEvent` |
| Component appears correct but re-renders with stale value on Back navigation | Derived output not re-fired in `connectedCallback` — fire `FlowAttributeChangeEvent` for derived attrs in both `connectedCallback` and the setter that triggers the change |
| `validate()` is never called | Method is not named exactly `validate` (case-sensitive) or is not exported from the class |
| Navigation event fires but nothing happens | `availableActions` does not include the action; component fires the event regardless |
| Component not reactive when Flow passes a new input | Component is reading `@api` in `connectedCallback` only; for setter-based reactivity, use the `set` accessor |

### FlowAttributeChangeEvent Datatype Constraints

The `value` parameter passed to `FlowAttributeChangeEvent` must match the Flow datatype of the corresponding `@api` property. Supported types are: `String`, `Number`, `Boolean`, and `JSON` (for record or SObject types). Passing a complex object where Flow expects a String causes silent failures. ([Salesforce Developers: Set Up Your Screen Flow Components for Reactivity](https://developer.salesforce.com/docs/platform/lwc/guide/use-flow-screen-reactivity.html))

### Navigation Events and availableActions

Components that drive navigation import the event classes from `lightning/flowSupport` and check `availableActions` before firing them. Available navigation events are:

- `FlowNavigationNextEvent` — go to the next screen
- `FlowNavigationBackEvent` — go to the previous screen
- `FlowNavigationPauseEvent` — pause the flow
- `FlowNavigationFinishEvent` — end the flow

If the component fires a navigation event that is not in `availableActions`, the event is ignored silently. ([Salesforce Developers: Configure a Component for Flow Screens](https://developer.salesforce.com/docs/platform/lwc/guide/use-config-for-flow-screens.html))

---

## Common Patterns

### Bidirectional Property With Reactive Output

**When to use:** The component receives a value from Flow (input) and must send a modified or user-entered value back (output) — the most common pattern for any form component.

**How it works:**

1. Declare both `@api inputValue` and `@api outputValue` in JS.
2. In the template, bind to a local reactive property (not directly to `@api`).
3. On user change, fire `FlowAttributeChangeEvent('outputValue', newVal)`.
4. If the output is derived from `inputValue`, also fire `FlowAttributeChangeEvent` in `connectedCallback` and in the `set inputValue()` setter so Flow always sees the current value even when navigating back.

```js
import { LightningElement, api, track } from 'lwc';
import { FlowAttributeChangeEvent } from 'lightning/flowSupport';

export default class BidirectionalComp extends LightningElement {
  @track _internalValue = '';

  @api
  get inputValue() {
    return this._internalValue;
  }
  set inputValue(val) {
    this._internalValue = val;
    // Re-fire derived output so Flow stays in sync on back-navigation
    this.dispatchEvent(new FlowAttributeChangeEvent('outputValue', this._computeOutput(val)));
  }

  @api outputValue;

  connectedCallback() {
    // Ensure output is initialized when component first mounts
    this.dispatchEvent(
      new FlowAttributeChangeEvent('outputValue', this._computeOutput(this._internalValue))
    );
  }

  handleChange(event) {
    this._internalValue = event.detail.value;
    this.dispatchEvent(new FlowAttributeChangeEvent('outputValue', this._internalValue));
  }

  _computeOutput(val) {
    return val ? val.trim() : '';
  }
}
```

**Why not the alternative:** Assigning `this.outputValue = x` bypasses the Flow runtime's change tracking and the value is never stored in the Flow variable.

### Custom Validation Before Navigation

**When to use:** The component has business rules that must be satisfied before the user can proceed — for example, a date-range picker where the end date must be after the start date.

**How it works:** Implement a public `validate()` method that returns `{ isValid: Boolean, errorMessage: String }`. The Flow runtime calls this method when the user attempts to navigate forward; if `isValid` is false, Flow blocks navigation and displays the `errorMessage`.

```js
@api validate() {
  const isValid = this.startDate < this.endDate;
  return {
    isValid,
    errorMessage: isValid ? '' : 'End date must be after start date.'
  };
}
```

([Salesforce Developers: Validate Flow User Input](https://developer.salesforce.com/docs/platform/lwc/guide/use-flow-validate-user-input-for-custom-components.html))

**Why not the alternative:** Putting validation only inside a button click handler does not integrate with Flow's native validation cycle — the user can still navigate away by pressing the standard Next button.

### Programmatic Navigation From the Component

**When to use:** The component should trigger navigation itself — for example, a custom "Skip this step" link or an action that completes after an async operation.

**How it works:**

```js
import { LightningElement, api } from 'lwc';
import { FlowNavigationNextEvent, FlowNavigationBackEvent } from 'lightning/flowSupport';

export default class NavComp extends LightningElement {
  @api availableActions = [];

  handleNext() {
    if (this.availableActions.includes('NEXT')) {
      this.dispatchEvent(new FlowNavigationNextEvent());
    }
  }

  handleBack() {
    if (this.availableActions.includes('BACK')) {
      this.dispatchEvent(new FlowNavigationBackEvent());
    }
  }
}
```

**Why not the alternative:** Firing navigation events without checking `availableActions` creates silent failures that are hard to diagnose — the event fires but nothing happens.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Component needs to send a value back to a Flow variable | Fire `FlowAttributeChangeEvent` from an event handler | Direct `@api` mutation is not observed by the Flow runtime |
| Component has complex internal validation | Implement `validate()` returning `{ isValid, errorMessage }` | Integrates with Flow's native navigation guard |
| Component should control navigation (e.g. auto-advance) | Fire `FlowNavigationNextEvent` after checking `availableActions` | Prevents silent failures when the action is unavailable |
| Derived output depends on an input that Flow can change | Fire `FlowAttributeChangeEvent` in both `connectedCallback` and the `set` accessor | Keeps output in sync on both initial load and back-navigation |
| Component needs to configure properties visible in Flow Builder | Declare `<property>` entries with `role` in `.js-meta.xml` | Exposes the prop as an assignable input/output in Flow Builder |
| Auto-launched flow behavior is needed | Use a different flow type — do not use a screen component | Screen components only execute within screen flows |

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

- [ ] `lightning__FlowScreen` target is declared in `.js-meta.xml`.
- [ ] All output properties use `FlowAttributeChangeEvent` — no direct `@api` mutation.
- [ ] `validate()` method (if present) returns exactly `{ isValid: boolean, errorMessage: string }`.
- [ ] Navigation events (if present) check `availableActions` before dispatching.
- [ ] Derived outputs are fired in both `connectedCallback` and the input property setter.
- [ ] `FlowAttributeChangeEvent` value types match the declared Flow data types.
- [ ] Component does not fire a navigation event and a `FlowAttributeChangeEvent` in the same synchronous call (race condition risk).

---

## Salesforce-Specific Gotchas

1. **Direct `@api` mutation is silently ignored by the Flow runtime** — Setting `this.outputProp = value` inside the component looks correct in JavaScript but the Flow runtime does not observe `@api` writes from within the owning component. The Flow variable stays blank. Always fire `FlowAttributeChangeEvent`.
2. **Back navigation loses derived output if not re-fired in `connectedCallback`** — When the user navigates back to a screen, the component remounts and `connectedCallback` runs again. If a derived output is only emitted in a change handler, the Flow variable reverts to its pre-component value. Fire `FlowAttributeChangeEvent` for all derived outputs in `connectedCallback`.
3. **`validate()` must be exactly that name** — The Flow runtime looks for a method named `validate` on the component instance. A method named `validateInput` or `runValidation` is ignored. Navigation is allowed regardless of internal state.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Reviewed or scaffolded LWC | Component with correct target declaration, `@api` properties, and event-based output |
| `FlowAttributeChangeEvent` audit | List of output properties and whether they are correctly wired |
| `validate()` implementation | Method returning `{ isValid, errorMessage }` integrated with Flow's navigation guard |
| Navigation-action guard | `availableActions` check before any `FlowNavigationXxxEvent` dispatch |
| Data-flow issue report | Identified root causes with corrective steps for each symptom |

---

## Related Skills

- `flow/screen-flows` — use when designing the overall screen flow, choosing between standard and custom components, or handling flow validation strategy at the flow level.
- `lwc/wire-service-patterns` — use when the flow screen component also needs to read Salesforce data via wire adapters.
- `lwc/lwc-component-communication` — use when the component needs to communicate with sibling or parent LWC components on the same screen.
