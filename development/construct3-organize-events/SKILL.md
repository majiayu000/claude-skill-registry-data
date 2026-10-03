---
name: construct3-organize-events
description: Organize Construct 3 event sheet JSON into professional top-level groups with clear descriptions/comments while preserving original event order and game behavior. Use when Codex needs to clean up .c3proj source eventSheets by grouping setup, gameplay, input, video flow, functions, debug, loader/progress, scene routing, tracing, matching, drag/drop, recording, or other event sections without extracting logic into functions or changing conditions, actions, Else chains, waits, picked-object scope, variables, includes, or existing helper functions.
---

# Construct 3 Organize Events

## Goal

Make Construct 3 event sheets easier to read in the editor by adding clean top-level groups and descriptions. Preserve behavior first; neatness is only useful if the project still runs the same.

## Safe Refactor Rules

- Keep all variables and includes at the top of each event sheet.
- Preserve the relative order of executable events.
- Preserve existing `function-block` events and place them in a `Functions` group if they are not already grouped.
- Preserve every condition, action, child event, `Else`, disabled flag, `isOrBlock`, wait order, and picked-object scope.
- Do not extract action bodies into new functions unless the user explicitly asks for that and accepts behavior risk.
- Do not move a child event out of its parent.
- Do not split an `Else` block away from the event it belongs to.
- Use group `description` fields as comments.
- Keep group names short and practical: `Setup`, `Input`, `Gameplay`, `Video And Scene Flow`, `Functions`, `Debug`, etc.

## Workflow

1. Back up `eventSheets` before editing.
2. Inspect current event-sheet structure and existing groups/functions.
3. Group top-level events only.
4. Name groups based on event conditions, object names, and function names.
5. Validate all JSON files.
6. Count blocks/functions before and after; block and function counts should stay the same.
7. Remind the user to reload/reopen Construct before saving.

## Script

Run from the Construct 3 project root:

```powershell
node C:\Users\Abhinav\.codex\skills\construct3-organize-events\scripts\organize_construct3_events.js --cwd .
```

Dry run:

```powershell
node C:\Users\Abhinav\.codex\skills\construct3-organize-events\scripts\organize_construct3_events.js --cwd . --dry-run
```

The script:

- Reads `eventSheets/*.json`
- Leaves `*.uistate.json` alone
- Leaves variables/includes at the top
- Preserves existing groups
- Wraps ungrouped top-level blocks/functions/scripts into inferred groups
- Adds clear group descriptions
- Avoids extracting functions or rewriting event logic

## Manual Grouping Guidance

Use these common group names:

- `Setup`: `on-start-of-layout`, initial variables, pinning, source setup, initial object state
- `Input`: keyboard, mouse, touch-start, control-mode events
- `Gameplay`: main interactive events when no domain-specific name is obvious
- `Drag And Drop`: `on-drag-start`, `on-drop`, drag-drop activity logic
- `Matching Activity`: connector lines, pair checks, matching cards/texts
- `Tracing`: checkpoints, touch dots, tracing phase/state
- `Recording Controls`: microphone, recording, playback buttons
- `Video And Scene Flow`: video playback, pause, ended, scene transition, narration hooks
- `Progress UI`: loader/progress bar and loading text updates
- `Scene Layer Routing`: shared layer visibility and scene switching helpers
- `Functions`: existing function blocks
- `Debug`: logs and temporary diagnostic events

Prefer project-specific group names when obvious, e.g. `Butterfly Activity`, `Grapes Activity`, `Feather Activity`.

## Validation Commands

Parse all project JSON:

```powershell
@'
const fs=require("fs"), path=require("path");
const files=["project.c3proj"];
for (const dir of ["eventSheets","layouts","families","objectTypes","timelines","flowcharts"]) {
  if (!fs.existsSync(dir)) continue;
  for (const f of fs.readdirSync(dir)) if (f.endsWith(".json")) files.push(path.join(dir,f));
}
for (const f of files) JSON.parse(fs.readFileSync(f,"utf8"));
console.log(`Parsed ${files.length} JSON files successfully.`);
'@ | node -
```

Count event structures:

```powershell
@'
const fs=require("fs"), path=require("path");
for(const f of fs.readdirSync("eventSheets").filter(x=>x.endsWith(".json")&&!x.includes("uistate"))){
  const d=JSON.parse(fs.readFileSync(path.join("eventSheets",f),"utf8"));
  let blocks=0, funcs=0, vars=0, includes=0, groups=0;
  function walk(e){ if(Array.isArray(e)) return e.forEach(walk); if(!e||typeof e!=="object") return;
    if(e.eventType==="block") blocks++;
    if(e.eventType==="function-block") funcs++;
    if(e.eventType==="variable") vars++;
    if(e.eventType==="include") includes++;
    if(e.eventType==="group") groups++;
    for(const v of Object.values(e)) walk(v);
  }
  walk(d.events||[]);
  console.log(`${f}: blocks=${blocks}, funcs=${funcs}, vars=${vars}, includes=${includes}, groups=${groups}`);
}
'@ | node -
```
