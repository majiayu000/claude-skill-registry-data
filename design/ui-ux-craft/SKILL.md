---
name: ui-ux-craft
category: frontend
description: Use when designing or building any screen, section or component that a user sees — visual hierarchy, typography, colour, spacing, states, forms and how to avoid the generic AI look.
source: anthropics/skills frontend-design (Apache-2.0), pbakaus/impeccable (Apache-2.0), vercel-labs/web-interface-guidelines (MIT), shadcn-ui/ui (MIT), ibelick/ui-skills (MIT), adapted
---
# UI/UX Craft

## Overview

Visual design is not decoration bolted on at the end — hierarchy, spacing, and states are load-bearing parts of the UI. The two most common failures are structural sameness (every screen reads as the same generic SaaS template) and a happy-path-only build (no loading/empty/error states).

**Core principle:** Decide the mode first — Marketing or App — then build to the quality floor: one primary action, systematic spacing, semantic tokens, and every state designed, never just the happy path.

## Pick the mode first

| | Marketing / landing | App / product UI |
|---|---|---|
| Visitor wants to | decide and act | complete a task |
| Optimise for | one strong idea per section, a visual direction grounded in the product's actual subject matter, generous whitespace, real imagery | density appropriate to the task, predictability, consistency over novelty |
| Call to action | a single primary CTA, repeated | no persuasion chrome — tables/forms/filters done right |

Ground the direction in the real subject (industry, materials, audience) — a toy brand's landing page and a financial dashboard should never default to the same look.

## Rules

### Hierarchy
- One primary action per view. Emphasise with size → weight → colour, in that order; de-emphasise secondary content instead of shouting the primary one louder.
- Squint test: if you can't tell what matters most with eyes half-closed, the hierarchy isn't set yet.

### Spacing & rhythm
- Use the token scale: `gap-1 gap-2 gap-3 gap-4 gap-6 gap-8 gap-12 gap-16 gap-24` (4px steps).
- Proximity: tight spacing inside a group, ≥2× that spacing between sections.
- More space above a heading than below it; align everything to one left edge or grid.

### Typography
- `text-xs` … `text-6xl`; body is `text-base` (16px); line-height 1.5–1.7 for body, 1.1–1.25 for display.
- Measure 60–75ch (`max-w-prose`); max two font families; weights 400/500/600/700 only.
- `text-balance` on headings, `text-pretty` on body paragraphs; `tabular-nums` on prices and stats.
- No letter-spacing hacks except a sparing uppercase small label — never a decorative eyebrow (see below).

### Colour
- Semantic tokens only (`bg-primary`, `text-muted-foreground`, `border-border`) — never raw palette classes or hex.
- Neutrals carry ~90% of the UI; one accent colour per view.
- Contrast ≥4.5:1 body text, ≥3:1 large text; status is never colour-only (pair with icon + text).
- Dark mode comes from the tokens, never a manual `dark:` override. On a coloured surface, tint secondary text from that hue — never grey-on-colour.

### Depth & shape
- One radius family (`--radius`, `rounded-md`/`rounded-lg`/`rounded-full`); a nested radius is ≤ its parent's.
- Shadows by elevation (`shadow-sm`/`shadow-md`/`shadow-lg`); borders use `border-border`.
- Avoid "everything is a card" as the page structure, and never nest a card inside a card.

### States — non-negotiable for every data view and every control
- Loading: a skeleton that mirrors the final layout — never a spinner-only full page.
- Empty: explain why, give one next action.
- Error: say what happened and how to recover, shown where it happened.
- Success: visible feedback (toast, inline confirmation, or state swap).
- Every control styles hover, `focus-visible`, active, disabled, and pending.
- Destructive actions go through `AlertDialog` or an undo window — never a silent delete.

### Forms
- Visible `<label>` for every field — a placeholder is not a label. Helper text under the field, not hidden in a tooltip, unless the field is self-explanatory.
- Inline error next to the field, plus `aria-invalid` + `aria-describedby` pointing at it.
- Validate on blur/submit, not on every keystroke; never block paste.
- Correct `type`/`inputmode`/`autocomplete`; on submit, focus the first invalid field.
- The submit button keeps its label and shows a spinner while pending (compose `Spinner`, don't swap the text to "Loading…").

### Copy & content
- UI copy in the app's locale. Buttons name the action ("Aboneliği başlat", not "Gönder"/"Submit").
- Errors state the problem and the fix, and don't apologise. No lorem ipsum — use realistic content.
- Numbers and currency through `Intl.NumberFormat`, dates through `Intl.DateTimeFormat`, both locale-aware.

### Imagery & icons
- One icon library for the whole app (e.g. `lucide-react`); consistent size and stroke width.
- `aria-hidden` on decorative icons; never emoji standing in for an icon.
- A placeholder visual is a tasteful SVG/illustration, not a grey box, in shipped UI.

### Motion
- Only `transform`/`opacity`; ≤200ms for interaction feedback; never `transition-all`.
- `motion-reduce:` respected. Prefer no animation over a gratuitous one; at most one purposeful moment per marketing page, not a fade-up on every section.

### Anti-generic-look list — refuse these unless the brief explicitly asks for them
- No eyebrow/kicker label above a heading — the heading carries its own weight.
- No gradient text; no purple or multicolour gradient washes by default.
- No "SaaS card kit": identical rounded cards, one radius and the same `rgba(0,0,0,.1)` shadow under everything, as the whole page's structure.
- No emoji as icons; no thick coloured `border-left`/`border-right` on cards or alerts; no nested cards; no decorative glassmorphism/blur.
- No centred-everything layout by default; no section numbers (01/02/03) unless the content really is a sequence.
- No AI-tell palette picked by category instead of the brief: warm cream (`#F4F1EA`) + terracotta accent, or near-black + a single acid-green/vermilion accent, are defaults, not a direction you chose.
- Inter (or any system sans) "because it's the default" — pick a typeface deliberately for the subject.

## Worked Example

```tsx
// ❌ generic hero: centred everything, eyebrow label, gradient text,
// no real hierarchy beyond font-size, no states considered
<section className="text-center py-24">
  <p className="text-sm uppercase tracking-widest text-muted-foreground">Welcome</p>
  <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-500 to-pink-500 bg-clip-text text-transparent">
    The best way to manage tasks
  </h1>
  <p className="mt-4 text-muted-foreground">Get started today.</p>
  <Button className="mt-6">Submit</Button>
</section>

// ✅ one idea, real copy, clear hierarchy, semantic tokens, named action
<Container className="py-16 sm:py-24">
  <div className="flex max-w-prose flex-col items-start gap-4">
    <h1 className="text-balance text-4xl font-semibold text-foreground sm:text-5xl">
      Plan the sprint in the time it takes to make coffee
    </h1>
    <p className="text-pretty text-lg text-muted-foreground">
      Turn a backlog into a week your team can actually run.
    </p>
    <div className="flex flex-wrap gap-3 pt-4">
      <Button size="lg">Start planning</Button>
      <Button size="lg" variant="ghost">See how it works</Button>
    </div>
  </div>
</Container>
```

The rewrite drops the eyebrow and gradient, picks one hierarchy path (size → weight → colour), names each action, keeps one primary CTA with a quieter secondary, and spaces everything with `gap` from the token scale — the atoms carry no margins of their own.

## Common Mistakes

- Shipping a view's happy path only — no loading skeleton, no empty state, no error recovery.
- Raw palette classes (`bg-blue-500`, `text-gray-600`) or hex instead of semantic tokens.
- An eyebrow label, gradient text, or identical icon-card grid because it's the default, not because the brief asked for it.
- Validating on every keystroke, or not focusing the first invalid field on submit.
- A placeholder instead of a `<label>`.

## Red Flags

- A screen with only a "loading" or only a "has data" render path in the diff.
- `bg-gradient-to-r` on text, or a palette colour class, anywhere in a component.
- More than one accent colour or more than one primary CTA in a single view.
- A card nested inside a card, or every section built from the same icon+heading+text card.
