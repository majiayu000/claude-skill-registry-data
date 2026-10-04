---
name: ecc-taste-dials
description: Brief Inference and The Three Dials calibration system. Use when starting any frontend layout, determining composition symmetry, spacing density, and animation intensity budget based on vibe keywords and target audience.
version: "1.0.0"
verified_date: 2026-06-01
category: design
---

# Brief Inference & The Three Dials

## Purpose
Enforce a disciplined styling calibration system that reads the room first, preventing default AI styling choices by mapping inferred design contexts to specific layout, animation, and spacing dials.

## When to Use This Skill
- Initial layout planning of any new page, portfolio, dashboard, or application.
- Defining macro styling, typography pairings, spacing rhythm, and CSS/Tailwind budgets.
- Redesigning existing interfaces to match or modernly elevate visual tones.

## Output Format / Delivery
Provide a one-line inferred design direction declaration before outputting any code, and document inferred dial values (`DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY`) in source code comments.

## Behavior Rules
1. **Always read the room first** — output the "Pre-Flight Design Read" declaration before coding.
2. **Never utilize default AI styling palettes** (stark saturated gradients, generic dark-mode boxes) without matching inferred tone.
3. **Always document dial settings in code comments** to make design engineering decisions explicit and inspectable.
4. **Never over-animate public sector or regulated sites** — respect tight motion budgets for accessibility and compliance.

## Maintenance Notes
This skill is locked for core visual calibration logic. Update if additional layout presets or dial-scale parameters are introduced.

---

## Phase 1: Brief Inference (Read the Room First)

Before writing code or defining layouts, infer the user's specific context. Avoid default AI aesthetics by analyzing the following signals:

1. **Page Classification**: Identify the layout type (landing page, solo portfolio, creative agency portfolio, editorial/blog, B2B SaaS, public sector).
2. **Vibe Indication**: Analyze tone keywords used in the request (e.g. "minimalist", "calm", "editorial", "Apple-y", "Awwwards-style", "brutalist", "technical hacker").
3. **Reference Targets**: Use brand colors, named competitors, linked URLs, or aesthetic benchmarks.
4. **Audience Demographics**: Adjust spacing, density, and layout complexity to suit target users (e.g., procurement committees vs. design recruiters).
5. **Brand Constancy**: Identify and preserve existing logos, typography assets, or designated color registers.
6. **Subtle Restraints**: Prioritize compliance constraints (regulated industries, public-sector accessibility rules, high-contrast readability).

### Pre-Flight "Design Read" Requirement
Before generating any HTML or CSS, output a single-line declaration of your inferred design direction:
`Reading this as: <page kind> for <audience>, with a <vibe> language, leaning toward <design system or aesthetic family>.`

*Example:*
> Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind utilities + Geist + restrained motion.

---

## Phase 2: The Three Dials Heuristic

Modulate layout, animation limits, and spacing density using three dynamic dials. Unless overridden conversationally by the user, infer these values from the "Design Read" and document their values in comments.

* **`DESIGN_VARIANCE` (1–10)**: Controls composition symmetry. `1` = mathematical grid symmetry; `10` = artistic, bento-breaking asymmetry.
* **`MOTION_INTENSITY` (1–10)**: Controls animation budget. `1` = purely static page; `10` = complex physics and scroll-scrubbed GSAP timelines.
* **`VISUAL_DENSITY` (1–10)**: Controls data-compactness. `1` = sparse, airy gallery; `10` = high-density instrument dashboard.

### Dial Inference Matrix

Use the table below to map the user's vibe and context to exact dial settings:

| Vibe & Context Signals | DESIGN_VARIANCE | MOTION_INTENSITY | VISUAL_DENSITY |
|:---|:---:|:---:|:---:|
| "minimalist / clean / calm / editorial" | 5-6 | 3-4 | 2-3 |
| "premium consumer / Apple-y / luxury" | 7-8 | 5-7 | 3-4 |
| "playful / Awwwards / agency / creative" | 9-10 | 8-10 | 3-4 |
| "trust-first / public-sector / regulated" | 3-4 | 2-3 | 4-5 |
| "landing page / marketing / default SaaS" | 7 | 6 | 4 |
| "SaaS dashboard / telemetry console" | 5 | 4 | 7-8 |
| "redesign - preserve existing structure" | match source | +1 | match source |
| "redesign - total modern overhaul" | +2 | +2 | match source |

---

## Phase 3: Presets by Use Case

| Use Case | DESIGN_VARIANCE | MOTION_INTENSITY | VISUAL_DENSITY |
|:---|:---:|:---:|:---:|
| **Landing Page (SaaS / Mainstream)** | 7 | 6 | 4 |
| **Landing Page (Creative / Agency)** | 9 | 8 | 3 |
| **Landing Page (DTC / Consumer)** | 7 | 6 | 3 |
| **Portfolio (Designer / Studio)** | 8 | 7 | 3 |
| **Portfolio (Developer / Engineer)** | 6 | 5 | 4 |
| **Editorial Layout / Blog** | 6 | 4 | 3 |
| **Public-Sector Service** | 3 | 2 | 5 |
