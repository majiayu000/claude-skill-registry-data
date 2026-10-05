---
name: blog-post
description: |
  Long-form editorial blog post layout with hero image, typography hierarchy,
  pull quotes, and code blocks. Use for "blog post", "article", "essay".
triggers:
  - "blog post"
  - "article"
  - "essay"
  - "editorial"
  - "long form"
df:
  mode: prototype
  platform: desktop
  scenario: content
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Blog Post Skill

Produce a single long-form editorial article page.

## Structure
1. **Header** — publication wordmark, minimal nav (3–4 links), search icon.
2. **Hero** — full-bleed cover image (CSS gradient placeholder), title in
   display font, byline (author · date · read time), topic tag.
3. **Body** — max-width 65ch, generous line-height (1.65–1.8).
   - Subheadings in display font.
   - Pull quotes: left border accent, larger type, lighter weight.
   - Inline code: mono, subtle background.
   - Code blocks: dark background, syntax-colored via CSS classes.
   - Images: full-bleed or inset with caption.
4. **Footer** — author bio card, related articles (3 cards), newsletter signup.

## Rules
- Serif for body, sans for UI, mono for code.
- Generous whitespace between sections.
- `data-df-id` on title, sections, pull quotes, code blocks.
- Responsive: comfortable reading at 375px–1440px.

## Output
Single `index.html`, inline CSS.
