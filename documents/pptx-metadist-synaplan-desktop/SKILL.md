---
name: pptx
description: Write a real PowerPoint deck (.pptx) from a Markdown outline — title slide, bullet slides, pictures and native editable charts — or read a .pptx back to Markdown. Standard library only, no PowerPoint needed.
license: Apache-2.0
compatibility:
  python: true
---

# pptx

Create a `.pptx` that opens in PowerPoint, Keynote, LibreOffice Impress and
Google Slides, or read an existing deck so its content can be summarised or
reused. No extra packages: the script builds the OOXML package itself.

This skill is original to Synaplan Desktop (Apache-2.0). It is not Anthropic's
document skill.

## When to use

- The user asks for a PowerPoint deck, `.pptx`, or slides that open in
  PowerPoint.
- For a browser slideshow instead, use the **slides** skill.
- The user has `.pptx` files in an allowed folder and wants their text
  (read them first, then write the new deck or document).

## How to run

Write: first save the outline with `write_file` into the out-box, then

```
python3 <skill_dir>/run.py write <outline.md> <output.pptx>
```

Read (Markdown out, so you can `read_file` it):

```
python3 <skill_dir>/run.py read <input.pptx> <output.md>
```

- `<output.pptx>` / `<output.md>` — paths **inside the out-box**.
- `<input.pptx>` — a deck in an allowed folder or in the out-box.

## Outline the writer understands

```
# Deck title
One line under it becomes the subtitle.   (this IS the title slide — do not
                                            add a slide called "Title slide")

## Slide title
- bullet (keep to about six per slide)
  - sub-bullet
| Region | Units |         a Markdown table becomes a native PowerPoint table
| --- | --- |
| North | 1,320 |
![](figure.png)          picture on the right half, path relative to the .md
```

A chart on the right half of a slide (same block as the docx skill):

````
```chart
type: bar            (bar | line | pie)
title: Organisations using AI (%)
categories: Finance, Health, Retail
series: 2024: 38, 22, 30
series: 2026: 61, 41, 52
```
````

Standard library only. After the script exits 0, tell the user the full path.
