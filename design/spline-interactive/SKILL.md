---
name: spline-interactive
description: "Integra escenas Spline (editor 3D visual sin código) en React/Next.js: @splinetool/react-spline, eventos onSpline*, emitEvent, findObjectByName, lazy load, SSR. No para 3D por código (threejs-webgl, react-three-fiber) ni juegos."
---

# spline-interactive (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (756 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: embeber una escena `.splinecode` diseñada en Spline en React/Next.js (hero 3D, configurador, showcase de producto).
- Usar: reaccionar a clics/hover sobre objetos Spline, disparar animaciones por estados desde código (`emitEvent`) o mover objetos (`findObjectByName`).
- Usar: exportar desde Spline a GLTF/GLB para reutilizar en Three.js.
- NO usar: escenas 3D construidas por código o con control total del render → threejs-webgl / react-three-fiber; juegos con físicas → babylonjs-engine.
- NO usar: animación DOM general o de UI → gsap-scrolltrigger / motion-framer.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L79-105 (§Pattern 1) + `scripts/project_generator.py` |
| Eventos y control de objetos desde React | L107-280 (§Pattern 2-4) + `references/api_reference.md` |
| Next.js / SSR / hidratación | L282-306 (§Pattern 5) + L686-705 (§Pitfall 6) |
| Scroll o UI animada alrededor de la escena | L444-502 (§With GSAP, §With Framer Motion) |
| Depurar / rendimiento | L504-566 (§Performance Optimization) + L568-705 (§Common Pitfalls) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 8-33 | Overview | Qué es Spline, cuándo usarlo y alternativas |
| 34-76 | Core Concepts | Escena, componentes, estados, eventos, opciones de exportación |
| 77-105 | Pattern 1: Basic React Integration | Instalación y componente `<Spline scene=...>` |
| 107-155 | Pattern 2: Event Handling and Object Interaction | Props `onSplineMouseDown/Hover/...` y lista completa de handlers |
| 156-225 | Pattern 3: Programmatic Object Control | `onLoad`, `findObjectByName/ById`, position/rotation/scale/material |
| 226-281 | Pattern 4: Triggering Spline Animations | `emitEvent` / `emitEventReverse` y tipos de evento |
| 282-307 | Pattern 5: Next.js Integration with SSR | Import `@splinetool/react-spline/next` |
| 308-341 | Pattern 6: Lazy Loading for Performance | `React.lazy` + `Suspense` |
| 342-423 | Pattern 7: Responsive Spline Scenes | Escena móvil alternativa o `setZoom` + cámara |
| 424-503 | Integration Patterns | GLTF a Three.js, ScrollTrigger con `emitEvent`, contenedor con Motion |
| 504-567 | Performance Optimization | `renderOnDemand`, optimizar en editor, prefetch, móvil |
| 568-706 | Common Pitfalls and Solutions | Escena no carga, refs perdidas, eventos, hidratación Next.js |
| 707-739 | Resources / Related Skills | Enlaces oficiales, formatos de exportación, skills relacionadas |
| 740-756 | Scripts / Assets | Descripción de scripts y assets del paquete |

## Recursos
- `references/api_reference.md` — API del runtime y del componente React (props, eventos, métodos de la app y objetos).
- `scripts/project_generator.py` — genera un proyecto React (o Next.js con `--nextjs`) con Spline: `py -3 scripts/project_generator.py --name mi-app` (`python3` en Linux/macOS).
- `scripts/component_builder.py` — genera wrappers de componente Spline con eventos: `py -3 scripts/component_builder.py --name ProductViewer`.
- `assets/README.md` — explica el uso del generador; no hay carpeta `starter_spline/` real pese a lo que dice el upstream.

## Reglas duras
- La prop `scene` debe ser la URL completa de exportación (`https://prod.spline.design/.../scene.splinecode`) y la escena debe estar publicada.
- Guarda la instancia y los objetos en `useRef`; llama a `emitEvent` solo tras `onLoad` (comprueba estado `isLoaded`).
- Usa los handlers `onSpline*` (no `onMouseDown`), y configura el evento también en el panel Events del editor.
- En Next.js importa desde `@splinetool/react-spline/next` o usa `dynamic(..., { ssr: false })` para evitar errores de hidratación.
- Mantén `renderOnDemand`, carga perezosa para escenas pesadas y una versión móvil (< 50k triángulos, texturas ≤ 512, sin sombras).
- Respeta `prefers-reduced-motion`: no dispares animaciones automáticas si el usuario lo pide.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). `@splinetool/react-spline` es solo React/Next.js; en Vue, Astro o vanilla usa `@splinetool/runtime` directamente (`new Application(canvas).load(url)`) o el Spline Viewer embebido, con la misma API de objetos y eventos.
