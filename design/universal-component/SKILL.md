---
name: universal-component
description: Use when adding a component to kasane, when a route file grows past a few hundred lines, when the same UI is needed on both the anime and manga side, or when asked to extract, dedupe, refactor, or split a screen in this repo.
---

# Universal Component

kasane renders one series screen (`/series/[id]`, which takes either side's AniList id) on four platforms. `/anime/[id]` and `/manga/[id]` survive only as redirects for old links. Shared UI that lives inside one route file gets copy-pasted into the next one and then drifts.

**This has already happened.** The anime, manga and series screens were once three forks of one screen. Their `QuickLookup` copies diverged, progress was keyed on different ids depending on which screen marked it, and the features users relied on ended up on screens nothing linked to. They were folded back into `/series/[id]`; do not reintroduce a side-specific screen.

## The rule

> A component name exists **once**. The moment a second route needs it, it moves to `src/components/` and both routes import it.

Before defining any component inside a route file:

```bash
grep -rn "function <Name>\|const <Name>" --include="*.tsx" app src
```

If `src/components/<Name>.tsx` exists, import it. If it does not do what you need, **change it and update both call sites** rather than writing a private variant.

## Where code goes

| Layer                     | Contains                                                                   | Never contains                                           |
| ------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------- |
| `app/**/*.tsx`            | Route params, data fetching (`useQuery`), composition, screen-level layout | A reusable component definition, domain maths            |
| `src/components/`         | Presentational components taking plain props                               | `useLocalSearchParams`, direct Supabase or AniList calls |
| `src/data/`, `src/state/` | Pure logic and stores                                                      | JSX                                                      |

A route file should read as: resolve params, fetch, compose. When it does anything else at length, that is the extraction signal.

## Extracting

1. Move the function into `src/components/<Name>.tsx` as a named export (never a default export).
2. Move only the `StyleSheet.create` entries it actually uses, and convert their literals with the `design-tokens` skill while you are there.
3. Take the **union** of the diverged copies' behaviour as props. For `QuickLookup` that means `mapping: SeriesMapping | null` (from the anime copy) plus the season badge (from the manga copy), with the badge driven by a prop rather than by which route imported it.
4. Delete both originals and import the shared one.
5. `bun run system-check`, then look at both routes in the browser. Type-checking cannot catch a lost style.

## Props conventions

- Named exports only; `export function Name({ ... }: { ... })` with the props type inline for small components, or a `type NameProps = { ... }` above for larger ones. Never `interface`.
- Optional props always pair `?.` with `??`, per CLAUDE.md.
- Pressable style callbacks spread `pressFeedback(state)` from `@/theme` for their press and hover feedback. The callback state is inferred; `hovered` comes from `src/types/react-native-augment.d.ts`.
- Pure logic a component needs (layout maths, grouping, formatting) goes in `src/data/` with a test, and the component calls it.
- Spacing via container `gap`/`padding`. No margins.

## Common mistakes

| Mistake                                             | Consequence                                                                                           |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Defining a component in a route "for now"           | It gets copied to the sibling route and the copies drift. That is the current state of `QuickLookup`. |
| Extracting the copy you happened to be reading      | You silently delete the other copy's extra behaviour. Take the union.                                 |
| Leaving the old private copy behind                 | Two definitions of one name; the next reader edits the wrong one.                                     |
| Putting `useLocalSearchParams` in `src/components/` | The component is no longer reusable and cannot be tested. Pass the id as a prop.                      |
| Adding a default export                             | The repo uses named exports outside of route files.                                                   |
