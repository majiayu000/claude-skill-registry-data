---

name: leeway-3d-geometry-topology

description: 3D mesh geometry, topology, retopology, normals and mesh-repair craft skill for reconstruction and authored assets.

license: MIT

---

# LeeWay 3D Geometry & Topology

## Inspect

Non-manifold edges, holes, duplicate/degenerate geometry, intersections, inverted/invalid normals, shading artifacts, excessive density, poor edge flow, disconnected islands and scale/transforms.

## Repair strategy

Preserve silhouette and approved dimensions first. Choose local repair, retopology, remesh or rebuild according to defect and downstream needs. Reconstruction meshes from single images require special inspection of occluded/backside surfaces.

## Game readiness

Prefer topology appropriate to deformation, shading, collision and LOD generation. Apply smoothing/normal/tangent strategy consistently with the target renderer.