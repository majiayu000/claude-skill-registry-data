---
name: pptpro
description: Create visually polished, editable PPT/PPTX presentations in a clean PPTPRO style. Use when the user asks for a beautiful, designed, non-generic PowerPoint deck, especially course presentations, reading applications, source-backed slides, scripts matched to slide pages, or requests to avoid AI-looking beige/card templates and repeatedly check visual quality.
---

# PPTPRO

## Purpose

Use PPTPRO to make PPTs that look intentionally designed, not like text dropped into a template. The default output is an editable `.pptx`, with optional speaker script matched to slide numbers.

Default deck shell: include a simple designed cover slide at the beginning and a simple closing slide at the end. The cover should only contain basic metadata: title, presentation date, and presenter. The date is the actual talk/report date, not the presentation duration. The closing slide should contain `Thank You` and either `Questions` or `Questions & Discussion`; default to `Questions & Discussion` for class/academic presentations. Do not add abstracts, argument previews, slogans, agendas, decorative summaries, contact lines, or extra content unless the user or an official template explicitly requires them.

Simple cover means metadata-only, not visually empty. A cover must still feel designed and balanced: use strong title placement, module/date/presenter grouping, restrained accent structure, a logo/brand mark, or one relevant high-quality traceable image/source object when allowed. Do not fill cover emptiness with agenda, thesis preview, abstract text, slogans, decorative summaries, or content cards.

Template-bound exception: when the user provides an existing deck/template and asks to modify it, follow the supplied deck structure over the default shell. Preserve required cover, conclusion, footer, section, and teammate pages unless the user explicitly asks to replace them. If the user says to edit only a section, keep the final deliverable as the full deck with the unedited sections intact by default.

## Core Style

Read these before building or redesigning a deck:

- `references/design-system.md`
- `references/slide-recipes.md`

Default to this style unless the user gives another brand/template:

- Sans-serif only. Avoid Georgia, Times New Roman, Cambria, Garamond, and other serif display fonts.
- Use white or light gray backgrounds by default. Avoid beige/cream/sand/tan backgrounds unless the user explicitly asks.
- Use one restrained accent palette: charcoal + white/light gray + teal/blue/coral.
- Prefer concept maps, process flows, case cards, and comparison structures over generic bullet lists.
- Avoid repeated same-structure content slides. Do not let 2-3 consecutive slides share the same visible layout such as title + three text cards + bottom takeaway. Each source-backed deck should vary the middle slides with a source/object page, mechanism/process diagram, case comparison, media/case analysis, timeline, matrix, or figure-led evidence slide.
- Do not use decorative short dashes, random connector marks, or unexplained design elements.
- Do not put text in a box unless the box has a clear role: step card, case card, callout, or discussion prompt.
- Keep card text short enough that it visibly breathes inside the card, but do not leave giant unused card space.
- Match container size to content size: a short one-sentence card should be shallow, or it must include a real visual sub-structure such as evidence chips, a mini table, a scale, or a comparison row.
- Keep every text box inside its card's safe area. Text must not cross, touch, or visually collide with the card border.
- When text is near a card boundary, fix the layout first: shorten the copy, enlarge the card, increase padding, split content, or lower the font size within the allowed range.
- Keep slide weight balanced across the useful canvas. Do not put all meaningful content in the upper third while the lower half is empty.
- Balance vertical rhythm: title, subtitle, main content, synthesis, and footer must feel evenly distributed rather than stacked at the top with a large blank middle.
- Check cover density separately: reject covers where a small title block is stranded in the upper-left or upper-middle with most of the canvas inert blank space. Fill the cover through layout, scale, logo/brand mark, traceable image, or purposeful accent while keeping cover text metadata-only.
- Multi-line titles must have readable line spacing, and subtitles must not sit too close to the title.
- Every pill/tag/legend label must fit on one line. If a short label wraps, widen it, shorten it, or switch to a different layout.
- For book, article, report, or source-led presentations, create a sense of the source as an object before abstracting the argument. Use available real source visuals such as a book cover, article page, official report cover, table of contents, chapter/case structure, method/site map, real data visual, or media screenshot when it is relevant and legally/provenance-safe.
- For book-based decks, at least one content slide should usually show the book cover or official book metadata, plus the book's actual content structure: field sites, chapters, cases, methods, key actors, or evidence types. Do not reduce the book to generic concept cards only.
- Turn abstract reading points into visual logic where possible, such as `old model -> access problem -> activist/public-care move`, two-site comparisons, chapter/case maps, or media-event-to-theory analysis. Use real content from the source, not decorative icons.
- When making a PPT from a report, essay, final paper, thesis, or manuscript, preserve real data visuals from the source document. If the paper uses original data figures, charts, model outputs, survey plots, screenshots of results, or other evidence images, reuse the original data figure assets in the PPT when that evidence is part of the presentation argument.
- Do not replace a real data figure with a generic icon, AI-generated visual, redesigned approximation, or text-only summary unless the user explicitly asks or the figure is irrelevant to the deck scope.
- After source-native visuals are accounted for, make visual enrichment a normal part of PPT design rather than an afterthought. For text-heavy decks, plan regular visual anchors such as supporting photos, contextual images, generated illustrations, diagrams, maps, object shots, process scenes, evidence chips, or compact visual systems. A polished deck should usually have at least one meaningful visual anchor every 2-3 content slides, and each major section should have at least one image-, illustration-, diagram-, or source-object-led slide unless the template or assignment forbids it.
- Good supporting images include official photos, maps, policy/document screenshots, event/news images, organization or place photos, product/lab/context photos, author/book-related visuals, generated conceptual illustrations, or other concrete visuals that make the argument easier to see.
- Supporting images must be source-attributable and context-relevant. Prefer official, publisher, government, university, museum/archive, reputable news, or clearly traceable image sources. Avoid vague stock photos, watermarked/low-resolution images, AI-looking filler, decorative illustrations, and images chosen only to fill space.
- External supporting images are secondary to source evidence. They may enrich a slide, but they must not replace required original data figures, book/source structure, or textual evidence from the assignment source. Record full image provenance in the source log or working audit when used; visible slide footers should contain only concise human-facing credits when needed.
- When no real source visual or traceable supporting image fits the slide, and a custom conceptual, scene, process, object, or atmosphere image would make the argument more concrete, use Codex/ChatGPT's built-in image generation capability. Default to the current latest built-in image model/tool exposed by the environment; do not hardcode a specific image model name in reusable instructions.
- AI-generated images are content-supporting visuals only. They must not stand in for real data figures, source screenshots, official documents, logos, portraits of real people, event evidence, or cited factual proof. Record generated-image provenance in the working audit, notes, or source log: tool/model, prompt summary, date, and intended slide role.
- Visible cards, callouts, panels, and synthesis bars should use softer rounded-rectangle corners by default. Avoid sharp square boxes unless the supplied template clearly uses square geometry. For default PPTPRO decks, use PowerPoint rounded rectangles or equivalent shapes with a medium-soft radius, roughly 0.12-0.18 in or 14-20% of the shorter side for normal cards.
- Visible slide copy must read like a human-made presentation, not a project work log. Do not put internal workflow, audit, source-log, provenance-record, or file-tracking sentences on slides, in speaker script, or in visible footers. Phrases like `Full source provenance and image credits are recorded in the project source log` are forbidden in the deck. Keep full provenance in working files; visible credits should be concise human-facing labels such as `Image: NASA` or a normal `Sources used` slide when needed.

When a real template is provided, do not default to the white/light-gray PPTPRO house style just because it is the default. First extract the template's visual language:

- background color and accent palette
- title capitalization, size, and placement
- footer/source/page-number treatment
- image crop style and border/radius style
- typical content density and spacing rhythm
- existing section ownership or teammate boundaries

Then improve within that direction. A template-bound deck should look like a polished version of the supplied file, not a different deck rebuilt from scratch.

## Scientific / Paper Deck Logic

When the deck is built from a scientific paper, preprint, thesis chapter, lab report, benchmark paper, methods paper, review, or other figure-led academic source, treat the scientific argument rather than the source section order as the presentation spine.

Before locking the slide recipe map:

- classify the source type: discovery/mechanism, methods/AI/tool, resource/dataset/atlas, clinical/population, materials/engineering, or review/perspective
- choose the matching presentation arc: question-to-evidence, problem-to-solution, workflow-to-validation, design-to-inference, property-to-mechanism, or evidence-map
- identify the central claim, the evidence that carries it, and the boundary where the claim stops
- select only the figures, tables, and workflow visuals that are needed for the story; do not force every paper figure into the deck

Scientific deck rules:

- do not mirror IMRaD mechanically if it weakens the talk; preserve the science, not the paper's exact table of contents
- use conclusion-style titles on most content slides; prefer `X improves Y under Z condition` over labels such as `Results`, `Method`, or `Figure 3`
- result/evidence slides should usually let one dominant figure or table own about 55-75% of the useful slide area when that visual carries the claim
- keep interpretation in a narrow rail, short takeaway band, or speaker notes; do not let commentary visually outweigh the evidence
- avoid default 50/50 left-right symmetry for figure-led slides unless the text and visual truly carry equal weight
- if a dense figure cannot be read at talk scale, crop it, split it, or move it to its own slide instead of shrinking it into a small slot
- if a slide uses multiple panels, each visible panel must have a distinct analytical role such as overview, comparison/deviation, validation, or relationship/mechanism; do not place two panels that answer the same question unless the redundancy is explicitly useful

## Strict Quality Contract

Treat PPTPRO as a strict production workflow, not a loose style prompt.

One-pass production bar:

- if the user asks for a nicer, better-looking, more polished, class-ready, or graded presentation, interpret that as a request for full visual structure repair, not only color/font cleanup
- before building, decide the final slide count, template scope, slide recipe map, visual enrichment/image plan, and audit/render path
- every revised content slide should have a visible design reason: process flow, image+analysis, matrix, comparison panel, platform/actor mix, conclusion synthesis, source object, or figure-led evidence
- do not wait for user criticism to add relevant images when the deck is text-heavy and the topic has suitable traceable visuals
- do not default to text-card slides when a generated illustration, contextual image, source object, map, process diagram, or compact visual system would make the slide easier to understand
- do not wait for a second pass to vary adjacent layouts; repeated card rows are a defect on the first pass
- do not hand off a template-bound deck until the revised slides and preserved slides have been seen together in a final render or preview

Do not hand off after one generation pass. A PPTPRO deck must go through:

1. design brief
2. template/style inventory when a source deck exists
3. slide recipe selection
4. supporting image/source visual/generated illustration/content visual candidate selection when the deck would otherwise feel text-only
5. editable PPTX build
6. rendered previews
7. manual visual defect sweep
8. repair pass
9. final audit

If a rendered preview shows text touching card edges, visual marks that are not self-explanatory, title overlap, cramped spacing, beige/template-like styling, or script/slide mismatch, revise and rerender before final response.

Also revise and rerender if a preview shows:

- oversized empty cards or panels
- card copy sitting only in the top-left corner of a tall frame
- any card where text crosses, touches, or appears clipped by the card border
- any text box whose visible copy needs more height or width than the box provides
- a page that feels top-heavy, left-heavy, or bottom-empty
- a cover slide that is metadata-only but visually sparse, with a small title/date/presenter cluster and a large unused blank field
- a large empty vertical gap between the main content row and the bottom takeaway
- title lines or title/subtitle spacing that visually compress into one block
- body text that looks small relative to its container
- pill labels, legend tags, or single-word labels wrapping onto multiple lines
- multiple content slides that look like copies of the same card layout with only the text swapped
- a book/source-based deck with no real source object, book cover, source metadata, table/chapter/case structure, or original visual material when such material is available and relevant
- a media/current-case slide that looks like an ordinary text-card slide instead of a clear case/event page with a visible event source and explicit reading connection
- a source-backed deck that remains purely text/card based after source-native visuals and relevant supporting images were available
- generic, decorative, low-resolution, watermarked, AI-looking, or weakly related images added only for visual noise
- AI-generated images used as evidence, source substitutes, real-event proof, or generic decoration instead of content support
- images that overpower the slide, reduce text contrast, crop away meaningful context, or create layout imbalance
- new PPTPRO cards, callouts, or panels using visibly sharp default rectangle corners when no template requires square geometry
- internal project/process language visible in the deck, such as `source log`, `final audit`, `working audit`, `requirement ledger`, `provenance recorded`, or `image credits are recorded`
- a template-bound deck where the revised slides visually detach from the supplied template without user approval
- a partial-scope deck where locked or teammate slides are missing from the final deliverable
- a final full deck whose slide count or slide order no longer matches the locked source deck strategy

## Workflow

1. Lock the deck job:
   - final format
   - slide count or expected pacing, including the default cover and `Thank You` + `Questions & Discussion` closing slide unless an existing template overrides that shell
   - language
   - sources
   - whether a speaker script is required
   - whether sources/references are required by the assignment or only included for traceability
   - for existing decks/templates: total source slide count, revised slide range, preserved slide range, and whether final handoff is the full deck or an excerpt

2. Build the narrative before styling:
   - cover slide: presentation title, presentation date, presenter; keep text metadata-only but design the page as a full cover with balanced placement, scale, logo/brand mark, restrained accent, or one relevant traceable image when needed; do not use presentation duration as the date field
   - for template-bound decks, extract template visual rules and preserve locked/teammate slide ranges before redesigning the user's range
   - if converting from a report, essay, final paper, thesis, or manuscript, inventory the original data figures/images before drafting slides
   - for scientific paper, preprint, journal-club, thesis-seminar, or other figure-led academic decks, classify the source type and choose the narrative arc before assigning slide recipes
   - if building from a book, article, report, or media source, inventory useful real source visuals and structures: cover image, official metadata, table of contents, chapter/case structure, field sites, methods, diagrams, data figures, article screenshots, or media-event facts
   - decide which source figures must appear in the PPT, and record any omitted figure with a reason
   - for scientific paper decks, build a figure plan before layout: selected figure/table, slide claim, why it matters, and whether the original figure should stay whole, be cropped, or be split across slides
   - decide which non-data source visuals or source structures should appear in the PPT so the deck has evidence/object specificity rather than generic summaries
   - for each content slide, decide whether its visual anchor should be a source object, real photo, contextual image, generated illustration, diagram, map, icon cluster, mini chart, or intentionally text-only layout
   - if the deck still risks feeling text-only, search for a limited set of relevant supporting images that can make the source, case, place, event, process, or object more concrete; record image provenance and reject generic filler
   - if no suitable real or traceable image exists and the slide would benefit from a custom content visual, generate a limited number of images with the current latest built-in Codex/ChatGPT image tool; keep the prompts specific to the slide message and record generated-image provenance
   - one job per slide
   - one dominant message per slide
   - speaker-script paragraphs mapped to slide numbers
   - sources matched to the claims they support
   - create a slide recipe map before building: slide number, ownership/scope, recipe, main message, image/source role, and script role
   - decide which `slide-recipes.md` pattern each revised slide uses
   - vary consecutive slide recipes; if two neighboring slides use the same structure, justify it or redesign one of them
   - closing slide: only `Thank You` and `Questions & Discussion`; `Questions` alone is acceptable when a shorter ending fits better, unless the supplied template or partial-scope structure requires a different existing closing/conclusion slide

3. Design the deck:
   - make slide 1 a polished cover with balanced visual mass; make the first content slide a concept or thesis page, not a generic bullet page
   - for book/source decks, make one early content slide a source/object page using real cover/metadata or source structure when available
   - make middle slides explain relationships through diagrams or flows
   - for scientific paper decks, use conclusion-style titles on most content slides rather than labels such as `Results`, `Method`, or `Figure 3`
   - use actual source structure for middle slides when possible: field-site comparison, chapter map, method/evidence map, case matrix, or source figure
   - for figure-led evidence slides, let the main figure or table dominate the page when it carries the claim; keep interpretation compact and subordinate
   - if a multi-panel scientific figure is used, give each visible panel a distinct analytical job rather than repeating similar subpanels that answer the same question
   - use supporting images as content anchors when they clarify the topic: pair an image with short analytical text, use a map/place image for field sites, use a news/event image for media cases, or use object/process photos for technical material
   - use generated illustrations or generated context images when a slide needs a visual scene, process, metaphor, or object composition that cannot be sourced cleanly
   - prefer mixed visual pacing over repeated text cards: image+analysis, diagram+takeaway, source object+structure, generated illustration+mechanism, or compact chart+interpretation
   - make media/case slides show why the example fits the reading or argument
   - make media/case slides visually read as a case page: event/source block on one side, theory/reading connection on the other
   - use open spacing, strong alignment, and a clear visual hierarchy
   - size cards around their actual content density instead of using large default boxes
   - reserve real padding inside each card before placing text; do not align text boxes exactly to card edges
   - use softer rounded-rectangle cards and callouts by default; keep radius visually consistent across the deck
   - after adding text, re-check the longest line and the last line against the card border
   - distribute the main content through the middle and lower-middle canvas, not only near the title
   - if a bottom synthesis bar is used, position or extend the main visual system so the middle does not become an empty gulf
   - give multi-line titles enough line height and keep a clear gap between title and subtitle
   - replace sparse card rows with compact cards plus synthesis bars, evidence chips, mini charts, or comparison strips
   - for a regional/topic sequence, do not give each region the same title + three-card + bottom-bar layout; vary the pages through image+analysis, mechanism/process, comparison matrix, platform mix, source/event page, or conclusion synthesis recipes

4. Generate editable PPTX:
   - use native PPT objects, text boxes, shapes, lines, and editable cards
   - use the source document's original data figure/image assets for evidence visuals; preserve aspect ratio and only crop margins or irrelevant surrounding whitespace
   - use real source visuals such as book covers, report covers, source screenshots, tables of contents, or article/media source blocks when they clarify what source is being discussed
   - use relevant supporting images when they improve presentation clarity or display power; keep them cropped cleanly, high enough resolution for projection, and visually subordinate to the slide's argument
   - use generated images or illustrations for custom conceptual, process, atmosphere, context, or object-composition visuals where they add clarity; never use them to replace original source/data visuals or imply real-world evidence
   - avoid screenshots of text as the final slide content
   - keep visible sources in quiet human-facing footers or a clearly labeled `Sources used` section when needed; do not mention source logs, audits, provenance records, working files, or other internal project tracking in the deck
   - for partial-scope template edits, preserve unedited slides in the final full deck; if the source only exists as PDF/images, append visually faithful full-slide images for the preserved range and record the limitation

5. Generate script when requested:
   - mark script sections as `[Slide 1: ...]`, `[Slide 2: ...]`, etc.
   - keep the script aligned with slide content
   - keep wording natural and presentation-ready

6. Check repeatedly:
   - render or preview every slide if tooling is available
   - inspect previews visually for overflow, overlap, odd spacing, and unclear design marks
   - run `scripts/pptpro_audit.py --strict` when working with local `.pptx` files
   - for partial-scope decks, run strict audit on the revised range when preserved slides are image-only or otherwise not parseable, then render and inspect the final full deck for assembly, page count, order, and visual continuity
   - fix defects and rerun the checks

## Required Checks Before Handoff

- No serif fonts unless explicitly required.
- No beige/cream default background unless explicitly requested.
- No text overflow, clipping, or obvious overlap in previews.
- No card text outside the card safe area or visually touching the border.
- No text box that is too short/narrow for its rendered copy.
- No giant empty card frames, sparse panels, or text stranded at the top-left of a tall box.
- No top-stacked layout with a large blank middle or bottom area.
- No cramped multi-line title or title/subtitle collision.
- No short pill/tag labels wrapping across lines.
- No slide whose meaningful content is visually concentrated only in the upper portion.
- Deck includes a cover slide with presentation date, not duration, and a final closing slide containing only `Thank You` plus `Questions` or `Questions & Discussion` unless explicitly forbidden.
- Cover slide is not mostly blank: the metadata may be minimal, but title placement, scale, accent/image/logo use, and lower-canvas balance must create a complete cover composition.
- For template-bound decks, existing required cover/conclusion/closing structure is preserved unless the user approved a replacement.
- No unexplained lines, dashes, boxes, or decorative marks.
- Slide text and script sections correspond.
- Source-backed claims are traceable.
- Scientific paper or journal-club decks classify the source type and follow a visible argument arc rather than mechanically mirroring the paper section order.
- Source-backed decks avoid repeated same-structure pages; consecutive content slides should be visually and conceptually distinct unless the repetition is intentionally useful.
- Figure-led scientific slides use conclusion-style titles and a readable evidence hierarchy rather than generic labels such as `Results` or `Figure 3`.
- Multi-panel scientific slides avoid redundant panels; each visible panel has a distinct analytical job and remains readable at presentation scale.
- Book/source-based decks include relevant real source material when available: cover or official metadata, table of contents/chapter structure, field sites, cases, methods, evidence types, original figures, or media/article source blocks.
- Media/current-case slides look like case analysis, not generic text summaries; the visible event/source and the reading/theory connection are both clear.
- Relevant images, illustrations, diagrams, or source-object visuals were planned for text-heavy decks. Any external supporting image used is source-attributable, relevant, high enough quality, and not generic filler.
- Images do not reduce readability, cover key text, overtake the slide, create awkward crops, or replace required original data/source evidence.
- Generated images, if used, have a clear content role, were made with the current latest built-in Codex/ChatGPT image tool, and are logged as generated assets rather than cited factual sources.
- No visible slide text, footer, note intended for delivery, or speaker-script line contains internal project workflow language such as `source log`, `final audit`, `working audit`, `requirement ledger`, `provenance recorded`, or `image credits are recorded`.
- For decks made from reports, essays, final papers, theses, or manuscripts, original data figures/images used in the source document were inventoried and relevant ones were reused in the PPT.
- No real data figure from the source document was silently replaced by a generic redraw, AI-generated image, icon, or text-only paraphrase.
- New cards, panels, callouts, and synthesis bars use consistent softer rounded corners unless an existing template requires square-corner geometry.
- Final folder contains only the user-required deliverables.
- Partial-scope edits preserve unedited sections in the final full deck unless an excerpt-only deliverable was explicitly locked.
- If strict audit was run on a revised-range audit copy because preserved slides are image-only, the final full deck was still rendered and manually inspected.
- A visual preview pass was performed, or the final response states precisely why it could not be performed.
- The final deck uses an identifiable recipe from `slide-recipes.md` rather than ad hoc text placement.

## Useful Resource

Run the audit script from any project folder:

```bash
python /Users/zin/.codex/skills/pptpro/scripts/pptpro_audit.py path/to/deck.pptx --script path/to/script.docx --render --strict
```

After inventorying source-document data figures or deciding to use supporting images, add `--min-pictures N` when the final deck is expected to contain at least `N` original source or supporting image assets.

If `--render` is used on macOS, the script attempts per-slide Quick Look PNG previews.
