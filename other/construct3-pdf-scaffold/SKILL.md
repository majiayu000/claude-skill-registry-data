---
name: construct3-pdf-scaffold
description: Create a new Construct 3 source project scaffold from a PDF story/activity document using the bundled goat project as the default template and the local pdf skill for PDF reading/rendering. Use when Codex needs to inspect a PDF, identify how many scenes/activities it contains, create matching L_SceneN layouts and ES_SceneN event sheets, preserve/copy universal MainLayout, GlobalSheet, Loader, Loader_BG, UI, Video, Overlay, shared objects/assets, adjust MainLayout SceneN layer hierarchy, adjust GlobalSheet includes and total scene count, and add common per-scene event sheet structure such as scene state variables, Setup, Gameplay, Video And Scene Flow, Functions, and example trigger-once scene-state blocks.
---

# Construct 3 PDF Scaffold

## Purpose

Use this skill to turn a story/activity PDF into a Construct 3 project shell that follows the current project conventions:

- `MainLayout`
- `GlobalSheet`
- `Loader`
- `L_Scene1`, `L_Scene2`, ...
- `ES_Scene1`, `ES_Scene2`, ...
- parent layers named `Scene1`, `Scene2`, ...
- scene-specific child/global layers such as `S1_Game`, `S2_Game`, `S2_Activity`
- common layers `Video`, `UI`, `Overlay`, `Loader_BG`

The skill creates the scaffold. It does not invent complete game logic for every PDF activity unless the user asks for implementation after the scaffold.

## Required Inputs

- PDF path
- Output folder path
- Optional template Construct 3 project folder path

By default, use the bundled goat template at `assets/goat-template`. Only pass a custom template folder when the user explicitly asks to use a different base project.

## Workflow

1. Back up or leave the template untouched.
2. Use the local `$pdf` skill to inspect the PDF and identify scene count and activity names.
3. Create a `scene-plan.json`.
4. Run `scripts/scaffold_from_template.js`.
5. Validate JSON.
6. Inspect generated `MainLayout`, `GlobalSheet`, and every `ES_SceneN`.
7. Tell the user to open the new project in Construct and preview the Loader/MainLayout first.

## PDF Scene Analysis

Use `$pdf` first when the user provides a PDF. Read `C:\Users\Abhinav\.codex\skills\pdf\SKILL.md` if it is available, then follow its workflow:

- Extract text with `pdfplumber` or `pypdf` for quick scene/story/activity identification.
- Render pages to PNG with `pdftoppm` when layout, screenshots, activity cards, image placement, or visual sequence matters.
- Inspect rendered pages before finalizing the scene count if the PDF has visual activities or weak text extraction.
- Keep temporary PDF extraction/rendering files under `tmp/pdfs/` or another clear temp folder, and remove them when they are no longer needed.
- If PDF dependencies are missing, install or use the `$pdf` fallback guidance before guessing scene count.

Extract enough text or page images from the PDF to identify:

- story/video sections
- interactive activity sections
- repeated scene headings
- per-scene game/activity labels

If the PDF has explicit scene headings, use them. If it only has pages, infer one scene per clear activity/story beat and include a short note in the final answer.

Do not build `scene-plan.json` from filename alone. Use extracted text and, when needed, rendered page images so the plan reflects the actual PDF.

Scene plan format:

```json
{
  "projectName": "New Construct 3 Project Name",
  "scenes": [
    {
      "title": "Intro",
      "layers": ["S1_Game"],
      "notes": "Opening story scene"
    },
    {
      "title": "Color Activity",
      "layers": ["S2_Game", "S2_ColorActivity"],
      "notes": "Interactive color matching activity"
    }
  ]
}
```

Layer rules:

- Always include at least `S{n}_Game`.
- Always include `S1_StartUI` for Scene 1 and preserve its `startbtn` instance from the bundled goat template.
- Add PDF-specific activity layers as `S{n}_ActivityName`, e.g. `S3_TracingActivity`, `S4_Read`, `S5_MatchingActivity`.
- Use concise Construct-safe names: letters, digits, and underscores.
- Keep scene layer names unique.

## Scaffold Script

Run:

```powershell
node C:\Users\Abhinav\.codex\skills\construct3-pdf-scaffold\scripts\scaffold_from_template.js --out "C:\path\to\empty-output-folder" --scene-plan "C:\path\to\scene-plan.json"
```

Optional:

```powershell
node ...\scaffold_from_template.js --out ..\NewC3Project --scenes 6 --project-name "My New C3 Game"
node ...\scaffold_from_template.js --template "C:\path\to\other-template-project" --out ..\NewC3Project --scenes 6
```

The script:

- Copies the bundled goat template project folder to the output folder unless `--template` is provided
- Keeps shared images/assets and icons
- Prunes unused template object types and families after generation
- Keeps object types that are placed in generated layouts, plus object types/families directly referenced by generated event sheets so Construct events remain valid
- Prunes unused template scripts, sounds, music, and videos from both `project.c3proj` and the physical project folders
- Keeps only media referenced by generated event sheets/layouts, such as shared star reward audio and preserved video sources
- Preserves MainLayout common layers exactly, including their existing object instances
- Preserves the first scene layout's common/global `Video`, `UI`, and `Overlay` layers with their instances
- Rebuilds `project.c3proj` layout and event sheet lists
- Rebuilds `layouts/MainLayout.json` scene parent layers
- Creates `layouts/L_SceneN.json` for each scene
- Creates `eventSheets/ES_SceneN.json` for each scene
- Copies `GlobalSheet.json` and adjusts includes to the generated scenes plus `Loader`
- Updates `SetSceneLayersActive` total scene count when present
- Keeps `Loader.json` intact

## Per-Scene Event Sheet Standard

Each generated scene sheet should include:

- `include GlobalSheet`
- a scene state variable:
  - Scene 1: `sceneState`
  - Scene N: `sceneNState`
- `Setup` group
  - `System: On start of layout`
  - set scene state to `0`
- `Gameplay` group
  - Scene 1 includes an enabled start-button block:
    - `Touch: On touched startbtn`
    - inverted `Video: Is playing`
    - `currentScene = 1`
    - request fullscreen with stretch letterbox scale
    - reset and play `Video`
    - hide and disable `S1_StartUI`
    - show `UI`
    - play `bright garden music` looping at `-10 dB`
    - set `progress` animation frame to `currentStars`
  - placeholder `scene state = 2` + `Trigger once while true` example
  - browser log or harmless placeholder action
- `Video And Scene Flow` group
  - `Video: On can play through`
  - `Video: Is playing` + `currentScene = N`
  - `Video: On ended` + `Trigger once while true`
  - disabled by default so the user can enable or replace the placeholder video flow intentionally
- `Functions` group, initially empty unless the scene needs helper functions

These examples are scaffolding only. Keep them easy to replace.

## MainLayout Standard

MainLayout must include:

- `Video`
- `Scene1` through `SceneN` parent layers
- each parent layer has the scene-specific child layers from the plan
- `UI`
- `Overlay`
- `Loader_BG`

Copy `Video`, `UI`, `Overlay`, and `Loader_BG` from the template MainLayout as full layers, with instances intact. This is required for shared UI such as star holders, progress UI, retry/next buttons, arrow prompts, loading visuals, overlay visuals, and any other universal helper objects already placed in MainLayout. Do not rebuild these layers from empty names unless the template layer is missing.

For `Scene1`, make the parent visible only when it matches the template convention; generally scene parents start invisible and are activated by `SetSceneLayersActive`.

## Common Object Preservation

The goat template stores some universal objects on `L_Scene1` global/common layers rather than directly on MainLayout. Preserve these too:

- `L_Scene1` `Video`: keep the video object and global layer settings when present.
- `L_Scene1` `UI`: keep stars, star holders, progress, retry/next controls, and other shared UI instances exactly as placed.
- `L_Scene1` `Overlay`: keep fade/overlay objects exactly as placed.
- `L_Scene1` `S1_StartUI`: keep the start button layer and its `startbtn` object exactly as placed.

For later generated scene layouts, create matching empty common layers unless the template convention requires otherwise. Do not duplicate shared UI instances into every scene layout; keep the template's global-layer ownership pattern so Construct can manage the shared objects cleanly. After generation, remove unused template object types and families so scene-specific leftovers such as old template activity objects do not remain in the project unless they are actually placed or referenced by generated event sheets.

## GlobalSheet And Loader Standard

GlobalSheet:

- Include every generated `ES_SceneN`
- Include `Loader`
- Preserve shared variables and functions from the template
- Update any hardcoded total scene count in `SetSceneLayersActive`
- Keep star, retry, scene routing, and video-layer routing logic from the template
- Keep only the sound/music files directly referenced by retained shared event logic

Loader:

- Copy exactly from the template unless the user asks to change loader visuals
- Preserve `Loader_BG`, loading progress, video-ready transition, and first-scene startup behavior

Project files:

- Remove unused template `scripts`, `sounds`, `music`, and `videos` files after generated layouts and event sheets are written.
- Keep video files referenced by generated layout video object properties such as `primary-source` or `secondary-source`.
- Keep audio files referenced by generated event sheet `Audio` actions.
- Remove template JavaScript project files unless generated layouts/event sheets explicitly reference them.
- Do not prune `images` or `icons` in this pass because retained object types and app metadata may reference them indirectly.

## Validation

Always parse all generated JSON:

```powershell
@'
const fs=require("fs"), path=require("path");
const files=["project.c3proj"];
function addJsonFiles(dir) {
  if (!fs.existsSync(dir)) return;
  for (const f of fs.readdirSync(dir)) {
    const full = path.join(dir, f);
    if (fs.statSync(full).isDirectory()) addJsonFiles(full);
    else if (f.endsWith(".json")) files.push(full);
  }
}
for (const dir of ["layouts","eventSheets","objectTypes","families","timelines","flowcharts"]) {
  addJsonFiles(dir);
}
for (const f of files) JSON.parse(fs.readFileSync(f,"utf8"));
console.log(`Parsed ${files.length} JSON files successfully.`);
'@ | node -
```

Then verify:

- `project.c3proj` lists all `L_SceneN`
- `project.c3proj` lists all `ES_SceneN`
- `GlobalSheet.json` includes all scene event sheets and `Loader`
- `MainLayout.json` has `Scene1..SceneN`
- `MainLayout.json` common layers `Video`, `UI`, `Overlay`, and `Loader_BG` have the same object instances as the template
- generated `L_Scene1.json` common/global layers `Video`, `UI`, and `Overlay` keep the same shared object instances as template `L_Scene1`
- each `L_SceneN.json` uses `ES_SceneN`
- `project.c3proj` object type lists contain only generated-layout object types plus event-sheet-only runtime dependencies such as `Audio`, `Browser`, or `Touch`
- unused template families are removed; retained families contain only retained object type members unless the family itself is explicitly referenced by generated event logic
- `project.c3proj` `rootFileFolders.script`, `sound`, `music`, and `video` lists contain only files referenced by generated layouts/event sheets
- physical `scripts`, `sounds`, `music`, and `videos` folders contain no unused template files
- no stale references to removed scene numbers remain

## Safety Notes

- Do not overwrite the bundled template project.
- The output folder may be missing or empty. If it exists and contains files, stop instead of merging into it.
- Do not delete template assets unless the user asks for cleanup.
- Do not generate detailed activity logic from guesses; scaffold first, then implement scene logic in a separate pass.
- If the PDF scene count is ambiguous, create a scene plan and explain the inference before running the script.
