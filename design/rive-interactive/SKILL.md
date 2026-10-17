---
name: rive-interactive
description: "Animaciones Rive (.riv) con máquinas de estados, inputs (boolean/number/trigger), ViewModel data binding y eventos en React (rive-react): botones, toggles, loaders, UI interactiva. No para timelines simples (usa lottie-animations)."
---

# rive-interactive (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (586 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: componentes animados con lógica de estados (hover/pressed/loading) controlados desde código mediante inputs de state machine.
- Usar: enlazar datos de la app (texto, números, colores, enums) a la animación con ViewModels, o reaccionar a eventos emitidos desde Rive.
- Usar: integrar un archivo `.riv` entregado por diseño en React, con precarga y control por refs.
- NO usar: animaciones de timeline sin interactividad (loaders simples, iconos) → lottie-animations.
- NO usar: animación de layout/gestos en React → motion-framer; scroll → gsap-scrolltrigger; 3D → spline-interactive.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L34-101 (§Core Concepts + Pattern 1) + `assets/README.md` |
| Controlar estados con inputs (hover, click, progreso) | L102-150 (§Pattern 2) |
| Data binding con ViewModels | L151-213 (§Pattern 3) + L343-381 (§Pattern 7) + `references/api_reference.md` |
| Eventos desde la animación / control por refs / precarga | L214-342 (§Pattern 4, 5, 6) |
| Combinar con Framer Motion o ScrollTrigger | L382-448 (§Integration Patterns) |
| Depurar / rendimiento | L449-483 (§Performance Optimization) + L484-546 (§Common Pitfalls and Solutions) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 8-33 | Overview | Qué aporta Rive frente a Lottie/Framer/GSAP y cuándo usarlo |
| 34-66 | Core Concepts | State Machines (36), Inputs (44), ViewModels (51), Events (61) |
| 67-381 | Common Patterns | Básico (69), inputs (102), ViewModel (151), eventos (214), precarga useRiveFile (262), refs/useImperativeHandle (294), multi-propiedad (343) |
| 382-448 | Integration Patterns | Con Framer Motion (384) y con GSAP ScrollTrigger (409) |
| 449-483 | Performance Optimization | useOffscreenRenderer, optimizar .riv, precarga, automaticallyHandleEvents |
| 484-546 | Common Pitfalls and Solutions | Input null (486), ViewModel no actualiza por autoBind (504), eventos no disparan (525) |
| 547-569 | Resources / Related Skills | Docs oficiales, editor, tutoriales y skills relacionadas |
| 570-586 | Scripts / Assets | Índice de scripts y assets (nota: `starter_rive/` y `examples/` no existen en esta copia) |

## Recursos
- `references/api_reference.md` — API de rive-react: useRive, useStateMachineInput, hooks de ViewModel, eventos, layout y props.
- `scripts/component_generator.py` — Imprime una plantilla de componente Rive React (modo interactivo): `py -3 scripts/component_generator.py`.
- `scripts/viewmodel_builder.py` — Imprime plantilla de bindings de ViewModel (modo interactivo): `py -3 scripts/viewmodel_builder.py`.
- `assets/README.md` — Quick start y ejemplos de uso básico con `rive-react` (único asset presente).

## Reglas duras
- Los nombres de state machine e inputs deben coincidir exactamente con el editor Rive; comprueba `if (input)` antes de usarlos (pueden ser null hasta cargar).
- Para ViewModels manuales usa `autoBind: false` en `useRive`; para recibir eventos, `automaticallyHandleEvents: true` y limpia con `rive.off(...)` en el cleanup.
- Colores de ViewModel como número (`parseInt(hex.substring(1), 16)`), no string.
- Rendimiento: `useOffscreenRenderer`, precarga con `useRiveFile`, artboards < 2 MB, vectores en vez de raster, pocos huesos y state machines simples.
- Respeta `prefers-reduced-motion`: pausa o muestra estado final estático (norma del proyecto, no del upstream).

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json).
- El upstream es solo React (`rive-react`). Para Vue, Astro o vanilla usa `@rive-app/canvas` (mismos conceptos: `new Rive({ src, stateMachines, autoplay })`, `stateMachineInputs()`), siempre solo en cliente (SSR-safe: `useEffect` / `client:only`).
