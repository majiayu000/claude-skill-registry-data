---
name: "design-breakdown"
description: "Use when taking a design, slide, landing page, ad or motion piece from a video or capture down to code, timing and workflow, then building an original made the same way."
---

# Design breakdown (the UI Specifics method)

This is the method behind the user's UI Specifics learning stream (a Claude chat artifact). Every design gets taken down to the minimum: where it appears, what is said over it, the HTML and CSS, the motion timing, and the workflow that made it. Then an original version built the same way, and the repos that go further.

## The five steps
1. **Capture.** The user screen-records each design with audio, about ten seconds either side. If only a link exists, run `design-intake` first.
2. **Timestamp.** Transcribe the recording, match it to the full transcript, read any scrubber on screen. State the accuracy (for example plus or minus 10 s inside recordings, plus or minus 30 s when interpolated).
3. **Rebuild the generic.** Templates, landing pages and slides get a faithful HTML/CSS rebuild, one standalone page each, CSS inline, shared helpers in one small file. Count the formula across them in an anatomy table (element by page, present or absent, with a count).
4. **Break down the distinctive.** Artworks, ads and films are NOT cloned. Give a shot list, timings, the tools seen in frame, what makes version 1 worse than the final, then make an original piece with the same method.
5. **Go further.** List repos that push past what was shown, each with stars, licence (or `unchecked`) and which design it maps to.

## Sub-methods
- **De-zombie a landing page.** Count the template formula (tinted two-line hero, muted subhead, pill pair, decorative glow, product mock, serif display, KPI numbers). Then rebuild from a three-line point of view with one fact, unit or image only that business has. Show both pages side by side.
- **Lettered-pin crit sheet.** One OVERALL line, then lettered fixes A, B, C pinned to exact spots on the image; write "same note as A" instead of repeating; go one level deeper than a customer would look.
- **Motion film pipeline (campfire).** Block out in 3D (Blender via Python: `diorama_blockout.py`), render clay and depth frames, explore style per element, animate each shot from a key frame, review every version on one wall (`contact_sheet.py`), cut on hidden wipes, hold the hero shot. Check for: continuous hard motion over about 4 s, camera clipping through geometry, scale jumps, dead static holds.
- **Scroll-scrubbed sequence.** Video to frames, scroll position is the only source of truth for the frame, nearby frames load first, the poster stays until a real frame paints, reduced motion removes pinning, real HTML text over the canvas.

## Rules
- Use `ui-design-guardrails` before writing any original page.
- Labels on everything: verified here, her/his words, our inference, unchecked.
- Never reproduce someone else's artwork, ad, logo or product design; describe it and make an original.
- Fonts are close matches, and say so. Blurry copy is a best reading, and say so.
- End every entry with a "Not checked" list.
- Publish or update the entry in UI Specifics; add a library entry with today's date.