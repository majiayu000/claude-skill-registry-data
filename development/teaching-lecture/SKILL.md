---
name: teaching-lecture
description: Author a Quarto reveal.js lecture deck for a class meeting. TRIGGER on "build a lecture", "slides for my class", "teaching deck", "lecture on X", "course slides", "make a lecture for week 3", "add a discussion slide". Conference and seminar decks are research-talk, the site around the decks is course-site, auditing an existing deck is slide-review.
---

# Teaching lecture decks

Builds a `.qmd` that renders to a reveal.js HTML deck for a class meeting, and
organizes a semester of them into one published course site.
Students are seeing the ideas for the first time, they are taking notes, they
will reread the deck a week later, and their attention resets every fifteen
minutes. That drives every choice here: bigger type, staged reveals, a visible
roadmap, a worked example after every formal idea, and questions they have to
answer out loud.

Out of scope: research presentations (use `research-talk`, which shares this
toolchain and theme family but stays quiet and dense), auditing a deck you did
not write (use `slide-review`), and LaTeX Beamer (use `compile-latex`). The
`course-site` skill owns everything around the decks: the landing page, the week
table, the site theme, publishing.

Shared theme and tooling live in `~/.claude/assets/quarto-yale/`.
`README.md` there is the machinery reference: the recipe, the class list, what
the filter rewrites, what the gates assert, and the settings that silently break
a deck. Read it for any of that; where it and the source disagree, the source
wins. The head of `starter-theme.scss` carries the palette and the theme's own
reasoning about a class. This skill does not restate what `research-talk`
already covers (`output-location` for code chunks, how `pdfread.py` works);
read that skill where the two overlap. The pointer map at the end of this file
says which reference file holds what.

## The theme carries a measured palette

The shipped theme is `starter-theme.scss`, a light editorial look (paper
ground, Literata display headings over IBM Plex Sans text, plum accent) with a
named block for each thing
a slide can ask of a student. The look is yours to replace; the discipline to
keep is that the theme documents its own palette as a measured contrast table,
each ink with its WCAG 2.1 ratio against the ground, checked with a checker
and written into the head of the scss. The starter theme's table:

| Role | Hex | Notes |
|---|---|---|
| Ground | `#faf7f2` | Every slide, including dividers. Nothing changes it. |
| Body text | `#33302b` | 12.3:1 on the ground. |
| Muted | `#6b6157` | 5.7:1. `.dim`, footer, slide number, captions, dates. |
| Quiet emphasis | `#4f463c` | 8.6:1. `.ygray`, `h3`, blockquotes, appendix headings. |
| Accent | `#7d3a5e` | 7.5:1. Links, list markers, block labels, progress fill. |
| Dark accent | `#54263f` | 11.4:1. `.yblue`, inline code, `.takeaway`. |
| Good | `#38684a` | 6.0:1. `.ygreen`. |
| Warning | `#7d5b12` | 5.8:1. `.yamber`, the `.warning` label. |
| Bad | `#9c3b26` | 6.4:1. `.yred`. |
| Pale accent | `#d9bccb` | 1.6:1. Hover underlines and other decoration. Never text. |
| Hairline | `#ddd6c9` | 1.4:1. Rules and block frames. Never text. |
| Panel tint | `#f2ede3` | Block grounds, one step off the paper; every text ink above also holds 4.5:1 here. |

Any hex copied out of an older deck gets checked against the table before it
ships; the two decoration rows exist so the check is mechanical. Your own
theme's rationale goes in `style/house.md`.

If you build a dark theme for a lecture hall, design it; an inverted light
theme is how a deck ends up with ink that measures near 1:1. The method: a
near-black ground, body text just off pure white (running text at pure white
halates on a projector; headings can take it), every accent re-picked and
re-measured against the dark ground, since a saturated brand colour that reads
as authority on white can land under 2:1 on near-black, which is invisible.
Reserve the 3:1 to 4:1 band for large solid marks and rules, never text, and
say so in the table. Pair the theme with a dark `highlight-style` (`a11y-dark`)
so code does not arrive on a white card, and rebuild figures on the deck ground
(`references/figures-dark.md` has the recipe), because a white-panel figure is
a lightbox on a dark wall.

## Before drafting anything

Ask, do not guess.

1. Which course, which week, and how long the class is. 50 and 75 minutes are
   different decks, not the same deck at a different pace.
2. What last week ended on. Every lecture opens by closing that loop, and the
   agenda slide needs it.
3. Who is in the room, and what they can be assumed to know. A business-school
   AI class can draw MBAs, undergrads, and CS or econ PhD students in one section. A
   business student reads a figure faster than an equation and a CS student the
   reverse, so ask the mix, then give both with the picture first. Naming the
   prerequisite is what decides whether a formal definition can appear at all.
4. What already exists: the paper the lecture is built on, prior years' slides,
   the R that makes the figures.

Then write the slide titles and read them back as a list before any bodies
exist. A lecture title may be a topic label where a research title may not
("What a loss function is" is fine), but each block of three or four slides
under it carries one claim, and the claims in order are the lecture.

## The verified front matter

The format is a Quarto extension, `starter-revealjs`. Adopt it once per deck
directory (or once at the project root):

```bash
cd <deck dir>
quarto add ~/.claude/assets/quarto-yale --no-prompt   # installs _extensions/starter/
cp -R ~/.claude/assets/quarto-yale/{mathjax,fonts} .  # the format self-hosts MathJax and both faces at relative urls
```

A standalone deck then needs only:

```yaml
title: "Prediction is not a decision"
author: "Your Name"       # exact form; see style/house.md
date: 2026-09-16
format: starter-revealjs
engine: knitr             # only if the deck has R chunks; R is the default here for figures
bibliography: lecture-refs.bib   # only on a deck that cites
```

The format carries, so the deck must not repeat: the theme layered on `default`
(eight of the twelve built-ins `@import` Google Fonts at display time),
`stage-slide.lua` in `filters:`, `citeproc: false` (harmless on a deck that does
not cite), `refs-fit: starter` (the packing preset measured for the starter
theme), `highlight-style: a11y`,
`slide-number: c/t`, `incremental: true`, `date-format: long`,
`fig-align: center`, `auto-animate-duration: 0.4`, `echo/warning/message:
false`, and self-hosted MathJax (`method: mathjax, url: mathjax/MathJax.js`)
pinned to MathJax's own TeX webfonts so the metrics match on every machine and
the fit gate's certification transfers. The comments in `_extension.yml` say why
per key. A deck off the extension writes all of that out by hand; that manual
recipe is in the README under "The recipe".

In a course project the per-course choices live once in `lectures/_metadata.yml`
and cover the whole semester. The verified working copy, from the example
course this repo's `examples/` lecture comes from:

```yaml
format:
  starter-revealjs:
    # These lectures render to docs/lectures/<name>.html and the site's MathJax
    # copy is at docs/assets/mathjax/ (a `resources` entry in _quarto.yml keeps
    # it there across renders), so the url is the path from the rendered page
    # to that copy.
    html-math-method:
      method: mathjax
      url: ../assets/mathjax/MathJax.js
engine: knitr
```

`bibliography:` stays out of it, in the one lecture that cites.

`stage-slide.lua` opens each content slide as its title alone and then reveals
its blocks in turn, which `incremental: true` does for list items only; its six
jobs are in the README under "What stage-slide.lua does", and its header comment
is the reference before changing how a slide stages. A deck with dividers needs
it or the divider numerals come out empty.

MathJax handles `\eqref`, `\label`, `\DeclareMathOperator`, `mathtools`, and
`physics`, none of which KaTeX can do. Do not switch to `mathml` or `plain`; a
room with no network takes the offline variant, which gives up `\eqref` and
friends (README, "The offline variant"). The `highlight-style` is the theme's
companion: `a11y` on the light starter theme, `a11y-dark` on a dark theme
(a light style there paints a white code card), and a misspelled style name
fails silently at exit 0.

The progress bar is on by default and the format sets `slide-number: c/t`.
Students pace themselves off the bar. Both the bar and the number take the
appendix and the references out of the
denominator, so the bar reads 100% on the `.closing-slide` and the class body
counts 1/25 to 25/25 with the tail on its own 1/8 run; the filter also writes
per-section cut positions a theme can draw as segments (the starter theme keeps
one plain fill). Measured details:
`references/staging.md`; bar mechanics: README "The progress bar".

Leave `chalkboard` off: with `embed-resources: true` it is a hard render error,
and annotation happens on the room's own boards. Misspelled YAML keys are
ignored silently at exit 0; `quarto inspect deck.qmd` prints the resolved
format.

## Math macros

Park them on a hidden slide at the top of the file:

```markdown
## Notation {visibility="hidden"}

\newcommand{\E}{\mathbb{E}}
\DeclareMathOperator*{\argmin}{arg\,min}
```

A bare macro block before the first `##` becomes its own completely blank
slide, counted in `c/t` and printed into the handout; `visibility="hidden"`
drops the slide from navigation, the count, and the PDF, and the macros still
resolve everywhere after it. Macros expand at parse time, before any renderer
sees the math, so the same block works under MathJax and under the offline
KaTeX variant; wrapping the definitions in `$$ ... $$` fails.

Number a result you will refer back to, which a lecture does more than a talk
does: `$$ ... $$ {#eq-bayes}`, then `@eq-bayes` in prose. Quarto's `@eq-` form
is the portable one; raw `\label` plus `\eqref` also works under MathJax and
breaks under the offline variant.

Math inside a raw HTML block works, because pandoc's `markdown_in_html_blocks`
is on by default, so `$a^\star = \argmin_a \E[L(a,y)\mid s]$` typesets
correctly inside a raw `<ol class="steps">` item.

## The teaching vocabulary

| Class | One line |
|---|---|
| `.keyidea` | The one thing to remember. At most three per deck. |
| `.definition` | New vocabulary. |
| `.example` | The concrete case. |
| `.warning` | The common error. |
| `.question` | A check the student answers; the answer goes on the next slide as a `.fragment`. |
| `.prompt` | Large centered discussion question, sized to fill a slide while students talk. |
| `.hero` | One number that should land hard. |
| `.full-bleed` | On a heading whose slide is one image, edge to edge, height-capped under the heading. |
| `.demo-tag` | Live-coding marker: `## Live demo [demo]{.demo-tag}`. |
| `.aside-note` | Muted caveat; arrives on the previous block's beat. |
| `.num` | Right-align a numeric table column. |
| `.jump`, `[]{.jump-back}` | The appendix jump buttons below. |
| `ul.agenda` | Roadmap list: `.done` muted, `.now` in the accent and bold, the rest plain. |
| `ol.steps` | Worked-example steps, four or five to a list; the theme spaces them, and can draw numbered discs. |
| `#thm-` family | Numbered theorem environments: `references/theorems.md`. |
| `.yblue` `.ypale` `.ygray` `.ygreen` `.yamber` `.yred` `.dim` | Colour spans, hex per the palette table. |

`ul.agenda` and `ol.steps` work both as raw HTML lists and as fenced divs
(`::: {.agenda}` / `::: {.steps}` around the list); the theme styles both
forms. The five teaching boxes each take a `[Label]{.label}` span, and the
label text is yours:

```markdown
::: {.keyidea}
[Key idea]{.label}
A predictor is only useful once you say what decision it feeds.
:::
```

The starter template exercises all five boxes, the agenda, the steps, `.hero`,
and `.prompt`. Keep the class-to-meaning mapping fixed for the whole semester
(`references/pedagogy.md` says why). Two blocks per slide is the limit, and it
is physical as well as pedagogical: at a lecture-hall root, three blocks of two
lines each fill nearly the whole canvas (94% when measured at a 34px root).

## Dividers, appendix, references, jump buttons

Two divider archetypes, the same architecture in a talk deck and a lecture deck
so the two read as one family. On the starter theme each is a display numeral
over a short standing rule over the centred title:

```markdown
## How much a leaderboard can move {.section-break}

## Appendix {.appendix-break background-color="var(--appendix-ground)"}
```

`.section-break` is the numbered divider. The number comes from
`stage-slide.lua`, so nothing is hand-numbered and the dividers renumber on the
next render. A divider carries its title and nothing else, no background
attribute; `.appendix-break` is the one divider that may change the ground, and
its attribute is copied exactly as written above. The starter theme keeps both
divider grounds on the page ground, so the attribute changes nothing there until
a theme pulls the values apart; the hex lives in the theme either way. The
fallbacks, the print-view
behaviour, and why a CSS counter is wrong here are in the README under "Things
that will silently break the deck"; divider title diction is in
`style/house.md`.

Slides after the appendix divider take `{.appendix}`: muted headings and marks,
a standing APPENDIX label above every heading, and the ground, the body text, and
the five teaching boxes unchanged. The scheme's reasons are
in `style/house.md`.

A lecture cites less than a seminar talk, and when it does the citation is a
pointer for the student taking notes rather than part of the argument. Cite
with `[@key]` or `@key`; the parentheses come from the citation style, never
from CSS. The reference list goes at the very end, after the appendix, and
paginates itself:

```markdown
## References {.references-break background-color="var(--references-ground)"}

## References {.references}

::: {#refs}
:::
```

The format's `citeproc: false` is what lets `stage-slide.lua` run citeproc
itself and cut the list across slides, and `refs-fit: starter` is the budget
measured for the starter theme: 25.9 rendered lines at 134 characters per
line, packed greedily, which is how the sample lecture packs 10 entries and
then 2. A restyled theme re-derives its budget and overrides it with
`refs-lines` and `refs-chars-per-line`.
`STAGE_REFS_DEBUG=1 quarto render deck.qmd` prints what the packer decided and
`refs-lines` overrides it. Never put `.scrollable` on a references slide. The
cite-form table, the hover and tooltip machinery, and the packing model are in
the README under "Citations and the reference list".

Jump buttons: a question in week three is usually a question the appendix
already answers. Give the appendix slide an id, name it from the lecture slide,
and put a Back button on every appendix slide you might land on:

```markdown
## Where the interval comes from {.appendix #ap-se}
```

```markdown
::: {.with-previous}
[Derivation]{.jump target="ap-se"}
:::
```

and on the appendix slide `[]{.jump-back}` in the same `.with-previous`
wrapper, which renders as Back and returns to the exact slide and fragment step
you left. A button goes on its own line, after a bordered or indented block and
never inside one, and a forward label names the destination in one to three
words. Run the fit gate after adding one; the button owns a line the slide did
not own before. Alignment, the silent target breakers, and the handler: README
"Jump buttons"; the lecture's measured numbers: `references/staging.md`; label
diction: `style/house.md`.

## Staging, in one paragraph

The invariant is that the title appears alone: every content slide opens as its
heading and reveals its blocks one beat at a time, a figure as much as a list.
`incremental: true` is the default to start from; opt lists out with
`::: {.nonincremental}`, group blocks into one beat with `::: {.together}`, put
an addendum on the previous beat with `::: {.with-previous}`, and opt a slide
out with `{.no-stage}`. Budget five to eight staged moments in a 75-minute deck
beyond the incremental lists. Fragment variants, `.r-stack` layers,
`fragment-index`, and `auto-animate` are in `references/staging.md`; the
filter's internals are in the README under "Staging: the title appears alone,
always".

## Pacing and structure

Every lecture opens with the same two slides. One slide of recap that ends on
the question this lecture answers, then the agenda as a `ul.agenda` with
`li.done` on last week and `li.now` on today's first block. Repeat that agenda
slide verbatim at each block boundary, moving `.now` down one, and close the
lecture with every item `.done`. Students use it to locate themselves and it
costs three slides.

A lecture does not end on a thank-you slide. The last two slides of the class
are the synthesis pair: the agenda with every item `.done`, then the
`.closing-slide`, which stages as heading, then one beat
(`references/closing-slide.md`). After that comes the appendix divider, which
the class only sees if a question sends you there.

Segment budget for 75 minutes:

| Minutes | What | Slides |
|---|---|---|
| 0-5 | Recap, agenda, the question | 3 |
| 5-25 | Block 1: motivation, the formal idea, a worked example | 8-10 |
| 25-30 | Discussion prompt or a check for understanding | 1-2 |
| 30-50 | Block 2: the complication and how it is handled | 8-10 |
| 50-55 | Second prompt, or a live demo | 1-2 |
| 55-70 | Block 3: application, or a paper read together | 6-8 |
| 70-75 | Synthesis: the agenda all `.done`, plus what is next | 2 |

A 50-minute class is the same shape with Block 3 dropped and one prompt instead
of two, about 22 content slides. Roughly 1.5 to 2 minutes per content slide,
half the density of a research talk. Sixty slides for 75 minutes is a reading,
not a lecture. Where the prompts go and how to run them:
`references/pedagogy.md`.

## Build and verify

The render exits 0 whether or not the deck is presentable, so the gates are not
optional. Run them every time.

```bash
cd <deck dir>
quarto render lecture.qmd --to starter-revealjs 2>&1 | tee /tmp/render.log
grep '\[WARNING\]' /tmp/render.log     # unclosed divs and missing images warn here, still exit 0

node ~/.claude/assets/quarto-yale/deck-check.mjs fit lecture.html   # must print DECK-FITS: YES
node ~/.claude/assets/quarto-yale/stage-check.mjs lecture.html      # must print STEP-0-CLEAN: YES

# only if this deck was built as the offline variant
~/.claude/assets/quarto-yale/check-offline.py lecture.html           # must print OFFLINE-SAFE: YES
```

`deck-check.mjs fit` drives headless Chrome, visits every slide, forces its
fragments visible, and measures; it fails on overflow, excess width, missing
images, crushed or shrunk figures, unrendered math, a dangling `.jump` target,
and an unpaginated bibliography, and `--json` adds per-image geometry. A
single-pass DOM scan cannot do this, because reveal sets `display: none` on
every slide that is not current. `stage-check.mjs` puts every slide in its
unadvanced state and asserts nothing but the heading is visible, then walks
each content slide forward and fails a press that changes no visible ink
(`DEAD STEP`, presses counted from 1), at a cost of about two seconds a deck. It
skips slides by class (the dividers, the reference pages, the closing slide
under either archetype name); `{.no-stage}` is not on that list. It is the
filter's opt-out and the gate has never read it, so an unstaged slide still has
to be classified as something other than content. Both gates are in the README
in full. The sample lecture measures zero dead steps.

`check-offline.py` runs only on a deck built as the offline variant. On a
default MathJax deck it reports the external MathJax reference and fails, which
is correct and is not a defect (README, "The offline variant").

Overflow matters more here than in a research deck. At a lecture-hall root, a
heading plus roughly ten single-line bullets fills the canvas (measured at a
34px root: ten fit exactly, twelve overshoot by 161 px, and lines eleven and
twelve are simply gone on the projector while the laptop preview looks fine),
so eight is the working limit. Fixes, in
order: split the slide (almost always right, since a slide that does not fit is
doing two jobs), move the delivery lines into `::: {.notes}` while the substance
stays in the body where the handout keeps it, or add `{.smaller}` to the
heading, kept for a table or a code block because shrinking type defeats a
lecture-sized root. `panel-tabset` is not a fix (only its first tab prints) and
`.scrollable` slides always fail the gate; split instead.

To look at slides rather than measure them, use decktape and `pdfread.py` per
the README ("Looking at a rendered deck"). The Read tool cannot open a PDF on
this machine.

## Course site and handout

The `course-site` skill owns the site in full; read it before touching
`_quarto.yml`, `index.qmd`, or anything else outside `lectures/`. A semester of
lectures lives in one Quarto website project per course
(the example lecture in this repo's `examples/` directory comes from one), each deck a
`lectures/wNN-slug.qmd` holding content only, with the shared config once in
`lectures/_metadata.yml` as shown above. While drafting, render one lecture:
`quarto render lectures/w03-slug.qmd`.

The site's week table links a `pdf` next to every deck, and the handout has to
be built by the render itself: a render prunes everything in `docs/` that it did
not produce, which deletes any PDF put there by hand. Build it in a
`post-render` hook, which runs after the prune; the script walks the decks
Quarto just rendered (`QUARTO_PROJECT_OUTPUT_FILES`, so rendering one lecture
rebuilds only that handout) and calls the exporter on each:

```bash
node ~/.claude/assets/quarto-yale/deck-check.mjs handout \
  docs/lectures/w03-slug.html docs/lectures/w03-slug.pdf
```

A workable `scripts/build-handouts.sh` skips with a warning when node or the exporter is missing, exits nonzero when
an export actually fails, and needs no change when a lecture is added. With
`pdf-separate-fragments` at its false default the print view collapses each
slide's build steps onto one fully revealed page (27 slides came out 27 pages),
which is the student handout;
set it true for a page per build step, a lecturer's cue printout that runs long
under `incremental: true`. decktape is the fallback exporter, speaker notes
appear in neither PDF, and `panel-tabset` prints only its first tab (README,
"PDF handouts").

## Starter template

`assets/starter-template.qmd` is the starter deck: recap and agenda, the five
boxes, a worked example with a jump to its appendix derivation, an
`auto-animate` pair, a `.prompt`, the synthesis pair, and the closing slide. It
renders standalone, and passes both gates, with `_extensions/starter/`
installed beside it; it needs no `_metadata.yml`. Math at display time additionally
needs a `mathjax/` copy beside the rendered HTML.

## Traps, all verified on this machine

| Symptom | Cause | Fix |
|---|---|---|
| Content clipped on the projector, clean on the laptop | reveal scales a fixed 1050x700 canvas and render exits 0 | `deck-check.mjs fit`, then split the slide |
| Figure axis labels unreadable, gate says the slide is ok | `auto-stretch` shrank the figure instead of overflowing | read `--json` per-image `w`, move the text into a column |
| A blank slide in the count and the handout | macro block before the first `##` | `## Notation {visibility="hidden"}` |
| `\argmin` errors as an unexpected control sequence | macros wrapped in `$$ ... $$` | bare raw LaTeX under the hidden slide |
| Section divider carries a stray coloured panel | a `background-color` attribute copied from another deck or theme | drop the attribute; `{.section-break}` alone is the contract |
| Divider numeral is missing | `stage-slide.lua` not running: a deck off the extension with no `filters:` line | use the extension format, or add the filter by absolute path |
| A figure or a note appears with the heading instead of waiting | the filter is not running, or the heading carries `{.no-stage}` | `stage-check.mjs` names the slide |
| Math unrendered even with wifi | the format's self-hosted `mathjax/MathJax.js` url resolves to nothing next to the rendered HTML | copy `~/.claude/assets/quarto-yale/mathjax/` beside the deck, or override the url as the course project does |
| Type looks wider than the fit gate measured | no `fonts/` copy next to the deck, so both faces fell back to the system stacks | copy `~/.claude/assets/quarto-yale/fonts/` beside the deck, or override the four @font-face urls |
| Appendix divider loses its tinted ground in the handout | reveal's print view builds no background elements at all | nothing to fix; the rule and the lone title carry it |
| Progress bar is one unbroken line | fewer than two `.section-break` dividers, or the filter is missing | nothing to fix if the deck has one section; otherwise add the filter |
| Progress bar is not full on the closing slide | the appendix has no `.appendix-break` divider and no `.appendix` slides, so nothing marks where the class ends | add the divider before the first appendix slide |
| A jump button navigates but Back does nothing | the deck has `.jump` spans and a stale render, or the filter was dropped | re-render; the filter emits the handler alongside the buttons |
| A jump button lands on the title slide | the target id is all digits, or the target slide is `{visibility="hidden"}` | rename the id; reveal reads an all-digits id as a slide index |
| Dividers numbered 1, 2, 2, 2 | a CSS counter, which `display: none` slides do not increment | the attribute plus `content: attr(...)`, which the theme already does |
| A paragraph on a divider slide lands under the title | the divider centres a full-height flex `h2` | put the sentence on the next slide |
| `pdf` link on the course site 404s after a render | a render prunes `docs/` of anything it did not build | build the handout in a `post-render` hook |
| Some text or a figure line is invisible on the wall | ink from another palette, measuring near 1:1 against the deck ground | check the hex against the theme's contrast table and swap in one of its inks |
| Code block renders with no highlighting at all | misspelled `highlight-style` (`solarized-dark` and `printing-dark` do not exist) | the format's `a11y`, or `a11y-dark` on a dark theme |
| Figure panel clashes with the deck ground | ggplot default theme | the ground-matched `deck_theme()` in `references/figures-dark.md` |
| Title slide is top-aligned instead of centred | a `top: 0 !important` rule was added to the theme | remove it; it also disables `{.center}` |
| Figure inside a column or an `.r-stack` renders tiny or overflows | `auto-stretch` only ever sizes a direct child of the section, and `.r-stretch` by hand only removes the size cap | set `fig-width`/`fig-height`, or `width=` on a file image |
| Handout is missing most of a slide's content | `panel-tabset` prints its first tab only | separate slides |
| Math gone in a room with no network | MathJax loads at display time (self-hosted or CDN) | build the offline variant, or ship the `mathjax/` copy with the deck |
| Offline variant loses its math anyway | the `{method:, url:}` object form left a runtime loader | bare `html-math-method: katex` plus `self-contained-math: true` |
| `\eqref` prints as literal text | the deck was built as the offline KaTeX variant | Quarto `@eq-` cross-references |
| Render fails, `RevealChalkboard is not compatible` | `chalkboard` with `embed-resources` | leave chalkboard off |
| Video slide shows "No compatible source was found" | `{{< video >}}` writes a `<source>` with no `type` | raw `<video src="...">` |
| plotly figure 403s in class | plotly.py 6.x emits a module import of cdn.plot.ly | add `plotly-connected: false` to the front matter |
| Choropleth blank with no network | plotly fetches topojson at display time | use a static image of the map |
| Regression table columns read `1.` and `2.` | pandoc parses `(1)` as an ordered-list marker | rename the columns |
| Blank image on a slide, render exited 0 | missing file, only a buried `[WARNING] Could not fetch resource` | the gate reports `MISSING IMG` |
| A YAML key silently does nothing | Quarto ignores unknown reveal keys | `quarto inspect deck.qmd` |
| Every asset 404s on GitHub Pages | Jekyll dropped the `_files` directories | `touch docs/.nojekyll` and commit it |
| Handout collapses every build step onto one page | `pdf-separate-fragments` defaults to false and decktape ignores it | that collapsed export is the student handout; for a page per build step set `pdf-separate-fragments: true` and use `deck-check.mjs handout` |
| A second, unpaginated bibliography on the last slide | `bibliography:` on a deck without `citeproc: false` (the extension format carries it) | use the extension, or add the line; the fit gate fails the deck for it |
| Reference list runs off the bottom | `refs-fit` missing or wrong for the theme | `STAGE_REFS_DEBUG=1 quarto render` prints the packer's decision; `refs-lines` overrides it |
| Citation renders as a literal `@key` | `citeproc: false` with the filter absent from `filters:` | put the filter back |

## Where the detail lives

| File | What it holds |
|---|---|
| `references/pedagogy.md` | The density doctrine, prompts and checks for understanding (Mazur), speaker notes, the semantic vocabulary rule, the pattern audit table. |
| `references/theorems.md` | The numbered theorem family, `#thm-` crossrefs, the `#def-`/`#exm-` guard, proof-in-appendix with jump buttons, the harmless citeproc warning. |
| `references/figures-dark.md` | Figure geometry for a lecture deck, the ground-matched `deck_theme()`, captioned figures, the silent-shrink trap, plotly, video, `.full-bleed`. |
| `references/closing-slide.md` | The closing slide: markup, heading-then-one-beat with `.together`, the rationale, how the gate classifies it. |
| `references/staging.md` | Fragment variants, `.r-stack`, `fragment-index`, `auto-animate`, the animation budget, progress bar and slide number details, jump-button measurements, layout numbers. |
| `style/house.md` | Your values, separated from the mechanisms: palette rationale, density calibration, the author line, dates, button diction, closing wording. A stub in the public repo; fill it in. |
| `assets/starter-template.qmd` | The starter deck, rendering clean under `starter-revealjs`. |
| `~/.claude/assets/quarto-yale/README.md` | The machinery: the filter's six jobs, staging internals, both gates, citations and refs packing, jump buttons, the progress bar, the silent breakers, handouts, fonts. |
