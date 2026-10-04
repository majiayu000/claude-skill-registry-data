---
name: vizuara-report
description: >
  Generate a comprehensive, in-depth client report as a polished A4 PDF in the
  Vizuara Ramco house style. Orchestrates two skills: vizuara-ramco-pdf for the
  layout and print pipeline, and wisprflow-figure for every chart or stat figure.
  Writes in a natural human voice with no em dashes. Use when the user asks for a
  full report, proposal, engagement roadmap, status review, evaluation writeup, or
  any long client-facing PDF that needs figures.
---

# Vizuara Report Generator

This skill turns a topic, a data set, or a pile of notes into a finished
client-facing PDF report. It does not reinvent styling. It combines two skills you
already have installed:

- **vizuara-ramco-pdf** gives the house style: the stylesheet, the HTML components,
  and the headless Chrome render step that produces the A4 PDF.
- **wisprflow-figure** gives every figure in the report: cream paper, Georgia serif,
  terracotta and sage and lilac palette, big number headers, hand drawn baseline.

You write the report as an HTML file using the house style components, generate a
figure for each quantitative point, then render to PDF and verify.

## Dependencies

Both skills must be installed next to this one (the usual place is
`~/.claude/skills/`). The build script finds them automatically. If you only have the
zip files, unzip all three into the same skills folder first. Requirements:
Google Chrome (or Chromium or Edge), and `pip install matplotlib numpy pymupdf`.

## Workflow

1. **Decide the argument.** Before writing anything, settle the one thesis the report
   proves, and the audience (usually Ramco management or the board). Everything serves
   that argument.

2. **Plan a comprehensive structure.** A real report is deep, not a summary. Use the
   blueprint below and expand each section with specifics, numbers, and reasoning. Aim
   for depth: name the mechanisms, quantify the claims, address the objections.

3. **Generate every figure first.** For each number that carries weight, make a figure
   with wisprflow-figure and save the PNG next to your HTML. Import the library:
   ```python
   import sys; sys.path.insert(0, "PATH/TO/wisprflow-figure/scripts")
   from wisprflow_figures import stat_bars, comparison_bars, donut
   stat_bars(counts=[...], labels=[...], headline="92.3%\ncore correct or better",
             sub="One or two sentence caption, no em dash.", out="fig_accuracy.png")
   ```
   Pick the type by shape: `stat_bars` for a headline number with a distribution,
   `comparison_bars` for before and after or ranked options, `donut` for a single
   share. Colours carry meaning: terra for low or cost, sage for the neutral good
   case, lilac for the strong result.

4. **Assemble the HTML.** Start from `assets/report_skeleton.html` in this skill. It is
   a full multi section document wired to `report.css` with figure slots already in
   place. Fill it in with the house style components (see the vizuara-ramco-pdf skill
   for the component reference: cover, section badges, pills, tables, gantt, callouts,
   appendix).

5. **Build the PDF.**
   ```bash
   python3 scripts/build.py path/to/report.html path/to/report.pdf
   ```
   `build.py` copies `report.css` from the vizuara-ramco-pdf skill next to your HTML,
   then renders A4 with headless Chrome. Figures referenced by the HTML must already
   sit in the same folder.

6. **Verify before handing over.** Render the PDF pages to PNG and read them. Check the
   cover wordmark and terracotta badges, the pill colours, every figure, and that no
   text overflows. Fix, rebuild, repeat until it is clean.
   ```bash
   python3 - <<'PY'
   import fitz; d=fitz.open("report.pdf")
   [p.get_pixmap(matrix=fitz.Matrix(2,2)).save(f"pg{i}.png") for i,p in enumerate(d)]
   PY
   ```

## Comprehensive structure blueprint

Adapt to the topic, but a strong report covers all of these. Go deep in each.

1. **Cover.** Wordmark, kicker, a title that states the thesis, a lead sentence, the
   meta grid (Prepared for, Scope, Prepared by, Document), one sage point box with the
   single most important takeaway, confidentiality line.
2. **Executive summary.** Half a page that a busy executive can read alone and get the
   whole argument, with the key numbers stated plainly.
3. **Context and problem.** What the situation is today, why it matters now, what it
   costs to leave it alone. Be concrete about the current state.
4. **What we did or propose.** The approach, the mechanism, why it works. This is the
   core. Break it into subsections with their own headers, bullet lists, and figures.
5. **Evidence.** The numbers that back the claim, each with a wisprflow figure. Explain
   what each figure shows and why it is credible.
6. **Timeline.** A gantt of the workstreams on one calendar, with a clearly bounded
   end. Follow it with a roadmap table (committed, optional, future) with status pills.
7. **Detail sections.** One per milestone or workstream: scope, key activities, exit
   criteria in a sage callout. This is where depth lives.
8. **Risks and open questions.** What could go wrong and how it is handled. Use the
   neutral grey status callout for anything still to be decided.
9. **Appendix.** Supporting material, method notes, glossary, anything that would
   clutter the main flow.

## Writing rules

- **Write like a person, not a model.** Do not use the em dash or a double hyphen
  anywhere in the prose. Where you would reach for one, use a comma, a colon, a period,
  or parentheses instead. For example, write "the engine runs the journey end to end,
  with no human step" rather than using a dash. This applies to section titles too:
  prefer "Chia: the milestones at a glance" over a dash. A plain hyphen inside a real
  compound word like "end-to-end" or "to-be-decided" is fine.
- Avoid the usual AI tells: no "in today's fast paced world", no "it is important to
  note", no empty throat clearing. Open sections with the point.
- Be specific. Prefer real numbers, dates, and named mechanisms over adjectives.
  "Handles 93 journeys per analyst day" beats "dramatically improves throughput".
- Keep it calm and confident. Short sentences. One idea per paragraph. Let the figures
  carry the quantitative weight so the prose can stay clean.
- Stay comprehensive. When in doubt, add the missing detail, the objection, the number,
  the example. A thin report reads as a sales sheet; a deep one reads as trustworthy.
- Match the house voice: Vizuara prepared it, it is commercial in confidence, prepared
  by "Raj, Rajat" and colleagues, for Ramco.

## What this skill produces

A single A4 PDF, styled exactly like the reference Vizuara Ramco documents, with
editorial figures embedded throughout, written in a clean human voice. Hand the PDF to
the client and keep the HTML and figure sources for the next revision.
