---
name: create-post-carousel
description: >
  Create a multi-slide carousel post — Instagram carousel, LinkedIn document
  post, or TikTok photo-mode — through the Marky API: pick a narrative
  framework, write the slide-by-slide copy, render every slide from one shared
  branded HTML template, and attach the slides in order. Use when the user says
  "make a carousel", "slide post", "LinkedIn document post", "turn this list
  into slides", or "swipeable post". For a single designed image, see
  create-post-graphic (this skill uses its render mechanics); for the caption
  and scheduling, see schedule-posts.
---

# Carousel Posts

A carousel is not a blog post chopped into squares — it's a swipe-through where
every slide has two jobs: deliver one idea, and earn the next swipe. This skill
owns the narrative structure and slide copy; the rendering mechanics (brand
pull, HTML authoring, headless render, upload) come from the
**create-post-graphic** skill — read it first.

## Stage 1 — Pick the framework

Read [references/carousel-frameworks.md](references/carousel-frameworks.md) and
pick by what the content IS, using its table:

| Content | Framework |
|---|---|
| List of resources/tools/tips | A: Value-Stack |
| A personal result with a system behind it | B: Problem-Proof |
| Several named techniques on one theme | C: Hack List |
| A strong opinion about a common practice | D: Rant Callout |
| A product or workflow you can show | E: Demo Walkthrough |

Don't force it: list content in a rant structure (or vice versa) is the #1
reason carousels flop. If nothing fits, it probably wants to be a single
graphic — hand off to create-post-graphic.

## Stage 2 — Write the slide copy

Write ALL slides as text before touching HTML, following the framework's
slide-by-slide table. Rules from the reference that are non-negotiable:

- Slide 1 must work as a standalone feed post (it competes alone as the
  thumbnail).
- One idea per slide; if a slide needs two sentences of setup, split it.
- Any count promised on the cover is exactly delivered — no filler slides.
- Claims and numbers must be real and this business's own.
- Final slide: ONE call to action, not three.

Run the slide copy and the caption through the **humanize** skill's pattern
check before rendering — fixing text is free, re-rendering isn't.

## Stage 3 — Render the slides

Use create-post-graphic's Stage 1 (brand pull), Stage 3 (HTML authoring), and
Stage 4 (headless render + LOOK at it) with one carousel-specific rule: **one
HTML template, N content swaps.** Author a single `slide.html` with the brand
tokens and layout, then render each slide by swapping the copy (a small
build loop or one file per slide from the same skeleton). Same type scale, same
palette, same layout on every interior slide — variety between slides reads as
clutter.

Dimensions: 1080x1350 (4:5) for Instagram and LinkedIn; check the marky-api
platform rules for the max slide count per platform before authoring.

## Stage 4 — Assemble and attach

- Upload the slide PNGs in order (slide 1 first — it's the cover) and create
  the post with all of them in `media_urls`. Marky publishes them as a
  carousel on platforms that support it.
- LinkedIn document posts: LinkedIn expects a PDF; Marky handles carousel
  delivery per platform — do NOT pre-convert unless the platform rules say so.
- The caption is a second hook, not a repeat of slide 1 — write it as its own
  post text.
- Tag `metadata`: `format: carousel`, `hook: <framework letter>`, plus `topic`
  — review-performance groups engagement by these tags, so framework
  performance becomes measurable per audience.

## Stage 5 — Approve, then schedule

Same hard gate as every creation skill: show the rendered slides (review board
in pick mode for multiple candidates), get explicit approval, then schedule via
the schedule-posts skill. Judge results later on **saves and completion**, not
likes (see "Measuring what worked" in the reference).

## Feedback

Friction or ideas? Send via the `submit_feedback` MCP tool (see marky-api
"Marky wants your feedback").
