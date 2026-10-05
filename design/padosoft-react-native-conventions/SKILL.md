---
name: padosoft-react-native-conventions
description: >-
  Use this skill when writing or reviewing React Native / Expo code — a screen, a component, a Zustand store,
  a React Query hook, a FlashList, a Reanimated animation, a navigation change, a tablet layout — and whenever
  a symptom like these shows up: "Maximum update depth exceeded", a list that jumps or overlaps while
  scrolling, an animation that starts but leaves the state wrong, a value that is stale right after being set,
  a colour that is unreadable in dark mode, a translation missing in one language only. It applies the
  conventions and the recurring mistakes distilled from two production apps. Do not use it for mobile security
  (padosoft-mobile-security-review), for what goes in a log (padosoft-logging-discipline), or for native
  module and build configuration.
license: MIT
compatibility: >-
  React Native with Expo, expo-router, React Query, Zustand, FlashList, Reanimated and a NativeWind-style
  utility CSS setup. The reasoning holds beyond those; the snippets assume them.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: The rules that survived independently in two production apps.
  profiles: react-native
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: react native, expo, react query, zustand, flashlist, reanimated, expo-router, nativewind, i18n
---

# React Native conventions

Rules distilled from the code review history of two production apps, where **90 of them are identical in
both**. That is the filter: what survived in two different products, not what sounded right once.

The complete catalogue, with stable IDs, is in [`references/rules.md`](references/rules.md). Read it when a
check fires and you need the reasoning, or before a review, to scan the area you are touching.

---

## 0. How to use it

```bash
git diff --name-only HEAD | grep -E '\.tsx?$'     # or --cached, before committing
```

Review by **area touched**, not rule by rule: a change to a list needs §6, one to an animation §7. The areas
below carry the rules that are broken most often; the catalogue has the rest.

---

## 1. Components: the design system, never the platform primitive

Use the project's shared components — text, button, pressable, icon, image — never the bare React Native ones
or a direct icon-library import. They carry theming, accessibility and the press feedback the platform
expects, and bypassing one of them re-implements it worse.

- `expo-image`, never `Image` from react-native.
- Ripple/press feedback comes from the shared component: **never** a manual `active:opacity-*` on top of it.
- Prefer a shared component's defaults to a local override; an inconsistent override is a bug in disguise.
- **One component per file**, always. No `native/` or `screen/` subfolders inside `screens/` — flat.
- No IIFE `(() => {…})()` inside JSX: extract a memoised component.
- A `Pressable` (or any View-based component) is never a child of `<Text>`.

## 2. Performance: memo, callbacks, complete dependencies

- Every exported component is wrapped in `memo()` **and** has `displayName` set right after.
- `useCallback` on every function passed to a child or used as an event handler; `useMemo` on derived
  computations — but **never** on a module-level constant.
- **Dependency arrays are complete.** The ones people forget: theme colours, `router`, the `t` of i18n, refs,
  values read out of a store selector, props.
- In a dependency array use the **root object**, never an optional path (`obj?.field`).
- Memoise string transformations done in render.

## 3. Store: selectors and reactivity

- Always use a shallow-comparison selector when reading store properties; prefer the array form for multiple
  values.
- A new store field is registered in the schema — a field that is not in the schema is not persisted, and
  nobody notices until a restart.
- `setState()` called outside a component is **not reactive** and has no action name: use it only in pure
  functions, never expecting a re-render from it.
- Prefer the store to direct key-value storage for system data.

## 4. Data: React Query

- **Query keys contain every parameter the query function reads.** A missing one serves another entry's data.
- Never type `useQuery` manually and never rebuild the returned object by hand: both throw away inference.
- Invalid parameters → `enabled`, **never** fake data, never nullable request params, never a key that
  changes shape with validity.
- Use the shared key builders; no hand-written key arrays.
- Never write a backend response into the cache without checking its shape, and never dereference a response
  array in render without a tolerant selector.
- A skeleton gated only on `isLoading` is wrong for a conditionally `enabled` query — gate on `!data` too.

See §9 for the feedback-loop trap, which is the expensive one.

## 5. Rendering and lifecycle

- Never `setState` or mutate a ref **during render** — that belongs in an effect.
- Never call navigation (`replace`/`back`) during render.
- An effect registering a subscription **always** returns its cleanup.
- A side effect gated on condition X must not sit after an early return on an unrelated condition Y.
- Gate rendering on nullable derived data while it loads; render the **error** state before the empty state.
- Clamp any index into an array that can shrink at runtime.

## 6. Lists

- An infinite-scroll list is the **primary scroll container** — never nested in another scroll view.
- **Never a list inside a slot of another list** (item, header, footer, empty). Object props passed to a list
  are stable references.
- Do not enable a query at mount inside a component rendered as a list item: it fires once per visible row.
- On a **horizontal** list, cells with intrinsic width must switch off the default layout animation —
  otherwise every recycle animates the width and the chips overlap.
- Horizontal list with paging or snapping: use the project's snapping props preset.
- No `overrideItemLayout` together with paging.

## 7. Animation

**The one that looks fine and is not** (§9 has the worked case): `withTiming` / `withSpring` return
**immediately** and animate on the UI thread. In the instant after assigning one, the shared value still holds
the **previous** value.

```tsx
scale.set(withTiming(DOUBLE_TAP_SCALE));
syncZoomState();        // ❌ reads the OLD value — gates and callbacks stay wrong
scale.set(withTiming(DOUBLE_TAP_SCALE));
syncZoomState(true);    // ✅ pass the known target explicitly
```

Only **synchronous** assignments (`sv.value = x`, as in a pinch handler) are readable right after. Otherwise
derive from the completion callback, or pass the target you already know.

Also: use `.get()`/`.set()` on shared values, never direct `.value` access or mutation. And a layout animation
(`layout`/`entering`/`exiting`) is a **mount cost across the whole surface**, not a local flourish — never on
a constant-frame wrapper, never in a dense mount window.

## 8. Navigation and layout

- Route groups: a section that is not a tab in **every** app is reached by its own path, never through an
  explicit tab-group href.
- A cross-cutting HOC (gate, guard, wrapper) is applied **once**, on the screen definition, never repeated per
  route file.
- Never an error boundary of your own: use the router's route-level one.
- Never derive **per-instance** state from a **global** routing hook in components that stay mounted under
  tabs — anchor the scope to the route that owns the subtree.
- **Structural** layout choices use the layout hooks, not CSS breakpoints; breakpoints are for styling. The
  layout class is measured on the **window** and reactively, never from a module constant, the device idiom or
  the aspect ratio.
- Font scaling applies to hero titles only, never to body text or UI chrome.

## 9. The three that cost the most

**A query key parameterised on state that a consumer of that query writes is an oscillator.** If an effect
consuming the query writes the parameter, changing it switches to a *different cache entry* — a snapshot taken
at another time. Two disagreeing snapshots ping-pong synchronously until `Maximum update depth exceeded`, and
with persistence the loop survives an app restart. The shape: a countries query keyed per locale, consumed by
an effect that writes the locale; removing and re-adding a language on the backend leaves two entries holding
different pictures. Fix: **one key without the parameter** plus explicit invalidation when it changes (a
sanctioned exception to the key rule, documented in a comment), with a **single root-level owner** of the
invalidation listener — never per-instance, or N mounted consumers fire N invalidations. Plus a ping-pong
detector on the automatic writer, which must record the **context** of the decision: an inversion caused by
the user genuinely changing context is legitimate and must not be blocked.

**Reading a shared value right after `withTiming`** — §7. The animation still plays, so it looks correct; only
the derived state is wrong.

**A literal colour next to a theme token that inverts.** Theme tokens swap between light and dark, so
`bg-primary` with `text-white` is correct in one theme and unreadable in the other: use the token's
`-foreground` counterpart. The signal to look for first: **a `dark:` override block that repeats the same
colour classes as the light one** is almost always a bug — the two blocks exist precisely to differ.

## 10. i18n

Keys added in **every** supported language, a new locale bundle registered in the locales tuple, plural
families always carrying a **base** key next to the suffixed ones, Spanish `¿`/`¡` closed, and new account
route headers given their key. Never build a locale-sensitive formatter per call: construct one object per
(locale, options) and reuse it.

## 11. TypeScript hygiene

- Never `as` to assert something already validated or already inferred; if a package's types are missing,
  **fix the package**.
- No pass-through re-exports or alias types: update the imports at the point of use.
- Barrel files use `export *`, never hand-maintained named exports.
- Destructure custom props **before** spreading onto a native component.

## 12. Logging

No `console.*`; full request/response at `debug`, never `info`; never pass a raw `Error` to the logger — wrap
it with the project's serializer. The reasoning and the per-stack mechanism live in
**`padosoft-logging-discipline`**.

---

## Checklist before committing

- [ ] Every exported component `memo()` + `displayName`; handlers in `useCallback`
- [ ] Dependency arrays complete, root objects not optional paths
- [ ] Store reads through a shallow selector; new fields registered in the schema
- [ ] Query keys complete and built with the shared builders; no manual typing; invalid params via `enabled`
- [ ] No `setState`, ref mutation or navigation during render; subscriptions return cleanup
- [ ] No list inside a list slot; horizontal lists with the right animation and snapping props
- [ ] No shared value read right after `withTiming`/`withSpring`
- [ ] No literal colour beside an inverting token; no `dark:` block identical to the light one
- [ ] i18n keys in every language, base key for plurals
- [ ] No `as` on something already validated or inferred
- [ ] Linter and type check clean

## Final report

```
Change: <what>  ·  files: <n>
Areas touched: components | performance | store | query | render | lists | animation | navigation | i18n
Violations: <n> fixed, <n> left with a reason
Sanctioned exceptions: <rule, why, where it is documented>
Linter/types: PASS | FAIL <detail>
```
