---
name: "ui-design-guardrails"
description: "Use before writing or restyling any UI, landing page, or component so the output matches the actual brand instead of defaulting to generic AI-template styling."
---

# UI design guardrails

Applies to any task that produces visual UI: a landing page, a hero, a redesign, a component, a Tailwind theme. Follow this before writing the first line of markup.

## 1. Write the brief before the code

State these five lines in the response first. If a line is unknown, ask — do not invent a brand.

- Business and what it sells
- Who is looking at it, on what device (assume mobile-first unless told otherwise)
- Three adjectives for the mood, none of which are "modern", "clean", or "premium"
- One real reference (a named brand, a site, or a `DESIGN.md` from `VoltAgent/awesome-design-md`)
- The one signature element that belongs to this business and no other

If the brief cannot be answered, the design will be generic. Stop and ask instead of shipping a template.

## 2. Banned by default

Do not produce these unless the user explicitly asks for them by name:

- Dark background with a purple/violet radial glow, optionally plus cyan and magenta
- Indigo-to-purple or purple-to-pink gradient headline text
- A row of three glassmorphism cards with `backdrop-blur` and a border glow
- Centered hero: badge pill, huge headline, one-line subhead, two buttons, logo strip
- Animated beams, sparkles, meteors, or a grid/dot pattern added "for depth"
- Inter or Geist at default weights for every piece of text on the page
- Emoji used as icons; `shadow-2xl` and `rounded-2xl` on everything
- 100vh hero with nothing signalling content below the fold
- Copy in the form "Elevate your ___" / "___, reimagined"

These are the defaults every AI-built site already has. Shipping them is the failure mode this skill exists to prevent.

## 3. Decide tokens before components

Write these into CSS variables or the Tailwind theme first, and justify each in one clause:

- One base surface, one raised surface, one ink colour, one muted ink
- Exactly one accent hue, taken from the brand (product photos, logo, existing materials) — not from a component library's demo
- A type pairing with a stated reason, and a scale of at most five sizes
- One spacing step (4px or 8px), one border radius, one shadow

Everything after this uses only those tokens. A colour that is not in the token list does not go in the page.

## 4. Depth comes from layering, not from glow

When a surface looks flat, in this order: increase whitespace; add one low-chroma gradient in the *same* hue family as the surface; add 3–5% grain to kill banding; add exactly one elevation shadow. At most one animated background element per page, disabled under `prefers-reduced-motion` and below 768px.

Never add a second and third accent hue to create "atmosphere".

## 5. Content leads

If the business has real photography, products, or work to show (fashion, food, tattoo, interiors, portfolio), the imagery is the design and the background stays quiet. Reach for background effects only when there is genuinely nothing to show — dev tools, APIs, abstract SaaS.

## 6. Libraries are ingredients, not a look

shadcn/ui for primitives. At most one borrowed showpiece component (Magic UI, Aceternity, cult/ui) per page, and its colours are rewritten to the tokens from step 3 before it ships. Never paste a component with its demo palette intact.

## 7. Self-check before declaring done

- Body text contrast ≥ 4.5:1, large text ≥ 3:1 — check, do not assume
- Render or screenshot it at 390px wide and look at it
- Answer honestly: could this page be swapped onto a different business by changing the words? If yes, the accent, the type pairing, or the signature element is not doing its job — fix one of them before finishing
- Name the design decisions in the response so they can be argued with

## 8. Never mass-apply

Do not apply one background treatment, palette, or "house style" across multiple projects or deployments. Each project gets step 1 to step 3 of its own.