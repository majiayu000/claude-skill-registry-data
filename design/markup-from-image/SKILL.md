---
name: markup-from-image
description: "Use to turn a screenshot, Figma export, mockup, wireframe, or any UI image into semantic, unstyled HTML or JSX. A scaffold to style later, not a finished build. Not for extracting components or recreating the image as an asset."
---

# Markup from image

Look at the image, write the semantic structure, no styling. One block of markup the human styles afterward.

## Steps

1. Look at the image and the request. Work out the output format, the target file, where it goes, and the scope: full page, page section, component, or embedded media.
2. If they want it inserted into a file and didn't say where, ask one question before editing.
3. Read the target file or surrounding component first.
4. Find the landmarks and groups. Header, nav, main, sections, articles, asides, footer, headings, lists, forms, tables, buttons, links, media, and any screenshot of an app inside the image.
5. Write one contiguous unstyled block in the target syntax.
6. Use existing project components only if the human named them or asked for reuse. Check their API first and keep them inline.
7. Insert at the requested spot, or hand back the block if they only wanted a snippet.

## Rules

- Semantic HTML first. `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`, heading levels, `ul` and `ol`, `dl`, `table`, `form`, `label`, `button`, `a`, where they match.
- Every `<section>` gets a kebab-case `id` from its content or purpose. `id="hero"`, `id="features"`, `id="pricing"`, `id="testimonials"`.
- Decide the scope before drafting. When it's ambiguous, take the narrowest visible one.
- The prompt, the requested filename, and the insertion target are scope evidence. `hero.jsx`, `pricing-card.jsx`, `feature-section.jsx`, or "insert this section" mean a section or component, not a page, unless they said page.
- Page-level `<main>` only for a full page. Page-level `<header>` and `<footer>` only when the content is clearly the site's, not because it's the first or last band in a crop.
- Completely unstyled. No `class`, `className`, `style`, Tailwind utilities, styling props, layout or decorative wrappers, inline dimensions except on placeholder icon `<svg>`, or presentational attributes.
- One block. No new components, helpers, data arrays, maps, slots, or partials.
- Repeated UI becomes lists, description lists, table rows, fieldsets, or repeated inline markup. Not an abstraction.
- Keep the visible copy. Short placeholder copy only where text is unreadable.
- Normal written casing. Never preserve all caps, small caps, or all lowercase from the image. That's CSS. Keep real acronyms and brand capitalization.
- `<a href="#">` for navigation, destinations, page or route changes, downloads, external links, and button-looking CTAs like "Get started", "Learn more", "View details", "Pricing", "Sign in", "Sign up", unless they visibly submit a form.
- `<button type="button">` only for same-page actions that mutate, toggle, open, close, dismiss, or control visible state. `<button type="submit">` only for a visible form submit.
- Form controls get visible `label` elements when the image shows labels, `aria-label` when there's none, `fieldset` and `legend` for groups.
- Icons are a 20px by 20px `<svg>` with `role="img"` and a comment naming what the icon seems to mean. Never `<img>` for an icon placeholder.
- App screenshots, mockups, interface previews, dashboards, charts, maps, code editors, device screens, browser windows, and product shots inside the image are media. A placeholder image, not recreated markup.
- Meaningful images, logos, avatars, screenshots, and thumbnails get placeholder media elements. Empty `alt` only for decorative or unidentified imagery.
- No ARIA roles where native HTML already carries the meaning.
- A requested existing component can replace a raw element, but no styling props or classes unless the human asked for that component's API.

## Don't

- Style anything, infer colors, recreate spacing, add responsiveness, or add Tailwind classes.
- Turn the scaffold into a finished implementation.
- Componentize it.
- Guess an insertion point when editing a file.
- Invent sections, copy, data, or behavior that isn't visible or asked for.

## Check

- No new `class`, `className`, `style`, utilities, or styling props unless explicitly requested through existing components.
- Lists, tables, forms, nav, buttons, links, headings, landmarks, and media all use native semantics, with accessible names on form controls.
- Every `<section>` has its `id`.
- Scope matches the prompt, filename, insertion target, and what's visible. An isolated section isn't wrapped in `<main>`.
- Casing is written casing.
- Every `<a>` has an `href`, `#` when unknown. No `<button>` exists only because a link was styled like one.
- Icon placeholders are 20px `<svg>` with only a comment, no `<title>`, no `<img>`.
- Embedded app screenshots are placeholder media.
- One contiguous block, no abstractions. Inserted where asked. Project checks run.
