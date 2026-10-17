---
name: aframe-webxr
description: "Escenas 3D/VR/AR declarativas en HTML con A-Frame (ECS sobre Three.js): WebXR, controladores VR, AR hit-test, visores 360, componentes custom. No para control fino de Three.js (threejs-webgl) ni para React (react-three-fiber)."
---

# aframe-webxr (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (1076 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: experiencias VR/AR en navegador (WebXR) con poco JavaScript, prototipos 3D con primitivas HTML (`<a-box>`, `<a-sky>`).
- Usar: visores de foto/vídeo 360, interacción con controladores/gaze/cursor, colocar objetos en AR con hit-test.
- NO usar: cuando necesitas control imperativo del renderer, shaders o postprocesado → `threejs-webgl`; escena 3D dentro de un árbol React → `react-three-fiber`.
- NO usar: motor de juego completo con física/editor → `babylonjs-engine` o `playcanvas-engine`.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L17-78 (§Core Concepts: ECS y Scene Setup) + `assets/starter_aframe/` |
| Controladores VR / agarrar objetos | L277-341 (§Pattern 1) + `references/webxr_guide.md` |
| AR con hit-test | L403-457 (§Pattern 3) + `references/webxr_guide.md` |
| Galería 360 / skybox / modelos GLTF | L342-402, L576-671 (§Pattern 2, 6, 7) |
| Componente custom / interacción click-gaze | L242-274 (§8) + L458-506 (§Pattern 4) o `scripts/component_builder.py` |
| Integrar con Three.js / GSAP / React | L672-770 (§Integration Patterns) |
| Depurar / rendimiento | L771-893 (§Performance) + L894-1061 (§Pitfalls) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 8-16 | When to Use This Skill | Casos de uso listados por el autor |
| 17-274 | Core Concepts | ECS (19), escena (51), cámaras/rig (79), luces (125), materiales (151), animación (178), assets (211), componentes custom (242) |
| 275-671 | Common Patterns | Controladores VR (277), galería 360 (342), AR hit-test (403), mouse/gaze (458), escena dinámica (507), entorno/skybox (576), GLTF (619) |
| 672-770 | Integration Patterns | Acceso a Three.js (674), GSAP (697), React con `useEffect` (731) |
| 771-893 | Performance Best Practices | `<a-assets>`, pooling, low-poly, draw calls, throttle `tick()`, `stats` |
| 894-1061 | Common Pitfalls and Solutions | Entidad invisible, eventos sin raycaster, FPS, z-fighting, VR móvil, CORS/carga |
| 1062-1076 | Resources / Related Skills | Enlaces oficiales y skills relacionadas |

## Recursos
- `references/api_reference.md` — API A-Frame 1.7: escena, entidad, componentes core, primitivas, sistemas.
- `references/components_library.md` — componentes de la comunidad (environment, physics, locomoción, loaders, UI).
- `references/webxr_guide.md` — configuración VR/AR, controladores, hand tracking, hit testing.
- `scripts/scene_generator.py` — genera escena basic/vr/ar/360/networked: `py -3 scripts/scene_generator.py vr MiProyecto` (Linux/mac: `python3 …`).
- `scripts/component_builder.py` — boilerplate de componente basic/interactive/animation/physics/networked: `py -3 scripts/component_builder.py interactive mi-comp`.
- `assets/starter_aframe/` — index.html + main.js + style.css listos; `assets/examples/README.md` — patrones avanzados (two-handed grab, networking, física).

## Reglas duras
- Precarga todo en `<a-assets>` y espera al evento `loaded` de la escena antes de añadir entidades dinámicamente; añade `crossorigin="anonymous"` en recursos externos.
- Nada de crear/destruir entidades por frame: usa pooling; throttlea `tick()` y limita luces (máx. ambient + directional en móvil).
- Interacción requiere raycaster: `<a-cursor raycaster="objects: .interactive">` y clase en los objetivos; sin ello no llegan `click`/`mouseenter`.
- En VR móvil limita `renderer="maxCanvasWidth: 1920; maxCanvasHeight: 1920"`, usa low-poly y valora `antialias: false`.
- Ofrece siempre fallback no-XR (desktop/móvil con look-controls) y respeta `prefers-reduced-motion` desactivando `animation__*` en bucle.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). A-Frame es vanilla/HTML-first: en Vue o Astro funciona con el script CDN o `import 'aframe'` solo en cliente (no SSR).
- En React usa `useEffect` + refs (L731-770) y registra componentes antes de montar `<a-scene>`; si el proyecto ya es React+Three, prefiere `react-three-fiber`.
