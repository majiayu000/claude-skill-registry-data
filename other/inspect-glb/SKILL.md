---
name: inspect-glb
description: Use before loading, placing, scaling, or animating GLB models in PlayCanvas to read clips, joints, hierarchy, and compression, and measure exact bounds.
---

# Inspect GLBs

Inspect models before choosing transforms or animation names. Shortlist files; do not dump a whole
asset pack into context.

## Read the JSON chunk

A GLB's first chunk is JSON holding every name, readable without decoding geometry, even when
compressed:

```js
import { readFileSync } from 'node:fs';

const b = readFileSync('model.glb');
const gltf = JSON.parse(b.toString('utf8', 20, 20 + b.readUInt32LE(12)));
```

Print only the fields you need:

- Clips: `animations[].name`. Each channel's `target.node` and `target.path` (`translation`,
  `rotation`, `scale`, or `weights`) is what the clip drives.
- Joints: `skins[].joints`, indices into `nodes`.
- Hierarchy: walk `children` from `scenes[scene].nodes`, building slash-separated name paths.
- Morphs: `meshes[].extras.targetNames`.
- Compression: `extensionsRequired`; see `load-assets` for decoders.

## Measure bounds

POSITION accessor `min`/`max` and runtime `meshInstance.aabb` are boxes rotated with their node, so
they over-estimate rotated nodes by up to 41 percent. For exact bounds, load the model under an
identity-transform entity in the running app (`inspect-runtime`) and transform each
`meshInstance.mesh.getPositions()` vertex by `meshInstance.node.getWorldTransform()`:

- `dims = max - min` is the uniform scale input.
- `center = (min + max) / 2`. Non-zero `center.x` or `center.z` means the model does not sit on
  its root.
- `groundOffset = -min.y` is the Y seat.

Skinned and morphed meshes deform at runtime, so their bounds are estimates. Bounds cannot prove
facing. Confirm it in the running app and record the yaw with `calibrate-model`.
