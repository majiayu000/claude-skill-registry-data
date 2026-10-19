---
name: perfect-ai-master
description: Build, audit, and refactor premium Persian/English responsive websites and interactive 3D experiences with Anime.js v4, Three.js, motion choreography, color theory, RTL design systems, accessible UI/UX and VibeFarsi registry. Use for website design, animations, motion, landing pages, 3D/WebGL, responsive interfaces, visual quality, or Perfect_AI projects in Codex.
---

# Perfect_AI — Codex Master Skill

> A practical engineering playbook, not a promise of pixel-perfect cloning or access to third-party private source files. Built from original guidance with links to official documentation and VibeFarsi catalog entries. Read the relevant referenced files before implementing.

## ULTRA skill pack routing — 2026-10-09

This package has **91 locally authored Codex Skills**, **279 per-item VibeFarsi implementation specifications**, **47 vetted-as-relevant GitHub repo/agent-skill references** (upstream files not copied), **an executable color engine**, **a live Anime.js+Three.js example** and installer scripts for official VibeFarsi CLI. It uses **no MCP**.  This is original technical guidance; real official third-party files are obtained separately using documented installers.

| Request | Must load | Local runnable artifact |
|---|---|---|
| Anime.js exact mechanism/scroll/text/SVG | `references/16-animejs-api-matrix.md`, `references/01-animejs-motion.md`; focus `zt-anime-*` | `examples/live-lab/` |
| True 3D, particles, camera, PBR, shaders | `references/17-threejs-production-guide.md`, `references/13-threejs-animation-atlas.md`; focus `zt-three-*` | `examples/live-lab/` |
| Choose professional colors (not random neon) | `references/18-color-decision-engine.md`, `references/19-design-matrix.md`; focus `zt-color-*` | `tools/color-engine.mjs` and `tools/create-palette.mjs` (also copied inside master Skill) |
| Any specific VibeFarsi item | `registry/vibefarsi-items/<category>/<slug>.md`, `references/21-vibefarsi-implementation.md`; `zt-vibefarsi-*` | `install/install-vibefarsi-all.ps1` (dry run default) |
| GitHub engineering best practices | `references/15-github-curated-skills.md`; `zt-react-*`, `zt-debugging`, `zt-tdd` | `github-skills-catalog.json` |
| Ship/test | `references/20-test-matrix.md`; `zt-e2e-playwright`, `zt-a11y-axe` | `tools/validate_pack.py`, `tests/color-engine.test.mjs` |

**Completion rule:** a component/pattern is not implemented merely because a Skill lists it. Write real code into the target application, run checks and report exactly what was/was not executed. Prioritize the user's specified visual identity and color constraints above default category palettes.

## Non-negotiable execution protocol

1. **Inspect** the repo, package manager, frameworks, baseline look, existing code, fonts, accessible semantics and performance budget. Keep working behavior. Never overwrite user files without checking. List major entrypoints.
2. **Define** objective, target audience, language(s), content, content hierarchy, direction, supported devices, interaction model, performance target, color/theme, and reference URLs. Use provided constraints rather than asking again.
3. **Reference decomposition:** for each sample site screenshot or URL break down shell, header, hero, 3D object geometry/material, typography, sticky/scroll phases, color, effects, layout, motion timeline, text, sections and responsive variants. Distinguish *observed* from *inferred* and *not verified*. Do not claim to have extracted exact original geometry or code without doing so.
4. **Architect:** choose native CSS for basic states, Anime.js v4 for orchestrated DOM/SVG/text/scroll, Three.js for truly 3D WebGL/WebGPU, and VibeFarsi components for Persian RTL UI. Pick one owner for each property: no Anime.js/CSS/Three.js competing transforms on the same node.
5. **Build progressively:** static accessible HTML first; mobile-first layout; typographic/token system; functional controls; scroll triggers; restrained enhancement; real 3D; performance fallback; reduced-motion handling; tests.
6. **Run:** install/build/typecheck/lint/tests; use a browser if present to inspect desktop/tablet/mobile, slow scroll, reverse scroll, focus/keyboard, low-power, RTL, reduced motion and browser console. Fix and recheck. Do not claim unseen tests passed.
7. **Report** files changed, what is implemented, what requires dependencies, browser checks done, measured vs target values, remaining caveats.

## Read exactly the matching reference modules

| Task | Primary reference | Supporting reference |
| --- | --- | --- |
| Anime.js animations, text, SVG, scroll | `references/01-animejs-motion.md` | `references/06-motion-recipes.md` |
| Three.js, point clouds, shaders, morphing | `references/02-threejs-3d.md` | `references/10-perfect-ai-experience.md` |
| Color theory, dark monochrome, token design | `references/03-color-theory.md` | `references/04-ui-ux-system.md` |
| UI/UX design, interactions, information architecture | `references/04-ui-ux-system.md` | `references/08-quality-tests.md` |
| Responsive / mobile / touch / RTL | `references/05-responsive-rtl.md` | `references/09-persian-localization.md` |
| Named animation recipes | `references/06-motion-recipes.md` | `references/01-animejs-motion.md` |
| VibeFarsi: **every listed registry entry** | `references/07-vibefarsi-full-catalog.md` | `references/09-persian-localization.md` |
| Test/audit/production ship | `references/08-quality-tests.md` | `references/11-workflow-architecture.md` |
| Iran/Persian language, form, dates, SEO | `references/09-persian-localization.md` | catalog Skill entries |
| Rebuild/extend user's Perfect_AI website | `references/10-perfect-ai-experience.md` | three, motion, color, responsive |
| Architecture, implementation patterns, dependency conflicts | `references/11-workflow-architecture.md` | quality tests |
| Source-of-truth links and version checks | `references/12-sources-and-rights.md` | official docs |
| Three.js individual animation mechanisms | `references/13-threejs-animation-atlas.md` | `references/02-threejs-3d.md` |

## Additional deep references
- `references/15-github-curated-skills.md`: upstream project selection and provenance; originals are not copied.
- `references/16-animejs-api-matrix.md`: v4 official API coverage and homepage demo techniques.
- `references/17-threejs-production-guide.md`: real mesh/shader/camera/render lifecycle.
- `references/18-color-decision-engine.md`: formal OKLCH/contrast/color-choice workflow.
- `references/19-design-matrix.md`: product-context design decisions.
- `references/20-test-matrix.md`: launch and regression QA.
- `references/21-vibefarsi-implementation.md`: all official registry items using CLI without MCP.
- `registry/vibefarsi-items/<category>/<slug>.md`: bundled with the master Skill, survives install into `.agents/skills/perfect-ai-master/`.

## Mandatory design rules

- **Real content first.** No empty fake buttons, invented testimonials or fake metrics. Every interaction has a defined outcome and keyboard equivalent.
- **Direction:** `lang="fa" dir="rtl"` for Persian; isolate URLs, numbers, code, model names in `dir="ltr"` or `<bdi>`. Use logical layout properties (`margin-inline-start`), avoid accidental double reversal.
- **Perfect_AI default visual:** genuinely black/white with a layered neutral ramp; no random cyan/purple/pink gradients. If another theme is explicitly requested, apply system tokens and check contrast.
- **Semantics:** one h1; ordered sections; meaningful labels; focus-visible; no canvas-only critical content; real links; ARIA only when native HTML is inadequate.
- **Motion:** every animated experience has initial/final states, a time/progress model, interruption/reversal strategy, ownership, fallback and cleanup. Respect `prefers-reduced-motion`.
- **Scroll:** use a single normalized progress signal, clamped 0..1; use rAF/coalesced updates, avoid forced layout inside the frame, ensure reverse scroll and short viewport correctness.
- **3D:** define actual topology (mesh/geometry/particles), camera, materials, lighting, render pipeline, animation, resolution and fallback. A 2D radial canvas is not automatically a 3D mesh. Inspect performance of transparent particles and postprocessing.
- **Quality:** no horizontal overflow at 320 CSS px; no text trapped behind the orb or fixed nav; avoid 100vh keyboard bugs; mobile tap targets generally >=44 CSS px; document zoom 200%; functionality without WebGL.
- **Color:** use semantic tokens and distinguish decoration from information. Check WCAG 2.2 contrast targets, not eyeballing.
- **Rights:** do not misrepresent third-party implementations as original or automatically copy proprietary page scripts/assets. Reuse open-source code only when permitted by its LICENSE and keep credits when required. For VibeFarsi official files, install via its published CLI if desired; local guidance is independent.

## Implementation decision tree

- One-off hover/focus transition? CSS transitions with `transform` and `opacity`.
- Enter/reveal/count/stagger/SVG path/interactive timeline? Anime.js v4.
- Scroll choreography involving DOM? Anime.js `onScroll` or a single scroll-controller with explicit `progress`.
- Dense particles, morphing 3D, glTF, HDR lighting? Three.js (choose BufferGeometry, InstancedMesh, Points, ShaderMaterial, AnimationMixer as appropriate).
- CSS-only rich RTL components desired? Look up `07-vibefarsi-full-catalog.md` and use official `npx vibefarsi add <slug>` where permitted.
- Visually delicate foreground text? Keep DOM HTML separate from a `pointer-events:none` 3D canvas; never rasterize text without reason.
- Device cannot support full effect? Static SVG/poster or lower-density animation fallback that preserves content.

## Working definition of finished

- [ ] At least one deliberate responsive layout for 320/375/768/1024/1440 widths.
- [ ] No console/runtime/build issues observed during completed tests.
- [ ] Scroll motion is bidirectional, bounded, and independent of frame rate.
- [ ] Color and typography tokens centralised; bright glow never replaces readable text.
- [ ] Keyboard and screen-reader accessible alternatives; reduced-motion mode.
- [ ] No infinite rAF after component unmount/navigation.
- [ ] Clearly report tests run and unverified areas.

## Suggested invocations

- `Use $perfect-ai-master to audit and rebuild this React landing page in monochrome with true 3D and Anime.js text transitions; read all relevant references first.`
- `Use $perfect-ai-master to build a responsive bilingual RTL site with VibeFarsi components, 3D product viewer, accessible form, and performance tests.`
- `Use $perfect-ai-master and apply the Perfect_AI scroll-experience spec, preserving existing content and source code.`


## OMEGA extension — ALL earlier Skills remain installed
This pack preserves 91 preceding local skills, all 279 VibeFarsi item specifications, 47 curated GitHub upstream references, Anime.js v4 and Three.js executable examples, and the existing OKLCH palette engine. It adds a large focused `ztx-*` skill family plus 29 deep reference chapters (22–50) and 30 responsive CSS recipes. No MCP required and no misleading claim of copying private source. Use task-relevant skills; never load all simultaneously.

**Responsive MUST-READ (first):** `references/22-responsive-engineering-foundations.md`, `references/23-container-query-design-system.md`, `references/24-fluid-type-persian-ltr.md`, `references/25-mobile-touch-gestures.md`, `references/26-scroll-choreography-responsive.md`, `references/27-adaptive-3d-quality-controller.md`, `references/30-responsive-audit-test-matrix.md`. Open `patterns/responsive/*.md` for exact component recipes.

**Color MUST-READ:** `references/36-advanced-color-science.md`, `references/37-color-algorithm-workbook.md`, `references/38-design-systems-at-scale.md`; run the palette tool, measure contrast, do not infer palette from stereotypical color psychology. Monochrome for Perfect_AI.

**Other motion engines:** `references/32-motion-libraries-decision-tree.md`, `references/33-animation-physics-timing.md`, `references/34-browser-native-animations.md`. Distinguish Anime.js, Motion `animate()`, Animate.css, GSAP and Three.js; use only engines the project needs. "animate.js" is ambiguous across ecosystems.

**QA:** `references/42-accessibility-wcag22.md`, `references/43-visual-regression-and-browser-matrix.md`, `references/44-performance-budget-core-web-vitals.md`; executable `examples/responsive-lab/`, `tests/omega-validation.test.mjs` and `tools/responsive-audit.mjs`.


## TITAN extension — 2026-10-09, zero deletion

This pack preserves the original OMEGA 187 skills, all 279 VibeFarsi local guides, existing 49 references, 30 responsive recipes, color toolchain and all three motion/responsive labs. It additionally includes **576** scoped implementation patterns (36 mechanisms × 16 usage contexts), each with a dedicated `ztp-*` Codex Skill; **144** author-written cross-domain specialist reference chapters; an ultimate color theory and decision procedure; and 40 locally authored GitHub integration Skills. The upstream repos are pointers, **not copied GitHub source**.

### Learn and route instead of flooding context

1. Read `references/51-ultimate-color-design-reasoning.md` before deciding a theme. Run the existing `tools/palette-decision.mjs` and review contrast. For strict Perfect_AI, remain grayscale.
2. Read `references/expert-atlas/<area>/<facet>` using the IDs from `expert-references-index.json` (also available at pack root).
3. For animations choose exactly one of Anime.js v4, Three.js, native CSS/WAAPI, Motion or GSAP for each property and component; open the matching `patterns/implementation-atlas/<engine>/ztp-*.md`. These are patterns with scoped starter code and acceptance tests, not 576 distinct animation algorithms.
4. For GitHub upstream engineering skills use the locally authored `ztg-*` guide first and review the license and package version before any download. No MCP.
5. For Persian components load the 279 `registry/vibefarsi-items/*/*.md` files as a selection catalog, then inspect and install official components via CLI only if approved; code is not embedded by that catalog.
6. Only report a production implementation if the code was integrated in the target app, dependencies installed, browser interactions tested and visual QA performed; none of those occur just by installing Skills.

The canonical pack index is `INDEX-TITAN.md`, with IDs for targeted loading. The master skill is not a command to paste all 763+ files into one prompt.
