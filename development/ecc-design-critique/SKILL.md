---
name: ecc-design-critique
description: Visual Design Critique and Pre-Flight Audit framework. Use when auditing layout hierarchy, typography contrast/alignment, content data realism, brand logo formatting, and section zigzag/repetition rhythm before shipping a frontend.
version: "1.0.0"
verified_date: 2026-06-01
category: design
---

# Visual Design Critique & Pre-Flight Audit

## Purpose
Enforce a comprehensive visual audit and layout critique protocol to verify typography, spacing containment, layout asymmetry, and content realism before shipping any user interface.

## When to Use This Skill
- Running a pre-flight visual audit on a completed landing page or web application screen.
- Checking contrast compliance (WCAG AA) on CTAs, text, and form inputs.
- Ensuring organic data realism and banishing placeholder boilerplate.
- Auditing layout repetition, grid cells, and section alignment rhythms.

## Output Format / Delivery
Provide a structured, categorized design critique report or direct code updates that satisfy the pre-flight checklists. Categorize audit feedback into: Typographic, Layout, and Content.

## Behavior Rules
1. **Never use standard broad placeholder copy** (lorem ipsum, John Doe, Acme Corp, duplicate CTAs) — all copy must be contextual, realistic, and unique.
2. **Never allow display descenders to clip on italics** — enforce vertical clearance margins and leading bounds.
3. **Always ensure CTA text remains on a single line on desktop viewports**.
4. **Never reuse identical section layout column counts consecutively** — break rhythms to prevent repetitive grid fatigue.

## Maintenance Notes
This skill is locked for pre-flight design checks. Update if additional visual standards or logo wall asset rules are established.

---

## Phase 1: Typography & Contrast Pre-Flight Checklist

* **Italic Descender Clearance**: When using italicized words in display headlines, standard `leading-none` or `leading-[1]` will clip the bottom of descender letters (`y, g, j, p, q`). You MUST enforce `leading-[1.1]` minimum on the wrapping element and reserve vertical space using padding or margin (`pb-1` or `mb-1`).
* **Button Contrast Validation**: Before shipping any Call-To-Action (CTA), verify the readability of the text color against the button background. White text on light buttons or dark text on dark surfaces is banned. Ensure contrast meets a minimum WCAG AA ratio of `4.5:1` (or `3:1` for large display text).
* **CTA Button Wrap Ban**: Button text MUST reside on a single line at desktop viewports. Labels that wrap to multiple lines are a Pre-Flight failure. Shorten the copy to $\leq 3$ words or broaden the button width.
* **No Duplicate CTA Intent**: Do not duplicate the same functional intent on a single page using different phrasing (e.g. do not mix "Contact Us" and "Get in touch" or "Get started" and "Sign up free"). Standardize on a single, clean label for each intent across navigation, hero, and footer sections.
* **Form Contrast Heuristic**: Form labels, input fields, border states, focus rings, placeholder text, and error indicators must pass WCAG AA contrast rules against the section background. Light gray inputs on near-white sections are forbidden.

---

## Phase 2: Layout, Rhythm & Asymmetry Critique

* **Hero Viewport Containment**: The primary Hero section (Headline, Subtext, and CTA) must fully fit inside the initial desktop viewport.
  * Headline size must map logically to copy length (e.g. `text-4xl md:text-5xl lg:text-6xl` for standard headers, and `text-6xl md:text-7xl` only for extremely brief 3-5 word headlines).
  * Subtext must not exceed **20 words** and must occupy at most 3-4 lines.
  * **Top Padding Ceiling**: Hero top padding must not exceed `pt-24` (≈6rem) on desktop to prevent hero content from floating too low.
  * **Hero Stack Cap**: Maximum of 4 text elements in the hero (1. Eyebrow/Brand strip, 2. Headline, 3. Subtext, 4. CTAs). Move tagline builders, client logs, pricing details, and bullet points to sections directly below the hero.
* **Section Layout Repetition Ban**: A landing page or portfolio must not reuse the same layout pattern across different sections. If you use a 3-column bento card grid or a split-screen zigzag in one section, you are forbidden from using that exact layout in adjacent sections. Vary the layout using vertical lists, hero tiles, marquees, or accordions.
* **Zigzag Alternation Cap**: Banish continuous "left-image/right-text" then "left-text/right-image" zigzag repetitions. Cap alternating split layouts to **maximum 2 consecutive sections**, breaking the rhythm with a full-width highlight, vertical grid, or marquee.
* **Bento Grid Cell Count Discipline**: A bento grid must contain exactly as many cells as there is unique content. Do not output blank placeholders or empty cells to satisfy a grid structure.
* **Bento Background Diversity**: A multi-cell bento grid must not consist of white-on-white text cards only. At least 2-3 cells must contain visual variation, such as an editorial photograph, an inline code window, a graphic pattern, or a distinct background tint.
* **Eyebrow Restraint**: Section headlines must not use the standard "small caps wide-tracking eyebrow" (e.g., `font-mono text-xs uppercase tracking-[0.2em]`) automatically in every section. Limit eyebrows to **maximum 1 instance per 3 page sections** (the Hero counts as 1). Drop them entirely for other sections.
* **Split-Header Ban**: The layout pattern featuring a wide H2 headline on the left and a small body paragraph on the right (split grid columns) is banned as a default. Stack them vertically with a clean max-width of `65ch`.

---

## Phase 3: Visual Content & Real-Data Discipline

* **Prohibit Fake Boilerplate**: Emojis are strictly banned from production code. Placeholder strings (such as "Lorem Ipsum", "John Doe", and "Acme Corp") are forbidden.
* **Organic Data Realism**: All telemetry numbers, stats, and metrics must reflect organic, complex values (e.g., `47.2%` or `1.84ms` instead of exact rounded integers like `50%` or `2.00ms`).
* **Visual Asset Priorities**:
  1. Generate high-quality aspect-ratio correct graphics using environment image-generation tools first.
  2. Use descriptive-seeded real placeholders (e.g. `https://picsum.photos/seed/{seeded-context}/{w}/{h}`) for stock mockups.
  3. Div-based raw HTML "fake screenshots" representing dashboards or terminal code blocks are banned. Use actual functional mini-component previews.
* **Social Proof Logo Wall**:
  * Utilize crisp SVG logo marks from community CDNs (e.g., Simple Icons `https://cdn.simpleicons.org/{slug}/ffffff`) rather than plain-text spans.
  * Ensure logo SVGs render clearly in both dark and light modes.
  * **Logo-Only Constraint**: Customer logo walls must display logo graphics only. Banish descriptive metadata labels (such as "payments", "cloud hosting") below customer marks.
* **Quote Length Constraints**: Testimonial quote bodies must not exceed **3 lines** of copy. attribution must include the customer's name, role, and company.
* **System-Wide Page Theme Lock**: A single page must adhere strictly to ONE base theme (light or dark). Flipping between stark light sections and dark-mode sections inside a single page scroll reads as a layout bug and is forbidden.
