---
name: padosoft-rn-screen-scaffolding
description: >-
  Use this skill when adding a new screen, component or data-fetching hook to a React Native / Expo app —
  "make me a screen for X", "add a component that shows Y", "I need the hook for this endpoint" — and whenever
  something added earlier is half-wired: a screen whose title shows the raw key, a route that exists in one
  app of the monorepo but not the other, a component not exported from its barrel. It lists every file a new
  piece touches, in order, so nothing is left half-registered. Do not use it to review existing code
  (padosoft-react-native-conventions) or for native modules and build configuration.
license: MIT
compatibility: >-
  React Native with Expo, expo-router, React Query and a monorepo where several apps share a core package.
  Paths are examples: read the repository layout first.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: What breaks is never the code, it is the registration.
  profiles: react-native
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: react native, expo, scaffolding, screen, component, react query, i18n, monorepo
---

# React Native screen scaffolding

**What breaks is never the code, it is the registration.** A screen compiles and runs while its title shows
`account.orders.title`, while it exists in one app of the monorepo and not the other, while its component is
not exported from the barrel. Each of those is a file nobody opened.

This skill is the list of files, in order. The conventions that the generated code must follow are in
**`padosoft-react-native-conventions`**.

---

## 0. Ask first, in one batch

Never scaffold on assumptions. Collect, in a single round:

- **what it is**: screen, component, or query hook;
- **name and placement**: app-specific or shared core? A screen belongs to an app unless it is used by more
  than one; a shared component belongs to core;
- **which apps** of the monorepo it has to exist in — the answer is usually *all of them*, and that is the
  step that gets skipped;
- **route params**, if any, and their types;
- **the endpoint**, for a query hook: path, parameters, response shape, and whether it paginates.

If the answer to "which apps" is not all, write down why.

## 1. New screen — the file list

| # | File | Skipping it means |
|---|---|---|
| 1 | The screen component | — |
| 2 | Its skeleton / loading state | A blank frame on a slow connection |
| 3 | The components barrel of the folder | The screen imports from a deep path, or does not resolve |
| 4 | The screen wrapper, if the project uses one | The cross-cutting HOCs are missing (see RN-NAV-003: applied **once**, here) |
| 5 | The parent barrel export | The route file cannot import it |
| 6 | **i18n, every language** | The UI shows the raw key — the most frequent defect of all |
| 7 | i18n namespace registration | The whole namespace resolves to nothing |
| 8 | Param validation schema | A malformed param reaches the render |
| 9 | **The route file in every app** | The screen exists but is unreachable in one app |
| 10 | The header title key | An empty or English-only header |

Steps 6, 7 and 9 are the ones that are actually forgotten, and each fails **silently**: everything compiles.

## 2. New component

Start from the shape that matches, and keep the conventions the shared components already carry:

```tsx
import { memo } from "react";

interface MyThingProps {
    title: string;
    onPress?: () => void;
}

export const MyThing = memo(({ title, onPress }: MyThingProps) => {
    // custom props destructured BEFORE any spread onto a native component (RN-TS-005)
    return ( /* … */ );
});
MyThing.displayName = "MyThing";
```

- `memo()` **and** `displayName` — always (RN-PERF-001).
- One component per file (RN-UI-011).
- Text, button, pressable, icon and image come from the design system, never the platform primitive
  (RN-UI-001…003).
- Press feedback from the shared component, never a manual opacity class (RN-UI-005).
- A list uses the virtualised component, never `array.map()` (RN-LIST-001).
- Export it from the barrel: a component not in the barrel exists only for whoever wrote it.

## 3. New query hook

```tsx
export function useThings(params: ThingsParams) {
    return useQuery({
        queryKey: thingsKeys.list(params),   // the shared builder, every parameter in (RN-QUERY-001/004)
        queryFn: () => api.getThings(params),
        enabled: isValid(params),            // invalid params gate here, never fake data (RN-QUERY-003)
    });
}
```

Four things not to do, because each one throws away something the library already gives you:

- **manual typing** of `useQuery` or of the returned object — the inference is already correct (RN-QUERY-002);
- **fake data** for invalid parameters, or nullable request params, to work around the gating — that is what
  `enabled` is for;
- **a hand-written key array** instead of the shared builder;
- **a key parameterised on state that a consumer of this query writes** — that is the oscillator in
  RN-QUERY-006, and it ends in `Maximum update depth exceeded`.

Options go in a local, non-exported interface (RN-QUERY-005). Cache times come from the central constants
(RN-PERF-011).

## 4. Before declaring it done

```bash
# the barrels actually export it
grep -rn "MyThing" src/**/index.ts packages/*/src/**/index.ts
# the route exists in every app
ls apps/*/app/**/my-route*
# the i18n key exists in every language
grep -rn "my.new.key" locales/*/ i18n/*/
```

Then run the project's type check and linter. A screen that type-checks and shows a raw key is the normal
outcome of skipping step 6 — the compiler has no opinion about a missing translation.

---

## Gotchas

- **"I'll add the other app later"** is how a route ends up existing in one app only. Later is a different
  session, with a different person.
- **A barrel is not optional.** An import that reaches a deep path works until the file moves.
- **The skeleton is not a nicety**: without it the first paint of a slow screen is a blank frame, which reads
  as a broken app rather than a loading one.
- **i18n keys in every language, including the ones nobody reviews.** A missing Spanish key shows the raw key
  to Spanish users and to nobody on the team.
- **Do not invent the layout of the repository.** Read where the neighbouring screens and hooks live before
  creating files: the map in this skill is the shape, the repository has the paths.

## Checklist

- [ ] Placement decided (app-specific vs shared) and, if not every app, the reason written down
- [ ] Screen + skeleton + barrels + wrapper
- [ ] i18n keys in **every** language, namespace registered, header title key
- [ ] Param schema for every route param
- [ ] Route file present in **every** app
- [ ] Component: `memo()` + `displayName`, design-system primitives, exported from the barrel
- [ ] Query: shared key builder, every param in the key, `enabled` gating, no manual typing
- [ ] Type check and linter clean

## Final report

```
Created: <what>  ·  placement: <app|core>  ·  apps: <which>
Files: screen · skeleton · barrels · i18n (<languages>) · schema · routes (<apps>)
Not applicable: <steps, with reason>
Type check / linter: PASS | FAIL <detail>
Left to fill in: <placeholder copy, endpoint, …>
```
