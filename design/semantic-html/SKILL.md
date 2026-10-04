---
name: semantic-html
description: Use when writing or reviewing HTML/JSX - catches divs-for-everything, skipped heading levels, onClick on non-interactive elements, cursor-pointer on divs, missing or incorrect alt text, a11y audit failures
---

# Semantic HTML

## Overview

Semantic HTML uses elements that convey meaning, not just appearance. Proper semantics improve accessibility (a11y), SEO, and maintainability. Screen readers, search engines, and future developers all benefit.

## When to Use

- Writing or reviewing any JSX/HTML
- Creating new UI components
- Responding to accessibility audit findings (WCAG, Lighthouse)
- Fixing "div soup" / "divitis" in existing code

## Review Checklist

### 1. Heading Hierarchy

- [ ] Single `<h1>` per page
- [ ] No skipped levels (h1 → h2 → h3, never h1 → h3)
- [ ] Headings reflect document outline, not visual styling

```tsx
// ❌ Using h3 for visual style
<h3 className="text-sm">Subtitle</h3>
// ✅ Correct level, styled smaller
<h2 className="text-sm">Subtitle</h2>

2. Landmark Elements

- Page has <main> (exactly one)
- Navigation uses <nav>
- Sections have headings or aria-labelledby

| Element   | Use For                             |
|-----------|-------------------------------------|
| <header>  | Page/section header                 |
| <nav>     | Navigation links                    |
| <main>    | Primary content (one per page)      |
| <section> | Thematic grouping with heading      |
| <article> | Self-contained content (post, card) |
| <aside>   | Supplementary (sidebars, CTAs)      |
| <footer>  | Page/section footer                 |

When multiple sections exist:
<section aria-labelledby="team-heading">
  <h2 id="team-heading">Our Team</h2>
</section>

3. Lists

- Collections use <ul> or <ol>, not div soup
- Navigation links wrapped in <ul> inside <nav>

// ❌ Divs for collection
<div className="cards"><div>Card 1</div></div>
// ✅ Semantic list
<ul className="cards"><li>Card 1</li></ul>

4. Links vs Buttons

- Navigation uses <Link> or <a href>
- Actions use <button>
- No onClick on divs or spans
- No <a href="#"> for actions

| Use                                 | Element               |
|-------------------------------------|-----------------------|
| Navigate to page                    | <Link to> or <a href> |
| Action (submit, toggle, open modal) | <button>              |

// ❌ Div with onClick for navigation
<div onClick={() => navigate('/about')}>About</div>
// ✅ Proper link
<Link to="/about">About</Link>

// ❌ Anchor for action
<a href="#" onClick={handleSubmit}>Submit</a>
// ✅ Button
<button onClick={handleSubmit}>Submit</button>

Clickable cards: wrap entire content in <Link>, not onClick on div.

5. Images

- Informative images have descriptive alt
- Decorative images have alt=""
- Images inside links with visible text have alt=""

// Informative - describe what's shown
<img src="/team.jpg" alt="Team working in the lab" />

// Decorative - empty alt
<img src="/pattern.svg" alt="" />

// Inside link with text - empty alt (link text provides context)
<Link to="/ssd">
  <img src="/ssd.jpg" alt="" />
  <h3>SSD Recovery</h3>
</Link>

6. Text Elements

- Paragraphs use <p>, not <div>
- Important text uses <strong>, not styled <span>
- Emphasized text uses <em>, not styled <span>
- Dates/times use <time datetime="...">
- Contact info uses <address>

| Element   | Use For                           |
|-----------|-----------------------------------|
| <p>       | Paragraphs of text                |
| <strong>  | Important text (not just bold)    |
| <em>      | Emphasized text (not just italic) |
| <time>    | Dates and times                   |
| <address> | Contact information               |

Common Mistakes

| Mistake                   | Fix                                |
|---------------------------|------------------------------------|
| <div> with heading styles | Use <h1>-<h6>                      |
| Skipped heading levels    | Correct hierarchy, style with CSS  |
| <a href="#"> for actions  | Use <button>                       |
| Missing alt attribute     | Add descriptive text or alt=""     |
| onClick on divs/spans     | Use <Link> or <button>             |
| cursor-pointer on div     | Make it a real interactive element |
| <div> for paragraphs      | Use <p>                            |
| <b> / <i> for semantics   | Use <strong> / <em>                |
| ```                       |                                    |
