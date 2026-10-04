---
name: lesson-animations
description: Design and build animations that make a lesson topic genuinely easier to understand — visual, moving explanations of the core idea (not decoration), authored as reusable React islands using the project's motion tokens and always respecting prefers-reduced-motion. Use when authoring a lesson that has a process/relationship/transformation worth showing, or when the user asks to "animate X", "add a visual", "make it move", or "explain this with an animation".
---

# Animations that teach

Every lesson should include animations that explain the topic **better than text
or a static image could**. Animation is a teaching tool here, not decoration — if
it doesn't increase understanding, don't add it.

**More, not one**: aim for an animation at *each* major
transformation/process/relationship in the lesson, placed next to the
explanation it illustrates — not a single hero animation per lesson.

## When an animation earns its place

Animate when the idea is about **change over time, a process, or a relationship**:
- a process with steps (a lifecycle, a recipe, a sorting pass)
- a transformation (input → output, before → after)
- a relationship where moving one knob changes another (turn one dial, watch
  another respond)
- accumulation / growth / decay

If the idea is a static fact or definition, use a `Callout`, diagram, or
`MatchConcepts` exercise instead.

## How to build it (reusable island)

**The template ships no subject-specific animation islands** — the chart/visual
islands are something *you build* for your topic. The generic building blocks
below exist; the moving explanation of *your* concept does not yet, so author it.

Author animations as React islands in `src/components/react/` and follow the
**same rules as every component** (see `exercise-components`): barrel export,
`@` alias + `cx`, design tokens only, JSDoc'd props, `bun run check` clean.
Prefer an **interactive** island (user scrubs a slider / steps through) over a
passive loop — interaction cements understanding.

Generic building blocks already in the project (`@/components/react`):

- **`MindMap`** — the **chunking close**. End each lesson with a learner-facing
  "big picture" mind map (Mermaid `mindmap`) that links the section concepts into
  one structure, so the learner *chunks* the lesson instead of reading a passive
  summary. Author it as structured data — the component renders both the diagram
  and an accessible text outline from the same tree:

  ```mdx
  import { MindMap } from '@/components/react';

  <MindMap
    client:visible
    title="The lesson in one picture"
    root={{
      label: 'Core idea',
      children: [
        { label: 'First concept', children: [{ label: 'Why it matters' }] },
        { label: 'Second concept', children: [{ label: 'How it connects' }] },
        { label: 'Third concept', children: [{ label: 'Common trap' }] },
      ],
    }}
  />
  ```

  Spanish twins translate `title`/`caption`/`eyebrow`/`outlineLabel` and every
  node `label`. Keep node labels short — Mermaid mindmap strips `()[]{}:` etc.
- **Motion tokens** in `src/styles/global.css`: `animate-fade-up`, `animate-float`
  (Tailwind: `animate-fade-up`, `animate-float`). Add new `@keyframes` + an
  `--animate-*` token there if you need more — never inline hard-coded hex or
  one-off CSS in a component.
- **`Reveal`** — to animate an element in on scroll. (For a discrete sequence of
  stages, author a numbered Markdown list — there is no `StepThrough`.)
- Plain React state + CSS transitions / SVG for custom interactive visuals
  (sliders driving a value, an animated SVG graph, a canvas).

## Non-negotiables

1. **Accessibility / motion safety.** Wrap motion in
   `@media (prefers-reduced-motion: reduce)` (the project already does this
   globally in `global.css`) — provide a static, equally-informative fallback.
   No essential information conveyed by motion alone.
2. **Performance.** Animate `transform`/`opacity`, not layout properties. Keep
   islands light; hydrate with `client:visible`.
3. **Labeled & controllable.** Interactive controls are real, keyboard-operable
   inputs with labels and visible focus rings; loops should be calm and not
   distract from reading.
4. **Tokens & alias only.** Tailwind design tokens, `@` imports, `cx` helper.

## Wire it into the lesson

```mdx
import { Reveal } from '@/components/react';
// or the custom island you authored for this topic, e.g.:
import { ConceptPlayground } from '@/components/react';

<ConceptPlayground client:visible />
```

(`ConceptPlayground` is illustrative — the kind of interactive visual you would
build for your subject. No such island ships with the template; you create it.)

Add Spanish label props in the `es` twin. Then `bun run check` and regenerate OG.
