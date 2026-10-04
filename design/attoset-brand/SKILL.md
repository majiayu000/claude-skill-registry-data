---
name: attoset-brand
description: AttoSet brand + design system. Use whenever building, editing, or reviewing any AttoSet website UI, component, page, copy, or visual asset to keep colors, typography, spacing, motion, and tone on-brand.
---

# AttoSet Brand & Design System

Apply this on every UI/visual/copy task for the AttoSet site.

## 1. Personality
Modern · intelligent · bold · premium · minimalistic · enterprise-ready.
Restraint over decoration. Confidence over noise. Every screen should feel engineered.

## 2. Color tokens

| Token | Value | Use |
|---|---|---|
| `--ink` | `#0A0A0A` | primary text, primary buttons, dark feature panels |
| `--ink-soft` | `#3A3A3A` | secondary text |
| `--muted` | `#6B6B6B` | tertiary text, captions |
| `--line` | `#ECEAE7` | hairline borders, dividers |
| `--bg` | `#FFFFFF` | base background |
| `--bg-warm` | `#FBFAF8` | alternating off-white sections |
| `--orange` | `#FF512A` | CTAs, AI/Atto, key highlights ONLY |
| `--orange-600` | `#E8431F` | hover state |
| `--peach` | `#FFE9E1` | soft tints, gradient stops |

**Orange is surgical.** It marks the most important action or any Atto/AI moment — not large fills of body UI. White + ink carry the structure; orange punctuates.

**Light mode only.** Never ship a `prefers-color-scheme: dark` default. Dark panels are an intentional design choice (e.g. a security/agents band), not theming.

## 3. Typography
- **Display / headings:** Bricolage Grotesque (tight tracking, weight 600–800). Large, confident, mostly `text-balance`.
- **Body / UI:** Geist Sans.
- **Eyebrows / labels / code:** Geist Mono, uppercase, `tracking-[0.2em]`, small, often in `--muted` or `--orange`. This monospace label is a signature element — use it above section headings.
- Headline sizes are big (hero `clamp(2.75rem, 6vw, 5rem)`). Body 16–18px, relaxed leading.

## 4. Layout & spacing
- Max content width ~1200px (`Container`).
- Generous vertical rhythm: sections ~`py-24`/`py-32`.
- Alternate `--bg` and `--bg-warm` between sections for quiet structure.
- Hairline borders (`--line`), rounded corners: cards `rounded-2xl`/`rounded-3xl`, buttons pill (`rounded-full`).
- Atmosphere: soft peach→orange **radial** glows behind hero & final CTA; subtle dot/grid textures for depth. Keep it tasteful.

## 5. Components
- **Buttons:** primary = ink fill / white text, pill, arrow on hover. Accent = orange fill. Secondary = white with `--line` border. Always have hover motion.
- **Eyebrow:** mono uppercase label, optionally a small orange dot.
- **Cards:** white, hairline border, soft shadow, hover lift.
- **Product mockups:** build in code — crisp table/kanban/calendar/gantt/dashboard/Atto-chat panels. Rounded, layered, subtle shadows. This is how we show the product.

## 6. Motion (Framer Motion)
- One orchestrated hero load: staggered fade+rise reveals.
- Scroll-triggered section reveals via a `Reveal` wrapper (`whileInView`, `once`, ~16–24px rise).
- Hover micro-interactions on buttons/cards. Respect `prefers-reduced-motion`.

## 7. Icons
`lucide-react`, stroke ~1.5–1.75, consistent sizing. Modern and clean — no emoji in product UI.

## 8. Voice & copy
Confident, concise, intelligent. Speak to organizations/teams. Lead with outcomes (build, automate, scale, execute). Highlight Atto (AI assistant) and autonomous AI Agents as differentiators. Avoid hype clichés; sound enterprise-credible.

## 9. Do / Don't
- ✅ White canvas, surgical orange, mono eyebrows, crisp code mockups, big confident type.
- ❌ Purple gradients, generic Inter/Roboto, dark-mode default, orange everywhere, stocky clip-art, cramped layouts.
