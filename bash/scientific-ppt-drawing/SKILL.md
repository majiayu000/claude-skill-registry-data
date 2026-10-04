---
name: scientific-ppt-drawing
description: Create or reconstruct scientific schematics as editable native PowerPoint shapes and live text, starting from a description, reference image, or SVG. Use when a user explicitly wants a scientific figure drawn or revised inside PPT/PPTX.
---

# Scientific PPT Drawing

Version 0.1.0. Create a scientific figure whose key biological structures and instruments are recognizable at the intended slide size, while keeping its lines, paths, shapes, and text editable in PowerPoint. This skill creates one figure per slide, then can transfer its native objects to an existing deck. It does not need a data file or vector source when the user asks for a conceptual figure.

## Start and route

Resolve `skill_dir` from this `SKILL.md`. Read [setup and application control](references/setup-and-app-control.md) on a new machine or when opening an existing deck. Run the bundled CLI with a CPython 3.11–3.13 environment containing `requirements.lock`:

```text
<python> <skill_dir>/scripts/figure_cli.py doctor
```

Choose the user's actual input route:

- **Description alone:** plan the scientific story, panels, labels, iconography, and hierarchy; draw a structured SVG from scratch using paths, basic shapes, and real `<text>`. If useful, consult relevant papers for visual conventions and cite them. Illustrative measurements must be visibly identified as illustrative; never infer experimental values from a picture.
- **Reference image:** inspect and redraw the scientific content as intentional PowerPoint objects. Follow [semantic drawing](references/semantic-drawing.md): one continuous line should normally become one editable path; construct each instrument or icon from a small set of meaningful parts. Recreate text as live text. Use [raster reconstruction](references/raster-reconstruction.md) only for selected details that cannot reasonably be redrawn by hand, and simplify those traces before delivery. Never place an unchanged full-panel screenshot into the PPTX as the figure.
- **Existing SVG:** validate it and render it directly. Resolve unsupported effects explicitly; the parser rejects them rather than omitting them.

Treat papers and web pages as visual references, not as evidence that the user's figure contains measured results. Preserve the user's original file and use new output filenames for iterations.

## Draw and render

Design on a white SVG canvas at the desired aspect ratio. First make an object plan: identify continuous lines, independent filled regions, device parts, labels, and repeated structures. For every key structure or instrument, list the visible features that make it identifiable; these features must survive the redraw. Use one path for each continuous mark rather than assembling it from short strokes or traced fragments. A repeated grid can be one compound path when its marks share styling. Add separate shapes for meaningful detail instead of minimizing shape count at the expense of recognition. Give important objects clear, unique `id`s; keep labels as separate `<text>` elements and one line per text object. Prefer a small coherent palette, consistent line widths, readable type, and meaningful grouping. The SVG is a portable editable source; its shapes and text are converted to native PowerPoint objects by:

```text
<python> <skill_dir>/scripts/figure_cli.py validate <figure.svg>
<python> <skill_dir>/scripts/figure_cli.py render <figure.svg> <new-figure.pptx> --width-in 13.333
<python> <skill_dir>/scripts/figure_cli.py inspect <new-figure.pptx>
<python> <skill_dir>/scripts/figure_cli.py compatibility <new-figure.pptx>
```

`render` writes a one-slide `.pptx` and adjacent `.audit.json`; it does not rasterize SVG paths or lettering. `inspect` reports native shape, live-text, curve, and picture counts. A zero picture count confirms that the artwork is native, but does not prove that its object structure is usable. Check the object count against the plan and select a representative continuous path in PowerPoint: it should be one freeform object. Read [supported SVG and output](references/svg-and-qa.md) for precise syntax and limits.

## PowerPoint control

When the user requests a new PPT figure, launch PowerPoint yourself and open the generated PPTX. The user need not pre-open the application. When the user explicitly names an already open PPT, inspect that actual deck and draw in it: generate the native figure, then use PowerPoint's UI to copy its native shapes onto the chosen slide, position them, and save the requested file. Keep the target's other content intact. If a referenced deck is unsaved or ambiguous, identify it by the visible document title before placing anything.

Use the available computer-control tool for application actions. On macOS, `cua.getApp("Microsoft PowerPoint")` can launch or select it; use its observed UI state to open files and manipulate slides. A direct file launch is a fallback if the control tool is unavailable, but opening a file alone is not visual QA. Do not claim UI or editing verification unless it was actually observed.

## Visual and editability acceptance gate

Follow [quality gates](references/quality-gates.md) before calling a figure complete. Open the output in PowerPoint. Compare reference and output side by side at the intended slide size and in crops of each critical object. A DNA helix must read as DNA without its label; an instrument must retain the reference's distinguishing parts, perspective, and visual hierarchy. A generic monitor, box, or rack substituted for a specific apparatus fails this gate. Check labels, arrows, layering, small structures, typography, and colors. Test selection and editing of representative curves, icons, and text. Continuous lines must be single freeforms where practical, while a device may use as many meaningful native parts as its recognition requires. If any critical object fails recognition or a distinguishing feature is missing, redraw it and repeat the PowerPoint review before delivery. Automated raster similarity and a low object count cannot override a visual failure.

For raster inputs, transcribe every label and check every meaningful structure against the original. A traced letter outline is a path, not editable text. Report any region intentionally simplified or any font substituted. Deliver the PPTX, SVG source, and audit record; include a PNG preview when possible. Keep all validation claims tied to the specific PowerPoint version and machine actually tested.

The renderer targets the base PPTX shape and text markup and avoids optional Office-version extensions. For another PowerPoint version or Windows, run the structural `compatibility` check and the small native open/edit check in [setup and application control](references/setup-and-app-control.md). If text changes because its font is unavailable, render a new file with `--fallback-font Arial` and inspect it again. Keep the SVG source and the original output; do not convert the editable artwork to a picture as a silent fallback. Windows native rendering and UI transfer remain unverified until tested there.
