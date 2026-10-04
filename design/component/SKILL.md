---
name: component
description: Builds and audits reusable presentational UI components in Storybook — props in, events out, no fetching, routing, global state, or domain types. Designs minimal prop APIs (controlled/uncontrolled, ref forwarding, native prop passthrough), enumerates visual variants and interaction states, writes stories per variant and per state plus interaction stories with play functions, and audits components for business-logic leaks, API smells, and missing story coverage. Use when authoring a presentational component, organizing Storybook stories, refactoring a prop API, extracting logic out of a UI primitive, or auditing a component library. Triggers on "storybook", "story", "presentational component", "dumb component", "ui component", "reusable component", "component api", "component props", "component variants", "component states", "controlled component", "extract logic", "business logic in component", "ref forwarding", "play function", "interaction story", "component audit".
---

# Component Engineer

Build presentational components that render pixels from props and emit events. Nothing else.

## Mode router

| Mode | Use when | Output |
|------|----------|--------|
| **Author** | A new component is needed | File scaffold, prop API, variant matrix, state plan, story plan |
| **Audit** | An existing component or library needs review | Severity-ranked findings with `file:line` |
| **Stories** | A component lacks coverage | Story file with default + variant matrix + per-state + interaction stories |

If the mode is ambiguous, ask.

## How components are built in this library

Every component in `react-basics-ui` follows the same shape. Match it — the
generic guidance further down is the *why*; this is the *how, here*.

### Folder layout

Components live under `src/components/<category>/`, with `forms/` further split
into `inputs/ selection/ date-time/ advanced/ structure/`. A folder holds:

```
Button/
  Button.tsx          root component — forwardRef + memo
  Button.types.ts     props and unions (the public type surface)
  Button.styles.ts    class-map constants (BASE_CLASSES, SIZE_STYLES, …)
  ButtonBase.tsx      shared internals, when siblings need them
  ButtonGroupContext.ts   context, when a compound part needs it (.ts, no JSX)
  Button.stories.tsx  CSF3 stories
  Button.test.tsx     behaviour tests (see /test for the suffix conventions)
  index.ts            the public barrel for this folder
```

Then export the folder from the category barrel (`src/components/forms/index.ts`),
which the root `src/index.ts` re-exports. Everything ships from the package root.

### Building blocks to reach for first

| Need | Use | Where |
|---|---|---|
| Merge class strings | `cn()` | `@/lib/cn` |
| Compound-component context | `createComponentContext()` | `@/lib/createComponentContext` |
| Controlled/uncontrolled value | `useControlledState` | `@/hooks` |
| Merge a forwarded ref with a local one | `useMergedRefs` | `@/hooks` |
| Stable form/aria ids | `generateFormId` | `@/lib/generateFormId` |
| Focus ring, disabled, transition classes | `FOCUS_RING`, `DISABLED_CLASSES`, `TRANSITION_COLORS` | `@/components/shared/styles` |
| Shared prop contracts | `ComponentSize`, `GranularSize`, `OverlaySize`, `StatusVariant`, `AlertVariant`, `SelectOption` | `@/components/shared/types` |

Six `Base*` primitives already carry the hard parts — **compose, don't
re-implement**: `BaseInputField` (input chrome, tone, slots), `BaseSelectionControl`
(checkbox/radio/switch mechanics), `BaseOverlayDialog` (portal, focus trap, scroll
lock, escape), `BaseCardContainer`, `BaseText`, `BaseAlertBox`.

### Size and tone scales — use the shared unions

This library does **not** use `"sm" | "md" | "lg"` for component sizes. Import
the canonical scale instead of inventing one:

```ts
import type { ComponentSize } from '@/components/shared/types/size';
// ComponentSize  = 'small' | 'default' | 'large'   ← form controls, buttons, badges
// GranularSize   = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'  ← icons, avatars, spinners
// OverlaySize    = 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full' ← modals, drawers
```

### Composition patterns in use

- **`forwardRef` + `memo`** on essentially every component (143 and 154 files respectively).
- **Compound components via `Object.assign`** (28 components): `export const Card = Object.assign(CardRoot, { Header, Content, Footer })`.
- **Context via `createComponentContext`** (26 components) rather than hand-rolled `createContext` + null checks.

### Story titles

`meta.title` is `'<Category>/<Component>'`, matching the folder category:
`Forms/`, `Data Display/`, `Layout/`, `Overlays/`, `Navigation/`, `Feedback/`,
`Typography/`, `Utility/`, `Theme/`. Nested form folders still title as `Forms/X`.
Keep the title in step with the folder — a drifting title makes the Storybook
sidebar disagree with the source tree.

## The contract

A presentational component must:

- Take props and render. Emit events for state changes the parent owns.
- Be deterministic — same props → same output.
- Reference named visual tokens, not raw values.
- Meet a keyboard-and-screen-reader baseline.
- Render correctly without context providers it does not itself supply.

It must not:

- Fetch, mutate, subscribe, or poll.
- Read from a router, store, query client, or auth context.
- Import domain types or models. Nothing in `src/components` may know about a consuming application.
- Hold business rules — it does not know *why* it is being used.
- Read environment, time, or random sources unless an explicit prop opts in.

## Component API design

Apply each rule when shaping the public API.

| Rule | Reason |
|------|--------|
| Prefer `children` or named slots over `items` arrays | Composition keeps the API small as needs grow |
| Pick controlled *or* uncontrolled; if both, pair `value` + `defaultValue` (and `onChange`) | Mixed conventions cause double-source-of-truth bugs |
| Variants are discriminated unions, not parallel booleans | `tone="danger"` beats `isDanger + isWarning` that can collide |
| Sizes and tones are enums from `shared/types`, not numbers or ad-hoc strings | Numbers leak implementation detail; ad-hoc scales fragment the library |
| Forward refs on inputs, buttons, and anything a parent may focus, scroll to, or measure | Ref access is a public contract |
| Spread remaining native HTML props through to the underlying element | Consumers need `aria-*`, `data-*`, `id`, `onBlur`, etc. without re-declaring each |
| Default to required props; opt into optional only when there is a real default | "Optional with no default" is a hidden invariant |
| Cap props at ~12; past that, decompose into sub-components | A swollen API signals a component doing two jobs |

### Sub-components vs monolithic

Expose sub-parts (`Dialog.Header`, `Dialog.Footer`) when consumers legitimately rearrange the parts. Otherwise keep a single closed surface — sub-components are public API and cost more to evolve.

## State coverage

Every interactive component addresses each applicable state. Mark N/A explicitly.

| State | Question |
|-------|----------|
| Default | Resting state with normal props? |
| Hover | Cursor over (or none, for touch-only)? |
| Focus-visible | Keyboard focus ring? |
| Active / pressed | Mid-click / mid-touch? |
| Disabled | Affordance shows *why* unavailable? |
| Loading | Async action in flight — what is reversible, what is not? |
| Error | Validation or async failure — message location, role="alert" semantics? |
| Success | Post-action confirmation? |
| Empty | No data / placeholder content? |
| Read-only | Same shape, no edit affordance, not styled as broken? |
| Indeterminate | Tri-state controls (checkbox, progress)? |
| Selected | Item is part of a selection set? |

## Style discipline

Components must not contain raw hex, rgb, hsl, px values, font families, or magic durations. Reference named tokens. If a needed token does not exist, propose a name and surface it as an Open Question — do not hardcode the value and move on.

## Accessibility baseline

- Correct semantic element first; ARIA only to fill gaps the element cannot.
- Role, accessible name, and value verifiable from the rendered DOM.
- Keyboard reachable; Tab order matches visual order; focus-visible ring is a token.
- Hit target ≥ 44×44 logical pixels for primary interactive elements.
- No information by color alone — pair with icon, text, or shape.
- Honor reduced-motion: non-essential motion is suppressed, not just slowed.
- Status changes from async actions announce via live region or moved focus.

## Storybook stories

### One story file per component

Co-locate the story file beside the component. `meta.title` is `'<Category>/<Component>'` matching the folder category (e.g. `Forms/Button`, `Data Display/Table`).

### What to write

| Story type | When | Notes |
|------------|------|-------|
| **Default** | Always | Canonical use with realistic args |
| **Variants matrix** | Per variant axis (size, tone, density) | One story per axis, or a single story rendering the matrix |
| **State** | One per state from the coverage table | Story name = state name |
| **Interaction** | One per behavior (open, submit, navigate keys) | Use `play` with `userEvent` + `expect` |
| **Edge content** | Long strings, RTL, narrow widths, dense data | Catches layout fragility |

### Story shape

- `args` define defaults users tweak via controls.
- `argTypes` constrain controls — disable controls for props that should not be tweaked.
- `parameters.a11y` enables the a11y addon and turns rules on for the component's pattern.
- `parameters.docs.description.story` gives one-sentence intent per story.
- Mock everything the component would not have in production — but if the component needs mocks to render, that is a business-logic leak. Fix the component, not the story.

### What does *not* belong in stories

- Real network calls. Real router. Real auth.
- Application-specific theme wrappers — register the theme in `.storybook/preview.ts` once.
- Snapshot tests masquerading as stories — stories are documentation + interactive playground; assertions live in `play` or sibling test files.

## Audit dimensions

Run in order. Each finding: location, observation, impact, suggestion.

### 1. Business-logic leaks

Search the component file for imports and calls that signal non-presentational behavior:

```bash
grep -nE "useQuery|useMutation|useSwr|useRouter|useNavigate|useStore|useSelector|useDispatch|fetch\(|axios|/api/|features/" <component>
```

Each hit moves out. In a library there is no container layer to hide it in — either lift it to a prop/callback the consumer supplies, or extract it into a co-located hook that takes plain arguments.

### 2. State coverage gaps

For each component, confirm a story exists per applicable state. Missing states are findings.

### 3. Token leaks

```bash
grep -nE "#[0-9a-fA-F]{3,8}\b|rgb\(|hsl\(" <component>
grep -nE "(padding|margin|gap|font-size|line-height|border-radius)\s*:\s*[0-9]" <component>
```

Each hit: replace with a token, or — if no token exists — propose one.

### 4. Prop API smells

| Smell | Fix |
|-------|-----|
| Parallel booleans that can collide (`isPrimary`, `isDanger`, `isGhost`) | Single discriminated union prop |
| > 12 props | Decompose into sub-components or compose primitives |
| Optional props with no defined default | Make required or document the default |
| Same concept named differently across siblings (`open` vs `isOpen` vs `visible`) | Pick one and align the library |
| Props that take JSX *and* objects for the same slot | Pick one shape per slot |

### 5. Reachability

- Native HTML props pass through? (Ref a small test: does `aria-label`, `data-*`, `id`, `onBlur` reach the underlying element?)
- Refs forward? (Try wrapping in a focus-management helper.)

### Severity

- **Critical** — component cannot be reused (business-logic import, broken keyboard path, no focus ring, missing role).
- **High** — state gap a real user hits; visible token drift; API collision.
- **Medium** — polish gap, naming inconsistency, missing edge-content story.
- **Low** — taste call.

## Author workflow

1. **Justify existence.** Why does no existing primitive (or composition of primitives) satisfy this?
2. **Define the API.** Props table with types, defaults, and notes. Events with payloads. Slots. Refs.
3. **Enumerate variants.** Size × tone × density (whatever axes apply).
4. **Cover states.** Walk the State Coverage table; mark each applicable or N/A.
5. **A11y contract.** Role, keyboard map, focus behavior, announcements.
6. **Tokens.** Name every visual token the component consumes; flag any that need to be added.
7. **Story plan.** Default, variants matrix, one story per state, interaction stories per behavior, edge-content story.
8. **Open questions.** Tag `[blocker]`, `[clarify]`, `[nice-to-have]`.
9. **Definition of Done.** Label the spec **Ready / Iterate / Blocked**.

## Definition of Done

Apply at the end of every mode.

```
- 0 business-logic imports in the component file
- 0 raw hex / rgb / hsl / px values
- 1 story per applicable state + 1 per variant axis
- ≥ 1 interaction story per public behavior
- A11y addon clean on every story (or known violation explicitly waived with rationale)
- Ref forwarded; native props spread through
- Public API typed and exported; defaults documented
```

If any item fails, label **Iterate** and list the gap. If a blocker is unresolved, label **Blocked**.

## Output templates

### Component spec

```
# Component: <Name>

## Why this exists
<Reuse walk-through — what was tried, why it didn't fit>

## API
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| ... | ... | ... | ... |

Events: <list with payloads>
Slots: <list>
Ref: <forwarded to which element>

## Variants
- size: sm | md | lg
- tone: neutral | success | danger | ...
- density: comfortable | compact

## States
<one row per applicable state with visual + behavior + a11y note>

## A11y contract
- Role: ...
- Keyboard: ...
- Focus: ...
- Announcements: ...

## Tokens consumed
- color: ...
- spacing: ...
- typography: ...
- radius / shadow / motion: ...

## Story plan
- Default
- Variants matrix: <axes>
- States: <list>
- Interactions: <list with what each play() asserts>
- Edge content: <list>

## Open questions
1. [blocker] ...
2. [clarify] ...

## Status
**[Ready / Iterate / Blocked]**
```

### Audit report

```
# Component Audit: <name or directory>
> Files examined: <clickable paths>

## Findings

### <Dimension>
**[Severity] — <title>**
- Location: file:line
- Observation: <what is there>
- Impact: <what a consumer or end user notices>
- Suggestion: <concrete change>

[repeat per finding, grouped by dimension]

## Summary
| Severity | Count |
|----------|-------|
| Critical | N |
| High     | N |
| Medium   | N |
| Low      | N |

## Status
**[Ready / Iterate / Blocked]**
```
