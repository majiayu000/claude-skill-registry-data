---
name: stl-to-openscad
description: Reverse-engineer STL files into clean, parametric OpenSCAD that reproduces the original and can then be customized. Measures meshes with cross-sections, rebuilds each part from named parameters, proves the rebuild matches the original by boolean diff (volume and IoU), then adds customization such as a different switch, display, board or screw size. Use this whenever someone wants to edit, remix, resize, re-parameterize or "make editable" an STL, convert STL/mesh to OpenSCAD/SCAD, or modify the printed enclosure of an open-source hardware project (keyboards, handheld gadgets, ESP32/Arduino/Raspberry Pi builds, sensor and display enclosures) that only ships STLs. Also use it when the user points to a GitHub repo with STLs and asks to change the case, even if they never say "OpenSCAD" or "reverse-engineer".
---

# STL → parametric OpenSCAD

An STL is only triangles: it has no dimensions, no design intent and no parameters. The goal is a set of `.scad` files that:

1. **reproduce the original exactly** (proved by a boolean diff, not by eye), and
2. **expose the design as named parameters**, so the next person can change a screw size, a switch type or a board footprint and have every part that depends on it update with it.

Do it in that order. A faithful baseline is what makes later changes safe: when a customized part doesn't fit, you can diff it against a rebuild you know is right instead of wondering whether the bug was there from the start.

## Tools

- **OpenSCAD** on the command line, in a version with the Manifold backend (`openscad --help` lists `--backend`; the 2021.01 release is too old). Use `--backend Manifold` for exports, which is much faster than CGAL. If it's missing, point the user to the skill's README.md install section.
- **uv** (https://docs.astral.sh/uv/) runs the bundled scripts. They declare their own Python dependencies (manifold3d, trimesh, numpy, matplotlib), so there's nothing else to install.
- Bundled scripts, in `scripts/` next to this file:
  - `stl_probe.py`: size, units, frame, flat levels and cross-sections of an STL, with circles, rectangles and repeated grids recognized. `--png` draws the sections so you can look at them.
  - `compare_stl.py`: original vs rebuilt (`.stl`, or a `.scad` it renders for you). Prints volume difference, IoU and a list of the regions that differ, each with its size and location. Has `--mirror` for left/right pairs, `--overlay z=… --png` for an outline overlay, and `--xor-out` to save the difference as an STL.
  - `check_assembly.py`: exported parts and reference components in one frame. Reports overlaps (volume and location), how far each nearby pair can slide before contact, and bed fit (`--bed 256x256x256`).
- If the companion `openscad`, `preview-scad` and `export-stl` skills are installed, use them for versioned files, PNG previews and validated exports. Otherwise use plain `openscad -o file.png` / `-o file.stl`.

Run the scripts with `uv run <skill-dir>/scripts/stl_probe.py …`, where `<skill-dir>` is this skill's folder (the base directory shown when the skill loads). Run any of them with `--help` for every option.

## Workflow

### 1. Get the source and check what you're allowed to do

- Clone the project into an `upstream/` folder and never edit it. If the repo is huge, a sparse, shallow clone (`git clone --depth 1 --filter=blob:none --sparse` + `git sparse-checkout set <dir>`) gets just the project folder.
- **Look for real CAD before reverse-engineering anything.** Check for `.step`, `.f3d`, `.scad`, `.FCStd` and Onshape links in the repo, its README, its releases and the author's Printables/Thingiverse page. If parametric source exists, use it.
- **Read the license** and tell the user what it means for them. Many hardware projects are CC BY-NC-SA or similar: a remix must credit the author, keep the same license and can't be sold. Put the attribution and license at the top of every `.scad` file and in the project README.
- Read the build guide, BOM and photos. They tell you what each feature is for ("the 9 × 3.5 slot is the board's USB-C port"), and that's what you'll name your parameters after.

### 2. Survey every STL before modelling any of them

Run `stl_probe.py` on each file and write down:

- **Units and frame.** If the largest size is < 15, it's probably inches. If the parts were exported in a shared assembly frame (they overlap in the right places when imported together), **keep that frame**: every rebuilt part then overlays its original with no transforms, and parts line up with each other for free. If each STL sits at its own origin, pick one assembly frame and record each part's placement in the common file.
- **Several bodies in one STL** (a print plate): treat each as its own part.
- **Mirror pairs.** `compare_stl.py left.stl right.stl --mirror x`. If the IoU is ~1.0, model one part with a `side` parameter.
- **Interfaces between parts.** Screw holes in one part that line up with bosses in another, a plate that sits on a ledge, a lid that slips into a rim. These become **shared** parameters (step 4).
- **Facet counts.** The probe reports `$fn≈N` for each circle. Using the same `$fn` in the rebuild keeps faceting from showing up as a volume difference.

### 3. Measure each part from cross-sections

The probe's default output is the core of the method:

- **Flat levels** (`## flat faces ⟂ z`) list every height where there's a horizontal face: the floor top, a ledge, a counterbore bottom, the rim. Most printed parts are a stack of extrusions between these heights.
- **Auto-slices** are taken midway between consecutive levels, so each one shows the 2D profile of one extrusion. Each ring is classified as `rect`, `rrect` (rounded rectangle, with an estimated radius), `circle` (diameter, centre, `$fn`) or `poly`. Identical holes are grouped, with their pitch.
- **Side features** (ports, switch slots, screw holes through walls) need `--axis x` or `--axis y` slices: for example `--axis y --at <just inside the back wall>`.
- Use `--png` and **look at the image** whenever a ring comes out as `poly` or the numbers don't make sense. Notches, chamfers and fillets are obvious in the picture and confusing in the numbers.
- Use `--at` to slice exactly where you need to, for example 0.1 mm above and below a level to see what changes there.

**Snap measurements to design intent.** The designer typed round numbers. A slice that reads 19.049 is 19.05 (0.75 in, the MX key pitch). 2.893 is a 2.9 hole with 48 facets. 64.098 is 64.1. Prefer numbers that are round in mm, in inches, or in standard part sizes (key pitch, M-screw clearances, header pitch 2.54). Then check the snapped value against the diff in step 5. Don't snap a dimension that is clearly derived from other ones, like a wall that is `outer − 2 × wall`: write it as that formula.

Curved and organic surfaces (fillets, domes, lofted shells) can't be read from slices exactly. Approximate them with `hull()`, `minkowski()`, `offset(r)` or stacked `linear_extrude` with `scale`, and accept a small, explained difference (step 5).

### 4. Structure the OpenSCAD project

```
<project>/
  upstream/                  untouched clone (original STLs live here)
  scad/
    common_001.scad          shared parameters, interfaces, helper modules
    <part>_001.scad          one file per part, include <common_001.scad>
    assembly_001.scad        every part + reference components, use <...>
    out/                     exported STLs (what gets sliced)
    reference/               overlay PNGs from compare_stl.py, for the README
  README.md                  what each file is, parameters, verification table, print notes
```

Conventions that make the files easy for other people to customize:

- **Parameters at the top, named for what they do**, with units and a comment saying what physical thing they fit: `usb_size = [9.5, 3.8]; // USB-C receptacle opening`, not `a = 11`. Group them: overall size, walls, features, hardware.
- **Anything two parts must agree on lives in `common_*.scad`**: screw positions (as a function or list both parts read), footprints, plate positions, clearances. That way a hole can't move in one part without its boss moving in the other.
- **Hardware in one block**: clearance hole, head counterbore Ø × depth, heat-set insert hole Ø × depth. Changing M2.5 to M2 should be a single edit.
- **`show_original = false;`** in every part file: when true, `%import()` the upstream STL as a ghost over the rebuild, so anyone can check it in the GUI.
- **Mirror pairs → one file** with `side = "left" | "right"`.
- Cutting tools overshoot every face they cut through by `eps` (0.01) to avoid coincident faces and preview flicker.
- **Versioned files** (`_001`, `_002`, …): `_001` is the faithful rebuild and stays faithful forever. Each customization goes into a new version, and the README says what changed in each one.

### 5. Prove the rebuild matches

For each part:

```
uv run <skill-dir>/scripts/compare_stl.py upstream/.../part.stl scad/part_001.scad [-D side='"right"']
```

- **Targets:** for prismatic parts (plates, trays, brackets) expect IoU ≥ 0.999 and a volume difference of a few mm³. A part with fillets or domes may land around 0.99–0.995; that's acceptable once you know *where* the difference is and that it doesn't touch a fit surface.
- **Read the diff regions, not just the IoU.** Each line gives a location and a size. A thin `missing` region 0.4 mm thick across a whole face means a height or thickness is off. Four identical small regions at the corners means a radius or a boss is wrong. A region that is "extra" in one place and "missing" right next to it means a feature is offset.
- When a region is unclear, use `--overlay z=<height> --png` to see both outlines, or `--xor-out diff.stl` and `import()` it in OpenSCAD.
- Iterate until the part passes, then record the result in a README table: part | volume diff | IoU | notes on any known difference.
- Render a PNG of each part and an exploded view of the assembly for the README. Read the images to check them yourself.

Tell the user honestly where a rebuild differs from the original. "Matches except at the outer top fillets (0.4 % of the volume), which don't touch any fit surface" is useful; "looks the same" is not.

### 6. Customize

Only once the baseline passes. For electronics projects, the usual changes are:

- **Swapping a component** (another switch type, a bigger display, a different MCU board, a USB-C module instead of micro-USB). Make the component a choice parameter (`switch_type = "choc" | "mx"`) that drives every dimension that depends on it, and keep a mode that still reproduces the original, so you can re-run the step 5 diff on it.
- **Changing hardware** to what the user actually has (screw size, heat-set inserts, magnets).
- **Adding features**: retaining screws, cable passages, standoffs for a new board, vents, labels.
- **Fitting the printer**: splitting a part that's bigger than the bed, or reorienting it.

Read `references/electronics-enclosures.md` before making changes like these. It covers reference component models, fastener and insert stacks, FDM tolerances, fit checks and test coupons.

Keep the original's style when you add features: if the original uses 3 mm walls and 3 mm corner radii, new bosses and ribs should too.

### 7. Check fit, export and document

- Build an `assembly_*.scad` that places every part and simple **reference models** of the electronics (board, display, battery, connectors) as boxes with the datasheet dimensions. Mark sizes taken from a datasheet or a guess as approximate, so the user knows to measure the real part.
- Check that parts don't overlap each other or the electronics (`check_assembly.py`), and that screw holes line up across parts, **by measuring the exported meshes**, not by re-reading the parameters (a check that reads the same parameters as the model will always agree with itself). See the fit-check section of the reference.
- Export each part to `out/` with `openscad --backend Manifold -o out/<part>_00N.stl scad/<part>_00N.scad` and confirm the mesh is watertight (`stl_probe.py` reports it).
- Check each part fits the bed of the printer the user will print on. Ask which printer if you don't know, and pass its build volume to `check_assembly.py --bed`. For anything with press fits, inserts or snap-in parts, suggest a small **test coupon** cut from the real part (see reference) before a multi-hour print.
- Update the README: file map, parameter table, the verification table from step 5, hardware/BOM, and print orientation and support notes.

## Pitfalls

- **Preview vs render.** F5 preview (OpenCSG) can draw `intersection()` of a hollow part as solid and make coincident faces flicker. Wrap derived parts in `render()` and cut with `difference()` of the complement instead. Judge geometry from the exported mesh, not the preview picture.
- **`include` vs `use`.** `include <common.scad>` brings in variables and modules; `use <part.scad>` brings in only modules, so top-level parameter changes in the part file are ignored. The assembly should `use` the parts and take shared values from `common`, otherwise overrides silently do nothing.
- **`-D` overrides on the command line** only affect the file being rendered and anything it `include`s, not files pulled in with `use`.
- **Non-manifold originals.** Some STLs aren't watertight, and then the probe and the compare script refuse them. Repair the file first (import it in OpenSCAD and export it again, or `trimesh` `fill_holes`) and say that you did.
- **Unit and axis surprises.** Inch exports, Y-up exports from some CAD tools (the part lies on its side), and print-plate STLs with several parts. Catch these in step 2, not after modelling.
