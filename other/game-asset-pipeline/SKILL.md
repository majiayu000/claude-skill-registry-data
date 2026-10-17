---
name: game-asset-pipeline
category: assets
description: Use when adding, importing, moving or loading textures, models, audio or scenes - per-platform compression, atlases, LODs, async loading per engine, engine metadata files (.meta, .import, .uid, .uasset), Git LFS, and asset validation tests.
tech_stack: Game core
source: informed by the Unity, Godot, Unreal, three.js, Babylon.js and Khronos KTX/glTF docs; own wording
---
# Game Asset Pipeline

## Overview

Assets are most of a game's size, most of its load time and most of its memory. They also come with engine metadata that silently breaks references when it is lost: a Unity `.meta` regenerated with a new GUID unhooks every prefab that used the asset. Treat assets like code — reviewed import settings, committed metadata, validated by tests.

**Core principle:** Compressed for the target platform, loaded asynchronously, committed with its metadata, and never moved outside the engine that owns its references.

## Metadata files — commit them, never orphan them

| Engine | Files | Rule |
|---|---|---|
| Unity | `<asset>.meta` (GUID + import settings) beside every asset and folder | Commit with the asset; move/rename inside the Editor or move the `.meta` with it; never delete and regenerate |
| Godot 4 | `<asset>.import` beside imported assets; `.uid` beside scripts and shaders (4.4+); `.godot/` cache | Commit `.import` and `.uid`; ignore `.godot/` |
| Unreal | `.uasset` / `.umap` (binary, references by path) | Move/rename only in the Editor, then "Fix Up Redirectors"; lock binaries (LFS `lockable`) |
| Web / Bevy | none | Paths are code — update every reference in the same change |

Moving a file with `mv` in a Unity or Unreal project without its metadata (or outside the editor) is a broken-reference bug even if the build is green.

## Git LFS

- Check `.gitattributes` first; follow the patterns it already has. Typical: `*.png *.psd *.fbx *.glb *.wav *.ogg *.uasset *.umap filter=lfs diff=lfs merge=lfs -text`, with `lockable` for Unreal binaries.
- A new binary type the repository does not track yet gets its pattern added in the same change — not a 40 MB `.fbx` committed as a regular blob.
- `git lfs ls-files` shows what is tracked; if `git lfs` is not installed here, say so instead of committing pointers by hand.

## Textures

| Target | Format |
|---|---|
| Desktop / console | BC7 (colour), BC5 (normal maps), BC4 (single channel) |
| Modern mobile | ASTC (block size by quality: 4×4 UI, 6×6–8×8 world) |
| Android fallback | ETC2 |
| Web | KTX2 / Basis Universal (transcoded per GPU at load), WebP/AVIF for UI and 2D |

- Unity: per-platform overrides in the importer; max size per platform; mipmaps on for world textures, off for UI and pixel art; Sprite Atlas for 2D.
- Godot: "VRAM Compressed" for 3D (enable ETC2/ASTC import in project settings for mobile), "Lossless" with filtering off for pixel art; AtlasTexture/TileSet for 2D.
- Unreal: texture groups and compression settings (`TC_Default`, `TC_Normalmap`, `TC_Masks`), LOD bias per platform.
- Web: KTX2 via three.js `KTX2Loader` / Babylon's KTX2 support; packed atlases (TexturePacker JSON) for Phaser/PixiJS.
- Power-of-two sizes where mipmaps or block compression need them; no 4K texture on a 64-pixel prop.

## Meshes and scenes

- LODs for anything seen at a distance: Unity `LODGroup`, Godot automatic mesh LOD on import, Unreal Nanite for static meshes where the platform supports it and classic LODs elsewhere (skeletal meshes, mobile).
- Web: glTF/GLB with Draco or meshopt geometry compression and KTX2 textures — `npx @gltf-transform/cli optimize in.glb out.glb` is a quick win; check the repository's pipeline first.
- Colliders are simplified shapes, not render meshes.

## Audio

- Compressed (Vorbis/Opus/AAC); music streamed, short frequent SFX decompressed on load.
- Unity: Load Type per clip (Streaming for music, Decompress On Load for short SFX); Godot: `.ogg` for music, `.wav` for short SFX; web: a format every target browser decodes, and an audio-unlock on the first user gesture.

## Loading without hitches

```csharp
// ❌ synchronous load mid-gameplay: a visible hitch, and Resources/ ships everything
var prefab = Resources.Load<GameObject>("Enemies/Boss");

// ✅ async, released when done (Addressables)
var handle = Addressables.LoadAssetAsync<GameObject>("enemies/boss");
var prefab = await handle.Task;
// ... later, when the level unloads:
Addressables.Release(handle);
```

```gdscript
# Godot: threaded load at a loading screen or ahead of need
ResourceLoader.load_threaded_request(LEVEL_PATH)
# poll in _process:
if ResourceLoader.load_threaded_get_status(LEVEL_PATH) == ResourceLoader.THREAD_LOAD_LOADED:
    var scene: PackedScene = ResourceLoader.load_threaded_get(LEVEL_PATH)
```

- Unreal: soft references (`TSoftObjectPtr`, `TSoftClassPtr`) with `UAssetManager` / `FStreamableManager::RequestAsyncLoad`; avoid hard references in Blueprints that pull whole asset graphs into memory.
- Web: Phaser's loader in a preload scene, PixiJS `Assets.loadBundle`, three.js `LoadingManager`; code-split per level.
- Bevy: `AssetServer::load` returns a handle immediately; gate the state change on the load state (or the repository's loading plugin).

## Validating assets in tests

An import-settings test fails the build when someone drops in an uncompressed 4K texture:

```csharp
[Test] public void WorldTextures_AreCompressedAndCapped() {
    foreach (var guid in AssetDatabase.FindAssets("t:Texture2D", new[] { "Assets/_Project/Art/World" })) {
        var path = AssetDatabase.GUIDToAssetPath(guid);
        var importer = (TextureImporter)AssetImporter.GetAtPath(path);
        Assert.That(importer.maxTextureSize, Is.LessThanOrEqualTo(2048), path);
        Assert.That(importer.textureCompression, Is.Not.EqualTo(TextureImporterCompression.Uncompressed), path);
    }
}
```

The same idea elsewhere: a Godot test reading `.import` files under `res://art/world`, a Node script checking `public/` sizes and formats, a data-validation rule in Unreal.

## Common Mistakes

- Moving or renaming assets with `mv` and losing `.meta` GUIDs or Unreal references.
- Committing Godot's `.godot/` cache or Unreal's `Intermediate/`, `Saved/`, `DerivedDataCache/`, `Binaries/`.
- Uncompressed or oversized textures; mipmaps on UI sprites.
- `Resources.Load` / synchronous `load()` during gameplay.
- Loaded assets never released (Addressables handles, three.js textures) — memory grows every level.

## Red Flags

- A new binary file in the diff that is not covered by `.gitattributes` LFS patterns the repo uses.
- An asset in the diff without its `.meta` / `.import`, or a `.meta` with a changed GUID.
- A hitch report and a synchronous load in the same code path.
