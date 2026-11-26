---
name: design-innovation-lord
description: Lord skill for innovative/generative design — creating NEW design directions (not just extracting references), signature moments, divergent-convergent exploration, award-tier quality bar, novelty scoring, and creative critique protocols for web/desktop/brand work.
triggers:
  - design innovation lord
  - innovative design
  - unique design
  - creative direction
  - design concept
  - signature design
  - standout design
  - original design
  - experimental layout
  - design exploration
  - awwwards
  - award winning
  - تصميم مبتكر
  - تصميم فريد
  - تصميم جديد
  - ابداع تصميمي
  - تصميم مميز
personas:
  - UX
  - ARCH
  - DEV
tech_stack:
  - design-foundations
  - tailwind-4-3
lord: true

---

# Design Innovation Lord

[SKILL] design-innovation-lord
[OBJ] Generate design that didn't exist before the session — award-tier directions, signature moments, and deliberate novelty grounded in design-research evidence. Breaks "good-looking-but-generic" output.

[RULES]
1. [REQ] Diverge Before Converge — Force ≥3 materially different directions (not palette-swaps — different structure/metaphor/motion). Sketch each as a sentence: "this direction says X because Y." Then converge on ONE dominant direction; a merged average is always worse than a committed choice.
2. [REQ] Signature Moment — Every product gets exactly ONE unforgettable element (hero interaction, transition, type treatment, spatial idea). Signature moments beat uniform polish; allocate the motion/detail budget there, keep the rest quiet.
3. [REQ] Constraint-as-Feature — Turn limits into identity: single font → extreme scale contrast; no images → type-driven; limited colors → signature accent; narrow viewport → editorial stacking. Constraints are where style comes from.
4. [REQ] Mashup Method — Cross-breed two unrelated references deliberately (e.g., "terminal aesthetic × luxury editorial", "blueprint drafting × SaaS dashboard"). State the genes each parent contributes; never copy either wholesale.
5. [REQ] Principle Extraction, Not Pixel Copying — From any reference, extract the transferable principle (why it works: rhythm, tension, restraint, density) and re-express it in the product's own material. Copying pixels = derivative; copying reasoning = original.
6. [REQ] Trend Radar — Sample current frontier work for calibration (Awwwards SOTD, CSSDA, FWA, Godly, Land-book, refero/mobbin via `design-research` skill) — know the trend so the output can deliberately ride it OR deliberately defy it; accidentally-of-the-moment is still generic.
7. [REQ] Type as Structure — Type is the cheapest novelty: oversized display, variable-font axes (wght/wdth/opsz animation), mono/display pairing, vertical text, outlined type, type-as-image. Before inventing layout tricks, try a type move.
8. [REQ] Layout Invention Ladder — Grid → asymmetric grid → editorial overlap → broken grid → spatial/scroll-narrative → generative/physics. Choose the rung that fits the message; novelty without purpose is noise.
9. [REQ] Motion Identity — Give the product a motion grammar: one easing personality (snappy-spring vs smooth-drift), one duration family, entrance choreography, and scroll-linked reveals. Consistent motion reads as brand, not animation.
10. [REQ] Color Novelty — Build palettes around one signature hue + disciplined neutrals; try real-world-material references (anodized, ink-on-paper, phosphor) over default Tailwind-looking ramps; verify contrast AA regardless of audacity.
11. [REQ] Novelty Score — Before shipping, score 0–5 on: "would an experienced designer screenshot this?", "is the signature moment identifiable in one line?", "could this be templated-looking?". <3 → back to divergent loop.
12. [REQ] Squint Test — Blur the mock mentally: does the hierarchy still read? If the eye can't find primary action in 1 second blurred, the layout fails regardless of polish.
13. [REQ] 5-Second Test — One glance, ask: what's this product and what do I do? If the answer isn't instant, the concept is decoration, not design.
14. [REQ] Prototype the Risky Bit — Mock the signature moment first (static → then motion pass). If the novel element can't be built cleanly, discover it in prototype — not after the rest is coded around it.
15. [REQ] Design Critique Loop — Self-review passes: (a) squint/hierarchy, (b) novelty score, (c) consistency audit (tokens, radii, spacing), (d) a11y sweep, (e) anti-slop sweep. Ship only after all five pass.
16. [REQ] Innovation for Constraints — For mundane domains (admin panels, CRUD tools): innovate at the edges — empty states, micro-copy, onboarding, transitions, data-viz personality — never at the cost of usability.
17. [PROHIBIT] Never produce trend-average output — glassmorphism+bento+purple-gradient+Geist is the AI-slop signature; if it looks like every AI mockup, restart.
18. [PROHIBIT] Never sacrifice usability/a11y/perf for novelty — experimental and inaccessible is a failed experiment.
19. [PROHIBIT] Never present references as the design — references calibrate, the direction must be stated in product terms.
20. [PROHIBIT] Never skip the divergent phase — the first direction is usually the cliché.
21. [CMD] Feed `design-research` skill BEFORE divergent phase (references → directions); feed `design-taste` when extracting DNA from a target product; hand token implementation to `ui-design-lord`/`python-ui-lord`; run `web-design-guidelines` checklist as the floor, not the ceiling.
22. [CMD] Context7 for motion/type tech before promising it: GSAP, Framer Motion, variable fonts (fontsource), Lottie, Three.js/R3F — verify API before designing around it.

[WORKFLOWS]
1. New product direction — research (references+DNA) → divergent 3+ directions → converge to dominant + signature moment → token system → prototype risky element → critique loop → implementation handoff.
2. Refresh/generic-rescue — diagnose why current design reads generic → identify its accidental signature → either amplify it or replace with deliberate one → novelty re-score.
3. Innovation inside a boring domain — find the moments users actually touch (empty state, onboarding, errors, loading) → invent signature there → keep the rest rigorously conventional.
4. Design critique (existing work) — squint → 5-second → hierarchy → novelty score → concrete fix list ranked by impact.
