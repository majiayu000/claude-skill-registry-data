---
name: web-ui-base-ui
description: Unstyled accessible React component primitives
---

# Base UI Primitives

> **Quick Guide:** Base UI is an unstyled React primitive library. Components are assembled from named parts (`Root`, `Trigger`, `Portal`, `Positioner`, `Popup`, `Arrow`), polymorphism goes through the `render` prop rather than `asChild`, state is published as data attributes and as an argument to `className`/`style` functions, and every change handler receives an `eventDetails` whose `cancel()` vetoes the change. **Current: v1.7.0** — package `@base-ui/react`, imported per component subpath.

**Detailed Resources:**

- [examples/core.md](examples/core.md) — part anatomy, portal containers, menus, positioning and collision handling
- [examples/composition.md](examples/composition.md) — both `render` forms, ref merging, `useRender`, `mergeProps` precedence
- [examples/styling.md](examples/styling.md) — attribute selectors, state functions, CSS variables, all four animation routes
- [examples/state.md](examples/state.md) — controlled vs uncontrolled, `eventDetails` cancelation, `actionsRef`
- [examples/forms.md](examples/forms.md) — Field anatomy, validation modes, server errors, Fieldset, external runtimes
- [reference.md](reference.md) — data-attribute and prop tables, checklists, Radix migration notes, version history

---

<critical_requirements>

## Before writing Base UI code

**Install `@base-ui/react` and import from per-component subpaths** — `@base-ui/react/popover`, `@base-ui/react/field`. `@base-ui-components/react` stopped at a release candidate and its APIs differ.

**Reach for the `render` prop for polymorphism.** There is no `asChild` here. A component passed to `render` forwards its `ref` and spreads every received prop onto its DOM node, which is what carries the event handlers and ARIA wiring.

**Nest popups as `Portal > Positioner > Popup`, with every positioning prop on `Positioner`.** `side`, `align`, `sideOffset` and `collisionPadding` belong to the element that carries the placement transform; `Popup` stays free for your own styling and transforms.

**Style state from the data attributes** — `data-open`/`data-closed`, `data-starting-style`/`data-ending-style`, `data-popup-open` — or from the state argument to `className`/`style`. The attributes are already correct and cost no render.

**Call `eventDetails.cancel()` to veto a change.** The handler's return value is ignored, so an early `return` leaves an uncontrolled component updating anyway.

</critical_requirements>

---

**Auto-detection:** @base-ui/react, useRender, mergeProps, mergePropsN, Positioner, Popup, Backdrop, Viewport, data-popup-open, data-starting-style, data-ending-style, data-uncentered, eventDetails, preventBaseUIHandler, Field.Root, Fieldset.Legend, alignItemWithTrigger, keepMounted, actionsRef, onOpenChangeComplete, DirectionProvider, CSPProvider

**Applies to:**

- Building an accessible design system where you own the whole visual layer
- Popup positioning with collision handling as a separately styleable part
- Vetoing or inspecting the reason behind a state change — `eventDetails.reason`, `eventDetails.cancel()`
- Native-form-compatible field grouping and validation without a form runtime
- Writing your own primitives that behave like the library's — `useRender`, `mergeProps`

**Handled elsewhere:**

- **Pre-styled components** — this library ships zero CSS by design; a kit that arrives with its own appearance answers a different question.
- **How the CSS itself is authored** — parts accept `className` and `style` and publish state as attributes; which styling layer consumes them settles nothing here.
- **Form state and schema validation** — `Field` handles presentation, ARIA and native constraint validation; a runtime that owns values across a wizard plugs in through `value`/`onValueChange`/`invalid`.
- **Animation runtimes** — `keepMounted` and `actionsRef.unmount()` are the two handoff points; what drives the motion beyond CSS is not settled here.
- **Non-React usage** — these primitives are React-only.

---

<philosophy>

## Philosophy

Base UI supplies behaviour, accessibility and positioning, and no appearance at all. Three consequences follow.

**Parts are separate elements, not props.** A popup is `Root`, `Portal`, `Positioner`, `Popup` and `Arrow`, plus an optional `Backdrop` and `Viewport`, each independently styleable and replaceable. That is why positioning props live on `Positioner`: the positioned element is a different element from the decorated one, so your transforms never fight the positioning math.

**State is published, not hidden.** Every part writes its state to data attributes and passes the same state object to `className` and `style` when those are functions. Reading it from the DOM in CSS, or from the callback argument in JS, is cheaper and more correct than duplicating it into React state.

**Composition is a prop, not a wrapper.** Instead of a `Slot` element and an `asChild` boolean, every part takes `render` — an element to clone, or a function of `(props, state)` returning an element. `useRender` exposes the same mechanism so components you write behave identically to components the library ships.

**Uncontrolled first, with an escape hatch.** Components manage their own state by default. Controlling one means supplying `value`/`open` plus a handler — but the handler also receives `eventDetails`, so you can inspect why a change was requested and refuse it without ever taking ownership.

</philosophy>

---

<decision_framework>

## Decision Framework

**Which popup component?**

```
Does it block the rest of the page until answered?
├─ YES → destructive or irreversible confirmation?
│   ├─ YES → Alert Dialog
│   └─ NO  → Dialog (Drawer for an edge-anchored panel)
└─ NO → what opens it?
    ├─ Hover or focus, short text       → Tooltip
    ├─ Hover or focus, rich content     → Preview Card
    ├─ Right-click                      → Context Menu
    ├─ Click, list of commands          → Menu (Menubar when in a bar)
    ├─ Click, arbitrary content         → Popover
    ├─ Click, pick from a list          → Select
    └─ Typing, filter a list            → Combobox (Autocomplete for free text)
```

**Which composition mechanism?**

```
Need to change the element a part renders?
├─ NO → className / style, done
└─ YES → does the output depend on the part's state?
    ├─ NO  → render={<YourElement />}          (element form)
    └─ YES → render={(props, state) => …}      (function form)

Building your own part that should accept `render` too?
└─ useRender({ defaultTagName, render, props: mergeProps(...) })
```

**Controlled or uncontrolled?**

```
Does anything outside need to SET the value?
├─ YES → controlled: value/open + onValueChange/onOpenChange
└─ NO → does anything outside need to OBSERVE it?
    ├─ YES → uncontrolled + handler only (read, don't own)
    └─ NO → do you need to FORBID some changes?
        ├─ YES → uncontrolled + eventDetails.cancel()
        └─ NO → defaultValue / defaultOpen
```

**Where does styling state come from?**

```
Can the rule be expressed as an attribute selector?
├─ YES → CSS: [data-open], [data-side="top"], [data-invalid]
└─ NO → does the CONTENT change with state, not just the styling?
    ├─ YES → render={(props, state) => …}
    └─ NO → className={(state) => …} / style={(state) => …}
```

**Which animation approach?**

```
Is the motion a single interpolation between two states?
├─ YES → CSS transition + [data-starting-style] / [data-ending-style]   (preferred)
└─ NO → multi-step motion?
    ├─ YES → CSS @keyframes on [data-open] / [data-closed]
    └─ Driven by an external animation runtime?
        ├─ Popup unmounts     → keepMounted on Portal + presence wrapper
        ├─ Popup stays in DOM → render={(props, state) => …}, animate on state.open
        └─ Motion runs outside the Web Animations API → actionsRef.unmount()
```

</decision_framework>

---

<patterns>

## Core Patterns

### Pattern 1: Part Anatomy, Portal and Positioner

Every interactive component is a namespace of parts assembled by hand, and popups all follow one shape.

```tsx
import { Popover } from "@base-ui/react/popover";

<Popover.Root>
  <Popover.Trigger />
  <Popover.Portal>
    <Popover.Positioner sideOffset={8}>
      <Popover.Popup>
        <Popover.Arrow />
        <Popover.Viewport>
          <Popover.Title />
          <Popover.Close />
        </Popover.Viewport>
      </Popover.Popup>
    </Popover.Positioner>
  </Popover.Portal>
</Popover.Root>;
```

`Portal` escapes ancestor `overflow` and stacking contexts, `Positioner` owns the collision math and carries the transform, `Popup` is yours to style and animate without disturbing it, `Viewport` keeps content stable while the popup resizes. Menus, Select, Tooltip, Preview Card and Context Menu repeat the skeleton with extra parts.

Full code: [examples/core.md](examples/core.md)

---

### Pattern 2: Styling Unstyled Parts

`className` and `style` take a plain value or a function of the part's state; data attributes carry the same information into CSS, which is where it costs nothing.

```css
.popup[data-open] {
  opacity: 1;
}
.popup[data-side="top"] {
  transform-origin: bottom center;
}
.arrow[data-uncentered] {
  visibility: hidden;
}
```

`data-side` is `top | bottom | left | right | inline-start | inline-end` and `data-align` is `start | center | end` — both report where the popup actually landed, not where you asked for it, so side-aware rules survive every collision outcome.

Full code: [examples/styling.md](examples/styling.md)

---

### Pattern 3: Render-Prop Composition

`render` replaces the element a part produces. The element form clones and merges for you; the function form hands you the merged props to spread yourself.

```tsx
// Element form — change the tag, or hand over your own component
<Menu.Item render={<a href="/library" />}>Add to Library</Menu.Item>

// Function form — full control, and content that varies by state
<Switch.Thumb
  render={(props, state) => (
    <span {...props}>{state.checked ? <CheckedIcon /> : <UncheckedIcon />}</span>
  )}
/>
```

`className` strings are concatenated, `style` objects merged and handlers chained — but only onto a target that forwards `ref` and spreads what it receives.

Full code: [examples/composition.md](examples/composition.md)

---

### Pattern 4: Building Your Own Parts

`useRender` plus `mergeProps` gives a component you write the same `render` API the library's parts have.

```tsx
import { mergeProps } from "@base-ui/react/merge-props";
import { useRender } from "@base-ui/react/use-render";

export function Text({ render, ...otherProps }: useRender.ComponentProps<"p">) {
  return useRender({
    defaultTagName: "p",
    render,
    props: mergeProps<"p">({ className: "text" }, otherProps),
  });
}
```

`mergeProps` merges right-to-left — handlers run rightmost-first, `className` concatenates rightmost-first, rightmost `style` keys win — and it does **not** merge `ref`. Every ref that needs the node goes to `useRender`'s `ref` parameter, which takes one ref or an array. `event.preventBaseUIHandler()` suppresses the library's own handler from inside a merged one.

Full code: [examples/composition.md](examples/composition.md)

---

### Pattern 5: Controlled vs Uncontrolled, and Canceling Changes

Components are uncontrolled by default. Every change handler takes `eventDetails` as its second argument, whose `reason` says why the change was requested and whose `cancel()` refuses it — on an uncontrolled component too.

```tsx
<Tooltip.Root
  onOpenChange={(open, eventDetails) => {
    if (eventDetails.reason === "trigger-press") {
      eventDetails.cancel();
    }
  }}
/>
```

Branch on `reason` rather than inferring intent from the new value. `isCanceled` only reports whether another handler in the chain already cancelled. `onOpenChangeComplete` fires after animations settle, and `actionsRef` exposes imperative `close()` and `unmount()`.

Full code: [examples/state.md](examples/state.md)

---

### Pattern 6: Fields, Fieldsets and Forms

`Field` wires a label, a control, a description and an error message together with the ARIA relationships. `Form` collects external errors and maps them onto fields by `name`.

```tsx
<Form errors={errors} onClearErrors={setErrors}>
  <Fieldset.Root>
    <Fieldset.Legend>Contact</Fieldset.Legend>
    <Field.Root name="url" validationMode="onBlur">
      <Field.Label>Homepage</Field.Label>
      <Field.Control type="url" required />
      <Field.Error />
    </Field.Root>
  </Fieldset.Root>
</Form>
```

`Field.Root` publishes `data-valid`, `data-invalid`, `data-dirty`, `data-touched`, `data-filled`, `data-focused` and `data-disabled`, so the whole group styles from one element. `name` on `Field.Root` puts the control into native `FormData` — non-native controls render hidden inputs to participate. `validationMode` is `onSubmit` (default), `onBlur` or `onChange`, and `validationDebounceTime` throttles an async `validate`.

Full code: [examples/forms.md](examples/forms.md)

---

### Pattern 7: Popup Positioning Essentials

`Positioner` is the whole positioning API. Defaults: `side="bottom"`, `align="center"`, `sideOffset={0}`, `collisionPadding={5}`, `sticky={false}`, `positionMethod="absolute"`, `collisionBoundary="clipping-ancestors"`.

```tsx
<Popover.Positioner
  side="top"
  align="start"
  sideOffset={8}
  collisionPadding={16}
  sticky
>
  <Popover.Popup>
    <Popover.Arrow />
  </Popover.Popup>
</Popover.Positioner>
```

- `sideOffset` is the anchor-to-popup gap — at least the arrow's height, or the arrow overlaps the trigger.
- `collisionBoundary` and `collisionPadding` define the box the popup stays inside; raise the padding when a fixed header would clip it.
- `sticky` keeps the popup in view as the anchor scrolls away, instead of letting it drift off with the anchor.
- `positionMethod="fixed"` is the fix for an anchor inside a transformed or `contain`-ed ancestor.
- `anchor` positions against an arbitrary element or virtual rect, which is how cursor- and selection-anchored popups are built.
- Popups publish `--anchor-width`, `--available-height`, `--popup-width` and `--popup-height` for width-matching and max-height rules.

Full code: [examples/core.md](examples/core.md)

</patterns>

---

<red_flags>

## Red flags

**Breaks at runtime:**

- Installing `@base-ui-components/react` — frozen at a release candidate, with APIs that differ from the maintained `@base-ui/react`.
- Reaching for `asChild` — it does not exist; the part renders its default element and your child is ignored or duplicated.
- A `render` target that neither spreads props nor forwards `ref` — the popup never opens, positioning never attaches, ARIA wiring is lost, and nothing throws.
- Positioning props on `Popup` instead of `Positioner` — not part of `Popup`'s API, so they land on the DOM node as unknown attributes.
- Omitting `Portal` — ancestor `overflow: hidden` clips the popup and ancestor stacking contexts trap it.
- A controlled component with `open` supplied and no `onOpenChange` — escape, outside press and `Close` all request a change nobody listens for, so the user is trapped.
- Returning early from a change handler to block a change — the return value is ignored and an uncontrolled component still updates. Call `eventDetails.cancel()`.

**Surprising behaviour:**

- A `transform` on `Positioner` overwrites the computed placement — put your own transforms on `Popup`, or express the gap as `sideOffset`.
- Mirroring `open` or `value` into React state to drive CSS — the data attributes already carry it, the copy drifts, and it updates a frame later than the attribute.
- `sideOffset={0}` with an `Arrow` — the arrow overlaps the trigger.
- A hard-coded popup `max-height` instead of `--available-height` — overflows short viewports.
- `data-uncentered` unhandled on `Arrow` — after collision handling the arrow points at nothing.
- `keepMounted` with nothing driving unmount — hidden markup stays in the DOM and in the accessibility tree.
- `defaultValue` is read once; changing it later warns in development and does nothing.
- `isCanceled` reports that some handler already called `cancel()`; assigning to it cancels nothing.
- `data-starting-style` and `data-ending-style` exist only during the transition — a rule written without them applies to the resting state too, which is why transitions here are recommended over `@keyframes`: a transition can also be cancelled mid-flight when a closing popup reopens.
- Unmount waits on `element.getAnimations()`, so motion applied to a _child_ of `Popup` does not delay it — animate `Popup` itself or call `actionsRef.unmount()`.
- `Select.Positioner` defaults `alignItemWithTrigger` to `true`, overriding ordinary `side`/`align` expectations, and switches itself off on touch or in a small viewport — so the popup positions differently across devices.
- `Menu.Item` closes the menu on click by default; `closeOnClick={false}` is for items that toggle something.
- `Menu.Item` renders a non-native button by default — set `nativeButton` where a real `<button>` matters.
- `Fieldset.Legend` renders a `<div>`, not a `<legend>`; select it by class.
- `mergeProps` runs handlers right-to-left, the opposite of most merge helpers.

</red_flags>
