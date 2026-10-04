---
name: sprite-sheet-layout
description: >
  Pokemon sheets are built in the SpriteCollab checkout and copied in
  whole: a folder per pokemon holding one layout, one binary of frames
  and a PNG per coat. Applies whenever writing or reviewing anything
  that reads a sheet, imports one, or draws a species sprite.
---

**A sheet is a bag of pictures, not a grid.** Every distinct picture sits wherever the packer put it, at whatever size its own content needs. Nothing is laid out in rows and columns, and **a clip does not own a region** — the pictures belong to the pokemon, and two animations holding the same drawing point at one copy of it.

**A pokemon is a folder**, `{region}/{species}/`, holding:

- `sheet.json` — the layout: `sheet.pictures` as `[x, y, width, height]`, an `anims` entry per animation saying how long each frame is held, a `sprites` entry per grid saying where its frames are, the coats that were drawn and who drew them.
- `frames.bin` — the frames themselves, deduplicated: one record per distinct frame, and a stream of indices pointing at them.
- `regular.png`, `shiny.png`, and `female.png` / `shiny_female.png` where a female was drawn.

**Every coat is packed to one layout.** A shiny is a second PNG over the same frames, and so is a female: swapping the image changes nothing else. `spriteImagePath(species, shiny, female)` picks the file, `spriteSheetPath` and `spriteFramesPath` the pair beside it.

**The anchors are on the frame, in the frame box's own pixels.** Shadow, body centre, head and both hands, from the collection's `-Offsets` images, and any of them may be absent (`-32768` in both slots of `frames.bin`). They may fall outside the frame: a flying pokemon's shadow is on the ground below everything drawn, and nothing clamps them.

**Read the format from the source.** `../SpriteCollab/compact/README.md` is the authority on `sheet.json` and `frames.bin`, down to the column order of the frame table; [`sprite-sheet.ts`](../../../src/canvas/sprite-sheet.ts) is this game's reader of it and nothing else.

**Two tiers of clip, and the collection names both.** The **bare minimum** six, `Idle` `Attack` `Walk` `Sleep` `Hurt` `Hop`, are what a sheet cannot be put on screen without; four more, `Charge` `Double` `Rotate` `Swing`, complete the ten a renderer may assume. They are [`MINIMUM_CAST` and `COMMON_CAST`](../../../src/data/constants/cast.ts), a cast list may end on any of the ten, and `pickCast` gives up onto two of the six. A sheet short of one of the six is unfinished art worth reporting; short of one of the other four it is drawn a little plainer.

`SpriteAnim`'s numbers are the collection's own and are **append-only**. A new animation takes the next free number; nothing already there ever moves.

## Rules

- **The clip's box is `frameWidth` × `frameHeight`.** It is the union of every frame of every direction and of every coat, it does not change while a clip plays, and **every anchor is in its coordinates**. It is what a sprite is placed, measured and hit-tested by, and what the DOM sizes its element to.
- **`sourceFrameWidth`/`sourceFrameHeight` are the cell the artist drew in.** They are authored generously, a Hop is given room for a jump twice the height anything reaches, so they are never a layout measure. They are for the shadow's width and the sparkle's spread, which are facts about the pokemon's size. A coat drawn past its own cell wins: Heracross' Attack box is a column wider than the eighty its `AnimData.xml` declares.
- **Read a frame through the description, never by arithmetic on the grid.** `frame * frameWidth` is wrong: two frames of a clip are different sizes and sit in different places, and the picture may be somewhere another clip put it.
- **A mirrored frame keeps its own place.** `flip` says the picture's pixels are reversed about the picture's own axis; `at` is still measured from the left of the box, and only a caller-requested flip turns it round.
- **Sheets are filed by region.** `public/sprites/pokemon/{region}/{species}` — `kanto` and `johto` for the first 251 and their forms, `unknown` for Missingno, the egg and the substitute. Which region a pokemon is in comes from its dex number ([`getSpeciesRegion`](../../../src/data/species/regions.ts)), never from a list beside the files; `coats.json` stays at the root and says nothing about regions.
- **Never assume a clip past the ten.** Ask the sprite, `SpeciesSpriteAnimation.has`, rather than keeping a table of which species owns what; a preference list is how a move asks for better and settles for less.
- **A clip the game has no number for does not load.** That is a gap in `SpriteAnim` rather than a bad sheet, and `pnpm import-sprites` says so when it finds one.

## Why

Cropping is most of a sheet, and sharing across clips is most of what is left. A clip's box has to hold its widest lunge, so every quieter frame rattles around inside a box drawn for one reach, and once cropped, two thirds of what remains turns out to be a drawing another clip already has. The 281 sheets that ship weigh 6.3MB, coats and all.

## Importing

```bash
pnpm import-sprites            # from ../SpriteCollab
pnpm import-sprites --dry-run  # say what it would copy
pnpm compact-sprites           # record them, and shrink any PNG that can be
```

[`scripts/import-sprites.ts`](../../../scripts/import-sprites.ts) replaces the tree rather than writing over it, so a pokemon no longer built stops being served. It renames the collection's `{region}/{dex}/{form}` to the species id this game knows it by, skips a form there is no id for, and rewrites `coats.json` with a fresh stamp per pokemon. Without that stamp browsers go on drawing yesterday's sheet against today's description, which draws nothing at all.

Nothing is repacked on the way in. A sheet that needs repacking is repacked in the SpriteCollab checkout and imported again.

## Source art

Pokemon sprites come from **SpriteCollab**, the PMD sprite collection. The working copy is the `SpriteCollab` checkout beside this repository (`../SpriteCollab`), a fork of [PMDCollab/SpriteCollab](https://github.com/PMDCollab/SpriteCollab) at [lxsmnsyc/SpriteCollab](https://github.com/lxsmnsyc/SpriteCollab), with the upstream on the `upstream` remote.

Go there for anything about which sprites exist and what shape they are in: `sprite/{dex}/` per pokemon with its `AnimData.xml` and the three images per animation, `compact/` for what this game reads, `tracker.json` for what is drawn and by whom, `credit_names.txt` for attribution. Read the answer out of that checkout rather than guessing from what is already packed under `public/sprites`, and pull the fork before deciding a sprite is missing.
