---
name: ui-hazards
description: Mesa and Sierra — a `.mesa` file, a resource, a form or control, a tether, prerendering, islands, `@frontierjs/css`. Correct-but-surprising behavior in the UI realm; use when touching any of them.
---

# UI-realm live hazards

**Correct behavior you have to know about.** Things that are *wrong* live in `ISSUES.md`, one id each; things that are *fixed* live in git. If a rule here is pinned by a test that cannot be deleted quietly, it does not need to be here.

**The index below is each hazard's rule; its section's reference file holds the rest** — the mechanism, the measurement, and what it refuses. Read that file before changing code the rule is about. A term the rules use without defining (`asSystem()`, `@system`, `callService`) is one line in `references/glossary.md` under `bridge-index`.

## Routes, prerender and static
Detail: `references/routes-prerender-and-static.md`

- **The route table is a naming convention over a file tree, so it is committed too.**
- **A component rendered at BUILD time may import a sibling by relative path, and that had never worked.**
- **On a static target, dev is an SPA and the build is files, and only the build checks anything.**
- **A static route that produced no page fails the build where it was broken, and warns where it opted out.**
- **A server render answers every browser global as a wide desktop, so only a mobile-first branch bakes correctly.**
- **`renderComponent` reuses a compiled tree, so `<script module>` state is shared across every render in the process.**
- **The Shell draws the nav twice, and the drawer's copy is mounted while it is closed.**

## Tethers and records
Detail: `references/tethers-and-records.md`

- **An entry is the synced truth for a row; a view remembers what it READ.**
- **A comparison between two independent `record()` views has THREE states, and drawing two of them is a screen that lies.**
- **A `@from` column moves when a CHILD row is written, and nothing announces the parent.**
- **A tether holds what its last `load(query)` asked for, so a patch can take a row OUT of it.**
- **`@version` is the revision a screen READ, and a push does not move it.**
- **A watched record empties itself on its own delete, before the handler's next line.**

## Resources and forms
Detail: `references/resources-and-forms.md`

- **A write drops the columns the SERVER owns, and the version column is the one exception.**
- **A `File` column's control sends the bytes WITH the record, and there is no upload step.**
- **`createResource` coerces, blank-strips and validates by default.**
- **`@system` is the column an application writes and its caller does not**
- **`<Form {resource} />` with no children IS the form**
- **`find()` answers the list envelope; `invoke()` answers exactly what the method returned** (`FJS-D937`)
- **`tethered()` is the one door a screen lists rows through; a route that calls `service.find` itself owns keeping it current.**
- **A resource's `<script module>` holds what the UI says about its model, so an enum's tone map lives there once.**
- **`tethered().more()` catches its error into `.error`, so a loop on `hasMore` alone spins on a failing call.**
- **A raw route is reached with `client.fetch(path)`, which carries the client's credentials.**

## Mesa
Detail: `references/mesa.md`

- **Everything a component reaches for is on `$`, and `$` is legal only as the object of a member expression** (`FJS-D132`)
- **A Mesa instance `<script>` exports two kinds of thing: a prop and a method.**
- **On an ELEMENT `bind:` means the DOM writes back, so it is `value`, `checked`, `files` — plus `group` and `this` — and every other `bind:x` there is refused, naming `x={expr}`** (`FJS-D136`)
- **Mesa's scoped styles do not reach into child components.**
- **A component's stylesheet is ADOPTED, not appended, and an adopted sheet sorts after every `<style>` and `<link>` in the document.**
- **A block that reads a `const` derived from another `const` can mount a STALE value** (`FJS-1684`)
- **A `const` read off a getter is a constant, whatever the getter reads.**
- **A `const` that CALLS something with a `let` in its arguments is made again on every write to that `let`.**
- **Replacing a value notifies; mutating one does not — and `o = o` is the deliberate exception.**
- **An import is inert in a component with no `$:` of its own on it, and the default hint level says nothing about that.**
- **A function hides its reads from the compiler, which costs a subscription and an ordering.**
- **A `$:` block is woken by what it reads from outside itself, never by its own writes.** A called function that does `++seq` subscribes the block to `seq`; the write is ignored while the block runs (`FJS-2652`), so a state change made BY the block is not a trigger for it.
- **A `$: dep, handler` does not run at mount, and its `prev` is the same object when the change was a mutation.**
- **A watched object cannot be cloned or spread out of its proxy — `unproxy()` it.**
- **An unkeyed `{#each}` is keyed by INDEX, so a row's DOM state stays with the position after a reorder.**
- **`null` renders as nothing, but `false` means three different things depending on where it lands.**
- **A `type="number"` or `"range"` input binds a NUMBER, and an empty box binds `undefined`.**
- **In a `.md` file `{…}` interpolates a bare path only; anything else stays literal text, with no error.**
- **A compiled component called directly instead of through `mount()` renders and never answers a click.**
- **A prop a component does not declare is not an error: it is the component's `$attributes`, spread onto its root element** (`FJS-1648`) — `fli check`'s `kit-prop-unknown` grades kit components
- **A parent sends a prop only when ITS value changed, so re-sending the same value does not reset a child's own edit** (`FJS-2589`)
- **A component reaches the DOM through nodes it owns.**

## Driving a browser
Detail: `references/driving-a-browser.md`

- **An overlay that is present is not an overlay that is visible.**
- **Headless Chrome delivers almost no rendering lifecycle after load.**
- **Headless Chrome answers `(hover: none)` and `(pointer: none)`.**

## Build output and `@frontierjs/css`
Detail: `references/build-output-and-frontierjs-css.md`

- **Vite injects the built `<script>` at the first textual match for the body tag and does not skip comments.**
- **A `var()` naming a token nothing defines drops the whole DECLARATION**
- **A class name is not checked by anything**
- **A code sample highlighted with `prefix: true` loses its first character.**
- **An inline `style=` carries a custom property and the `<style>` block reads it.**
