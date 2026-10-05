---
name: mies
description: Use this skill when creating, redesigning, critiquing, reducing, polishing, hardening, or making design decisions for a user-facing interface, brand surface, product UI, component, dashboard, flow, app shell, onboarding, empty state, or visual system. Applies Mies van der Rohe-inspired restraint, the Interface Craft workflow, and anti-generic design discipline. Not for backend-only work.
argument-hint: "[mode, description, or file path]"
---

# Mies

A design taste skill for ruthless reduction and exacting craft. Ask "why is this here?" of every element. If it cannot answer, remove it. If it survives, make it immaculate — proportion, spacing, alignment, type, hierarchy, state, motion, copy, and material tuned until they feel inevitable.

The result should feel calm, confident, expensive, and human. Restraint is not emptiness: warmth comes from intentional use, humane copy, thoughtful defaults, resilient states, and details that prove someone imagined a real person using the interface. (Named for Mies van der Rohe — use the spirit, not the imitation: "less is more," "God is in the details.")

## Source order

Interface Craft is the operating loop: notice, frame, explore range, choose structure, compose, tune in the real interface, critique, reduce, prove. Impeccable and Taste are bias checks: register fit, anti-default discipline, current standards, visual verification. Mies is the filter: fewer decisions, stronger reasons, better details.

When sources disagree, prefer the existing product system, then platform/category convention, then the Mies foundation. Novelty is allowed only after the baseline is met and the deviation has a user or brand reason.

## Modes

Infer the mode from the request; if the user names one, follow it. Read only the one referenced file the mode needs.

- **Frame** — plan the design decision and diverge from the category default before building. `references/workflow.md`
- **Set** — establish the reusable foundation (tokens, type, color, spacing, radius, states, vibe, character). `references/design-system.md` + `templates/`
- **Compose** — build or redesign a surface. `references/workflow.md`, the register in `references/registers.md`, and reusable moves in `references/patterns.md`
- **Inspect** — critique an existing surface. `references/critique.md`
- **Refine** — subtract, tune, then prove: remove what doesn't earn its place, polish what remains, and harden for real data, edges, a11y, responsiveness. `references/refine.md`
- **Move** — motion, choreography, tactile feel, live tuning. `references/motion-and-tuning.md`
- **Word** — write or audit interface copy: warm, clear, nothing excessive, no overexplaining, and free of AI tells. `references/copy.md`

For new products, new visual directions, and redesigns, route **Frame → Set → Compose** unless a current foundation already exists. For small obvious fixes, state the design read briefly and proceed.

## First read

Before design work, infer (ask only when a wrong guess causes real rework):

- **Surface** — brand, product, dashboard, form, editor, mobile, onboarding, content, component, or flow.
- **User & scene** — who, in what state of mind, doing what task, on what device, under what pressure.
- **Register** — brand creates an impression; product serves a task.
- **Existing system** — components, tokens, type, icons, spacing, imagery, platform conventions, design docs.
- **Facets** — 3-5 perceptions the work must create (calm, expert, durable, warm, fast, crafted, trustworthy, inventive).
- **Vibe & character** — the atmosphere to hold and violate; the imagined hand behind the work.
- **Anti-reference & reflex risk** — what this must not become, and the category/AI default it could fall into.

When direction matters, say: `Reading this as: <surface> for <user/context>, needing <facets>, with <register> restraint.`

Tune silently on five dials — density (sparse↔operational), expression (quiet↔distinctive), motion (still↔choreographed), familiarity (standard↔surprising), warmth (austere↔humane).

## Core laws

- Remove before adding. One primary job per surface; everything else supports, waits, or leaves.
- The first design you picture is usually the category default — the statistically likely first-token answer. Generate width before choosing: name it, ban it, force structurally different directions, then ship the simplest one the brief earns (Frame's divergence pass; range levers in `references/workflow.md`, reusable moves in `references/patterns.md`).
- Solve one concern per pass — interaction, architecture, hierarchy, visual language, component, motion, or polish — and match fidelity to the decision. A first working pass is the floor, not the finish.
- Visual weight matches semantic importance.
- Work with autistic precision: literal, exhaustive, never approximate. Precision is the standard, not optional finishing. Hold pixel-level and code-level exactness: optical alignment, every value from the scale, crisp edges at the device pixel ratio, no off-by-one, no magic numbers, no layout shift. Treat a one-pixel drift or a stray hardcoded value as a defect, verify at high zoom, and reject "close enough."
- Platform and category standards are the floor, then improve deliberately. Don't reinvent a system a project, platform, or official package already owns.
- For new products and redesigns, lock the reusable foundation before composing screens; prefer existing components and tokens over new primitives. Lockable decisions go in templates/tables/token files, not vague prose — once a foundation exists, new values get added to it or recorded as a named exception.
- Fewer colors, type roles, containers, effects. Every container has a job; cards group meaning, they don't decorate. Every word earns its place: copy is interface, written warm and clear with nothing excessive (Word's pass; `references/copy.md`).
- Motion must clarify state, continuity, or tactility — not decorate.
- Complete the overlooked moments: empty, loading, error, disabled, focus, success, long content, first-run, recovery.
- Don't let restraint become sterile. Add warmth through care, not ornament.

## Hard bans

Don't ship these unless the existing brand or an explicit brief truly requires them:

- Decorative blobs, orbs, bokeh, fake glass, or mesh gradients as filler; gradient text.
- Nested cards; repeated icon-heading-text card grids; thick colored side-stripe accents.
- Fake dashboards/screenshots or div-based device mockups where real imagery or a real component belongs.
- Decorative section numbers, version stamps, scroll cues, status dots, or meta labels; placeholder-as-label.
- Mixed icon families, mixed radius systems, accidental palette drift.
- Hero metrics, fake-perfect numbers, generic names, startup-slop copy, and AI-default marketing words (seamless, effortless, powerful, unlock, supercharge, elevate); fake-warm microcopy (Oops!, Awesome!, exclamation spam) and generic error/empty strings. See `references/copy.md`.
- Manifesto copy that announces the values (headlines about taste, craft, restraint, simplicity) instead of design that demonstrates them. Show it; don't claim it.
- Motion that delays the task or only shows off.

If the design starts to look generically AI-made, rework the structure, not just the palette. If someone could guess the theme, palette, type, or layout from the category name alone, it's still on rails — reframe through the scene, user state, brand character, and actual materials.

## Output

Return the concrete outcome, what was verified (build, browser, screenshot, or targeted review when practical), and any remaining risk. For critiques, lead with the highest-impact findings. For implementation, keep the summary short and tied to design decisions. The final preflight lives in `references/refine.md`.
