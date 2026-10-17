---
name: html-craft
description: Write semantic, accessible HTML — structure before styling, real controls, valid markup.
version: 1
triggers: html, semantic html, accessible markup, write html
category: Engineering & code
blurb: Write semantic, accessible HTML — structure before styling, real controls, valid markup.
archetype: knowledge
example: Rewrite this page as semantic, accessible HTML.
---

# HTML Craft

HTML is the foundation: get the structure and semantics right and accessibility, SEO, and maintainability come almost free.

## When to use
- Any user-facing page or component markup.
- Accessibility fixes and markup reviews.

## Method
1. **Structure first**: one `<h1>` per page, logical heading order; landmarks (`header`/`nav`/`main`/`footer`); sections with real meaning.
2. **Semantic elements**: `nav`, `main`, `article`, `section`, `figure/figcaption`, `time` — ask "what is this?" before reaching for `div`.
3. **Real controls**: `button` for actions, `a` for navigation, `label` bound to every input, `fieldset`/`legend` for groups; never clickable `div`s.
4. **Text alternatives**: meaningful `alt` for content images; empty `alt` for decorative; captions for media.
5. **Data tables**: only for data — `<thead>`, `<th scope>`, `<caption>`; never for layout.
6. **Document hygiene**: `lang` on `<html>`, viewport meta, charset first, descriptive `<title>`.
7. **ARIA — sparingly**: native semantics first; ARIA only to fill real gaps, never to fake controls.
8. **Validate**: W3C validator / htmlhint clean; no invalid nesting (`<a>` in `<a>`, block in inline).

## Quality gates
- [ ] Validator-clean markup.
- [ ] Keyboard-only pass of every interactive element.
- [ ] Every image has appropriate alt text; every input has a label.
- [ ] Heading order logical; one main landmark.

## Red lines
- No `div`/`span` with click handlers.
- No layout tables; no missing `lang`/`title`.

## Related
`ux-ui-design` · `frontend-engineering` · `javascript-engineering`.
