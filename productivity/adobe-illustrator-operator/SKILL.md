---
name: adobe-illustrator-operator
description: Use when working with Adobe Illustrator files, .ai brand assets, artboards, layers, vector exports, SVG/PDF/PNG rendering, Illustrator scripting, Illustrator-to-Penpot 1:1 reconstruction, Flue Illustrator bridges, or computer-use fallback for Adobe UI workflows.
---

# Adobe Illustrator operator

Use this skill to operate Illustrator work safely, starting with the least fragile path that can prove the result.

## Operating rule

Do not open or mutate Illustrator by reflex. Pick the lowest-risk lane that satisfies the task.

1. Inspect the asset and requested output.
2. Use file-level tools when the `.ai` file is PDF-compatible and the task is render, contact sheet, preview, page count, or basic extraction.
3. Use Illustrator scripting only when the task needs real Illustrator document state, artboards, layers, paths, swatches, text, or native export behavior.
4. Use Flue only as an optional bridge when installed and reviewed. Treat it as a runtime, not authority.
5. Use browser/computer-use only for UI-only flows, dialogs, plugin installs, visual confirmation, or workflows the scripting lane cannot reach.
6. Never save, close, overwrite, package, relink, or destructive-export unless the user explicitly asks.
7. Verify with a file readback or visual review before claiming completion.

## Lane selection

| Task | Default lane | Proof |
|---|---|---|
| Preview `.ai`, make PNGs, count pages | File-level tools | `file`, `pdfinfo`, rendered output |
| Export PDF-compatible `.ai` to PNG/SVG/PDF | File-level tools first | output files plus visual check |
| Inspect artboards, layers, swatches, selected objects | Illustrator scripting | JSON from Illustrator runtime |
| Native Illustrator export, outline text, package assets | Illustrator scripting | exported file plus readback |
| Dialogs, plugins, font UI, manual import screens | Computer-use | screenshot or visible app state |
| Experimental bridge automation | Flue optional | smoke test and JSON response |

## Illustrator to Penpot 1:1 reconstruction

When the task is to recreate an Illustrator file, brandbook, logo sheet, or layered brand asset in Penpot, Illustrator is the canonical source for both visuals and structure.

Read `references/penpot-1to1-reconstruction.md` before acting.

Non-negotiable rules:

1. Work one Illustrator document at a time.
2. Snapshot the source file before touching it.
3. Read the full Illustrator artboard and layer tree before exporting or importing.
4. Import or recreate in Illustrator tree order, not by fastest export convenience.
5. Preserve native text as text wherever technically possible.
6. Preserve source names where available.
7. Replace generic imported names with semantic names tied to the source tree.
8. Verify each artboard visually and structurally before advancing.
9. Verify the original Illustrator file stayed unchanged before reporting completion.

## Required first probe

For local assets, run the bundled probe before choosing a heavier lane:

```bash
python3 <skill>/scripts/probe_illustrator_asset.py /path/to/file.ai
```

The probe reports whether Illustrator appears installed, whether the file is PDF-compatible, page count when available, and which lane is recommended.

## Illustrator scripting lane

Use this lane only after confirming Illustrator is installed and the user wants Illustrator-level behavior.

On macOS, Illustrator scripting normally runs through AppleScript/JXA calling JavaScript in Illustrator. Keep scripts small and return JSON text.

Safe first script goal:

- list document name
- list artboards
- list layer names
- do not edit
- do not save

If the script needs API details, use Adobe Illustrator scripting docs or local app introspection before guessing.

Read `references/illustrator-control-map.md` before running scripting or Flue.

## Flue lane

Flue can be useful, but it is optional and alpha-quality until locally proven.

Use Flue only if all are true:

- the user approved using it for this session
- `flue` is installed and version is known
- Illustrator is installed and open
- a read-only smoke test succeeds

Do not install `flue`, run `flue setup`, or change agent configs without explicit user approval.

## Computer-use lane

Use computer-use or Chrome/browser control when the task depends on UI state that scripting cannot reach. Examples: plugin installation, font upload UI, save/export dialogs, or visual checks inside Illustrator.

Before acting through UI:

- state the exact intended click or menu action
- avoid destructive choices
- prefer screenshots before and after
- stop if a modal asks for account, license, overwrite, cloud sync, or payment decisions

## File-level fallback

Many `.ai` files are PDF-compatible. For brand assets, this is often enough and safer than launching Illustrator.

Read `references/file-level-recipes.md` for `pdftocairo`, `pdfinfo`, page rendering, and contact-sheet workflows.

## Completion report

Report:

- lane used: file-level, Illustrator scripting, Flue, or computer-use
- files read or created
- whether Illustrator was actually used
- strongest proof level
- limitations, especially if text/vector editability was not proved

Do not say an asset is editable in Illustrator unless Illustrator or a real vector import path proved it.
