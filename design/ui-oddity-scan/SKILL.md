---
name: ui-oddity-scan
description: "Analyze a website page's UI for obvious oddities: the same information repeated multiple times (a phone number shown three times in the header, a '24/7' badge in two places, a bullet list restating the paragraph above it), duplicated or near-duplicate copy and sections, stray/orphaned text near CTAs, copy that doesn't match the business or section subject, placeholder text, overcrowded heroes, misaligned elements, and imagery that doesn't fit the business. Use this whenever the user asks to check, audit, review, sanity-check, QA, or 'look over' a web page, landing page, or UI — whether they give a live URL, a localhost/dev-server URL, a screenshot, or HTML/JSX/template files — even if they only say something casual like 'does this page look right?', 'find anything weird on this page', or 'anything off about my landing page?'."
---

# UI Oddity Scan

Audit a single web page the way a design director does a hero-to-footer critique: is each piece of information said **once, in the right place**? Does the structure make sense? Do things line up? Does the imagery match the business? The output is a section-by-section HTML review with numbered pins on screenshot crops.

## Scope — what this is and is not

This is a **UI, visual design, and copy-structure** scan. The question is always "does this look and read correct?", never "could this be optimized?".

Explicitly OUT of scope — do not report these even if you notice them:

- **Link/href auditing** (dead links, `#` targets, where buttons navigate). That's QA/SEO work, not visual design. A CTA is only a finding here for what it *looks and reads* like: duplicated, vague, conflicting with nearby copy, oddly placed.
- **SEO** (meta descriptions, title tags, heading hierarchy for crawlers).
- **Accessibility audits** (WCAG ratios, aria labels) — except contrast so low a sighted visitor visibly struggles.
- **UX flow / conversion strategy** advice, and **mobile responsiveness** speculation from desktop captures.
- **Copywriting rewrites.** "This sentence could be punchier" is not a finding. "This bullet list says the same thing as the paragraph directly above it, just worded differently" IS a finding — the oddity is the *duplication of information*, not the word choice.

Why so strict: mixing in link QA and SEO advice buries the findings the user actually wants, and makes the report read like a generic site audit instead of a designer's eye.

The core insight of this skill: these oddities survive because everyone *skims* the page. To catch them you must *inventory* the page first, then judge it. Do not skip the inventory step.

## Step 1 — Understand the business first

You cannot judge "does this copy match the subject?", "is this element odd here?", or "does this image fit?" without knowing what the page is *for*. So before scanning:

- If the user hasn't said what the business/product is and it's not instantly obvious from the page, **ask them one short question** before finalizing judgments — e.g. "Quick check so I judge this right: what's the business, and what's the #1 thing you want a visitor to do on this page?" (Use the structured question tool if available.)
- If the user isn't around to answer (or already told you), infer it from the page and **state the inferred subject at the top of the report** — e.g. "Read as: a local garage-door repair company; primary action: call now." That line lets the user instantly correct you if the whole scan was judged against the wrong premise.

Every subject-mismatch and imagery finding must trace back to this stated subject.

## Step 2 — Get the page in front of you

You want two artifacts wherever possible: a **full-page screenshot** (for visual checks) and the **extracted text/DOM data** (for copy and repetition checks).

**A. Public URL** — run the bundled capture script. It needs Python + Playwright; if Playwright is missing, install it first (`pip install playwright && playwright install chromium`):

```bash
python3 scripts/capture_page.py "https://example.com/pricing" --outdir capture/
```

This produces `page.png` (full-page screenshot) and `page.json` (text blocks with bounding boxes, CTA inventory, precomputed exact-duplicate pairs, repeated phone numbers, broken images, overflow elements). Read `page.json` and *look at* `page.png` with the Read tool — you need both.

**B. Localhost / dev server / behind a login** — first ask: does your shell run on the same machine as the dev server? If yes (e.g. Claude Code running locally), just point `capture_page.py` at the localhost URL like any other URL. If your shell is in a cloud sandbox, it cannot reach the user's `localhost:3000` — instead drive a browser that runs *on the user's machine*: the Claude-in-Chrome tools (`mcp__claude-in-chrome__*`), or a locally installed browser MCP (e.g. `chrome-devtools`, `playwright-mcp`, `puppeteer`, `desktop-commander` running the capture script locally). Take a full-page screenshot and pull the page text. If no browser bridge is connected, ask the user to paste a screenshot + the page HTML. If the user can share the page's HTML file directly, that also works via input type D.

**C. Screenshot only** — analyze the image visually. You can catch nearly everything in scope this way: repetition, restatement, placement, alignment, imagery, density, tone.

**D. HTML / JSX / template files** — read the source for copy and repetition checks. If it's renderable HTML, *also* render it so you can see the layout:

```bash
python3 scripts/capture_page.py "file:///path/to/page.html" --outdir capture/
```

For JSX/templates that can't be rendered easily, do the copy/consistency checks from source and say clearly that layout checks were skipped.

## Step 3 — Inventory the page (before judging anything)

Build four small inventories. This is fast and it's where most catches actually happen:

1. **Heading outline** — every h1–h6 (or visually-heading text) in order: the page's claimed subject and each section's claimed topic.
2. **Fact map** — the key facts a page like this carries: phone number, hours/availability ("24/7"), rating/review count, service area, tagline, promo offer. For each fact, list **every place it appears**. The rule of thumb is *one fact, one home per screenful* — a phone number in the top bar AND directly below it AND again in the hero button is three homes for one fact. `page.json → repeated_facts` precomputes phone-number repeats; badges, taglines, and availability claims you map yourself, and repeats count **even when the wording differs** ("24/7 Emergency Repairs" vs "emergency service around the clock" is the same fact twice).
3. **CTA inventory** — every button and prominent link: exact text and where it sits (not where it navigates).
4. **Repeat/restate map** — verbatim duplicates (`page.json → duplicates` precomputes these with pixel distances) plus *restatements*: a list, card row, or section that re-says what nearby copy already said in different words, and sections that are near-clones of each other.

## Step 4 — Run the checks

Read `references/checks.md` for the full checklist with examples. The six categories:

1. **Repetition & redundancy** — the headline category: repeated facts, verbatim duplicates too close together, restated content (paragraph + list saying the same thing), near-duplicate sections.
2. **Copy oddities** — orphaned/stray fragments, placeholder/debug text, copy not matching the stated subject, typos.
3. **CTA oddities (visual/copy only)** — identical CTAs stacked too close, vague labels, CTA text conflicting with surrounding copy.
4. **Layout & alignment** — overlaps, truncation, misaligned elements that should line up (stars vs. their text, icon rows), broken images, overflow, spacing incoherence, unreadably low contrast, **overcrowding** (a hero carrying too many competing messages).
5. **Imagery fit** — does each prominent image match the business and the section it sits in? A generic house photo behind a garage-door-repair hero, stock photos with visible watermarks, an image showing a different product.
6. **Consistency** — naming drift, tone whiplash, heading-case drift, person/voice drift, format drift.

## Step 5 — Rate and prune findings

For each finding assign **severity** (high = visitors will notice and it damages trust or blocks conversion; medium = noticeable on a careful read; low = polish) and, when you couldn't verify directly, a confidence note. Phrase every finding as *what is odd and why*, and every fix structurally ("keep the phone number in the top bar; remove the other two") — never as a rewording exercise.

Prune hard, but prune the right things. The same primary CTA repeating once per major scroll section is convention — don't flag it. A phone number or availability badge appearing two or three times **within the same screenful** is a real finding — do flag it, even though each instance is "normal" on its own. Two sections both *mentioning* fast service is marketing; a list that adds no information beyond the sentence above it is redundancy. If the page is clean, say so plainly — a short "no significant oddities" report with a note on what was checked is a good outcome. Never pad with invented nitpicks or out-of-scope advice to look thorough.

## Step 6 — Build the report (section-by-section HTML)

The deliverable is a single self-contained HTML review organized **section by section down the page** — each section card shows a screenshot crop of just that region with numbered severity pins overlaid, and the numbered notes (with a one-line structural Fix each) directly beneath. Never ship one enormous full-page screenshot, and never ship a wall of text without pictures. Write a `findings.json` and run the bundled builder:

```bash
python3 scripts/build_report.py capture/page.png findings.json
```

The full schema is in the script's docstring. The shape:

```json
{
  "meta": {
    "business": "OnSite Garage Doors", "source": "URL or file", "date": "YYYY-MM-DD",
    "subject": "inferred business + primary visitor action from Step 1",
    "pattern_intro": "1-2 sentences naming the pattern behind most findings",
    "repeats": [{"count": "7x", "message": "Phone number", "where": "top bar, header, hero button, footer"}],
    "recommendation": "the one structural change that fixes most of it"
  },
  "sections": [{
    "title": "Header + Hero",
    "region": [y0, y1],
    "working_well": false,
    "findings": [
      {"severity": "high|medium|low", "text": "the oddity, quoting exact copy", "fix": "structural fix", "pin": [x, y]},
      {"severity": "good", "text": "something in this section that genuinely works — keep it"}
    ]
  }]
}
```

What makes this report format work — preserve these properties:

- **The summary table is the headline.** `meta.repeats` counts every repeated message across the whole page ("7× phone number", "~8× the service list") with where each lives — that table is what makes the clutter undeniable — and `meta.recommendation` names the single structural change that fixes most of it.
- **Sections run in page order, top to bottom**, sliced at natural boundaries (hero, each grid, each band, footer). Get `region` y-ranges and `pin` coordinates from `page.json` bboxes (or estimate from the image for screenshot input). Pin numbering restarts at 1 in each section and matches the notes.
- **Say what works, not just what's wrong.** Use `"severity": "good"` notes (green check) for elements worth keeping, and `"working_well": true` on genuinely clean sections — that's what makes the criticism credible. A clean page produces a short report of mostly-green sections, not invented findings.

The builder writes `crops/<section>.png` — view at least one with the Read tool, and check that pins land where you meant (adjust `pin` coords and rerun if not).

`scripts/annotate.py` still exists for a quick full-page annotated overview, but only produce that if the user asks for it.

## Step 7 — Name it properly and deliver

The builder names the file `ui-review-<business>-<date>.html` automatically — keep that convention. Never deliver a file called `report.html`, `review.html`, or `output.html`: the name should tell the user what it is when they find it in a folder next week.

Send the file to the user explicitly — use the file-delivery tool if this environment has one (e.g. SendUserFile / present_files); in a local CLI, give the absolute path and offer to open it. Never leave the report sitting in a working directory unmentioned: producing it is not delivering it. Keep the accompanying chat message to a one-line summary — the report speaks for itself. If the user asks for markdown instead, mirror the same structure in a .md file.
