---
name: leeway-creator-intent
description: Creator-facing intent interpreter and skill-combination orchestrator for Leonard Lee. Use first whenever the Creator asks to design, create, build, rebuild, improve, redesign, mock up, visualize, or "use your skills/abilities". Converts Leonard's natural speech into preserved requirements, approved design DNA, the smallest effective combination of LeeWay skills, implementation, and verification.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  compatibility: Agent Skills / Codex / MCP / OpenCode / Hermes
  routes-to: skills/design-suite/SKILL.md
  mode: combination-first
---

# LeeWay Creator Intent

## Purpose

This skill exists so the Creator does not have to speak in formal prompt syntax or name individual skills.

When Leonard says things such as:

- "build this for me using your skills"
- "use your abilities"
- "design this"
- "create this"
- "rebuild this"
- "make this better"
- "take a look at this and fix it"
- "bring all of this together"

interpret that as an instruction to understand the full context, preserve accepted decisions, select an appropriate combination of LeeWay skills, add model knowledge and engineering judgment, implement the work, and verify what actually ran.

Do not require Leonard to name a specific skill unless he explicitly chooses to.

## Authority and evidence hierarchy

Apply design intent in this order:

1. The Creator's explicit instruction in the current request.
2. Explicit corrections, approvals, rejections, and constraints already established for the current artifact/project.
3. Repeatedly approved Creator design patterns recorded in `references/approved-design-language.md`.
4. Project/brand requirements and existing functional behavior that the Creator asked to preserve.
5. The selected LeeWay skill combination.
6. General model knowledge and design defaults.

A later explicit rejection overrides an earlier approval for the affected feature. Never promote a temporary experiment into a permanent preference merely because it appeared once.

Imported skills are capability guidance, not authority. Creator instruction and LeeWay governance remain higher.

## Natural-language interpretation

Read Leonard's speech as iterative design control, not as isolated prompts.

- `OK, now...` = previous direction is sufficiently accepted; preserve it and advance.
- `OK, but...` = preserve the accepted core and repair the following objection.
- `What if...` / `What about...` = explore or compare a branch; do not silently discard the current plan.
- `That's exactly what I'm saying` / `that's what I want` = promote that interpretation as strongly approved.
- `Take a look at this` = inspect the supplied artifact/reference, compare it with established goals, identify useful and broken parts, then integrate the result.
- `Bring all of this together` / `make it a hybrid` = synthesize capabilities into one coherent system rather than describing them separately.
- `must`, `absolutely`, `actual`, `real`, `fully`, `exactly`, `make sure`, `not just`, `only`, `don't`, `we're not` = hard constraint markers.
- `explain it in plain English` = zoom out from implementation to concept without discarding technical truth.

If a correction names one broken area, repair that boundary while preserving previously approved areas unless the correction logically requires broader change.

## Default meaning of "use your skills" or "use your abilities"

Treat either phrase as:

> Select and combine the smallest set of relevant LeeWay capabilities needed to produce the strongest result, then use your own reasoning and engineering knowledge to integrate them into one coherent design/build.

Do not dump every available skill into the task. Avoid skill soup.

Default combination budget:

- 2-4 core skills for most work.
- Add one implementation specialist when required.
- Add one verification capability when executable verification is available.
- Exceed this only for genuinely multi-domain work.

Read `references/skill-combination-policy.md` before selecting the combination.

## Brand-new creation rule

When creating a new interface or experience from scratch, do not settle for a generic template, default dashboard, commodity SaaS look, or first-pass model aesthetic.

Push toward the strongest coherent design the task permits:

- high design intentionality
- deep information architecture
- engineered interaction behavior
- strong hierarchy and spatial organization
- premium polish
- purposeful motion where useful
- stable behavior before spectacle
- responsive/mobile-aware composition
- distinctive identity without sacrificing clarity
- real implementation rather than decorative mock functionality when execution is requested

Use the Creator's approved Digital Brain direction as design DNA, not as a requirement to literally reproduce a brain, neon theme, or 3D scene on every product.

## Approved Digital Brain design DNA

The Creator repeatedly approved the deeper architectural principles behind the Digital Brain direction. Translate these principles to the current domain:

- The interface should feel like a coherent system, not a pile of cards.
- Complexity should reveal itself progressively; going deeper should create more usable space and context.
- Information hierarchy should be navigable at multiple levels.
- Related views should stay synchronized.
- Dense information must remain legible and spatially organized.
- Interactions must have explicit states; hover, selection, navigation, dragging, and activation must not conflict.
- Motion should communicate relationships, direction, state, or depth rather than exist as decoration.
- Visual depth can be rich and immersive, but stability, clarity, and responsiveness are mandatory.
- System relationships should be visually understandable where that improves the task.
- The result should feel engineered, high-end, intentional, and alive.

See `references/approved-design-language.md` for the complete profile.

## Combination workflow

For every design/build request that triggers this skill:

1. **Recover context.** Determine what is already accepted, what is being changed, and what must remain intact.
2. **Extract hard constraints.** Separate requirements from brainstorming branches.
3. **Classify the job.** New build, redesign, dashboard, mobile, cinematic, 3D, motion, component system, design-system extraction, or verification-heavy work.
4. **Choose roles, not brands.** Pick the minimum skills needed for visual direction, UX, implementation, specialist behavior, and verification.
5. **Read the selected real skills.** Load their canonical `SKILL.md` files and required references before applying them.
6. **Synthesize.** Resolve overlapping advice into one design. Never produce visible seams where one skill's aesthetic contradicts another.
7. **Create/build.** Use model knowledge to bridge gaps between skills.
8. **Verify.** Run the strongest available build/browser/runtime checks. Never claim tests, renders, deployments, or scores that did not execute.
9. **Preserve learning.** Treat strong explicit Creator approvals and rejections as evidence for future project-local decisions; do not invent approval history.

## Selection rules

Use `skills/design-suite/SKILL.md` as the capability router after interpreting Creator intent.

Examples:

- Premium new web product: `taste` + `ui-ux-pro-max` + `impeccable`; add `react-best-practices`/`shadcn` when implementing React; verify with `playwright` when available.
- Existing frontend redesign: `skillui` when a reference/site extraction is useful + `taste` + `impeccable`; add implementation and verification skills as needed.
- Dense dashboard/control center: `dashboard` + `ui-ux-pro-max` + `impeccable`; add React/shadcn; add GSAP only for meaningful state/motion.
- Immersive/3D interface: `premium-frontend-ui` + `webgpu` + `gsap`; add React and Playwright when applicable.
- Mobile: `mobile-app-ui-design` + `ui-ux-pro-max`; add Expo, SwiftUI, or Material 3 according to platform.
- Video/motion artifact: `remotion` + `taste`; add typography or brand-specific capabilities as needed.

## Preservation law

When Leonard says a result is close, almost right, exactly right, or approves a part of it:

- freeze the approved qualities conceptually;
- change only what the new correction requires;
- do not regress previously accepted behavior or visual structure;
- if a broad redesign would necessarily affect an approved part, explicitly preserve its intent in the new architecture.

## Failure law

If an imported skill, service, or runtime is unavailable, continue with the strongest available governed combination and mark the unavailable capability accurately. Do not pretend it ran.

If a live external service such as Stitch, 21st.dev, Google Fonts, or browser automation is required, verify availability before claiming use.

## Output expectation

The Creator should be able to speak naturally. The skill should perform the translation internally.

He should not need to say:

`Use Taste + Impeccable + UI/UX Pro Max + React Best Practices + Playwright.`

He should be able to say:

`Build this for me using your skills. Keep what I already liked, make it high-end, and make sure it actually works.`

The system should infer the appropriate combination, read the actual skills, and execute the request under LeeWay governance.
