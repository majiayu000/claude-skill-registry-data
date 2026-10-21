---
name: ui-ux-craft
description: "Build or redesign polished React and Next.js interfaces by selecting and composing shadcn/ui, shadcnblocks, Beautiful UI, AI SDK Elements, beUI, Rare UI, Transitions.dev, Magic UI, and Aceternity UI without turning the product into a mismatched component collage. Use for UI/UX implementation, landing pages, dashboards, AI chat or agent interfaces, component-library selection, interaction design, animation, visual polish, responsive design, and accessibility QA."
---

# UI/UX Craft

Create a coherent product interface, not a catalog demo. The named libraries
are sources, not requirements: choose only the sources that serve the product's
visual direction, interaction model, stack, and accessibility contract.

Before selecting a source, read
[`references/source-catalog.md`](references/source-catalog.md). Revisit the
official page linked there whenever component names, install commands,
dependencies, licenses, or paid/free boundaries matter.

## Required outcome

The finished interface must:

1. fit the existing product and framework;
2. have one clear visual direction;
3. use a small, explicit component-source stack;
4. preserve semantic HTML, keyboard operation, focus visibility, and reduced
   motion;
5. cover responsive and non-happy-path states;
6. pass the repository's checks and real browser QA.

Do not stop at a mockup, plan, or dependency install when the user asked for
working UI.

## Phase 0: inspect before choosing

Read the current implementation and establish:

- framework, React version, Tailwind version, package manager, and build tool;
- existing `components.json`, aliases, CSS variables, tokens, fonts, icons,
  primitives, and animation dependencies;
- route boundaries, server/client component boundaries, and data states;
- existing visual language worth preserving;
- the user's reference, audience, task, content density, brand constraints,
  and accessibility requirements.

If a concrete reference exists, treat it as the visual contract. If it does
not, state one concise design direction before implementation: product mood,
type character, color strategy, spacing rhythm, surface treatment, and motion
principle.

Do not migrate frameworks, replace the design system, or introduce a new
animation runtime merely to use a preferred library.

## Phase 1: assign source roles

Choose by role. A source may fill more than one role only when that reduces
dependencies and keeps the result coherent.

| Role | Default choices | Use when |
|---|---|---|
| Foundation | shadcn/ui or existing primitives | Forms, dialogs, menus, tables, navigation, feedback, and other behavior-heavy controls |
| Page structure | shadcnblocks or custom composition | Marketing sections, auth shells, pricing, settings, dashboards, and page-level scaffolding |
| AI product domain | AI SDK Elements or Beautiful UI | Streaming chat, messages, reasoning, tools, attachments, approvals, tasks, and agent status |
| Product motion | Transitions.dev or beUI | State changes, spatial continuity, feedback, and component-level interaction |
| Visual accent | Rare UI, Magic UI, or Aceternity UI | One or two high-salience moments such as a hero, spotlight, background, marquee, card, or reveal |

### Selection rules

- Prefer the repository's existing primitives over adding an equivalent.
- Use **shadcn/ui** as the behavioral foundation when no foundation exists.
- Use **shadcnblocks** for page composition, then rewrite copy, spacing,
  hierarchy, and tokens so the result belongs to the product.
- Choose **AI SDK Elements** for functional AI chat composition and
  **Beautiful UI** for crafted AI-agent states. Combine them only when each has
  a distinct responsibility.
- Choose **Transitions.dev** for transition behavior and **beUI** for a
  source-owned animated component. Do not stack competing motion systems on
  one interaction.
- Choose at most one dominant accent family among **Rare UI**, **Magic UI**,
  and **Aceternity UI** per surface.
- A normal screen should use no more than three external source families:
  foundation, domain or structure, and motion or accent. Exceed this only when
  every source has a non-overlapping role recorded before implementation.
- Never select a component because it is visually impressive in isolation.

## Phase 2: write the composition contract

Before code changes, record a compact contract in working notes or the
repository's design document:

```text
Direction: <one sentence>
Foundation: <existing system or shadcn/ui>
Structure: <custom or source and exact sections>
Domain: <source and exact product states>
Motion: <purpose, trigger, duration class, reduced-motion behavior>
Accent: <single focal treatment or none>
Rejected: <tempting alternatives and why they do not fit>
```

Define shared tokens before adapting copied components:

- semantic color roles rather than component-specific hex values;
- type scale and line lengths;
- spacing and layout grid;
- radii, border, shadow, and elevation policy;
- motion durations, easing, distance, and reduced-motion substitutions.

## Phase 3: source safely

For every selected external component:

1. open the official component page;
2. verify its current install or copy path;
3. inspect dependencies, client-component requirements, CSS, assets, and
   license or paid access;
4. compare it with existing components to avoid duplication;
5. install only the exact component and dependencies needed;
6. treat copied source as product code: rename, simplify, type, theme, test,
   and maintain it locally.

Never invent a registry URL, component name, import path, CLI command, or API
from memory. Never copy code from unofficial aggregators when the original
source is available. Do not conceal provenance: retain required notices and
report the source pages used.

## Phase 4: implement product behavior

Work from low-level behavior to high-level polish:

1. semantic structure and data states;
2. accessible primitives and keyboard interactions;
3. responsive layout and content hierarchy;
4. product tokens and source-component adaptation;
5. transitions that explain state or space;
6. one restrained focal accent;
7. final copy, truncation, overflow, and localization handling.

Every interactive surface must define the applicable states:

- default, hover, focus-visible, active, selected, and disabled;
- loading, streaming, success, empty, error, and retry;
- open/closed or expanded/collapsed;
- narrow mobile, typical desktop, and wide desktop;
- light and dark when the product supports both;
- reduced motion.

Motion must explain space, confirm input, show state, or soften a change. Keep
frequent interactions fast; reserve expressive animation for infrequent,
high-salience moments. Prefer opacity and transform, avoid layout-thrashing
effects, and remove movement that has no product purpose.

## Visual quality bar

- Establish hierarchy through scale, spacing, contrast, and composition before
  decoration.
- Let one element lead; not every card, heading, and button can be the hero.
- Use intentional asymmetry or rhythm where it supports the concept, but keep
  repeated product controls predictable.
- Replace demo gradients, placeholder copy, generic icons, stock imagery, and
  default palettes with product-specific decisions.
- Avoid the recognizable AI-generated collage: excessive rounded cards,
  nested glass panels, purple-blue gradients, glowing borders everywhere,
  floating blobs, gratuitous marquees, and motion on every element.
- Keep decorative layers non-interactive and invisible to assistive
  technology.

## Verification gate

Run the repository's relevant type check, lint, tests, and production build.
Then use the real browser surface and verify:

- target route loads without console or hydration errors;
- primary flow and one invalid/error flow work;
- keyboard-only traversal, focus order, Escape behavior, and focus return;
- labels, names, roles, contrast, hit targets, and screen-reader semantics;
- mobile and desktop layout, overflow, long content, empty content, and zoom;
- reduced-motion behavior and absence of autoplay distraction;
- loading and streaming behavior without layout jumps;
- no unnecessary dependency, duplicate primitive, oversized asset, or
  expensive animation entered the bundle.

For visual changes, capture and inspect the actual rendered surface. A clean
build without browser use does not complete the task.

## Completion report

Report:

- design direction;
- selected sources and each source's unique role;
- important source components and official URLs;
- states and responsive behavior implemented;
- automated checks and browser scenarios observed;
- any paid asset, license condition, or source not used and why.
