---
name: review-doc
description: Render any document the user needs to review (design docs, plans, story bibles, proposals, reports) as a self-contained HTML page with Google-Docs-style commenting — highlight text, attach notes, export feedback. Use whenever producing or updating a document whose primary purpose is for the user to READ AND REACT TO, whenever the user asks for "a review doc", or when they hand back a *.feedback.md file. The user has standing instructions that all review documents get this treatment.
---

# review-doc — reviewable HTML documents with margin comments

## What this produces

A single self-contained `.review.html` file (no network, no deps) that
renders a markdown document with:

- Google-Docs-style commenting: select text → 💬 → type a note; comments
  live as cards in a right margin rail, anchored to highlights.
- Persistence in `localStorage` (survives reload, keyed per document).
- **Export feedback** button → downloads `<doc>.feedback.md` (quoted
  passages + the user's notes) and a copy-to-clipboard alternative.
- General (unanchored) comments, dark/light theme support.

## Workflow

1. **The markdown source stays canonical.** Never hand-edit the
   generated HTML; regenerate it.
2. Generate:
   `node <dir-containing-this-SKILL.md>/build-review.mjs <source.md> [out.html]`
   (the script sits next to this SKILL.md — use the path you read it from)
   (default output: `<source>.review.html` next to the source).
3. Deliver: `open <out.html>` on macOS so it lands in the user's real
   browser (commenting + export need a full browser, not a preview
   pane), and/or send the file. Tell the user the loop in one line:
   *highlight → comment → Export feedback → give me the file.*
4. When the user returns a `*.feedback.md` (or pastes its contents):
   read every quoted passage + note, respond to or apply each one,
   then regenerate the review HTML from the updated markdown. Existing
   comments re-anchor by quote; notes on text that changed appear in
   the rail as "unanchored" rather than being lost.

## Notes

- Works for any markdown: headings, tables, lists, code fences,
  blockquotes, links, images.
- The document id (localStorage key + feedback filename) is derived
  from the output filename — keep it stable across regenerations so
  the user's in-progress comments survive.
- If the user asks for review docs in some other format, that wins.
