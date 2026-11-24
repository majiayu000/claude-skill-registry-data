---
name: "typst-paper-pipeline"
description: "Build Typst papers with fletcher, lilaq, codly and cetz when the package registry is blocked, and check every page visually for layout, typography and diagram problems."
---

# Typst paper pipeline

## Build

- Install the compiler as a Python package: `pip install typst` (0.15 worked).
- If `packages.typst.org` is unreachable, use `typst_vendor.py`: it sparse-checks out
  `github.com/typst/packages`, follows each package entrypoint's local imports (not docs or
  examples), loops `while todo - done`, skips git when already vendored, and compiles with a local
  package path. Usage: `uv run tools/typst_vendor.py doc.typ [--png] [--all]`. Cache: `~/.cache/typst-vendored`.
- Pin versions that exist in the registry (fletcher 0.5.8, not the 0.5.9 dev version; lilaq 0.6.0;
  codly 1.3.0; cetz 0.4.2). WebAssembly plugins (lilaq's komet and suiji, diagraph) work through
  the Python package.
- For web pages about Typst (typst.app, Universe), WebFetch may be refused; Firecrawl works.

## Editions

- Every paper should build three editions from one source, as Erase does:
  - print (US letter);
  - phone, a narrow page readable at a phone's size (`sys.inputs.edition == "phone"`);
  - HTML, where drawings become inline SVG through `html.frame`.
- CI builds Erase, Cannonballs, Peggle and Tenzi with `--all`. It compares the print and phone PDFs with the committed PDFs. The HTML is a build output.
- For a new paper, start with the edition switch and width handling in the closest existing paper.

Read the densest table in the rendered phone PDF at page width. Check the actual text size after scaling. If a table falls below the 9 pt used for shared tables, split it into narrow groups with repeated headers or move detail to an appendix.

## Text shared with the README

Erase, Cannonballs, Peggle and Tenzi each share their results table, rules, checks and open questions with their README.
- Write each shared part once, as Markdown in `<game>/docs/<name>.md`. Numbers are
  placeholders into the results file the game's scripts write, `<game>/results.json`:
  `{{deals.stuck}}` (commas added), `{{x.share:.4f}}`, `{{lists.found:and}}`; the formats are
  listed in `tools/sync_docs.py`.
- The README holds each part between `<!-- shared:<name> -->` and `<!-- /shared -->`;
  `uv run tools/sync_docs.py` fills them, and a test fails when a README is out of date.
- The paper reads the filled section out of the README, so formatting happens once:
  `#import "/tools/shared_docs.typ": shared, fmt`, `#let readme = read("README.md")`,
  `#shared(readme, "open")`. It renders with cmarker 0.1.10 (MIT); Markdown tables come out in
  the house style, and `shared(..., columns: (1fr, 1.2fr, 1.2fr))` sets the widths.
- Paper-only words go in `<!--raw-typst ...-->` comments, which GitHub hides: cross-references
  such as `Proved<!--raw-typst  (@thm-big)-->`. Keep links absolute and images out of fragments.
- `typst_vendor.py` compiles with the repository as root, so `/tools/...` and `../README.md`
  resolve; plain `typst compile` needs `--root .`.
- Numbers the paper writes in its own prose come from `json("results.json")` with `fmt`, not
  typed by hand. A whole-number placeholder and `fmt` print the same digits.
- What cmarker does not do well: inline math needs a converter (mitex 0.2.7 works, but splits
  `10^{18}` into `1 0^18` in the HTML edition), so fragments use Unicode (`n²`, `−`, `×`,
  `10<sup>18</sup>`); Markdown column alignment is lost; a long table must be allowed to break
  on the phone edition (`show figure: set block(breakable: phone)`, `placement: none`), and the
  phone rule that scales wide tables skips tables whose columns are all `1fr`.
- When moving text out of a README, check that no number was lost:
  `uv run tools/numbers_kept.py <game> origin/main --paper <doc>.html` after building `--all`.

## House style that worked

- New Computer Modern 12 pt, US letter, margins 1.55 in by 1.1 in, justified paragraphs. That
  gives about 72 characters per line; 11 pt with 1.3 in margins gave 86, too long to read
  comfortably. Measure it: `pdftotext -layout`, median length of lines longer than 55 characters.
- Set math in NCM Math Regular to match the text weight:
  `#show math.equation: set text(font: "New Computer Modern Math", weight: 400)`. Typst's default
  is the Book weight, visibly heavier than NCM text. Check with `pdffonts`.
- To compare fonts, build the whole document in each candidate and compare one page side by side
  at 75 dpi, plus the page count and measure. Libertinus 12 pt needed 1.8 in margins to match.
- Okabe–Ito colors (colorblind-safe): blue #0072B2, green #009E73, red #D55E00, orange #E69F00.
- Theorem-like environments as `figure(kind: "thm")` with one shared counter and bold labels.
  Statements upright when young readers are in the audience (long italic passages tire them); proofs end with a filled ∎ pushed right (`#h(1fr)$qed$`).
- Tables: no vertical rules, three horizontal rules, header on top, caption above. One quantity
  per column (do not mix "cleared" and "all but 1 in N" in one column). Keep the last column short
  and move long remarks into the caption; give the widest text column `1fr`, not `auto`, or the
  others get squeezed into one-word lines. Bold the row the reader should find first.
- Use one notation for the same object across tables (spaced digits `0 0 0 0 6 7 7`, not digit
  strings in one table and spaced digits in another).
- codly for listings: no zebra stripes, light border, muted line numbers.
- `#show math.equation.where(block: false): box` so inline formulas never break across lines.
- Captions: centered when they fit on one line, otherwise a justified paragraph
  (`layout(size => if measure(it).width <= size.width {...} else {...})`).
- Side boxes: one quiet style (light tint, colored left rule, small uppercase label); at most two
  labels ("Idea", "Try it").

## fletcher techniques worth reusing

The local gallery is at `~/.cache/typst-vendored/preview/fletcher/0.5.8/docs/gallery/`.
- `node(enclose: (<a>, <b>, ...))` with a dashed stroke and light fill to group a subtree.
- Edge labels on the line (`label-side: center`) to show values flowing up an expression tree.
- Colored edges by meaning (proof map: green by hand, purple case-checked, grey for the
  wastebasket), with the meaning in the caption. Do not reuse a color that already marks a drawn
  object or a kind of box.
- Scale diagrams to the text width in every edition, not only on narrow pages:
  `layout(size => if measure(x).width > size.width { scale(size.width / w * 100%, reflow: true, x) } else { x })`.
  A wide diagram otherwise overflows both margins by the same amount and is easy to miss.
- Callout notes as `node(..., stroke: none)` next to the group, with a curved arrow
  (`bend: -25deg`) when there is room. Anchor arrows on real nodes or on columns that have width:
  fractional coordinates between empty columns collapse to a lone arrowhead.
- Orthogonal tree edges (`(from, "|-", mid), (mid, "-|", to)`) for org-chart-style trees.
- Keep layouts free of long detour edges. If one node needs edges from everywhere, consider
  taking it out of the diagram and naming its dependencies in the caption.

## Layout

- Figures stay with their words by default (no `placement`). Use `placement: auto` or
  `place(auto, float: true)` only when an unbreakable block would otherwise leave a big hole.
- Put a lead-in sentence and its display in one `block(breakable: false, width: 100%)`.
- A short explanatory box and its picture can sit side by side in a `grid`.
- Label appendices as appendices: `#set heading(numbering: (..n) => "Appendix " + numbering("A.", ..n.pos()))`
  after `#counter(heading).update(0)`, plus a `show ref` rule that renders references to those
  headings as "Appendix A" (a numbering function otherwise leaks "Appendix A." into references).
- Decide the break before appendices by looking: `#pagebreak(weak: true)` is right when the first
  appendix table would otherwise leave a large hole, wrong when it leaves a page with two lines.
  Re-check after every change in length or font size.
- A figure introduced by a sentence ending in a colon cannot float. If it leaves a big hole,
  rewrite the sentence as a reference ("@fig-x counts ...") and give the figure `placement: auto`.
- Small appendix tables can drop to 10 pt (`show figure.where(kind: table): set text(size: 10pt)`
  after the appendix marker) to keep them on the page they belong to.
- Numbers with thousands separators inside math need quotes: `$"66,045"$`.
- Do not draw meaning with bare glyphs (a "|" between card groups looked misplaced and was
  unclear). Label things in words instead (HAND / CENTER).
- Margin notes: a `place` written before a paragraph is its own flow item, so when the paragraph
  moves to the next page the note stays behind. Anchor the note inside the paragraph instead:
  `box(place(top + left, dx: <text width + gap>, dy: -5.5pt, note))` as the first thing on the
  line, with no space or newline between it and the text. The `dy` puts the note's first
  baseline on the text's. Keep the plain `place(right, dx: ..., dy: 2.7pt, note)` form only for
  a note that precedes a block (a theorem or proof).
- Long numbered headings ("Appendix B. ...") wrap with a hanging indent as wide as the number.
  `#set heading(hanging-indent: 0pt)` makes them wrap flush left.
- For "Sections 1 to 5", use `#ref(<label>, supplement: none)` for each number.
- Keep a short final list (Sources) together with its heading in `block(breakable: not-print)`,
  so the last page never holds one stray bullet. Do not make a captioned table breakable to
  save space: its caption can be stranded at the bottom of the previous page.
- A table may need `placement: none` in print and `placement: auto` on the narrow edition; pass
  the edition flag to `placement`.
- After moving sections, rebuild and read the outline (`pdftotext | grep` for headings and
  theorem numbers); figure and proposition numbers shift, and comments in code that cite them
  must follow.

## Numbers, data and ports

- The script that computes a document's numbers also writes a CSV next to the `.typ`; plots
  read it with `csv("x.csv", row-type: dictionary)`. A test checks that the committed CSV is
  exactly what the script writes, so a figure cannot drift from the code.
- Porting from LyX or TeXmacs: rewrite rather than convert, and recompute every claim before
  keeping it. A ported Bayes integral had lost its $q^k$ and its $dq$; a TeXmacs note stopped
  mid-derivation and was finished by computing the distribution exactly.
- In markup `<` starts a label: write `\<0.001%` in a table cell.
- An ordinal built from a formula breaks badly at a line end; keep it whole with
  `#box[$(k + 1)$th]`.
- fletcher self-loops: `edge(<a>, <a>, "-|>", bend: 130deg, loop-angle: 90deg)`. A row of nine
  6.5 mm circles at spacing 5.5 mm fits a 5.4 in column without scaling; at 9.5 mm it was
  scaled down until the loop labels were unreadable.
- To keep a short last page from holding a lone bullet, cut words (drop the weakest item),
  and let a table float (`placement: auto`, introduced by a reference rather than a colon).

## Visual QA procedure (every version)

1. Contact sheets for layout: `pdftoppm -r 45 -png doc.pdf p`, then paste eight pages per image
   with PIL. Look for holes at page bottoms, figures far from their text, stranded headings or
   single lines, crowded pages, boxes stacked together.
2. Crops at symbol level: `pdftoppm -r 100`, crop each figure, deal row and table, and look at
   alignment, label collisions, arrowheads, baseline of inline elements, line breaks inside
   formulas.
3. Text extraction: `pdftotext -layout` and grep for leftover private names, British/American
   mixes, numbers formatted like "66, 045".
4. Check color meanings are consistent across figures, and every axis or figure label is defined
   in the text.
5. After fixing, rebuild and re-check the pages that moved.
6. Scan every page by machine as well: `pdftotext -bbox` gives word boxes. Flag any body word
   past the right text edge (overflow), any page whose last body line sits well above the
   bottom (a hole), and any margin note whose first line is not level with the nearest text
   line (compare `yMax`; a constant offset of under a point is the font-size difference).
   Count boxes per page with `pdftotext -f N -l N | grep -c '^IDEA\|^TRY IT'`.
7. Diff the extracted text against the previous version (`pdftotext` both, then `diff`): the
   changed lines should be exactly the ones you meant to change.
8. Rebuild from the repository copy in an empty folder and compare the extracted text with the
   built PDF, so the committed source is known to produce the committed file.