---
name: source-files
description: Store and document source files the user provides for a car, map or other game content - 3D models (STL, GLB, glTF, OBJ, FBX), reference photos / screenshots / renders, data downloads (DEM, GIS, archives) and reference links. Use whenever the user attaches or points to such files or links (pasted images, @-mentioned paths, Downloads, Sketchfab / Printables / map links) for a model or map.
---

# Source files (models, references, data)

Every original file the user shares for game content is kept in **`sources/`** (repo root) and documented in the
`DETAILS.md` of the code folder that uses it. `sources/` is **git-ignored** (local only, can be large) - so the
`DETAILS.md` is the permanent record: it must list every file, link, author and licence (and the short `README.md` + `THIRD-PARTY.md` carry the licence summary).

```
sources/
  cars/<car-folder>/     <- same name as src/games/<game>/cars/<car-folder>/
  maps/<map-folder>/     <- same name as src/games/<game>/maps/<map-folder>/
```

For other content types follow the same pattern (`sources/<kind>/<folder>/`, mirroring the code folder).

## When the user shares files

1. **Find them.** Attached / pasted images are saved by the harness under
   `%TEMP%\claude\<project>\<session-id>\images\N.png|webp` - the message shows the exact path
   (`[Image: source: ...]`). `@"C:\...\file"` mentions and Downloads paths are real files - copy, never move.
2. **Copy** into `sources/<cars|maps>/<folder>/` with descriptive, ASCII, kebab-case names that keep the order
   they were given, e.g. `livery-ref-03-rear.webp`, `ref-08-streetview-canal-bridge.webp`,
   `rally-zavodni-auto.stl` (note the original upload name in the DETAILS.md if you rename).
   Large downloads (archives, DEMs, STL) go here too - never into `src/` or `public/`.
   **Car body model (STL / GLB / OBJ)?** Scan it right away - `python scripts/car-model/scan-mesh.py <file>` - and report the
   verdict (already split / real panel edges / blob) before anything else is built on it; a blob (image-to-3D, photo mesh) is
   documented in the DETAILS.md as rejected and not imported (`.claude/skills/rally-car-import/SKILL.md`, step 1).
3. **Document** in the code folder's `DETAILS.md` (create it if missing; keep it short, see `AGENTS.md` "Write short" - a file table, not a story):
   - a "Sources - `sources/<kind>/<folder>/` (local only, not in git)" table: file, what it is, what it was used for - one short row each;
   - credit-worthy links (model pages, data sets) also go in the def's `sources` (`CarDef` / `MapDef`) - shown on
     the main menu About screen;
   - a "Links" table: every URL the user gave (model page, photo source, map / data portal) with what it was used
     for and the **verified** licence / author (run the licence gate in `rally-car-import` first; an unknown licence is treated as
     forbidden - some sites, e.g. Printables, block automated access: ask the user to paste the licence text, never try to get
     around bot checks, never write "TODO" and carry on);
   - add rows, never delete them - mark replaced items as `superseded`.
4. **Wire credits** where the game shows them: `sources` in the `CarDef` / `MapDef` (About screen) and
   `public/models/CREDITS.md` for any shipped model. CC BY needs author + link.
5. **Generated assets** (GLB, baked map data) are produced from `sources/` by scripts
   (`scripts/car-model/stl-to-glb.mjs`, `scripts/realmap/bake.py`); put the exact command in the DETAILS.md so the
   asset can be rebuilt by anyone who has the source files.

## Rules

- Third-party photos / screenshots (Google imagery, team press photos) are reference only: never copy them into
  `public/`, never reproduce their logos / brands in liveries.
- Nothing in `sources/` is served or bundled; game code must not import from it.
- If the user shares a file without saying what it is for, ask which car / map it belongs to before filing it.
- Existing DETAILS files to follow as examples: `src/games/rally/cars/skoda-rally/DETAILS.md`,
  `src/games/rally/maps/ajvatovci/DETAILS.md`.
