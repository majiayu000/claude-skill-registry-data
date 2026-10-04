---
name: frontend-stack
description: Router for the frontend design stack. Use at the start of any frontend UI task (build a page or component, redesign, pick a style or palette, polish, audit, animate, review UI) to decide which installed skill leads, which ones support, and which rule wins when the packs disagree. Also use when two design skills give contradicting advice.
---

# Frontend Stack router

Five design packs are installed side by side. Each is good alone and each
assumes it is the only one in the room. This skill decides who leads, so the
agent loads one lead skill plus at most two supporting ones instead of five
competing rulebooks.

## 1. Read the project first

Before picking anything, look for what the project already decided:

- `PRODUCT.md` / `DESIGN.md` at the repo root (Impeccable's context files)
- an existing design system: tokens, `tailwind.config.*`, `components/ui/`, a
  component library in `package.json`
- a brand guide the user pointed at

If any of these exist, they outrank every skill below (see rule 1 of the
precedence ladder). Your job becomes extending that system, not replacing it.

## 2. Pick the lead skill

| The task is... | Lead | Support |
|---|---|---|
| New landing page, portfolio, marketing site | `taste:design-taste-frontend` | `frontend-design:frontend-design` for direction, `ui-ux-pro-max:ui-ux-pro-max` for palette/font lookup |
| New product UI: dashboard, settings, tables, multi-step flows | `frontend-design:frontend-design` | `ui-ux-pro-max:ui-ux-pro-max` (stack + UX guidelines), `impeccable:impeccable` for `harden` at the end |
| "Plan it before coding", discovery, UX flow | `impeccable:impeccable` (`shape`) | - |
| Set up design context for a repo | `impeccable:impeccable` (`init`, then `document`) | - |
| Redesign an existing site or app | `impeccable:impeccable` (`critique` then `audit`) | `taste:redesign-existing-projects` for marketing pages |
| Polish before shipping | `impeccable:impeccable` (`polish`) | `emil-design-eng:emil-design-eng` for interaction details |
| Accessibility, performance, responsive checks | `impeccable:impeccable` (`audit`, `optimize`, `adapt`) | - |
| Choose a style, palette, font pairing, chart type | `ui-ux-pro-max:ui-ux-pro-max` | - |
| Design tokens / design system architecture | `ui-ux-pro-max:design-system` | `impeccable:impeccable` (`extract`) |
| shadcn/ui + Tailwind component work | `ui-ux-pro-max:ui-styling` | `emil-design-eng:pick-ui-library` |
| Build an animation | `emil-design-eng:animate` | `emil-design-eng:animation-vocabulary` when the user describes motion vaguely |
| Review or fix existing motion | `emil-design-eng:review-animations` / `improve-animations` | - |
| "Where should this animate?" | `emil-design-eng:find-animation-opportunities` | - |
| Gesture, spring, Apple-feel UI | `emil-design-eng:apple-design` | - |
| Web app should feel native on phones | `emil-design-eng:mobile-native` | `impeccable:impeccable` (`adapt`) |
| Try several versions of a component | `emil-design-eng:prototype` | - |
| Which library for X (charts, OTP, virtual lists...) | `emil-design-eng:pick-ui-library` | - |
| Toasts with Sonner | `emil-design-eng:ask-sonner` | - |
| UX copy, errors, microcopy | `impeccable:impeccable` (`clarify`) | - |
| Brand identity, logo, banners, slides | `ui-ux-pro-max:brand` / `design` / `banner-design` / `slides` | - |
| Explicit look: minimalist, brutalist, "expensive agency" | `taste:minimalist-ui` / `industrial-brutalist-ui` / `high-end-visual-design` | `taste:design-taste-frontend` pre-flight checklist |
| Google Stitch DESIGN.md | `taste:stitch-design-taste` | - |
| React Native / Expo motion, Swift | `emil-native:animate-expo` / `write-swift` (optional plugin) | - |
| Mockup image first, then code | `taste-imagegen:*` (optional plugin, needs image generation) | - |

If a pack is not installed, fall back to the next row's lead or to
`frontend-design:frontend-design`, which covers general direction on its own.

## 3. Precedence ladder

When two loaded skills disagree, the higher rule wins:

1. **The user's explicit request and brand.** "Use Inter", "purple is our
   brand", "keep it like Linear" beat every skill ban.
2. **The project's existing system.** `DESIGN.md`, tokens, the component
   library already in use. Extend it; do not swap libraries or mix systems.
3. **Accessibility and correctness.** Contrast, focus states, reduced motion,
   keyboard access, no layout shift. Impeccable `audit` is the referee.
4. **Scope of the lead skill.** A skill's own "not for X" line is binding:
   `design-taste-frontend` says it is not for dashboards, tables or multi-step
   product UI, so it does not lead those.
5. **Domain owner.** Motion questions go to Emil's skills, style/palette data to
   UI UX Pro Max, critique/audit/polish to Impeccable, aesthetic direction to
   frontend-design or taste.
6. **The lead skill's taste defaults.**

The rules that actually collide between packs, and how each is settled, are in
[references/conflicts.md](references/conflicts.md). Read it when a supporting
skill contradicts the lead.

## 4. Load budget

- One lead, at most two supporting skills per task. Big skills
  (`design-taste-frontend`, `ui-ux-pro-max`, `impeccable`) are long; loading all
  of them burns context and produces averaged, generic output.
- Aesthetic presets (`minimalist-ui`, `industrial-brutalist-ui`,
  `high-end-visual-design`) never stack with each other. Pick one or none.
- `taste:full-output-enforcement` only when the user asks for complete output.

## 5. Finish the same way every time

For anything user-facing, end with a review pass before calling it done:

1. `impeccable:impeccable` `audit` (or delegate to the `ui-reviewer` agent)
2. if the change has motion, `emil-design-eng:review-animations`
3. fix what they flag, then summarize what changed and what was left as-is
