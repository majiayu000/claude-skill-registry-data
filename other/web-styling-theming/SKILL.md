---
name: web-styling-theming
description: Runtime theming - applying a theme system to a live app without flash
---

# Runtime Theming Patterns

> **Quick Guide:** Two independent signals decide a theme — the OS preference (`prefers-color-scheme`) as the default, and an explicit attribute on `<html>` as the override that has to win in both directions. The attribute is stamped by a synchronous inline script in `<head>` before first paint; anything running in an effect flashes on every load. Persist the _preference_ (`light | dark | system`), never the resolved value, so "system" stays a live subscription to the OS. Themes swap token values under stable role names, one complete block per scope, each declaring `color-scheme` so native UI follows.

**Detailed Resources:**

- [examples/core.md](examples/core.md) — dual-signal CSS, pre-paint boot script, SSR and cookie theming, the three-state preference module, provider configuration, semantic token switching
- [examples/advanced.md](examples/advanced.md) — multi-brand axis, nested theme scopes, portal caveats, transition suppression, reduced motion, browser chrome
- [reference.md](reference.md) — `next-themes` prop and return-value contract, platform feature support, the specificity table

---

## Which path applies

- **The OS preference is the whole requirement, with no in-app control** — a `prefers-color-scheme` block is the entire job. None of the JavaScript below is needed.
- **A user-facing choice, in any framework** — Patterns 1, 2, 3 and 5 are the complete hand-rolled system: guarded media query, pre-paint script, three-state preference, token blocks. Follow [examples/core.md](examples/core.md).
- **A React app where localStorage is acceptable** — a provider library already implements the boot script, the persistence, the live tracking, the cross-tab sync and the transition suppression. Read Pattern 4 for its contract and its one structural limitation, then skip Patterns 2 and 3.
- **The server-rendered HTML itself must carry the theme** — the preference has to be a cookie, read during the render, because localStorage is unreachable from the server. That rules out the provider libraries, which are localStorage-only.

---

<critical_requirements>

## Before writing theming code

**Stamp the theme attribute from a synchronous inline script in `<head>`.** It is the only code that runs before the first paint — an effect runs after commit and commit runs after paint, so the flash is the defined order of operations rather than a race fast code can win.

**Persist the preference, `light | dark | system`.** Storing the resolved value discards the fact that the user asked to follow the OS, and nothing afterwards can recover it.

**Make the OS preference the default and the attribute the override, guarding the media block with `:root:not([data-theme])`.** That raises the block to (0,2,0), so an explicit choice wins in both directions whatever the source order turns out to be.

**Declare `color-scheme` in every theme scope.** It is what makes scrollbars, form controls, pickers and the overscroll canvas follow the theme, and no controller applies one for a theme name outside `light` and `dark`.

**Declare the complete token key set in every theme block.** A key present in one block and missing from another inherits the other theme's value in silence, which is how near-white borders end up on a near-black canvas.

</critical_requirements>

---

**Auto-detection:** prefers-color-scheme, color-scheme, `data-theme`, `light-dark()`, theme flash, FOUC, next-themes, ThemeProvider, useTheme, resolvedTheme, systemTheme, forcedTheme, disableTransitionOnChange, enableColorScheme, suppressHydrationWarning, `matchMedia("(prefers-color-scheme: dark)")`, `meta[name="theme-color"]`, nested theme scope, `data-brand`

**Applies to:**

- Wiring the OS preference and an explicit user override together so both are honoured
- Eliminating the flash of the wrong theme on first paint and on hydration
- Persisting a light/dark/system preference and keeping "system" live
- Swapping semantic token values per scope at runtime
- Adding a second axis — brand, tenant, contrast level — alongside light and dark
- Applying a theme scope to a subtree rather than the whole document
- Deciding what a theme provider must own and what CSS should own

**Handled elsewhere:**

- Authoring the token set — names, scales, tiers, contrast ratios and the build pipeline. This skill starts from role-named tokens already existing, and covers only what happens when a theme is _applied_ to a running application
- Utility-class authoring, and the directive a class generator uses to reference an external variable. The framework-agnostic half is Pattern 5's indirection rule: a generated layer must _reference_ the swappable variable rather than copy its value
- Component variant APIs. A variant is a choice within one theme; a theme is a set of values across all variants — and needing to edit a variant definition to add a theme means the token layer is incomplete
- Per-user density or layout differences. Those change which elements exist or how they are arranged, which no token block can express

---

<philosophy>

Runtime theming is a signal problem before it is a styling problem. Two sources of truth arrive at different times: the OS preference is available to CSS on the very first byte, and the user's stored choice is available only once a script or the server has read storage. Every classic theming bug is a failure to order those two correctly.

Three rules follow:

1. **CSS owns whatever CSS can own.** `prefers-color-scheme` is evaluated before first paint, tracks the OS live with no listener, works with JavaScript disabled, and costs nothing. Push "system" into CSS and the JavaScript layer shrinks to one job — recording an explicit override.
2. **Absence is a state.** No attribute means "follow the system". That makes the default free, makes `removeAttribute` a meaningful action, and makes the stored preference and the DOM attribute distinct on purpose rather than by accident.
3. **Store intent, derive appearance.** The preference is input and the rendered theme is output. Storing the output destroys the input, and every "my dark mode stopped following my OS" report traces back to that one substitution.

**What a theme is:** a set of values bound to stable role names within a scope. Adding a theme is adding a block of values, never editing a component — the moment a component names a mode, the theme system has stopped being data and become branching logic.

| Question                         | Answered by                                                    |
| -------------------------------- | -------------------------------------------------------------- |
| What theme is rendered?          | The attribute if present, otherwise the OS media query         |
| What did the user choose?        | The persisted preference — the only source of truth for the UI |
| What is the OS currently saying? | The media query, at all times, whatever theme is active        |
| What do components reference?    | Role tokens only — never a mode, never a raw value             |

</philosophy>

---

<patterns>

## Core patterns

### Pattern 1: The dual signal

`:root` and `[data-theme="dark"]` both score (0,1,0), so with equal specificity source order decides — and an unguarded `@media (prefers-color-scheme: dark) { :root { … } }` placed after the override rules silently defeats them. Guarding the media block breaks the tie and removes the ordering dependency.

```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme]) {
    /* (0,2,0) — applies only while no explicit choice exists */
    color-scheme: dark;
    --color-canvas: #0d0f12;
  }
}
```

Where the axis is exactly light and dark, `light-dark()` collapses the duplication: every value is declared once and `color-scheme` becomes the only switch. It resolves against the used `color-scheme`, so it does nothing under the initial `normal`.

```css
:root {
  color-scheme: light dark;
  --color-canvas: light-dark(#ffffff, #0d0f12);
}
:root[data-theme="dark"] {
  color-scheme: dark;
}
```

Full code: [examples/core.md](examples/core.md)

---

### Pattern 2: FOUC-free boot

Only a synchronous inline script in `<head>` runs early enough. On a server-rendered page the streamed HTML paints, _then_ hydration runs, _then_ effects fire — so the flash is the order of operations, and `useLayoutEffect` moves nothing because it still runs after hydration.

```html
<script>
  (function () {
    try {
      var stored = localStorage.getItem("theme-preference");
      if (stored === "light" || stored === "dark") {
        document.documentElement.setAttribute("data-theme", stored);
      }
    } catch (error) {}
  })();
</script>
```

The script stamps explicit choices only. "system" stamps nothing, which hands that case back to the media query — free, live, and with no listener. Three details go with it: `suppressHydrationWarning` on `<html>`, because the script mutates an element the framework also renders (it suppresses one level, not the subtree); a CSP nonce or hash where the policy is strict; and a **cookie** rather than localStorage wherever the server-rendered markup itself has to carry the theme.

Full code: [examples/core.md](examples/core.md)

---

### Pattern 3: Three-state preference

Two states cannot express "follow the system", so a two-state toggle invents a value at the first click and whatever it writes freezes that user out of OS tracking for good. Resolving `system` to `dark` at load and storing _that_ is the same bug wearing a different hat.

```ts
function applyThemePreference(preference: ThemePreference): void {
  const root = document.documentElement;

  if (preference === "system") {
    root.removeAttribute("data-theme"); // hand control back to the media query
    return;
  }
  root.setAttribute("data-theme", preference);
}
```

Where "system" stays live is the question that decides the cost. The media query is re-evaluated by the browser for nothing; a `matchMedia` listener costs a subscription and a re-render. Let CSS own it, and add the listener only for surfaces that genuinely cannot read CSS — a canvas, a chart library, map tiles, an embedded document.

```ts
const query = window.matchMedia("(prefers-color-scheme: dark)");
query.addEventListener("change", (event) =>
  onChange(event.matches ? "dark" : "light"),
);
```

Full code: [examples/core.md](examples/core.md)

---

### Pattern 4: A theme provider library

`next-themes` automates Patterns 2 and 3 for React: it injects the pre-paint script, persists the preference, tracks the system query live, stamps the attribute, sets `color-scheme`, syncs across tabs through the `storage` event, and can suppress transitions across the swap.

```tsx
<ThemeProvider
  attribute="data-theme"
  defaultTheme="system"
  enableSystem
  enableColorScheme
  disableTransitionOnChange
  storageKey="theme-preference"
>
  {children}
</ThemeProvider>
```

**The contract it cannot fulfil.** The preference lives in localStorage, which the server cannot read, so `theme`, `resolvedTheme` and `systemTheme` are all `undefined` on the server and during the first client render. Either drive the visual difference from CSS so it is correct on the first paint, or gate the component behind a `mounted` flag and reserve its layout. `color-scheme` is also applied only for the names `light` and `dark` — any custom theme name declares its own in CSS.

The full prop and return-value contract is in [reference.md](reference.md).

Full code: [examples/core.md](examples/core.md)

---

### Pattern 5: Semantic token switching

A theme swaps token _values_ under _stable role names_, one selector block per scope, each declaring the same complete key set. A token present in the light block and missing from the dark block does not fail loudly — it inherits the light value into the dark page.

```css
:root {
  color-scheme: light;
  --color-canvas: #ffffff;
  --color-border: #d8dce3;
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --color-canvas: #0d0f12;
  --color-border: #2a2f38;
}
```

**The indirection rule.** Any generated or tooling-owned token layer that _copies_ a value at definition time captures one theme's value forever. A one-hop `var()` reference defers resolution to use time, so the swap reaches through the generated layer:

```css
.themed {
  --color-canvas: var(--app-canvas); /* referenced, not copied */
}
```

**Per-theme imagery** cannot use `media` on `<source>` or on `<meta name="theme-color">` — both evaluate only the OS preference and are blind to the explicit override. Drive imagery from a token (`background-image: var(--image-hero)`) or from visibility rules reading the same dual signal.

Full code: [examples/core.md](examples/core.md)

---

### Pattern 6: Multi-brand and nested scopes

Brand and mode are orthogonal: brand is chosen by the deployment, tenant or route, and mode by the user and the OS. Two attributes keep them independent, so adding a brand is one block of brand inputs rather than a duplicate of every mode.

```css
:root[data-theme="dark"] {
  --color-accent: var(--brand-accent-dark);
}
:root[data-brand="acme"] {
  --brand-accent-light: #2563eb;
  --brand-accent-dark: #6ea8ff;
}
```

The same attribute lower in the tree themes a subtree, because custom properties inherit through the DOM. Three consequences: the nested block declares the **complete** token set, or the subtree renders half in each theme; it sets its own `color-scheme` and paints its own background, since it does not inherit the root canvas; and **portals escape it** — an overlay rendered into `document.body` resolves page tokens wherever it lands on screen, so render it inside the scope or copy the attribute onto the portal container. (`position: fixed` is fine; inheritance follows the DOM, not the visual box.)

Full code: [examples/advanced.md](examples/advanced.md)

---

### Pattern 7: Switch ergonomics

Any element with a `transition` on a colour property animates during the swap, and mismatched durations make the page tear through the change in waves. The fix has a load-bearing middle step:

```ts
document.head.append(style); // * { transition: none !important }
applyTheme();
window.getComputedStyle(document.body); // forces the recalc — do not remove
setTimeout(() => style.remove(), 1);
```

Without the forced read, the injection and the swap coalesce into one style recalculation and the transitions run regardless. `disableTransitionOnChange` performs exactly this sequence; enable it rather than reimplementing it.

**An instant swap is the correct default for everyone**, not a concession — suppressing it is never an accessibility regression. Where the switcher control itself animates, gate that behind `@media (prefers-reduced-motion: no-preference)`, and never animate a full-page colour crossfade for a reduced-motion user.

Full code: [examples/advanced.md](examples/advanced.md)

</patterns>

---

<decision_framework>

## Decision framework

### Who owns "system"?

```
Does anything outside CSS need to know the rendered mode?
|-- NO --> CSS owns it: media query, and no attribute for "system"
|          (live tracking is free, works without JS, correct on first paint)
|-- YES --> Which surfaces?
    |-- Canvas / charts / map tiles / embedded documents
    |   --> Add a matchMedia listener for THOSE surfaces only
    |-- The whole app, "because it is easier"
        --> Reconsider: that reintroduces the flash and the render cost
```

### Where does the preference live?

```
Must the SERVER-rendered HTML already carry the theme?
|-- NO --> localStorage plus the pre-paint inline script
|-- YES --> A cookie, read during the server render
    |-- Still need "system"? --> Yes, and CSS handles it; the cookie
                                 carries only explicit overrides
```

### Hand-rolled or provider library?

```
React, light/dark (plus named themes), and localStorage is acceptable?
|-- YES --> A provider library already solves the script, the persistence,
|           the live tracking, the cross-tab sync and the transition suppression
|-- NO --> Hand-roll, which is the answer when:
    |-- The preference must be a cookie for server rendering
    |-- The framework is not React
    |-- The theme comes from account data rather than device storage
```

### How many axes?

```
Is the second dimension chosen by the USER, as the mode is?
|-- YES --> A second user-facing axis: its own attribute, its own control
|-- NO --> Chosen by deployment, tenant or route?
    |-- YES --> Stamp it server-side as its own attribute, and leave the mode
    |           axis untouched so the switcher stays brand-agnostic
    |-- NO --> It is not an axis, it is a token value. Put it in the tokens.
```

### Should this difference be a theme at all?

```
Does it change VALUES bound to existing role names?
|-- YES --> A theme block
|-- NO --> Does it change which elements exist, or how they are laid out?
    |-- YES --> Not a theme — a feature flag or a layout decision
    |-- NO --> Does it change one component's appearance only?
        |-- YES --> Not a theme — a component variant, settled elsewhere
```

</decision_framework>

---

<red_flags>

## Red flags

**Produces a flash on every load:**

- **Applying the theme in `useEffect` or `useLayoutEffect`** — the page paints with the default theme and flips afterwards, and the flash grows with the bundle. On a slow device it reads as a broken app rather than a loading one.
- **Reading `localStorage` in the boot script without `try`/`catch`** — it throws in some privacy modes and in sandboxed iframes, and because the script runs before paint an uncaught throw blanks the page.
- **Branching on the resolved theme during render** under a provider — it is `undefined` until mount, so the server sends the light asset and it visibly swaps after hydration.

**Ignores the user's choice:**

- **An unguarded `@media (prefers-color-scheme: dark) { :root { … } }` after the override rules** — equal specificity means source order decides, so explicit light on a dark OS silently fails, and the bug moves whenever stylesheets are reordered or concatenated differently.
- **Persisting `resolvedTheme` instead of the preference** — every "system" user is frozen at whatever the OS was at first load and never tracks it again.
- **A `.dark` class with no `prefers-color-scheme` default** — a first-time visitor on a dark OS gets a white flash of a light app until they find the toggle.
- **Media-query-only theming with no override** — the user is told what their theme is.
- **A toggle reading `document.documentElement.dataset.theme`** rather than the stored preference — the attribute is absent for "system" users, so the first click appears to do nothing and cross-tab changes desync it.
- **`<source media="(prefers-color-scheme: dark)">` for theme imagery** — blind to the override, so the hero contradicts the page, and the failure is invisible in testing unless the tester's OS disagrees with their in-app choice.

**Renders half in each theme:**

- **A theme scope overriding only some tokens** — the rest inherit the other theme and produce contrast failures that no single rule looks wrong enough to reveal, worsening every time a token is added to the root.
- **Omitting `color-scheme`** — white scrollbars, blinding date pickers and a light overscroll canvas on a "dark" app.
- **A custom theme name with no explicit `color-scheme`** — no controller applies one outside `light` and `dark`.
- **Mode-named tokens referenced by components** (`--color-white`, `--gray-900`) — each new theme then means editing every component, and the names become lies once `--color-white` holds a dark grey.
- **The attribute or `color-scheme` on `<body>` rather than `<html>`** — the area outside the body, visible on overscroll, keeps the old canvas.
- **A portalled overlay rendered outside the scope that opened it** — the modal resolves page tokens instead of the scope's.

**Surprising behaviour:**

- `resolvedTheme` equals `theme` for every non-system theme; it is not "the light/dark resolution" of an arbitrary theme name. `systemTheme` reports the OS preference regardless of the active theme, which is what a "follows your system (currently dark)" label should read.
- `light-dark()` silently does nothing while `color-scheme` is `normal`.
- Stamping `data-theme="light"` for the "system" case opts that user out of live tracking — absence is the state that means "follow the OS".
- A dark theme prints as a page of black ink. `@media print { :root { color-scheme: light; … } }`.
- An `<iframe>` inherits neither your custom properties nor your `color-scheme`; an embedded document needs its own signal passed in.
- Back/forward-cache restores do not re-run the boot script. Where JavaScript owns the resolution, handle `pageshow` with `event.persisted` — CSS-owned "system" is immune.
- Forced-colors mode replaces the palette wholesale. Inside `@media (forced-colors: active)` use system colour keywords, and reserve `forced-color-adjust: none` for the rare element that loses meaning without its own colours.
- Cross-tab sync arrives through the `storage` event, which fires in _other_ tabs only — a tab never receives its own write.
- Suppressing transitions without forcing a reflow batches the injection and the swap into one recalculation, and the transitions run anyway.
- A switcher rendered outside its provider gets a no-op default context, so nothing throws and clicks silently do nothing.
- A generic storage key such as `theme` on a shared origin is overwritten by any other app on the same host.

</red_flags>
