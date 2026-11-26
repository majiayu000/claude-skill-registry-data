---
vendored_from: https://github.com/jessl2juice/kindlepub
name: kindlepub
description: >-
  End-to-end Amazon KDP self-publishing pipeline for a finished book manuscript.
  Builds the reflowable Kindle EPUB (epubcheck-clean), generates cover art with Gemini
  Nano Banana and assembles the cover in KDP Cover Creator (which auto-sizes the spine —
  no custom print PDF), drafts all KDP metadata, and walks the user through the KDP
  Details/Content/Pricing/Publish flow for Kindle ebook, paperback, and hardcover. Use this
  whenever the user wants to publish, self-publish, or upload a book to Amazon, KDP, or
  Kindle Direct Publishing; make a Kindle ebook; set up a paperback or hardcover; build a
  book cover or EPUB; or asks about KDP pricing, royalties, DRM, KDP Select, AI-content
  disclosure, or pre-orders. Trigger even if the user only says "put my book on Amazon,"
  "make this a Kindle book," or "I finished my manuscript, now what."
license: MIT
metadata:
  owner: BetterMind / Clinician Assist
  visibility: public
  portability: portable
  requires_config: []
  provenance: "First built 2026-06-24, battle-tested on a real book launch"
triggers:
  - kindlepub
  - kindlepub

---

# KindlePub — Amazon KDP publishing pipeline

Take a finished manuscript all the way onto Amazon. Each format (Kindle ebook, paperback,
hardcover) is a SEPARATE KDP title that KDP links on one product page. The Kindle ebook is
the fast win; the paperback is the value-priced print edition; the hardcover is the premium
edition. You can do one, two, or all three.

Build everything to the edge, then hand the user the irreversible clicks. The user enters
credentials, operates native file pickers, sets anything permanent, and presses Publish.
You never type passwords or drive an OS file-open dialog.

**Cover approach (important):** generate the cover ART with Gemini Nano Banana, then assemble
the actual cover in **KDP Cover Creator** — it lays in the title/author typography and
auto-sizes the spine to the page count. Do **not** build a custom print-cover PDF or a custom
6×9 interior PDF; let KDP's tools size and paginate. (This is the path that shipped.)

## What you need from the user (gather first)

- The FINAL manuscript source. A Google Doc is ideal; a .docx also works. Confirm it is truly
  final — filenames lag content, so open it and read the version stamp (a "v15.7 FINAL" doc
  beats a "v16 draft" with a higher number).
- Title, subtitle, author name, and the imprint/publisher line.
- Cover art or a cover concept. If they have brand art, great; if not, you will generate it
  with Nano Banana (see Phase 3).
- Which formats they want, and their KDP account email.

Flag early: the KDP account needs **Two-Step Verification + tax/banking** complete before the
final Publish and before any royalty payment. That is the user's to finish.

## Phase 1 — Lock the source, export a clean DOCX

If the source is a Google Doc, export a clean DOCX through the logged-in browser by navigating
to: `https://docs.google.com/document/d/<DOC_ID>/export?format=docx`. This downloads the .docx
with no copy/paste loss. Stage it for the EPUB build and (for print) for upload to KDP.

## Phase 2 — Build the Kindle EPUB

Use `scripts/build_epub.py`. Edit the CONFIG block at the top (input DOCX, title, subtitle,
author, contributors, cover JPG path, publisher) and run it. It uses `mammoth` (DOCX->HTML) +
`ebooklib`, segments chapters, and adds the front matter most manuscripts lack: a copyright
page, a medical/crisis disclaimer (the 988 block — keep it for anything touching health or
safety), and a navigable table of contents. It preserves in-text diagrams.

Then validate with `scripts/validate_epub.py` (wraps `epubcheck`, which needs Java). Ship only
on a clean pass. The script already encodes the three ebooklib traps that cost real time the
first time:

- Set `EpubHtml.content` to HTML with NO `<?xml ... encoding?>` declaration. ebooklib's lxml
  path silently returns an EMPTY body on an encoding-declared Unicode string, so your pages
  come out 0 bytes and "valid."
- Attach CSS with `add_link(...)`, not a `<link>` in your own head — ebooklib rebuilds the
  head from the title + links you register.
- After `set_cover(create_page=True)`, set the cover page `is_linear=True` and pass
  `write_epub(..., {'epub3_pages': False})`, or epubcheck throws OPF-096 / the page-list
  generator crashes on the empty cover body.

## Phase 3 — The cover: Nano Banana art → KDP Cover Creator

Generate the cover **art** with Nano Banana (Gemini's image model), then assemble the cover in
**KDP Cover Creator**. Cover Creator adds the title/author typography and auto-sizes the spine
to the page count, so there is no custom PDF and no manual spine math.

Read `references/nanobanana-cover-prompts.md` for the prompt recipes and the one rule that
matters: AI models always sneak garbled text onto pennants, clothing, book spines, and screens,
so the prompt must forbid text on those surfaces — Cover Creator adds the real title later. The
flow:

1. Give the user the prompt (and tell them which reference image to attach). They generate the
   art in Nano Banana / Gemini and send back the file (no text in the art).
2. In KDP, open **Cover Creator**, upload that art, and let it lay in the title, subtitle, and
   author and size the spine + back automatically. Uncheck "my cover has a barcode" so KDP
   leaves room for its own. Iterate on the layout with the user.
3. For the **Kindle ebook** front cover, use Cover Creator's front-cover image (download it) as
   the ~1600x2560 JPG you upload in the ebook Content step — same art, one cover everywhere.

(Do NOT build a custom wraparound print-cover PDF — Cover Creator is the path.)

## Phase 4 — Print interior (paperback / hardcover) — no custom PDF

Do **not** build a 6×9 interior PDF. Upload the **manuscript DOCX** to KDP for the print title;
KDP paginates it, and Cover Creator sizes the spine to the resulting page count. Pick **Black &
white** interior for a text book (see the print-cost trap in the walkthrough) and the common
**6×9** trim. Let KDP's tools handle pagination and the spine.

## Phase 5 — Draft the KDP metadata

Fill in `references/metadata-template.md`: title, subtitle, author, the back-cover-style
description (KDP allows light HTML — paste clean <p> paragraphs via the Description box's
"Source" mode), 3 BISAC categories, 7 keywords, the AI-content answers, price, and the release
plan. Reuse the description as the online blurb and a trimmed version on the back cover.

## Phase 6 — Walk the user through KDP

Drive the browser through Details -> Content -> Pricing -> Publish. Read
`references/kdp-walkthrough.md` for the field-by-field script and every decision (AI-content
disclosure, DRM, KDP Select, pre-order dates, the Cover Creator steps, and the print-cost trap
that quietly forces a ~$49.99 hardcover). Hand the user every native file picker and the final
Publish click.

## Phase 7 — Document it

When the book is set up, save a publication record to the user's knowledge base (every KDP book
id, the locked blurb + back-cover copy, asset locations, pricing, the AI disclosures, release
dates) so the next format and the next book go faster. If the user keeps a notes repo, write it
there and commit.

## The scripts are templates, not black boxes

The two EPUB scripts each have a CONFIG block at the top — edit it for the book at hand. They are
the exact tools that shipped a real title; read them before running so you can adapt rather than
fight them. The cover and print spine are done in KDP's own tools (Cover Creator), not in code.

## Tools & adapters

| Capability | Claude Code / Cowork | Codex / Cursor / other |
|------------|----------------------|------------------------|
| Build EPUB | bash + `python3 scripts/build_epub.py` (pip deps) | same |
| Validate EPUB | `python3 scripts/validate_epub.py` (epubcheck + Java) | same |
| Generate cover art | hand user the Nano Banana / Gemini prompt | same |
| Assemble cover + spine | KDP **Cover Creator** in the browser | same |
| Drive KDP / native pickers | hand the user the irreversible clicks | same |

Deps: `mammoth ebooklib beautifulsoup4 lxml epubcheck` (+ Java on PATH for epubcheck).

## Portability

Class: **portable**. A self-contained pipeline with no external coupling and no secrets — the
only dependencies are pip packages plus Java for epubcheck, and there is no env config
(`requires_config: []`). The cover and spine are assembled in KDP Cover Creator (no custom PDF),
and the worked example in `references/nanobanana-cover-prompts.md` is fully generic (no real book
or author names). The installed original remains the untouched fallback until this copy is
validated at parity.

## Acceptance check
- Trigger: "put my book on Amazon" / "make this a Kindle book" / "I finished my manuscript, now what".
- Expect: builds an epubcheck-clean EPUB; generates cover art with Nano Banana (no garbled
  text); assembles the cover in KDP Cover Creator (auto-spine) and reuses its front for the
  ebook; uploads the manuscript DOCX for print; drafts KDP metadata; walks
  Details→Content→Pricing→Publish, handing the user every irreversible click.
- Must NOT: type the user's passwords or drive native OS file pickers; ship an EPUB that fails
  epubcheck; build a custom print-cover or 6×9 interior PDF (use Cover Creator 