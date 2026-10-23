---
name: cinematic-web-director
description: Design, build, critique, or polish cinematic websites with a product-specific visual world, semantic tokens, purposeful motion, responsive behavior, and real browser verification. Use for landing pages, product stories, resource libraries, galleries, decks, scroll scenes, video scrub pages, Spline pages, and other frontend work that must feel authored rather than generated.
---

# Cinematic Web Director

Build a distinct page, not a reskinned template.

## 1. Load the truth

Before editing:

1. Read `PRODUCT.md` and `DESIGN.md` when present.
2. Inspect the target page end to end.
3. Inspect one representative source of visual authority: a live page, token file, shared component, stylesheet, or approved asset.
4. Trace existing motion and media behavior before replacing it.

A missing `DESIGN.md` does not make an established product greenfield. Preserve a coherent identity already present in production unless the user asked for a redesign.

## 2. Name the surface mode

Choose the mode from this surface:

- **Persuade** — the visitor decides and acts.
- **Operate** — the visitor completes a task.
- **Read** — the visitor understands material.
- **Experience** — the visitor enters the work itself.

Write the mode down before choosing the composition. A tool's landing page is Persuade; its dashboard is Operate; its guide is Read.

## 3. Set the direction

Resolve the smallest useful brief:

- user and desired outcome
- primary action
- real proof or assets
- concrete visual world
- category default to avoid
- anti-references
- color strategy
- type character
- material and composition
- one signature interaction

Do not ask for arbitrary CSS values. Ask what would change the direction.

When the project has no context files, create the compact versions from `docs/project-context.md` if the task includes establishing or replacing the visual system. A narrow refinement may proceed from the incumbent implementation.

## 4. Climb the implementation ladder

Use the lightest renderer that carries the idea:

1. Existing pattern in the repository.
2. CSS transforms, masks, clip paths, and layout.
3. Existing dependency.
4. Spline or video for authored media.
5. Frame sequence for exact cinematic playback.
6. Three.js or WebGL only for live geometry, lighting, or manipulation.

Keep content, theme, scene, and motion separate. Prefer the public `ds-*` token and module APIs for new work. Use `aigent-*` compatibility APIs only when preserving an AIgent-branded page.

## 5. Taste floor

The brief may earn any visual device. Your habit does not.

By default, refuse:

- an identical card grid as the page scaffold
- cards nested inside cards
- an eyebrow above every heading
- numbered sections without a real sequence
- gradient text
- glass without valuable content behind it
- pure black or arbitrary gray when the visual world has a tint
- mono used as a generic technical costume
- a random floating 3D object
- glow that does not represent emitted light or active state
- bounce or elastic easing
- one identical fade-up applied to every section

Prefer:

- one dominant focal point per chapter
- rules, spacing, and lists before another container
- body measure near 65–75 characters
- more space between groups than inside them
- explicit focus states and real semantic controls
- one authored motion moment with quiet supporting transitions
- product-specific copy and proof in the first viewport

## 6. AIgent showcase rule

`theaigent.xyz` and `tools.theaigent.xyz` are the visual authority for the AIgent preset.

They demonstrate:

- editorial command-center composition
- tinted green-black surfaces, warm ink, cyan signal, amber counterpoint
- large condensed type
- mono reserved for instrumentation
- narrative chaptering on the brand site
- direct indexed utility on the tools site
- motion that supports descent, orientation, and access

Preserve that world when working on AIgent properties. For outside projects, reuse the discipline and engineering—not the palette or skin.

## 7. Motion and media

- Map scroll to a small set of inspectable CSS variables.
- Keep the focal point stable unless camera travel is the story.
- Ensure the scene reaches its intended end state before the page ends.
- Load the hero asset first; warm later video only near use.
- Use scrub-ready video with frequent keyframes or all-intra encoding.
- Confirm MP4 byte-range requests return `206`.
- Keep useful state change when motion is reduced.

## 8. Verification

Run one batched desktop and mobile inspection, fix all findings, then confirm once.

Required checks:

- one `h1` and a clear first viewport
- no horizontal overflow
- readable real copy at 1440px and about 390px
- visible keyboard focus
- semantic links, buttons, labels, and landmarks
- WCAG AA text contrast
- touch targets near 44px or larger
- complete reduced-motion experience
- smooth scene and media behavior
- links and calls to action actually work
- `npm run audit -- <target>`
- `npm run smoke` when the repository provides it

If the page is impressive but unclear, remove or rewrite. If it is clear but generic, strengthen the visual world—not the effect count.
