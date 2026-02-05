---
name: vue-threejs-skilltree
description: Build Vue 3 components that render a 3D skill tree using Three.js and OrbitControls. Use when asked to visualize skills as an interactive 3D constellation or to turn skills/INDEX.json into a Vue scene.
---

# Vue Three.js Skilltree

Build a Vue 3 single-file component that renders a 3D skill tree.

## Workflow

1) Load `skills/INDEX.json` and sanitize names/descriptions for display.
2) Map skills into a radial or spherical layout.
3) Render nodes and labels in a Three.js scene with OrbitControls.
4) Add hover or click interactions for humanized descriptions.
5) Keep the camera and renderer responsive to resize.

## Scripts

- Run: python skills/interface/vue-threejs-skilltree/scripts/generate_component.py --output runs/SkillTree3D.vue

## References

- references/scene_defaults.json
