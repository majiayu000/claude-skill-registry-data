---

name: leeway-3d-asset-lifecycle

description: 3D asset identity, version, provenance, dependency and approval lifecycle skill for source scenes, derived meshes, textures, materials, rigs, exports and engine-ready artifacts.

license: MIT

---

# LeeWay 3D Asset Lifecycle

## Identity

Assign stable asset/scene identity and distinguish SOURCE, WORKING, DERIVED, EXPORT and RUNTIME artifacts.

## Provenance

Track source/reference, generator/provider, transformations, dependencies, licenses where applicable, hashes/version identifiers and approval state.

## Change control

Before consequential edits preserve baseline identity/rollback. Do not overwrite approved source with destructive derived output unless explicitly authorized.

## Dependency graph

Textures, materials, rigs, animations, caches, linked scenes, generated meshes and exports must resolve to their owning asset/version.