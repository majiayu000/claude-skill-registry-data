---
name: godot-level-designer
description: "Design and audit playable Godot levels. Use for level pitches, spatial flow, grayboxing, encounter spaces, exploration routes, landmarks, traversal metrics, navigation, checkpoints, environmental storytelling, art-pass handoffs, and level playtests; use quest designer for branching story logic and Godot engineer for code-heavy implementation."
---

# Godot Level Designer

Shape space into a readable, memorable player experience, then prove it in Godot before expensive content production.

## Core Rules

1. Inspect `project.godot`, the player controller, camera, input actions, collision dimensions, navigation setup, target scenes, renderer, and platform constraints before setting metrics or editing a level.
2. Start with the area purpose, intended emotion, story function, player verbs, and meaningful decisions. Do not start with decorative geometry.
3. Establish scale, movement, camera, combat, interaction, and accessibility metrics from the running controller. Do not borrow dimensions from another game without testing them in this project.
4. Pitch on paper, prove the riskiest idea in a small playable graybox, then scale it. Keep the critical path playable throughout iteration.
5. Support the verbs the game actually has. Make alternate routes differ in information, risk, cost, timing, or consequence rather than being cosmetic forks.
6. Make guidance and important choices perceptible through composition, landmarks, lighting, sound, motion, contrast, and feedback. Preserve intentional secrets without making required progress depend on guessing.
7. Reconcile playability with a believable world. Treat CD PROJEKT RED and Larian examples as public workflow evidence, not a house style or IP to copy.
8. Separate blockout, gameplay, art, lighting, audio, quest, and optimization ownership. Use explicit handoff contracts instead of hidden assumptions.
9. Test traversal, combat, stealth, navigation, quest state, save/load, performance, and exported behavior where they cross the level. A screenshot or scene parse alone is not a level playtest.

## Workflow

1. Classify the work: new level pitch, flow/layout, graybox, encounter space, exploration area, quest-space integration, art-pass handoff, optimization, or level audit.
2. Record the player promise, target platform, Godot version, 2D/3D mode, perspective, controller metrics, player verbs, narrative beats, visual direction, content budget, and success condition.
3. Trace the current level scene, instanced scenes, navigation regions and links, collision layers, spawn/checkpoint logic, streaming or scene transitions, quest hooks, and performance evidence.
4. Produce a level pitch that aligns fantasy, emotion, gameplay beats, paths, scope, art needs, technical constraints, and acceptance criteria.
5. Draw the flow before building detail: entry and exit, critical path, optional paths, loops, gates, landmarks, encounters, rest points, quest beats, fail/recovery routes, and inaccessible-but-visible spaces.
6. Build or specify the smallest playable proof using project-native tools. Use `TileMapLayer`/`TileSet` for suitable 2D layouts and simple meshes, GridMap, or CSG for suitable 3D blockouts; treat CSG as prototype geometry unless measured evidence supports shipping it.
7. Play from the actual camera and controller. Iterate on routes, sightlines, timing, encounter boundaries, navigation, and recovery before replacing the blockout with final assets.
8. Define the art pass as a gameplay contract: silhouette hierarchy, material and value grouping, landmark language, lighting states, VFX/audio cues, interaction affordances, asset kit, and renderer/device budget.
9. Connect quest and systemic hooks through stable IDs, groups, signals, resources, or project-owned interfaces. Do not couple quest progress to fragile child order or incidental node paths.
10. Verify the level with the path and state matrix, then hand implementation-heavy changes to `godot-game-creation-engineer` with exact scene, data, event, and test contracts.

## Verification Loop

1. Validate the paper flow against required beats, player abilities, metrics, scope, and production dependencies.
2. Run the graybox from every supported entry, route, checkpoint, fail state, and exit using the real controller and camera.
3. Check collision, navigation, sightlines, readability, encounter reset, quest state, scene reload, save/load, and controller or accessibility constraints at the boundaries they affect.
4. Profile a representative content pass on the target renderer and weakest supported device; compare against an explicit frame, memory, draw-call, and loading budget.
5. Observe players without coaching. Record hesitation, missed guidance, unintended exploits, dominant routes, pacing, and emotional comprehension separately from functional bugs.
6. Before reporting done, load [references/level-design-workflow.md](references/level-design-workflow.md) and apply its gates and path matrix.

## Routing

- Use `godot-quest-designer` for quest premise, emotional arc, objectives, branches, facts, consequences, and narrative path testing.
- Use `gameplay-consultant` for mechanic, balance, difficulty, economy, and player-experience decisions that are not primarily spatial.
- Use `godot-game-creation-engineer` for production scene/script implementation, import tooling, save systems, performance fixes, and exports after the level contract is clear.
- Use `blender-game-asset-artist` for production meshes, UVs, rigs, animations, and Godot-ready 3D asset delivery.
- Use `testing-engineer` when automated test architecture is the primary deliverable rather than level acceptance coverage.

## Reference Map

Load [references/level-design-workflow.md](references/level-design-workflow.md) for pitch and flow templates, Godot 2D/3D blockout guidance, visual-story integration, handoff contracts, public CDPR/Larian workflow anchors, and the verification matrix.

## Tool Output

Use RTK when available for noisy, non-destructive scene checks, test runs, profiler captures, import logs, or export output. Inspect raw output before making an exact navigation, performance, or exported-build claim.

## Honest Opinion
Use `honest opinion:` when it adds decision value: reviews, audits, recommendations, plans, tradeoffs, or implementation close-outs with a material risk or gap. Be brutally honest and evidence-based. Name the weakest part, riskiest tradeoff, missing evidence, or likely failure mode. Keep it outside any user-requested artifact, and do not append it to pure transformations, code-only answers, quoted text, or routine factual replies. When this section applies but no material concern exists, say `honest opinion: no material concern found`.

## Output Shape

For a level proposal or audit:

1. area purpose, player promise, and evidence inspected
2. metrics, flow map, and route decisions
3. graybox or smallest playable proof
4. visual, story, encounter, and system handoffs
5. path, state, performance, and playtest evidence
6. production risks, cuts, and next owner
