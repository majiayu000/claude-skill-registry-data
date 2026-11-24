---
name: unslop-pages
description: Use when a web page, site template, slide deck or HTML artifact looks AI-generated, or the user asks to unslop, de-slop or clean up a page's layout. Symptoms include a small uppercase label above every heading, a subtitle under every heading, "KEY INSIGHT" style badges, numbered section labels like "01 / THE PROBLEM", stat strips, and status dots. For the wording itself, see unslop.
user-invocable: true
argument-hint: "[files, routes or deck to clean up]"
---

# Unslop pages

AI-generated pages wrap each piece of content in extra layout: a label above
the title, a subtitle below it, and a badge on the box. Remove that layout
and keep every piece of real information.

`unslop` covers the sentences. This skill covers the layout around them. Run
both.

## Recipe

1. **Find every place the layout is defined.** In a template-driven site,
   that usually means one helper (`intro()`, `<PageHeader>`, a slide layout)
   plus the pages that call it. Fix the helper first, then each call.
2. **List every text element that sits next to a heading.** That includes
   the line above it, the line below it, and any badge or tag on its box.
3. **Sort each element into one of three groups:**
   - **Information** (author, speaker, date, page number, source
     reference): keep it. Move it under the heading as one plain line in
     sentence case ("Murray Shanahan · Day 1 · album items 3–17"), or under
     the paragraph it cites ("Handout section: Q*").
   - **Duplicate** (repeats the heading, the nav or the page title): delete
     it.
   - **Decoration** (a mood word, a number, a category name, a "badge"):
     delete it. If the box still needs a name, use a plain heading
     ("Takeaways") or a bold lead-in ("**Example:** …").
4. **Check the list against the catalogue below** for anything step 2
   missed.
5. **Rewrite the remaining titles and leads with `unslop`.** Drop trailing
   full stops on titles. Name sections for their content ("Handouts"), not
   for their role ("The problem", "Why it matters", "Key insight").
6. **Render the pages and look at them.** Check the spacing where you moved
   things, and check that pages with empty leads don't leave a gap.

## Catalogue

| Pattern | Example | Fix |
|---|---|---|
| Kicker above the title | `THE TALKS` over "Talks and slides" | Delete. |
| Metadata kicker above the title | `DAY 1 · SHANAHAN · ALBUM 3–17` | Move under the title as a plain byline. |
| Subtitle under every title | A lead paragraph that restates the h1 | Delete, or keep one only where it adds a fact. |
| Numbered section labels | `01 / THE TALKS` over "Notes and slides" | Delete. Rename the heading to its content. |
| Badge or tag on a box | `KEY INSIGHT`, `IF YOU REMEMBER ONLY THIS`, `LOCAL STUDY MATERIAL` | Delete the badge. Use a plain heading, or no box. |
| Label that repeats its heading | `GENERATION DISCLOSURE` above "Generation disclosure" | Delete the label. |
| Labelled callout boxes | Shaded box headed `EXAMPLE` | `**Example:** …` in the paragraph. |
| Section reference above a heading | `SOURCE Q*` over each h3 | Move under the paragraph as a citation. |
| Role-name headings | "The problem", "The solution", "Why it matters" | Name the content. |
| Stat strip | `09 TALKS · 222 ITEMS · 03 HANDOUTS` | Delete if the nav or text already gives the numbers. |
| Status dot | Green dot next to "Workshop materials" | Delete. Nothing is live. |
| Arrows on internal links | "All talks ↗" | Keep ↗ for external links only. |
| Decorative caption caps | `OPENING PRESENTATION.<br>HKU · 5 NOV` | Sentence case, one line. |
| Mood titles with a full stop | "Minds, meaning & *machines.*" | Plain title, no full stop. |

## Keep

This is a cleanup, not a redesign. Keep these unless the user asks:

- Images and figures that show the subject, such as the hero photo.
- Navigation, counts in the nav, and primary action buttons.
- Function buttons (copy, download, search).
- Source notes, caveats and disclosures. Remove their badges and keep their text.
- Colour, type and spacing tokens.

## Report

List each change grouped by page, with the pattern from the catalogue it
fixes. Say which pages you rendered and looked at.
