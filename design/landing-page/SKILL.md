---
name: landing-page
description: This skill should be used when the user wants to create a landing page, sales page, home page, lead-capture page, or any conversion-oriented page. Trigger phrases include "build a landing page", "make a sales page", "create a home page for my product", "I need a page to sell X", "landing for my SaaS/course/service", "lead capture page". It asks up to 3 questions, applies a proven psychological section order, generates the copy, and produces ready-to-use components.
---

# Landing Page

This skill builds landing pages that convert — not just pages that look nice. It combines a proven section order with real copy and production-ready code.

Analogy: a landing page is a salesperson who never sleeps. A good salesperson follows an order — grab attention, name the pain, show the cure, prove it works, ask for the sale. The section structure below is that script.

## Workflow

### Step 1 — Ask up to 3 questions (no more)

- What are you selling or offering? (product, service, SaaS, consulting)
- Who is the ideal customer? (the avatar — be specific)
- What is the single main action you want the visitor to take? (buy, book a call, sign up, join waitlist)

If the message already answers these, skip ahead.

### Step 2 — Build the section structure (proven psychological order)

1. **Hero** — clear value proposition + primary CTA. The visitor must understand what this is and why it matters in 5 seconds.
2. **Problem** — agitate the customer's pain. Make them feel the cost of not solving it.
3. **Solution** — how the product/service resolves that pain.
4. **Features** — 3-6 key items, written as **benefits, not specifications** ("ship in a weekend," not "built with X framework").
5. **Social proof** — testimonials, logos, numbers, results.
6. **Pricing** — if applicable; clear tiers, one highlighted.
7. **FAQ** — kill the top objections before they stop the sale.
8. **Final CTA** — restate the value and repeat the main action.

### Step 3 — Activate `ui-design` for the visual system

Hand off to the `ui-design` skill to generate the design system (style, palette, typography, spacing, dark mode) before writing components. Do not invent visual choices here.

**Delegation:** the design system itself is sourced per availability — if `ui-ux-pro-max` is installed, let it generate the system (optionally refined by `taste-skill`); if neither is installed, fall back to the embedded principles in `ui-design`. The landing page works either way; the originals just make it sharper. Never block on a missing dependency.

### Step 4 — Generate the copy, not just the code

This skill writes the **base copy for every section** — headline, subhead, body, CTA labels — tailored to the offer and avatar. Code without copy is half a landing page.

### Step 5 — Stack and optional add-ons

Default stack: **React + Vite + Tailwind**. Before building, ask whether the page needs:

- **Animations** → Framer Motion
- **A form** → React Hook Form
- **Analytics** → which provider (e.g. Plausible, GA, PostHog)

Only add these if the user wants them; do not bloat by default.

### Step 6 — Output

Deliver **ready-to-use components**, not prototypes — each section as a real component, wired to the design tokens, with the generated copy in place and empty/loading/error states handled where relevant (e.g. the form).
