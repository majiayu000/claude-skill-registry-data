---
name: react-spring-physics
description: "Física de muelles en React con @react-spring/web (useSpring, useTrail, useTransition, useScroll, useInView) y Popmotion (inertia). Gestos, drag con momentum, listas enter/exit. Solo React; no para vanilla/Vue ni timelines."
---

# react-spring-physics (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (464 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: movimiento natural e interrumpible en React (mass/tension/friction), drag/swipe con conservación de velocidad, inercia y snap a grid.
- Usar: transiciones de listas (`useTransition`), cascadas (`useTrail`), reveal por viewport (`useInView`) o scroll (`useScroll`), animar props de react-three-fiber con `@react-spring/three`.
- NO usar: proyecto vanilla, Vue o Astro sin React → `animejs` (easing `spring(...)`) o `gsap-scrolltrigger`; coreografía por timeline/scrub → `gsap-scrolltrigger`; variantes declarativas con gestos → `motion-framer`.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L26-97 (§Core Concepts) + `assets/README.md` (Vite react + `npm i @react-spring/web`) |
| Click / hover / trail / listas | L100-176 (§1-3) o `scripts/spring_generator.py --type transition` |
| Scroll / viewport / cadenas async | L177-236 (§4-6) |
| Drag con momentum / inercia Popmotion | L237-259 (§7) + L290-312 + `references/popmotion_api.md` |
| Ajustar la sensación del muelle | L75-97 (presets) + `scripts/physics_calculator.py --feel bouncy` + `references/physics_guide.md` |
| Integrar con react-three-fiber / formularios | L262-330 (§Integration Patterns) |
| Depurar / rendimiento | L331-367 (§Performance) + L368-441 (§Common Pitfalls) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 10-25 | Overview | Cuándo usar; paquetes `@react-spring/web`, `/three`, `popmotion` |
| 26-97 | Core Concepts | Física del muelle (28), patrones de `useSpring` objeto vs función+api (50), presets `config.*` (75) |
| 98-259 | Common Patterns | Click (100), trail (131), transiciones de lista (155), scroll (177), inView (198), cadenas async (216), velocidad preservada (237) |
| 260-330 | Integration Patterns | react-three-fiber (262), Popmotion `inertia` (290), shake en validación de formulario (313) |
| 331-367 | Performance Optimization | `precision`, `useSprings` en lote, `Globals.skipAnimation` |
| 368-441 | Common Pitfalls | Deps de `useSpring`, mutar valores, precisión, velocidad, mezclar patrones, strings no numéricos |
| 442-464 | Resources / Related Skills | Scripts, referencias, física vs timeline |

## Recursos
- `references/react_spring_api.md` — hooks, `animated`, interpolación `.to()`, `api.start/stop`, eventos.
- `references/popmotion_api.md` — `spring`, `inertia`, `decay`, keyframes y streams de Popmotion.
- `references/physics_guide.md` — mass/tension/friction, amortiguación crítica, tabla de tuning.
- `scripts/spring_generator.py` — boilerplate click/scroll/trail/transition/inview/chain/gesture: `py -3 scripts/spring_generator.py --type gesture` (Linux/mac: `python3 …`).
- `scripts/physics_calculator.py` — calcula parámetros por sensación o amortiguación crítica: `py -3 scripts/physics_calculator.py --feel bouncy` / `--critical-damping --tension 170`.
- `assets/README.md` — solo instrucciones de starter con Vite y enlaces oficiales (no existe carpeta `starter_spring/` real pese al upstream).

## Reglas duras
- `useSpring(() => ({...}), [])` con array de deps y usa `api.start()`; nunca `springs.x.set()` ni recrear el spring por render.
- Anima valores numéricos individuales (`x`, `rotation`) y compón el `transform` con `.to()`; no pases strings compuestos.
- Al interrumpir una animación pasa `velocity: springs.x.getVelocity()` para no cortar el momentum.
- Fija `config.precision` (p. ej. 0.01) y agrupa con `useSprings`/`useTrail` para evitar renders innecesarios.
- Respeta `prefers-reduced-motion` con `Globals.assign({ skipAnimation: true })` (L356-367).

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). Librería **solo React** (también Next/Remix/Astro con islas React); los hooks se ejecutan en cliente y `useScroll`/`useInView` requieren `window`, así que en SSR envuélvelos en componentes client-only.
- Si el proyecto es Vue, Svelte o vanilla, no la instales: usa `animejs` (easing spring) o `gsap-scrolltrigger`; para 3D en React combina con `react-three-fiber` vía `@react-spring/three`.
