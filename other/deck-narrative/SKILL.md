---
name: deck-narrative
description: >
  The ARCHITECTURE layer beneath every deck skill — decides WHAT goes on slides
  and in WHAT ORDER, before any visual skill decides what it looks like. Covers
  action titles vs topic titles (the verb test), one-message-per-slide, Minto
  top-down sequencing (conclusion on slide 2, never a surprise ending), pacing
  by meeting length, horizontal logic (titles alone read as a persuasive essay)
  and vertical logic (body proves title), table-vs-chart selection, and
  decision/approval-slide construction (Challenge>Options>Decision,
  Goal>Obstacle>Strategy>Action, Insight>Action>Outcome). Every rule is written
  as an auditable pass/fail check, not a style opinion. Ships
  `scripts/audit_deck.py` — a runnable Python auditor that reads a .pptx and
  mechanically reports per-slide font size, title word/line counts, a
  verb-test heuristic, table vs chart counts, reader-only-content (process-
  meta marker) review candidates, a deck-wide font-family inventory with a
  hard system-font (Calibri/Arial/etc.) fail flag, and a title-sequence dump
  for human/agent read-through. Co-load with `strategic-deck` or
  `marp` (or whichever deck/visual skill your setup uses) — this skill is
  silent on color, aesthetic font choice, and layout; it only decides content,
  order, and one narrow file-level exception (Rule 9: does the .pptx leak an
  Office default font that no visual review can see because the renderer
  substitutes a lookalike). Trigger on "review this deck's narrative", "does
  this deck make sense", "audit deck structure", "is this an action title",
  "check my slide titles", "Minto pyramid", "top-down deck", "one message per
  slide", "deck says nothing" / "deck doesn't land" / "deck feels like a wall
  of text", "should this be a table or a chart", "decision slide", "approval
  slide", "check deck fonts", "system font check", or any request to
  build/fix/review a deck's argument rather than its look. Numeric thresholds
  (slide counts, pt sizes, word limits) are MEDIUM-confidence conventions from
  McKinsey/BCG/Bain practice — present as defaults with stated reasoning,
  never as hard gates that block work.
---

# deck-narrative

Deck-building skills in this system (e.g. `strategic-deck`, `marp`,
or whichever visual/deck skill your setup uses) are all **visual systems** —
CSS classes, palettes, fonts, slide-type names, build mechanics. None of them
say anything about whether the *content* is any good: whether the title makes
a claim, whether the deck argues top-down, whether a table should have been a
chart. This skill is the missing layer underneath all of them. It is a
**reasoning discipline, not a template.**

## Read this first: architecture vs visual system

| Layer | Decides | Owned by |
|---|---|---|
| **Architecture** (this skill) | What goes on the slide, in what order, and whether it makes an argument | `deck-narrative` |
| **Visual system** | What it looks like — color, type, layout, motion | `strategic-deck` / `marp` / whichever visual skill your setup uses |

**Co-load, don't choose.** When building or reviewing a deck, load `deck-narrative`
alongside whichever visual skill applies (your project's routing convention
decides which visual skill to co-load). This skill never touches CSS,
`pptxgenjs` calls, or slide-type names — it decides the titles, the sequence,
and whether a slide should be a table or a chart, then hands the visual skill
the content to lay out. Running a visual deck skill without this one is how
decks get built by instinct: correct fonts, no argument.

**The one narrow exception (Rule 9):** which brand font to use, its weight,
its pairing — those stay the visual skill's job (whichever brand/visual skill
you co-loaded). But whether the shipped `.pptx` FILE actually contains that
font, versus an Office default that survived because a rendering pipeline
substituted a lookalike glyph, is not an aesthetic judgment — it's a
file-integrity check a visual review structurally cannot make (see Rule 9
below). That single check lives here because it needs to read the `.pptx`
XML, not because deck-narrative has an opinion on typography.

## Provenance and confidence

Source: NotebookLM deep research, 61 web sources — McKinsey/BCG/Bain deck
conventions, Barbara Minto's pyramid principle, Michael Alley's
assertion-evidence structure, Edward Tufte's data-ink principle. Full source:
internal research archive (not included in this public skill mirror).

- **Structural rules** (action titles, one-message-per-slide, top-down
  sequencing, horizontal/vertical logic) — **HIGH confidence.** Multiple
  independent sources converge.
- **Exact numeric thresholds** (word counts, pt sizes, slide counts, minutes
  per slide) — **MEDIUM confidence.** These are conventions that vary by
  source, not laws. Present them as defaults with stated reasoning. Never
  treat a threshold miss as a hard gate that blocks shipping a deck — flag
  it, explain why the convention exists, let the human/agent decide.

---

## Rule 1 — Action titles vs topic titles

**The rule:** a slide headline must make a complete, active claim, not name a
category.

**Checks:**
- Contains a verb — not just a noun phrase.
- ≤15 words.
- ≤2 lines.
- **"So what" test:** the title states the strategic implication of the
  slide's content, not just a label for it. (Judgment — see below.)
- Layout: left-justified, 30-32pt. Under 28pt is a text-stuffing red flag
  (MEDIUM-confidence convention — a slide with a 24pt title isn't broken, but
  it's a signal the title got squeezed to fit too much).

**Before/after:**
- Before (topic label): *"Launch Readiness"*
- After (action title): *"Launch Is 6 Weeks Behind Schedule — Three Decisions
  Required by Friday to Recover the Timeline"*

**Worked example (anonymized, from a real audit)** — a defence-sector
trade-show deck audit (see `scripts/audit_deck.py` output below): slide 8's
title *"Từ hợp tác toàn cầu đến làm chủ công nghệ"* ("From global cooperation
to technology mastery") is a topic label — a "from X to Y" bridge phrase with
no independent verb clause and no claim. It names the section, it doesn't
argue anything. Compare slide 14: *"Kênh duy nhất tăng tiếp cận với chi phí
media bằng 0"* ("The only channel that grows reach at zero media cost") — a
verb ("tăng"/"grows"), a claim, a number backing it up.

**Mechanical vs judgment:** the verb test and word/line counts are mechanical
— `audit_deck.py` checks them. The "so what" test (does the claim carry
*implication*, not just description) is judgment — flag candidates, don't
auto-fail them.

---

## Rule 2 — One message per slide

**The rule:** each slide conveys exactly one distinct insight.

**Checks:**
- **The "so what" element test:** point at any chart, shape, or text block on
  the slide. If it doesn't directly prove the action title, delete it.
- **The 5-second test:** a viewer grasps the core point within 5 seconds of
  first seeing the slide.
- **The 10-second test:** a reader can explain the slide's purpose and proof
  back to you in 10 seconds.
- **The 90% whitespace rule:** if the canvas is ≥90% full, it's overloaded —
  split it into two slides.

**Mechanical vs judgment:** none of this is mechanically checkable from a
`.pptx` file alone — it requires reading the slide the way a viewer would.
This is human/agent judgment, always. `audit_deck.py` cannot run the 5-second
test; a critic agent with the rendered slide can.

---

## Rule 3 — Minto pyramid / top-down sequencing

**The rule:** present arguments top-down — conclusion first, supporting
pillars second, granular evidence third. Never save the recommendation for a
"surprise ending."

**Checks:**
- **Conclusion first:** the recommendation appears on slide 2, not buried at
  the end.
- **Title slide (slide 1):** exactly three elements allowed — presentation
  title (<10 words), client/company logo, date. Nothing else.
- **The five-minute window (slides 1-3):** these three slides completely
  outline the entire recommendation. A reader who only sees slides 1-3 should
  know the whole argument.
- **The bold-bullet summary (slide 2):** use bold-bullet format; the bolded
  phrases alone must tell the entire story when skimmed.

**Worked example (same anonymized deck):** puts the single committed KPI
("Reach is the only committed KPI") on slide 2, immediately after the cover —
not a section-by-section build toward a reveal. That's the pattern to
replicate.

**Mechanical vs judgment:** "is slide 2 actually the conclusion" and "do
slides 1-3 outline the whole recommendation" require reading content and
comparing against the deck's actual thesis — judgment, not something
`audit_deck.py` can verify from shape geometry.

---

## Rule 4 — Pacing and text density

**The rule:** align slide count and formatting to the meeting length, to
prevent live cognitive overload.

**Checks (MEDIUM-confidence conventions, present as defaults):**
- 20-minute slot → target ~10 slides.
- 30-minute slot → 10-15 slides (max 15-25).
- Board meeting → 10-15 slides.
- Reserve the last ~10 minutes of a 30-minute slot entirely slide-free, for
  Q&A/discussion.
- Pacing: 1-2 minutes per slide.
- On-slide limits: max 5-7 bullets, max 6-8 words/line, max 2-3 lines of body
  text. Apply the 5×5 rule (5 words/line, 5 lines/slide) or 7×7×7 as house
  convention allows.

**Mechanical:** slide count and word-per-title checks are mechanical
(`audit_deck.py` reports both). Bullets-per-slide and words-per-line on body
content would require parsing every text box on every slide — not currently
in the script; extend it if a deck's body density becomes a recurring
problem.

---

## Rule 5 — Horizontal and vertical logic

**The rule:** verify narrative continuity across the deck (horizontal) and
empirical support within each slide (vertical).

**Checks:**
- **The read-through test (horizontal):** strip away everything but the
  titles, read them in sequence. If they don't read as a logically flowing,
  persuasive essay — the deck's "narrative spine" — it fails.
- **The dual-coding test (vertical):** strict 1-to-1 correlation — the visual
  in the slide body must immediately prove the claim in the title.

**Mechanical vs judgment:** `audit_deck.py` prints the full title sequence in
order specifically so a human or agent can run the read-through test — the
script cannot judge whether titles "read as a persuasive essay," but it
removes the friction of extracting them by hand. The dual-coding test
(does the body prove the title) needs the slide content, not just its shape —
judgment.

---

## Rule 6 — Tables vs charts

**The rule:** choose the data format for the audience's cognitive task, not
visual variety.

**Checks:**
- **Use a TABLE when:** presenting precise values to look up/compare, sparse
  data, ≤20 numbers, or when a zero-baseline would compress/distort variation.
- **Use a CHART when:** showing trends, variations, or relationships. Match
  chart type to comparison goal:
  - Trend over time → line chart
  - Categorical ranking → bar/column chart (pie capped at 6 categories)
  - Part-to-whole → stacked bar or Mekko (cap at 5 segments)
  - Cumulative walk → waterfall chart

**Mechanical:** `audit_deck.py` counts tables vs charts per slide and
deck-wide (via `shape.has_table` / `shape.has_chart`). It does NOT judge
whether a given table *should* have been a chart — that requires knowing the
underlying data shape and the audience's task, which is judgment. A deck-wide
`total_charts: 0` with several tables holding trend data (numbers changing
across time periods) is a real signal worth a human/agent look — the script
surfaces the count, not the verdict.

**Hand-off:** when a table should become a chart, or a new chart is needed,
use whichever chart-rendering skill or tool your setup provides to produce a
native, editable chart (e.g. a `pptxgenjs` `addChart()` call, or an
SVG-as-PNG embed for chart types with no native PPTX equivalent: waterfall,
heatmap, bullet). If the right chart type isn't obvious, pick it by data
relationship + category count + audience task (see Rule 6's checks above)
before rendering. `deck-narrative` decides *that* a chart is needed and *what
kind* in principle (Rule 6 above); your chart-rendering tool renders it.

---

## Rule 7 — Decision / approval-request slides

**The rule:** action slides must clearly define options, stakes, and next
steps to force an outcome.

**Checks:**
- **Visual placement:** the requested decision sits in a distinct callout box
  at the bottom of the slide.
- **Grammar standard:** bullets always begin with an active verb (Grow,
  Reduce, Improve, Increase, Target).
- **Approved structural frameworks — audit against one of these three:**
  1. *Challenge > Options > Decision* — problem, paths, recommendation.
  2. *Goal > Obstacle > Strategy > Action* — objective, barriers, approach,
     direct steps.
  3. *Insight > Action > Outcome* — finding, proposal, expected return.
- **Credibility:** every data point cites a source line at 8-9pt.
- **Pre-wire verification:** confirm key recommendation slides were shared
  individually with stakeholders before the meeting — eliminate surprises.

**Worked example (same anonymized deck):** slide 22, *"Đề nghị ban lãnh đạo /
người phê duyệt phê duyệt các nội dung sau"* ("Requesting the board / the
approver approve the following") — an active-verb approval ask. Slide 20's
title (*"Người trình bày → Người phê duyệt → CEO + Chủ tịch"* / "Presenter →
Approver → CEO + Chairman") is the governance-chain slide feeding into it —
worth checking it isn't standing in for the actual decision framework above.

**Mechanical vs judgment:** active-verb-bullet detection and callout
placement could be scripted (not yet in `audit_deck.py` — extend if this
becomes a recurring gap). Which of the three frameworks a given slide fits,
and whether pre-wiring actually happened, are judgment calls outside what any
script can see in a `.pptx` file.

---

## Rule 8 — Reader-only content (no process meta in the .pptx, and no
spoken material on the slide)

**The rule:** every slide must contain only information the audience needs
to **see**. This is two separate tests, applied in order. Getting either one
wrong does damage — Test 1 wrong in the strict direction guts the deck's
most important slides; Test 2 skipped entirely produces the bloated,
over-justified decks this rule exists to prevent.

### Test 1 — addressed to the audience, or to the producer/reviewer?

Process and production annotations — "decision needed", "comment on
content", "needs review", "TBD", "placeholder", open questions, reviewer
notes, confirmation requests aimed at the producer or an internal reviewer —
belong in the accompanying `.html` plan/working document, never the
`.pptx`. The `.pptx` is the artifact that leaves the building; it gets
forwarded to executives and clients standalone, with no narration and no
context. Process meta aimed at the internal reviewer reads as unfinished
work to the person who receives it.

The discriminator is **who the line is addressed to — NOT whether it
mentions a decision.**

- **PASSES Test 1 (stays, subject to Test 2):** a line addressed to the
  deck's actual audience — the person who reads this deck cold, with no
  narration, and is expected to act on it. Asking the deck's real
  decision-maker to decide something IS reader-useful.
- **FAILS Test 1 (moves to .html):** a line addressed to the producer or an
  internal reviewer — anyone standing between the deck and its audience.
  Markers: "TBD", "placeholder", "needs review", "under review", "open
  question", "confirm with the internal reviewer", "draft",
  unverified-assumption flags, reviewer commentary asking an internal party a
  question.

### Test 2 — does the audience need to SEE it, or can the presenter SAY it?

**This is the test that makes decks shorter, and the one that carries real
weight here — not a footnote to Test 1.** Passing Test 1 is necessary but
not sufficient. Even genuinely audience-facing content — supporting
rationale, evidence tables, methodology, the reasoning behind an ask — is
usually **spoken**, not slide real estate. Executives and boards do not have
time to read what was researched; they ask when they want more, and the
presenter answers live (or from an appendix built to answer exactly that
question if it comes up). A deck that pre-empts every possible question with
a slide is too long by construction.

**Rule of thumb:** the ASK can stay on a slide. The JUSTIFICATION behind the
ask usually should not.

**Interaction with Rule 4 (pacing):** Test 2 is a primary mechanism for
hitting the 10-15 slide board-meeting target — it is not a separate concern
from pacing, it is how pacing actually gets achieved without cutting content
that matters. A deck failing Rule 4's slide-count guidance is very often a
deck that skipped Test 2.

**Worked example (anonymized) — the corrected read on a real defence-sector
deck:** slides 5, 6, and 7 each gave one of three go/no-go decisions its own
slide, with supporting context and evidence on each. Test 1 alone would have
kept all three as-is (they're addressed to the approver, the actual
decision-maker — correct under Test 1). **Test 2 changes the verdict:** the
chairman and the board don't have time to read the research behind each ask;
they'll ask if they want it, and the presenter answers outside the slide.
Correct treatment is **one slide** stating all three asks, with the
supporting reasoning spoken (or held in appendix) — a 3-slides-to-1
compression driven entirely by Test 2, not by Test 1.

**Other worked examples (Test 1 only — these do not implicate Test 2, they
are already single asks with no accompanying research dump):**

- **PASSES both tests** — slide 22: *"Đề nghị ban lãnh đạo / người phê duyệt
  phê duyệt các nội dung sau"* ("Requesting the board / the approver approve
  the following"). Addressed to the deck's actual decision-maker (Test 1),
  and it's the ask itself, not the justification (Test 2). This is Rule 7's
  approval-slide pattern — Rules 7 and 8 agree here.
- **PASSES Test 1** — slide 7 (v3): *"Cần xác nhận: đội marketing đang kiểm
  soát các trang hiện có"*. Trips the "cần xác nhận" (needs confirmation)
  marker on sight, but read who it's addressed to: it's one of the items the
  deck's audience (the approver) must settle by the deadline. It stays as an
  ask — whether the surrounding slide also carries research-dump
  justification that should be spoken instead is a separate Test 2 question
  to ask of the slide as a whole.
- **PASSES both tests (data gap, not a process note)** — slide 7 (v3):
  *"Audit 07/2026 (chưa xác định)"*. A table cell stating a factual data
  gap — the audit hasn't happened yet — addressed to the reader who needs to
  know the number isn't in, not a note asking an internal reviewer for
  anything. The naive "contains chưa xác định → strip" rule would wrongly
  gut this cell.
- **FAILS Test 1 (hypothetical, not present in the live deck):** *"TBD —
  confirm actual CPM with media buyer before this goes to the approver"*.
  Addressed to the producer/internal team, not the audience. Never survives
  into a shipped `.pptx` — it belongs in the `.html` plan's
  surfaced-questions section.

**Where stripped/spoken material goes:** the `.html` plan/working document,
per `html-plan-style` — that is the working surface where review commentary,
process meta, and the spoken-not-shown supporting rationale all live.

**Mechanical vs judgment:**
- Test 1 is scriptable as a heuristic. `audit_deck.py`'s process-meta scan
  (see below) can find marker strings ("TBD", "chưa xác định", "cần xác
  nhận", etc.) anywhere in slide text — shapes and table cells both. It
  CANNOT tell producer-facing from audience-facing — that still requires
  reading who the line speaks to. Every hit is reported as a **REVIEW
  CANDIDATE**, never a violation. Treating a marker match as an automatic
  fail is the naive implementation this rule explicitly warns against — see
  the KEEP examples above, both of which trip a marker and are correct
  as-is.
- Test 2 is **pure judgment and is explicitly NOT automated.** See-vs-say
  requires knowing what the audience already needs vs. what they'd only ask
  for — there is no mechanical signal for that in a `.pptx` file.
  `audit_deck.py` lists it in its NOT-CHECKED-BY-THIS-SCRIPT output by name
  so a reviewer knows to apply it by hand on every slide, especially ones
  that passed Test 1.

---

## Rule 9 — No system-font leak in the shipped file (file-level, not aesthetic)

**The rule:** every text run and every reachable chart-text element in the
`.pptx` must declare a real font — never an Office/OS default (Calibri,
Arial, Times New Roman, Helvetica, Cambria, Verdana, Tahoma). This is not a
brand preference call; whichever brand/visual skill you co-loaded should
already state it outright: "Never use system fonts (Arial, Calibri) — they
immediately signal non-institutional origin." Whichever fonts your project's
brand skill declares canonical, that skill owns which fonts are correct —
this rule only owns whether the file leaked a default.

**Why this rule exists — a live incident, not a hypothetical:** a manual XML
dump of an anonymized real deck (v3 of a three-build revision cycle) found
every text run set to Calibri. This script's own scan reproduces that
finding independently — Calibri is the only named font in all three build
versions, 100% of runs/elements in each (622 in v1, 608 in v2, 688 in v3 —
see verification below; exact counts differ from a hand dump depending on
what's counted as a "run," but the finding — zero non-system fonts anywhere
in the deck — is unambiguous and reproducible). That defect survived a full
8-dimension design critique, a manual visual verification, and three build
cycles — because every one of those checks inspected a *rendered* view (JPEG
screenshots, a live preview), and the renderer substituted a lookalike
sans-serif that LOOKED correctly typed. The defect was only visible by
reading the file's XML directly. **This is the exact class of defect a
file-reading auditor exists to catch and a visual review structurally
cannot** — no amount of eyeballing a screenshot finds a font substitution
the renderer is actively hiding from you.

**Checks:**
- **System-font hard flag — MECHANICAL, HIGH confidence.** Calibri, Arial,
  Times New Roman, Helvetica, Cambria, Verdana, Tahoma anywhere in the deck
  is a hard fail, not a review candidate. A font name string either is or
  isn't in this fixed list — no judgment required, no addressed-to test, no
  discriminator to get wrong. Unlike Rule 8, this check IS a verdict.
- **Font inventory.** Every distinct font family found, with a run/element
  count, reported regardless of pass/fail — useful context even on a clean
  deck.
- **Unset/theme-inherited font count**, reported separately. A run with no
  explicit font name inherits from the presentation theme — invisible in the
  file, resolves differently machine to machine. Not necessarily wrong, but
  always worth knowing; not folded into the system-font flag.
- **Expected-family check — optional, brand-supplied.** `--expect "Be
  Vietnam Pro,Manrope"` flags any named font outside that set (this example
  uses one project's actual brand fonts — swap in yours). Omit it and the
  script reports the inventory with no family-membership judgment beyond
  the system-font check — `deck-narrative` does not hardcode brand font
  names; they come from whichever brand/visual skill you co-loaded for this
  build.
- **Scope: text runs AND chart text.** Shape text frames, table cells, chart
  title, category/value axis tick labels, legend, and plot/series data
  labels are all walked. Chart text is the usual miss — a deck's tables can
  look correctly typed while its chart axis labels quietly default to a
  generic sans, because chart text lives in a separate object model
  (`chart.category_axis.tick_labels.font`, not `run.font`) that a naive
  run-only scan skips entirely.

**What this does NOT check:**
- Whether the declared font is installed on the machine running the audit.
  Installation is a property of the rendering environment, not the deck
  file — a deck can legitimately be built for a different machine than the
  one auditing it. Never flag this.
- An individual chart data point's font override
  (`point.data_label.font`) — python-pptx exposes those one point at a time
  and the scan doesn't iterate points. A real but narrow blind spot; series/
  axis/legend/title-level chart fonts (where almost all chart font defects
  actually live) are fully covered.
- Bullet-character glyph fonts (`<a:buFont>` in the raw XML) — a separate
  paragraph-formatting element from text runs. Not walked by this rule,
  which scopes strictly to "every run" per its own definition; if bullet-
  glyph font consistency becomes a recurring complaint, extend the scan,
  don't silently fold it into the run count.

**Mechanical vs judgment:** this entire rule is mechanical. The system-font
flag and the font inventory are ground truth — a font name string is either
in the fixed system-font list or it isn't. The only place judgment enters is
choosing what `--expect` to pass, and that choice belongs to whichever brand
skill is co-loaded, not to `deck-narrative`.

---

## The audit script

`scripts/audit_deck.py` — takes a `.pptx` path, reports what a machine can
mechanically check. Does not touch HTML-based decks — those need a
human/agent read-through of the rendered page instead (whichever visual
skill your setup uses for HTML decks); extend this script with a
Playwright-based title extractor if that becomes a recurring need.

```bash
python3 {agency-root}/skills/deck-narrative/scripts/audit_deck.py path/to/deck.pptx
python3 {agency-root}/skills/deck-narrative/scripts/audit_deck.py path/to/deck.pptx --json
```

Requires `python-pptx` (`pip3 install python-pptx`).

### What it checks mechanically (HIGH confidence — it either measured this or it didn't)

- Slide count.
- Per-slide title font size (pt) and deck-wide range.
- Per-slide title word count and explicit line-break count.
- Per-slide table count vs chart count (`has_table` / `has_chart`), deck-wide
  totals.
- Full title sequence, in order (for the horizontal read-through).
- **Deck-wide font inventory (Rule 9).** Every text run (shapes + table
  cells) plus every reachable chart-text font (title, axis tick labels,
  legend, plot/series data labels) — one font-name entry per run/element,
  with a distinct-family run count. Reported unconditionally, pass or fail.
- **System-font hard flag (Rule 9).** Calibri, Arial, Times New Roman,
  Helvetica, Cambria, Verdana, Tahoma anywhere in the font inventory is a
  hard fail — a fixed-list string match, not a heuristic. Unlike everything
  else in the heuristic section below, this one IS a verdict.
- **Unset/theme-inherited font count (Rule 9).** Runs with no explicit font
  name, counted separately from named fonts.
- **Expected-family check (Rule 9, optional, `--expect "Family A,Family B"`).**
  When supplied by the caller (from whichever brand skill is co-loaded), any
  non-system named font outside the expected set is flagged. Deterministic
  string-set membership once the caller supplies the ground truth — still
  mechanical, just conditional on an argument.

### What it checks as a heuristic (review candidate, not a verdict)

- **Verb test.** Curated Vietnamese + English verb/copula list, plus a
  quantitative-anchor exemption (a data-led headline like "50M VND ads in a
  175M budget" functions as an implicit assertion even with no explicit verb
  — it needs a unit-bearing number: currency, %, or grouped thousands, not a
  bare digit), plus an unresolved-conditional-opener check ("If budget
  changes" with no "then/sẽ/thì" resolution clause fails even though
  "changes"/"thay đổi" is a verb — it's a dangling hypothesis, not a
  complete claim). This is real linguistic signal, not a per-deck hack — see
  the code comments in `audit_deck.py` for the exact rules and why "làm" is
  deliberately excluded from the Vietnamese verb list (too ambiguous,
  produces false positives on nominal compounds).
- **Estimated wrapped-line count.** No rendering engine is available, so this
  is a chars-per-line estimate from shape width and font size — flagged
  `estimated_wrapped_lines` in the output, separate from the exact
  `explicit_line_breaks` count. Treat it as a rough guide; a screenshot is
  the real verifier for line-wrap.
- **Process-meta scan (Rule 8).** Scans every text block on the slide —
  shape text frames and table cells both — for a curated list of English +
  Vietnamese process/production markers ("TBD", "placeholder", "needs
  review", "cần xác nhận", "chưa xác định", etc. — full list in
  `PROCESS_META_MARKERS` in the script). Every hit is reported as a
  `process_meta_candidates` entry with its location and matched text — never
  as a pass/fail verdict. The script has no way to run the addressed-to test
  from Rule 8 (who the line speaks to); a human/agent must read each
  candidate. This is deliberately in the heuristic section, not the
  mechanical one — see Rule 8's worked examples for two cases where a marker
  match is correct as-is and must NOT be flagged as a failure.

### What it does NOT check (judgment — human/agent territory, listed explicitly in the script's own output)

- The "so what" test (implication, not description).
- One-message-per-slide (5-second/10-second tests, the deletion rule).
- Minto sequencing (is slide 2 really the conclusion; do slides 1-3 cover the
  whole recommendation).
- Horizontal logic (do the titles read as a persuasive essay in sequence —
  the script prints the sequence, a human/agent reads it).
- Vertical logic (does the body prove the title).
- Decision-slide framework fit (which of the three approved structures).
- Pre-wire verification, footnote citation completeness.
- Rule 8 TEST 1 verdict — whether a process-meta marker hit is actually
  producer-facing (the script finds the string, not the addressee).
- Rule 8 TEST 2 — see-vs-say. Whether audience-facing content belongs on the
  slide at all, or should be spoken by the presenter instead. Never
  automated; applies even to slides that pass every other check.

### Verified against a real deck (anonymized)

Tested against all three build stages of an anonymized real deck at
`{project}/outputs/strategy/{date}-{deck-name}/` (Vietnamese-language
strategic deck). Reproduces:

- **v1** (`deck-v1.pptx`, 22 slides, 19 tables/0 charts): 4
  titles failing the verb test (slides 8, 19, 20, 21); every headline under
  28pt, range 21-27pt; **1 Rule 8 Test 1 review candidate** — slide 6,
  marker `cần xác nhận` inside a multi-line callout ("Cần xác nhận: đội
  marketing đang kiểm soát các trang hiện có, hoặc phải tạo trang mới.");
  **Rule 9: 622/622 named runs are Calibri, 0 other named fonts, 0 unset.**
- **v2** (`deck-v2.pptx`, 24 slides, 19 tables/2 charts): 1
  title failing the verb test (slide 14, unresolved conditional); **1 Rule 8
  Test 1 review candidate** — same callout, now on slide 7 after a
  slide-count shift; **Rule 9: 608/608 named runs are Calibri (incl. both
  charts' axis/legend text — confirmed reachable), 4 unset.**
- **v3** (`deck-v3.pptx`, 25 slides, 20 tables/3 charts): 1
  title failing the verb test (slide 14); **2 Rule 8 Test 1 review
  candidates, both on slide 7** — `cần xác nhận` (the same confirmation
  callout, decision #2 of the three asks) and `chưa xác định` (a table
  cell, "Audit 07/2026 (chưa xác định)", stating a factual data gap). Both
  are correct as-is under Test 1 — the script reports them as review
  candidates only and does not fail the deck; see Rule 8's worked examples
  above for why neither should be stripped. Note: as of v3, the deck still
  carries the three-slides-for-three-decisions layout (slides 6-8 in v3,
  originally 5-7 in v1) that Rule 8's Test 2 worked example above calls out
  for compression to one slide — this is real, live, uncompressed Test 2
  debt in the current build, not a hypothetical, and Test 2 is not something
  this script can flag; it's listed here so the next revision catches it.
  **Rule 9: 688/688 named runs are Calibri (13 of those from the 3 embedded
  charts' axis/legend text), 6 unset. With `--expect "Be Vietnam Pro,Manrope"`:
  0/2 expected families present anywhere in the deck.** All three versions —
  every build stage — ship with zero non-system-font text.

Re-run the script yourself to reproduce — it's deterministic, no LLM call
involved in the mechanical checks. Rule 8 Test 2 (see-vs-say) and Rule 9's
`--expect` choice are not in default output by design — Test 2 is a judgment
call the script explicitly refuses to automate, and `--expect` is optional
brand input the script doesn't assume.

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The title's close enough, it's basically a claim" | Run the verb test. "Launch Readiness" isn't close to "Launch Is 6 Weeks Behind Schedule" — one names a topic, the other forces a decision. Vague titles are why decks get built by instinct. |
| "We don't have time to restructure for Minto" | Restructuring after the fact costs a full rebuild. Front-loading the conclusion on slide 2 costs one rewrite of one slide, before the rest gets built on top of it. |
| "It's just an internal deck, the numeric thresholds don't matter" | The thresholds are MEDIUM confidence and adjustable — the structural rules (action titles, one message, top-down) are HIGH confidence and don't get a pass just because the audience is internal. |
| "The chart-vs-table pick is a style choice" | It's a cognitive-task choice. A table of 30 trend numbers across 6 quarters forces the reader to do the trend-spotting the chart should have done for them. |
| "I ran the visual deck skill, so the deck's done" | The visual skill controls what it looks like. It has zero opinion on whether slide 8 is a topic label or slide 20 skips the decision framework it's supposed to feed into. Co-load this skill. |
| "The verb-test script flagged it, so it's wrong" | The verb test is a heuristic — a review candidate, not a verdict. Read the flagged title and decide; don't auto-fix based on the script alone. |
| "It says 'cần xác nhận' / 'decision', so it has to come out" | Wrong test. The discriminator is who the line is addressed to, not whether it names a decision. A decision addressed to the deck's actual audience is the deck's purpose — stripping it on a keyword match guts the most important slide in the deck. |
| "I already eyeballed the screenshots, fonts look fine" | They looked fine because the renderer substituted a lookalike — that's exactly how one real deck shipped 688 Calibri runs through an 8-dimension design critique, a manual visual check, and three build cycles undetected. Visual review cannot see this class of defect. Run Rule 9. |

---

## Red Flags — stop and re-check the deck's argument, not its slides

- The recommendation doesn't appear until the last third of the deck.
- More than a couple of slide titles are pure noun phrases with no verb and
  no data anchor.
- Reading only the titles in sequence doesn't produce a coherent argument.
- A slide has a chart/table/callout that doesn't obviously prove its own
  title.
- A "decision slide" has no callout, no active-verb bullets, and doesn't map
  to any of the three approved frameworks.
- Zero charts across an entire deck that's full of trend or comparison data
  in tables — worth a Rule 6 pass with whichever chart-picking skill/tool
  your setup provides.
- A slide reads like it's talking to an internal reviewer instead of the
  deck's actual audience — "TBD", "confirm with", "needs review", or similar
  producer-facing language survived into the `.pptx` (Rule 8). Move it to
  the `.html` plan; do not strip audience-facing decision asks by mistake.
- A deck was approved on a rendered/screenshot review but `audit_deck.py`
  was never run against the actual `.pptx` file (Rule 9) — visual review and
  file audit catch different defect classes; neither substitutes for the
  other.

## See also

- Chart rendering — hand off Rule 6's table-vs-chart decision to whichever
  charting skill/tool your setup provides for a native, editable chart.
- `html-plan-style` — destination for stripped process-meta content (Rule 8):
  "decision needed", reviewer comments, TBD/placeholder notes all live in the
  `.html` plan this skill produces, never in the shipped `.pptx`.
- Your project's brand/visual skill — owns which fonts are correct for your
  decks and the "never use system fonts" convention Rule 9 mechanically
  enforces at the file level; pass its font names to `audit_deck.py --expect`.
- Pick whichever visual deck skill fits your build — `strategic-deck`,
  `marp`, `gws-slides`, or another visual/deck skill your setup provides —
  `deck-narrative` is silent on that choice.
- `quality-loop-router` — every deck deliverable still ends here
  (`task_type: deck`) after the narrative and visual passes are both done.
