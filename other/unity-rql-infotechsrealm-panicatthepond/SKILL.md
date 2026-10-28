---
name: unity-rql
description: |-
  How to read and change anything in the Unity Editor with RQL (rql-query / rql-mutate / rql-schema): the query
  language, operators, sources (scene objects, assets, scenes, prefabs, console logs, Editor state), Editor operations
  (create, add components, scenes, prefabs, assets, selection, Play Mode) and what installed extensions add.
metadata:
  generated-by: unity-mcp
  ai-game-dev: exclude
---
# RQL — query and change the Unity Editor

RQL is one pipeline language for the whole Editor: find objects, read members, filter, aggregate, and change them in one
call. Prefer one precise query over many exploratory calls.

- `rql-query` — read-only queries, compact table results.
- `rql-mutate` — queries ending with `set` / `call`; all-or-nothing, undoable (Ctrl+Z), `dry_run: true` previews.
- `rql-schema` — sources and component types in the scene; `rql-schema(type)` lists one type's members and methods.

```bash
unity-mcp-cli run-tool rql-query --input '{"query": "objects | where name contains \"Enemy\" | select $ref name"}'
unity-mcp-cli run-tool rql-mutate --input '{"query": "objects | where name == \"Player\" | set active = false"}'
```

## Language

```
RQL: source | stage | stage ...
Sources: objects (every GameObject in the loaded scenes, inactive included), roots, scenes, selection, prefab (the prefab open in prefab editing mode), console (Editor log entries), shaders, componentTypes, profiler (memory / rendering / frame snapshots; call Start / Stop / Save), tests (test methods; run a selection with tests-run query), testResults (last run), editor (Editor state and operations). Assets: unity.assets("t:Material") or unity.assets("t:Prefab", "Assets/Enemies"), unity.asset("Assets/Mats/Red.mat"). ref("Light#1234") resolves a $ref; unity.find("Player") or unity.find("Level/Pillar_1") a GameObject by unique name or path.
Stages:
  where <predicate>                  filter
  select a b.c alias=(expr)          project columns (wrap computed expressions in parentheses)
  sort <expr> [desc], ...            stable sort
  first N | skip N | count
  get <path>                         replace each item by a member (lists are flattened)
  recurse children [max-depth=N] [include-self=false]   walk the hierarchy (input items included by default)
  distinct [expr] | group-by expr | sum expr | min expr | max expr | avg expr
Expressions: == != < <= > >= and or not + - * / %; contains, starts-with, ends-with (case-insensitive); matches "regex"; x in [a, b]; x is null; x is not null; $ is Light (includes subclasses); has(member). Literals: numbers, "strings", true/false/null, lists [a, b], objects {x: 1, y: 2}.
Paths: a.b.c, list[0], map["key"]; .member on a list maps over its elements. List methods: .any(pred) .all(pred) .count([pred]) .sum(e) .min(e) .max(e) .first([pred]); inside them bare names refer to the element, falling back to the outer item.
Meta: $ (current item), $ref (stable id such as Light#1234), $type, $path, $index, $depth. Enums compare to strings (type == "Spot"); == on strings is case-sensitive.
Unity: GameObject has components (list), children (list), active, name, tag, layer, transform (position, localPosition, eulerAngles, localScale, parent). Component members are the C# members (public + [SerializeField]); find them via objects | get components | where $ is Light. Vectors/colors print as (x, y, z); write "(1, 2, 3)", [1, 2, 3] or {x: 1, y: 2, z: 3}; colors also "#ff8800". Material shader properties: properties["_Color"]. Destroyed objects read as null (missing references: where target == null). Navigate with paths or get; select only projects output columns.
Results come back as compact rows (header line, then col|col). Long results are truncated — refine with where/first or use count. Unknown members produce warnings with suggestions; rql-schema(type) lists a type's members.
```

## Changing things (rql-mutate)

```
  set path = expr, ...   assign members (paths may go through structs: set transform.position.y = transform.position.y + 1)
  call Method(args)      invoke a method the tools expose
Examples:
  objects | where name == "Player" | set transform.position = "(0, 1, 0)"
  objects | get components | where $ is Light | set intensity = intensity * 2, color = "#ffcc88"
  objects | where tag == "Enemy" | set active = false
  unity.asset("Assets/Mats/Red.mat") | set properties["_Color"] = "(1, 0, 0, 1)"
  objects | where name == "Spawner" | set targets = append(targets, ref("GameObject#1234"))
Create / add / remove (call; the receipt's result column holds the new object's $ref for follow-up queries):
  editor | call CreateGameObject("Props")                                   new root GameObject
  editor | call CreateGameObject("Crate", ref("GameObject#1234"), "Cube")    child of a parent, optional primitive
  objects | where name == "Crate" | call AddComponent("Rigidbody")           add a component by type name
  objects | where name == "Old" | call Destroy()                             remove a GameObject (components: get components | where $ is X | call Destroy())
  objects | where name == "Lamp" | set transform.parent = ref("GameObject#1234")   reparent (keeps the world position)
  objects | where name == "Crate" | call Duplicate()                          copy next to it (returns the copy)
Scenes, prefabs, assets, Editor state:
  editor | call OpenScene("Assets/Scenes/Level.unity")          editor | call NewScene("Assets/Scenes/New.unity")
  scenes | where path == "" | call SaveAs("Assets/Scenes/New.unity")   scenes | where name == "Level" | call SetActive()
  editor | call InstantiatePrefab("Assets/Prefabs/Enemy.prefab", ref("GameObject#1234"), "(0, 0, 5)")
  objects | where name == "Crate" | call SaveAsPrefab("Assets/Prefabs/Crate.prefab")
  editor | call OpenPrefab("Assets/Prefabs/Enemy.prefab")  then  prefab | recurse children | …  then  editor | call ClosePrefab()
  editor | call CreateMaterial("Assets/Mats/Glow.mat")        editor | call MoveAsset("Assets/A.mat", "Assets/Mats/A.mat")
  editor | set selection = [ref("GameObject#1234")]         editor | set isPlaying = true
  profiler | call Start()      profiler | call Save("Logs/profile.json")      (read: profiler | select memory frame)
```

## Sources

| Source | What |
|---|---|
| `animation` | animation: animators (every Animator in the loaded scenes), CreateClip(path, frameRate, loop), CreateController(path, motion) |
| `cinemachine` | Cinemachine: cameras, brains, noiseProfiles, bodyTypes / aimTypes / extensionTypes; CreateCamera(name, follow, lookAt, position, eulerAngles, priority), EnsureBrain(camera) |
| `componentTypes` | component types that can be added (name fullName namespace) |
| `console` | captured Editor log entries, oldest first (last 1000): logType message timestamp stackTrace sequence |
| `editor` | Editor state (isPlaying, isPaused, selection …) and operations: CreateGameObject, OpenScene, NewScene, SaveScenes, InstantiatePrefab, OpenPrefab / SavePrefab / ClosePrefab, CopyAsset / MoveAsset / DeleteAsset / CreateFolder, CreateMaterial, SaveAssets, RefreshAssets, ClearConsole, ExecuteMenuItem (rql-schema "editor" for signatures) |
| `input` | Input System: assets (.inputactions), layouts, interactions, processors; CreateAsset(path, map?) |
| `lighting` | the active scene's lighting: environment (ambient, fog, skybox, sun), Lighting Settings asset, bake (rql-schema "lighting" for members and calls) |
| `navigation` | AI Navigation project settings and operations: agentTypes (bake settings, writable), areas (name, cost), BakeAll(), ClearAll() |
| `objects` | every GameObject in the loaded scenes, depth-first, inactive ones included |
| `prefab` | root GameObject of the prefab open in prefab editing mode (none otherwise) |
| `probuilder` | ProBuilder: meshes (every ProBuilderMesh in the loaded scenes), CreateShape(type, name, size, position, rotation, parent), CreatePolyShape(points, height, name, position, flipNormals, parent), Merge(meshes, deleteSources) |
| `profiler` | Unity profiler: enabled supported memory rendering script frame modules (live snapshots, MB / ms); calls Start, Stop, ClearFrames, EnableModule, Save, Load (rql-schema "profiler" for signatures) |
| `roots` | root GameObjects of the loaded scenes |
| `scenes` | loaded scenes |
| `selection` | objects selected in the Editor |
| `shaders` | every shader the Editor knows (built-in and project): name supported hasErrors |
| `splines` | spline containers of the loaded scenes (containers) and CreateContainer(name, position, eulerAngles, closed, parent) |
| `terrain` | terrain operations without an owner: Create (Terrain GameObject + TerrainData asset), CreateLayer (TerrainLayer asset) |
| `testResults` | results of the last tests-run: name status durationMs message stackTrace |
| `tests` | test methods (fullName name fixture namespace assembly mode categories parameterized explicit ignored); run a selection with tests-run query, e.g. tests \| where fixture == "PlayerTests" |
| `tilemap` | tilemap operations without an owner: CreateTilemap (Grid + Tilemap GameObject), CreateTile, CreateRuleTile (tile assets) |
| `timeline` | timeline operations without an owner: Create (TimelineAsset .playable), CreateSignal (SignalAsset .signal) |
| `probuilder.edges(…)` | probuilder.edges(mesh, faces?): distinct edges [[a, b], …] of the faces (index list; default every face), for Bevel / SubdivideEdges / ConnectEdges |
| `probuilder.facing(…)` | probuilder.facing(mesh, direction): indices of the faces pointing Up, Down, Left, Right, Forward, Back or Other (local space, within 45°) |
| `probuilder.openEdges(…)` | probuilder.openEdges(mesh): border edges [[a, b], …] (a face on one side only: around holes, plane borders), for Bridge |
| `probuilder.vertices(…)` | probuilder.vertices(mesh, start?, count?): [{index, position}] local vertex positions (at most 20 per call; default 0, 20) |
| `terrain.heightAt(…)` | terrain.heightAt(terrain, worldX, worldZ): world-space surface height (Y) at a world X / Z position |
| `terrain.heightStats(…)` | terrain.heightStats(terrain, x?, y?, w?, h?): {min, max, average, cells} of a heightmap region (default: the whole heightmap) |
| `terrain.heights(…)` | terrain.heights(terrain, x, y, w?, h?): normalized heights 0 … 1 of a heightmap region as rows (at most 20 × 20 cells) |
| `tilemap.cell(…)` | tilemap.cell(tilemap, cell): {cell, tile, path, sprite, color, colliderType, flags, transform} of one cell (tile null when empty) |
| `tilemap.cellToWorld(…)` | tilemap.cellToWorld(tilemap, cell): the world position of a cell's center |
| `tilemap.cells(…)` | tilemap.cells(tilemap, tile?): the first 20 occupied cells (optionally of one tile asset, path or name), bottom-left first |
| `tilemap.count(…)` | tilemap.count(tilemap, tile?, minX?, minY?, maxX?, maxY?, z?): occupied cells, optionally of one tile (asset, path or name) and inside a region |
| `tilemap.tileAt(…)` | tilemap.tileAt(tilemap, cell): the tile asset at a cell "(x, y, z)", or null |
| `tilemap.tiles(…)` | tilemap.tiles(tilemap, minX, minY, maxX, maxY, z?): tile names of a region as rows, top row (maxY) first, null = empty (at most 20 × 20) |
| `tilemap.worldToCell(…)` | tilemap.worldToCell(tilemap, "(x, y, z)"): the cell containing a world position |
| `unity.asset(…)` | unity.asset(path): the main asset at a path, e.g. "Assets/Mats/Red.mat" |
| `unity.assets(…)` | unity.assets(filter, folder?): AssetDatabase search, e.g. "t:Material", "t:Prefab Enemy" (at most 200, loaded as needed) |
| `unity.find(…)` | unity.find(name): the GameObject with that unique name or hierarchy path ("Level/Pillar_1"), e.g. set Follow = unity.find("Player") |

## Animation

Clips and controllers are assets: `unity.assets("t:AnimationClip")`, `unity.asset("Assets/…/Walk.anim")`,
`unity.asset("Assets/…/Player.controller")`. An AnimationClip has `curves` (path type property keyCount timeRange keys, keys with
writable time value inTangent outTangent …), `objectCurves` (sprite swaps), `events` and `settings` (loopTime loopBlend mirror …), all
writable views, plus ordinary members (frameRate wrapMode legacy length isLooping). An AnimatorController has `layers` (name
defaultWeight blendingMode defaultState `states` anyStateTransitions) and `parameters` (name type defaultFloat defaultInt defaultBool);
states and transitions are assets whose members (speed motion tag … / hasExitTime exitTime duration conditions …) are set directly.
Writes and calls are undoable; creating an asset is not. `rql-schema "AnimationClip"` / `"AnimatorController"` list the methods.

Clips (curve `path` is the child path under the Animator, "" = its own GameObject; `type` the animated component):

```
animation | call CreateClip("Assets/Animations/Walk.anim")   empty clip, 60 fps
animation | call CreateClip("Assets/Animations/Idle.anim", 30, true)   path, frameRate, loop
unity.assets("t:AnimationClip") | select name length frameRate isLooping n=(curves.count()) e=(events.count())
unity.asset("Assets/Animations/Walk.anim") | call SetCurve("", "Transform", "localPosition.y", [[0, 0], [0.5, 1], [1, 0]])   path, type, property, keys [time, value(, inTangent, outTangent)]
unity.asset("Assets/Animations/Walk.anim") | call SetCurve("Body", "SpriteRenderer", "m_Color.a", [{time: 0, value: 1}, {time: 1, value: 0, inTangent: -1}])
unity.asset("Assets/Animations/Walk.anim") | get curves | select path type property keyCount timeRange
unity.asset("Assets/Animations/Walk.anim") | get curves | where property == "localPosition.y" | get keys | select index time value inTangent outTangent
unity.asset("Assets/Animations/Walk.anim") | get curves | where property == "localPosition.y" | set keys[1].value = 2, keys[1].outTangent = 0
unity.asset("Assets/Animations/Walk.anim") | get curves | where property == "localPosition.y" | call AddKey(1.5, 0.5)   returns the key index; RemoveKey(index), SetKeys([[t, v], …]), Evaluate(t)
unity.asset("Assets/Animations/Walk.anim") | get curves | where path == "Body" | set postWrapMode = "Loop"
unity.asset("Assets/Animations/Walk.anim") | call RemoveCurve("Body", "SpriteRenderer", "m_Color.a")   or … | get curves | where … | call Remove()
unity.asset("Assets/Animations/Walk.anim") | set frameRate = 30, settings.loopTime = true
unity.asset("Assets/Animations/Walk.anim") | call AddEvent(0.5, "Footstep", "left")   time, functionName, stringParameter?, floatParameter?, intParameter?
unity.asset("Assets/Animations/Walk.anim") | get events | select index time functionName stringParameter
unity.asset("Assets/Animations/Walk.anim") | set events[0].time = 0.25, events[0].intParameter = 1
unity.asset("Assets/Animations/Walk.anim") | call RemoveEvent(0)   ClearEvents() / ClearCurves() remove all
```

Animator controllers (states by name; a trailing `layer` argument is a layer name or index, default 0):

```
animation | call CreateController("Assets/Animations/Player.controller")   Base Layer, empty state machine (CreateController(path, motion) adds a state)
unity.asset("Assets/Animations/Player.controller") | call AddParameter("Speed", "Float")   Float, Int, Bool or Trigger
unity.asset("Assets/Animations/Player.controller") | call AddParameter("Grounded", "Bool", true)   optional default value
unity.asset("Assets/Animations/Player.controller") | call AddParameter("Jump", "Trigger")
unity.asset("Assets/Animations/Player.controller") | call AddState("Idle", unity.asset("Assets/Animations/Idle.anim"))   name, motion?, layer?; the first state becomes the default
unity.asset("Assets/Animations/Player.controller") | call AddState("Walk", unity.asset("Assets/Animations/Walk.anim"))
unity.asset("Assets/Animations/Player.controller") | call AddTransition("Idle", "Walk", "Speed", "Greater", 0.1)   from, to ("Exit" = exit), parameter?, mode?, threshold?, layer?
unity.asset("Assets/Animations/Player.controller") | call AddTransition("Walk", "Idle", "Speed", "Less", 0.1)
unity.asset("Assets/Animations/Player.controller") | call AddAnyStateTransition("Idle", "Jump")   mode defaults by parameter type: Bool / Trigger If, Float Greater, Int Equals
unity.asset("Assets/Animations/Player.controller") | call SetDefaultState("Idle")
unity.asset("Assets/Animations/Player.controller") | get layers | select index name defaultWeight defaultState.name states.name
unity.asset("Assets/Animations/Player.controller") | get layers | get states | select name speed motion.name transitions.destinationState.name
unity.asset("Assets/Animations/Player.controller") | get layers | get states | where name == "Walk" | set speed = 1.5
unity.asset("Assets/Animations/Player.controller") | get layers | get states | where name == "Idle" | get transitions | set hasExitTime = true, exitTime = 0.9, duration = 0.25
unity.asset("Assets/Animations/Player.controller") | get layers | get states | where name == "Idle" | get transitions | call AddCondition("Grounded", "If")   RemoveCondition(index), ClearConditions()
unity.asset("Assets/Animations/Player.controller") | get layers | get states | get transitions | select destinationState.name hasExitTime conditions
unity.asset("Assets/Animations/Player.controller") | get parameters | select name type defaultFloat defaultBool
unity.asset("Assets/Animations/Player.controller") | get parameters | where name == "Speed" | set defaultFloat = 0.5
unity.asset("Assets/Animations/Player.controller") | call AddLayer("Upper Body")   returns the layer index
unity.asset("Assets/Animations/Player.controller") | set layers[1].defaultWeight = 0.5, layers[1].blendingMode = "Additive"
unity.asset("Assets/Animations/Player.controller") | call AddState("Wave", null, "Upper Body")
unity.asset("Assets/Animations/Player.controller") | call RemoveTransition("Walk", "Idle")   from "AnyState" / to "Exit" for those transitions
unity.asset("Assets/Animations/Player.controller") | call RemoveState("Wave", "Upper Body")
unity.asset("Assets/Animations/Player.controller") | call RemoveLayer("Upper Body")
unity.asset("Assets/Animations/Player.controller") | call RemoveTransition("AnyState", "Idle")
unity.asset("Assets/Animations/Player.controller") | call RemoveParameter("Jump")   conditions using it are removed too
```

Animator components (`animation | get animators` = every Animator in the loaded scenes):

```
editor | call CreateGameObject("Player")
objects | where name == "Player" | call AddComponent("Animator")
animation | get animators | set runtimeAnimatorController = unity.asset("Assets/Animations/Player.controller"), applyRootMotion = false
animation | get animators | select gameObject.name runtimeAnimatorController.name isHuman cullingMode
```

Parameter names and types are read-only (conditions refer to them): rename by RemoveParameter + AddParameter. New transitions
have no exit time and no blend duration; set them on the transition. Only the Animator's configuration members are readable (its
playback state is not meaningful in Edit Mode); in Play Mode `call SetParameter("Speed", 2)` / `call Play("Walk")` drive it.
Other components' AnimationCurve fields take keyframe lists too: `set curve = [[0, 0], [1, 1]]`.

## Cinemachine

Cinemachine 3: a `CinemachineCamera` (virtual camera) on its own GameObject; the `CinemachineBrain` on the Unity Camera
shows the live one (highest `Priority.Value`) and blends between them. A camera's pipeline is a Body component
(position: Follow, OrbitalFollow, ThirdPersonFollow, PositionComposer …), an Aim component (rotation: RotationComposer,
HardLookAt, PanTilt …), an optional noise component and extensions, all on the camera's GameObject. Follow / LookAt
targets take a GameObject name or ref. Writes and calls are undoable.

```
editor | call CreateGameObject("Player", null, "Capsule")   (a target for the examples)
cinemachine | call CreateCamera("FollowCam", "Player", null, "(0, 3, -6)", "(20, 0, 0)", 10)   name, follow?, lookAt?, position?, eulerAngles?, priority? (adds a CinemachineBrain to the main Camera)
cinemachine | call CreateCamera("Overview")
cinemachine | get cameras | select name Priority.Value IsLive Follow.name LookAt.name body.$type aim.$type noise.$type
cinemachine | get cameras | where name == "FollowCam" | call SetBody("Follow")   Body by name; cinemachine | get bodyTypes lists them ("None" removes)
cinemachine | get cameras | where name == "FollowCam" | call SetAim("RotationComposer")   Aim by name; cinemachine | get aimTypes
cinemachine | get cameras | where name == "FollowCam" | set body.FollowOffset = "(0, 2, -8)", body.TrackerSettings.PositionDamping = "(1, 1, 1)"
cinemachine | get cameras | where name == "FollowCam" | set aim.Composition.ScreenPosition = "(0.1, 0)", aim.Damping = "(0.5, 0.5)"
cinemachine | get cameras | where name == "FollowCam" | set Lens.FieldOfView = 50, Lens.NearClipPlane = 0.3, Lens.Dutch = 5
cinemachine | get cameras | where name == "Overview" | set Lens.ModeOverride = "Orthographic", Lens.OrthographicSize = 12
cinemachine | get cameras | where name == "FollowCam" | set Priority.Value = 20
cinemachine | get cameras | where name == "Overview" | call SetTargets("Player")   follow (and look at) Player; SetTargets(follow, lookAt) for both, null clears
cinemachine | get cameras | where name == "Overview" | set LookAt = null
cinemachine | get cameras | where name == "FollowCam" | call SetNoise("Handheld_normal_mild", 1.5, 1)   profile, amplitudeGain?, frequencyGain?; cinemachine | get noiseProfiles | select name
cinemachine | get cameras | where name == "FollowCam" | set noise.AmplitudeGain = 0.5
cinemachine | get cameras | where name == "FollowCam" | call SetBody("OrbitalFollow")   replace the Body
cinemachine | get cameras | where name == "FollowCam" | set body.Radius = 6, body.OrbitStyle = "Sphere"
objects | where name == "FollowCam" | call AddComponent("CinemachineDeoccluder")   extensions are components (cinemachine | get extensionTypes)
cinemachine | get cameras | select name extensions.$type
cinemachine | call EnsureBrain()   brain on the main Camera (EnsureBrain("Camera name") for another)
cinemachine | get brains | set DefaultBlend.Style = "EaseInOut", DefaultBlend.Time = 1.5
cinemachine | get brains | select gameObject.name DefaultBlend.Style DefaultBlend.Time UpdateMethod activeCamera
cinemachine | get cameras | where name == "Overview" | call SetNoise("None")
cinemachine | get cameras | where name == "Overview" | call Destroy()   remove the CinemachineCamera component (objects | … | call Destroy() removes the GameObject)
```

`body` / `aim` / `noise` are the pipeline components themselves, so their members are written directly
(`rql-schema "CinemachineFollow"` lists them). LensSettings is a struct written in place (`set Lens.FieldOfView = …`);
`Lens.ModeOverride` (None, Orthographic, Perspective, Physical) overrides the Unity Camera's projection. Blend styles:
Cut, EaseInOut, EaseIn, EaseOut, HardIn, HardOut, Linear, Custom. Brains update the live camera in Play Mode; `IsLive`
reports it.

## Input System

An InputActionAsset (`.inputactions` file) has `maps` → `actions` → `bindings` and `controlSchemes`; `actions` also lists
every action of every map. Every `set` and `call` is validated (control paths need a known device layout, interactions /
processors / composites must be registered, groups must be control schemes of the asset), written to the `.inputactions`
file and re-imported at once, and is undoable. Paths look like `"<Keyboard>/space"`, `"<Gamepad>/leftStick"`,
`"<Mouse>/leftButton"`; groups are scheme names joined by `;` (`"Keyboard&Mouse;Gamepad"`).

```
input | call CreateAsset("Assets/Input/Player.inputactions", "Player")   path, map? (first action map); missing folders are created
input | get assets | select $ref name path
unity.asset("Assets/Input/Player.inputactions") | call AddControlScheme("Keyboard&Mouse", ["<Keyboard>", "<Mouse>"])   name, requiredDevices?, optionalDevices?, bindingGroup? (default: name)
unity.asset("Assets/Input/Player.inputactions") | call AddControlScheme("Gamepad", ["<Gamepad>"])
unity.asset("Assets/Input/Player.inputactions") | call AddMap("UI")
unity.asset("Assets/Input/Player.inputactions") | get maps | where name == "Player" | call AddAction("Jump")   name, type? (Button, Value, PassThrough), expectedControlType?, binding?
unity.asset("Assets/Input/Player.inputactions") | get maps | where name == "Player" | call AddAction("Move", "Value", "Vector2")
unity.asset("Assets/Input/Player.inputactions") | get actions | where name == "Jump" | call AddBinding("<Keyboard>/space", "Keyboard&Mouse")   path, groups?, interactions?, processors?
unity.asset("Assets/Input/Player.inputactions") | get actions | where name == "Jump" | call AddBinding("<Gamepad>/buttonSouth", "Gamepad", "hold(duration=0.4)")
unity.asset("Assets/Input/Player.inputactions") | get actions | where name == "Move" | call AddComposite("2DVector", {up: "<Keyboard>/w", down: "<Keyboard>/s", left: "<Keyboard>/a", right: "<Keyboard>/d"}, "Keyboard&Mouse")   composite, {part: path}, groups?, interactions?, processors?
unity.asset("Assets/Input/Player.inputactions") | get actions | where name == "Move" | call AddBinding("<Gamepad>/leftStick", "Gamepad", null, "stickDeadzone")
unity.asset("Assets/Input/Player.inputactions") | get maps | select name actionCount
unity.asset("Assets/Input/Player.inputactions") | get actions | select map name type expectedControlType interactions bindingCount
unity.asset("Assets/Input/Player.inputactions") | get actions | get bindings | select action index path name groups interactions processors isComposite isPartOfComposite
unity.asset("Assets/Input/Player.inputactions") | get controlSchemes | select name bindingGroup requiredDevices optionalDevices
unity.asset("Assets/Input/Player.inputactions") | get actions | get bindings | where path == "<Gamepad>/buttonSouth" | set path = "<Gamepad>/buttonEast", interactions = "tap"
unity.asset("Assets/Input/Player.inputactions") | get actions | get bindings | where isPartOfComposite and name == "up" | set path = "<Keyboard>/upArrow"
unity.asset("Assets/Input/Player.inputactions") | get actions | where name == "Jump" | set name = "Leap", type = "PassThrough", interactions = "press"
unity.asset("Assets/Input/Player.inputactions") | get actions | where name == "Move" | set processors = "invertVector2", initialStateCheck = true
unity.asset("Assets/Input/Player.inputactions") | get controlSchemes | where name == "Keyboard&Mouse" | set requiredDevices = ["<Keyboard>"], optionalDevices = ["<Mouse>"]
unity.asset("Assets/Input/Player.inputactions") | get controlSchemes | where name == "Gamepad" | set name = "Controller"   also renames the group of its bindings
unity.asset("Assets/Input/Player.inputactions") | get maps | where name == "Player" | set name = "Gameplay"
unity.asset("Assets/Input/Player.inputactions") | get actions | get bindings | where groups == "Controller" | call Remove()   a composite root removes its parts
unity.asset("Assets/Input/Player.inputactions") | get actions | where name == "Leap" | call Remove()
unity.asset("Assets/Input/Player.inputactions") | get controlSchemes | where name == "Controller" | call Remove()
unity.asset("Assets/Input/Player.inputactions") | get maps | where name == "UI" | call Remove()
input | select interactions processors   registered names; input | get layouts lists device and control layouts
```

Assets referenced by a scene component work the same way: `objects | get components | where $ is PlayerInput | get actions | get maps`.
Bindings are addressed by id, so removing some bindings in one query does not shift the others. `call` needs rql-mutate.
Created assets are not removed by Undo; undoing an edit rewrites the file.

## Navigation

AI Navigation components are components: `objects | get components | where $ is NavMeshSurface` (also NavMeshModifier,
NavMeshModifierVolume, NavMeshLink, NavMeshAgent). Add them with AddComponent, then set members (all undoable):

```
objects | where name == "Ground" | call AddComponent("NavMeshSurface")
objects | get components | where $ is NavMeshSurface | set collectObjects = "Volume", size = "(20, 5, 20)", center = "(0, 1, 0)"
objects | get components | where $ is NavMeshSurface | set agentType = "Humanoid", defaultAreaName = "Walkable", layerMask = ["Default", "Water"]
objects | get components | where $ is NavMeshSurface | set overrideVoxelSize = true, voxelSize = 0.1
objects | get components | where $ is NavMeshSurface | call Bake()          build now (saved scene: NavMesh-<name>.asset next to it)
objects | get components | where $ is NavMeshSurface | call Clear()         remove the baked data
objects | get components | where $ is NavMeshSurface | select gameObject.name agentType navMeshData buildSettings.agentRadius
navigation | call BakeAll()                                                   every active surface (also ClearAll())
```

Modifiers, volumes, links:

```
objects | where name == "Water" | call AddComponent("NavMeshModifier")
objects | get components | where $ is NavMeshModifier | set overrideArea = true, areaName = "Not Walkable"
objects | get components | where $ is NavMeshModifier | set ignoreFromBuild = true, applyToChildren = false, affectedAgents = ["All"]
objects | where name == "Mud" | call AddComponent("NavMeshModifierVolume")
objects | get components | where $ is NavMeshModifierVolume | set size = "(4, 2, 4)", center = "(0, 1, 0)", areaName = "Jump"
objects | where name == "Gap" | call AddComponent("NavMeshLink")
objects | get components | where $ is NavMeshLink | set startPoint = "(0, 0, -2)", endPoint = "(0, 1, 3)", width = 1, bidirectional = false, costModifier = 2, areaName = "Jump"
```

Agents (`SetDestination` / `Warp` / `ResetPath` act only on an agent on a baked NavMesh, i.e. in Play Mode; they return false otherwise):

```
objects | where name == "Enemy" | call AddComponent("NavMeshAgent")
objects | get components | where $ is NavMeshAgent | set speed = 5, acceleration = 12, angularSpeed = 240, stoppingDistance = 0.5
objects | get components | where $ is NavMeshAgent | set agentType = "Humanoid", areaNames = ["Walkable", "Jump"]   area mask; ["All"] = every area
objects | get components | where $ is NavMeshAgent | call SetDestination("(10, 0, 5)")
objects | get components | where $ is NavMeshAgent | select gameObject.name isOnNavMesh hasPath remainingDistance
```

Bake settings live on the agent type (shared by every surface baking for it; rebake afterwards); areas name the area indices:

```
navigation | get agentTypes | select agentTypeID name agentRadius agentHeight agentSlope agentClimb
navigation | get agentTypes | where name == "Humanoid" | set agentRadius = 0.4, agentHeight = 1.8, agentSlope = 40, agentClimb = 0.5
navigation | get areas | where name != "" | select index name cost
navigation | get areas | where index == 3 | set name = "Water", cost = 4
```

`agentType`, `areaName` / `defaultAreaName`, `areaNames` and `affectedAgents` are the name views of agentTypeID, area /
defaultArea, areaMask and the agent-type list; the numeric members stay writable. A LayerMask reads as its int mask and takes an
int (-1 = Everything), a layer name or a list of layer names.

## Particle systems

Particle systems are components: `objects | get components | where $ is ParticleSystem`. Module structs (`main`,
`emission`, `shape` …) are written through, even though they are get-only properties:

```
objects | get components | where $ is ParticleSystem | set main.startLifetime = 3, main.loop = false
objects | get components | where $ is ParticleSystem | set emission.rateOverTime = [5, 25]          random between two
objects | get components | where $ is ParticleSystem | set main.startColor = "#ff8800"
objects | get components | where $ is ParticleSystem | set main.startColor = [["#ff0000", 0], ["#0000ff", 1]]   gradient
```

`MinMaxCurve` takes a number or `[min, max]`; `MinMaxGradient` a color, `[color, color]` or gradient keys.
Playback in the Editor: `objects | get components | where $ is ParticleSystem | call Play()` (also Pause, Stop, Clear,
Simulate(seconds)).

## ProBuilder

ProBuilder meshes are components: `probuilder | get meshes` (= `objects | get components | where $ is ProBuilderMesh`). A mesh
reads as faceCount vertexCount edgeCount triangleCount, `bounds` (local) / `worldBounds`, `directions` (face indices per local
direction), `materials` (slots: index material faceCount) and `faces` (read-only views: index direction center normal
submeshIndex material vertices edges); the raw vertex arrays are not members. Edit with `call` (rql-mutate): faces are index lists
`[0, 1]`, edges vertex index pairs `[[0, 1], [1, 2]]`. `probuilder.facing($, "Up")`, `probuilder.edges($, faces?)`,
`probuilder.openEdges($)` and `probuilder.vertices($, start?, count?)` compute selections (also as call arguments). The receipt's
result column holds the created mesh's $ref: `ref("ProBuilderMesh#…") | call Extrude([0], 1)`.

Create and inspect:

```
probuilder | call CreateShape("Cube", "Crate", "(2, 1, 2)", "(0, 0.5, 0)")   type, name?, size?, position?, rotation?, parent?
probuilder | call CreateShape("Cube", "Box", null, "(3, 0.5, 0)")   types: Cube Stair CurvedStair Prism Cylinder Plane Door Pipe Cone Sprite Arch Sphere Torus
probuilder | call CreateShape("Cylinder", "Block", "(1, 2, 1)", "(6, 1, 0)")
probuilder | call CreatePolyShape(["(0, 0)", "(4, 0)", "(4, 3)", "(0, 3)"], 0.5, "Floor", "(-6, 0, 0)")   points (x, z), height, name?, position?, flipNormals?, parent?
probuilder | get meshes | select $ref gameObject.name faceCount vertexCount edgeCount triangleCount bounds.size
probuilder | get meshes | where gameObject.name == "Crate" | select directions materials worldBounds.center
probuilder | get meshes | where gameObject.name == "Crate" | get faces | select index direction center normal vertexCount submeshIndex material.name
probuilder | get meshes | where gameObject.name == "Crate" | get faces | where direction == "Up" | select index center edges
probuilder | get meshes | where gameObject.name == "Crate" | select up=(probuilder.facing($, "Up")) edges=(probuilder.edges($, [0])) v=(probuilder.vertices($, 0, 4))
```

Faces (indices shift after DeleteFaces; Extrude appends the new side faces and returns their indices):

```
editor | call CreateMaterial("Assets/Materials/Grass.mat")
probuilder | get meshes | where gameObject.name == "Crate" | call SetFaceMaterial(probuilder.facing($, "Up"), "Assets/Materials/Grass.mat")   faces, material (path, unity.asset(…) or ref); returns the submesh index
probuilder | get meshes | where gameObject.name == "Crate" | get materials | select index material.name faceCount
probuilder | get meshes | where gameObject.name == "Crate" | call Extrude(probuilder.facing($, "Up"), 0.5)   faces, distance (negative = inward), method? FaceNormal | IndividualFaces | VertexNormal
probuilder | get meshes | where gameObject.name == "Crate" | call Extrude(probuilder.facing($, "Forward"), 0.25, "IndividualFaces")
probuilder | get meshes | where gameObject.name == "Crate" | call FlipNormals([0])   faces? (every face when omitted)
probuilder | get meshes | where gameObject.name == "Box" | call DeleteFaces(probuilder.facing($, "Up"))   at least one face must remain
probuilder | get meshes | where gameObject.name == "Box" | select open=(probuilder.openEdges($))
probuilder | get meshes | where gameObject.name == "Box" | call Bridge(probuilder.openEdges($)[0], probuilder.openEdges($)[2])   two open edges [a, b], allowNonManifold?; returns the new face index
```

Edges, pivot, merge:

```
probuilder | get meshes | where gameObject.name == "Block" | call Bevel(probuilder.edges($, probuilder.facing($, "Down")), 0.1)   edges, amount 0 … 1 (exclusive); returns the new face indices
probuilder | get meshes | where gameObject.name == "Block" | call SubdivideEdges(probuilder.edges($, [0]), 1)   edges, subdivisions (1 = split in half); returns the vertices added
probuilder | get meshes | where gameObject.name == "Block" | call ConnectEdges(probuilder.edges($, [1]))   at least 2 edges sharing faces; returns the new face indices
probuilder | get meshes | where gameObject.name == "Floor" | call SetPivot("Center")   "Center" (bounds) or "FirstVertex"; the geometry stays in place
probuilder | get meshes | where gameObject.name == "Floor" | call SetPivotAt("(-6, 0, 0)")   a world position
probuilder | call Merge([meshes.first(gameObject.name == "Crate"), meshes.first(gameObject.name == "Box")])   refs to meshes or GameObjects (first = target), deleteSources? (default true)
```

Directions are in the mesh's local space (normal within 45° of the axis; the rest is Other). Invalid indices, edges that are not
edges of the mesh, amounts outside the range and deleting every face fail without changing anything. Every call is undoable
(the mesh is rebuilt after Undo / Redo); a created material asset stays.

## Splines

A `SplineContainer` component holds splines; `splines[i]` has `closed`, `knotCount`, `length` (world units) and
`knots[j]` with writable `position` (container-local), `worldPosition`, `tangentIn`, `tangentOut`, `eulerAngles`,
`tangentMode` (AutoSmooth, Linear, Mirrored, Continuous, Broken) and `tension`. The `splines` source lists every
container (`splines | get containers`) and creates new ones. Writes and calls are undoable. `rql-schema "SplineContainer"`
lists the methods; `… | get splines | get knots | first 1 | describe` lists the knot members.

```
splines | call CreateContainer("Road")   new GameObject + SplineContainer (one empty spline)
splines | call CreateContainer("Loop", "(0, 0, 5)", "(0, 90, 0)", true)   name, position, eulerAngles, closed
splines | get containers | select gameObject.name n=(splines.count()) splines.knotCount
objects | get components | where $ is SplineContainer | where gameObject.name == "Road" | call AddKnots(["(0, 0, 0)", "(5, 0, 2)", "(10, 0, 0)"])   append several knots to spline 0
objects | get components | where $ is SplineContainer | where gameObject.name == "Road" | call AddKnot("(15, 0, 3)")   append one knot to spline 0
objects | get components | where $ is SplineContainer | where gameObject.name == "Road" | call AddSpline()   returns the new spline index
objects | get components | where $ is SplineContainer | where gameObject.name == "Road" | call AddKnot(1, "(0, 2, 0)")   append to spline 1
objects | get components | where $ is SplineContainer | where gameObject.name == "Road" | call InsertKnot(1, "(2, 0, 1)")   insert at knot index 1 (InsertKnot(spline, knot, position) for others)
objects | get components | where $ is SplineContainer | where gameObject.name == "Road" | call RemoveKnot(0)   RemoveKnot(spline, knot) for other splines
objects | get components | where $ is SplineContainer | where gameObject.name == "Road" | call Evaluate(0.5)   point at t: position (world) localPosition tangent up
objects | get components | where $ is SplineContainer | where gameObject.name == "Road" | get splines | get knots | select index position tangentMode
objects | get components | where $ is SplineContainer | where gameObject.name == "Road" | set splines[0].knots[2].position = "(10, 1, 0)"   move a knot (container-local)
objects | get components | where $ is SplineContainer | where gameObject.name == "Road" | set splines[0].knots[0].tangentMode = "Linear"
objects | get components | where $ is SplineContainer | where gameObject.name == "Road" | get splines | get knots | set tangentMode = "AutoSmooth"   every knot of every spline
objects | get components | where $ is SplineContainer | where gameObject.name == "Road" | set splines[0].closed = true
objects | get components | where $ is SplineContainer | where gameObject.name == "Road" | call RemoveSpline(1)
```

Knot methods take an optional leading spline index (`AddKnot(position)` = spline 0, `AddKnot(1, position)` = spline 1);
new knots are AutoSmooth. Writing a tangent of an AutoSmooth / Linear knot switches it to Broken so the value sticks.
Evaluate needs rql-mutate (it is a call); its result column holds the sample. Unity.Mathematics `float2` / `float3` /
`float4` / `quaternion` values print and are written like vectors: `"(1, 2, 3)"`; a quaternion also accepts euler
degrees `"(0, 90, 0)"`.

## Terrain

Terrains are components: `objects | get components | where $ is Terrain`. Settings are members of the Terrain, the data
(size, resolutions, layers, prototypes) lives in its `terrainData`. Heights are normalized 0 … 1 (fraction of
`terrainData.size.y`); heightmap / alphamap cells are `x` along world X and `y` along world Z.

```
objects | get components | where $ is Terrain | select $ref gameObject.name terrainData.size terrainData.heightmapResolution terrainData.terrainLayers.name
terrain | call Create("Island", "Assets/Terrain/Island.asset", 257, "(500, 120, 500)", "(0, 0, 0)")   name, dataPath, heightmapResolution, size, position
objects | get components | where $ is Terrain | set terrainData.size = "(800, 200, 800)"
objects | get components | where $ is Terrain | set terrainData.heightmapResolution = 513, terrainData.alphamapResolution = 512
objects | get components | where $ is Terrain | set heightmapPixelError = 2, drawTreesAndFoliage = false, materialTemplate = unity.asset("Assets/Mats/Terrain.mat")
```

Heights (`call` needs rql-mutate; sampling functions work in rql-query):

```
objects | get components | where $ is Terrain | call SetHeights(0.25)                                  flatten everything to 25 %
objects | get components | where $ is Terrain | call SetHeights(0.6, 100, 100, 32, 32)                 height, x, y, w, h (w / h 0 = to the edge)
objects | get components | where $ is Terrain | call SetHeightGrid([[0.1, 0.2], [0.3, 0.4]], 10, 20)    explicit rows (row = y) starting at cell (10, 20)
objects | get components | where $ is Terrain | select h=(terrain.heights($, 10, 20, 2, 2))            normalized rows, at most 20 × 20
objects | get components | where $ is Terrain | select s=(terrain.heightStats($))                       {min, max, average, cells}; region: ($, x, y, w, h)
objects | get components | where $ is Terrain | select y=(terrain.heightAt($, 250, 250))                world surface Y at world X / Z
```

Layers (textures), trees and details:

```
terrain | call CreateLayer("Assets/Terrain/Grass.terrainlayer", unity.asset("Assets/Textures/grass.png"), "(10, 10)")
objects | get components | where $ is Terrain | call AddLayer(unity.asset("Assets/Terrain/Grass.terrainlayer"))   returns the layer index
objects | get components | where $ is Terrain | call PaintLayer(1, 1.0, 0, 0, 64, 64)                  layer, strength, x, y, w, h on the alphamap
objects | get components | where $ is Terrain | call RemoveLayer(0)
objects | get components | where $ is Terrain | set terrainData.terrainLayers[0].tileSize = "(20, 20)"
objects | get components | where $ is Terrain | call AddTreePrototype(unity.asset("Assets/Trees/Oak.prefab"))    returns the prototype index
objects | get components | where $ is Terrain | call PlaceTrees(0, 200, 0.1, 0.1, 0.5, 0.5)            prototype, count, minX, minZ, maxX, maxZ (normalized), heightScale?, widthScale?
objects | get components | where $ is Terrain | call PlaceTreesAt(["(0.5, 0.5)", "(0.25, 0.75)"], 0)     normalized (x, z) positions, prototype
objects | get components | where $ is Terrain | call ClearTrees()
objects | get components | where $ is Terrain | select terrainData.treeInstanceCount terrainData.treePrototypes.prefab
objects | get components | where $ is Terrain | set terrainData.treePrototypes[0] = {prefab: unity.asset("Assets/Trees/Oak.prefab"), bendFactor: 0.3}   prototypes are replaced whole
objects | get components | where $ is Terrain | set terrainData.treeInstances[0].heightScale = 2
objects | get components | where $ is Terrain | call AddDetailPrototype(unity.asset("Assets/Textures/grass_blade.png"))   texture = grass billboard, prefab = detail mesh
objects | get components | where $ is Terrain | get terrainData | call SetDetailResolution(1024, 32)
objects | get components | where $ is Terrain | where gameObject.name == "Center" | call SetNeighbors(ref("Terrain#…"), null, ref("Terrain#…"), null)   left, top, right, bottom
```

`terrainData.treeInstances` is read only when named (`select terrainData.treeInstances[0]`). Tree / detail prototype
members are read-only (TerrainData returns copies): replace the element with an object literal. Invalid resolutions, regions
outside the map and out-of-range indices fail without changing anything. Heights, paint, layers and trees are undoable;
created assets (TerrainData, TerrainLayer) are not removed by Undo. Neighbors are not saved with the scene (Unity
reconnects terrains with `allowAutoConnect` and the same `groupingID`).

## Tilemap

Tilemaps are components on children of a `Grid`: `objects | get components | where $ is Tilemap`. Cells are `"(x, y, z)"` (z = 0 for 2D);
tile arguments take an asset path (`"Assets/Tiles/Grass.asset"`), a ref or `unity.asset(…)`; sprite arguments also take
the texture (`unity.asset("Assets/Art/grass.png")`), its path or `"Assets/Art/sheet.png#grass_3"` (one sprite of a sheet).

```
objects | get components | where $ is Tilemap | select $ref gameObject.name tileCount usedTiles cellBounds orientation
tilemap | call CreateTilemap("Ground")                                    name, parent?, cellSize?, gridName? (new Grid + Tilemap)
tilemap | call CreateTilemap("Walls", ref("GameObject#…"))                  parent with a Grid: another layer of that Grid
tilemap | call CreateTile("Assets/Tiles/Grass.asset", "Assets/Art/grass.png", "#FFFFFF", "Grid")   path, sprite?, color?, colliderType?
tilemap | call CreateRuleTile("Assets/Tiles/Ground.asset", "Assets/Art/ground.png#ground_4")        path, defaultSprite?, colliderType?
```

Painting (`call` needs rql-mutate; undoable):

```
objects | get components | where $ is Tilemap | where gameObject.name == "Ground" | call SetTile("(0, 0, 0)", "Assets/Tiles/Grass.asset")
objects | get components | where $ is Tilemap | call SetTile("(3, 1, 0)", null)                                erase one cell
objects | get components | where $ is Tilemap | call SetTiles(["(0, 0, 0)", "(1, 0, 0)", "(2, 0, 0)"], "Assets/Tiles/Grass.asset")
objects | get components | where $ is Tilemap | call BoxFill("Assets/Tiles/Grass.asset", -5, -3, 5, 3)          tile, minX, minY, maxX, maxY, z? (corners inclusive)
objects | get components | where $ is Tilemap | call ClearBox(0, 0, 2, 2)                                       returns how many tiles were removed
objects | get components | where $ is Tilemap | call FloodFill("(1, 1, 0)", "Assets/Tiles/Water.asset")
objects | get components | where $ is Tilemap | call ClearAllTiles()
objects | get components | where $ is Tilemap | call SetColor("(0, 0, 0)", "#FF8080")                           tint one painted cell
objects | get components | where $ is Tilemap | call SetTransform("(0, 0, 0)", 90, "(1, 1, 1)", true, false)     rotation°, scale?, flipX?, flipY?
objects | get components | where $ is Tilemap | call SetColliderType("(0, 0, 0)", "None")                       None / Sprite / Grid
objects | get components | where $ is Tilemap | set orientation = "XZ", tileAnchor = "(0.5, 0.5, 0)", color = "(1, 1, 1, 0.5)"
objects | get components | where $ is Tilemap | call CompressBounds()                                           shrink cellBounds to the painted cells
objects | get components | where $ is Grid | set cellSize = "(1, 0.5, 0)", cellLayout = "Isometric"
objects | get components | where $ is TilemapRenderer | set sortingOrder = 2, mode = "Individual"
```

Reading cells (functions work in rql-query):

```
objects | get components | where $ is Tilemap | select t=(tilemap.tileAt($, "(0, 0, 0)"))                     the tile asset or null
objects | get components | where $ is Tilemap | select c=(tilemap.cell($, "(0, 0, 0)"))                        {cell, tile, path, sprite, color, colliderType, flags, transform}
objects | get components | where $ is Tilemap | select rows=(tilemap.tiles($, 0, 0, 9, 9))                       tile names, top row (maxY) first, at most 20 × 20
objects | get components | where $ is Tilemap | select n=(tilemap.count($, "Grass"))                            occupied cells of a tile (name, path or asset); region: ($, tile, minX, minY, maxX, maxY)
objects | get components | where $ is Tilemap | select cells=(tilemap.cells($, "Assets/Tiles/Grass.asset"))      first 20 cells holding that tile
objects | get components | where $ is Tilemap | select c=(tilemap.worldToCell($, "(2.5, 1.2, 0)")) w=(tilemap.cellToWorld($, "(2, 1, 0)"))
```

Tile assets are ordinary objects: `unity.assets("t:TileBase") | select $ref name`,
`unity.asset("Assets/Tiles/Grass.asset") | set sprite = "Assets/Art/grass2.png", colliderType = "Grid"`. RuleTile rules:

```
unity.asset("Assets/Tiles/Ground.asset") | call AddRule("Assets/Art/ground.png#ground_1", "NNN/T.T/TTT")   sprite, pattern, colliderType?
unity.asset("Assets/Tiles/Ground.asset") | call ClearRules()
objects | get components | where $ is Tilemap | call RefreshAllTiles()                                          repaint after editing rules
```

A pattern lists the 8 neighbors in rows top to bottom (center ignored): `T` = this tile, `N` = not this tile, `.` = any;
rules are checked in order and the first match wins (`"..."` = always). Methods on empty cells (SetColor, SetTransform,
SetColliderType), regions over 1 048 576 cells and bad paths fail without changing anything. `cellBounds.max` is exclusive.
Created assets are not removed by Undo.

## Timeline

A TimelineAsset (`.playable`) holds tracks; tracks hold clips and markers; a scene `PlayableDirector` plays it and binds
each track to a scene object. Times are seconds. Find timelines with `unity.assets("t:TimelineAsset")`.

```
unity.assets("t:TimelineAsset") | select $ref name duration frameRate tracks.name
unity.asset("Assets/Cutscenes/Intro.playable") | get tracks | select $ref name $type bindingType muted clips.count() markers.count()
unity.asset("Assets/Cutscenes/Intro.playable") | get tracks | recurse children | select $depth name $type              groups and their sub-tracks
unity.asset("Assets/Cutscenes/Intro.playable") | get tracks | get clips | select track.name displayName start duration end asset.name
timeline | call Create("Assets/Cutscenes/Intro.playable", 30)                 path, frameRate?, fixedDuration? (> 0 = FixedLength)
unity.asset("Assets/Cutscenes/Intro.playable") | set frameRate = 24, durationMode = "FixedLength", fixedDuration = 12
```

Tracks (type: Animation, Activation, Audio, Signal, Control, Playable, Group or a TrackAsset type name):

```
unity.asset("Assets/Cutscenes/Intro.playable") | call AddTrack("Animation", "Hero")                 type, name?, group? — returns the track
unity.asset("Assets/Cutscenes/Intro.playable") | call AddTrack("Group", "Crowd")
unity.asset("Assets/Cutscenes/Intro.playable") | call AddTrack("Activation", "Door", "Crowd")       nested in the GroupTrack named Crowd
unity.asset("Assets/Cutscenes/Intro.playable") | get tracks | where name == "Hero" | set muted = true, locked = false, name = "Hero Anim"
unity.asset("Assets/Cutscenes/Intro.playable") | get tracks | where name == "Door" | call Delete()        with its clips, markers and sub-tracks
```

Clips (AnimationTrack: an AnimationClip, AudioTrack: an AudioClip, other tracks: a default clip with asset null):

```
unity.asset("Assets/Cutscenes/Intro.playable") | get tracks | where name == "Hero" | call AddClip(unity.asset("Assets/Anim/Walk.anim"), 2, 3, "Walk")   asset?, start?, duration?, name?
unity.asset("Assets/Cutscenes/Intro.playable") | get tracks | where name == "Door" | call AddClip(null, 0, 1.5)
unity.asset("Assets/Cutscenes/Intro.playable") | get tracks | get clips | where displayName == "Walk" | set start = start + 0.5          move (duration kept)
unity.asset("Assets/Cutscenes/Intro.playable") | get tracks | get clips | where displayName == "Walk" | set duration = 4, clipIn = 0.25, timeScale = 1.5, easeInDuration = 0.5, easeOutDuration = 0.3
unity.asset("Assets/Cutscenes/Intro.playable") | get tracks | get clips | where displayName == "Walk" | set asset.removeStartOffset = false   the clip's PlayableAsset
unity.asset("Assets/Cutscenes/Intro.playable") | get tracks | get clips | where end > 10 | call Delete()
```

Markers and signals:

```
timeline | call CreateSignal("Assets/Cutscenes/Boom.signal")
unity.asset("Assets/Cutscenes/Intro.playable") | call AddMarker(3.5)                                    SignalEmitter on the timeline marker track
unity.asset("Assets/Cutscenes/Intro.playable") | get tracks | where $type == "SignalTrack" | call AddMarker(1, "Signal")
unity.asset("Assets/Cutscenes/Intro.playable") | get markers | set asset = unity.asset("Assets/Cutscenes/Boom.signal"), time = 4
unity.asset("Assets/Cutscenes/Intro.playable") | get tracks | get markers | where time > 8 | call Delete()
```

Director and bindings (a GameObject is narrowed to the component the track drives, e.g. its Animator):

```
objects | where name == "Cutscene" | call AddComponent("PlayableDirector")
objects | get components | where $ is PlayableDirector | where gameObject.name == "Cutscene" | set playableAsset = unity.asset("Assets/Cutscenes/Intro.playable"), playOnAwake = false
objects | get components | where $ is PlayableDirector | select gameObject.name playableAsset.name bindings
objects | get components | where $ is PlayableDirector | set bindings["Hero"] = ref("GameObject#…"), bindings["Door"] = null
```

Crossfades (blendInDuration / blendOutDuration, read-only) come from overlapping clips: move a clip's start into its neighbour.
Invalid values (negative times, eases longer than the clip, a time scale on clips that cannot change speed, a clip asset that does not fit the track, unknown track names)
fail without changing anything; Timeline does not clamp them silently here. Creating, deleting and editing tracks, clips,
markers and bindings is undoable; created asset files stay. rql-mutate saves the edited .playable.
Clips have no $ref: address them through their timeline (`… | get tracks | get clips | where …`).

## Installed RQL modules

- `com.IvanMurzak.Unity.MCP.Editor.Rql.Modules.UnityCoreModule`
- `com.IvanMurzak.Unity.MCP.Editor.Rql.ToolTypesModule`
- `com.IvanMurzak.Unity.MCP.Editor.Rql.Mathematics.MathematicsModule`
- `com.IvanMurzak.Unity.MCP.Editor.Rql.Animation.AnimationModule`
- `com.IvanMurzak.Unity.MCP.Editor.Rql.Cinemachine.CinemachineModule`
- `com.IvanMurzak.Unity.MCP.Editor.Rql.InputSystem.InputSystemModule`
- `com.IvanMurzak.Unity.MCP.Editor.Rql.Lighting.LightingModule`
- `com.IvanMurzak.Unity.MCP.Editor.Rql.Navigation.NavigationModule`
- `com.IvanMurzak.Unity.MCP.Editor.Rql.Particles.ParticleSystemModule`
- `com.IvanMurzak.Unity.MCP.Editor.Rql.Physics3D.PhysicsModule`
- `com.IvanMurzak.Unity.MCP.Editor.Rql.ProBuilder.ProBuilderModule`
- `com.IvanMurzak.Unity.MCP.Editor.Rql.Splines.SplinesModule`
- `com.IvanMurzak.Unity.MCP.Editor.Rql.Terrains.TerrainModule`
- `com.IvanMurzak.Unity.MCP.Editor.Rql.Tilemaps.TilemapModule`
- `com.IvanMurzak.Unity.MCP.Editor.Rql.Timelines.TimelineModule`


> CLI installation and usage: see the `unity-cli` skill.
> If this task needs unavailable asset-generation or Blender tools, consult `ai-game-dev-app` for an optional integrated workflow.

