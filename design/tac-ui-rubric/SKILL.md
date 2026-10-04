---
name: tac-ui-rubric
description: >-
  Use this skill to score any UI surface (page, component, dashboard panel, marketing section) against the TAC Express 10-criterion premium rubric. Returns a per-criterion 0-10 score and a total /100, with concrete file:line evidence and a remediation plan. Trigger when the user asks "is this 10/10?", "score this UI", "audit this page", "is the design premium enough?", or as a pre-merge gate on any feature touching apps/web or apps/dashboard. Adapted from the affaan-m/everything-claude-code design-system Audit mode, refit to Violet Grid v6.
---

# TAC Express — UI/UX Premium Scoring Rubric (Violet Grid v6)

> The Violet Grid is a constraint identity. This rubric is how we know we're hitting it. Score is **measurable** — every criterion has a 0/5/10 anchor with file evidence.

---

## How to Score

For a target surface (page route, component file, dashboard panel):

1. **Read the surface** — load every file in scope (route + composed components used).
2. **Walk the 10 criteria** — for each, find evidence in code and in rendered DOM.
3. **Anchor the score** — 0 (absent / wrong), 5 (present but not premium), 10 (premium).
4. **Cite file:line** for every score below 10.
5. **Sum + verdict** — see § Verdicts.

Always include partial credit between anchors (3, 7, 8) — but only when justified by mixed evidence.

---

## The 10 Criteria

### 1. Token Discipline (Violet Grid Compliance) — 10 pts
Does every visual decision route through `globals.css` tokens? Zero raw hex, zero arbitrary px, zero forbidden Tailwind color classes, zero rebuilt shadcn primitives.

| Score | Anchor |
|---|---|
| 0 | Raw hex / `bg-blue-500` / `w-[347px]` / `rounded-full` / soft `shadow-md` blur present |
| 5 | Mixed: tokens for colors, but ad-hoc spacing or arbitrary values in 1-2 spots |
| 10 | 100% semantic tokens; ESLint `pnpm lint --max-warnings 0` passes; uses `.t-*` type scale and `tac-*` FUI utilities |

### 2. Hierarchy by Scale Contrast — 10 pts
Does the type scale create unmissable hierarchy? Display vs h1 vs body should be at least 2× size ratio with weight + tracking shifts.

| Score | Anchor |
|---|---|
| 0 | All text reads as one block — sub-2× ratio between hero and body, same weight |
| 5 | Two clear levels but weak contrast on third |
| 10 | Display (3rem/800/-0.045em) → h1 (1.75rem/700/-0.035em) → body (0.9375rem/400) → caption (0.75rem) — readable from 2 meters |

### 3. Rhythm & Whitespace — 10 pts
Are spacings on a 4/8/12/16/24/32/48/64/80 rhythm? Do dense regions vs breathing regions feel intentional?

| Score | Anchor |
|---|---|
| 0 | Random p-3, p-7, p-11 or arbitrary [13px] paddings |
| 5 | Mostly on-rhythm, 1-2 spots break |
| 10 | Every spacing on the 4-multiple; dense (`py-2 px-3`) and breathing (`py-12 px-8`) regions read as different gears |

### 4. Surface Depth (v6 Tier System) — 10 pts
Does the layout use `--surface-base/elevated/floating/interactive/hover/active`? Do tiers stack visibly without soft shadows?

| Score | Anchor |
|---|---|
| 0 | Flat `bg-card` everywhere, no perceived depth — OR hacked `shadow-2xl/blur` to fake depth |
| 5 | Two surface tiers used; floating panels read as flat against parent |
| 10 | Three+ tiers in use; brutalist offset shadow on `surface-elevated`; hover state shifts to `surface-hover` |

### 5. Motion Choreography (v6 3-Layer) — 10 pts
Are interactions on `instant` (mission-control), `smooth` (modal/sheet), `expressive` (hero entrance)? Do timings feel intentional, not stock?

| Score | Anchor |
|---|---|
| 0 | No motion, OR `transition-all duration-300` everywhere |
| 5 | Some motion, but mixed timings without intent |
| 10 | Hover = `--motion-instant`; modal = `--motion-smooth`; hero entrance staggered with `--motion-expressive` + `delay-100/200`; `prefers-reduced-motion` honored |

### 6. Mono Discipline (Tabular Data) — 10 pts
Every numeric value (AWB, weight, currency, timestamp) renders in `font-mono` with `tabular-nums`. Field keys carry `.tac-mono-label`.

| Score | Anchor |
|---|---|
| 0 | Numbers in font-sans; columns shift width as values change |
| 5 | Mono on KPIs only, not on table cells |
| 10 | Every numeric in `.t-data` / `.t-data-sm` / `.t-mono` / `.t-mono-sm`; every `<dt>` field key in `.tac-mono-label` |

### 7. State Choreography (Loading / Empty / Error / Stale) — 10 pts
Does each interactive surface have all four states designed? Skeletons match shape; empty states have intent; errors recover.

| Score | Anchor |
|---|---|
| 0 | Loading = blank screen, empty = "No results", error = throws |
| 5 | 2 of 4 states designed |
| 10 | All four: `animate-skeleton-pulse` skeleton matches final shape; empty state has CTA + icon + helpful copy; error has remedy + retry; stale has timestamp + refresh trigger |

### 8. Focus & Hover Polish — 10 pts
Does every focusable element have `tac-focus-premium` (1px outline + 8px bloom)? Does every interactive surface have `tac-hover-lift` or `tac-fui-hover`?

| Score | Anchor |
|---|---|
| 0 | Default browser focus (gray dotted ring); no hover state on cards |
| 5 | Custom focus on buttons only; cards have border-color shift only |
| 10 | `focus-visible:tac-focus-premium` on every focusable; `tac-hover-lift` on every clickable card; transform reduces on `:active` |

### 9. Content Voice (Copy + Density) — 10 pts
Is every label terse, technical, mission-control? No "Welcome back!" garbage. No empty buzzword paragraphs.

| Score | Anchor |
|---|---|
| 0 | Marketing tone in dashboard ("Hello, hope you're having a great day!") |
| 5 | Mostly tight, occasional fluff |
| 10 | Every label is `[VERB] [NOUN]` or `[NOUN] · [STATE]`; data tables have eyebrow `t-overline` labels; empty states are <12 words |

### 10. Anti-AI-Slop (Distinctiveness) — 10 pts
Does the surface read as bespoke TAC Express, or as generic Tailwind/shadcn template? Does it have at least one detail that couldn't be on any other dashboard?

| Score | Anchor |
|---|---|
| 0 | "Generic SaaS dashboard" — centered hero, gradient blob, three feature cards in a row, soft shadows, indigo CTAs |
| 5 | Has Violet Grid identity but at least one section reads as template (e.g., default shadcn Card grid) |
| 10 | Every section earns its layout; uses at least one FUI signature (`tac-scanline`, `tac-hazard-stripes`, `tac-mono-label`, asymmetric grid like 2/7/3, AWB hero with mono kerning); could be screenshot for an awwwards submission |

---

## Verdicts

| Total /100 | Verdict | Action |
|---|---|---|
| 90-100 | **Premium** ✅ | Ship. Document as a reference pattern in `tac-premium-patterns`. |
| 75-89 | **Strong** | Ship after closing the 1-2 lowest-scoring criteria. |
| 60-74 | **Acceptable** | Fix every criterion < 7 before shipping. |
| 40-59 | **Below standard** | Block merge. Schedule a redesign pass with `tac-premium-patterns` + `tac-design-tokens`. |
| 0-39 | **Reject** | The surface is not Violet Grid. Start over with `tac-brainstorming`. |

---

## Output Format

Always produce a verdict block like this:

```
SURFACE: apps/dashboard/app/(authenticated)/shipments/page.tsx
SCORE: 78/100 — STRONG

  1. Token Discipline           ▮▮▮▮▮▮▮▮▮▮  10/10
  2. Hierarchy by Scale         ▮▮▮▮▮▮▮▮▯▯   8/10  — h1 at 1.5rem; should be t-h1 (1.75rem)
  3. Rhythm & Whitespace        ▮▮▮▮▮▮▮▯▯▯   7/10  — line 84 uses p-5 (off-rhythm)
  4. Surface Depth              ▮▮▮▮▯▯▯▯▯▯   4/10  — uses bg-card only; no surface-elevated tier
  5. Motion Choreography        ▮▮▮▮▮▮▮▮▮▯   9/10
  6. Mono Discipline            ▮▮▮▮▮▮▮▮▮▮  10/10
  7. State Choreography         ▮▮▮▮▮▮▯▯▯▯   6/10  — empty state missing icon + CTA
  8. Focus & Hover Polish       ▮▮▮▮▮▮▮▮▯▯   8/10  — cards lack tac-hover-lift
  9. Content Voice              ▮▮▮▮▮▮▮▮▮▮  10/10
 10. Anti-AI-Slop               ▮▮▮▮▮▮▯▯▯▯   6/10  — KPI row reads as default shadcn grid

REMEDIATION (smallest path to 90+):
  - Replace bg-card with bg-surface-elevated on KPI cards (depth +5)
  - Apply tac-hover-lift to card.tsx:42 (focus +2)
  - Add empty-state icon + CTA to ShipmentsList.tsx:118 (states +3)
  - Asymmetric KPI grid (2/7/3 instead of 4-equal) (slop +3)
  
  Estimated lift: 78 → 91/100 (PREMIUM).
```

---

## When to Run This Skill

- ✅ **Pre-merge** on any UI-touching PR (gate at score ≥ 75)
- ✅ When user says "is this 10/10?", "audit this", "score this", "is this premium?"
- ✅ As the final step in `tac-code-review` for UI changes
- ✅ Before declaring a feature "done"

Never run on:
- Backend-only changes (services, schema, RLS)
- Generated files (Supabase types, prisma client, etc.)
- Test files (they are not user-facing surfaces)

---

## Cross-Reference

- Token compliance → `tac-design-tokens`
- Component pattern reference → `tac-premium-patterns`
- Motion vocabulary → `tac-micro-interactions`
- Anti-template detection → `rules/violet-grid-quality.md`
- Accessibility cross-check → `tac-accessibility`
