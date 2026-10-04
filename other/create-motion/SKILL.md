---
name: create-motion
description: Generate 3D character motion/animation using HunyuanMotion text-to-3D-motion API with retargeting support.
argument-hint: <motion-description>
---

# Create 3D Motion

Generate 3D character animation from a text description using the HunyuanMotion API (Tencent HY-Motion-1.0 on HuggingFace). The generated motion can be retargeted to any 3D character with a mapped skeleton.

## Purpose

Create 3D animation clips from natural language descriptions (e.g., "a person walking confidently", "jumping and waving"). Motions are generated as FBX files, automatically converted to GLB, and can be applied to any 3D character via skeleton retargeting.

## Pipeline

The full motion generation pipeline (`generateMotion()` in `hunyuanMotion.ts`):

1. **Start generation** -- Send text prompt, duration, and FPS to `/api/motion/generate`
2. **Poll until complete** -- Check `/api/motion/task/:taskId` every 5 seconds (10 minute timeout)
3. **Download file** -- Fetch the generated animation file from `/api/motion/download/:taskId`
4. **Convert FBX to GLB** -- If the HuggingFace Space returns FBX, convert to GLB using `fbxConverter.ts`
5. **Return GLB blob** -- Ready for IndexedDB storage and Three.js playback

## API

### Client Functions

```ts
// Full pipeline (recommended)
generateMotion(prompt: string, duration?: number, fps?: number, onProgress?): Promise<{ glbBlob: Blob; taskId: string }>

// Individual steps
startMotionGeneration(request: MotionGenerateRequest): Promise<{ taskId: string }>
pollMotionTask(taskId: string): Promise<MotionTaskStatus>
downloadMotionFile(taskId: string): Promise<Blob>
pollMotionUntilComplete(taskId: string, options?: MotionPollOptions): Promise<MotionTaskStatus>
```

### Request/Response Types

```ts
interface MotionGenerateRequest {
  prompt: string     // Natural language motion description
  duration?: number  // Duration in seconds (default: 3)
  fps?: number       // Frames per second (default: 30)
}

interface MotionTaskStatus {
  id: string
  status: 'pending' | 'processing' | 'complete' | 'failed'
  progress: number   // 0-100
  error?: string
  fileFormat?: 'fbx' | 'glb'
}
```

## Server Route

The Express server (`server/routes/hunyuanMotion.ts`) proxies to the HuggingFace Space:

- **POST `/api/motion/generate`** -- Creates a task, starts async Gradio generation
- **GET `/api/motion/task/:taskId`** -- Returns task status and progress
- **GET `/api/motion/download/:taskId`** -- Streams the generated animation file

The server uses `@gradio/client` to connect to the `tencent/HY-Motion-1.0` HuggingFace Space. The Gradio API flow:
1. `/_prompt_engineering` -- Rewrites the prompt for better motion quality
2. `/generate_motion_func` -- Generates the actual motion with rewritten prompt

An in-memory task store tracks async Gradio operations. Tasks auto-expire and include progress tracking.

## Skeleton Retargeting

Generated motions can be applied to characters with different skeletons using `skeletonRetarget.ts`:

1. Both source (HunyuanMotion) and target (character) skeletons need bone mappings
2. Retargeting maps animations from source bone names to target bone names via the 20 standard bone names
3. Quaternion rotations are transferred, positions are scaled proportionally

Standard bone names used for retargeting:
```
Pelvis, Spine1, Spine2, Spine3, Neck, Head,
L_Collar, L_Shoulder, L_Elbow, L_Wrist,
R_Collar, R_Shoulder, R_Elbow, R_Wrist,
L_Hip, L_Knee, L_Ankle, R_Hip, R_Knee, R_Ankle
```

## Key Files

| Purpose | Path |
|---------|------|
| HunyuanMotion client | `src/services/hunyuanMotion.ts` |
| FBX to GLB converter | `src/services/fbxConverter.ts` |
| Skeleton retargeting | `src/services/skeletonRetarget.ts` |
| 3D animation store | `src/stores/use3DAnimationStore.ts` |
| 3D rig store | `src/stores/use3DRigStore.ts` |
| Character 3D types | `src/types/character3d.ts` |
| GLTF utilities | `src/services/gltfUtils.ts` |
| Motion library panel | `src/components/panels/MotionLibraryPanel.tsx` |
| Animation modal | `src/components/panels/AnimationModal3D.tsx` |
| Server route | `server/routes/hunyuanMotion.ts` |

## Common Issues

- **HuggingFace Space unavailable**: The `tencent/HY-Motion-1.0` Space may be cold-started or down. The server catches unhandled rejections from `@gradio/client` to prevent crashes.
- **HF_TOKEN not set**: Optional `HF_TOKEN` in server `.env` may be needed for rate-limited Spaces. The server checks `process.env.HF_TOKEN`.
- **FBX conversion fails**: Some FBX files may use unsupported features. The `fbxConverter.ts` service handles the conversion; if it fails, check the FBX version and structure.
- **Motion too short/long**: Default duration is 3 seconds. HunyuanMotion supports variable durations; adjust the `duration` parameter.
- **Retargeting artifacts**: If the target skeleton's bone mapping is incomplete or incorrect, retargeted animations may look wrong. Verify bone mapping using the `BoneMappingEditor`.
- **Task timeout**: Motion generation can take several minutes. The default timeout is 10 minutes (`maxWaitMs: 600000`). If the Space is under heavy load, this may need to be increased.
- **Credit gating**: Motion generation uses `hunyuan-motion` credit type.

## Example

Prompt: "A person doing a confident walk with arms swinging"
Duration: 4 seconds
FPS: 30

The pipeline will:
1. Send the prompt to the HuggingFace Space
2. Gradio rewrites the prompt for motion quality
3. Motion is generated (typically 1-3 minutes)
4. FBX file is downloaded and converted to GLB
5. GLB blob is stored in IndexedDB
6. Animation appears in the Motion Library panel
7. User can drag-apply the animation to any 3D character
8. If the character uses a different skeleton (e.g., Mixamo), retargeting maps the bones automatically
