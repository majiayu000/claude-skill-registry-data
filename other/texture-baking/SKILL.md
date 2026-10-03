---

name: leeway-3d-texture-baking

description: 3D texture authoring and baking skill for high-to-low projection, normal/AO/curvature/id maps, channel packing, dilation, cage/ray validation, seams, mip safety and engine-ready texture outputs.

license: MIT

---

# LeeWay 3D Texture Baking

## Pipeline

Source/high detail → low/game mesh → UV validation → cage/ray setup → bake normal/AO/curvature/id/thickness as needed → inspect skew/seams/projection errors → author/derive PBR textures → channel pack/compress → mip/dilation validation → engine/render validation.

## Truth

A successful bake command is not a clean bake. Inspect gradients, hard-edge/UV relationships, tangent basis, cage intersections and visible seams.