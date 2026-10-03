---
name: nuxt-ui-tools-playground
description: Use this skill when adding, restructuring, or validating the nuxt-ui-tools playground examples, shell, navigation, or route-level composition demos.
---

# nuxt-ui-tools Playground

The playground is a maintainer-facing inspection surface. It should make one
runtime abstraction or one composition variant easy to find, run, compare, and
extend without making the shell part of the behavior under test.

## Architecture

The app has three intentionally separate layers:

- `playground/app/layouts/default.vue` and `empty.vue` both mount the shared
  `PlaygroundShell`; page layouts no longer invent their own navigation chrome.
- `playground/app/components/playground/` owns reusable shell primitives:
  `PlaygroundShell.vue`, `PlaygroundPageHeader.vue`, `PlaygroundSidebar.vue`,
  the recursive tree node, and `PlaygroundContent.vue`.
- `playground/app/pages/` owns example code, runtime fixtures, runtime controls,
  and route-level composition decisions. A page must not reimplement playground
  navigation or testing chrome.

`playground/app/app.config.ts` contains only the canonical Nuxt UI color
baseline. Keep it neutral and monochrome (`primary: 'neutral'` and
`neutral: 'zinc'`). `main.css` owns the small canonical token adjustment that
makes primary fills true black in light mode and near-white in dark mode;
neutral gray remains the secondary surface. Component `ui` props belong in an
example only when the example is explicitly demonstrating a package
composition or slot contract; never use app config as a global visual patch.

## Navigation registry

The playground is organized as abstraction families with a persistent,
collapsible tree navigator:

- `/form/*` owns field labs plus form workflows.
- `/table/*` owns data-source examples and the nested composition family.
- `/spreadsheet/*` owns core flow, reference, and stress/validation groups.

`usePlaygroundNavigation.ts` is the single hierarchy registry. Each abstraction
owns a `navigation` tree made of group nodes and route nodes. Route nodes declare
a stable `id`, exact `path`, concise `label`, useful `description`, and content
`mode`; group nodes declare `children`. The shared sidebar renders that tree and
expands only the branch relevant to the current route, so large families remain
scannable without flattening every example into one dropdown.

Keep variants as separate routes when behavior, schema, or content mode differs.
For example, table offset remote, cursor remote, filter rail, staged finance,
selection operations, and people directory are independent modules rather than
one schema behind a variant toggle. Legacy aliases may redirect to a canonical
route when the redirect is explicit and cheap.

Table size is playground testing chrome, not example UI. Every rendered table
example binds its root size to `usePlaygroundShell().tableSize`; the shared page
header owns the desktop XS/SM/MD/LG/XL selector and the mobile navigation drawer
owns the mobile copy. All table examples default to `md`. Do not add local size
selectors or make an example's concept be "small table" versus "large table".
Granular size overrides are appropriate only when the example is explicitly
testing that override.

Keep the table canvas edge-aligned inside one `NutDataListContent` boundary;
do not add decorative nested table shells. Selection actions belong in the
schema and render through `NutDataListSelectionActions`, while filter-rail
examples use their explicit rail controls.

## Page shell and content modes

Wrap normal pages in `PlaygroundContent` and choose the mode that owns their
scroll contract:

```vue
<PlaygroundContent mode="document">
  <!-- normal page: this shell content region scrolls -->
</PlaygroundContent>

<PlaygroundContent mode="fixed">
  <!-- full-height composition: the child runtime owns its viewport -->
</PlaygroundContent>

<PlaygroundContent mode="scroll">
  <!-- full-height route with one internal vertical scroll boundary -->
</PlaygroundContent>

<PlaygroundContent mode="canvas">
  <!-- free-form canvas or custom viewport ownership -->
</PlaygroundContent>
```

`document` is for forms, indexes, and narrative examples and owns the shell's
vertical content scroll. `fixed` is for table compositions whose runtime owns
the available viewport. `scroll` is for bounded examples such as assembled
DataList recipes that intentionally scroll as one page region. `canvas` is for
an example that deliberately manages its own free layout. The browser body must
remain fixed to the shell; do not combine a mode with negative margins, a second
viewport-sized wrapper, or an implicit `100vh` height.

Spreadsheet fullscreen scenarios may keep `definePageMeta({ layout: 'empty' })`
for route intent, but both playground layouts mount the same `PlaygroundShell`.
The spreadsheet canvas owns the remaining shell viewport (`h-full`), never the
entire browser viewport, so navigation stays consistent across abstractions.

## Recipe for a new sample

1. Choose the owning runtime abstraction and decide whether the sample is a
   document, fixed, scroll-contained, or canvas route.
2. Add a focused page module under `playground/app/pages/`; split variants into
   separate files when comparing behavior would otherwise require a toggle.
3. Keep the demonstrated schema, fixture, and runtime calls in the page or an
   adjacent feature folder under `playground/app/components/`. Extract shared
   data only when it makes the example easier to compare, not when it hides the
   API being assessed.
4. Add navigation metadata to the relevant abstraction in
   `usePlaygroundNavigation.ts`, a concise row to that abstraction's `index.vue`,
   and only a high-level abstraction row to `pages/index.vue`.
5. Add loading, empty, error, disabled, focus, keyboard, responsive, overflow,
   and reduced-motion handling when the example exercises those states.
6. Validate the route in the configured browser at desktop and mobile widths,
   then run the focused playground typecheck and formatter.

## Validation matrix

Before handoff, verify the following for each changed route:

| Surface               | Desktop                                                      | Mobile                                                  |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------- |
| document page         | one document scroll, heading visible, no horizontal overflow | readable line lengths, controls wrap, no clipped labels |
| fixed composition     | shell header plus one runtime viewport, no body scroll       | controls wrap or stack, runtime viewport remains usable |
| scroll-contained page | exactly one internal scroll boundary                         | touch scrolling stays inside the intended region        |
| canvas/fullscreen     | one deliberate canvas boundary                               | close/back action remains reachable                     |
| navigation            | active tree branch, collapse control, keyboard focus         | drawer remains reachable; active hierarchy is preserved |
| color mode            | neutral contrast in light and dark                           | controls retain visible focus and disabled states       |

Focused commands from the repository root are:

```sh
cd playground && bun run typecheck
bunx oxfmt --check playground/app playground/nuxt.config.ts
```

Use the repository-configured browser skill for visible acceptance. Source
inspection or an HTTP 200 response does not prove a route's rendered layout.

## Anti-patterns

- Do not add page-specific playground navigation, duplicate sidebars, or local
  example switchers; the shared collapsible tree is the navigation chrome.
- Do not add global `ui` slot overrides, gradients, broad shadows, or a theme
  control panel to compensate for a page-level layout problem.
- Do not use negative viewport margins, nested `h-screen`/`overflow-auto`
  wrappers, or a body scroll plus an unrelated page scroll.
- Do not wrap every section in `UCard`, nest bordered cards, or generate generic
  equal-card grids for route navigation.
- Do not hide a variant behind a toggle when separate route modules make the
  behavior easier to assess.
- Do not move runtime feature code into the shell or a generic playground
  helper where the example's API usage becomes hard to see.
