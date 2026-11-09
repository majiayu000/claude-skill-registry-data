---
name: unity-build-scenes
description: Build Unity scenes and prefab lifecycles with explicit data, navigation, loading, and serialization ownership.
engines: [UNITY]
---

# Unity Build Scenes

## When to use

Build Unity scenes and prefab lifecycles with explicit data, navigation, loading, and serialization ownership. Use this feature only for Unity-owned project code and assets.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unity-build-scenes` before edits or tool launches. Continue only when the effective engine is `UNITY` and this skill is eligible. A requested skill never selects its engine. Honor the resolved task override evidence and permitted output scope when an isolated prototype is selected.

Read ProjectVersion.txt, package manifest and lock, existing assembly definitions, target platforms, scene loading strategy, and gameplay acceptance scenarios. Identify the selected navigation package before using NavMesh APIs. Use the project's Unity-compatible C# profile; standalone .NET tooling does not select Unity's compiler.

## Workflow

1. Map lifetime across MonoBehaviour components, scene services and persistent application state. Assign Awake, OnEnable, Start, OnDisable and OnDestroy responsibilities; avoid relying on accidental execution order or introducing hidden global objects.
2. Author GameObjects, components, prefabs and scenes through the project's supported Editor workflow. Preserve asset .meta GUIDs, prefab references and intentional overrides; a textual edit must not invent missing binary content or change file identities.
3. Keep ScriptableObject assets as validated authoring configuration unless mutable shared state is explicitly intended. Build runtime state separately; entering Play Mode must not silently persist gameplay mutations into source assets.
4. Choose additive versus replacement loading through SceneManager, define the active scene and loading gate, and keep scene activation/cancellation from leaving duplicate listeners, players or services. Addressables remains an explicit package and delivery decision.
5. Integrate world streaming, navigation ownership and AI scheduling at scene boundaries. Record bake inputs, agent dimensions and link traversal; AI intent must enter the same movement authority as player movement. Read [navigation lifetime](references/navigation-lifetime.md) for surfaces, path status, cancellation and rebaking.
6. Define save records using stable domain identifiers and schema versions instead of scene instance references. Validate loaded data before applying it, restore dependencies in order, and make failed migration preserve the original save.
7. Separate Editor-only authoring assemblies from runtime assemblies. Use project-owned validation to catch missing scripts, broken prefab links, duplicate IDs and invalid content before building.

For staged Blender assets, read [Blender asset handoff](references/blender-asset-handoff.md) for importer identity, actual rig selection, curated LODs and renderer-specific material review.

## Verification

- Open and reload a representative scene with real Unity; check missing scripts, GUID references, prefab variants and deterministic bootstrap.
- Load, unload and reload additive content, disable and re-enable actors, and repeat Play Mode entry with the project's domain reload configuration.
- Round-trip a versioned save, reject malformed data, and test a navigation path that becomes unavailable. Record measured load and allocation budgets.

## Output

Changed scene/prefab/component assets, a lifetime and loading map, content/save schemas and migration behavior, and native Editor/player evidence tied to the project version. Record environment, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not install a navigation or loading package implicitly. A source scan can verify references but cannot certify a scene plays correctly. Engine guidance applies to engine-owned code; independent services retain their architecture contracts.

## References

- [Unity scene management](https://docs.unity3d.com/6000.0/Documentation/Manual/CreatingScenes.html). Use the documentation matching the installed project version.
- [Script execution lifecycle](https://docs.unity3d.com/6000.0/Documentation/Manual/execution-order.html). Use the documentation matching the installed project version.

