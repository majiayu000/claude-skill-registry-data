---
name: raw
description: Completely unstyled browser defaults — honest HTML, brutal simplicity, zero CSS.
---
# Raw
## Mission
Deliver semantic HTML with zero styling — the browser's built-in defaults are the design system. Honest, fast, and universally accessible.
## Brand
### 🎨 Colors
- `#0000EE` — Link (browser default)
- `#551A8B` — Visited link (browser default)
- `#000000` — Text (browser default)
- `#FFFFFF` — Background (browser default)
- `#808080` — Secondary text (browser default)
- `#FF0000` — Error/validation (semantic only)
### 🔤 Typography
- Heading font: Times New Roman (serif, browser default)
- Body font: Times New Roman (serif, browser default)
- Type scale: browser defaults — `1rem` base, headings at `2rem`/`1.5rem`/`1.17rem`/`1rem`/`0.83rem`/`0.67rem`
### 📐 Spacing
- No grid system — flow layout only
- Section padding: `1rem` (browser default block margins)
- Card gaps: none (no cards, just semantic sections)
### 🧩 Components
- Buttons: native `<button>` elements, no styling override
- Cards: not used — prefer `<section>`, `<article>`, `<fieldset>`
- Nav: `<nav>` with unordered list, browser default indentation
- Hero: `<h1>` followed by `<p>`, no hero section abstraction
- Footer: `<footer>` with `<small>`, browser default styling
### ♿ Accessibility
- Maximum accessibility by default — browser semantics are inherently accessible
- No contrast issues to fix — system colors guaranteed WCAG AAA
- Focus states: browser default focus rings preserved and honored
- Reduced motion: automatically respected via `prefers-reduced-motion` in browser
- Font size minimums: no override needed — user agent stylesheet handles it
### ✍️ Writing Tone
- Direct, unadorned, truthful
- No marketing language — just information architecture
- Labels match element semantics: "Submit" not "Get Started Free"
## Do / Don't
### ✅ Do
- Use semantic HTML elements exclusively (`<main>`, `<nav>`, `<article>`, `<aside>`)
- Let the browser handle all visual presentation
- Include `<meta name="viewport">` for mobile rendering
- Use `<table>` for tabular data with `<caption>` and `<th>` scope
- Validate HTML — valid markup is the only quality gate
### ❌ Don't
- Add any CSS whatsoever — no `<style>`, no `style=""`, no stylesheets
- Use `<div>` or `<span>` when a semantic element exists
- Nest `<section>` without a heading
- Override browser focus rings or selection colors
- Add JavaScript unless strictly required for form submission fallback
## Quality Gates
- [ ] Valid HTML5 (W3C validator passes with zero errors)
- [ ] No CSS present anywhere in the document
- [ ] Every `<section>` and `<article>` has a heading
- [ ] Forms use `<label>` with `for` attributes, `<fieldset>` + `<legend>` for groups
- [ ] Images have `alt` text; tables have `<caption>` and `<th scope>`
- [ ] Page renders readably with JavaScript disabled