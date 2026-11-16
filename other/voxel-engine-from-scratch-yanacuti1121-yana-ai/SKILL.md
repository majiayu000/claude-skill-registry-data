---
name: voxel-engine-from-scratch
description: "Use when building a voxel (cube-based) world engine from first principles — chunking, mesh generation, terrain generation. Not for general 3D rendering or using an existing voxel engine. Triggers on: 'build a voxel engine', 'minecraft-style world generation', 'chunk meshing', 'greedy meshing algorithm', 'voxel terrain generation', 'implement a block world'. Covers chunk representation, face culling, greedy meshing, and noise-based terrain."
origin: yana-ai — synthesized from public voxel-engine design write-ups (0fps.net chunking/meshing series, common Minecraft-clone tutorials) and community from-scratch tutorials indexed in codecrafters-io/build-your-own-x
license: Apache-2.0
version: 1.0.0
compatibility: yana-ai >= 0.43.2
---

# /voxel-engine-from-scratch

## When to Use

- Building a block/voxel-based 3D world (Minecraft-style) from raw block data, including chunking, meshing, and terrain generation.
- Implementing or choosing a mesh-generation strategy (naive cubes, culled faces, greedy meshing) for voxel rendering performance.
- Generating procedural terrain from noise functions for a voxel world.

## Do NOT use for

- General 3D rendering not based on a uniform block grid — see `threejs-skills`/`spline-3d-integration` for scene-graph-based 3D work instead.
- Non-voxel procedural generation (dungeon layout, L-systems for foliage) — this skill is specifically about the block/chunk/mesh pipeline.
- Physics/collision for arbitrary 3D meshes — voxel collision is simpler (grid lookup) and covered in Step 4 here; general mesh collision is a different, harder problem.

---

## Pipeline Overview

```
1. World representation  — chunks of blocks, not one giant 3D array
2. Terrain generation     — noise function decides block type per (x,y,z)
3. Meshing                — convert block data into a renderable triangle mesh (the hard part)
4. Chunk loading           — load/unload chunks around the player as they move
```

## Step 1: Chunk-Based World Representation

Never store the whole world as one 3D array — even a modest 1000×1000×256 world is 256 million cells. Instead, divide the world into fixed-size **chunks** (commonly 16×16×16 or 32×32×32 blocks), each stored as a flat array indexed `x + y*W + z*W*H`. The world is a hash map from chunk coordinate `(cx, cy, cz)` to chunk data, so only chunks near the player need to exist in memory at all.

Each cell stores a block type (a small integer/enum — air, stone, dirt, etc.), not a full object; a 16³ chunk of 1-byte block IDs is 4KB, cheap to keep thousands of in memory.

## Step 2: Terrain Generation

Use a coherent noise function (Perlin or Simplex noise — smooth, continuous pseudo-random values, unlike raw random which produces uncorrelated block-to-block noise) to decide terrain height and block type:

```
height(x, z) = base_height + amplitude * perlin_noise(x / scale, z / scale)
for y in 0..height(x,z): block[x][y][z] = STONE
block[x][height(x,z)][z] = GRASS
```

Layering multiple noise octaves at different frequencies (fractal/fBm noise: sum several noise calls at increasing frequency, decreasing amplitude) produces more natural-looking terrain than a single noise call — large-scale hills from low-frequency octaves, small-scale bumps from high-frequency ones.

## Step 3: Meshing — Where the Performance Problem Actually Is

**Naive approach (don't ship this)**: render a cube (12 triangles) for every non-air block. A 32³ chunk with mostly-solid terrain generates ~100K+ triangles for a single chunk, almost all of them faces buried inside solid stone that the camera can never see — this doesn't scale past a handful of chunks.

**Step 3a — Face culling**: for each block, only emit a face if the neighboring block in that direction is air (or transparent). This alone eliminates the vast majority of interior faces (a solid stone chunk's interior contributes zero visible faces) and is the mandatory first optimization.

**Step 3b — Greedy meshing**: even after culling, adjacent coplanar faces of the same block type are still separate quads (e.g. a flat 16×16 grass floor is 256 separate face quads). Greedy meshing merges adjacent same-type, same-orientation faces into the largest possible rectangle before emitting geometry — that same 16×16 floor becomes a *single* quad. Algorithm sketch per chunk, per axis direction:

```
for each 2D slice of the chunk along the current axis:
  build a 2D grid marking (block_type, needs_face) per cell
  greedily scan the grid: starting from the first unprocessed cell,
    grow a rectangle as wide as possible (same type, all need-face),
    then as tall as possible (every row in that width also matches),
    emit ONE quad for the whole rectangle, mark those cells processed
  repeat until the whole slice is processed
```

This is the single biggest mesh-size win in a voxel engine — typically an order of magnitude fewer triangles than culled-but-ungreedy meshing, which is the difference between a chunk rendering smoothly and a chunk tanking framerate.

**Rebuild triggers**: a chunk's mesh only needs rebuilding when its block data (or an edge-adjacent neighboring chunk's block data, since face culling reads across chunk boundaries) changes — cache the generated mesh and don't regenerate every frame.

## Step 4: Chunk Loading Around the Player

Maintain a "render distance" in chunks. Each frame (or on player chunk-boundary crossing, not every frame), compute which chunk coordinates fall within render distance of the player's current chunk, load/generate any that are missing, and unload (or just stop rendering, if memory allows) chunks that fell outside the radius. Do generation and meshing for newly-loaded chunks on a background thread/worker where possible — synchronous chunk generation on the main/render thread is the most common cause of stutter when a player crosses a chunk boundary.

Block-level collision, for reference: since the world is a uniform grid, collision is a lookup, not a geometric intersection test — round the entity's bounding box corners to block coordinates and check `is_solid(block_at(x,y,z))`, far cheaper than mesh-based collision.

## What NOT to Do

- Don't render one cube mesh per block — see Step 3's naive-approach warning; this is the change that makes a voxel engine unshippable at any real render distance.
- Don't skip greedy meshing "for later" if performance matters at all — face culling alone still leaves an order of magnitude more triangles than necessary on any large flat/uniform region (floors, walls, water).
- Don't regenerate a chunk's mesh every frame — cache it, invalidate only on the actual block-data change that affects that chunk's visible faces.
- Don't do chunk generation/meshing synchronously on the render thread if you want smooth movement — it's the standard cause of hitching when the player crosses into unloaded territory.
