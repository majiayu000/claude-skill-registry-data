---
name: scientific-illustrator-local
description: Rebuild scientific schematic images as editable SVG and Adobe Illustrator paths with live text, or draw new scientific diagrams from explicit content. Use for raster-to-vector reconstruction, editable paper figures, and local Illustrator drawing. Separates labels from tracing and preserves existing artwork through a shared Windows/macOS CLI. Do not use tracing to recover experimental data or apply this workflow to every uploaded image.
---

# Scientific Illustrator Local

Version 0.2.1. Produce editable paths and live text through a local workflow shared by Codex, Claude Code, and OpenCode. Instructions are in English; preserve the original language and content of figure labels.

## Start

Resolve `skill_dir` from this file's actual location. Use its scripts directly for project-local work; registering a global skill is unnecessary. For setup or a different machine, read [installation and compatibility](references/installation-and-compatibility.md).

In the commands below, `<python>` is the skill's `.venv/Scripts/python.exe` on Windows or `.venv/bin/python` on macOS, or an explicitly verified CPython 3.11-3.13 environment. `<cli>` means `skill_dir/scripts/figure_cli.py`. Quote full paths; PowerShell needs `&` before a quoted executable path.

```text
<python> -X utf8 <cli> doctor
<python> -X utf8 <cli> illustrator-doctor
```

The native adapter attaches to an already-running Illustrator instance: Windows uses PowerShell 5.1 and COM; macOS uses the actual running application bundle and AppleScript. The Python scheduler and JSX renderer are shared. Windows with Illustrator 27.2.0 has been tested on hardware; macOS and other versions still require native validation.

## Choose the input route

- **New schematic:** write structured SVG with paths, basic shapes, and real `<text>`. Use polygons for arrowheads. Data plots require the user's actual data or original vector output.
- **Existing vector SVG:** validate and prepare it directly, preserving its vector structure.
- **Raster reconstruction:** read the [workflow](references/workflow.md) and [input specification](references/input-and-validation.md). Transcribe and review every label first, remove only the text from a copy, trace the remaining artwork, then add real text at the original baselines. Do not trace letters and hide their outlines beneath white overlays.
- Use `--text-mode none` only for genuinely text-free input. Use `--text-mode outlines` only when the user explicitly accepts non-editable lettering.

Reuse established goals, preferences, and authorization. Ask only about unresolved information that materially changes the result. Preserve the source image and use a new job directory whenever the input changes.

## Prepare and review

```text
<python> -X utf8 <cli> vectorize --image <text-cleaned.png> --source-image <original.png> --text-manifest <text.json> --text-mode manifest --backend vtracer-cli --profile faithful --out-dir <new-job-directory>
```

`faithful` is a configurable starting point for detailed, low-resolution schematics: VTracer 1.x, 4x Lanczos resampling, and up to 128 colors. Interpolation smooths curve fitting without recovering missing information. For simpler diagrams, the default `--profile auto` compares lighter candidates. Parameters and candidate results are recorded in QA.

```text
<python> -X utf8 <cli> validate --svg <figure.svg>
<python> -X utf8 <cli> prepare --svg <figure.svg> --out-dir <new-job-directory>
```

Inspect candidate SVGs/PNGs, the text manifest, and `qa.json` before writing thousands of native objects. Check small structures, nuclei, fine boundaries, arrows, and pale regions. Use `--regions` for explicit local checks. Automated scores rank candidates; they do not establish biological correctness.

For a white background, edit reviewed background objects or regions specifically. Keep page background separate from pale tissue, gradients, and nuclei. Do not globally replace approximately beige colors. Unsupported SVG effects must be explicitly expanded into supported vector structures and visually checked, rather than silently removed.

## Native drawing

Connect only to Illustrator that the user has opened. For a new system or Adobe version, run a disposable-document check within the user's drawing/testing authorization:

```text
<python> -X utf8 <cli> native-test --create-document --out-dir <new-test-directory>
```

This creates and retains its own test document and audit files. Alternatively, use `--confirm-empty-document` for an explicitly designated empty document. Reuse a trustworthy native test for the same environment; do not repeat it for every figure.

```text
<python> -X utf8 <cli> draw --job-dir <job-directory> --dry-run
<python> -X utf8 <cli> draw --job-dir <job-directory> --approve-review
```

`--approve-review` records that the agent or user actually reviewed this figure; it does not mandate another permission question. Default placement finds clear artboard space. Use `--allow-overlap` only with established authorization to cover existing artwork. Map SVG coordinates through the actual `artboardRect` and viewBox; do not assume an artboard top of zero or move existing objects to make room.

Labels become native TextFrames. If all labels originally sit above the artwork, they receive a separate `Editable text` layer. Interleaved text retains the original paint order. Font selection distinguishes regular/bold faces from Black/Light; missing fonts stop preparation before artwork is added. Record when a font or size was estimated from the raster.

The scheduler creates batches, saves a job-owned `figure.ai` periodically, and exports `figure.png` after redrawing. It identifies saved documents by full path and verifies completed batches before skipping them. To resume, activate this job's saved document and rerun the same `draw` command. Do not retrace into an existing job or resume against a manually reorganized copy.

For optional native Image Trace, use `trace-native --image <image.png> --output <new.svg> --allow-temporary-document`, or add `--allow-illustrator-temp-document` to `vectorize`. The adapter closes only its own temporary document and restores the previous active document. Validate and compare the result before use; successful execution does not establish better tracing quality.

## Acceptance and delivery

- Match every label and important structure against the source, including arrows, color, layout, and fine details. Native text count must match the reviewed SVG and fonts must be correct.
- Deliver real paths and text, with no embedded raster, external resource, or script. Verify that the user's existing artwork and original files were preserved.
- Inspect the actual Illustrator PNG for layout, holes, layering, and font errors. The local path preview does not fully render text and cannot replace this check.
- `native_export_complete_visual_review_required` means automated native checks completed; visual review is still required. Claim native `.ai` delivery only after Illustrator actually saved it.
- Provide `.ai`, `.svg`, `.png`, and the necessary audit records. Disclose tracing differences; visual acceptance is not proof of pixel-perfect identity.

Core scripts do not upload images or require a vectorization API key. Dependency installation is a separate explicit step, not a per-image download. Model and Adobe access remain the user's responsibility; showing an image to a cloud model is not fully offline. Keep LICENSE and NOTICE with the skill.
