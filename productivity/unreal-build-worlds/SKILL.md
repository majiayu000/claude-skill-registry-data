---
name: unreal-build-worlds
description: Build Unreal streaming worlds with explicit World Partition, data-layer, level-instance and HLOD ownership and measured unload behavior.
engines: [UNREAL]
---

# Unreal Build Worlds

## When to use

Author or change Unreal world partitioning, runtime streaming, data layers, level instances and world build artifacts. Gameplay behavior, asset import and procedural generation retain their own owners; this skill defines when their content is available in a world.

## Activation and inputs

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unreal-build-worlds`; require effective `UNREAL` and `compatible: true` before edits or tool launches. Honor validated task-only override evidence and its output scope. `ENGINE.md` remains authoritative; observations and receipts belong under `.hephaera/.cache`.

Inspect the project's Unreal version, existing map/streaming format, target platforms, persistence identities, multiplayer authority, traversal speeds and CPU/memory/loading budgets. A map-format conversion or HLOD rebuild can change many binary/external-actor packages: preview its exact scope before writing through native tools.

## Workflow

1. Read [streaming and world ownership](references/streaming-and-world-ownership.md) for the selected world system. Keep existing project conventions unless the task calls for a migration; do not enable World Partition just because a map is large.
2. Define streaming sources, activation conditions and readiness gates. Separate requested loading from loaded/visible/usable content. Gameplay must tolerate late loads, teleportation, cancellation and world teardown without accessing departed actors.
3. Author real `.umap`, Data Layer and Level Instance packages through the matching Editor or supported commandlet. Preserve external-actor ancestry and intended package scope; never fabricate binary content or use an Editor-visible layer as evidence of runtime availability.
4. Resolve persistent IDs independently of actor pointers, editor labels and unloaded instances. Restore world state only after required actors/data are ready; define server/client responsibilities for runtime layer changes.
5. Build navigation/HLOD/other required world artifacts using selected native builders. Record inputs, plugin settings, generated packages, invalidation and cook inclusion; no unrelated bulk resave or builder execution is implied.

## Verification and output

Deliver native world changes, streaming/dependency manifest, budget measurements and expected/observed lifecycle evidence. Exercise boundary traversal, teleport, rapid load/unload, overlapping sources, layer activation, save restoration and world exit. Verify unloaded content stops collision, ticking and callbacks, then returns with the intended state. Revisit the same area repeatedly to detect retained actors, delegates and memory growth.

Cook and test the relevant maps in the actual target player. Record native tools or fixtures as blocked/not-run when unavailable; commandlet success does not certify HLOD appearance, collision or player comfort.
