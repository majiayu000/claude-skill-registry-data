---
name: aura-to-lwc-migration
description: "Migrating Aura components to LWC: feature mapping, interoperability wrappers, event translation, navigation patterns, and Aura-LWC coexistence strategies. NOT for new LWC development from scratch or Aura feature development."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - User Experience
  - Operational Excellence
triggers:
  - "How do I convert an Aura component to LWC?"
  - "My Aura component uses aura:event — what is the LWC equivalent?"
  - "Can I use an LWC inside an Aura component or vice versa during migration?"
  - "How do I replace force:navigateToSObject in LWC?"
  - "We have 40 Aura components and need to migrate them incrementally to LWC"
tags:
  - aura-to-lwc-migration
  - interoperability
  - event-translation
  - lightning-message-service
  - navigation-mixin
inputs:
  - "List of Aura components to migrate (names, purpose, event model)"
  - "Whether the org uses Aura application events, component events, or both"
  - "Migration strategy preference: big-bang or incremental"
  - "Whether components are embedded in App Builder pages, community pages, or custom Visualforce"
outputs:
  - "LWC component parity implementation replacing the Aura component"
  - "Aura wrapper shell (when an Aura component must be surfaced inside LWC context)"
  - "Lightning Message Channel definition to replace Aura application events"
  - "Migration checklist with feature-mapping decisions documented"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# Aura to LWC Migration

This skill activates when a practitioner needs to migrate an existing Aura component to a Lightning Web Component, navigate Aura-LWC interoperability during a partial migration, or translate Aura-specific patterns (events, navigation, lifecycle hooks) to their LWC equivalents.

---

## Before Starting

Gather this context before working on anything in this domain:

- Inventory all Aura application events the component registers as handler or fires — these have no direct LWC equivalent and require redesign via Lightning Message Service (LMS).
- Confirm whether the component lives in a Lightning App Builder page, Experience Cloud page, custom tab, or embedded in Visualforce — each surface has different LWC metadata requirements (`targets` in `*.js-meta.xml`).
- Identify dynamic component creation (`ltng:dynamicComponent`, `$A.createComponent`) — this pattern has no LWC native equivalent and must be refactored using conditional rendering or a slot-based composition strategy.

---

## Core Concepts

### 1. Aura-LWC Interoperability Direction

Salesforce supports one direction of mixed-framework embedding natively:

- **LWC inside Aura** — supported. An LWC component can be added to an Aura component's markup just like any other child component. The LWC runs in its own synthetic shadow context.
- **Aura inside LWC** — not directly supported. An LWC component cannot directly include an Aura component tag in its template. The workaround is to create a thin **Aura wrapper** that exposes the Aura component and communicates with the LWC layer via Lightning Message Service or standard DOM events.

This asymmetry is critical for incremental migration planning. You can always wrap an existing Aura component inside LWC context using the wrapper pattern, but you should plan to eliminate the wrapper as the Aura component itself is eventually migrated.

### 2. Event Model Translation

Aura has two event types with different scoping semantics:

- **Component events** (`aura:event type="COMPONENT"`) — propagate up the component tree to registered ancestor handlers. LWC equivalent: `CustomEvent` dispatched with `bubbles: false` (or `bubbles: true` for limited propagation up the shadow DOM tree). Component events are a straightforward one-to-one translation.
- **Application events** (`aura:event type="APPLICATION"`) — broadcast to all registered handlers org-wide, regardless of component hierarchy. LWC has no equivalent mechanism. The canonical replacement is **Lightning Message Service (LMS)** using a `LightningMessageChannel` metadata type. LWC subscribes with `subscribe()` from `@salesforce/messageChannel`, Aura can also publish/subscribe to the same channel during a transitional coexistence period.

### 3. Lifecycle Hook Mapping

Aura and LWC lifecycle hooks map as follows:

| Aura Hook | LWC Equivalent | Notes |
|---|---|---|
| `init` handler | `connectedCallback()` | LWC `connectedCallback` fires when the element is inserted into the DOM |
| `afterRender` | `renderedCallback()` | Fires after every render; guard with a flag to avoid infinite loops |
| `unrender` / `destroy` | `disconnectedCallback()` | Fires when the element is removed from the DOM |
| `render` override | Not available | LWC does not support overriding the render function; use reactive properties instead |

`$A.getCallback()` in Aura is used to re-enter the Aura lifecycle from async contexts. In LWC this is unnecessary — standard JavaScript async patterns (`Promise`, `async/await`) work directly and property reassignment triggers re-render automatically.

### 4. Navigation Pattern Translation

Aura navigation uses `force:navigateToSObject`, `force:navigateToURL`, and similar application events. LWC uses the `NavigationMixin` from `lightning/navigation`.

| Aura Pattern | LWC Equivalent |
|---|---|
| `force:navigateToSObject` | `NavigationMixin.Navigate` with `type: 'standard__recordPage'` |
| `force:navigateToURL` | `NavigationMixin.Navigate` with `type: 'standard__webPage'` |
| `force:navigateToComponent` | Not directly available; refactor to URL-based routing |
| `force:createRecord` | `NavigationMixin.Navigate` with `type: 'standard__objectPage'`, `actionName: 'new'` |

---

## Common Patterns

### Pattern 1: Incremental Page-by-Page Migration with LMS Bridge

**When to use:** The org has many Aura components wired together via application events. A big-bang rewrite is too risky. Components need to coexist during a multi-sprint migration.

**How it works:**
1. Create a `LightningMessageChannel` (`.messageChannel-meta.xml`) that carries the same payload the Aura application event carried.
2. Update the Aura component that fires the event to publish to the LMS channel (Aura can publish LMS using `lightning:messageChannel`).
3. Build the new LWC version of the consuming component using `subscribe()` on the same LMS channel.
4. Deploy both side-by-side. The Aura publisher and LWC subscriber coexist until the publisher is also migrated.
5. Migrate the publisher component last; once it is LWC, the LMS channel can be kept or collapsed into direct CustomEvent/property binding.

**Why not the alternative:** Attempting to wire Aura application events directly to LWC breaks silently — the LWC never receives the event. LMS is the only supported cross-framework messaging channel.

### Pattern 2: Aura Wrapper for Legacy Aura Components in LWC Pages

**When to use:** A page or parent component has been migrated to LWC but it depends on an Aura child component that has not yet been rewritten.

**How it works:**
1. Create a thin Aura component (the wrapper) that contains only the legacy Aura component in its markup.
2. Expose `@api` attributes on the wrapper using `aura:attribute` — these become the interface the LWC can set.
3. Use LMS to pass data from the LWC parent to the Aura wrapper and back. The Aura wrapper subscribes to the LMS channel and updates the inner Aura component.
4. When the inner Aura component is fully migrated, delete the wrapper.

**Why not the alternative:** You cannot embed an Aura component tag directly in an LWC template — it will be treated as an unknown HTML element and silently ignored.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Component uses only component events and no global state | Direct rewrite: Aura component events → CustomEvent | Straightforward 1:1 translation; no infrastructure needed |
| Component uses Aura application events with multiple subscribers | Create LMS channel; migrate publisher and subscribers independently | LWC cannot receive Aura application events; LMS is the supported bridge |
| Component uses `$A.createComponent` for dynamic rendering | Refactor to conditional rendering (`if:true`) or a slot-based pattern | LWC has no `$A.createComponent` equivalent |
| Aura component is low-risk and isolated (no shared events) | Big-bang rewrite | Lower effort when event surface is small |
| Aura component is deeply embedded in a complex page | Incremental migration with Aura wrapper | Reduces deployment risk; allows independent testing |
| Component uses `force:navigateToSObject` | Replace with `NavigationMixin.Navigate` | NavigationMixin is the LWC-native navigation API |
| Component targets Lightning Out / Visualforce embedding | Verify LWC `@salesforce/platformResourceUrl` and `targets` metadata before migrating | LWC in Visualforce has different target metadata requirements |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Audit the Aura component.** List all `aura:attribute` (becomes `@api` or reactive `@track`/plain property), `aura:event` registrations and handlers, `force:navigation` events, `$A.*` API calls, lifecycle hooks, and any `ltng:dynamicComponent` usage.
2. **Map events to LWC equivalents.** Component events → `CustomEvent`. Application events → design a `LightningMessageChannel`. Document payload shape parity.
3. **Scaffold the LWC component.** Create the `.js`, `.html`, `.css`, and `.js-meta.xml` files. Port `aura:attribute` to `@api` properties. Port lifecycle hooks to `connectedCallback` / `renderedCallback` / `disconnectedCallback`.
4. **Translate navigation calls.** Extend the LWC class with `NavigationMixin`. Replace each `force:navigate*` event fire with the equivalent `this[NavigationMixin.Navigate](...)` call.
5. **Implement LMS channel if needed.** Create the `.messageChannel-meta.xml`, update the Aura component to publish on it, subscribe in the LWC with `subscribe()` inside `connectedCallback` and `unsubscribe()` inside `disconnectedCallback`.
6. **Verify parity.** Side-by-side functional testing: same inputs must produce same DOM output and navigation behavior. Check shadow DOM event propagation differences.
7. **Deploy and clean up.** Deploy the new LWC and, where applicable, the Aura wrapper. After the migration is confirmed stable, deprecate and remove the original Aura component and any bridge wrappers.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] All `aura:attribute` values have been ported to `@api` (public) or reactive private properties in the LWC
- [ ] Aura application events have been replaced with an LMS channel definition committed to source control
- [ ] `force:navigate*` calls have been replaced with `NavigationMixin.Navigate` calls
- [ ] Aura lifecycle hooks (`init`, `afterRender`, `destroy`) have been mapped to the correct LWC hooks
- [ ] The `.js-meta.xml` `targets` array matches the deployment surfaces (App Builder, Experience, etc.)
- [ ] Shadow DOM event propagation verified — events that used to bubble up the Aura tree may not propagate through LWC shadow roots without `composed: true`
- [ ] No `$A.*` API calls remain in the new LWC code
- [ ] Dynamic component creation patterns have been explicitly refactored or deferred with a documented plan

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **LWC cannot receive Aura application events** — An LWC component that calls `application.on('c:MyAppEvent', handler)` or registers `<aura:handler event="c:MyAppEvent">` will silently never fire. There is no runtime error. The LWC event listener simply does not exist in the Aura event registry. Impact: cross-component communication breaks completely and the failure is invisible in the console.

2. **Shadow DOM blocks Aura-style event bubbling** — In Aura, events bubble up the logical component tree regardless of rendering hierarchy. In LWC, the synthetic shadow DOM retargets events at shadow boundaries. An event dispatched inside an LWC child will not propagate outside the shadow root unless you set `bubbles: true, composed: true`. If a migrated component relied on event bubbling to reach a parent Aura component, you must add `composed: true` or redesign the communication.

3. **`renderedCallback` fires on every render, not just the first** — Aura's `afterRender` hook was triggered after initial render. LWC's `renderedCallback` fires after every re-render, including reactive property changes. Code that initializes a third-party library or modifies the DOM in `renderedCallback` without a `hasRendered` guard flag will run on every property update, causing duplicate initialization or DOM corruption.

4. **`ltng:dynamicComponent` has no LWC equivalent** — Aura's `ltng:dynamicComponent` allows runtime component injection by string name. LWC has no equivalent API. Migration requires either static conditional rendering (`if:true` / `lwc:if`) or a slot-based composition pattern. This is the most architecturally disruptive pattern to migrate and should be identified before estimating effort.

5. **`$A.enqueueAction` replaced by wire or imperative Apex — not by any `$A` equivalent** — LWC does not expose any `$A` global. Attempting to call `$A.enqueueAction` in LWC JavaScript throws a ReferenceError. Server calls must use `@wire` adapters for reactive data or `import apexMethodName from '@salesforce/apex/...'` for imperative calls wrapped in `async/await`.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| LWC component bundle | `.js`, `.html`, `.css`, `.js-meta.xml` files replacing the Aura component |
| LightningMessageChannel definition | `.messageChannel-meta.xml` file replacing Aura application events |
| Aura wrapper component (transitional) | Thin Aura shell for use when an Aura component must be consumed inside an LWC-first page during incremental migration |
| Migration checklist | Completed audit table documenting every Aura feature and its LWC mapping decision |

---

## Related Skills

- `architect/platform-selection-guidance` — Use when deciding whether to migrate at all or when comparing Aura vs LWC for new work
- `lwc/lwc-imperative-apex` — Use when porting `$A.enqueueAction` Apex calls to LWC imperative or wire patterns
