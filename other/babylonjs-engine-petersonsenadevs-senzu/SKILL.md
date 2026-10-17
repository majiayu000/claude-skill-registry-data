---
name: babylonjs-engine
description: "Motor 3D Babylon.js 7: escenas WebGL/WebGPU, cámaras, luces, PBR, glTF, física Havok, sombras, GUI, WebXR, juegos en navegador. Disparadores: Babylon, @babylonjs/core, Havok. No para Three.js/R3F ni efectos 3D ligeros."
---

# babylonjs-engine (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (1233 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: el proyecto ya usa `@babylonjs/core` o pide juego/visualización 3D con física (Havok), GUI 2D integrada, WebXR o Node Material.
- Usar: cargar modelos glTF/GLB con PBR, sombras y post-procesado en un canvas propio.
- NO usar: si el proyecto usa Three.js o React Three Fiber → `threejs-webgl` / `react-three-fiber`; decoración 3D ligera (tilt, Zdog, Vanta) → `lightweight-3d-effects`.
- NO usar: escenas exportadas de Spline o PlayCanvas → `spline-interactive` / `playcanvas-engine`.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L16-84 (§1 Engine and Scene Initialization) + `assets/starter_babylon/` (Vite) |
| Cámaras, luces, materiales, cargar glTF | L85-188, L299-367, L368-424 |
| Física Havok / animaciones | L425-493 (§7 Physics), L494-569 (§8 Animations) |
| Post-procesado, GUI, sombras, partículas | L652-768 (Patterns 4-7) |
| Integrar en React / WebXR | L771-825, L826-863 |
| Depurar / rendimiento | L884-997 (§Performance), L998-1134 (§Pitfalls), L1200-1222 (§Debugging) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 8-13 | Related Skills | Alternativas (threejs, r3f, gsap, motion) |
| 16-84 | 1. Engine and Scene Initialization (§Core Concepts 14-569) | Engine, Scene, render loop, resize, setup ES6/TS |
| 85-132 | 2. Camera Systems | FreeCamera, ArcRotateCamera (órbita + límites), UniversalCamera |
| 133-188 | 3. Lighting Systems | Hemispheric, Directional, Point, Spot, includedOnlyMeshes |
| 189-298 | 4. Mesh Creation | MeshBuilder, transformaciones, propiedades |
| 299-367 | 5. Materials | StandardMaterial, PBRMaterial, MultiMaterial |
| 368-424 | 6. Model Loading | SceneLoader (Append/ImportMeshAsync), AssetsManager |
| 425-493 | 7. Physics Engine | Havok, PhysicsAggregate, shapes, fuerzas |
| 494-569 | 8. Animations | Animation, keyframes, AnimationGroup, esqueletos |
| 570-768 | Common Patterns | Entorno por defecto, carga async, picking, post-proceso, GUI, sombras, partículas |
| 769-883 | Integration Patterns | React (useEffect + dispose), WebXR, Node Material |
| 884-997 | Performance Optimization | Merge/instances/thin instances, SceneOptimizer, hardware scaling, texturas KTX2 |
| 998-1134 | Common Pitfalls | Leaks, draw calls, bloqueo del hilo, attachControl, async, física sin habilitar |
| 1135-1199 | Advanced Topics | Shaders custom, compute shaders (WebGPU), texturas procedurales |
| 1200-1233 | Debugging / Resources / Version Notes | Inspector, bounding boxes, FPS, SceneInstrumentation; enlaces; basado en Babylon.js 7.x |

## Recursos
- `references/api_reference.md` — referencia de clases, métodos y propiedades de Babylon.js 7.x.
- `scripts/scene_generator.py` — genera escena base: `py -3 scripts/scene_generator.py --type basic|physics --camera arc-rotate --typescript --output scene.js` (o `--interactive`).
- `scripts/mesh_builder.py` — genera código de mallas: `py -3 scripts/mesh_builder.py --shape sphere --params '{"size":2}' --output meshes.js`.
- `assets/starter_babylon/` — starter Vite (index.html, src/main.js, style.css, package.json); `assets/examples/README.md` — ejemplos por tema (carga, PBR, física, GUI, XR, rendimiento).

## Reglas duras
- Libera siempre recursos: `mesh.dispose()`, `scene.dispose()`, `engine.dispose()`; en React en el cleanup de `useEffect` junto al listener de resize.
- Muchas copias del mismo mesh → `createInstance` o thin instances, nunca un mesh por copia (un draw call cada uno).
- Carga de modelos y física son async: usa `ImportMeshAsync`/`await HavokPhysics()` y habilita `scene.enablePhysics` antes de crear `PhysicsAggregate`.
- Llama a `camera.attachControl(canvas, true)`; sin ello la cámara no responde.
- Solo en cliente: Babylon toca `window`/canvas; en Next.js/Astro usa componentes client-only o `dynamic(..., { ssr: false })`.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). Librería agnóstica: vanilla/Vite (usa el starter), React (patrón L771-825 con refs), Vue/Astro (mismo patrón en `onMounted`/`client:only`).
- Si package.json ya trae `three` o `@react-three/fiber`, no introduzcas Babylon: usa `threejs-webgl` / `react-three-fiber`.
