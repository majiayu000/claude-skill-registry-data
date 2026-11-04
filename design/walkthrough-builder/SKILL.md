---
name: Walkthrough Builder
description: Builds a stakeholder guided-tour over live sandbox prototypes — rail, plain-language copy, and per-step iframe deep-links. Use after a prototype exists when the user asks for a walkthrough, guided tour, click-through, or stakeholder explanation of a feature.
version: 1.0.0
author: Mattermost Design Team
tags: [prototype, walkthrough, stakeholder, phase-6, presentation, defense-ux]
---

# Walkthrough Builder

Builds a **guided tour shell** over existing sandbox prototype screens. The walkthrough is not the product UI. It is a presentation wrapper: left rail = story, center = why / what to look at, right = a live iframe of a specific prototype state.

Gold example (copy, beats, deep-links): `prototype-playground/mattermost-proto-playground/src/pages/GlobalMembershipPolicy/SimplifiedWalkthrough/gmpSimplifiedWalkthroughSteps.ts` and the live route `/prototypes/global-membership-policy-simplified-walkthrough`.

## When to Use

- After at least one sandbox prototype route exists (typical post-Phase-6 / post-Gate-6)
- When stakeholders need to understand the project, the tasks, the customer stories, and the vision in one sitting
- When a built prototype is hard to demo without a narrator

## When NOT to Use

- Before a sandbox prototype exists — **stop**. Do not substitute screenshots, Figma, or a copy-only deck.
- To replace the product UI or the Phase 6 option comparison
- For DPC-style "drive the app yourself" demos (that is a different pattern; see `src/pages/dpc-v2/walkthrough/`)
- To auto-run as part of every Phase 6 build — invoke only when the user asks for a walkthrough

## Preconditions (hard stop)

All of these must be true before any walkthrough files are created:

1. A sandbox prototype is registered in `src/manifests/prototypes.ts` with a `/prototypes/...` path
2. Those screens can be loaded in an iframe (same origin)
3. You can name the live routes this tour will iframe

If any is missing: stop and say which prototype to build first. Do not invent a slideshow.

## Input

```json
{
  "feature_name": "GlobalMembershipPolicy",
  "feature_slug": "global-membership-policy-simplified",
  "prototype_routes": ["/prototypes/global-membership-policy-simplified"],
  "eyebrow": "Design proposal walkthrough",
  "title": "Global Membership Policies — Simplified",
  "subtitle": "One-line vision the viewer can repeat after the first screen."
}
```

Pull customer stories from the brief, personas, PRD, or the prototype's own seed policies. If none exist, compose 2–4 from the seed data and flag each `[VERIFY]`.

## Output

| File | Role |
|---|---|
| `src/pages/{Feature}/Walkthrough/{Feature}Walkthrough.tsx` | Thin wrapper around `WalkthroughShell` |
| `src/pages/{Feature}/Walkthrough/{feature}WalkthroughSteps.ts` | All copy, rail order, preview URLs |
| `src/manifests/prototypes.ts` | New `PrototypeEntry` for `/prototypes/{slug}-walkthrough` |
| Product pages under the iframe | Query-param presets + `data-tour-focus` anchors as needed |

Do **not** copy the GMP/Attribute Hub shell TSX or SCSS. The chrome lives in `src/components/walkthrough/WalkthroughShell.tsx`.

## Workflow

Copy this checklist and complete it in order:

```
Walkthrough progress:
- [ ] 1. Inventory live routes, query params, and existing focus ids
- [ ] 2. Outline required beats (+ optional extras only if needed)
- [ ] 3. List deep-link gaps (missing presets / focus anchors)
- [ ] 4. Wire product pages (presets, data-tour-focus, WalkthroughFocusProvider)
- [ ] 5. Author the steps file
- [ ] 6. Add the thin WalkthroughShell page + manifest entry
- [ ] 7. Copy pass (ux-copy-reviewer) + jargon pass
- [ ] 8. Browser-check every step: iframe matches lookFor
- [ ] 9. npm run build in the sandbox
```

### Step 1 — Inventory

Read `src/manifests/prototypes.ts` and the product pages this tour will iframe. Collect:

- Routes (`/prototypes/...`)
- Existing query params (`?policy=`, `?state=`, `?focus=`, …)
- Existing `data-tour-focus` ids in `src/components/walkthrough/walkthroughFocus.ts`

Do not author copy that points at a state the product page cannot show.

### Step 2 — Outline

Required beats (every tour, in this order). Extra sections only if the project needs them.

1. **Why** — current pain, what we are building, the vision in one sentence
2. **How it works** — screen-by-screen product tour
3. **Customer stories** — 2–4 named situations: who, problem, how this solves it, which screen
4. **In / out of scope** — what this tour is not claiming, plus open `[VERIFY]` items

Optional extras (insert only when they earn a slot): a short **primer** before the tour (a concept the screens assume), **save / impact / guardrails**, mobile, licensing.

Length: **8–22 steps**. Prefer fewer. One step = one idea + one prototype state. Do not split a single view into six steps unless `lookFor` actually changes.

Details and copy craft: [copy-and-beats.md](copy-and-beats.md)

### Step 3–4 — Deep-links (required)

Every step's `preview.path` must land on the **exact** state the copy describes. If the product page cannot show that state yet, add a query-param preset and/or a `data-tour-focus` anchor **on the product page** before writing the step.

Protocol: [deep-links.md](deep-links.md)

### Step 5 — Steps file

```ts
import {
  withFocus,
  type WalkthroughStep,
} from '@/components/walkthrough/walkthroughTypes';

export type WalkthroughSection = 'intro' | 'tour' | 'stories' | 'appendix';
export type WalkthroughRailGroup = 'Requirements' | 'Scope';

export const WALKTHROUGH_SECTION_LABELS: Record<WalkthroughSection, string> = {
  intro: 'Why we need this',
  tour: 'How it works',
  stories: 'Customer stories',
  appendix: 'Scope and open items',
};

export const STEPS: Array<WalkthroughStep<WalkthroughSection, WalkthroughRailGroup>> = [
  {
    id: 'why',
    section: 'intro',
    title: 'Why this exists',
    bullets: ['…'],
    lookFor: ['The control this step is about'],
    preview: { kind: 'iframe', path: withFocus('/prototypes/{slug}', 'table') },
  },
];
```

Section keys are project-specific. Rail labels in `WALKTHROUGH_SECTION_LABELS` are plain language, not spec IDs.

### Step 6 — Thin page + manifest

```tsx
import WalkthroughShell from '@/components/walkthrough/WalkthroughShell';
import { STEPS, WALKTHROUGH_SECTION_LABELS } from './{feature}WalkthroughSteps';

export default function {Feature}Walkthrough() {
  return (
    <WalkthroughShell
      eyebrow="Design proposal walkthrough"
      title="{Feature title}"
      subtitle="{one-line vision}"
      steps={STEPS}
      sectionLabels={WALKTHROUGH_SECTION_LABELS}
    />
  );
}
```

Register in `src/manifests/prototypes.ts` (read the current `PrototypeEntry` shape first):

- `id`: `{slug}-walkthrough`
- `path`: `/prototypes/{slug}-walkthrough`
- `label`: `{Short name} · Walkthrough`
- `group`: same group as the product prototype

### Step 7 — Copy pass

Audience: mixed internal stakeholders (PM, eng, design, security). They may not know this feature.

- Easy to understand. No process jargon. No unexplained acronyms.
- Every step explains **what it does** and **why we built it that way**.
- One idea per bullet. Present tense. Short.
- Introduce a domain term once in plain English, then use it.
- Run `ux-copy-reviewer` on the steps file before sharing.
- Keep `[VERIFY]` flags visible — never bury them.

### Step 8–9 — Verify

In the browser, click every rail item. For each step: the iframe shows what `lookFor` names, and the copy is true of that screen. Then `npm run build` in `prototype-playground/mattermost-proto-playground`.

## Anti-patterns

| Do not | Do this |
|---|---|
| Copy GMP/Attribute Hub shell TSX+SCSS | Use `WalkthroughShell` |
| Iframe the default screen for every step | Deep-link each step to a specific state |
| Write the tour before the product page can show the state | Wire presets / focus anchors first |
| Spec-speak, unexplained acronyms | Plain English; introduce a term once |
| Pad to 22 steps | Cut steps that do not change `lookFor` |
| Skip customer stories | Always 2–4 named stories |
| Customer names in copy | Role + situation ("program security officer") |
| Screenshot / Figma / markdown fallback | Stop until a prototype exists |
| Auto-add a walkthrough to every Phase 6 package | Only when the user asks |

## Related Skills

- **Prototype Scaffolder** — product screens this tour iframes
- **UX Copy Reviewer** — required pass on walkthrough copy
- **Option Presenter** — option comparison is a different artifact; do not merge them

## Gold example

- Shell: `src/components/walkthrough/WalkthroughShell.tsx`
- Steps: `src/pages/GlobalMembershipPolicy/SimplifiedWalkthrough/gmpSimplifiedWalkthroughSteps.ts`
- Focus registry: `src/components/walkthrough/walkthroughFocus.ts`
- Live: `/prototypes/global-membership-policy-simplified-walkthrough`
