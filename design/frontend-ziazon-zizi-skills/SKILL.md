---
name: frontend
description: >
  Use for frontend STRUCTURE and behavior — organizing components, state, and data
  access (typed service layer, stores, thin components), building list/table/filter
  views, forms, and modals, loading/empty/error UX, routing/nav, SSR/public pages,
  and web performance. Invoke whenever building or refactoring UI, adding any
  new screen (a page, a data table, a filter, a form, a modal), or making
  component/state/perf/UX decisions. Centered on Vue 3 + vanilla Tabler today, but
  the approach is framework-agnostic. Do NOT use for Tabler component specifics or
  Vue 3 workarounds ("which Tabler class/JS component, and does it fight Vue?") —
  that's tabler-ui; do NOT use for visual/aesthetic judgment (color, typography,
  spacing) — that's design-guide; do NOT use for which content belongs on which
  page, or how nav is labelled and grouped — that's information-architecture (this
  skill builds the routing, IA draws the map). These often apply to one task; this
  skill owns the structural and behavioral side.
---

# Frontend

Goal: build well-structured, performant, good-UX frontends, and learn the user's
preferences (component styles, layouts, patterns) over time so future work matches taste.

## Step 1 — route to the reference file(s) and READ them first

The real content of this skill lives in topic reference files (indexed in
`LEARNINGS.md` beside this skill, when your copy keeps one). Pick by task — reading the
wrong-or-no file is how established conventions get reinvented badly:

| Task involves… | Read first |
| --- | --- |
| Any list/table view — building, altering, or filtering one | The project's list/table reference — the shared table/list component's rules, operator filtering, row actions, async list states |
| A new service/endpoint wire-up, types/enums, stores, persistence, routing/nav, legacy-UI migration | The project's architecture reference — service layer, shared-types traps, the storage helper, route/nav conventions |
| Public pages, SEO, or anything server-rendered | The project's SSR/public-pages reference — SSR foundation, client-only libs, the SPA-vs-SSR local-testing split |
| Field placement, permissions/edit surfaces, modal-vs-page, icons, maps, taste | The project's UI/UX reference — includes the light+dark verification rule |
| Performance / Lighthouse / SEO scores | [web-performance.md](web-performance.md) — `scripts/lh-audit.sh` + the ordered remediation playbook |
| A stack other than the primary Vue 3 + Tabler one (e.g. R/Shiny) | [other-stacks.md](other-stacks.md) |

Keep one project reference file per topic beside this skill, named for the project and
topic, and route to it from this table. This install's project files are listed in
`LOCAL.md` beside this skill, when your copy keeps one — *Project reference files*.

Also check the sibling skills when the task touches their territory: **tabler-ui**
(component exceptions — always, before using any Tabler interactive component) and
**design-guide** (color/type/spacing decisions).

## Step 2 — mirror the codebase before inventing

Read neighboring components/services/stores for the feature area first. The bar is
"indistinguishable from the code around it" — a parallel pattern (a second modal style,
a hand-rolled localStorage helper, a bespoke table) is a review reject even when it works.

## Step 3 — structure the change

- **Layered data access:** API calls in a typed service class, state in stores,
  components thin — raw HTTP in a component leaks untyped, untestable coupling.
- **Reusable, prop-driven components:** one component parameterized by props (e.g. an
  add/edit modal switched by an optional id) over near-duplicates, so fixes land once.
- **Performance:** lazy-load heavy/rare views, code-split by route, keep large lists
  paginated/virtualized, memoize derived data, and watch bundle size when adding a
  library — each avoids shipping cost to every user for a minority feature.
- **UX:** loading, empty, AND error states for every async surface (the error branch is
  the one that gets forgotten — see the data-tables file); inline validation feedback;
  don't block the whole view on one slow call.

## Step 4 — verify (hard gates, not suggestions)

1. **Light AND dark mode.** Tabler theming means a change can look perfect in one and
   broken in the other (contrast, hardcoded colors, theme-reactive re-renders). Toggle
   both before showing anything.
2. **Built output when class names are composed dynamically.** If the production build
   runs PurgeCSS (or a Tailwind-style content scan), a runtime-composed class
   (`` `btn-${x}` ``) passes dev and unit tests but ships unstyled in prod. Any dynamic
   class composition → verify against the built (SSR) output (see tabler-ui's PurgeCSS
   exception; this install's build: `LOCAL.md` beside this skill, when your copy keeps
   one — *Built output and PurgeCSS*).
3. **Show the UI as inline screenshots.** The user reviews visuals, not prose — render
   the change (component harness or full stack) and screenshot it, both themes.
4. Run the project's checks: lint (e.g. oxlint) + build are enforceable; when the main
   branch is already red under the type-checker (vue-tsc), the bar is "no NEW errors in
   my files" (this install's baseline: `LOCAL.md` beside this skill, when your copy keeps
   one — *Checks baseline*).
5. **Gate with PARALLEL vitest, the way CI runs it** (plain `vitest run` — never
   `--no-file-parallelism` as the merge gate). A services↔stores barrel import cycle
   only threw when the module graph was entered service-first, i.e. under CI's parallel
   run, and stayed invisible to every local serial run.
6. **"The page renders" is not evidence a FORM is usable.** A render check proves the
   route mounted; it says nothing about whether the field accepts input, validates, or
   submits. Exercise the interaction.
7. **A CSS fix that "looks right" is unverified — A/B it against the DOM.** Confirm the
   rule you added is the one taking effect (computed styles, or toggle it off and back)
   rather than inferring causation from the screenshot having changed.

## Reactivity and layout traps

Each of these ships a green build and a plausible-looking screenshot.

- **Post-auth pages must be REMOUNT-SAFE.** Adopting a session re-registers routes,
  which **remounts** the page — a guard reading state that `onMounted` had just cleared
  bounced a *successful* booking back to the start, and state handed via
  `router.replace(…, { state })` arrived empty after the same remount. Assume any
  post-auth view mounts more than once.
- **Aggregates must not be derived from the loaded page.** A total computed from the
  rows currently in memory silently becomes "total of page 1". Derive it from the
  source, not the slice you happen to be rendering.
- **A composable with an `immediate: true` watcher runs BEFORE its own `const` is
  assigned** — the watcher fires during setup, hitting the temporal dead zone of the very
  binding it references. Guard it, or drop `immediate`.
- **Vue auto-casts `v-model` on `type="number"`** — the model holds a *number*, so
  calling a string method on it throws at runtime while the template looks fine.
- **Money formatters must normalise negative zero at the boundary.** Negating a zero sum
  yields JavaScript's `-0`, which `Intl.NumberFormat` renders as **`-$0.00`**. Normalise
  where the value is formatted, and test the zero/empty case explicitly.
- **Vue scoped CSS reaches a CHILD component's ROOT element** — a scoped rule on the
  parent styles the child's root, which makes `display: contents` on that root a foot-gun
  (the element vanishes from the box tree while still matching the selector).
- **A flex/grid item's automatic minimum size silently defeats its own basis** — the
  default `min-width: auto` refuses to shrink below content, so a `flex-basis` or `1fr`
  track that should compress simply doesn't. Set `min-width: 0` (or `min-height: 0`).
- **A stubbed `Teleport` can silently stop repatching attributes inside it**, so a test
  that stubs it stops observing updates the real component would make.

## Common failure modes

- **Hand-rolling a `<table>` for a data list** — if the app has a shared data-table/list
  component, every tabular list goes through it. Stop and read the project's list/table
  reference (this install's: `LOCAL.md` beside this skill, when your copy keeps one —
  *Data tables and shared types*).
- **Importing a backend-shared workspace types package's runtime values (enums) in the
  frontend** — when that package carries decorator metadata (reflect-metadata /
  class-transformer), a value import white-screens the app at boot. Type-only imports
  only; redefine enums locally.
- **Testing only in light mode / only in dev mode** — dark-mode-only and prod-only
  breakage are both established bug classes in Tabler apps (carousel desync, PurgeCSS stripping).
- **`.filter((item) => item.condition)` on action-menu items** — filtering on the
  function *reference* (always truthy) instead of calling it; shows every action
  regardless of permission. Invoke the condition.
- **Skipping loading/error branches on a new fetch** — a swallowed failure renders a
  misleading "no data" empty state.
- **Writing `wrapper.get(x).exists()` in a spec** — recorded **four separate times**,
  which is why it is here rather than in the journal. `get()` already throws when the
  element is missing, so `.exists()` is both redundant and a **vue-tsc type error**. Use
  `find(x).exists()` to assert presence, or `get(x)` alone when you need the element.
- **Deriving a landing page from the user's "highest" role** — render additively
  instead; picking a winner hides surfaces a multi-role user is entitled to.
- **Showing shared data on a multi-tenant "all" view without labelling its owner** —
  correct rows, unattributable to a person, read as someone else's data.

## Before you call this done

- [ ] Read the routed reference file(s) and matched the existing convention.
- [ ] Async surfaces have loading + empty + error states.
- [ ] Verified in BOTH light and dark mode.
- [ ] If any class name is composed at runtime: verified against the BUILT output.
- [ ] Inline screenshots shared for anything visual.
- [ ] Lint + build green; no new vue-tsc errors in changed files.

## Related skills

- [plain-language](../plain-language/SKILL.md): the words inside empty, loading and error states, and every other UI label.

## Capturing learnings

Accumulate frontend conventions and the user's taste as you go, in the learnings files. The
corpus is split by topic, indexed from `LEARNINGS.md` beside this skill, when your copy keeps
one (the table in Step 1 mirrors it). At the end of a session, when asked to update the
skills, or after frontend work: record structural conventions, component patterns that
worked, performance/UX decisions, and any referenced layouts/styles the user liked (and why)
into the most relevant reference file — dedupe/merge, tag by stack. When the user shares a
layout/site they like, record what about it appeals (structure, density, interaction). If a
file outgrows ~250 lines, split it further by topic behind a slim index (this install's
split rule: `LOCAL.md` beside this skill, when your copy keeps one — *Capturing
learnings*).
