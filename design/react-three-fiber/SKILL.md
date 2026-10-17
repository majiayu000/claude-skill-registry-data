---
name: react-three-fiber
description: "3D declarativo en React con React Three Fiber + drei: Canvas, useFrame, useGLTF, Environment, ScrollControls. ÚSALA en Next.js/React para heros 3D, configuradores, escenas. No para Vue (TresJS en threejs-webgl) ni Astro sin React."
---

# react-three-fiber (capa Senzu, en español)

Skill upstream (inglés): `SKILL.upstream.md` (conceptos, 7 patrones, drei, integraciones, rendimiento, pitfalls),
`references/api_reference.md` (Canvas, hooks, eventos, drei, 928 líneas), `assets/starter_r3f/`, `assets/examples/`,
`scripts/component_generator.py`, `scripts/scene_setup.py`. Capa Senzu (español): `references/es/next.md`.
Fundamentos de Three.js, assets, shaders y rendimiento: skill `threejs-webgl` (`references/es/*`); scroll 3D con GSAP:
`threejs-webgl/references/es/gsap-three.md`.

R3F convierte Three.js en componentes: `<mesh>`, `<boxGeometry>`, `<meshStandardMaterial>` son clases de Three
instanciadas por el reconciler. Estética y presupuesto (peso, FPS, LCP) salen del `senzu/design-system/*/MASTER.md`
(skill `ui-ux-pro-max`) y del §2 de `threejs-webgl/SKILL.md`.

## 1. Cuándo sí / cuándo no
| Situación | Skill |
|---|---|
| Next.js / React / Astro con island React: escena 3D con estado, eventos, hooks | **react-three-fiber** |
| Vue 3 (SPA o Laravel + Inertia) | `threejs-webgl` → TresJS (`threejs-webgl/references/es/tresjs-vue.md`) |
| Astro sin React, vanilla, Laravel Blade | `threejs-webgl` → clase `Scene` (`threejs-webgl/references/es/vanilla-astro.md`) |
| Efecto 2D ligero (tilt, partículas CSS, distorsión de imagen) | `lightweight-3d-effects` |
| Escena exportada de Spline | `spline-interactive` (o exportar GLB y cargarlo aquí) |

## 2. Lectura mínima por tarea (`SKILL.upstream.md`)
| Tarea | Líneas |
|---|---|
| Primera escena: `<Canvas>`, objetos declarativos, luces | 33-89, 226-255, 345-377 |
| Animar por frame (`useFrame`, delta, refs) | 90-126, 279-305 |
| Acceso a cámara/gl/viewport (`useThree`) | 127-158 |
| Cargar GLB/texturas (`useLoader`, `useGLTF`, `Suspense`) | 159-223, 306-344, 546-560 |
| Click/hover en objetos | 256-278 |
| Muchas copias (instancing) y grupos | 378-472, 739-771 |
| drei: OrbitControls, Environment, Text, Html, Center/Bounds | 473-597 |
| Scroll dentro del canvas (`ScrollControls`) | 598-633 |
| GSAP, Motion, Zustand con R3F | 634-716 |
| Rendimiento: `frameloop="demand"`, culling, LOD, `PerformanceMonitor` | 717-839 |
| Errores frecuentes (setState en useFrame, dispose, objetos en render…) | 840-976 |
| Props de `<Canvas>` y eventos (`ThreeEvent`) | `references/api_reference.md` 17-115, 450-562 |
| Helpers de rendimiento drei (`AdaptiveDpr`, `Preload`) | `references/api_reference.md` 875-922 |

## 3. Integración con perfiles Senzu
| Perfil | Cómo | Puntos críticos |
|---|---|---|
| Next.js App Router | `npm i three @react-three/fiber @react-three/drei` (+ `@types/three`); escena en `components/three/*.tsx` con `"use client"`; se monta con `next/dynamic(() => import(...), { ssr: false, loading })` desde un Client Component | `Suspense` con fallback accesible; `useGLTF.preload('/models/x.glb')`; modelos en `public/models/` optimizados con `gltf-transform`; texto y CTA en HTML encima del canvas. Detalle: `references/es/next.md`. |
| Astro + island React | Componente R3F con `client:visible` o `client:only="react"` | Un solo React runtime; View Transitions desmontan → dispose automático de R3F. |
| Vue / Inertia | No aplica | `threejs-webgl/references/es/tresjs-vue.md` (misma filosofía declarativa con TresJS + cientos). |
| GSAP / Motion | `useGSAP` sobre refs de Three (`ref.current.rotation`) o `useMotionValue` leído en `useFrame` | Nunca dos sistemas animando la misma propiedad. |

## 4. Reglas duras
- R3F **dispone automáticamente** geometrías/materiales al desmontar el JSX; lo creado a mano (`new THREE.*` en
  `useMemo`, render targets, texturas de `useLoader` compartidas) se libera en el cleanup del efecto o con `dispose={null}` si es intencional.
- Nada de DOM ni `setState` dentro de `useFrame`: muta refs; el estado React solo para cambios discretos (upstream 842-861).
- No crear objetos ni vectores en el render: `useMemo` / refs reutilizados (upstream 862-879).
- `dpr={[1, 2]}` siempre (1,5 máximo en móvil si baja el FPS; `AdaptiveDpr` de drei para degradar solo).
- `frameloop="demand"` + `invalidate()` cuando la escena es estática o solo cambia por interacción (configuradores,
  visores); `"always"` solo con animación continua; pausar fuera del viewport (`useInView` / `IntersectionObserver`).
- Fallback obligatorio: sin WebGL → imagen/vídeo estático que mantiene el LCP; `prefers-reduced-motion` → escena
  quieta sin autorotación; `webglcontextlost` gestionado.
- Un solo `<Canvas>` por página (varias vistas → drei `View`). Sin `Stats`, Leva ni `r3f-perf` en producción.
- Color y tono: `gl={{ toneMapping: ACESFilmicToneMapping, outputColorSpace: SRGBColorSpace }}`; texturas de color
  con `colorSpace = SRGBColorSpace`, resto lineal. Hero ≤ 2 MB, texturas ≤ 2048 px, < 100 draw calls en móvil.

## 5. Decisiones rápidas
| Necesidad | Solución |
|---|---|
| Hero con modelo que sigue al ratón | `useGLTF` + `useFrame` con lerp hacia `state.pointer`; `Environment preset` + `ContactShadows` |
| Configurador de producto | Estado en Zustand; `material.color.set()` en efecto; `frameloop="demand"` + `invalidate()` |
| Galería/carrusel 3D con scroll | `ScrollControls` + `useScroll` de drei si el scroll vive en el canvas; GSAP ScrollTrigger si es scroll de página |
| Miles de partículas/objetos | `<instancedMesh>` + `Object3D` temporal para matrices, o `Points` + shader |
| Texto 3D | drei `Text` (SDF, ligero) o `Text3D` solo con fuente JSON optimizada |
| Etiquetas HTML ancladas | drei `Html` con `occlude` y `distanceFactor` |
| Glow/bloom | `@react-three/postprocessing` `EffectComposer` + `Bloom`; desactivar en móvil |
| Cargar mientras se muestra placeholder | `Suspense` + drei `useProgress` en overlay accesible (`role="status"`) |

## 6. Salida esperada
Antes del código: objetivo, presupuesto (peso/FPS), cómo se monta en Next (dynamic/Suspense), fallback y limpieza.
Después: código + pasos de optimización del asset + verificación (FPS ≥ 50 en móvil medio, memoria estable, consola limpia).
