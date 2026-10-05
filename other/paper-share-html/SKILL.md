---
name: paper-share-html
description: Create or revise audience-ready HTML paper presentations for lab meetings and journal clubs. Use when Codex needs source-grounded figures and tables, a fluent live-talk narrative, verified quotations, varied explanatory diagrams, presenter-paced reveals, or browser QA for evidence fidelity, interaction, responsive layout, and print.
license: MIT
---

# Paper Share HTML

Build a source-grounded paper presentation that works as a live talk first and
as a readable static page second. Keep the narrative audience-facing: the page
must present the research, not explain the editing process to the requester.

## Read First

- Read [references/editorial-style.md](references/editorial-style.md) before
  drafting Chinese copy, quotations, or slide titles.
- Read [references/visual-qa.md](references/visual-qa.md) before extracting
  figures/tables or validating the finished page.
- Read [references/visual-story-patterns.md](references/visual-story-patterns.md)
  before designing explanatory or synthesis diagrams.
- Use [assets/template/index.html](assets/template/index.html) as a structural
  starter, not as a fixed slide count or visual theme.

## Workflow

### 1. Ground the report in primary sources

Inspect the complete paper before drafting. Prefer the local PDF; otherwise use
the official publisher, arXiv, project, and code pages. Record the exact title,
authors, version, venue or identifier, project URL, code URL, and BibTeX when
available. Download the paper and supplementary material into `source/` when
licensing and access permit.

Treat the paper as the source of truth for claims, metrics, captions, and
quotations. Use external primary sources to verify cited work and full titles.
Never reconstruct missing citation metadata from memory. If verification is
not possible, mark it as unverified in working notes and omit it from the
audience-facing page rather than guessing.

### 2. Ask one compact intake

After inspecting the supplied material, use `request_user_input` or the
available equivalent when the answers are not already known. Ask at most three
questions in one intake:

1. audience and talk duration;
2. emphasis: balanced, method, results, or critical discussion;
3. delivery language.

Offer concrete choices and put the recommended choice first. If the tool is
unavailable or the user does not answer, use these defaults:

- cross-disciplinary research group;
- 15-20 minutes;
- balanced reconstruction plus evidence review;
- natural Chinese narration with English paper titles, technical terms, and
  verbatim quotations preserved where accuracy benefits.

Do not ask for decisions that can be derived from the paper or workspace.

### 3. Build a claim-evidence map

Before writing HTML, identify:

- the problem and why existing approaches are insufficient;
- the paper's central claim and assumptions;
- the mechanism that is necessary to understand the claim;
- the strongest evidence, including metric direction and comparison scope;
- limitations, unresolved questions, and unsupported extrapolations;
- the final takeaway appropriate for the selected audience.

Separate author claims, observed experimental results, and the presenter's
assessment. Use a problem -> claim -> mechanism -> evidence -> boundary ->
takeaway arc when it fits, but add, merge, or reorder sections to match the
paper. Do not force every paper into the same number of slides.

### 4. Storyboard and rehearse the argument

Assign one main rhetorical job to each slide. For every slide, verify what it
inherits from the previous slide, what it establishes, and why the next slide
is now necessary. Add full-size figure, qualitative comparison, or visual
transition slides when they improve comprehension; do not assume every slide
needs the same speaking time.

Mark a slide for progressive disclosure only when the presenter must establish
an actual sequence, such as a causal chain, timeline, equation construction,
method data flow, or evidence boundary. Do not fragment ordinary prose or
complete experimental comparisons merely to add motion.

Read the sequence aloud as a presenter before polishing individual sentences.
Repair missing premises, repeated claims, abrupt method-to-result jumps, and
conclusions that exceed the evidence. Prefer a coherent talk over a fixed slide
count or a mechanically repeated section template.

### 5. Create the paper package

Run:

```bash
python scripts/init_paper_share.py --title "FULL PAPER TITLE" --root "OUTPUT ROOT"
```

Use `--folder-name` only when the user explicitly chooses a short title or the
automatic main-title folder is ambiguous. The script refuses to overwrite an
existing package.

Maintain this output contract:

```text
Paper Main Title/
├── index.html
├── assets/
│   ├── figures/
│   └── tables/
│       └── raw/
├── source/
└── qa/
    └── archive/
```

Keep CSS and JavaScript inside `index.html`; keep visual assets as relative
files. The report must open directly through `file://` without a development
server or network dependency.

### 6. Prepare visual evidence

Use paper and project-page visuals before decorative or generated imagery.
Preserve original figures unless a simpler explanatory redraw is genuinely
needed; label any redraw as a schematic and do not alter the scientific claim.

For rasterized paper figures and experimental tables, render directly from the
PDF at about 300-360 DPI or at least 3x scale. Preserve the initial page or
capture in `assets/tables/raw/`, then crop the presentation copy tightly around
the table. Do not upscale a small screenshot and call it high resolution.

Use 1600-2200 pixels as a practical full-slide table target and treat 1400
pixels as the warning floor. Make the table readable in the default desktop
view; click-to-zoom is only a secondary inspection path. Prefer a faithful
image over manually retyping values. State metric direction, comparison scope,
and meaningful exceptions honestly.

### 7. Design explanatory visuals

Use original diagrams only for background, related work, method explanation,
or presenter synthesis. Never redraw experimental evidence in a way that can be
mistaken for a paper result. Keep each synthesis traceable to the figures,
tables, or claims it combines.

Choose composition from the semantic relationship: sequence, comparison,
hierarchy, convergence, feedback, continuum, evidence structure, or state
change. Do not default to a left-to-right row of rectangular boxes. Add
`data-visual-pattern` to slides containing original diagrams so the audit can
detect repeated horizontal chains. Variation serves meaning; do not change
layouts merely to make adjacent slides look different.

### 8. Write for the audience

Use direct, formal, natural statements. Make slide titles carry the finding or
question rather than editorial labels. Explain unfamiliar terms where they
first matter without calling the audience outsiders or announcing a simplified
version.

Let a readable table or figure carry secondary metrics and tradeoffs when it
clearly shows the metric, unit, direction, comparison scope, and necessary
conditions. The narration and slide copy should state the main finding and its
meaning; do not make a table-visible drawback the final line of a talk track.
Keep a boundary condition when it affects fairness, applicability, or the central
claim, and state it directly where the audience interprets the evidence. Avoid
defensive setup or pre-emptive concessions; contrast words remain appropriate
when they express a real logical relation.

When literary, historical, or cross-disciplinary language participates in the
paper's argument, include it only when it improves the talk. Preserve the full
English sentence, provide the full title of the cited article or book, and let
the Chinese text continue the argument. Do not create a compulsory quote slide
or cite only an internal location such as “Section 2” or “the abstract.”

### 9. Build the presentation

Adapt the template's theme and composition to the paper while retaining:

- desktop 16:9 slide navigation;
- continuous narrow-screen reading;
- keyboard and icon-button navigation;
- progress indication;
- an accessible image lightbox;
- print styles;
- stable dimensions that prevent layout shifts;
- descriptive alternative text.

Use `data-fragment="N"` for optional presenter-paced disclosure. Start at `1`
on each slide, keep groups contiguous and in DOM order, and give elements the
same number when they must appear together. Do not nest fragments. Forward
actions reveal the next group before changing slides; backward actions hide the
latest group before returning. Preserve per-slide progress when revisiting a
slide.

Keep primary result tables, quantitative plots, and qualitative comparisons
fully visible by default. Fragment method schematics or presenter synthesis
only when the reveal order clarifies a genuine dependency without hiding
evidence needed for comparison. Exclude links, controls, images, selected text,
and lightbox interaction from click-to-advance behavior.

Progressive content must remain fully visible on mobile, in print, and without
JavaScript. Respect `prefers-reduced-motion`, and keep transitions to a quiet
180-250 ms fade or slight vertical movement.

Remove every placeholder and unused component. Do not add visible instructions
about how the presentation was written or how the audience should operate it.

### 10. Audit and verify

Run the static audit:

```bash
python scripts/audit_paper_share.py "PATH/TO/PAPER PACKAGE"
```

Fix all errors and review every warning. Then open `index.html` in a real
browser and validate at desktop and mobile viewports. Exercise every slide,
keyboard navigation, table lightbox, local asset, external source link, and
print layout. At 1280x720, 1440x900, and 1920x1080, confirm that ordinary table
cells are readable without zoom and that dense tables are not compressed into
split or card layouts. Save final screenshots under `qa/` and iteration
artifacts under `qa/archive/`. Inspect screenshots visually; a successful
command is not proof that the page is legible or the talk is coherent.

When fragments are present, also verify forward reveal, backward retreat,
progress persistence, first/last boundaries, click isolation, mobile and print
expansion, no-JavaScript readability, and reduced-motion behavior.

### 11. Deliver the package

Report the direct local link to `index.html`, the source and QA artifacts
created, and any claim or citation that could not be verified. Do not deploy
the report unless the user explicitly asks for hosting.

## Non-Negotiable Checks

- Do not address the requester inside the presentation.
- Do not use meta labels such as `一句话版`, `外行版`, `值得展示的表述`,
  `下面保留`, `这页适合`, `结果解读`, or `表格解读`.
- Do not shorten a quotation while presenting it as a complete sentence.
- Do not invent a full reference title or metric value.
- Do not claim universal superiority when the table supports only most metrics
  or a subset of tasks.
- Do not accept a small table merely because a zoom control exists; the default
  slide view must remain readable.
- Do not present a PDF screenshot with long captions or large page margins as a
  finished table crop.
- Do not repeat a horizontal box-and-arrow chain across three consecutive
  original-diagram slides.
- Do not invent a unified star rating or strength scale for assumptions that
  act at different levels unless the source defines and measures that scale.
- Do not fragment a primary experimental table or comparison figure to force
  the audience through evidence that should be judged simultaneously.
- Do not finish without desktop and mobile visual inspection.
