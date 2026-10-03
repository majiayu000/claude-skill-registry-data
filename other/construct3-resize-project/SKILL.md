---
name: construct3-resize-project
description: Resize and scale Construct 3 project source folders, especially converting layouts and viewport from one 16:9 resolution to another such as 1920x1080 to 1280x720. Use when Codex needs to migrate .c3proj source projects by scaling layout dimensions, world object positions/sizes, text sizes, particle values, Sine magnitudes, hardcoded event-sheet coordinates, tween position/size/scale values, set-position/set-size/create-object values, and simple JavaScript pixel speeds while preserving IDs, pair/state variables, timing, opacity, audio, and image asset dimensions.
---

# Construct 3 Resize Project

## Workflow

Use this skill for Construct 3 source-folder projects, not exported web builds. Prefer the bundled script for the mechanical migration, then inspect suspicious leftovers manually.

1. Confirm the source and target resolutions. For a proportional 16:9 resize, use one scale factor:
   - `1280 / 1920 = 720 / 1080 = 2/3`
2. Create a backup before editing:
   - `Compress-Archive -Path project.c3proj,layouts,eventSheets,scripts -DestinationPath construct3-resize-backup.zip -Force`
3. Run `scripts/resize_construct3_project.js` from the project root.
4. Validate all JSON files parse.
5. Search for old hardcoded values and inspect every remaining hit.
6. Tell the user to reload/reopen Construct before saving, because the editor can overwrite external JSON edits from memory.

## Script

Run:

```powershell
node C:\Users\Abhinav\.codex\skills\construct3-resize-project\scripts\resize_construct3_project.js --from 1920x1080 --to 1280x720 --cwd .
```

Useful flags:

```powershell
node ...\resize_construct3_project.js --from 1920x1080 --to 1280x720 --cwd . --dry-run
node ...\resize_construct3_project.js --from 1920x1080 --to 1280x720 --cwd . --script-speed scripts\guideHand.js:HAND_SPEED
```

The script scales:

- `project.c3proj` `viewportWidth` and `viewportHeight`
- every runtime `layouts/*.json` layout `width` and `height`
- instance `world.x`, `world.y`, `world.width`, `world.height`
- text size and text margins
- particle size/speed/randomiser pixel values
- Sine behavior `magnitude` and `magnitude-random`
- event-sheet spatial constants for `create-object`, `set-position`, `pick-overlapping-point`, `pick-nearestfurthest`, `set-size`, `set-width`, `set-height`, `set-scale`, `set-magnitude`, Tween `position`, Tween `size`, Tween `scale`, Tween `offsetX/offsetY`
- simple JavaScript constants named through `--script-speed`, e.g. `const HAND_SPEED = 400;`

The script intentionally does not scale:

- UID/SID values
- pair IDs, indexes, state numbers, counters
- times, wait durations, playback rates
- opacity, volume, stereo pan
- sprite animation frame asset dimensions in `objectTypes`
- layout editor `.uistate.json` view positions, unless the user specifically asks for editor-state cleanup

## Manual Checks

After running the script, search for old resolution anchors:

```powershell
rg -n -g "!*.uistate.json" "\b1920\b|\b1080\b|\b960\b|\b540\b" project.c3proj layouts eventSheets scripts
```

Remaining hits can be valid, but inspect each one:

- A remaining `960,540` in runtime logic may need to become `640,360`.
- A remaining `1024` in `objectTypes/*.json` usually is an image asset frame size and should stay unchanged.
- Expressions like `LayoutWidth/2` and `LayoutHeight/2` are already relative and should stay unchanged.
- Expressions like `ImageCard.X + 20` should scale only the pixel offset, becoming `ImageCard.X + 13.333333`.

## Safety Rules

- Keep a backup zip before any migration.
- Do not scale project IDs, object SIDs, instance UIDs, function parameters used as IDs, or event state values.
- Do not delete assets or object types as part of resizing.
- If the project is open in Construct, warn the user to reload before saving.
- For non-proportional changes, stop and ask whether to use independent X/Y scaling or preserve aspect ratio with letterboxing.
