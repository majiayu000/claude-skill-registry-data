---
name: solid-conventions
description: "Use when writing or reviewing SolidJS components: the component function runs once, props and signals are read inside tracking scopes, why destructuring props breaks reactivity, effects versus memos, control-flow components in place of ternaries and map, stores for nested state, event delegation and cleanup."
paths: "**/*.tsx, **/*.jsx"
---

# solid-conventions

Step 6 of the pipeline (`WORKFLOW.md`), for the signal-based UI library whose JSX looks like React's but whose
runtime does not re-render components. **Status: a base to confront with real work**, no in-house project behind it
yet (same status as `go-conventions`). Pinned to Solid 1.x (the documentation read 2026-10-02 describes the 1.x
API; latest release on the package registry that day: solid-js 1.9.15; 1.9.17 on 2026-10-20). A project on a later major re-reads the
reactivity pages first. The full-stack meta-framework (SolidStart) and the router are not covered. Habits carried
over from React are the main source of defects here, so each rule says what to unlearn.

## When
As soon as a `.tsx`/`.jsx` file importing `solid-js` is written or modified, during `code` (6) and `review` (8).

## Steps

### 1. The execution model
1. **A component function runs once**, when it is first rendered into the DOM. It is set-up code, not a render
   function. What changes later is carried by signals, memos and stores that the returned JSX reads; nothing
   re-executes the body. Conditions and computations that depend on reactive values therefore go inside the JSX or
   inside a derived function, never in the top level of the body.
2. **Reactivity exists only inside a tracking scope**: the JSX returned by a component, an effect, a memo. A signal
   read in the component body, outside any of these, is read once and never updates anything.
3. **A signal is a getter function plus a setter**: read with a call (`count()`), written with the setter, which
   also accepts an updater from the previous value. Storing an object or array in a signal and mutating it in place
   notifies nobody: set a new object or array, or use a store for frequent nested updates.

### 2. Props
1. **Do not destructure props, and do not copy a prop into a local constant**: `const { name } = props` and
   `const name = props.name` both read once and freeze the value. Read `props.name` where it is used, or wrap it in
   a function (`const name = () => props.name`) and call that.
2. **Defaults and splitting keep reactivity only through the library's helpers**: merge defaults with `mergeProps`
   (it behaves like an assignment of objects but keeps each property reactive); split props into groups with
   `splitProps` (for example to forward the rest to a DOM element).
3. **Props are read-only**; data flows down, and a child changes the parent's state through a callback prop.

### 3. Derived values, effects, cleanup
1. **Derive with a function; memoise with `createMemo`.** A derived signal (`const double = () => count() * 2`)
   stores nothing and is recomputed by each reader; a memo caches its result and recomputes once per dependency
   change. Memoise expensive or widely read computations.
2. **Effects are for side effects that leave the reactive system** (DOM work the framework does not do, logging,
   subscriptions, requests). Do not write to a signal inside an effect to derive a value: use a memo; writing in an
   effect causes extra updates or loops. Dependencies are tracked automatically from what the effect reads; an
   effect runs once at start even with no dependencies, and the order of several effects is not guaranteed.
3. **Effects nest independently**: signals read in an inner effect are not dependencies of the outer one.
4. **`onMount` runs once after set-up and tracks nothing; `onCleanup` runs when the component unmounts.** Pair every subscription, timer or listener created in an effect with an `onCleanup`.

### 4. Rendering
1. **Use the control-flow components instead of JavaScript branching in JSX** (this preference is the block's: the
   official pages present these components and neither recommend against a ternary nor against `.map`). `<Show when fallback>` for a
   condition (its `when` may be a function), `<Switch>`/`<Match>` for several, `<For each>` for a list of objects
   whose order or length changes (it moves DOM nodes and gives the index as a signal, called as `index()`), and
   `<Index each>` when the order and length are stable and the content changes (the item is the signal). `<Dynamic
   component>` renders a component chosen at run time; `<Portal>` renders outside the flow (it wraps its content in
   a `div`; `isSVG` for SVG).
2. **An error boundary catches errors during rendering and updating of its children, not errors in event handlers
   or timers.** Give it a fallback that offers the `reset` function it receives.
3. **Events**: `onClick` style attributes are delegated to the document (not case-sensitive); the `on:` form
   attaches a native listener (case-sensitive) for events that must not be delegated or custom events. An event
   handler is not reactive: changing the signal that holds a handler does not rebind it; call a reactive source
   inside a stable handler instead. Passing an array `[handler, data]` binds data without a closure.
4. **Styling**: the `class` and `classList` attributes; the `style` attribute takes a string or an object with
   dash-case keys and string values. Prefer classes to inline styles.

### 5. Shared state
1. **Prefer a module-level signal imported where needed** for simple shared state; use context when state is tied to
   a subtree or when the provider must be replaced (tests, repeated widgets: own guidance, unverified); do not drill props through several
   layers that do not use them, and consider restructuring the tree first.
2. **A store (`createStore`) is for nested objects and arrays**: it tracks each property separately through a proxy,
   so only what changed updates. Read store values directly (no call) but only inside a tracking scope; change them
   through the setter, not by assignment.

## Output / checkpoint
Components that keep every reactive read inside a tracking scope, with no destructured props, and control flow done
with the library's components. No dedicated checkpoint: `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Never an install: name the package, the person runs `pnpm add <package>`
(`CONVENTIONS.md`). Never destructure props. Never read a signal in a component body and expect it to update.
A rule with a number or an API name is the pinned major's; read `package.json` before applying it to another.

## Mechanical checks

```
grep -rnE "const \{[^}]+\} *= *props" src
grep -rnE "const [a-zA-Z]+ *= *props\.[a-zA-Z]+" src
grep -rnE "function [A-Z][A-Za-z]*\(\{" src
grep -rnE "\.map\(" src --include=*.tsx
grep -rnE "\?[^:]+:" src --include=*.tsx | grep -E "return|=>"
grep -rnE "createEffect\([^)]*set[A-Z]" src
grep -rnE "if \(.*\(\)" src --include=*.tsx
```

- A destructured parameter on a component (`function Card({ title })`) is the same defect as rule 2.1.
- `.map(` in JSX is a candidate for `<For>`; a ternary returning JSX is a candidate for `<Show>`.
- A signal call inside an `if` at the top of a component body is rule 1.2.

## Origin
Rewritten from the official SolidJS documentation (the `solidjs/solid-docs` repository, `src/routes`), read from
a shallow clone on 2026-10-02: the concepts pages (components, props, class and style, event handlers, signals,
effects, derived values and memos, control flow, context, stores, intro to reactivity). **Licence, honestly:** that
repository carries no licence file, so under rule B of `CONVENTIONS.md` the documentation is **idea only**: only
mechanisms were taken (when a component runs, what a tracking scope is, what breaks reactivity) and every sentence
here is our own wording. The library's code repository is a separate project and was not read. **Facts that move,
with their pin (Solid 1.x):** the API names (`createSignal`, `createMemo`, `createEffect`, `mergeProps`,
`splitProps`, `createStore`) and the control-flow components. **Not read, a stated gap:** the reference pages
(secondary primitives, reactive utilities, `batch`, `untrack`, `createResource`, `lazy`, `Suspense`), server
rendering and hydration, SolidStart, the router, TypeScript configuration, and testing. Refresh with
`skills/source-freshness` on the next major. Re-verified on 2026-10-20 against the official documentation site (docs.solidjs.com), pages read for facts only and
credited, no text taken, the documentation repository staying unlicensed: components and props (destructuring and
`const name = props.name` lose reactivity, `mergeProps`, `splitProps`, props read-only), effects (run once at start,
rerun on dependency change, order not guaranteed, nested effects track separately, `onMount` tracks nothing,
`onCleanup` at unmount, do not write signals in effects), signals (getter and setter, updater form, in-place mutation
notifies nobody), memos (executed once per dependency change, strict-equality skip, use for expensive derivations),
event handlers (delegation, case-insensitive delegated names, case-sensitive `on:`, array form, handler not
reactive), stores (proxy, direct reads in tracking scopes, setter for writes), intro to reactivity (components run
once, JSX, effects and memos as scopes, reads outside a scope are one-shot), conditional and list rendering (`Show`
`when` boolean or function, `Switch`, `For` against `Index`), `ErrorBoundary` (rendering and update errors only, `err`
and `reset`), `Portal` (default mount `document.body`, container element, `isSVG`), context (large trees, fewer than
a few layers: restructure first, signals imported directly as the simplest option). The code repository
(solidjs/solid) licence file was read: MIT, not otherwise used. Nothing was found wrong. **Still unverified:** `Dynamic`
and the `class`, `classList` and `style` attribute rules (§4.1, §4.4), the "provider must be replaced (tests, repeated
widgets)" reason for context (§5.1), and the delegation caveats the page lists (not carried here). Written 2026-10-02,
never run on real work.

Independent verification 2026-10-21: 20 checked, 19 matched, 0 corrected, 1 unverified
