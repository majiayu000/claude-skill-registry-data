---
name: web3d-integration-patterns
description: "Meta-skill de arquitectura para combinar Three.js, GSAP ScrollTrigger, React Three Fiber, Motion y React Spring: capas, estado (Zustand), render bajo demanda, conflictos entre librerías. No para la API de una sola librería (usa su skill)."
---

# web3d-integration-patterns (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (852 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: decidir qué combinación de librerías 3D + animación usar para una experiencia concreta (matriz de decisión).
- Usar: diseñar la arquitectura de una app que mezcla Three.js/R3F con GSAP, Motion o React Spring y compartir estado entre escena 3D y UI.
- Usar: resolver conflictos de animación, fugas de memoria o renders innecesarios en stacks multi-librería.
- NO usar: dudas de API de una sola librería → threejs-webgl, gsap-scrolltrigger, react-three-fiber, motion-framer, react-spring-physics.
- NO usar: escenas visuales sin código → spline-interactive; motores de juego → babylonjs-engine / playcanvas-engine.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L792-806 (§Decision Matrix) y luego el patrón elegido (L30-427) |
| Landing con 3D dirigido por scroll (vanilla + GSAP) | L30-208 (§Pattern 1) + L431-501 (§1. Scroll-Driven Camera Movement) |
| App React con 3D declarativo y gestos | L210-327 (§Pattern 2) + L503-528 (§2. Gesture-Driven) |
| Estado compartido escena/UI | L530-598 (§3. State-Synchronized) + L601-653 (§State Management Strategies) |
| Depurar / rendimiento | L655-724 (§Performance Optimization) + L726-790 (§Common Pitfalls) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 8-27 | Overview | Cuándo aplica y las 5 combinaciones de librerías cubiertas |
| 30-208 | Pattern 1: Layered Separation (Three.js + GSAP + React UI) | Capas 3D / animación / UI, código completo de escena y ScrollTrigger |
| 210-327 | Pattern 2: Unified React Component (React Three Fiber + Motion) | Canvas R3F + `framer-motion-3d` para 3D declarativo |
| 329-376 | Pattern 3: Hybrid Approach (R3F + GSAP Timelines) | Timelines GSAP sobre refs de R3F con limpieza en `useEffect` |
| 378-427 | Pattern 4: Physics-Based 3D (R3F + React Spring) | `@react-spring/three`, `useSpring` + `animated('mesh')` |
| 429-598 | Common Integration Patterns | Cámara por scroll (GSAP y Drei `ScrollControls`), drag con Motion 3D, Zustand + GSAP |
| 601-653 | State Management Strategies | Store Zustand global para cámara, objetos y selección |
| 655-724 | Performance Optimization | Render condicional en bucle propio; `frameloop="demand"` + `invalidate()` en R3F |
| 726-790 | Common Pitfalls | Conflictos de animación, desincronización de estado, fugas por tweens sin `kill()` |
| 792-806 | Decision Matrix | Tabla caso de uso → stack recomendado |
| 808-852 | Resources / Related Skills | Recursos anunciados (no incluidos) y skills base a las que remitir |

## Recursos
- Sin recursos adicionales; todo está en `SKILL.upstream.md`. Los `references/`, `scripts/` y `assets/` que menciona L808-824 NO existen en el paquete instalado.

## Reglas duras
- Una sola librería por propiedad animada: nunca GSAP y React Spring (o Motion) sobre el mismo `position`/`scale`.
- Toda animación creada en `useEffect` se limpia en el return (`tween.kill()`, `tl.kill()`, `ScrollTrigger.kill()`); dispón la escena Three.js al desmontar.
- Render bajo demanda: `frameloop="demand"` + `invalidate()` en R3F, o bandera `needsRender` en bucle propio; `dpr` limitado a `[1, 2]`.
- Estado compartido escena/UI en un store (Zustand) o refs, nunca mutar Three.js sin reflejarlo en React cuando la UI depende de ello.
- Respeta `prefers-reduced-motion`: desactiva scrubs y animaciones automáticas de cámara si el usuario lo pide.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). Los patrones 2-4 requieren React (R3F, Motion 3D, React Spring); en vanilla, Vue o Astro usa el patrón 1 (Three.js + GSAP con capa UI del framework) y remite a threejs-webgl y gsap-scrolltrigger.
