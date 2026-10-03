---
name: construct3-pdf-scaffold-v2
description: Create a Construct 3 source project scaffold from a PDF story/activity document using the bundled updated Letter G V2 template. Use when Antigravity needs to inspect a PDF, identify scene/activity count, generate scene-plan.json, create L_SceneN layouts and ES_SceneN event sheets, preserve updated LetterG universal systems including GlobalSheet, Loader, Continue save/resume flow, currentProgress star system, stars.js, Scene 1 start UI, shared UI/video/overlay layers, audio, effects, and required object types.
---

# Construct 3 PDF Scaffold V2

## Purpose

Use this skill to turn a PDF story/activity document into a Construct 3 source project scaffold using the updated Letter G base project. The scaffold creates the project shell and preserves the universal runtime systems; it does not invent full custom activity logic unless the user asks for that after scaffolding.

Default template: `assets/letterg-v2-template`.

## Workflow

1. Use the local `pdf` skill first when a PDF is provided. Read `C:\Users\Abhinav\.gemini\config\skills\pdf\SKILL.md`, extract text, and render pages when visuals affect scene/activity count.
2. Identify scenes, story beats, and activities from the PDF. Do not infer scene count from filename alone.
3. Create a `scene-plan.json` with `projectName` and `scenes`.
4. Run `scripts/scaffold_from_template.js`.
5. Parse all generated Construct JSON and verify the V2 universal systems survived.
6. Tell the user to open the generated source project in Construct and preview `Loader`/`MainLayout` first.

## Scene Plan

Use this shape:

```json
{
  "projectName": "New Construct 3 Project",
  "scenes": [
    {
      "title": "Intro",
      "layers": ["S1_Game"],
      "notes": "Opening story scene"
    },
    {
      "title": "Tracing Activity",
      "layers": ["S2_Game", "S2_TracingActivity"],
      "notes": "Interactive tracing activity"
    }
  ]
}
```

Layer rules:

- Always include `S{n}_Game`.
- Always include `S1_StartUI` for Scene 1; the script preserves V2 `startbg`, `startbtn`, and `Continue`.
- Add activity layers as `S{n}_ActivityName`, for example `S3_MatchingActivity`, `S4_TracingActivity`, or `S5_Read`.
- Use Construct-safe names: letters, digits, and underscores only.

## Scaffold Script

Run:

```powershell
node C:\Users\Abhinav\.gemini\config\skills\construct3-pdf-scaffold-v2\scripts\scaffold_from_template.js --out "C:\path\to\empty-output-folder" --scene-plan "C:\path\to\scene-plan.json"
```

Optional:

```powershell
node ...\scaffold_from_template.js --out "C:\path\to\out" --scenes 6 --project-name "My Project"
node ...\scaffold_from_template.js --template "C:\custom\ConstructProject" --out "C:\path\to\out" --scene-plan "C:\path\scene-plan.json"
```

The script refuses to merge into a non-empty output folder. It copies the V2 template, deletes generated scene layouts/sheets, rebuilds scene lists, updates `GlobalSheet` includes and hardcoded total scene count, writes generated scene layouts/sheets, prunes unused non-universal object types/media/scripts, and writes `scene-plan.generated.json`.

## V2 Universal Systems To Preserve

Read `references/letterg-v2-conventions.md` when changing the script or debugging generated output.

Always preserve:

- `MainLayout`, `GlobalSheet`, `Loader`, `Loader_BG`, `Video`, `UI`, and `Overlay`.
- `L_Scene1` global/common layers: `frame`, `Video`, `UI`, `Overlay`, and `S1_StartUI`.
- Scene 1 start UI objects: `startbg`, `startbtn`, and `Continue`.
- Continue/save variables and flow: `currentProgress`, `currentStars`, `ContinueVideoTime`, `checkOnPlayed`, and `gameOVer`.
- New progress/star system: `scripts/stars.js`, `DoStarIncrement(runtime)`, `star2`, `starTrail`, `starsHolder`, `progress`, `3starProgress`, `starpanel`, and related effects.
- Runtime/plugin object types used by universal systems: `LocalStorage`, `Array`, `Audio`, `Browser`, `Touch`, `Video`, `Continue`, `ClickVFX`, `Retry`, `startbg`, `startbtn`, `starTrail`, `star2`, `starsHolder`, `progress`, `3starProgress`, and `starpanel`.
- Universal audio/video: `bright garden music`, `starsound`, `whoosh 1`, `whoosh 2`, `snap`, `snap place`, `star`, `You got a star!`, `You got one more star!`, `FX01 1`, `FX02 1`, `FX03 1`, `FX04 1`, and the template video.

## Generated Scene Event Sheets

Each generated `ES_SceneN` should include:

- `include GlobalSheet`
- Scene state variable: `sceneState` for Scene 1, `sceneNState` for later scenes
- `Setup`
- `Gameplay`
- `Video And Scene Flow`
- `Functions`

For Scene 1, the generated gameplay start block must use the V2 flow: request fullscreen, reset/play `Video`, show `UI`, hide and disable `S1_StartUI`, play `bright garden music`, and set `progress` frame from `currentProgress` instead of the old `currentStars`-only behavior. It must also include the `Continue` button touch handler block to load checkpoint information from `localStorage`, map progress/stars/time configurations, set current scene routing, restore star milestones, and resume video playback.

For activity completion in later implementation passes, prefer calling `DoStarIncrement(runtime)` from `stars.js` for progress completion instead of manually incrementing only `currentStars`.

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
for (const dir of ["layouts","eventSheets","objectTypes","families","timelines","flowcharts"]) addJsonFiles(dir);
for (const f of files) JSON.parse(fs.readFileSync(f,"utf8"));
console.log(`Parsed ${files.length} JSON files successfully.`);
'@ | node -
```

Then verify:

- `project.c3proj` lists exactly generated `L_SceneN` and `ES_SceneN`, plus `MainLayout`, `GlobalSheet`, and `Loader`.
- `GlobalSheet.json` includes every generated scene sheet plus `Loader`.
- `MainLayout.json` has `Video`, `Scene1..SceneN`, `UI`, `Overlay`, and `Loader_BG`.
- `L_Scene1.json` retains `frame`, `Video`, `UI`, `Overlay`, and `S1_StartUI` instances.
- `Continue`, `LocalStorage`, `Array`, `starTrail`, `3starProgress`, `ClickVFX`, and `stars.js` remain after pruning.
- Required universal sounds/music/video remain listed in `project.c3proj` and physically present.
- No stale scene layout or event sheet files above the generated scene count remain.

## Safety

Do not overwrite `assets/letterg-v2-template`. Do not delete template assets unless the user explicitly requests template maintenance. Keep PDF extraction/rendering temp files outside the generated Construct project unless the user asks to include them.
