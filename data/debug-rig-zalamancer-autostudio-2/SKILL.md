---
name: debug-rig
description: Debug 2D and 3D rigging systems including bone skeletons, mesh deformation, weight painting, animation playback, and spring bones.
---

# Debug Rig

Diagnose and fix issues in ProAnimate's 2D and 3D character rigging systems, covering bone skeletons, mesh generation, skinning weights, pose interpolation, animation playback, spring bones, and the BoneRigging engine.

## Purpose

ProAnimate supports two rigging systems: 2D image-based rigging (mesh deformation with Linear Blend Skinning) and 3D model rigging (Three.js skeletal animation). Both systems have complex pipelines from skeleton creation through animation playback. This skill helps debug issues at each stage.

## Steps

### 2D Rigging

1. **Verify the rig exists** in `useRigStore`:
   - `rigs` -- map of rigId to `RigData`.
   - `activeRigId` -- currently edited rig.
   - A `RigData` contains: `skeleton` (BoneSkeleton), `mesh` (MeshData), `skinning` (VertexSkinning), `imageUrl`, `imageWidth`, `imageHeight`.

2. **Check the bone skeleton** (`BoneSkeleton`):
   - `joints` -- array of `BoneJoint` with: `id`, `name`, `x`, `y`, `parentId`, `category`.
   - Root joint has `parentId: null`.
   - Joint positions are in image-space coordinates (pixels from top-left).
   - If bones appear in wrong positions, check `x` and `y` relative to the source image dimensions.
   - `category` values: `root`, `torso`, `head`, `arm-left`, `arm-right`, `hand-left`, `hand-right`, `leg-left`, `leg-right`, `tail`, `other`. Used for per-bone weight radius scaling.

3. **Check mesh generation** (`meshGenerator.ts`):
   - `generateGridMesh()` creates a uniform triangle grid. `gridSpacing` controls density (default 16px). Smaller = more vertices, better quality, slower.
   - `generateAlphaAwareMesh()` skips fully transparent regions (no expansion padding). Prevents stretching at transparent edges.
   - If the mesh looks wrong, verify `imageWidth` and `imageHeight` match the actual image dimensions.

4. **Check skinning weights** (`meshDeformer.ts`):
   - `computeSkinningWeights()` assigns up to 4 bone influences per vertex using cubic falloff.
   - Default influence radius: `max(80, imageDiagonal * 0.18)`.
   - Per-bone radius multipliers by category: root 1.2x, head 0.6x, hands 0.35x, legs 0.8x.
   - Alpha-barrier checking prevents cross-body-part influence when transparent gaps exist.
   - If a body part does not deform, the influence radius may be too small for that bone category. Check `CATEGORY_RADIUS_MULTIPLIER`.
   - Weight paint visualization: enable `showMeshWireframe` and check `WeightPaintPanel.tsx`.

5. **Check mesh deformation** (`meshDeformer.ts`):
   - `deformMesh()` applies Linear Blend Skinning: for each vertex, blend bone transforms weighted by skinning weights.
   - Input: mesh, skeleton, current pose, rest pose.
   - If deformation looks wrong, check: bone world positions via `computeJointWorldPositions()`, pose values (dx, dy, rotation), and weight normalization.

6. **Check pose interpolation** (`poseInterpolation.ts`):
   - `getPoseAtFrame(tracks, frame)` interpolates between keyframed poses using linear interpolation.
   - Pose tracks are in `poseTracks` array in the rig store.
   - If animation jumps, check that keyframes are properly ordered by `frame` value.

7. **Check BoneRigging engine** (`boneriggingPlayback.ts`):
   - Wraps `@bonerigging/core` for squash & stretch, spring physics, and FFD.
   - Uses serialized rig data (`boneriggingSerializedData` on `RigData`).
   - If BoneRigging engine is not available, stubs in `src/stubs/bonerigging-editor.tsx` are used.

8. **Check SVG-native rigging** (`svgRigService.ts`):
   - SVG elements bind directly to bones via `svgElementSkinning` on `RigData`.
   - `computeElementSkinningWeights()` assigns bone influences based on element center position.
   - If SVG elements do not move with bones, verify `pivotX`/`pivotY` are correct.

### 3D Rigging

9. **Verify 3D rig exists** in `use3DRigStore`:
   - `rigs` -- map of rigId to `RigData3D`.
   - `RigData3D` contains: `skeletonTree`, `restPose`, `boneMapping`, `characterId`.
   - `skeletonTree` is built from Three.js skeleton via `buildSkeletonTree()`.

10. **Check bone mapping** (`character3d.ts`, `BoneMappingEditor.tsx`):
    - Maps between skeleton standards: Mixamo, RPM, SMPL, HunyuanMotion, biped, custom.
    - `BoneMapping` maps standard bone names (e.g., `hips`, `spine`, `leftArm`) to actual bone names in the model.
    - If animation looks wrong on a specific skeleton, the bone mapping is likely incorrect.
    - Auto-detection tries to match bone names heuristically. Manual correction via `BoneMappingEditor.tsx`.

11. **Check 3D pose representation**:
    - Poses use quaternions (`Quat`) and vectors (`Vec3`).
    - Manual poses are OFFSETS applied on top of AnimationMixer output.
    - `getPose3DAtFrame()` in `poseInterpolation3d.ts` uses SLERP for quaternion interpolation.
    - If the character collapses or distorts, check quaternion normalization. Invalid quaternions (all zeros) cause NaN propagation.

12. **Check spring bones** (`springBones3d.ts`):
    - Verlet-style physics for hair, tails, accessories.
    - `SpringBoneChain3D` requires init with a Three.js Skeleton before simulation.
    - Config: `stiffness` (0-1), `damping` (0-1), `gravity` (world-space vector).
    - If spring bones are jittery, increase `damping`. If they do not move, decrease `stiffness`.
    - Particles store `currentPos` and `previousPos` for velocity computation.

13. **Check animation retargeting** (`skeletonRetarget.ts`):
    - Cross-skeleton animation transfer. Maps bones between source and target skeletons.
    - Requires compatible bone mappings on both skeletons.
    - If retargeted animation looks distorted, the bone mapping between source and target is incorrect.

## Key Files

| Purpose | Path |
|---------|------|
| 2D rig store | `src/stores/useRigStore.ts` |
| 3D rig store | `src/stores/use3DRigStore.ts` |
| Mesh generator | `src/services/meshGenerator.ts` |
| Mesh deformer (LBS) | `src/services/meshDeformer.ts` |
| Forward kinematics | `src/services/forwardKinematics.ts` |
| Pose interpolation (2D) | `src/services/poseInterpolation.ts` |
| Pose interpolation (3D) | `src/services/poseInterpolation3d.ts` |
| Spring bones 3D | `src/services/springBones3d.ts` |
| Squash & stretch 3D | `src/services/squashStretch3d.ts` |
| Skeleton retarget | `src/services/skeletonRetarget.ts` |
| GLTF utilities | `src/services/gltfUtils.ts` |
| BoneRigging playback | `src/services/boneriggingPlayback.ts` |
| SVG rig service | `src/services/svgRigService.ts` |
| Auto-rig service | `src/services/autoRigService.ts` |
| Rig types (2D) | `src/types/rig.ts` |
| Rig types (3D) | `src/types/rig3d.ts` |
| Animation curves | `src/types/animCurves.ts` |
| Animation state machine | `src/types/animStateMachine.ts` |
| Bone overlay (2D) | `src/components/canvas/BoneOverlay.tsx` |
| Bone gizmo (3D) | `src/components/canvas/BoneGizmo3D.tsx` |
| Rigged character renderer | `src/components/canvas/RiggedCharacterRenderer.tsx` |
| Weight paint panel | `src/components/panels/WeightPaintPanel.tsx` |
| Rig editor page | `src/components/pages/RigEditorPage.tsx` |

## Common Issues

- **Mesh not deforming**: Skinning weights are all zero for the moved bone. Increase `influenceRadius` or check bone placement relative to mesh vertices.
- **Body parts stretching incorrectly**: Alpha-barrier check may be disabled or the image has no transparent gaps between body parts. Enable alpha-aware mesh generation.
- **Bone overlay not visible**: `showBoneOverlay` is false in `useRigStore`. Toggle it via the rig editor UI.
- **3D bone mapping incorrect**: Auto-detection guessed wrong names. Open `BoneMappingEditor.tsx` and manually map bones.
- **Spring bones explode**: `stiffness` too low or `damping` too low. Try `stiffness: 0.5, damping: 0.8`.
- **Animation state machine not transitioning**: Check transition conditions in `useAnimStateMachineStore`. Conditions reference parameter values that may not be set.
- **Rigged character not rendering in export**: Ensure `preloadRiggedCharacters()` in `canvas2dRenderer.ts` loads the rig data. Check that `RigExportData` is included in `VideoCompositionProps`.
- **SVG elements not rigging**: `svgElementSkinning` array is empty. Call `createSvgRig()` with the SVG data URL, or run `recomputeSvgWeightsIfNeeded()`.

## Examples

Inspect 2D rig data:
```ts
const store = useRigStore.getState()
const rig = store.rigs[store.activeRigId!]
console.log('Joints:', rig.skeleton.joints.length)
console.log('Mesh vertices:', rig.mesh?.vertices.length)
console.log('Has skinning:', !!rig.skinning)
```

Inspect 3D rig data:
```ts
const store = use3DRigStore.getState()
const rig = store.getActiveRig()
console.log('Skeleton tree:', rig?.skeletonTree)
console.log('Bone mapping:', rig?.boneMapping)
console.log('Rest pose bones:', Object.keys(rig?.restPose || {}))
```
