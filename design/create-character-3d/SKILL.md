---
name: create-character-3d
description: Generate a 3D character model using Meshy API (text-to-3D or image-to-3D), with bone mapping and animation import.
argument-hint: <character-description>
---

# Create 3D Character

Generate a 3D character model from text or an image using the Meshy API, with automatic bone mapping, skeleton retargeting, and animation import support.

## Purpose

Create a rigged 3D character model (GLB format) that can be placed on the canvas, animated with imported or generated motions, and exported via Remotion. Supports text-to-3D and image-to-3D workflows through the Meshy API, with optional auto-rigging.

## Workflow

### Text-to-3D

1. User provides a text description (e.g., "a cartoon robot with blue eyes")
2. Client calls `startTextTo3D(request)` which sends to `/api/meshy/text-to-3d`
3. Server proxies to Meshy API, returns a `taskId`
4. Client polls `pollTask(taskId)` until status is `SUCCEEDED`
5. Result includes `model_urls.glb` -- the GLB download URL
6. GLB is loaded into Three.js, skeleton is extracted

### Image-to-3D

1. User provides an image (uploaded or generated)
2. Client calls `startImageTo3D(request)` which sends to `/api/meshy/image-to-3d`
3. Same polling and download flow as text-to-3D

### Auto-Rigging

After generation, models can be auto-rigged:
1. Client calls `startAutoRig({ modelUrl })` -> `/api/meshy/auto-rig`
2. Poll `pollRigTask(taskId)` until complete
3. Result is a rigged GLB with skeleton hierarchy

### Remeshing

High-poly models can be decimated:
1. Client calls `startRemesh({ modelUrl, targetPolycount })` -> `/api/meshy/remesh`
2. Poll `pollRemeshTask(taskId)` until complete
3. Result is a reduced-poly GLB (default: 30,000 polygons)

## Skeleton Types and Bone Mapping

The system supports multiple skeleton naming conventions:

| Type | Source | Example Bones |
|------|--------|--------------|
| `mixamo` | Mixamo characters | `mixamorigHips`, `mixamorigSpine` |
| `readyplayerme` | Ready Player Me | `Hips`, `Spine` |
| `smpl` | SMPL body model | `Pelvis`, `L_Hip` |
| `hunyuan` | HunyuanMotion output | `pelvis`, `spine_01` |
| `biped` | Standard biped | `Pelvis`, `Spine1` |
| `custom` | Unknown skeleton | User-mapped |

Bone mapping maps 20 standard bone names to actual skeleton bone names:
```
Pelvis, Spine1, Spine2, Spine3, Neck, Head,
L_Collar, L_Shoulder, L_Elbow, L_Wrist,
R_Collar, R_Shoulder, R_Elbow, R_Wrist,
L_Hip, L_Knee, L_Ankle, R_Hip, R_Knee, R_Ankle
```

The `BoneMappingEditor` component provides a visual UI for mapping bones. Skeleton type is auto-detected from bone names using heuristics in `gltfUtils.ts`.

## 3D Lip Sync

2D viseme sprites can be projected onto 3D character faces via `VisemeFaceMapping`:
- A textured plane is positioned relative to the Head bone
- Offset, scale, and rotation are configurable
- Cross-fade transitions between viseme sprites
- Auto-fit recalculates placement based on actual model geometry

## Storage

3D character GLB blobs are stored in IndexedDB via `character3dDB.ts` (too large for Supabase). Character metadata (name, bone mapping, settings) is stored in the Zustand store and can be persisted to Supabase.

## Key Files

| Purpose | Path |
|---------|------|
| Meshy API client | `src/services/meshyAPI.ts` |
| 3D character types | `src/types/character3d.ts` |
| 3D character store | `src/stores/use3DCharacterStore.ts` |
| Saved 3D characters | `src/stores/useSaved3DCharactersStore.ts` |
| 3D animation store | `src/stores/use3DAnimationStore.ts` |
| GLTF utilities | `src/services/gltfUtils.ts` |
| FBX converter | `src/services/fbxConverter.ts` |
| Skeleton retarget | `src/services/skeletonRetarget.ts` |
| Bone mapping editor | `src/components/panels/BoneMappingEditor.tsx` |
| 3D character panel | `src/components/panels/Character3DPanel.tsx` |
| 3D renderer | `src/components/canvas/Character3DRenderer.tsx` |
| Remotion 3D layer | `src/remotion/Remotion3DCharacter.tsx` |
| 3D rig store | `src/stores/use3DRigStore.ts` |
| IndexedDB storage | `src/services/character3dDB.ts` |
| Server route | `server/routes/meshy.ts` |

## Meshy API Request Types

```ts
interface MeshyTextTo3DRequest {
  prompt: string
  mode?: 'preview' | 'refine'
  art_style?: string
  negative_prompt?: string
}

interface MeshyImageTo3DRequest {
  image_url: string
  mode?: 'preview' | 'refine'
}

interface MeshyAutoRigRequest {
  modelUrl: string
}
```

## Polling Pattern

All Meshy operations are async with task-based polling:

```ts
const { taskId } = await startTextTo3D({ prompt: 'a cartoon robot' })

const result = await pollTaskUntilComplete(taskId, {
  intervalMs: 5000,     // Poll every 5 seconds
  maxWaitMs: 600000,    // 10 minute timeout
  onProgress: (progress, status) => {
    console.log(`${status}: ${progress}%`)
  },
})
```

## Common Issues

- **Meshy API key missing**: Requires `MESHY_API_KEY` in server `.env`. All calls go through the Express proxy.
- **GLB loading fails**: Some Meshy models may have unsupported extensions. Use `useSafeGLTF` hook for error-tolerant loading.
- **Bone mapping wrong**: Auto-detection may fail for non-standard skeletons. Use the `BoneMappingEditor` to manually map bones.
- **Model too heavy**: Use remeshing to reduce polygon count before rendering. Default target is 30,000 polygons.
- **Animation retargeting mismatch**: Cross-skeleton retargeting requires correct bone mapping on both source and target skeletons.
- **Credit gating**: Operations use credit types `meshy-text-to-3d`, `meshy-image-to-3d`, `meshy-auto-rig`.

## Example

Description: "A stylized knight character with silver armor and a red cape"

The workflow will:
1. Call Meshy text-to-3D with the description
2. Poll until the 3D model is generated (typically 1-3 minutes)
3. Download the GLB file
4. Auto-detect skeleton type and build bone mapping
5. Store GLB blob in IndexedDB, metadata in store
6. Render on canvas via Three.js with OrbitControls
7. Optionally auto-rig if the model lacks a skeleton
8. Import animations (walk, idle, run) from the motion library
