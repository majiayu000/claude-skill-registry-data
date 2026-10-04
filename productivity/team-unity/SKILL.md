---
name: team-unity
description: "Use when the task touches Unity Editor assets, scenes, prefabs, UI Toolkit, Unity-MCP, Play Mode visuals, Console, screenshots, package/project settings, or when an agent is about to hand-edit .unity/.prefab/.meta YAML. Use when localhost:8080 / ai-game-developer is down or unproven."
argument-hint: "[scene|prefab|ui-toolkit|dots|addressables|shaders|mcp|build-profile|performance|full-feature] [scope] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion
model: sonnet
agent: unity-specialist
---

# Team Unity — Unity Engine / MCP Orchestration

Use this skill when work crosses Unity Editor assets, runtime presentation,
Unity-MCP operations, package configuration, or engine-specific implementation.
It coordinates Unity specialists while enforcing the architecture rule that Unity
Presentation and Adapter code do not leak into pure Data or Simulation assemblies.

## MCP connectivity gate (before any Editor work)

Run this **before** scene/prefab/UXML/Play Mode/screenshot work. Skip only for
pure headless sim/delegation (`dotnet test`, no Unity assets).

```bash
curl -sS -o /dev/null -w "%{http_code}\n" --max-time 3 http://localhost:8080
```

If this clone has not pinned yet: `./tools/pin-unity-mcp-8080.sh` then open
Editor **6000.3.22f1** on `unity/ProjectAegis`. Clients: `.mcp.json`,
`.cursor/mcp.json`, `.grok/config.toml` → `ai-game-developer` at
`http://localhost:8080`.

**HTTP 2xx — Editor MCP live**

1. Discover tools (`ping`, `unity-tool-list`, or `search_tool` query `unity`).
2. Propose scene/prefab/asset mutations; wait for approval on writes.
3. Mutate **only** through Unity-MCP (`scene-*`, `gameobject-*`, `assets-*`).
4. `scene-save` / `assets-prefab-save`.
5. Visual check: `editor-application-set-state` (Play Mode) → `console-get-logs` → `screenshot-game-view`.
6. Stop Play Mode. Report Console errors and the screenshot.

**Connection failed — stay headless**

- Say `:8080` is down. Do not invent Editor tools.
- Use `dotnet test` / PlayModeSmokeHarness / file edits under `src/`.
- Do **not** hand-edit `.unity`, `.prefab`, or `.meta` YAML to change
  hierarchy, GUIDs, or component refs.
- Do **not** call Unity-MCP tools that require a live Editor.

Never mutate `DelegationBridge` via `script-execute`, `script-update-or-create`,
or reflection.

| Excuse | Reality |
|--------|---------|
| "Editor is closed, I'll patch the YAML" | Stay headless or ask to open Editor. Wrong GUIDs break the asset. |
| "It's just one component field" | Use `gameobject-component-modify` when `:8080` is up. |
| "MCP isn't in this session so tools don't exist" | Probe `:8080`. If down, headless. If up, `search_tool` / `unity-tool-list`. |

## Phase 0: Resolve Mode and Review Level

Modes:

- `scene` — scene hierarchy, lighting, cameras, test scenes, play-mode setup.
- `prefab` — prefab structure, variants, component references, and serialization safety.
- `ui-toolkit` — UXML/USS, PanelSettings, runtime UI Toolkit, focus/navigation.
- `dots` — Entities, Burst, Jobs, NativeContainers, ECS world-state presentation.
- `addressables` — asset groups, labels, loading/unloading, memory and catalog strategy.
- `shaders` — Shader Graph, HLSL, VFX Graph, render-pipeline customization.
- `mcp` — Unity-MCP editor operations and real-time editor automation planning.
- `build-profile` — Unity packages, project settings, platforms, build profiles.
- `performance` — Unity Profiler, frame budget, GC, rendering, asset memory.
- `full-feature` — engine architecture → implementation → validation → QA handoff.
- No mode — infer from request; if ambiguous, ask one focused question.

Review mode:
1. If `--review [full|lean|solo]` is present, use it.
2. Else read `production/review-mode.txt` if present.
3. Else default to `lean`.

## Team Composition

- **unity-specialist** — Unity architecture lead and engine API authority.
- **unity-ui-specialist** — UI Toolkit, UXML/USS, UGUI exceptions, input/focus.
- **unity-dots-specialist** — DOTS/ECS, Jobs, Burst, NativeContainers.
- **unity-addressables-specialist** — asset groups, catalogs, async loading, memory lifecycle.
- **unity-shader-specialist** — Shader Graph, HLSL, VFX Graph, render pipeline.
- **technical-artist** — art-to-engine pipeline, import settings, visual optimization.
- **c-sharp-devops-engineer** — Unity batchmode, package/build automation, CI.
- **c-sharp-reviewer / c-sharp-test-engineer** — Unity C# review and test coverage.
- **qa-lead / qa-tester** — play-mode, smoke, and manual QA evidence.

## Phase 1: Load Required Context

Read only relevant context:

- `Tech-Stack.md`, `.mcp.json`, `.cursor/mcp.json`, `.grok/config.toml`, Unity package manifests.
- `docs/engine-reference/unity/VERSION.md` and package-specific notes.
- `docs/architecture/architecture.md` layer rules.
- Unity project paths under `unity/ProjectAegis/**` and adapter code in scope.
- Existing scene, prefab, UXML, USS, shader, material, Addressables, or test assets.

Report the affected Unity subsystem, owning specialists, and required validation.

## Phase 2: Select Workflow Pipeline

### MCP / Editor Pipeline

Follow the **MCP connectivity gate** above. Then:

1. Present planned scene/prefab/asset operations before execution.
2. Require explicit user approval before editor-side mutations.
3. Mutate through Unity-MCP, then save.
4. Close the loop with Console + Game View screenshot when the change is visual.
5. Headless `PlayModeSmokeHarnessTests` still gates C2/delegation — Editor Play Mode is not a substitute.

### UI Toolkit Pipeline

1. Coordinate with `/team-ui` and `ui-experience-lead` for UX and command-boundary gates.
2. Spawn `unity-ui-specialist` for UXML/USS, PanelSettings, focus, input, and performance.
3. Route UI C# controllers through `/team-csharp` review/test gates.

### DOTS Pipeline

1. Spawn `unity-dots-specialist` for ECS/Burst/Jobs architecture.
2. Coordinate with `/team-simulation` for deterministic sim boundaries.
3. Confirm no pure sim code references UnityEngine and no per-frame managed allocations.

### Addressables / Asset Pipeline

1. Spawn `unity-addressables-specialist` for groups, labels, catalogs, loading strategy.
2. Spawn `technical-artist` for import settings and asset budget review.
3. Run `/asset-audit` when assets or import settings are in scope.

### Shader / VFX Pipeline

1. Spawn `unity-shader-specialist` for shader/VFX architecture and render pipeline fit.
2. Spawn `performance-analyst` when frame budget or GPU cost is at risk.
3. Ensure visual effects do not become hidden gameplay-state owners.

### Build / Package Pipeline

1. Spawn `c-sharp-devops-engineer` for package, asmdef, batchmode, or CI changes.
2. Ask before package changes or build profile changes.
3. Validate with the smallest safe Unity or dotnet command available.

## Phase 3: Blocking Gates

Stop and ask before proceeding when a change affects:

- Unity-MCP scene/prefab/asset mutation.
- UPM package versions or ProjectSettings.
- Pure Sim/Data/Delegation dependency direction.
- Addressables catalogs, remote content, or memory strategy.
- DOTS/Burst hot paths or deterministic simulation behavior.
- Shader/render pipeline selection or platform quality tiers.

## Output

Produce a concise report:

- Mode and Unity subsystem.
- Agents/skills invoked or recommended.
- Files/assets likely affected.
- Architecture, performance, and asset risks.
- Validation plan and next approved action.
- MCP probe result (`:8080` live vs down) and whether the visual loop ran.

## Red flags — stop

- About to `Write`/`Edit` a `.unity`, `.prefab`, or `.meta` to "fix" hierarchy or GUIDs
- Calling Unity-MCP tools without a successful `:8080` probe this session
- Claiming Play Mode / screenshot evidence from headless-only work
- Editing `DelegationBridge` through Unity-MCP script/reflection tools
- Adding URP, HDRP, or the new Input System without explicit human approval
