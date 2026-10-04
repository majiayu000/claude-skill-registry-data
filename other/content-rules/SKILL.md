---
name: content-rules
description: Use when writing, editing, or reviewing any user-facing copy on this site - page text, headings, captions, button labels, error and empty states, or metadata. Also use before telling someone the site is ready to share, since it covers what must not be published on an internal demo.
---

# Content rules

## What must never appear on a demo site

These are in `docs/content-rules.md` and take precedence over anything else
here. Read that file. If a request would put restricted content on a page, say
so plainly rather than writing it.

## Voice

- Sentence case for headings and buttons. Not Title Case, not ALL CAPS.
- Active voice. Plain verbs.
- Say what something does, do not sell it.
- Name things the way the reader would, not the way the system is built.

## Buttons and links

A label says exactly what happens: "Read the design doc", not "Learn more".
The same action keeps the same name everywhere it appears.

## Headings

One `h1` per page, in the `Hero`. Headings descend in order with no gaps —
never skip from `h2` to `h4` for visual reasons.

## Every page needs

- A `title` that reads well in a browser tab and a shared link
- A `description` of one or two sentences, written for someone who has not
  seen the page
- An owner, so a reader knows who to ask (set in `src/site.config.ts`)

## Demo framing

These sites get shared and forwarded. A reader who lands cold must be able to
tell that it is an internal demo and not a shipped product. The footer says so
on every page; do not remove it.

## Before calling a site finished

- Every `DELETE-ME` block removed
- `src/pages/example.astro` deleted
- `site.config.ts` filled in with a real owner
- No placeholder text, no lorem ipsum, no "Your Name"
- `npm run build` passes
