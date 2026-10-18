---
name: using-anti-slop
description: Router for the anti-slop family — twenty-two vendored skills that keep an AI-built interface from looking templated (the centred hero, purple gradient, three icon cards, Inter everywhere) and raise it to a deliberate design. Use when building, redesigning, auditing or styling a web or mobile UI and the result must not read as AI slop; it names the one skill for the job and the order to chain them. Triggers include "anti-slop", "doesn't look AI-generated", "make it premium", "less generic", "redesign this", "pick a style", "design system", "audit my UI".
---

# Using Anti-Slop

**A router, not a rulebook.** Pick the row that matches the task, load that skill, follow it. The skills live verbatim in `skills/vendor/<name>/`; each one's `UPSTREAM.md` says where it came from.

## 1. Pick by task

| You are… | Load | Why this one |
|---|---|---|
| **Building a new page or landing** and it must not look templated | **`design-taste-frontend`** | reads the brief, infers a direction, strict pre-flight check before shipping |
| — same, and you want a second, differently-opinionated pass | **`hallmark`** | anti-AI-slop for greenfield, audits, redesigns, and extracting a design from a URL or screenshot |
| — or Anthropic's own take on a distinctive, intentional look | **`frontend-design`** | aesthetic direction, typography, colour and motion with a point of view |
| **Aiming for a high-end agency finish** | **`high-end-visual-design`** | exact fonts, spacing, shadows, card structure and animation that read as premium |
| **Motion-heavy landing** where layouts must not repeat | **`gpt-taste`** | randomised layout variance, AIDA structure, GSAP ScrollTrigger rules |
| **Design image first, then code to match it** | **`image-to-code`** | generates the design, analyses it, builds to it |
| **Upgrading an existing site** without breaking it | **`redesign-existing-projects`** | audits first, names the generic AI patterns, then replaces them |
| **Critiquing, polishing or hardening** a UI that already works | **`impeccable`** | 46 anti-slop patterns across 7 dimensions; commands such as critique, polish, distill, colorize |
| **Structuring the page** — hierarchy, grid, responsive composition | **`gridgeist`** | product-specific structure instead of the stock section stack |
| **Committing to a style** so every page does not look the same | **`minimalist-ui`** · **`industrial-brutalist-ui`** | one named, enforceable visual language each |
| **Choosing palette, font pairing, style** from a catalogue | **`ui-ux-pro-max`** | searchable data: 67 styles, 161 palettes, 57 font pairings |
| **Writing the design system down** so it holds across pages | **`design-system`** (tokens) · **`stitch-design-taste`** (`DESIGN.md`) | primitive → semantic → component tokens; an agent-readable anti-generic spec |
| **Applying a ready theme** to a page, deck or report | **`theme-factory`** | ten preset colour + font themes |
| **Implementing** with shadcn/ui + Tailwind | **`ui-styling`** | accessible components on Radix, utility-first styling |
| **Brand** — voice, identity, a brand-guidelines board | **`brand`** · **`brandkit`** | messaging and consistency; premium identity boards |
| **Generating a visual reference before code** | **`imagegen-frontend-web`** · **`imagegen-frontend-mobile`** | one mockup image per screen to build against |
| **Checking against interface guidelines** — accessibility, UX basics | **`web-design-guidelines`** | Vercel's Web Interface Guidelines review |
| Depending on the old taste-skill behaviour exactly | `design-taste-frontend-v1` | kept only for that; the default is `design-taste-frontend` |

## 2. The chain for a new page

1. **Direction** — `design-taste-frontend` (or `hallmark`); add a style skill if the brief names one.
2. **Structure** — `gridgeist`.
3. **Tokens** — `ui-ux-pro-max` to choose, `design-system` to write them down.
4. **Build** — the family's own `using-design` chain (`design-setup` → `design-rules`), `ui-styling` if the stack is shadcn/Tailwind.
5. **Polish** — `impeccable`.
6. **Done** — `design-ship-gate`. A page is not finished on a skill's say-so; it is finished when the gate passes and a real browser (`playwright-cli`) shows it.

For a redesign, start at `redesign-existing-projects` and join the chain at step 3.

## 3. Rules

- **Load one skill per step.** Two direction skills at once give two contradicting briefs; pick one, finish, then take a second opinion if needed.
- **Do not edit `skills/vendor/`.** To update a skill, re-copy it from upstream at a newer commit and update its `UPSTREAM.md`.
- **3D, canvas, motion or scroll effects** belong to **`using-web3d`**; come back here for the look.
- **If no row fits, say so** and use `using-design` directly.
