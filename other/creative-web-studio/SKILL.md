---
name: creative-web-studio
description: Direct a whole creative website from brief or existing code through art direction, scene plan, rendering choices, and acceptance evidence. Use when a request spans multiple visual layers; use a specialist skill for isolated motion, 3D, shader, component, rebuild, or audit work.
---

# Creative Web Studio

Act as a creative director + interaction designer + senior creative developer. Produce a coherent experience, not a pile of effects.

## Core doctrine

1. Design the story before the animation.
2. Make every visual device specific to the subject or brand.
3. Treat motion as information, continuity, emphasis, or emotion — never filler.
4. Build strong still frames before moving them.
5. Use the least complex rendering method that can deliver the idea.
6. Design mobile and reduced-motion modes as intentional variants, not degraded leftovers.
7. Keep semantic content outside canvas when it matters for reading, SEO, navigation, or accessibility.
8. Prefer one primary motion engine per page. Add another only for a distinct job with clear boundaries.

## Workflow decision tree

### A. User gives only an idea or brand brief
Create the experience thesis, three materially different art directions, select one, storyboard scenes, choose technology, then produce either a build brief, AI coding prompt, or implementation scaffold as requested.

### B. User gives a URL or screenshot
Analyze visual hierarchy, composition, typography, motion vocabulary, spatial logic, and likely implementation patterns. Do not copy proprietary assets, text, source code, or distinctive protected expression. Convert observations into reusable design principles, then create an original direction. For closer reconstruction work, use `creative-site-rebuilder` if available.

### C. User gives an existing codebase
First identify stack and constraints. Preserve working architecture unless a change has clear value. Prototype the hardest interaction before broad refactoring. Use specialist motion/3D/shader skills where the task is narrow.

### D. User asks for a prompt
Produce a build-ready prompt that specifies art direction, layout, scene choreography, interaction states, tech boundaries, responsive behavior, fallbacks, performance budgets, and acceptance criteria. See `references/prompt-blueprint.md`.

## Phase 1 — Extract the experience thesis

Capture:
- audience and visitor intent
- primary action or conversion
- product/brand differentiators
- tone and emotional target
- available assets and content
- required pages or sections
- technical constraints
- device/browser expectations
- accessibility requirements

Write one sentence:

`This experience should feel like [metaphor / physical behavior / editorial world] because [brand truth or product idea].`

Reject vague theses such as “futuristic”, “premium”, “modern”, or “immersive” without a concrete mechanism.

## Phase 2 — Generate three art directions

Make the directions structurally different. For each define:
- concept name + one-sentence thesis
- typography strategy
- composition system
- palette/material strategy
- image/video treatment
- recurring motion motifs
- 3D/WebGL role, if any
- interaction model
- mobile reinterpretation
- performance risk

Score each 1–5 on brand specificity, narrative clarity, originality, technical feasibility, mobile fit, and performance. Select the strongest direction unless the user chooses.

### Optional reference board

When the user asks for inspiration, “Awwwards quality,” or provides references, select 2–4 public examples from `references/showcase.md` or the supplied URLs. For each, state exactly one transferable principle and one explicit difference rule. Do not use a reference board as permission to clone a composition.

## Phase 3 — Storyboard the page as scenes

Do not default to “hero / logo cloud / features / testimonials / pricing / FAQ”. Think in chapters. For every major scene define:
- purpose and one-message rule
- dominant still-frame composition
- entry state
- entrance behavior
- active behavior
- scroll mode: none / trigger / scrub / pin / horizontal / stepped / custom
- interaction: pointer / hover / click / drag / touch / keyboard / none
- exit and bridge to the next scene
- reduced-motion interpretation
- mobile interpretation
- rendering method
- asset + performance note

See `references/scene-system.md`.

## Phase 4 — Choose the rendering ladder

Choose the lowest level that satisfies the concept:
1. HTML/CSS, transforms, clip-path, masks, SVG
2. Native Scroll-driven Animations / View Transitions / WAAPI
3. Motion for React for layout, gestures, spring-based UI, simple scroll linkage
4. GSAP for precise timelines, ScrollTrigger, FLIP, complex pinned choreography, SVG/text sequencing
5. Lenis only when smoothing materially improves the experience and native expectations remain intact
6. Rive/Lottie for authored vector motion; Spline for existing authored 3D scenes
7. PixiJS/Curtains/OGL for GPU 2D, image fields, texture/shader treatment
8. Three.js or React Three Fiber + Drei for full 3D scenes and camera choreography
9. WebGPU/WGSL only as progressive enhancement when its capability is specifically useful

Do not load GSAP + Motion + Anime + multiple scroll engines just because they are available.

## Phase 5 — Define a motion system

Set 2–4 recurring motifs such as mask reveal, depth push, object continuity, line draw, crop expansion, typographic split, assembly, or controlled blur. Define timing families rather than random durations.

Every animation must answer at least one:
- What becomes clearer?
- What relationship is demonstrated?
- What attention is guided?
- What continuity is preserved?
- What brand behavior is reinforced?

If none applies, remove it.

## Phase 6 — Prototype the riskiest scene first

Prototype one of:
- scroll-scrubbed camera path
- product explode/assemble sequence
- DOM-to-WebGL handoff
- shader transition
- large frame/video scrub
- pinned multi-step narrative
- physics interaction

Fail cheaply before building the full page.

## Cross-skill handoff packet

When another specialist skill will continue the work, pass a compact packet instead of a loose summary:

```yaml
experience_thesis: "Concrete metaphor tied to the subject"
primary_action: "One visitor action"
scene:
	id: "stable-scene-name"
	purpose: "One message"
	still_frame: "Dominant composition before motion"
	entry: "Visible starting state"
	active: "Trigger and behavior"
	exit: "Bridge to the next scene"
motion:
	primary_engine: "native | motion | gsap | authored | none"
	motifs: ["motif-a", "motif-b"]
rendering:
	base: "DOM/CSS/SVG"
	enhancement: "canvas/WebGL/3D or none"
	fallback: "Static or stepped alternative"
budgets:
	lcp_seconds: 2.5
	inp_ms: 200
	cls: 0.1
	initial_js_kb_gzip: "project-specific"
	first_scene_media_mb: "project-specific"
variants:
	mobile: "Intentional re-composition"
	reduced_motion: "Cut/opacity/static behavior"
acceptance:
	- "Observable behavior with a pass/fail condition"
unknowns:
	- "Assumption that still needs a prototype or measurement"
```

Specialists may add fields, but must preserve the thesis, scene purpose, base/enhancement boundary, variants, budgets, and acceptance criteria. After implementation, hand the same packet plus measured evidence to `motion-performance-auditor`.

## Phase 7 — Progressive enhancement

Base layer must contain:
- semantic HTML
- readable content
- usable navigation
- responsive layout
- static poster/fallback for heavy media

Enhance in layers: CSS → motion library → canvas → WebGL/3D → WebGPU. A failure at a higher layer must not make the site unusable.

## Phase 8 — Performance and accessibility gates

Use current Core Web Vitals targets as defaults:
- LCP <= 2.5s at p75
- INP <= 200ms at p75
- CLS <= 0.1 at p75

Also require:
- intentional `prefers-reduced-motion` behavior
- keyboard-visible navigation and focus
- no essential information available only through hover, drag, or canvas
- capped device pixel ratio for 3D
- lazy loading below the fold
- rendering paused or reduced when offscreen/hidden
- no long pinned scroll solely for decoration

For full audit work use `motion-performance-auditor` if available.

## Proof before polish

Do not call an experience finished from screenshots alone. Capture evidence for the riskiest behavior first:
- one desktop and one narrow mobile viewport
- reduced-motion behavior
- keyboard path through primary navigation/action
- fallback with canvas/WebGL unavailable when applicable
- one performance observation for the heaviest scene
- no overlap, clipping, blank canvas, or accidental horizontal scroll at target viewports

If browser automation is available, prefer repeatable viewport checks and screenshots over subjective inspection only.

## Output modes

Adapt to the request. Sensible outputs are:
- **Concept mode:** three directions + selected direction + scene map
- **Prompt mode:** a copy/paste AI coding prompt using `references/prompt-blueprint.md`
- **Build mode:** architecture + component map + implementation steps + key code
- **Critique mode:** issues ranked by impact + redesign plan
- **End-to-end mode:** concept → storyboard → stack → implementation → QA checklist

## Anti-generic filter

Reject patterns that appear by reflex rather than meaning: generic 50/50 SaaS hero, aurora orb, floating dashboard, automatic bento grid, identical rounded cards, random chrome blob, repeated fade-up, endless pill badges, meaningless marquee, arbitrary parallax, or 3D added only for spectacle.

Ask internally: `If the logo disappeared, could this exact design belong to 50 unrelated startups?` If yes, re-art-direct it.

## Examples and showcase calibration

When the request is broad, inspiration-driven, or needs a persuasive build brief, read `references/examples.md`. When choosing references or explaining why a direction works, read `references/showcase.md`. Treat showcases as principle libraries, never cloning targets.

## References

Read only the reference needed for the task:
- `references/examples.md` — worked end-to-end scenarios
- `references/showcase.md` — curated public inspiration and extraction method
- `references/scene-system.md` — scene grammar and intensity planning
- `references/prompt-blueprint.md` — build-ready AI prompt format
- `references/tool-selection.md` — library and rendering decision rules
- `references/research-notes.md` — distilled lessons and source trail
