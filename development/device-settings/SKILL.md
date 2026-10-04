---
name: device-settings
description: >
  How a setting that belongs to the machine rather than to the account
  is stored and read: one module signal in
  src/components/app/settings.ts, one JSON key in localStorage, loaded
  after hydration. Applies whenever adding a preference a player sets
  for themselves, or reading one from a component or from canvas code.
---

# Device settings

A setting the player changes for themselves is not account data. Two
browsers signed in as the same player disagree about it and the server
never sees it, so it does not go near `src/auth` and it does not go in
a table.

## Where it lives

[`src/components/app/settings.ts`](../../../src/components/app/settings.ts)
holds the whole of it:

- `GameSettings` names every setting and its type.
- `defaults()` says what an unasked machine is set to. Where the
  browser already knows the answer, ask it: reduced motion comes from
  `prefers-reduced-motion` rather than from a guess of ours.
- `stored()` reads the one JSON key and normalises every field through
  `src/auth/__normalize`. A stored value can be anything at all,
  including from an older version of the game, so every field falls
  back rather than being trusted.
- `settings` is the default export, a plain accessor. `setSetting(key,
  value)` changes one and writes the lot.

It is a **module signal rather than a context**, so anything can read
it: a component, a canvas module, a helper with no owner. There is no
provider to forget and nothing throws where one is missing.

## Reading and writing

```tsx
import settings, { setSetting } from '../app/settings';

const wide = (): number => settings().boxColumns;
setSetting('boxColumns', 8);
```

## The two rules that are easy to get wrong

**Storage is read after hydration, never at import.** `loadSettings()`
is called from `onMount` in `src/app.tsx`. Reading it while the page is
still being matched against the server's markup is what makes the two
disagree.

**A setting that CSS acts on is a class on the root element**, put
there by a `createEffect` in `src/app.tsx`, with the rule itself in
`src/app.css`. That is how `reduce-motion` works and how the theme
works. Do not reach for inline styles or a `<style>` tag.

**A dev-only setting is gated twice.** Its switch sits inside
`<Show when={import.meta.env.DEV}>` in the settings panel, and its
reader ANDs the setting with `import.meta.env.DEV`, so a build drops
the effect whatever a stored value says.

## The theme is not one of these

Terracotta owns the colour scheme, including its own `localStorage`
key and the no-flash script in `entry-server.tsx` that reads it before
the page paints. Read it with `useColorScheme` and
`usePreferredColorScheme`; do not mirror it into `GameSettings`.
