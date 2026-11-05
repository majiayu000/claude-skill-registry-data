---
name: docx
description: Write a real Word document (.docx) from Markdown — headings, lists, tables, pictures and native editable charts — or read a .docx back to Markdown. Standard library only, no Word needed.
license: Apache-2.0
compatibility:
  python: true
---

# docx

Create a `.docx` that opens in Word, LibreOffice and Google Docs, or read an
existing `.docx` so its text can be summarised, merged or rewritten. No extra
packages: the script builds the OOXML package itself.

## When to use

- The user wants a Word file: report, memo, thesis chapter, meeting notes.
- The user wants a **document with graphs** — use a `chart` block, it becomes
  a native Word chart the user can restyle.
- The user has `.docx` files in an allowed folder and wants their content
  (read them first, then write the new document).

## How to run

Write: first save the Markdown with `write_file` into the out-box, then

```
python3 <skill_dir>/run.py write <input.md> <output.docx>
```

Read (Markdown out, so you can `read_file` it):

```
python3 <skill_dir>/run.py read <input.docx> <output.md>
```

- `<output.docx>` / `<output.md>` — paths **inside the out-box**.
- `<input.docx>` — a `.docx` in an allowed folder or in the out-box.

## Markdown the writer understands

```
# Document title            (first H1 only)
## Heading 1 / ### Heading 2
Paragraphs with **bold**, *italic*, `code`.
- bullets            1. numbered            > quote
| Col A | Col B |     (first row is the header)
![Caption](figure.png)      picture, path relative to the .md
---                         page break
```

A chart block:

````
```chart
type: bar            (bar | line | pie)
title: AI adoption by sector (%)
categories: Finance, Health, Retail
series: 2024: 38, 22, 30
series: 2026: 61, 41, 52
```
````

Standard library only. After the script exits 0, tell the user the full path.
