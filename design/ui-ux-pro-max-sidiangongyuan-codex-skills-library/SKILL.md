---
name: ui-ux-pro-max
description: Use when designing, implementing, reviewing, or improving web and mobile UI/UX. Consults searchable design data for product patterns, styles, palettes, typography, accessibility, charts, icons, and common frontend stacks.
license: MIT
compatibility: Requires Python 3 to run the bundled design search scripts.
---

# UI/UX Pro Max

Use the bundled search data to make product-specific interface decisions, then
validate the implemented experience. Treat search results as design evidence,
not as a substitute for reading the existing product, audience, and codebase.

## Use this skill when

- designing or refactoring a page, screen, component, navigation flow, form,
  table, chart, design system, or responsive layout;
- choosing or auditing typography, color, spacing, hierarchy, motion, icons,
  interaction states, accessibility, or platform conventions;
- implementing a frontend in a supported stack; or
- diagnosing an interface that feels unclear, inconsistent, inaccessible, or
  visually unfinished.

Skip it for backend-only, infrastructure-only, database-only, or non-visual
automation work. If a change affects how a feature looks, feels, moves, or is
operated, this skill is relevant.

## Workflow

### 1. Understand the product before choosing a style

Inspect the existing interface and code when present. Establish:

- product type and primary user goal;
- audience, usage context, and accessibility needs;
- current design system, component library, icon set, and frontend stack;
- information density, target devices, themes, and required states; and
- brand constraints and the intended visual tone.

Prefer the repository's established patterns over a new visual language unless
the task explicitly calls for a redesign. Operational products should optimize
scanning, comparison, and repeated action; branded or editorial experiences can
support a more expressive composition.

### 2. Generate a design-system recommendation

Start with a multidimensional query: product + industry + tone + density. Run
the bundled script from any working directory by resolving `<skill-dir>` to this
installed skill directory:

```bash
python "<skill-dir>/scripts/search.py" "healthcare operations dashboard calm dense" --design-system -p "Care Console"
```

Use `python3` instead of `python` where that is the available executable. The
result combines product, style, color, landing, and typography data with
reasoning rules and anti-patterns.

Do not apply the first recommendation mechanically. Re-query when it conflicts
with the product, established UI, platform conventions, or accessibility.

### 3. Search only the domains needed for the task

```bash
python "<skill-dir>/scripts/search.py" "keyboard focus error recovery" --domain ux -n 5
python "<skill-dir>/scripts/search.py" "financial trend comparison" --domain chart -n 5
python "<skill-dir>/scripts/search.py" "table virtualization rerender" --stack react -n 5
python "<skill-dir>/scripts/search.py" "data table toolbar" --stack shadcn -n 5
```

Available domains:

| Domain | Use for |
|---|---|
| `product` | Product-specific patterns and reasoning |
| `style` | Visual languages, effects, and anti-patterns |
| `color` | Product and industry palettes |
| `typography` | Font pairings and type-system direction |
| `google-fonts` | Individual Google Font discovery |
| `icons` | Icon families, semantics, and consistency |
| `landing` | Landing-page structure and conversion patterns |
| `chart` | Data relationships, chart types, and libraries |
| `ux` | Accessibility, interaction, responsive, and state guidance |
| `web` | Web and app-interface implementation guidance |
| `react` | React and Next.js performance patterns |

Available stacks are `react`, `nextjs`, `vue`, `svelte`, `astro`, `swiftui`,
`react-native`, `flutter`, `nuxtjs`, `nuxt-ui`, `html-tailwind`, `shadcn`,
`jetpack-compose`, `threejs`, `angular`, `laravel`, and `javafx`.

Use `--json` when another script will consume results. Use `-f markdown` for
human-readable design-system output.

### 4. Persist decisions only when useful

For a multi-page product or a workflow that will continue across sessions:

```bash
python "<skill-dir>/scripts/search.py" "B2B analytics precise compact" --design-system --persist -p "Metrics Hub" --output-dir .
```

This creates `design-system/MASTER.md`. A page-specific call adds an override:

```bash
python "<skill-dir>/scripts/search.py" "B2B analytics settings form" --design-system --persist -p "Metrics Hub" --page settings --output-dir .
```

When implementing a page, read the master first, then
`design-system/pages/<page>.md` if it exists. Page rules override the master
only where they differ. Do not persist generated files unless they belong in
the user's project.

### 5. Turn evidence into a coherent interface

Define a compact decision set before implementation:

- content hierarchy and the primary action;
- layout grid, container behavior, responsive breakpoints, and fixed regions;
- semantic color, typography, spacing, radius, elevation, and motion tokens;
- component states: default, hover/press, focus, selected, disabled, loading,
  empty, error, success, and permission-limited;
- navigation, keyboard, touch, and screen-reader behavior; and
- what must be verified in a browser, simulator, or device.

Use familiar symbols or the existing icon library for standard actions. Use
real product imagery when the user needs to inspect a product, place, object,
person, or state. Avoid decorative visuals that compete with operational work.

### 6. Validate the implementation

Inspect the actual rendered experience, not only source code. Use the relevant
items in [references/quality-checklist.md](references/quality-checklist.md), and
query the bundled data when a rule needs more detail.

At minimum verify:

- representative desktop and mobile widths, including the narrowest supported
  viewport and landscape where relevant;
- keyboard order, visible focus, labels, roles, contrast, reduced motion, and
  enlarged text;
- loading, empty, error, retry, disabled, overflow, and long-content states;
- touch targets, safe areas, fixed-element offsets, and absence of unintended
  horizontal scrolling;
- theme parity when both light and dark modes exist; and
- layout stability, media dimensions, and performance on large lists or data
  views.

For 3D or canvas work, verify that pixels render, the scene is correctly
framed, assets load, motion is active where expected, and controls do not
overlap the scene across supported viewports.

## Priority order

When findings compete, resolve them in this order:

| Priority | Category | Non-negotiable signal |
|---|---|---|
| 1 | Accessibility | Operable and understandable without excluding users |
| 2 | Interaction safety | Reliable targets, feedback, recovery, and confirmation |
| 3 | Information architecture | Clear hierarchy, navigation, and primary task |
| 4 | Responsive layout | No clipping, overlap, hidden content, or accidental scroll |
| 5 | Performance | Stable layout and responsive input |
| 6 | Product fit | Style and density match the domain and audience |
| 7 | Typography and color | Readable, semantic, consistent tokens |
| 8 | Forms and system states | Complete feedback and error recovery |
| 9 | Motion | Meaningful, interruptible, reduced-motion compatible |
| 10 | Polish | Icons, charts, spacing, and details reinforce the system |

Visual novelty never outranks comprehension, accessibility, or task success.

## Output expectations

For a design task, return the chosen direction, key tokens and interaction
decisions, component or page structure, and validation plan. For an
implementation task, make the scoped code changes and report the tested states
and viewports. For a review, lead with concrete findings tied to the rendered UI
or code and separate blocking usability problems from optional polish.

Do not present database recommendations as universal rules, invent brand
requirements, or claim a UI is verified without inspecting the relevant
rendered states.
