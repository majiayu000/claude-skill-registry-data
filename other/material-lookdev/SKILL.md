---

name: leeway-3d-material-lookdev

description: PBR material, UV, texture and surface-look development skill for game and interactive 3D assets, including texel density, channel packing, normals/tangents, roughness/metalness, material reuse, atlasing and visual/performance verification.

license: MIT

---

# LeeWay 3D Material & Lookdev

## Surface workflow

Classify surface → inspect UVs → define texel-density target → repair/unwrap → select PBR model → author/bind base color, roughness, metallic/specular, normal, AO/emissive/opacity as appropriate → validate color space/tangent basis → light-test → optimize → verify.

## Wrapping/skin repair

For 'wrapping' or 'skin' requests inspect seams, stretching, overlap, island scale, orientation, padding, texture resolution, filtering, normal-map convention and visible repetition. Repair the actual failure rather than hiding it with a new texture.

## Material intelligence

Choose materials from object semantics and art direction: wood, glass, painted metal, stone, concrete, fabric, foliage, plastic, clay, etc. Preserve physically plausible response where realism is desired; stylization may deliberately alter response but remains internally consistent.

## Performance

Track material slots, shader complexity, texture dimensions/formats/mips, atlas opportunities, draw calls and VRAM. Quality target must match target hardware/platform.

## Verification

Use neutral/material-check lighting plus final scene lighting. Compare before/after and inspect close/mid/far distances.