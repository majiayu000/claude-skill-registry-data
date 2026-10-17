---
name: playcanvas-engine
description: "Motor WebGL/WebGPU PlayCanvas: juegos 3D en navegador, ECS, scripts pc.createScript, física Ammo.js, carga glTF, export del Editor. No para 3D low-level (threejs-webgl), R3F (react-three-fiber) ni VR declarativo (aframe-webxr)."
---

# playcanvas-engine (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (1062 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: juegos o apps 3D en navegador con arquitectura ECS (entidades + componentes model/camera/light/rigidbody).
- Usar: proyectos que parten del PlayCanvas Editor (export, `config.json`, `loadSceneHierarchy`) o necesitan física Ammo.js, input de teclado/ratón/touch y animación esquelética.
- Usar: experiencias 3D críticas en rendimiento donde Three.js requiere demasiado boilerplate.
- NO usar: control WebGL de bajo nivel o escenas 3D "de web" (landing, producto) → `threejs-webgl`; React declarativo → `react-three-fiber`.
- NO usar: simulaciones físicas pesadas o editor más completo → `babylonjs-engine`; VR/AR declarativo en HTML → `aframe-webxr`.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L30-167 (§Core Concepts) + L171-230 (§Pattern 1) + `assets/starter_playcanvas/` |
| Cargar modelos glTF y materiales PBR | L232-346 (§Pattern 2 y 3) |
| Física, scripts propios e input | L348-560 (§Pattern 4, 5 y 6) |
| Animación esquelética y tweens | L562-628 (§Pattern 7) |
| Integrar en React o cargar export del Editor | L630-730 (§Integration Patterns) |
| Depurar / rendimiento | L732-850 (§Performance Optimization) + L852-1014 (§Common Pitfalls) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 10-28 | When to Use This Skill | Disparadores y comparación con Three.js, Babylon.js y A-Frame |
| 30-167 | Core Concepts | Application, ECS, bucle `update(dt)` y componentes básicos |
| 169-628 | Common Patterns | Escena base, glTF, materiales, física, scripts, input, animación |
| 416-498 | Pattern 5: Custom Scripts | `pc.createScript`, atributos de editor y ciclo de vida |
| 630-730 | Integration Patterns | Wrapper React con `useEffect`/`app.destroy()` y export del Editor |
| 732-850 | Performance Optimization | Object pooling, LOD manual, batching, texturas comprimidas |
| 852-1014 | Common Pitfalls | Olvidar `app.start()`, mutar en update, fugas de assets, jerarquía, Ammo, canvas |
| 1016-1025 | Resources | Enlaces oficiales (API, docs, ejemplos, foro) |
| 1027-1060 | Quick Reference | Snippets mínimos: app, entidad, update, assets |

## Recursos
- `references/api_reference.md` — Referencia de la API de PlayCanvas (clases, componentes, constantes).
- `references/editor_workflow.md` — Flujo de trabajo con el Editor online y su exportación a código.
- `references/optimization_guide.md` — Guía de optimización ampliada (draw calls, memoria, móviles).
- `scripts/project_generator.py` — Genera un HTML de proyecto por tipo: `py -3 scripts/project_generator.py --list` / `--type <tipo> --output out.html` (o `python3`).
- `scripts/component_builder.py` — Genera scripts de componente (basic, interactive, animation, physics, character, camera, ui): `py -3 scripts/component_builder.py -n Nombre -t tipo -o ./scripts/`.
- `assets/starter_playcanvas/` — Starter con `index.html`, `styles.css` y carpeta `scripts/`; `assets/examples/README.md` — índice de ejemplos.

## Reglas duras
- Llama siempre a `app.start()` tras crear la escena; sin él no hay bucle de render.
- Canvas responsivo: `setCanvasFillMode(FILLMODE_FILL_WINDOW)`, `setCanvasResolution(RESOLUTION_AUTO)` y `app.resizeCanvas()` en `resize`.
- Nunca destruyas entidades dentro del `update`: márcalas y elimínalas en `postUpdate`.
- Limpia assets (`app.assets.remove` + `asset.unload()`) y llama a `app.destroy()` al desmontar (React `useEffect` cleanup).
- Carga Ammo.js antes de añadir `rigidbody`/`collision`; en bucles de spawn usa pooling en lugar de crear/destruir.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). Librería vanilla (`import * as pc from 'playcanvas'`), válida en React (patrón L632-690), Vue o Astro con `client:only`; el canvas requiere `window`, así que inicializa solo en cliente (SSR-safe).
