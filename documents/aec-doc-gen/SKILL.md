---
name: aec-doc-gen
description: "Converts structured Markdown into Word, Excel, or PDF for issue to a client, contractor, or authority: meeting minutes, RFIs, transmittals, change orders, punchlists, decision logs, payment applications. Trigger on \"render this as Word\", \"export to Excel\", \"save as PDF\", \"make this a transmittal\", or when a slash command in this catalog reaches its output step with a non-Markdown format declared. One direction only, Markdown to file. Carries the conversion recipes and the rules that stop a converter from quietly rewriting project content: units are never converted, dates are never re-localised, clause symbols and authority names survive intact, and a table stays a real table rather than becoming an image or a block of text."
license: MIT
metadata:
  title: "Document Export"
  summary: "Render Markdown into Word, Excel, or PDF for transmittal"
  discipline: "practice-contracts"
  tags: "Catalog Tooling, Document Generation"
---

# AEC Doc Gen

Take Markdown a command produced and write the file someone can actually
receive. The risk in this step is not the conversion, it is the converter
helpfully changing something. Most of this file is about that.

## Scope and limits — read first

**What this does.** Converts Markdown to `.docx`, `.xlsx`, or `.pdf`, keeping
tables as tables and leaving project content byte-identical.

**What this does not do.**

- It does not go the other way. To read a Word, Excel, or PDF file, use Read or
  a parser. This is one direction.
- It does not decide what goes in the document. The command upstream, or the
  user, produced the Markdown; this renders it.
- It does not apply your office template, letterhead, or numbering. Ask for the
  template file if the output must match one, and say plainly when there is none.
- It does not check the content against anything. It is a renderer.

**What you need before starting.** The Markdown, the target format, the output
path, and the template file if the output has to match a house style.

## Choosing the format

- **Word** for anything that will be marked up, signed, or filed as
  correspondence: RFIs, change orders, site visit reports, transmittal covers.
- **Excel** for anything that is a log and will be sorted or filtered:
  punchlists, payment applications, decision logs, submittal registers.
- **PDF** for anything that is issued and must not change: transmittals, owner
  reports, printable archives.

If the command did not declare one and the user did not say, ask. Do not default.

## Dependencies

Check before converting, and say which is missing rather than failing mid-run.

```bash
pip install python-docx openpyxl markdown weasyprint
```

WeasyPrint needs system libraries for PDF on some platforms. If installation
fails, say so, produce the Markdown, and tell the user what to install. Do not
block the work on a rendering dependency.

## Conversion recipes

Write the conversion inline. These are short enough that a script adds a file to
maintain without adding reliability.

**Markdown to Word.** Parse the Markdown, then with `python-docx`: headings to
heading styles at the matching level, paragraphs to paragraphs, Markdown tables
to real Word tables with a header row. A table rendered as preformatted text is
a failed conversion, because the recipient cannot sort or edit it.

**Markdown to Excel.** With `openpyxl`: each Markdown table becomes a worksheet
in document order, header row frozen. Everything outside a table goes to a final
`Notes` sheet in reading order rather than being dropped. Name sheets from the
heading above each table where there is one.

**Markdown to PDF.** Markdown to HTML with `markdown`, then WeasyPrint with a
stylesheet. Serif body, sans headings, page numbers, and generous margins for
binding and stamps. If the user has a stylesheet or template, use theirs.

## Rules that protect the content

These are the ones that matter. A converter that silently normalises project
text produces a document that looks right and says something else.

- **Never convert units.** `12 ft (3.66 m)` renders exactly as written. If the
  source has one unit system, the output has the same one.
- **Never re-localise dates or times.** `March 4, 2026` and `9:00 AM ET` render
  as written, with no locale inference and no timezone conversion.
- **Never expand or normalise an authority name.** A named building department
  or agency stays exactly as typed.
- **Never alter clause references.** Section symbols, article numbers, and
  standard designations pass through as characters, not as things to reformat.
- **Never round a number.** Not a dimension, not a dollar figure, not a
  quantity.
- **Never drop content that does not fit the format.** Text outside a table
  still goes somewhere in the Excel output. A footnote still appears in the PDF.
- **Never re-order.** Document order in equals document order out.

## Workflow

1. Confirm the target format and the output path.
2. Ask whether a template or stylesheet must be matched, and read it if so.
3. Check the dependency for that format.
4. Convert, following the recipe and the content rules above.
5. Confirm the output exists and report its path and size.
6. If the source was a temporary file written by a command, remove it after a
   successful conversion, not before.

If a dependency is missing, stop at step 3, leave the Markdown in place, and
report what to install. A missing renderer is not a reason to lose the document.

## Anti-patterns

- Rendering a Markdown table as fixed-width text in Word or PDF. It has to be a
  table.
- Converting units, currency, dates, or times "to be helpful".
- Reflowing or rewording content to fit a page break.
- Deleting the source Markdown before verifying the output was written.
- Defaulting to a format because the user did not name one.
- Silently dropping non-table content when converting to Excel.

## Resources

None. This skill is one file. The conversions are written inline at run time.
