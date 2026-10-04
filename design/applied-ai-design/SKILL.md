---
name: applied-ai-design
description: Apply the Anthropic "Applied AI" frontend visual language to BMC components — calm warm palette, generous whitespace, serif display + clean sans body, restrained color, content-first layout. Use when redesigning a screen, creating a new panel, or auditing existing JSX/CSS for visual consistency. Trigger when user mentions "Applied AI design", "Anthropic style", "claude.ai look", or asks to redesign/restyle a BMC component.
---

# Applied AI Design — BMC

Visual language inspired by Anthropic's Applied AI demos and claude.ai. The stack is **React 18 + Vite + plain CSS** (no Tailwind, no shadcn). Apply principles via CSS variables and component-level className conventions, not by introducing new dependencies.

## Core principles

1. **Content first.** One primary action per view. Push chrome, badges, and meta to the periphery.
2. **Warm neutral palette.** Off-white background, warm gray text, single accent. No gradients, no shadows beyond `0 1px 2px rgba(0,0,0,.04)`.
3. **Typography hierarchy.** Serif (Tiempos/Source Serif/Charter) for display + headings. Sans (Inter/system-ui) for UI and body. Long-form copy gets serif.
4. **Generous whitespace.** Section padding `48–80px` desktop, `24–32px` mobile. Line-height ≥ 1.55 for body.
5. **Borders over fills.** Cards: 1px border `#E8E4DD` + 12–16px radius. Avoid heavy backgrounds.
6. **Restrained motion.** 150–200ms ease-out only. No bouncy springs.
7. **Accent discipline.** One accent color per surface. Use it for the single primary CTA + active states. Everything else is neutral.

## Token reference (drop into `src/styles/applied-ai.css`)

```css
:root {
  --aa-bg:        #FAF9F6;
  --aa-surface:   #FFFFFF;
  --aa-border:    #E8E4DD;
  --aa-text:      #1F1B16;
  --aa-text-mute: #6B645B;
  --aa-accent:    #C96442;   /* Anthropic clay */
  --aa-accent-ink:#FFFFFF;
  --aa-radius:    14px;
  --aa-radius-sm: 8px;
  --aa-shadow:    0 1px 2px rgba(0,0,0,.04);

  --aa-font-serif: "Source Serif 4", "Charter", Georgia, serif;
  --aa-font-sans:  "Inter", system-ui, -apple-system, sans-serif;

  --aa-space-1: 4px;  --aa-space-2: 8px;  --aa-space-3: 12px;
  --aa-space-4: 16px; --aa-space-5: 24px; --aa-space-6: 32px;
  --aa-space-7: 48px; --aa-space-8: 64px; --aa-space-9: 80px;
}
```

## Component patterns

- **Card:** `background: var(--aa-surface); border:1px solid var(--aa-border); border-radius: var(--aa-radius); padding: var(--aa-space-6);`
- **H1/H2:** `font-family: var(--aa-font-serif); font-weight: 500; letter-spacing: -0.01em;`
- **Body:** `font-family: var(--aa-font-sans); color: var(--aa-text); line-height: 1.6;`
- **Primary button:** filled accent, no border, radius `var(--aa-radius-sm)`, padding `10px 18px`.
- **Secondary button:** transparent, 1px border `var(--aa-border)`, hover → bg `#F2EEE7`.
- **Input:** 1px border, radius 8px, padding `10px 12px`, focus ring `2px var(--aa-accent)/20`.
- **Tabs:** underline-only, no pills.
- **Tables:** hairline rows, no zebra, label row uppercase 11px tracking 0.06em.
- **Money/USD:** tabular-nums, serif for hero figures only.

## Anti-patterns (reject in audit)

- Bootstrap-style colored badges (success/warning/danger) — replace with neutral chip + accent dot.
- Drop shadows on cards.
- Gradients on buttons or headers.
- Multiple accent colors on the same screen.
- Emoji icons inside operator UI (keep emojis only in chat content).
- Mixed border radii on the same surface.
- Inline color literals — must reference `--aa-*` vars.

## Workflow when invoked

1. Ask which screen/component to target if not specified. Confirm scope (single file vs module).
2. Read the file(s) and identify violations against the anti-patterns list.
3. Propose changes as a **before/after** diff (per BMC feedback rule `feedback_edits_approval.md`) — do NOT edit until user approves.
4. If `src/styles/applied-ai.css` doesn't exist, propose creating it with the token block above as step 1.
5. After approval, apply edits incrementally; run `npm run gate:local` before declaring done.

## Out of scope

- Do not introduce Tailwind, shadcn, or new UI libraries.
- Do not change business logic, calculations, or data shapes.
- Do not restyle PDF templates (those follow print rules, not screen rules).
