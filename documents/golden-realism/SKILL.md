---
name: golden-realism
description: Make every golden deliverable look like a work product a real analyst produced, because a golden that reads as overly LLM-generated is sent back even when every figure recomputes. Carries the tells a reviewer reads at a glance, the per-format editing passes for memos, workbooks, decks, charts, conformed data and code, the metadata scrub, and the hard line that realism is presentation and may never move a graded figure or open a second reading. Use after the golden's numbers are correct and before the bundle is declared ready, on any deliverable an LLM drafted, and when a submission comes back for looking machine-made.
---

# Golden Realism

A golden that looks LLM-generated is sent back even when every figure recomputes. Drafting with an LLM is
fine; shipping its first draft is not. This is an **editing pass over a draft already numerically
correct**, run after the figures are asserted and beside `reduce-house-fixes` (which owns the container,
H1, and the write-up prose, H2 and H3).

**The hard line.** Realism is presentation. No edit may change a graded figure, answer or contradict an
ask, or open a second reading. A "realistic caveat" that makes a number ambiguous is a Gate E failure;
when a realism move and a determinism gate collide, the gate wins.

## Part 1. The tells

1. **Uniform precision.** Real work varies it: headcounts whole, money to the cent at invoice scale and the
   thousand at budget scale, rates to one decimal. The fastest tell, visible without reading.
2. **Default styling.** The library's first colour, 8.43-character columns, stock template, legend where the
   library put it.
3. **The four-heading spine** (Executive Summary, Key Findings, Recommendations, Next Steps). Take the shape
   from the genre: a determination has a standard and a finding, a reconciliation a bridge.
4. **Sections of equal length.** Real documents are lopsided toward the decision.
5. **Everything in threes.** Real lists are as long as the world is.
6. **Bullets and prose inverted.** The argument is prose; the enumerable (candidates, periods, exceptions)
   is the list or table.
7. **No trace of use.** Real products carry residue: a footnote on a disputed definition, a noted
   exclusion, a stated rounding convention. Take it from the pack's own fiction (Part 4).
8. **The hedge register.** "This analysis suggests", "it is important to note", comprehensive, robust,
   leverage, key insights, actionable.
9. **Titles that restate the task.** The finding is the title.
10. **Generic file names.** Not `analysis_report.pdf`; name it after the decision in the organisation's
    vocabulary.

## Part 2. Per-format passes

**Text (PDF, DOCX).** The genre's identifying block (addressee, author, date, subject, reference); page
numbers and a running header or footer where the genre has one; a finding as title; lopsided sections with
the decision longest, in prose; enumerables in tables; a source line under every table in the fiction's
vocabulary; at least one true footnote that opens no second reading; precision per quantity.

**Data (XLSX).** Named sheets, never `Sheet1`; frozen header (and key columns when wide); widths set to
content; number formats per column (currency, %, thousands separators, dates), never a fourteen-decimal
float; numbers right, text left; a total row computed from unrounded source that ties to every deliverable
citing it; print area and repeat rows where a person would print; a notes sheet with definitions, as-of
date and exclusions; autofilter only where one belongs.

**Visual (PPTX).** Slide titles as finding sentences; the chart is the slide, not bullets about it; slide
numbers and a source strip; stock template replaced or colours and type set deliberately.

**Charts (PNG, SVG, embedded).** Load `dataviz` first. Units on axes; ticks formatted for reading, never
scientific notation; a finding as title; the threshold line labelled with its value; the key point
annotated; a deliberate palette with the recommended item distinguished; size and resolution for where it
lands.

**Data (CSV, TSV, JSON, Parquet).** Column names in the source systems' vocabulary; a stated, stable sort;
consistent precision per column; ISO dates; booleans as the consuming system writes them; a dictionary
alongside where the fiction would have one.

**Code (PY, IPYNB, SQL, R).** Constants at the top, read from the pack, never hardcoded twice; assertions on
control totals; formatted output with units (the deliverable is what it prints); comments only where a
choice was made; a notebook's outputs match one top-to-bottom run and its markdown carries the argument.

## Part 3. The container

`reduce-house-fixes` H1 owns it and its tool:

```
python3 .claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py <dir>
python3 .claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py <dir> --apply \
    --producer "<the organisation in the fiction>" --stamp <the in-fiction date>
```

Audit first: the producer and date are the fiction's and cannot be guessed. Never re-save through the
writing library.

## Part 4. Honest texture only

Every piece of texture must be true of the pack, in this order of preference: the pack's governing
documents (a definition, an exclusion, a tolerance, cited in a footnote); the pack's own disputes (a belief
someone held and how it was resolved); the analysis's own conventions (rounding, as-of date, population
after exclusions, grain), each already pinned.

**Never:** a fabricated caveat, a fake revision history, invented initials, a data-quality note about a
problem the pack lacks, or a value made scruffy (a wrong figure fails Gate A).

## Part 5. The pass

1. Figures correct, asserted and frozen first.
2. Read the draft once at speed as a reviewer; note the tells before fixing anything.
3. Run each format's pass.
4. Add texture from Part 4 only, checking each addition against every ask.
5. Scrub the container.
6. Re-run the bundle verifier: every graded figure unchanged in every file at the same rounding.
7. Read once more cold; a draft still reading as a template usually has a structure problem (tell 3).

## Checklist

- [ ] Figures asserted before and after; no edit moved a value, answered an ask or opened a reading
- [ ] Precision varies by quantity; no default styling survives
- [ ] Structure from the genre; lopsided sections; lists their natural length; argument in prose
- [ ] At least one true note from the pack; nothing fabricated; no hedge register
- [ ] Titles state findings; files named after the decision
- [ ] Format passes done (workbook affordances, chart pass with `dataviz`, code assertions and prints)
- [ ] Container scrubbed, audited first; bundle verifier green
